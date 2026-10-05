"""Backend (:9000): carta, pedidos y reservas de El Mediterráneo. Solo acepta llamadas del Gateway."""
import os
import secrets
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

INTERNAL_GATEWAY_SECRET = os.getenv("INTERNAL_GATEWAY_SECRET")
if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError("INTERNAL_GATEWAY_SECRET no está configurado")

app = FastAPI(title="Backend El Mediterráneo")
ENVIO = 2500
PRODUCTS: list[dict] = []
ORDERS: list[dict] = []
RESERVATIONS: list[dict] = []

_CARTA = [  # categoría, nombre, precio, descripción, foto (pexels)
    ("hummus", "Hummus Especial", 5200, "Garbanzos molidos con suave crema de sésamo, limón y toque de pimentón.", "1640777"),
    ("falafel", "Falafel Wrap", 4900, "Wrap en pan pita con falafels crujientes, lechuga, tomate y salsa tahini.", "6287525"),
    ("shawarma", "Shawarma Pollo", 6500, "Láminas de pollo marinado con especias finas, vegetales frescos y salsa especial.", "461198"),
    ("parrilla", "Brochetas de Cordero Premium", 14500, "Tiernas brochetas de cordero marinadas a las brasas con pimientos y cebollas.", "2233729"),
    ("pescados", "Pescado del Día", 12000, "Filete de pescado a la plancha con finas hierbas y limón marroquí.", "262959"),
    ("ensaladas", "Ensalada Griega", 5500, "Tomates frescos, pepino, aceitunas kalamata, cebolla morada y queso feta.", "1213710"),
    ("hummus", "Hummus con Carne", 6800, "Hummus suave coronado con carne salteada de ternera y piñones tostados.", "5938/food-salad-healthy-lunch.jpg"),
    ("falafel", "Falafel Plato", 7200, "8 piezas de falafel acompañadas de tabbouleh, hummus y pan pita caliente.", "2092906"),
    ("shawarma", "Shawarma Ternera", 7200, "Cortes selectos de ternera especiada en pan lavash con un par de salsas.", "299347"),
]


def _foto(p: str) -> str:
    ruta = p if "/" in p else f"{p}/pexels-photo-{p}.jpeg"
    return f"https://images.pexels.com/photos/{ruta}?auto=compress&cs=tinysrgb&w=600"


def reset_data() -> None:
    """Restaura los datos de ejemplo (al iniciar y en las pruebas)."""
    PRODUCTS[:] = [
        {"id": i, "categoria": c, "nombre": n, "precio": pr, "descripcion": d, "img": _foto(f)}
        for i, (c, n, pr, d, f) in enumerate(_CARTA, start=1)
    ]
    ORDERS.clear()
    RESERVATIONS.clear()


reset_data()


# ---------- modelos (el cliente nunca envía precios ni totales) ----------
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


class ProductoIn(BaseModel):
    categoria: Literal["hummus", "falafel", "shawarma", "parrilla", "pescados", "ensaladas"]
    nombre: str = Field(min_length=1, max_length=80)
    descripcion: str = Field(default="", max_length=300)
    precio: int = Field(gt=0, le=1_000_000)
    img: str = Field(default="", pattern=r"^(https://[^\s\"'<>]*)?$", max_length=500)


