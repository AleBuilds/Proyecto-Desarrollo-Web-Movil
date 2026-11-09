"""Microservicio Inventory (:9001): Catálogo, disponibilidad y reservas de stock.
Persistencia en dbInventory.sqlite.
Solo accesible por componentes autorizados con INTERNAL_SERVICE_SECRET.
"""
import os
import secrets
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from db_inventory import get_connection, init_db, reset_test_data

INTERNAL_SERVICE_SECRET = os.getenv("INTERNAL_SERVICE_SECRET", "gateway-api-secret-456")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Inventory Microservice - El Mediterráneo", lifespan=lifespan)


def verify_internal_secret(x_internal_secret: str | None = Header(default=None)):
    if x_internal_secret is None or not secrets.compare_digest(
        x_internal_secret.encode("utf-8"), INTERNAL_SERVICE_SECRET.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Acceso no autorizado al servicio privado inventory")


class ProductoIn(BaseModel):
    categoria: Literal["hummus", "falafel", "shawarma", "parrilla", "pescados", "ensaladas"]
    nombre: str = Field(min_length=1, max_length=80)
    descripcion: str = Field(default="", max_length=300)
    precio: int = Field(gt=0, le=1_000_000)
    img: str = Field(default="", pattern=r"^(https://[^\s\"'<>]*)?$", max_length=500)
    stock: int = Field(default=50, ge=0)


class ItemReserva(BaseModel):
    id: int
    cantidad: int = Field(ge=1)


class ReservaStockIn(BaseModel):
    items: list[ItemReserva] = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok", "servicio": "inventory"}


@app.post("/reset-data")
def reset_endpoint(_: None = Depends(verify_internal_secret)):
    reset_test_data()
    return {"status": "reset_completed"}


@app.get("/products")
def get_products(
    categoria: str | None = None,
    available_only: bool = True,
    _: None = Depends(verify_internal_secret),
):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, categoria, nombre, precio, descripcion, img, stock, disponible FROM products WHERE 1=1"
    params = []
    if available_only:
        query += " AND disponible = 1 AND stock > 0"
    if categoria and categoria != "todos":
        query += " AND categoria = ?"
        params.append(categoria)
    cur.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"products": rows}


@app.get("/products/{product_id}")
def get_product(product_id: int, _: None = Depends(verify_internal_secret)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, categoria, nombre, precio, descripcion, img, stock, disponible FROM products WHERE id = ?",
        (product_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return dict(row)


@app.post("/products", status_code=201)
def add_product(
    datos: ProductoIn,
    x_authenticated_roles: str | None = Header(default=None),
    _: None = Depends(verify_internal_secret),
):
    roles = [r.strip() for r in (x_authenticated_roles or "").split(",") if r.strip()]
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador para agregar productos")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (categoria, nombre, precio, descripcion, img, stock, disponible) VALUES (?, ?, ?, ?, ?, ?, 1)",
        (datos.categoria, datos.nombre, datos.precio, datos.descripcion, datos.img, datos.stock),
    )
    nuevo_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"id": nuevo_id, **datos.model_dump(), "disponible": 1}


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    x_authenticated_roles: str | None = Header(default=None),
    _: None = Depends(verify_internal_secret),
):
    roles = [r.strip() for r in (x_authenticated_roles or "").split(",") if r.strip()]
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador para eliminar productos")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    cur.execute("UPDATE products SET disponible = 0 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return {"deleted": product_id, "status": "marcado_no_disponible"}


@app.post("/inventory/reserve")
def reserve_stock(datos: ReservaStockIn, _: None = Depends(verify_internal_secret)):
    """Operación atómica: comprueba stock de todos los ítems y reserva si es suficiente."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN IMMEDIATE")
        productos_reservados = []
        for it in datos.items:
            cur.execute("SELECT id, nombre, precio, stock, disponible FROM products WHERE id = ?", (it.id,))
            prod = cur.fetchone()
            if not prod:
                conn.rollback()
                raise HTTPException(status_code=400, detail=f"Producto {it.id} no existe")
            if prod["disponible"] == 0 or prod["stock"] < it.cantidad:
                conn.rollback()
                raise HTTPException(
                    status_code=409,
                    detail=f"Stock insuficiente para {prod['nombre']} (disponibles: {prod['stock']}, pedidos: {it.cantidad})",
                )
            cur.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (it.cantidad, it.id))
            productos_reservados.append({"id": prod["id"], "nombre": prod["nombre"], "precio": prod["precio"], "cantidad": it.cantidad})
        conn.commit()
        return {"status": "reserved", "items": productos_reservados}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al reservar inventario: {str(e)}")
    finally:
        conn.close()


@app.post("/inventory/release")
def release_stock(datos: ReservaStockIn, _: None = Depends(verify_internal_secret)):
    """Devuelve el stock en caso de pedido cancelado o pago fallido."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN IMMEDIATE")
        for it in datos.items:
            cur.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (it.cantidad, it.id))
        conn.commit()
        return {"status": "released"}
    finally:
        conn.close()
