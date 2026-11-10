"""Pruebas de registro, GraphQL autenticado, credencial propia de payments y ciclo de vida del pedido."""
import os
import secrets as _s

from fastapi.testclient import TestClient

import gateway
import inventory_service
import orders_service
import payments_service
import server as gql_server

SECRET = os.environ["INTERNAL_SERVICE_SECRET"]
PAY_SECRET = os.environ["PAYMENTS_SERVICE_SECRET"]

gw = TestClient(gateway.app)
inv = TestClient(inventory_service.app)
orders = TestClient(orders_service.app)
pay = TestClient(payments_service.app)
gql = TestClient(gql_server.app)

ANA = {"X-Internal-Secret": SECRET, "X-Authenticated-User": "USR-001", "X-Authenticated-Username": "ana",
       "X-Authenticated-Roles": "user"}
ADMIN = {"X-Internal-Secret": SECRET, "X-Authenticated-User": "USR-003", "X-Authenticated-Username": "administrador1",
         "X-Authenticated-Roles": "user,admin"}


def _datos_registro(**extra):
    u = "test" + _s.token_hex(4)
    d = {"username": u, "password": "Clave-segura-123", "nombre_completo": "Persona de Prueba",
         "email": f"{u}@ejemplo.cl", "telefono": "+56911112222"}
    d.update(extra)
    return d


def _limpiar():
    gateway._solicitudes.clear()


# ---------------- Registro ----------------
def test_registro_crea_cuenta_con_rol_user_y_perfil():
    _limpiar()
    d = _datos_registro(roles=["admin"], role="admin")  # intento de escalar privilegios
    r = gw.post("/auth/register", json=d)
    assert r.status_code == 201 and r.json()["username"] == d["username"]

    cliente = TestClient(gateway.app)
    assert cliente.post("/auth/login", json={"username": d["username"], "password": d["password"]}).status_code == 200
    assert cliente.get("/auth/me").json()["roles"] == ["user"]            # el rol lo decide el servidor
    perfil = cliente.get("/api/clients/me")
    assert perfil.status_code == 200 and perfil.json()["email"] == d["email"]
    r_admin = cliente.post("/api/products", json={"categoria": "hummus", "nombre": "x", "precio": 1,
                                                   "descripcion": "x", "img": "x", "stock": 1})
    assert r_admin.status_code == 403


def test_registro_rechaza_duplicados_y_datos_invalidos():
    _limpiar()
    d = _datos_registro()
    assert gw.post("/auth/register", json=d).status_code == 201
    assert gw.post("/auth/register", json=d).status_code == 409
    assert gw.post("/auth/register", json=_datos_registro(password="corta")).status_code == 422
    assert gw.post("/auth/register", json=_datos_registro(email="no-es-correo")).status_code == 422
    assert gw.post("/auth/register", json=_datos_registro(username="MAYUS cULAS")).status_code == 422


def test_registro_tiene_rate_limit():
    _limpiar()
    gateway.RATE_LIMIT_LOGIN_POR_MIN, previo = 2, gateway.RATE_LIMIT_LOGIN_POR_MIN
    try:
        codigos = [gw.post("/auth/register", json=_datos_registro(password="x")).status_code for _ in range(4)]
    finally:
        gateway.RATE_LIMIT_LOGIN_POR_MIN = previo
        _limpiar()
    assert codigos[:2] == [422, 422] and codigos[2:] == [429, 429]


def test_contrasena_se_guarda_con_hash_no_reversible():
    import sqlite3
    import db_auth
    d = _datos_registro()
    _limpiar()
    assert gw.post("/auth/register", json=d).status_code == 201
    fila = sqlite3.connect(db_auth.DB_PATH).execute(
        "SELECT password_hash FROM identities WHERE username = ?", (d["username"],)).fetchone()
    assert fila[0].startswith("scrypt$") and d["password"] not in fila[0]


# ---------------- GraphQL privado ----------------
def test_graphql_privado_rechaza_llamada_directa_sin_secreto():
    q = {"query": "{ catalogoDisponible { id } }"}
    assert gql.post("/graphql", json=q).status_code == 403
    assert gql.post("/graphql", json=q, headers={"X-Internal-Secret": "incorrecto"}).status_code == 403
    assert gql.post("/graphql", json=q, headers={"X-Internal-Secret": SECRET}).status_code == 200


def test_graphql_resumen_exige_identidad_verificada():
    """Sin sesión, resumenPedido no usa ningún usuario por defecto: responde error y data nula."""
    _limpiar()
    q = {"query": "{ resumenPedido(orderId: 1) { orderId total } }"}
    r = TestClient(gateway.app).post("/graphql", json=q)           # anónimo, vía gateway
    cuerpo = r.json()
    assert cuerpo["data"] is None or cuerpo["data"]["resumenPedido"] is None
    assert cuerpo.get("errors")
    r2 = gql.post("/graphql", json=q, headers={"X-Internal-Secret": SECRET})  # con secreto pero sin identidad
    assert r2.json().get("errors")


