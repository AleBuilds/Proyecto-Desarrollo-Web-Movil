import httpx
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

import gateway

SECRETOS = {"backend_shared_secret": "gateway-api-secret-456", "auth_introspection_secret": "gateway-auth-secret-789"}
SESIONES = {
    "tok-ana": {"active": True, "user_id": "USR-001", "username": "ana", "roles": ["user"]},
    "tok-administrador1": {"active": True, "user_id": "USR-003", "username": "administrador1", "roles": ["user", "admin"]},
}


@pytest.fixture
def stack(monkeypatch):
    """Gateway con Vault, Auth y Backend simulados. Registra las llamadas al backend."""
    llamadas = {"backend": [], "revocados": []}

    async def secretos():
        return SECRETOS

    async def introspeccionar(token, secreto):
        assert secreto == "gateway-auth-secret-789"
        return SESIONES.get(token)

    async def login_falso(username, password):
        if (username, password) == ("ana", "1234"):
            return {"access_token": "tok-ana", "token_type": "bearer", "expires_in": 900}
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    async def revocar_falso(token, secreto):
        llamadas["revocados"].append(token)

    async def backend(method, path, params, body, content_type, headers):
        llamadas["backend"].append({"method": method, "path": path, "headers": headers})
        return 200, b'{"ok": true}', "application/json"

    monkeypatch.setattr(gateway, "get_gateway_secrets", secretos)
    monkeypatch.setattr(gateway, "introspect", introspeccionar)
    monkeypatch.setattr(gateway, "login_upstream", login_falso)
    monkeypatch.setattr(gateway, "revocar", revocar_falso)
    monkeypatch.setattr(gateway, "enviar_al_backend", backend)
    cliente = TestClient(gateway.app)
    cliente.llamadas = llamadas
    return cliente


# ---------- autorización (función pura) ----------
@pytest.mark.parametrize("roles,metodo,ruta,permitido", [
    (["user"], "GET", "products", True),
    (["user"], "GET", "products/1", True),
    (["user"], "GET", "orders", True),
    (["user"], "DELETE", "products/1", False),
    (["user"], "POST", "products", False),
    (["user"], "GET", "secretos", False),
    (["user", "admin"], "DELETE", "products/1", True),
    (["admin"], "GET", "orders", True),
    (["admin"], "POST", "orders", False),
    ([], "GET", "products", False),
    (["desconocido"], "GET", "products", False),
])
def test_matriz_de_autorizacion(roles, metodo, ruta, permitido):
    if permitido:
        gateway.autorizar(roles, ruta, metodo)
    else:
        with pytest.raises(HTTPException) as exc:
            gateway.autorizar(roles, ruta, metodo)
        assert exc.value.status_code == 403


# ---------- login / cookie ----------
def test_login_crea_cookie_httponly_y_no_expone_el_token(stack):
    r = stack.post("/auth/login", json={"username": "ana", "password": "1234"})
    assert r.status_code == 200
    cookie = r.headers["set-cookie"]
    assert cookie.startswith("session_token=tok-ana")
    assert "HttpOnly" in cookie and "SameSite=lax" in cookie and "Path=/" in cookie
    assert "tok-ana" not in r.text  # el token no va en el cuerpo


def test_login_incorrecto_es_401_sin_cookie(stack):
    r = stack.post("/auth/login", json={"username": "ana", "password": "mala"})
    assert r.status_code == 401 and "set-cookie" not in r.headers


def test_login_con_auth_caido_es_503(monkeypatch):
    monkeypatch.setattr(gateway, "AUTH_URL", "http://127.0.0.1:1")
    r = TestClient(gateway.app).post("/auth/login", json={"username": "ana", "password": "1234"})
    assert r.status_code == 503


# ---------- sesión ----------
def test_me_sin_cookie_es_401(stack):
    assert stack.get("/auth/me").status_code == 401


def test_me_con_sesion_valida(stack):
    stack.cookies.set("session_token", "tok-administrador1")
    r = stack.get("/auth/me")
    assert r.status_code == 200 and r.json() == {"user_id": "USR-003", "username": "administrador1", "roles": ["user", "admin"]}


def test_cookie_revocada_o_inventada_es_401(stack):
    stack.cookies.set("session_token", "token-inventado")
    assert stack.get("/auth/me").status_code == 401
    assert stack.get("/api/products").status_code == 401


