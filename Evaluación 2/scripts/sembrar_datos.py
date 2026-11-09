"""Script maestro para inicializar y sembrar datos de prueba en todas las bases de datos SQLite."""
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "auth_service"))
sys.path.insert(0, str(RAIZ / "services" / "inventory"))
sys.path.insert(0, str(RAIZ / "services" / "orders"))
sys.path.insert(0, str(RAIZ / "services" / "clients"))
sys.path.insert(0, str(RAIZ / "services" / "payments"))

import db_auth
import db_inventory
import db_orders
import db_clients
import db_payments


def sembrar():
    print("--- Inicializando bases de datos SQLite del Caso 22: El Mediterráneo ---")

    db_auth.init_db()
    print("✓ dbIdentity.sqlite inicializada con identidades (ana, silenay, administrador1, alejandro).")

    db_inventory.init_db()
    print("✓ dbInventory.sqlite inicializada con 9 platos de la carta y stock.")

    db_orders.init_db()
    print("✓ dbOrders.sqlite inicializada con tablas de pedidos, ítems, reservas e idempotencia.")

    db_clients.init_db()
    print("✓ dbClients.sqlite inicializada con perfiles de clientes y datos de contacto protegidos.")

    db_payments.init_db()
    print("✓ dbPayments.sqlite inicializada con tabla de transacciones de pago.")

    print("\n¡Todas las bases de datos están listas para ejecución y pruebas!")


if __name__ == "__main__":
    sembrar()