# ---------------- payments con credencial propia ----------------
def test_payments_no_acepta_el_secreto_interno_del_gateway():
    pago = {"order_id": 987654, "user_id": "USR-001", "monto": 1000, "metodo_pago": "webpay"}
    assert pay.post("/payments/process", json=pago, headers={"X-Internal-Secret": SECRET}).status_code == 403
    assert pay.post("/payments/process", json=pago).status_code == 403


def test_gateway_no_enruta_payments_a_ningun_rol():
    _limpiar()
    c = TestClient(gateway.app)
    c.post("/auth/login", json={"username": "administrador1", "password": "admin123"})
    assert c.get("/api/payments/order/1").status_code == 403
    assert c.post("/api/payments/process", json={}).status_code == 403


# ---------------- Ciclo de vida del pedido ----------------
def _pedido(headers, monkeypatch_pagos=None):
    clave = "t-" + _s.token_hex(6)
    body = {"items": [{"id": 1, "cantidad": 1}], "metodo": "retiro", "nombre": "Ana", "telefono": "+56912345678"}
    return orders.post("/orders", json=body, headers={**headers, "X-Idempotency-Key": clave})


def test_pedido_con_pago_aprobado_queda_confirmado():
    r = _pedido(ANA)
    assert r.status_code == 201 and r.json()["status"] == "confirmed"


def test_pedido_queda_pendiente_si_payments_no_responde(monkeypatch):
    monkeypatch.setattr(orders_service, "PAYMENTS_URL", "http://127.0.0.1:9")  # nadie escucha
    r = _pedido(ANA)
    assert r.status_code == 201 and r.json()["status"] == "pending"
    assert orders.get(f"/orders/{r.json()['id']}", headers=ANA).json()["status"] == "pending"


def test_transiciones_invalidas_y_cancelacion_devuelve_stock():
    stock0 = inv.get("/products/1", headers={"X-Internal-Secret": SECRET}).json()["stock"]
    oid = _pedido(ANA).json()["id"]
    stock1 = inv.get("/products/1", headers={"X-Internal-Secret": SECRET}).json()["stock"]
    assert stock1 == stock0 - 1

    # Un cliente no puede cambiar estados
    assert orders.patch(f"/orders/{oid}/status", json={"status": "cancelled"}, headers=ANA).status_code == 403
    # Salto de estados no permitido: confirmed -> completed
    assert orders.patch(f"/orders/{oid}/status", json={"status": "completed"}, headers=ADMIN).status_code == 409
    assert orders.patch(f"/orders/{oid}/status", json={"status": "in_preparation"}, headers=ADMIN).status_code == 200
    # Anular: conserva el registro y devuelve el stock
    assert orders.patch(f"/orders/{oid}/status", json={"status": "cancelled"}, headers=ADMIN).status_code == 200
    assert inv.get("/products/1", headers={"X-Internal-Secret": SECRET}).json()["stock"] == stock0
    assert orders.get(f"/orders/{oid}", headers=ANA).json()["status"] == "cancelled"
    # Un pedido cancelado es terminal
    assert orders.patch(f"/orders/{oid}/status", json={"status": "in_preparation"}, headers=ADMIN).status_code == 409


# ---------------- Contacto (REQ-08) ----------------
def test_contacto_publico_se_guarda_y_solo_admin_lo_lee():
    _limpiar()
    c = TestClient(gateway.app)
    marca = "msg-" + _s.token_hex(4)
    r = c.post("/public/contact", json={"nombre": "Visita Anónima", "email": "visita@ejemplo.cl", "mensaje": f"Consulta {marca}"})
    assert r.status_code == 201
    assert c.post("/public/contact", json={"nombre": "X", "email": "malo", "mensaje": "corto"}).status_code == 422
    assert c.get("/api/contact").status_code == 401                         # anónimo no lee
    c.post("/auth/login", json={"username": "ana", "password": "1234"})
    assert c.get("/api/contact").status_code == 403                         # cliente tampoco
    adm = TestClient(gateway.app)
    adm.post("/auth/login", json={"username": "administrador1", "password": "admin123"})
    lista = adm.get("/api/contact")
    assert lista.status_code == 200 and any(marca in m["mensaje"] for m in lista.json()["messages"])


def test_contacto_tiene_rate_limit():
    _limpiar()
    gateway.RATE_LIMIT_LOGIN_POR_MIN, previo = 2, gateway.RATE_LIMIT_LOGIN_POR_MIN
    try:
        c = TestClient(gateway.app)
        cod = [c.post("/public/contact", json={"nombre": "Spam Bot", "email": "s@s.cl", "mensaje": "mensaje de spam"}).status_code
               for _ in range(4)]
    finally:
        gateway.RATE_LIMIT_LOGIN_POR_MIN = previo
        _limpiar()
    assert cod == [201, 201, 429, 429]
