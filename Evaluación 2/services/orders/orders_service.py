"""Microservicio Orders (:9002): Ciclo de vida de pedidos, reservas, control de idempotencia y autorización por propiedad.
Persistencia en dbOrders.sqlite.
Colabora mediante contratos con Inventory (:9001) y Payments (:9004).
"""
import json
import os
import secrets
from contextlib import asynccontextmanager
from typing import Literal

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Response
from pydantic import BaseModel, Field

from db_orders import get_connection, init_db, reset_test_data

INTERNAL_SERVICE_SECRET = os.getenv("INTERNAL_SERVICE_SECRET", "gateway-api-secret-456")
INVENTORY_URL = os.getenv("INVENTORY_URL", "http://127.0.0.1:9001")
PAYMENTS_URL = os.getenv("PAYMENTS_URL", "http://127.0.0.1:9004")
ENVIO_COSTO = 2500


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Orders Microservice - El Mediterráneo", lifespan=lifespan)


def verify_internal_secret(x_internal_secret: str | None = Header(default=None)):
    if x_internal_secret is None or not secrets.compare_digest(
        x_internal_secret.encode("utf-8"), INTERNAL_SERVICE_SECRET.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Acceso no autorizado al servicio privado orders")


def obtener_identidad(
    _: None = Depends(verify_internal_secret),
    x_authenticated_user: str | None = Header(default=None),
    x_authenticated_username: str | None = Header(default=None),
    x_authenticated_roles: str | None = Header(default=None),
) -> dict:
    if not x_authenticated_user:
        raise HTTPException(status_code=401, detail="Contexto de identidad no provisto por el Gateway")
    roles = [r.strip() for r in (x_authenticated_roles or "").split(",") if r.strip()]
    return {
        "user_id": x_authenticated_user,
        "username": x_authenticated_username or "anónimo",
        "roles": roles,
    }


class ItemIn(BaseModel):
    id: int
    cantidad: int = Field(ge=1, le=20)


class PedidoIn(BaseModel):
    items: list[ItemIn] = Field(min_length=1, max_length=30)
    metodo: Literal["delivery", "retiro"]
    nombre: str = Field(min_length=1, max_length=80)
    telefono: str = Field(min_length=6, max_length=20)
    direccion: str = Field(default="", max_length=160)
    notas: str = Field(default="", max_length=300)


class ReservaIn(BaseModel):
    fecha: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    hora: str = Field(pattern=r"^\d{2}:\d{2}$")
    personas: int = Field(ge=1, le=20)
    nombre: str = Field(min_length=1, max_length=80)
    telefono: str = Field(min_length=6, max_length=20)


class EstadoUpdateIn(BaseModel):
    status: Literal["pending", "in_preparation", "dispatched", "completed", "cancelled"]


@app.get("/health")
def health():
    return {"status": "ok", "servicio": "orders"}


@app.post("/reset-data")
def reset_endpoint(_: None = Depends(verify_internal_secret)):
    reset_test_data()
    return {"status": "reset_completed"}


@app.post("/orders", status_code=201)
async def create_order(
    datos: PedidoIn,
    ident: dict = Depends(obtener_identidad),
    x_idempotency_key: str | None = Header(default=None),
):
    # 1. Comprobación de Idempotencia (Paso C3-4 y D_F02_Reintento)
    conn = get_connection()
    cur = conn.cursor()
    if x_idempotency_key:
        cur.execute(
            "SELECT response_json FROM idempotency_records WHERE idempotency_key = ?",
            (x_idempotency_key,),
        )
        prev = cur.fetchone()
        if prev:
            conn.close()
            # Devuelve exactamente el pedido registrado previamente sin re-procesar ni duplicar cobros
            return json.loads(prev["response_json"])

    if datos.metodo == "delivery" and not datos.direccion.strip():
        conn.close()
        raise HTTPException(status_code=400, detail="El método delivery requiere dirección de entrega válida")

    # 2. Coordinación con Inventory: Reserva atómica de Stock y obtención de Precios oficiales
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            inv_res = await client.post(
                f"{INVENTORY_URL}/inventory/reserve",
                json={"items": [it.model_dump() for it in datos.items]},
                headers={"X-Internal-Secret": INTERNAL_SERVICE_SECRET},
            )
        if inv_res.status_code == 409:
            conn.close()
            raise HTTPException(status_code=409, detail=inv_res.json().get("detail", "Stock insuficiente"))
        if inv_res.status_code != 200:
            conn.close()
            raise HTTPException(status_code=502, detail="Error en comunicación con microservicio de inventario")
        items_con_precio = inv_res.json()["items"]
    except httpx.RequestError:
        conn.close()
        raise HTTPException(status_code=503, detail="Servicio de inventario no disponible")

    # 3. Cálculo de negocio en el Servidor (Regla estricta: nunca confiar en precios del navegador)
    subtotal = sum(i["precio"] * i["cantidad"] for i in items_con_precio)
    envio = ENVIO_COSTO if datos.metodo == "delivery" else 0
    total = subtotal + envio

    # 4. Persistencia en dbOrders.sqlite
    cur.execute(
        """INSERT INTO orders (user_id, username, metodo, nombre, telefono, direccion, notas, subtotal, envio, total, status, idempotency_key)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', ?)""",
        (
            ident["user_id"],
            ident["username"],
            datos.metodo,
            datos.nombre,
            datos.telefono,
            datos.direccion,
            datos.notas,
            subtotal,
            envio,
            total,
            x_idempotency_key,
        ),
    )
    pedido_id = cur.lastrowid

    for it in items_con_precio:
        cur.execute(
            "INSERT INTO order_items (order_id, product_id, nombre, precio, cantidad) VALUES (?, ?, ?, ?, ?)",
            (pedido_id, it["id"], it["nombre"], it["precio"], it["cantidad"]),
        )

    # 5. Coordinación con Payments: Registro de transacción inicial
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"{PAYMENTS_URL}/payments/process",
                json={"order_id": pedido_id, "user_id": ident["user_id"], "monto": total, "metodo_pago": "webpay"},
                headers={"X-Internal-Secret": INTERNAL_SERVICE_SECRET},
            )
    except httpx.RequestError:
        # Registro degradado controlado
        pass

    resultado = {
        "id": pedido_id,
        "user_id": ident["user_id"],
        "username": ident["username"],
        "items": items_con_precio,
        "metodo": datos.metodo,
        "nombre": datos.nombre,
        "telefono": datos.telefono,
        "direccion": datos.direccion,
        "notas": datos.notas,
        "subtotal": subtotal,
        "envio": envio,
        "total": total,
        "status": "confirmed",
    }

    # Guardar en registro de idempotencia si se proveyó la clave
    if x_idempotency_key:
        cur.execute(
            "INSERT OR REPLACE INTO idempotency_records (idempotency_key, order_id, response_json) VALUES (?, ?, ?)",
            (x_idempotency_key, pedido_id, json.dumps(resultado)),
        )

    conn.commit()
    conn.close()
    return resultado


