"""Persistencia SQLite para perfiles de clientes (dbClients.sqlite)."""
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("CLIENTS_DB_PATH", Path(__file__).parent / "dbClients.sqlite"))

_CLIENTES_INICIALES = [
    ("USR-001", "ana", "Ana García", "ana@elmediterraneo.cl", "+56912345678", "Av. Pajaritos 2100, Maipú", "Sin cebolla en ensaladas"),
    ("USR-002", "silenay", "Silenay Sarmiento", "silenay@elmediterraneo.cl", "+56987654321", "Av. Américo Vespucio 1500, Maipú", "Extra salsa de ajo"),
    ("USR-003", "administrador1", "Administrador General", "admin@elmediterraneo.cl", "+56911223344", "Av. del Mar 1042", "Personal de operaciones"),
    ("USR-004", "alejandro", "Alejandro Narváez", "alejandro@elmediterraneo.cl", "+56999887766", "Av. Pajaritos 1234, Maipú", "Cliente frecuente"),
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            nombre_completo TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion_frecuente TEXT NOT NULL,
            notas_preferencias TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) as c FROM clients")
    if cur.fetchone()["c"] == 0:
        cur.executemany(
            "INSERT INTO clients (user_id, username, nombre_completo, email, telefono, direccion_frecuente, notas_preferencias) VALUES (?, ?, ?, ?, ?, ?, ?)",
            _CLIENTES_INICIALES,
        )
        conn.commit()
    conn.close()


def reset_test_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS clients")
    conn.commit()
    conn.close()
    init_db()


if __name__ == "__main__":
    init_db()
    print("dbClients inicializada exitosamente.")
