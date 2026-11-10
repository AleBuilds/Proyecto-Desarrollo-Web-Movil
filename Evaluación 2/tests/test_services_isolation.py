"""Pruebas de Aislamiento y Reglas de Negocio en Microservicios (Módulo 3 y 10).
Valida idempotencia, stock atómico, cálculo de precios en servidor y control de pagos.
"""
from fastapi.testclient import TestClient
import inventory_service
import orders_service
import payments_service
import clients_service

inv_client = TestClient(inventory_service.app)
orders_client = TestClient(orders_service.app)
pay_client = TestClient(payments_service.app)
cli_client = TestClient(clients_service.app)

import os
SECRET = os.environ["INTERNAL_SERVICE_SECRET"]
HEADERS_AUTH = {
    "X-Internal-Secret": SECRET,
    "X-Authenticated-User": "USR-001",
    "X-Authenticated-Username": "ana",
    "X-Authenticated-Roles": "user",
}


def test_calculo_estricto_de_precios_y_totales_en_servidor():
    """El cliente envía precios fraudulentos ($1 peso). El backend debe ignorarlos."""
    pedido_tramposo = {
        "items": [{"id": 1, "cantidad": 2}],  # Hummus Especial vale 5.200 cada uno
        "metodo": "delivery",
        "nombre": "Ana García",
        "telefono": "+56912345678",
        "direccion": "Av. Pajaritos 2100",
        "notas": "",
        "precio": 1,
        "total": 1,
    }
    r = orders_client.post("/orders", json=pedido_tramposo, headers=HEADERS_AUTH)
    assert r.status_code == 201
    data = r.json()
    # 2 * 5.200 = 10.400 subtotal + 2.500 envio = 12.900 total
    assert data["subtotal"] == 10400
    assert data["envio"] == 2500
    assert data["total"] == 12900


def test_control_de_idempotencia_sin_duplicar_pedido():
    """DSL D_F02_Reintento: Reenviar solicitud con misma clave devuelve el pedido existente."""
    import secrets
    clave = f"idem-key-test-{secrets.token_hex(4)}"
    pedido = {
        "items": [{"id": 2, "cantidad": 1}],
        "metodo": "retiro",
        "nombre": "Ana García",
        "telefono": "+56912345678",
        "direccion": "",
        "notas": "Primer intento",
    }
    headers_con_clave = {**HEADERS_AUTH, "X-Idempotency-Key": clave}

    # 1. Primera ejecución: crea el pedido
    r1 = orders_client.post("/orders", json=pedido, headers=headers_con_clave)
    assert r1.status_code == 201
    id_creado = r1.json()["id"]

    # 2. Segunda ejecución (reintento de red con misma clave)
    r2 = orders_client.post("/orders", json=pedido, headers=headers_con_clave)
    assert r2.status_code == 200 or r2.status_code == 201
    assert r2.json()["id"] == id_creado  # Devuelve el mismo ID sin duplicar


def test_reserva_y_conflicto_de_stock_insuficiente():
    """Verifica reserva atómica y rechazo 409 cuando se excede la existencia."""
    # Pedir cantidad que supera el stock disponible (ej. 999 unidades)
    r_exceso = inv_client.post(
        "/inventory/reserve",
        json={"items": [{"id": 1, "cantidad": 999}]},
        headers={"X-Internal-Secret": SECRET},
    )
    assert r_exceso.status_code == 409
    assert "Stock insuficiente" in r_exceso.json()["detail"]


def test_validacion_de_metodo_delivery_exige_direccion():
    pedido_sin_dir = {
        "items": [{"id": 1, "cantidad": 1}],
        "metodo": "delivery",
        "nombre": "Ana",
        "telefono": "+56912345678",
        "direccion": "",  # Vacía
    }
    r = orders_client.post("/orders", json=pedido_sin_dir, headers=HEADERS_AUTH)
    assert r.status_code == 400
    assert "requiere dirección" in r.json()["detail"]


def test_pagos_previene_doble_transaccion():
    import random
    unique_order_id = random.randint(100000, 999999)
    pago = {"order_id": unique_order_id, "user_id": "USR-001", "monto": 15000, "metodo_pago": "webpay"}
    headers = {"X-Internal-Secret": os.environ["PAYMENTS_SERVICE_SECRET"]}

    # Primer pago
    r1 = pay_client.post("/payments/process", json=pago, headers=headers)
    assert r1.status_code == 201
    assert r1.json()["status"] == "approved"
    tx1 = r1.json()["transaction_code"]

    # Reintento de pago para la misma orden
    r2 = pay_client.post("/payments/process", json=pago, headers=headers)
    assert r2.status_code == 200 or r2.status_code == 201
    assert r2.json()["status"] == "already_processed"
    assert r2.json()["transaction_code"] == tx1
