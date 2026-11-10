"""Pruebas del GraphQL Gateway (Módulo 8).
Valida agregación de subsistemas (Orders + Inventory + Clients), autorización por recurso y límites de consulta.
El servicio es privado: todas las llamadas llevan el secreto interno que en producción inyecta el API Gateway.
"""
import os
import secrets as _s

from fastapi.testclient import TestClient

import orders_service
import server as gql_server

client = TestClient(gql_server.app)
orders = TestClient(orders_service.app)

SECRET = {"X-Internal-Secret": os.environ["INTERNAL_SERVICE_SECRET"]}
ANA = {**SECRET, "X-Authenticated-User": "USR-001", "X-Authenticated-Username": "ana", "X-Authenticated-Roles": "user"}
SILENAY = {**SECRET, "X-Authenticated-User": "USR-002", "X-Authenticated-Username": "silenay",
           "X-Authenticated-Roles": "user"}
ADMIN = {**SECRET, "X-Authenticated-User": "USR-003", "X-Authenticated-Username": "administrador1",
         "X-Authenticated-Roles": "user,admin"}


def _crear_pedido_de_ana() -> int:
    r = orders.post(
        "/orders",
        json={"items": [{"id": 1, "cantidad": 2}, {"id": 4, "cantidad": 1}], "metodo": "retiro",
              "nombre": "Ana García", "telefono": "+56912345678"},
        headers={**ANA, "X-Idempotency-Key": "gql-" + _s.token_hex(6)},
    )
    assert r.status_code == 201
    return r.json()["id"]


def test_catalogo_disponible_graphql():
    query = "query { catalogoDisponible { id nombre precio categoria disponible } }"
    response = client.post("/graphql", json={"query": query}, headers=SECRET)
    assert response.status_code == 200
    productos = response.json()["data"]["catalogoDisponible"]
    assert len(productos) >= 9
    assert all(p["disponible"] for p in productos)


def test_limite_de_profundidad_rechaza_consulta_abusiva():
    """DSL D_F04_GraphQL_Limite_C3: profundidad mayor a 6 se rechaza antes de resolver."""
    query_profunda = "query { a { b { c { d { e { f { g { h } } } } } } } }"
    response = client.post("/graphql", json={"query": query_profunda}, headers=SECRET)
    assert response.status_code == 400
    assert "supera el límite permitido" in response.json()["detail"]


def test_agregacion_resumen_pedido_combina_tres_sistemas():
    """Orders (pedido) + Inventory (categoría, imagen) + Clients (perfil) en una sola consulta."""
    oid = _crear_pedido_de_ana()
    query = """
    query ($id: Int!) {
        resumenPedido(orderId: $id) {
            orderId status total avisoParcial
            cliente { nombreCompleto email telefono }
            items { nombre cantidad subtotalLinea categoria img }
        }
    }"""
    response = client.post("/graphql", json={"query": query, "variables": {"id": oid}}, headers=ANA)
    assert response.status_code == 200
    resumen = response.json()["data"]["resumenPedido"]
    assert resumen["orderId"] == oid and resumen["status"] == "confirmed"
    assert resumen["avisoParcial"] is None
    assert resumen["cliente"]["nombreCompleto"] == "Ana García"        # viene de clients
    assert all(i["categoria"] and i["img"] for i in resumen["items"])   # viene de inventory
    assert sum(i["subtotalLinea"] for i in resumen["items"]) == resumen["total"]  # viene de orders


def test_resumen_de_pedido_ajeno_no_filtra_datos():
    oid = _crear_pedido_de_ana()
    query = "query ($id: Int!) { resumenPedido(orderId: $id) { orderId total cliente { email telefono } } }"
    r = client.post("/graphql", json={"query": query, "variables": {"id": oid}}, headers=SILENAY).json()
    assert r.get("errors")
    assert r["data"] is None or r["data"]["resumenPedido"] is None
    assert "ana@" not in str(r) and "912345678" not in str(r)
    # El administrador sí puede verlo (autorización por rol, verificada en orders)
    ok = client.post("/graphql", json={"query": query, "variables": {"id": oid}}, headers=ADMIN).json()
    assert ok["data"]["resumenPedido"]["orderId"] == oid
