import pytest
from fastapi.testclient import TestClient

import backend_api

SECRETO = "gateway-api-secret-456"
client = TestClient(backend_api.app)


def como(usuario="ana", roles="user", secreto=SECRETO):
    return {
        "X-Gateway-Secret": secreto,
        "X-Authenticated-User": "USR-001",
        "X-Authenticated-Username": usuario,
        "X-Authenticated-Roles": roles,
    }


@pytest.fixture(autouse=True)
def datos_limpios():
    backend_api.reset_data()


def test_health_es_publico():
    assert client.get("/health").status_code == 200


@pytest.mark.parametrize("ruta", ["/products", "/orders"])
def test_acceso_directo_sin_secreto_es_403(ruta):
    assert client.get(ruta).status_code == 403


def test_secreto_incorrecto_es_403():
    assert client.get("/products", headers=como(secreto="incorrecto")).status_code == 403


def test_secreto_con_caracteres_no_ascii_es_403_y_no_500():
    assert client.get("/products", headers={"X-Gateway-Secret": b"\xf1and\xfa"}).status_code == 403


def test_headers_de_identidad_sin_secreto_no_sirven():
    falsos = {"X-Authenticated-User": "USR-003", "X-Authenticated-Username": "ernesto", "X-Authenticated-Roles": "user,admin"}
    assert client.delete("/products/1", headers=falsos).status_code == 403
    assert len(backend_api.PRODUCTS) == 9


def test_con_secreto_pero_sin_identidad_es_401():
    assert client.get("/products", headers={"X-Gateway-Secret": SECRETO}).status_code == 401


def test_user_lista_productos_y_ordenes():
    r = client.get("/products", headers=como())
    assert r.status_code == 200 and r.json()["authenticated_user"] == "ana" and len(r.json()["products"]) == 9
    assert client.get("/orders", headers=como()).status_code == 200


def test_rol_user_no_puede_eliminar_productos():
    assert client.delete("/products/1", headers=como()).status_code == 403
    assert len(backend_api.PRODUCTS) == 9


def test_rol_admin_puede_eliminar_productos():
    r = client.delete("/products/1", headers=como("ernesto", "user,admin"))
    assert r.status_code == 200 and r.json()["deleted"] == 1
    assert all(p["id"] != 1 for p in backend_api.PRODUCTS)
    assert client.delete("/products/1", headers=como("ernesto", "user,admin")).status_code == 404
