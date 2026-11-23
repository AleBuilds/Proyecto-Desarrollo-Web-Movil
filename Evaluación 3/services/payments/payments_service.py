"""Microservicio Payments (:9004): Gestión y procesamiento seguro de transacciones.
Persistencia en dbPayments.sqlite.
Previene cobros duplicados y verifica estados con proveedor de pago.
"""
import logging
import os
import secrets
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from db_payments import get_connection, init_db, reset_test_data

# Credencial propia de payments: solo `orders` la posee (el gateway no puede invocar este servicio).
PAYMENTS_SERVICE_SECRET = os.environ["PAYMENTS_SERVICE_SECRET"]

logger = logging.getLogger("payments")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [payments] %(message)s"))
    logger.addHandler(_h)
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Payments Microservice - El Mediterráneo", lifespan=lifespan)


def verify_internal_secret(
    request: Request,
    x_internal_secret: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
):
    if x_internal_secret is None or not secrets.compare_digest(
        x_internal_secret.encode("utf-8"), PAYMENTS_SERVICE_SECRET.encode("utf-8")
    ):
        logger.warning("rid=%s SECRETO DE PAYMENTS RECHAZADO %s %s -> 403", x_request_id, request.method, request.url.path)
        raise HTTPException(status_code=403, detail="Acceso no autorizado al servicio privado payments")
    logger.info("rid=%s secreto de payments VERIFICADO %s %s", x_request_id, request.method, request.url.path)


class PagoIn(BaseModel):
    order_id: int
    user_id: str
    monto: int = Field(gt=0)
    metodo_pago: Literal["webpay", "transferencia", "efectivo_contraentrega"] = "webpay"


@app.get("/health")
def health():
    return {"status": "ok", "servicio": "payments"}


@app.post("/reset-data")
def reset_endpoint(_: None = Depends(verify_internal_secret)):
    reset_test_data()
    return {"status": "reset_completed"}


@app.post("/payments/process", status_code=201)
def process_payment(
    datos: PagoIn,
    _: None = Depends(verify_internal_secret),
    x_request_id: str | None = Header(default=None),
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, estado, transaccion_proveedor_id FROM payments WHERE order_id = ?", (datos.order_id,))
    pago_previo = cur.fetchone()
    logger.info("rid=%s DB dbPayments SELECT payments order_id=%s -> %s",
                x_request_id, datos.order_id, "pago previo existente" if pago_previo else "sin pago previo")

    if pago_previo:
        conn.close()
        # Si ya estaba pagado, responde con el comprobante existente evitando cobro doble
        return {
            "status": "already_processed",
            "payment_id": pago_previo["id"],
            "order_id": datos.order_id,
            "estado": pago_previo["estado"],
            "transaction_code": pago_previo["transaccion_proveedor_id"],
        }

    transaccion_id = f"TX-MED-{datos.order_id}-{secrets.token_hex(4).upper()}"
    cur.execute(
        "INSERT INTO payments (order_id, user_id, monto, metodo_pago, estado, transaccion_proveedor_id) VALUES (?, ?, ?, ?, ?, ?)",
        (datos.order_id, datos.user_id, datos.monto, datos.metodo_pago, "approved", transaccion_id),
    )
    pago_id = cur.lastrowid
    conn.commit()
    conn.close()
    logger.info("rid=%s DB dbPayments INSERT payments id=%s order_id=%s monto=%s estado=approved COMMIT",
                x_request_id, pago_id, datos.order_id, datos.monto)

    return {
        "status": "approved",
        "payment_id": pago_id,
        "order_id": datos.order_id,
        "monto": datos.monto,
        "estado": "approved",
        "transaction_code": transaccion_id,
    }


@app.get("/payments/order/{order_id}")
def get_payment_status(order_id: int, _: None = Depends(verify_internal_secret)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, order_id, user_id, monto, metodo_pago, estado, transaccion_proveedor_id, created_at FROM payments WHERE order_id = ?",
        (order_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="No se encontró registro de pago para este pedido")
    return dict(row)
