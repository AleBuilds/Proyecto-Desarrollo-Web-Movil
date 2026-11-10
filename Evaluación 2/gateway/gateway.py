"""API Gateway (:8000) - Plataforma Comercial El Mediterráneo (Caso 22).
Punto único de entrada público al backend.
Valida sesión en cookies HttpOnly, verifica permisos RBAC, enruta peticiones
a microservicios privados (Inventory, Orders, Clients, Payments, GraphQL) e
inyecta el secreto interno de servicio X-Internal-Secret.
"""
import logging
import os
import re
import time
import uuid
from collections import defaultdict, deque
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

AUTH_URL = os.getenv("AUTH_URL", "http://127.0.0.1:8100")
INVENTORY_URL = os.getenv("INVENTORY_URL", "http://127.0.0.1:9001")
ORDERS_URL = os.getenv("ORDERS_URL", "http://127.0.0.1:9002")
CLIENTS_URL = os.getenv("CLIENTS_URL", "http://127.0.0.1:9003")
PAYMENTS_URL = os.getenv("PAYMENTS_URL", "http://127.0.0.1:9004")
GRAPHQL_URL = os.getenv("GRAPHQL_URL", "http://127.0.0.1:8050")

INTERNAL_SERVICE_SECRET = os.environ["INTERNAL_SERVICE_SECRET"]
AUTH_INTROSPECTION_SECRET = os.environ["AUTH_INTROSPECTION_SECRET"]

COOKIE_NAME = "session_token"
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
TIMEOUT_DOWNSTREAM = 8.0

# Límites de solicitudes por IP y por minuto (ventana deslizante en memoria).
RATE_LIMIT_GENERAL_POR_MIN = int(os.getenv("RATE_LIMIT_GENERAL_POR_MIN", "120"))
RATE_LIMIT_LOGIN_POR_MIN = int(os.getenv("RATE_LIMIT_LOGIN_POR_MIN", "5"))
_VENTANA_SEG = 60.0
_solicitudes: dict[tuple[str, str], deque] = defaultdict(deque)

# Registros con identificador de correlación; nunca se registran cuerpo, query string ni cookies.
logger = logging.getLogger("gateway")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(_h)
logger.setLevel(logging.INFO)
_RID_VALIDO = re.compile(r"[A-Za-z0-9-]{8,64}")

CSP = (
    "default-src 'self'; "
    "img-src 'self' https://images.pexels.com https://images.unsplash.com data:; "
    "script-src 'self' https://cdn.jsdelivr.net; "
    "style-src 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'unsafe-inline'; "
    "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com"
)

STATIC_DIR = Path(__file__).parent / "static"
SITE_DIR = STATIC_DIR / "site"

app = FastAPI(title="API Gateway - El Mediterráneo")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def _excede_limite(ip: str, cubo: str, maximo: int) -> int:
    """Devuelve 0 si la solicitud cabe en el límite; si no, los segundos a esperar."""
    ahora = time.monotonic()
    ventana = _solicitudes[(ip, cubo)]
    while ventana and ahora - ventana[0] > _VENTANA_SEG:
        ventana.popleft()
    if len(ventana) >= maximo:
        return max(1, int(_VENTANA_SEG - (ahora - ventana[0])) + 1)
    ventana.append(ahora)
    return 0


@app.middleware("http")
async def correlacion_y_limites(request: Request, call_next):
    rid = request.headers.get("X-Request-ID", "")
    request.state.request_id = rid if _RID_VALIDO.fullmatch(rid) else uuid.uuid4().hex
    inicio = time.monotonic()
    ip = request.client.host if request.client else "desconocida"
    ruta = request.url.path

    espera = 0
    if not ruta.startswith("/static") and ruta != "/health":
        if ruta in ("/auth/login", "/auth/register", "/public/contact") and request.method == "POST":
            # Contadores separados: equivocarse al registrarse no bloquea el inicio de sesión
            espera = _excede_limite(ip, ruta, RATE_LIMIT_LOGIN_POR_MIN)
        if not espera:
            espera = _excede_limite(ip, "general", RATE_LIMIT_GENERAL_POR_MIN)

    if espera:
        response = JSONResponse({"detail": "Demasiadas solicitudes, intente más tarde"}, status_code=429,
                                headers={"Retry-After": str(espera)})
    else:
        response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    logger.info("rid=%s ip=%s %s %s -> %s %.0fms", request.state.request_id, ip, request.method, ruta,
                response.status_code, (time.monotonic() - inicio) * 1000)
    return response

# Matriz de permisos RBAC: (Método, Primer segmento de ruta)
PERMISOS_POR_ROL: dict[str, set[tuple[str, str]]] = {
    "user": {
        ("GET", "products"),
        ("GET", "orders"),
        ("POST", "orders"),
        ("GET", "reservations"),
        ("POST", "reservations"),
        ("GET", "clients"),
        ("PUT", "clients"),
    },
    "admin": {
        ("GET", "products"),
        ("POST", "products"),
        ("DELETE", "products"),
        ("GET", "orders"),
        ("POST", "orders"),
        ("PATCH", "orders"),
        ("GET", "reservations"),
        ("POST", "reservations"),
        ("GET", "clients"),
        ("PUT", "clients"),
        ("GET", "contact"),
    },
}


