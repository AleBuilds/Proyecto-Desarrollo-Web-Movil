"""Pedidos, reservas y carta pública del restaurante (backend directo, simulando al Gateway)."""
from fastapi.testclient import TestClient

import backend_api

client = TestClient(backend_api.app)
SECRETO = "gateway-api-secret-456"


def como(user_id="USR-001", usuario="ana", roles="user"):
    return {"X-Gateway-Secret": SECRETO, "X-Authenticated-User": user_id,
            "X-Authenticated-Username": usuario, "X-Authenticated-Roles": roles}


PEDIDO = {"items": [{"id": 1, "cantidad": 2}], "metodo": "delivery", "nombre": "Ana",
          "telefono": "+56912345678", "direccion": "Av. Pajaritos 2100"}


def setup_function():
    backend_api.reset_data()


def test_menu_publico_exige_gateway_pero_no_usuario():
    assert client.get("/menu").status_code == 403
    r = client.get("/menu", headers={"X-Gateway-Secret": SECRETO})
    assert r.status_code == 200 and len(r.json()["products"]) == 9


def test_total_se_calcula_en_el_servidor():
    r = client.post("/orders", json={**PEDIDO, "precio": 1, "total": 1}, headers=como())
    assert r.status_code == 201 and r.json()["subtotal"] == 10400 and r.json()["total"] == 12900


def test_retiro_no_cobra_envio_y_delivery_exige_direccion():
    assert client.post("/orders", json={**PEDIDO, "metodo": "retiro"}, headers=como()).json()["envio"] == 0
    assert client.post("/orders", json={**PEDIDO, "direccion": ""}, headers=como()).status_code == 400


def test_producto_inexistente_y_cantidad_invalida():
    assert client.post("/orders", json={**PEDIDO, "items": [{"id": 99, "cantidad": 1}]}, headers=como()).status_code == 400
    assert client.post("/orders", json={**PEDIDO, "items": [{"id": 1, "cantidad": 0}]}, headers=como()).status_code == 422


def test_cada_cliente_ve_solo_sus_pedidos_y_el_admin_todos():
    client.post("/orders", json=PEDIDO, headers=como())
    otro = como("USR-009", "luis")
    assert client.get("/orders", headers=otro).json()["orders"] == []
    admin = como("USR-003", "ernesto", "user,admin")
    assert len(client.get("/orders", headers=admin).json()["orders"]) == 1


def test_reservas_y_creacion_de_platos_solo_admin():
    reserva = {"fecha": "2026-10-14", "hora": "20:30", "personas": 4, "nombre": "Ana", "telefono": "+56912345678"}
    assert client.post("/reservations", json=reserva, headers=como()).status_code == 201
    nuevo = {"categoria": "pescados", "nombre": "Dorada", "precio": 13000}
    assert client.post("/products", json=nuevo, headers=como()).status_code == 403
    assert client.post("/products", json=nuevo, headers=como("USR-003", "ernesto", "user,admin")).status_code == 201
    assert client.post("/products", json={**nuevo, "img": "javascript:alert(1)"}, headers=como("USR-003", "ernesto", "user,admin")).status_code == 422
