"""Persistencia SQLite para pagos y cobros (dbPayments.sqlite)."""
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("PAYMENTS_DB_PATH", Path(__file__).parent / "dbPayments.sqlite"))


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL UNIQUE,
            user_id TEXT NOT NULL,
            monto INTEGER NOT NULL,
            metodo_pago TEXT NOT NULL,
            estado TEXT NOT NULL,
            transaccion_proveedor_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def reset_test_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS payments")
    conn.commit()
    conn.close()
    init_db()


if __name__ == "__main__":
    init_db()
    print("dbPayments inicializada exitosamente.")
