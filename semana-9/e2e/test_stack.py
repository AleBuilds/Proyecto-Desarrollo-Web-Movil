"""Pruebas de integración contra el sistema completo ya levantado (Vault, Auth, Backend y Gateway).

    pytest e2e/test_stack.py -q

Variables opcionales: GATEWAY_URL, AUTH_URL, BACKEND_URL.
"""
import os

import httpx
import pytest

GATEWAY = os.getenv("GATEWAY_URL", "http://localhost:8000")
AUTH = os.getenv("AUTH_URL", "http://localhost:8100")
BACKEND = os.getenv("BACKEND_URL", "http://localhost:9000")


@pytest.fixture(scope="session", autouse=True)
def sistema_levantado():
    for nombre, url in (("Gateway", GATEWAY), ("Auth", AUTH), ("Backend", BACKEND)):
        try:
            httpx.get(f"{url}/health", timeout=3).raise_for_status()
        except Exception:
            pytest.skip(f"{nombre} no responde en {url}: levanta el sistema antes de correr estas pruebas")


def nuevo_cliente():
    return httpx.Client(base_url=GATEWAY, timeout=10)


def iniciar_sesion(usuario, password):
    c = nuevo_cliente()
    r = c.post("/auth/login", json={"username": usuario, "password": password})
    assert r.status_code == 200, r.text
    return c, r


# A. Backend directo
def test_backend_directo_sin_secreto_es_403():
    assert httpx.get(f"{BACKEND}/products").status_code == 403
    assert httpx.get(f"{BACKEND}/orders").status_code == 403


def test_auth_exige_secreto_del_gateway():
    assert httpx.post(f"{AUTH}/introspect", json={"token": "x"}).status_code == 403
    assert httpx.post(f"{AUTH}/logout", json={"token": "x"}).status_code == 403


# B. Login incorrecto
def test_login_incorrecto_es_401():
    r = nuevo_cliente().post("/auth/login", json={"username": "ana", "password": "incorrecta"})
    assert r.status_code == 401 and "session_token" not in r.headers.get("set-cookie", "")


# Sin sesión
def test_sin_sesion_es_401():
    c = nuevo_cliente()
    assert c.get("/auth/me").status_code == 401
    assert c.get("/api/products").status_code == 401
    assert c.get("/api/orders").status_code == 401


# C + D. Ana: login -> cookie -> me -> products -> authorization -> logout
def test_flujo_completo_de_ana():
    c, login = iniciar_sesion("ana", "1234")
    cookie = login.headers["set-cookie"]
    assert "HttpOnly" in cookie and "SameSite=lax" in cookie
    assert c.cookies.get("session_token") not in login.text  # el token no viaja en el cuerpo

    me = c.get("/auth/me")
    assert me.status_code == 200 and me.json()["username"] == "ana" and me.json()["roles"] == ["user"]

    productos = c.get("/api/products")
    assert productos.status_code == 200 and productos.json()["authenticated_user"] == "ana"
    assert c.get("/api/orders").status_code == 200

    assert c.delete("/api/products/1").status_code == 403  # autenticada, pero no autorizada

    assert c.post("/auth/logout").status_code == 200
    assert c.get("/auth/me").status_code == 401


# E. Administrador
def test_ernesto_puede_eliminar_productos():
    c, _ = iniciar_sesion("ernesto", "admin123")
    assert c.get("/auth/me").json()["roles"] == ["user", "admin"]
    r = c.delete("/api/products/3")
    # 200 la primera vez; 404 si ya se eliminó en una corrida anterior (el backend guarda en memoria).
    assert r.status_code in (200, 404), r.text
    c.post("/auth/logout")


# F. Logout revoca la sesión en el servidor (no solo borra la cookie)
def test_token_robado_no_sirve_despues_del_logout():
    c, _ = iniciar_sesion("ana", "1234")
    token = c.cookies.get("session_token")
    assert nuevo_cliente_con(token).get("/auth/me").status_code == 200
    c.post("/auth/logout")
    assert nuevo_cliente_con(token).get("/auth/me").status_code == 401


def nuevo_cliente_con(token):
    c = nuevo_cliente()
    c.cookies.set("session_token", token)
    return c


# Identidad: el cliente no puede falsificarla
def test_headers_de_identidad_falsos_no_cambian_el_rol():
    c, _ = iniciar_sesion("ana", "1234")
    r = c.delete("/api/products/2", headers={"X-Authenticated-Roles": "admin", "X-Authenticated-Username": "ernesto"})
    assert r.status_code == 403
    c.post("/auth/logout")
