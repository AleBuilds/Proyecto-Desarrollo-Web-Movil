"""API Gateway (:8000): valida la sesión (cookie), autoriza por rol, enruta y propaga identidad."""
import os
import re
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:9000")
AUTH_URL = os.getenv("AUTH_URL", "http://127.0.0.1:8100")
COOKIE_NAME = "session_token"
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"  # true cuando se use HTTPS
VAULT_TIMEOUT = 5.0
AUTH_TIMEOUT = 5.0
BACKEND_TIMEOUT = 10.0

if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no está configurado")

# CSP estricto (sin 'unsafe-inline'): solo se agregan los hosts que necesita el diseño antiguo (Bootstrap, Font Awesome, fotos).
CSP = ("default-src 'self'; img-src 'self' https://images.pexels.com https://images.unsplash.com data:; "
       "script-src 'self' https://cdn.jsdelivr.net; "
       "style-src 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
       "font-src https://fonts.gstatic.com https://cdnjs.cloudflare.com")
STATIC_DIR = Path(__file__).parent / "static"
SITE_DIR = STATIC_DIR / "site"  # frontend antiguo convertido con construir_frontend.py
app = FastAPI(title="API Gateway")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Permisos por rol: (método, recurso). El recurso es el primer segmento de la ruta.
PERMISOS_POR_ROL: dict[str, set[tuple[str, str]]] = {
    "user": {("GET", "products"), ("GET", "orders"), ("POST", "orders"), ("GET", "reservations"), ("POST", "reservations")},
    "admin": {("GET", "products"), ("POST", "products"), ("DELETE", "products"), ("GET", "orders"), ("GET", "reservations")},
}


def autorizar(roles: list[str], path: str, method: str) -> None:
    recurso = path.split("/", 1)[0]
    if any((method, recurso) in PERMISOS_POR_ROL.get(rol, set()) for rol in roles):
        return
    raise HTTPException(status_code=403, detail="No tienes permisos para esta operación")


# ---------- llamadas a otros servicios (se aíslan para poder probarlas) ----------
async def get_gateway_secrets() -> dict:
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    try:
        async with httpx.AsyncClient(timeout=VAULT_TIMEOUT) as client:
            response = await client.get(url, headers={"X-Vault-Token": VAULT_TOKEN})
        if response.status_code != 200:
            raise ValueError(f"Vault respondió {response.status_code}")
        datos = response.json()["data"]["data"]
        if not datos.get("backend_shared_secret") or not datos.get("auth_introspection_secret"):
            raise ValueError("Faltan secretos en Vault")
        return datos
    except (httpx.RequestError, ValueError, KeyError):
        raise HTTPException(status_code=500, detail="No fue posible acceder a Vault")


async def login_upstream(username: str, password: str) -> dict:
    """Pide el token al Auth Service. Devuelve su respuesta; 401 si las credenciales son malas."""
    try:
        async with httpx.AsyncClient(timeout=AUTH_TIMEOUT) as client:
            r = await client.post(f"{AUTH_URL}/login", json={"username": username, "password": password})
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Servicio de autenticación no disponible")
    if r.status_code == 401:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    if r.status_code != 200:
        raise HTTPException(status_code=503, detail="Servicio de autenticación no disponible")
    return r.json()


async def introspect(token: str, secreto: str) -> dict | None:
    """Pregunta al Auth Service quién es el dueño del token. None si no está activo."""
    try:
        async with httpx.AsyncClient(timeout=AUTH_TIMEOUT) as client:
            r = await client.post(
                f"{AUTH_URL}/introspect", json={"token": token}, headers={"X-Introspection-Secret": secreto}
            )
        if r.status_code != 200:
            raise ValueError(f"Auth respondió {r.status_code}")
        datos = r.json()
    except (httpx.RequestError, ValueError):
        raise HTTPException(status_code=503, detail="Servicio de autenticación no disponible")
    return datos if datos.get("active") else None


async def revocar(token: str, secreto: str) -> None:
    try:
        async with httpx.AsyncClient(timeout=AUTH_TIMEOUT) as client:
            r = await client.post(
                f"{AUTH_URL}/logout", json={"token": token}, headers={"X-Introspection-Secret": secreto}
            )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Servicio de autenticación no disponible")
    if r.status_code != 200:
        raise HTTPException(status_code=503, detail="Servicio de autenticación no disponible")