@app.get("/orders")
def get_orders(ident: dict = Depends(obtener_identidad)):
    """Aplica control de propiedad: clientes ven solo sus pedidos; admins ven todos."""
    conn = get_connection()
    cur = conn.cursor()
    es_admin = "admin" in ident["roles"]

    if es_admin:
        cur.execute("SELECT * FROM orders ORDER BY id DESC")
    else:
        cur.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC", (ident["user_id"],))

    orders_rows = cur.fetchall()
    pedidos = []
    for o in orders_rows:
        o_dict = dict(o)
        cur.execute("SELECT product_id as id, nombre, precio, cantidad FROM order_items WHERE order_id = ?", (o["id"],))
        o_dict["items"] = [dict(it) for it in cur.fetchall()]
        pedidos.append(o_dict)

    conn.close()
    return {"authenticated_user": ident["username"], "orders": pedidos}


@app.get("/orders/{order_id}")
def get_order_by_id(order_id: int, ident: dict = Depends(obtener_identidad)):
    """Verificación de acceso a recurso ajeno (DSL D_F03_Ajeno)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order_row = cur.fetchone()

    if not order_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    es_titular = order_row["user_id"] == ident["user_id"]
    es_admin = "admin" in ident["roles"]

    if not es_titular and not es_admin:
        conn.close()
        # Rechazo explícito: no revela información de un pedido que no pertenece al usuario autenticado
        raise HTTPException(status_code=403, detail="Acceso denegado: este pedido pertenece a otro usuario")

    cur.execute("SELECT product_id as id, nombre, precio, cantidad FROM order_items WHERE order_id = ?", (order_id,))
    items = [dict(it) for it in cur.fetchall()]
    conn.close()

    resultado = dict(order_row)
    resultado["items"] = items
    return resultado


@app.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    datos: EstadoUpdateIn,
    ident: dict = Depends(obtener_identidad),
):
    if "admin" not in ident["roles"]:
        raise HTTPException(status_code=403, detail="Solo administradores u operadores pueden cambiar el estado del pedido")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, status FROM orders WHERE id = ?", (order_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    cur.execute("UPDATE orders SET status = ? WHERE id = ?", (datos.status, order_id))
    conn.commit()
    conn.close()
    return {"order_id": order_id, "status": datos.status, "updated_by": ident["username"]}


@app.get("/reservations")
def get_reservations(ident: dict = Depends(obtener_identidad)):
    conn = get_connection()
    cur = conn.cursor()
    es_admin = "admin" in ident["roles"]

    if es_admin:
        cur.execute("SELECT * FROM reservations ORDER BY id DESC")
    else:
        cur.execute("SELECT * FROM reservations WHERE user_id = ? ORDER BY id DESC", (ident["user_id"],))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"reservations": rows}


@app.post("/reservations", status_code=201)
def create_reservation(datos: ReservaIn, ident: dict = Depends(obtener_identidad)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO reservations (user_id, username, fecha, hora, personas, nombre, telefono, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'confirmed')""",
        (ident["user_id"], ident["username"], datos.fecha, datos.hora, datos.personas, datos.nombre, datos.telefono),
    )
    reserva_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"id": reserva_id, "user_id": ident["user_id"], "username": ident["username"], **datos.model_dump(), "status": "confirmed"}
