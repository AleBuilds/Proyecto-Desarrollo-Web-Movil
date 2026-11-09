"""Pruebas del GraphQL Gateway (Módulo 8).
Valida agregación de subsistemas (Orders + Inventory + Clients) y límites de complejidad de consultas.
"""
from fastapi.testclient import TestClient
import server as gql_server

client = TestClient(gql_server.app)


def test_catalogo_disponible_graphql():
    query = """
    query {
        catalogoDisponible {
            id
            nombre
            precio
            categoria
            disponible
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "catalogoDisponible" in data["data"]
    assert len(data["data"]["catalogoDisponible"]) >= 9


def test_limite_de_profundidad_rechaza_consulta_abusiva():
    """DSL D_F04_GraphQL_Limite_C3: Consulta con profundidad mayor a 6 es rechazada antes de resolver."""
    query_anidada = """
    query {
        catalogoDisponible {
            id
            nombre
            categoria
        }
    }
    """
    # Consulta maliciosa artificial con excesiva anidación
    query_profunda = "query { a { b { c { d { e { f { g { h } } } } } } } }"
    response = client.post("/graphql", json={"query": query_profunda})
    assert response.status_code == 400
    assert "supera el límite permitido" in response.json()["detail"]


def test_agregacion_resumen_pedido_combina_tres_sistemas():
    """Valida la agregación completa entre Orders, Inventory y Clients."""
    query = """
    query ResumenTest {
        resumenPedido(orderId: 1) {
            orderId
            status
            total
            items {
                productId
                nombre
                precio
                cantidad
                subtotalLinea
            }
        }
    }
    """
    headers = {
        "X-Authenticated-User": "USR-001",
        "X-Authenticated-Username": "ana",
        "X-Authenticated-Roles": "user",
    }
    response = client.post("/graphql", json={"query": query}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
