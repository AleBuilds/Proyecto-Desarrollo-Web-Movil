"""Pruebas E2E del Stack Completo integrado con API Gateway (Módulo 10).
Simula el flujo completo de un usuario desde el navegador.
"""
from fastapi.testclient import TestClient
import gateway

gw_client = TestClient(gateway.app)


def test_gateway_public_menu():
    r = gw_client.get("/public/menu")
    assert r.status_code == 200
    data = r.json()
    assert "products" in data
    assert len(data["products"]) >= 9


def test_gateway_flujo_login_y_proteccion_de_rutas():
    # 1. Intentar acceder a ruta protegida sin sesión -> 401
    r_unauth = gw_client.get("/api/orders")
    assert r_unauth.status_code == 401
    assert "Sesión requerida" in r_unauth.json()["detail"]

    # 2. Login correcto
    r_login = gw_client.post("/auth/login", json={"username": "ana", "password": "1234"})
    assert r_login.status_code == 200
    assert "session_token" in gw_client.cookies

    # 3. Consulta de identidad actual
    r_me = gw_client.get("/auth/me")
    assert r_me.status_code == 200
    assert r_me.json()["username"] == "ana"

    # 4. Acceso a pedidos autenticado a través del Gateway
    r_orders = gw_client.get("/api/orders")
    assert r_orders.status_code == 200
    assert "orders" in r_orders.json()

    # 5. Logout y verificación de revocación
    r_logout = gw_client.post("/auth/logout")
    assert r_logout.status_code == 200

    # 6. Ya no puede acceder
    r_after = gw_client.get("/api/orders")
    assert r_after.status_code == 401
