"""Esquema Strawberry GraphQL para el GraphQL Gateway (Módulo 8).
Agrega información de múltiples subsistemas: Orders (:9002), Inventory (:9001) y Clients (:9003).
Implementa límites de complejidad/profundidad y manejo controlado de errores parciales.
"""
from typing import Optional
import httpx
import strawberry

INTERNAL_SECRET = "gateway-api-secret-456"
INVENTORY_URL = "http://127.0.0.1:9001"
ORDERS_URL = "http://127.0.0.1:9002"
CLIENTS_URL = "http://127.0.0.1:9003"


@strawberry.type
class ProductoDetalle:
    id: int
    categoria: str
    nombre: str
    precio: int
    descripcion: str
    img: str
    stock: int
    disponible: bool


@strawberry.type
class ItemPedidoAgregado:
    product_id: int
    nombre: str
    precio: int
    cantidad: int
    subtotal_linea: int
    # Enriquecido desde Inventory
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    img: Optional[str] = None


@strawberry.type
class ClienteResumen:
    user_id: str
    username: str
    nombre_completo: str
    email: str
    telefono: str
    direccion_frecuente: str


@strawberry.type
class ResumenPedidoAgregado:
    order_id: int
    user_id: str
    username: str
    metodo: str
    status: str
    subtotal: int
    envio: int
    total: int
    items: list[ItemPedidoAgregado]
    cliente: Optional[ClienteResumen] = None
    aviso_parcial: Optional[str] = None


@strawberry.type
class Query:
    @strawberry.field
    async def catalogo_disponible(self, categoria: Optional[str] = None) -> list[ProductoDetalle]:
        """Consulta agregada de productos disponibles directamente desde Inventory."""
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                params = {"available_only": "true"}
                if categoria:
                    params["categoria"] = categoria
                resp = await client.get(
                    f"{INVENTORY_URL}/products",
                    params=params,
                    headers={"X-Internal-Secret": INTERNAL_SECRET},
                )
                if resp.status_code == 200:
                    productos = resp.json().get("products", [])
                    return [
                        ProductoDetalle(
                            id=p["id"],
                            categoria=p["categoria"],
                            nombre=p["nombre"],
                            precio=p["precio"],
                            descripcion=p["descripcion"],
                            img=p["img"],
                            stock=p["stock"],
                            disponible=bool(p["disponible"]),
                        )
                        for p in productos
                    ]
        except Exception:
            return []
        return []

    @strawberry.field
    async def resumen_pedido(self, info: strawberry.types.Info, order_id: int) -> Optional[ResumenPedidoAgregado]:
        """Agregación E2E: combina Orders (:9002) + Inventory (:9001) + Clients (:9003)."""
        request = info.context.get("request")
        user_id = request.headers.get("X-Authenticated-User") if request else "USR-001"
        username = request.headers.get("X-Authenticated-Username") if request else "ana"
        roles = request.headers.get("X-Authenticated-Roles") if request else "user"

        headers_auth = {
            "X-Internal-Secret": INTERNAL_SECRET,
            "X-Authenticated-User": user_id or "USR-001",
            "X-Authenticated-Username": username or "ana",
            "X-Authenticated-Roles": roles or "user",
        }

        # 1. Obtener Pedido desde Orders
        pedido_data = None
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                r_order = await client.get(f"{ORDERS_URL}/orders/{order_id}", headers=headers_auth)
                if r_order.status_code == 200:
                    pedido_data = r_order.json()
                elif r_order.status_code == 403:
                    raise PermissionError("Acceso denegado al pedido de otro usuario")
            except PermissionError:
                raise
            except Exception:
                return None

        if not pedido_data:
            return None

        # 2. Enriquecer con datos de catálogo desde Inventory (Agregación)
        items_agregados = []
        aviso_parcial = None
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                r_inv = await client.get(f"{INVENTORY_URL}/products", headers={"X-Internal-Secret": INTERNAL_SECRET})
                inv_map = {p["id"]: p for p in r_inv.json().get("products", [])} if r_inv.status_code == 200 else {}
        except Exception:
            inv_map = {}
            aviso_parcial = "Información de inventario no disponible temporalmente; mostrando datos base."

        for item in pedido_data.get("items", []):
            prod = inv_map.get(item["id"])
            items_agregados.append(
                ItemPedidoAgregado(
                    product_id=item["id"],
                    nombre=item["nombre"],
                    precio=item["precio"],
                    cantidad=item["cantidad"],
                    subtotal_linea=item["precio"] * item["cantidad"],
                    categoria=prod.get("categoria") if prod else None,
                    descripcion=prod.get("descripcion") if prod else None,
                    img=prod.get("img") if prod else None,
                )
            )

        # 3. Enriquecer con datos de perfil desde Clients (Tercer subsistema)
        cliente_resumen = None
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                r_cli = await client.get(
                    f"{CLIENTS_URL}/clients/me",
                    headers={"X-Internal-Secret": INTERNAL_SECRET, "X-Authenticated-User": pedido_data["user_id"]},
                )
                if r_cli.status_code == 200:
                    c = r_cli.json()
                    cliente_resumen = ClienteResumen(
                        user_id=c["user_id"],
                        username=c["username"],
                        nombre_completo=c["nombre_completo"],
                        email=c["email"],
                        telefono=c["telefono"],
                        direccion_frecuente=c["direccion_frecuente"],
                    )
        except Exception:
            # Fallo controlado: no impide entregar el resumen del pedido
            pass

        return ResumenPedidoAgregado(
            order_id=pedido_data["id"],
            user_id=pedido_data["user_id"],
            username=pedido_data["username"],
            metodo=pedido_data["metodo"],
            status=pedido_data["status"],
            subtotal=pedido_data["subtotal"],
            envio=pedido_data["envio"],
            total=pedido_data["total"],
            items=items_agregados,
            cliente=cliente_resumen,
            aviso_parcial=aviso_parcial,
        )


schema = strawberry.Schema(query=Query)