def autorizar_rbac(roles: list[str], path: str, method: str) -> None:
    recurso = path.strip("/").split("/")[0]
    permitido = False
    for rol in roles:
        if (method, recurso) in PERMISOS_POR_ROL.get(rol, set()):
            permitido = True
            break
    if not permitido:
        raise HTTPException(
            status_code=403,
            detail=f"Permiso denegado: rol(es) {roles} no autorizados para {method} en /{recurso}",
        )


async def introspect_session(token: str) -> dict | None:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
            resp = await client.post(
                f"{AUTH_URL}/introspect",
                json={"token": token},
                headers={"X-Introspection-Secret": AUTH_INTROSPECTION_SECRET},
            )
            if resp.status_code == 200:
                data = resp.json()
                return data if data.get("active") else None
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Servicio de autenticación no disponible")
    return None


async def get_current_identity(request: Request) -> dict:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        # Permitir fallback en cabecera Authorization para pruebas automatizadas
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
    if not token:
        raise HTTPException(status_code=401, detail="Sesión requerida: inicie sesión")

    identidad = await introspect_session(token)
    if not identidad:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")
    return identidad


def resolver_destino_microservicio(path: str) -> tuple[str, str]:
    """Mapea la ruta de la API al microservicio privado correspondiente."""
    partes = path.strip("/").split("/", 1)
    recurso = partes[0]
    resto = partes[1] if len(partes) > 1 else ""

    if recurso == "products":
        return INVENTORY_URL, f"products/{resto}" if resto else "products"
    elif recurso in ("orders", "reservations"):
        return ORDERS_URL, path.strip("/")
    elif recurso in ("clients", "contact"):
        return CLIENTS_URL, path.strip("/")
    elif recurso == "payments":
        return PAYMENTS_URL, f"payments/{resto}" if resto else "payments"
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado en el Gateway")


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class RegistroIn(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
    nombre_completo: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=120, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    telefono: str = Field(default="", max_length=25)


@app.get("/health")
def health():
    return {"status": "ok", "servicio": "api_gateway"}


def _html_response(ruta: Path) -> HTMLResponse:
    if not ruta.is_file():
        raise HTTPException(status_code=404, detail="Archivo HTML no encontrado")
    return HTMLResponse(
        ruta.read_text(encoding="utf-8"),
        headers={"Content-Security-Policy": CSP, "Cache-Control": "no-store"},
    )


@app.get("/", response_class=HTMLResponse)
async def index():
    inicio = SITE_DIR / "index.html"
    return _html_response(inicio if inicio.is_file() else STATIC_DIR / "index.html")


@app.get("/panel", response_class=HTMLResponse)
async def panel():
    return _html_response(STATIC_DIR / "index.html")


@app.get("/{pagina}.html", response_class=HTMLResponse)
async def pagina_sitio(pagina: str):
    if not re.fullmatch(r"[a-z-]+", pagina):
        raise HTTPException(status_code=404, detail="Ruta no permitida")
    archivo = SITE_DIR / f"{pagina}.html"
    return _html_response(archivo)


@app.post("/auth/login")
async def login(datos: LoginIn, response: Response):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
            r = await client.post(f"{AUTH_URL}/login", json=datos.model_dump())
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Servicio de autenticación no disponible")

    if r.status_code == 401:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    if r.status_code != 200:
        raise HTTPException(status_code=503, detail="Error en servicio de autenticación")

    resultado = r.json()
    token = resultado["access_token"]
    max_age = resultado.get("expires_in", 900)

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
        path="/",
    )
    return {
        "status": "ok",
        "username": resultado["username"],
        "roles": resultado["roles"],
        "expires_in": max_age,
    }


@app.post("/auth/register", status_code=201)
async def register(datos: RegistroIn, request: Request):
    """Registro público: identidad en auth_service + perfil en clients. El rol lo decide el servidor (`user`)."""
    rid = {"X-Request-ID": request.state.request_id}
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
            r = await client.post(
                f"{AUTH_URL}/register",
                json={"username": datos.username, "password": datos.password},
                headers={"X-Introspection-Secret": AUTH_INTROSPECTION_SECRET, **rid},
            )
            if r.status_code == 409:
                raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
            if r.status_code == 422:
                raise HTTPException(status_code=422, detail="Contraseña no válida")
            if r.status_code != 201:
                raise HTTPException(status_code=503, detail="No se pudo completar el registro")
            identidad = r.json()
            rp = await client.post(
                f"{CLIENTS_URL}/clients",
                json=datos.model_dump(include={"nombre_completo", "email", "telefono"}),
                headers={
                    "X-Internal-Secret": INTERNAL_SERVICE_SECRET,
                    "X-Authenticated-User": identidad["user_id"],
                    "X-Authenticated-Username": identidad["username"],
                    **rid,
                },
            )
            if rp.status_code != 201:
                # Compensación: no dejar una identidad sin perfil
                await client.delete(
                    f"{AUTH_URL}/identities/{identidad['user_id']}",
                    headers={"X-Introspection-Secret": AUTH_INTROSPECTION_SECRET, **rid},
                )
                raise HTTPException(status_code=503, detail="No se pudo completar el registro")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Servicio no disponible, intente más tarde")
    return {"status": "registrado", "username": identidad["username"]}


class ContactoIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=120, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    mensaje: str = Field(min_length=5, max_length=1000)


@app.post("/public/contact", status_code=201)
async def contacto(datos: ContactoIn, request: Request):
    """Ruta pública (REQ-08): valida y limita por IP; clients es el custodio del dato."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
            r = await client.post(
                f"{CLIENTS_URL}/contact",
                json=datos.model_dump(),
                headers={"X-Internal-Secret": INTERNAL_SERVICE_SECRET, "X-Request-ID": request.state.request_id},
            )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Servicio no disponible, intente más tarde")
    if r.status_code != 201:
        raise HTTPException(status_code=503, detail="No se pudo registrar el mensaje")
    return {"status": "recibido"}


@app.get("/auth/me")
async def auth_me(request: Request):
    identidad = await get_current_identity(request)
    return {
        "user_id": identidad["user_id"],
        "username": identidad["username"],
        "roles": identidad["roles"],
    }


@app.post("/auth/logout")
async def logout(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if token:
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
                await client.post(
                    f"{AUTH_URL}/logout",
                    json={"token": token},
                    headers={"X-Introspection-Secret": AUTH_INTROSPECTION_SECRET},
                )
        except Exception:
            pass
    resp = JSONResponse({"status": "logged_out"})
    resp.delete_cookie(COOKIE_NAME, path="/")
    return resp


@app.get("/public/menu")
async def public_menu():
    """Ruta pública sin autenticación: el Gateway consulta al microservicio Inventory con su secreto interno."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
            r = await client.get(
                f"{INVENTORY_URL}/products",
                params={"available_only": "true"},
                headers={"X-Internal-Secret": INTERNAL_SERVICE_SECRET},
            )
        return Response(content=r.content, status_code=r.status_code, media_type="application/json")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Microservicio de inventario no disponible")


@app.api_route("/graphql", methods=["GET", "POST"])
async def proxy_graphql(request: Request):
    """Enrutamiento hacia el GraphQL Gateway propagando la identidad verificada si existe."""
    headers = {"X-Internal-Secret": INTERNAL_SERVICE_SECRET, "X-Request-ID": request.state.request_id}
    token = request.cookies.get(COOKIE_NAME)
    if token:
        try:
            identidad = await introspect_session(token)
            if identidad:
                headers["X-Authenticated-User"] = identidad["user_id"]
                headers["X-Authenticated-Username"] = identidad["username"]
                headers["X-Authenticated-Roles"] = ",".join(identidad["roles"])
        except Exception:
            pass

    body = await request.body()
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
            r = await client.request(
                method=request.method,
                url=f"{GRAPHQL_URL}/graphql",
                params=list(request.query_params.multi_items()),
                content=body,
                headers={**headers, "Content-Type": request.headers.get("content-type", "application/json")},
            )
        return Response(content=r.content, status_code=r.status_code, media_type="application/json")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="GraphQL Gateway no disponible")


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_api(path: str, request: Request):
    if ".." in path.split("/"):
        raise HTTPException(status_code=400, detail="Ruta inválida no permitida")

    identidad = await get_current_identity(request)
    autorizar_rbac(identidad["roles"], path, request.method)

    base_url, endpoint = resolver_destino_microservicio(path)

    # Inyección de contexto seguro: el Gateway construye cabeceras limpias
    headers = {
        "X-Internal-Secret": INTERNAL_SERVICE_SECRET,
        "X-Authenticated-User": identidad["user_id"],
        "X-Authenticated-Username": identidad["username"],
        "X-Authenticated-Roles": ",".join(identidad["roles"]),
        "X-Request-ID": request.state.request_id,
    }
    # Si viene idempotency key en la solicitud, se propaga
    idempotency_key = request.headers.get("X-Idempotency-Key")
    if idempotency_key:
        headers["X-Idempotency-Key"] = idempotency_key

    content_type = request.headers.get("content-type")
    if content_type:
        headers["Content-Type"] = content_type

    body = await request.body()
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_DOWNSTREAM) as client:
            r = await client.request(
                method=request.method,
                url=f"{base_url}/{endpoint}",
                params=list(request.query_params.multi_items()),
                content=body,
                headers=headers,
            )
        return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("content-type"))
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Microservicio de destino no disponible")
