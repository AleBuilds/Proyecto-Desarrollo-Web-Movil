import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "gateway"))
sys.path.insert(0, str(RAIZ / "auth_service"))
sys.path.insert(0, str(RAIZ / "graphql_gateway"))
sys.path.insert(0, str(RAIZ / "services" / "inventory"))
sys.path.insert(0, str(RAIZ / "services" / "orders"))
sys.path.insert(0, str(RAIZ / "services" / "clients"))
sys.path.insert(0, str(RAIZ / "services" / "payments"))
sys.path.insert(0, str(RAIZ / "services" / "delivery_telemetry"))

os.environ["INTERNAL_SERVICE_SECRET"] = "gateway-api-secret-456"
os.environ["AUTH_INTROSPECTION_SECRET"] = "gateway-auth-secret-789"

import httpx
from httpx import ASGITransport

import auth_service
import inventory_service
import orders_service
import clients_service
import payments_service
import server as gql_server

# Mapeo de microservicios para ejecución en pruebas sin requerir puertos abiertos
APP_MAP = {
    8100: auth_service.app,
    9001: inventory_service.app,
    9002: orders_service.app,
    9003: clients_service.app,
    9004: payments_service.app,
    8050: gql_server.app,
}

TRANSPORTS = {port: ASGITransport(app=app) for port, app in APP_MAP.items()}

_orig_send = httpx.AsyncClient.send


async def _routed_send(self, request, *args, **kwargs):
    port = request.url.port
    if port in TRANSPORTS:
        resp = await TRANSPORTS[port].handle_async_request(request)
        await resp.aread()
        return resp
    return await _orig_send(self, request, *args, **kwargs)


httpx.AsyncClient.send = _routed_send