# ---------- seguridad ----------
def verify_gateway(x_gateway_secret: str | None = Header(default=None)) -> None:
    """Rechaza (403) cualquier llamada que no traiga el secreto interno del Gateway."""
    # Se compara en bytes: compare_digest con str lanza TypeError si hay caracteres no ASCII.
    if x_gateway_secret is None or not secrets.compare_digest(
        x_gateway_secret.encode("utf-8"), INTERNAL_GATEWAY_SECRET.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada desde Gateway")


def identidad(
    _: None = Depends(verify_gateway),  # primero se valida el secreto, siempre
    x_authenticated_user: str | None = Header(default=None),
    x_authenticated_username: str | None = Header(default=None),
    x_authenticated_roles: str | None = Header(default=None),
) -> dict:
    """Identidad propagada por el Gateway. Solo se confía en ella si el secreto fue válido."""
    if not x_authenticated_user:
        raise HTTPException(status_code=401, detail="Identidad no informada por el Gateway")
    roles = [r.strip() for r in (x_authenticated_roles or "").split(",") if r.strip()]
    return {"user_id": x_authenticated_user, "username": x_authenticated_username, "roles": roles}


def solo_admin(ident: dict = Depends(identidad)) -> dict:
    if "admin" not in ident["roles"]:
        raise HTTPException(status_code=403, detail="Se requiere el rol admin")
    return ident


# ---------- rutas ----------
@app.get("/health")
def health():
    return {"status": "ok", "servicio": "backend"}


@app.get("/menu")
def menu(_: None = Depends(verify_gateway)):
    """Carta pública: no requiere usuario, pero sí que la llamada venga del Gateway."""
    return {"products": PRODUCTS}


@app.get("/products")
def products(ident: dict = Depends(identidad)):
    return {"authenticated_user": ident["username"], "products": PRODUCTS}


@app.post("/products", status_code=201)
def add_product(datos: ProductoIn, ident: dict = Depends(solo_admin)):
    nuevo = {"id": max((p["id"] for p in PRODUCTS), default=0) + 1, **datos.model_dump()}
    PRODUCTS.append(nuevo)
    return nuevo


@app.delete("/products/{product_id}")
def delete_product(product_id: int, ident: dict = Depends(solo_admin)):
    for producto in PRODUCTS:
        if producto["id"] == product_id:
            PRODUCTS.remove(producto)
            return {"deleted": product_id, "deleted_by": ident["username"]}
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.get("/orders")
def orders(ident: dict = Depends(identidad)):
    visibles = ORDERS if "admin" in ident["roles"] else [o for o in ORDERS if o["user_id"] == ident["user_id"]]
    return {"authenticated_user": ident["username"], "orders": visibles}


@app.post("/orders", status_code=201)
def add_order(datos: PedidoIn, ident: dict = Depends(identidad)):
    if datos.metodo == "delivery" and not datos.direccion.strip():
        raise HTTPException(status_code=400, detail="El delivery requiere dirección")
    por_id = {p["id"]: p for p in PRODUCTS}
    lineas = []
    for it in datos.items:
        if it.id not in por_id:
            raise HTTPException(status_code=400, detail=f"Producto {it.id} no existe")
        p = por_id[it.id]  # el precio sale de la carta del servidor, no del cliente
        lineas.append({"id": p["id"], "nombre": p["nombre"], "precio": p["precio"], "cantidad": it.cantidad})
    subtotal = sum(l["precio"] * l["cantidad"] for l in lineas)
    envio = ENVIO if datos.metodo == "delivery" else 0
    pedido = {
        "id": 1000 + len(ORDERS) + 1, "user_id": ident["user_id"], "username": ident["username"],
        "items": lineas, "metodo": datos.metodo, "nombre": datos.nombre, "telefono": datos.telefono,
        "direccion": datos.direccion, "notas": datos.notas,
        "subtotal": subtotal, "envio": envio, "total": subtotal + envio, "status": "pending",
    }
    ORDERS.append(pedido)
    return pedido


@app.get("/reservations")
def reservations(ident: dict = Depends(identidad)):
    visibles = RESERVATIONS if "admin" in ident["roles"] else [r for r in RESERVATIONS if r["user_id"] == ident["user_id"]]
    return {"reservations": visibles}


@app.post("/reservations", status_code=201)
def add_reservation(datos: ReservaIn, ident: dict = Depends(identidad)):
    reserva = {"id": len(RESERVATIONS) + 1, "user_id": ident["user_id"], "username": ident["username"], **datos.model_dump()}
    RESERVATIONS.append(reserva)
    return reserva
