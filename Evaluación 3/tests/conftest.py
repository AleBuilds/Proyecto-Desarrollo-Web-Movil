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

# Secretos aleatorios por sesión de pruebas: nada queda escrito en el código.
import secrets as _secrets
os.environ["INTERNAL_SERVICE_SECRET"] = _secrets.token_hex(24)
os.environ["AUTH_INTROSPECTION_SECRET"] = _secrets.token_hex(24)
os.environ["GRPC_SERVICE_SECRET"] = _secrets.token_hex(24)
os.environ["PAYMENTS_SERVICE_SECRET"] = _secrets.token_hex(24)
os.environ["RATE_LIMIT_LOGIN_POR_MIN"] = "1000"
os.environ["RATE_LIMIT_GENERAL_POR_MIN"] = "100000"

# Bases SQLite temporales y aisladas: las pruebas jamás tocan ni agotan los datos reales (stock, pedidos).
import tempfile
_TMP = Path(tempfile.mkdtemp(prefix="mediterraneo-tests-"))
os.environ["AUTH_DB_PATH"] = str(_TMP / "dbIdentity.sqlite")
os.environ["INVENTORY_DB_PATH"] = str(_TMP / "dbInventory.sqlite")
os.environ["ORDERS_DB_PATH"] = str(_TMP / "dbOrders.sqlite")
os.environ["CLIENTS_DB_PATH"] = str(_TMP / "dbClients.sqlite")
os.environ["PAYMENTS_DB_PATH"] = str(_TMP / "dbPayments.sqlite")

import httpx
from httpx import ASGITransport

import auth_service
import inventory_service
import orders_service
import clients_service
import payments_service
import server as gql_server
import db_auth, db_inventory, db_orders, db_clients, db_payments

for _db in (db_auth, db_inventory, db_orders, db_clients, db_payments):
    _db.init_db()  # crea esquema y datos de prueba ficticios en la base temporal

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
