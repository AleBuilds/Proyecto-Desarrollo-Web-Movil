import os
import secrets
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

INTERNAL_GATEWAY_SECRET = os.getenv("INTERNAL_GATEWAY_SECRET")
if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError("INTERNAL_GATEWAY_SECRET no está configurado")

app = FastAPI(title="El Mediterráneo - Backend")


def verify_gateway(
    x_gateway_secret: str | None = Header(default=None),
    x_client_id: str | None = Header(default=None),
) -> str:
    """Acepta solo llamadas que vengan del gateway (secreto interno válido)."""
    if x_gateway_secret is None or not secrets.compare_digest(
        x_gateway_secret, INTERNAL_GATEWAY_SECRET
    ):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada desde gateway")
    return x_client_id or "desconocido"


# datos (en memoria)
PRODUCTOS = [
    {"id": 1, "nombre": "Hummus Especial", "categoria": "Hummus", "descripcion": "Crema de garbanzos con tahini y aceite de oliva", "precio": 5200},
    {"id": 2, "nombre": "Falafel Wrap", "categoria": "Falafel", "descripcion": "Croquetas de garbanzo en pan pita con vegetales", "precio": 4900},
    {"id": 3, "nombre": "Shawarma Pollo", "categoria": "Shawarma", "descripcion": "Pollo marinado con salsa de ajo y pickles", "precio": 6500},
    {"id": 4, "nombre": "Brocheta de Carne", "categoria": "Parrilla", "descripcion": "Brocheta a la parrilla con pimientos y cebolla", "precio": 8900},
    {"id": 5, "nombre": "Pescado del Día", "categoria": "Pescados", "descripcion": "Pesca fresca a la plancha con limón", "precio": 12000},
    {"id": 6, "nombre": "Ensalada Griega", "categoria": "Ensaladas", "descripcion": "Tomate, pepino, aceitunas y queso feta", "precio": 5500},
    {"id": 7, "nombre": "Hummus con Carne", "categoria": "Hummus", "descripcion": "Hummus coronado con carne especiada", "precio": 6800},
    {"id": 8, "nombre": "Falafel Plato", "categoria": "Falafel", "descripcion": "Plato de falafel con ensalada y salsa tahini", "precio": 7200},
    {"id": 9, "nombre": "Shawarma Ternera", "categoria": "Shawarma", "descripcion": "Ternera especiada con vegetales frescos", "precio": 7200},
]
PEDIDOS: list[dict] = []
RESERVAS: list[dict] = []


#  modelos
class ItemPedido(BaseModel):
    producto_id: int
    cantidad: int = Field(ge=1, le=50)


class PedidoIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    telefono: str = Field(min_length=6, max_length=20)
    email: str = Field(min_length=5, max_length=120)
    metodo_entrega: Literal["delivery", "retiro"]
    direccion: str | None = Field(default=None, max_length=200)
    items: list[ItemPedido] = Field(min_length=1)


class ReservaIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    telefono: str = Field(min_length=6, max_length=20)
    email: str = Field(min_length=5, max_length=120)
    fecha: str
    hora: str
    personas: int = Field(ge=1, le=20)


# rutas
@app.get("/health")
def health(cliente: str = Depends(verify_gateway)):
    return {"status": "ok", "servicio": "backend", "cliente": cliente}


@app.get("/productos")
def listar_productos(categoria: str | None = None, cliente: str = Depends(verify_gateway)):
    productos = PRODUCTOS
    if categoria:
        productos = [p for p in PRODUCTOS if p["categoria"].lower() == categoria.lower()]
    return {"cliente": cliente, "productos": productos}


@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int, cliente: str = Depends(verify_gateway)):
    for producto in PRODUCTOS:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.post("/pedidos", status_code=201)
def crear_pedido(pedido: PedidoIn, cliente: str = Depends(verify_gateway)):
    if pedido.metodo_entrega == "delivery" and not pedido.direccion:
        raise HTTPException(status_code=422, detail="El delivery requiere dirección")
    precios = {p["id"]: p["precio"] for p in PRODUCTOS}
    total = 0
    for item in pedido.items:
        if item.producto_id not in precios:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no existe")
        total += precios[item.producto_id] * item.cantidad  # el precio lo fija el servidor
    registro = {"id": len(PEDIDOS) + 1001, "total": total, "cliente": cliente, **pedido.model_dump()}
    PEDIDOS.append(registro)
    return registro


@app.get("/pedidos")
def listar_pedidos(cliente: str = Depends(verify_gateway)):
    return {"cliente": cliente, "pedidos": PEDIDOS}


@app.post("/reservas", status_code=201)
def crear_reserva(reserva: ReservaIn, cliente: str = Depends(verify_gateway)):
    registro = {"id": len(RESERVAS) + 1, "cliente": cliente, **reserva.model_dump()}
    RESERVAS.append(registro)
    return registro


@app.get("/reservas")
def listar_reservas(cliente: str = Depends(verify_gateway)):
    return {"cliente": cliente, "reservas": RESERVAS}
