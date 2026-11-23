"""Pruebas de Seguridad, Autenticación y Autorización (Módulos 4 y 7).
Valida rechazo de acceso directo sin secreto, control RBAC, propiedad de recursos y protección de contraseñas.
"""
from fastapi.testclient import TestClient
import auth_service
import inventory_service
import orders_service
import gateway

auth_client = TestClient(auth_service.app)
inv_client = TestClient(inventory_service.app)
orders_client = TestClient(orders_service.app)
gw_client = TestClient(gateway.app)

import os
SECRET = os.environ["INTERNAL_SERVICE_SECRET"]
INTRO_SECRET = os.environ["AUTH_INTROSPECTION_SECRET"]


def test_password_hashing_scrypt_no_reversible():
    """Módulo 7: Verifica que no se use texto plano ni hash reversible."""
    h1 = auth_service.hash_password("passwordSegura123")
    assert h1.startswith("scrypt$")
    assert "passwordSegura123" not in h1
    assert auth_service.verify_password("passwordSegura123", h1) is True
    assert auth_service.verify_password("passwordErronea", h1) is False


def test_login_exitoso_y_credenciales_invalidas():
    # Login correcto
    r_ok = auth_client.post("/login", json={"username": "ana", "password": "1234"})
    assert r_ok.status_code == 200
    data = r_ok.json()
    assert "access_token" in data
    assert data["username"] == "ana"
    assert "user" in data["roles"]

    # Login incorrecto (tiempo constante protegido)
    r_fail = auth_client.post("/login", json={"username": "ana", "password": "badpassword"})
    assert r_fail.status_code == 401


def test_introspeccion_exige_secreto_de_servicio():
    r_login = auth_client.post("/login", json={"username": "ana", "password": "1234"})
    token = r_login.json()["access_token"]

    # Sin secreto: 403
    assert auth_client.post("/introspect", json={"token": token}).status_code == 403
    # Con secreto falso: 403
    assert auth_client.post("/introspect", json={"token": token}, headers={"X-Introspection-Secret": "falso"}).status_code == 403
    # Con secreto correcto: 200
    r_intro = auth_client.post("/introspect", json={"token": token}, headers={"X-Introspection-Secret": INTRO_SECRET})
    assert r_intro.status_code == 200
    assert r_intro.json()["active"] is True
    assert r_intro.json()["user_id"] == "USR-001"


def test_rechazo_de_acceso_directo_a_microservicios_privados():
    """Garantiza que nadie externo pueda llamar directo a inventory u orders sin secreto."""
    assert inv_client.get("/products").status_code == 403
    assert orders_client.get("/orders").status_code == 403

    # Con secreto interno sí responde
    assert inv_client.get("/products", headers={"X-Internal-Secret": SECRET}).status_code == 200


def test_control_de_propiedad_de_recursos_recurso_ajeno():
    """DSL D_F03_Ajeno: Ana no puede consultar el pedido de otro usuario."""
    headers_ana = {
        "X-Internal-Secret": SECRET,
        "X-Authenticated-User": "USR-001",
        "X-Authenticated-Username": "ana",
        "X-Authenticated-Roles": "user",
    }
    headers_silenay = {
        "X-Internal-Secret": SECRET,
        "X-Authenticated-User": "USR-002",
        "X-Authenticated-Username": "silenay",
        "X-Authenticated-Roles": "user",
    }

    # Silenay crea un pedido
    nuevo_pedido = {
        "items": [{"id": 1, "cantidad": 1}],
        "metodo": "retiro",
        "nombre": "Silenay",
        "telefono": "+56987654321",
        "direccion": "",
        "notas": "Retiro pronto",
    }
    r_crear = orders_client.post("/orders", json=nuevo_pedido, headers=headers_silenay)
    assert r_crear.status_code == 201
    pedido_id = r_crear.json()["id"]

    # Silenay puede consultar su propio pedido
    r_propio = orders_client.get(f"/orders/{pedido_id}", headers=headers_silenay)
    assert r_propio.status_code == 200

    # Ana intenta consultar el pedido de Silenay -> 403 Rechazado
    r_ajeno = orders_client.get(f"/orders/{pedido_id}", headers=headers_ana)
    assert r_ajeno.status_code == 403
    assert "Acceso denegado" in r_ajeno.json()["detail"]


def test_rbac_solo_administrador_puede_agregar_o_eliminar_platos():
    headers_user = {
        "X-Internal-Secret": SECRET,
        "X-Authenticated-User": "USR-001",
        "X-Authenticated-Roles": "user",
    }
    headers_admin = {
        "X-Internal-Secret": SECRET,
        "X-Authenticated-User": "USR-003",
        "X-Authenticated-Roles": "user,admin",
    }
    nuevo_plato = {
        "categoria": "hummus",
        "nombre": "Hummus Trufado",
        "precio": 8500,
        "descripcion": "Garbanzos seleccionados con aceite de trufa blanca.",
        "img": "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg",
        "stock": 20,
    }

    # Usuario estándar es rechazado
    assert inv_client.post("/products", json=nuevo_plato, headers=headers_user).status_code == 403
    # Administrador es autorizado
    r_admin = inv_client.post("/products", json=nuevo_plato, headers=headers_admin)
    assert r_admin.status_code == 201
    plato_id = r_admin.json()["id"]

    # Usuario estándar no puede eliminar
    assert inv_client.delete(f"/products/{plato_id}", headers=headers_user).status_code == 403
    # Administrador sí puede
    assert inv_client.delete(f"/products/{plato_id}", headers=headers_admin).status_code == 200
