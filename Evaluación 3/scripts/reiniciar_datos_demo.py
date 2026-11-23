"""Deja las bases de datos en el estado inicial de la demostración (sin pedidos ni pagos, stock original).

Detenga la plataforma antes de ejecutarlo (scripts\\detener-todo.ps1).
Uso:  py scripts\\reiniciar_datos_demo.py
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for sub in ("auth_service", "services/inventory", "services/orders", "services/clients", "services/payments"):
    sys.path.insert(0, str(RAIZ / sub))

import db_clients
import db_inventory
import db_orders
import db_payments

for modulo in (db_inventory, db_orders, db_clients, db_payments):
    modulo.reset_test_data()
print("Datos de demostración restaurados: sin pedidos ni pagos, stock original. Cuentas por rol intactas.")