async def enviar_al_backend(method: str, path: str, params: list, body: bytes, content_type: str | None, headers: dict):
    if content_type:
        headers = {**headers, "Content-Type": content_type}
    try:
        async with httpx.AsyncClient(timeout=BACKEND_TIMEOUT) as client:
            r = await client.request(method=method, url=f"{BACKEND_URL}/{path}", params=params, content=body, headers=headers)
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Backend no disponible")
    return r.status_code, r.content, r.headers.get("content-type")


async def sesion_actual(request: Request) -> tuple[dict, dict]:
    """Cookie -> introspección -> identidad. 401 si no hay sesión válida."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Sesión requerida")
    secretos = await get_gateway_secrets()
    identidad = await introspect(token, secretos["auth_introspection_secret"])
    if identidad is None:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")
    return identidad, secretos


# ---------- modelos ----------
class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


# ---------- rutas ----------
@app.get("/health")
async def health():
    return {"status": "ok", "servicio": "gateway"}


def _html(ruta: Path) -> HTMLResponse:
    return HTMLResponse(ruta.read_text(encoding="utf-8"), headers={"Content-Security-Policy": CSP, "Cache-Control": "no-store"})


@app.get("/", response_class=HTMLResponse)
async def index():
    inicio = SITE_DIR / "index.html"  # sitio antiguo; si aún no se construyó, cae al panel
    return _html(inicio if inicio.is_file() else STATIC_DIR / "index.html")


@app.get("/panel", response_class=HTMLResponse)
async def panel():
    """Login, pedidos y administración (semana 9)."""
    return _html(STATIC_DIR / "index.html")


@app.get("/{pagina}.html", response_class=HTMLResponse)
async def pagina_sitio(pagina: str):
    if not re.fullmatch(r"[a-z-]+", pagina) or not (SITE_DIR / f"{pagina}.html").is_file():
        raise HTTPException(status_code=404, detail="Página no encontrada")
    return _html(SITE_DIR / f"{pagina}.html")


@app.post("/auth/login")
async def auth_login(datos: LoginIn, response: Response):
    resultado = await login_upstream(datos.username, datos.password)
    response.set_cookie(
        key=COOKIE_NAME,
        value=resultado["access_token"],
        max_age=resultado.get("expires_in"),
        httponly=True,       # JavaScript no puede leer la cookie
        samesite="lax",
        secure=COOKIE_SECURE,
        path="/",
    )
    # El token NO va en el cuerpo: el navegador solo lo conoce como cookie HttpOnly.
    return {"status": "ok", "expires_in": resultado.get("expires_in")}


@app.get("/auth/me")
async def auth_me(request: Request):
    identidad, _ = await sesion_actual(request)
    return {"user_id": identidad["user_id"], "username": identidad["username"], "roles": identidad["roles"]}


@app.post("/auth/logout")
async def auth_logout(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    error = None
    if token:
        try:
            secretos = await get_gateway_secrets()
            await revocar(token, secretos["auth_introspection_secret"])  # 1) revocar en el servidor
        except HTTPException:
            error = True
    if error:
        respuesta = JSONResponse({"detail": "No se pudo revocar la sesión en el servidor"}, status_code=503)
    else:
        respuesta = JSONResponse({"status": "logout"})
    respuesta.delete_cookie(COOKIE_NAME, path="/")  # 2) eliminar la cookie
    return respuesta


@app.get("/public/menu")
async def menu_publico():
    """Carta sin sesión: el Gateway la pide al Backend con su secreto, sin identidad de usuario."""
    secretos = await get_gateway_secrets()
    estado, contenido, tipo = await enviar_al_backend(
        "GET", "menu", [], b"", None, {"X-Gateway-Secret": secretos["backend_shared_secret"]}
    )
    return Response(content=contenido, status_code=estado, headers={"Content-Type": tipo} if tipo else None)


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request):
    identidad, secretos = await sesion_actual(request)  # 401 / 503 / 500
    if ".." in path.split("/"):
        raise HTTPException(status_code=400, detail="Ruta inválida")
    autorizar(identidad["roles"], path, request.method)  # 403

    # Los headers hacia el backend se construyen desde cero: nada de lo que mande el cliente
    # (cookies, Authorization, X-Authenticated-*) se reenvía.
    headers = {
        "X-Gateway-Secret": secretos["backend_shared_secret"],
        "X-Authenticated-User": identidad["user_id"],
        "X-Authenticated-Username": identidad["username"],
        "X-Authenticated-Roles": ",".join(identidad["roles"]),
    }
    estado, contenido, tipo = await enviar_al_backend(
        request.method, path, list(request.query_params.multi_items()),
        await request.body(), request.headers.get("content-type"), headers,
    )
    return Response(content=contenido, status_code=estado, headers={"Content-Type": tipo} if tipo else None)
