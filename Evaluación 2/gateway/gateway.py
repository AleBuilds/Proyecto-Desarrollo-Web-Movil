"""API Gateway (:8000) - Plataforma Comercial El Mediterráneo (Caso 22).
Punto único de entrada público al backend.
Valida sesión en cookies HttpOnly, verifica permisos RBAC, enruta peticiones
a microservicios privados (Inventory, Orders, Clients, Payments, GraphQL) e
inyecta el secreto interno de servicio X-Internal-Secret.
"""
import os
import re
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

INTERNAL_SERVICE_SECRET = os.getenv("INTERNAL_SERVICE_SECRET", "gateway-api-secret-456")
AUTH_INTROSPECTION_SECRET = os.getenv("AUTH_INTROSPECTION_SECRET", "gateway-auth-secret-789")

COOKIE_NAME = "session_token"
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
TIMEOUT_DOWNSTREAM = 8.0

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
    elif recurso == "clients":
        return CLIENTS_URL, f"clients/{resto}" if resto else "clients"
    elif recurso == "payments":
        return PAYMENTS_URL, f"payments/{resto}" if resto else "payments"
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado en el Gateway")


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


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
    headers = {"X-Internal-Secret": INTERNAL_SERVICE_SECRET}
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