def test_auth_caido_es_503_al_validar_sesion(monkeypatch):
    async def secretos():
        return SECRETOS
    monkeypatch.setattr(gateway, "get_gateway_secrets", secretos)
    monkeypatch.setattr(gateway, "AUTH_URL", "http://127.0.0.1:1")
    cliente = TestClient(gateway.app)
    cliente.cookies.set("session_token", "tok-ana")
    assert cliente.get("/api/products").status_code == 503


# ---------- logout ----------
def test_logout_revoca_en_el_servidor_y_borra_la_cookie(stack):
    stack.cookies.set("session_token", "tok-ana")
    r = stack.post("/auth/logout")
    assert r.status_code == 200
    assert stack.llamadas["revocados"] == ["tok-ana"]
    cookie = r.headers["set-cookie"]
    assert cookie.startswith('session_token=""') or "Max-Age=0" in cookie


def test_logout_sin_sesion_responde_200(stack):
    assert stack.post("/auth/logout").status_code == 200
    assert stack.llamadas["revocados"] == []


def test_logout_con_auth_caido_avisa_503_pero_borra_la_cookie(stack, monkeypatch):
    async def falla(token, secreto):
        raise HTTPException(status_code=503, detail="x")
    monkeypatch.setattr(gateway, "revocar", falla)
    stack.cookies.set("session_token", "tok-ana")
    r = stack.post("/auth/logout")
    assert r.status_code == 503 and "Max-Age=0" in r.headers["set-cookie"]


# ---------- /api ----------
def test_api_sin_cookie_es_401_y_no_llega_al_backend(stack):
    assert stack.get("/api/products").status_code == 401
    assert stack.llamadas["backend"] == []


def test_user_lee_productos_y_el_backend_recibe_identidad_y_secreto(stack):
    stack.cookies.set("session_token", "tok-ana")
    assert stack.get("/api/products").status_code == 200
    enviado = stack.llamadas["backend"][0]["headers"]
    assert enviado["X-Gateway-Secret"] == "gateway-api-secret-456"
    assert enviado["X-Authenticated-User"] == "USR-001"
    assert enviado["X-Authenticated-Username"] == "ana"
    assert enviado["X-Authenticated-Roles"] == "user"


def test_user_no_puede_eliminar_y_la_peticion_no_llega_al_backend(stack):
    stack.cookies.set("session_token", "tok-ana")
    assert stack.delete("/api/products/1").status_code == 403
    assert stack.llamadas["backend"] == []


def test_admin_elimina_producto(stack):
    stack.cookies.set("session_token", "tok-administrador1")
    assert stack.delete("/api/products/1").status_code == 200
    assert stack.llamadas["backend"][0]["method"] == "DELETE"


def test_headers_de_identidad_enviados_por_el_cliente_no_se_reenvian(stack):
    stack.cookies.set("session_token", "tok-ana")
    stack.get("/api/products", headers={"X-Authenticated-Roles": "admin", "X-Authenticated-Username": "administrador1", "Authorization": "Bearer x"})
    enviado = stack.llamadas["backend"][0]["headers"]
    assert enviado["X-Authenticated-Roles"] == "user" and enviado["X-Authenticated-Username"] == "ana"
    assert "Authorization" not in enviado and "Cookie" not in enviado


def test_ruta_con_puntos_es_rechazada(stack):
    stack.cookies.set("session_token", "tok-administrador1")
    assert stack.get("/api/products/%2e%2e/orders").status_code in (400, 403)
    assert stack.llamadas["backend"] == []


def test_backend_caido_es_502(stack, monkeypatch):
    # se usa el enviar_al_backend real contra un puerto cerrado
    monkeypatch.undo()
    async def secretos():
        return SECRETOS
    async def introspeccionar(token, secreto):
        return SESIONES.get(token)
    monkeypatch.setattr(gateway, "get_gateway_secrets", secretos)
    monkeypatch.setattr(gateway, "introspect", introspeccionar)
    monkeypatch.setattr(gateway, "BACKEND_URL", "http://127.0.0.1:1")
    cliente = TestClient(gateway.app)
    cliente.cookies.set("session_token", "tok-ana")
    assert cliente.get("/api/products").status_code == 502


# ---------- frontend ----------
def test_frontend_se_sirve_con_csp(stack):
    r = stack.get("/")
    csp = r.headers.get("Content-Security-Policy", "")
    assert r.status_code == 200 and "El Mediterráneo" in r.text
    assert "default-src 'self'" in csp and "unsafe-inline" not in csp and "unsafe-eval" not in csp
    assert stack.get("/static/app.js").status_code == 200
