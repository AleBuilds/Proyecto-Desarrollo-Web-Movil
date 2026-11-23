"""Verificación independiente de persistencia (solo lectura) para la demostración del Avance 1.

Consulta directamente las bases SQLite (sin pasar por el frontend ni la API) para comprobar que el
módulo "Realizar pedido" dejó rastro en dbOrders, dbPayments y dbInventory.
No imprime hashes de contraseña ni tokens de sesión.

Uso:  py scripts\\verificar_persistencia.py
"""
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DBS = {
    "orders": RAIZ / "services" / "orders" / "dbOrders.sqlite",
    "payments": RAIZ / "services" / "payments" / "dbPayments.sqlite",
    "inventory": RAIZ / "services" / "inventory" / "dbInventory.sqlite",
    "clients": RAIZ / "services" / "clients" / "dbClients.sqlite",
}


def consulta(nombre: str, sql: str):
    # mode=ro: la conexión no puede modificar la base
    con = sqlite3.connect(f"file:{DBS[nombre]}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    filas = con.execute(sql).fetchall()
    con.close()
    return filas


def mostrar(titulo: str, filas):
    print(f"\n=== {titulo}")
    if not filas:
        print("  (sin filas)")
    for f in filas:
        print("  " + " | ".join(f"{k}={f[k]}" for k in f.keys()))


mostrar("dbOrders.orders (últimos 5 pedidos)",
        consulta("orders", "SELECT id, username, metodo, subtotal, envio, total, status, created_at "
                           "FROM orders ORDER BY id DESC LIMIT 5"))
mostrar("dbOrders.order_items (ítems de los últimos 5 pedidos)",
        consulta("orders", "SELECT order_id, product_id, nombre, precio, cantidad FROM order_items "
                           "WHERE order_id IN (SELECT id FROM orders ORDER BY id DESC LIMIT 5) ORDER BY order_id DESC"))
mostrar("dbPayments.payments (últimos 5 pagos)",
        consulta("payments", "SELECT id, order_id, monto, metodo_pago, estado, transaccion_proveedor_id "
                             "FROM payments ORDER BY id DESC LIMIT 5"))
mostrar("dbInventory.products (stock actual, primeros 5)",
        consulta("inventory", "SELECT id, nombre, precio, stock FROM products ORDER BY id LIMIT 5"))
mostrar("dbClients.contact_messages (últimos mensajes de contacto)",
        consulta("clients", "SELECT id, nombre, email, mensaje, created_at FROM contact_messages ORDER BY id DESC LIMIT 5"))
