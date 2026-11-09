"""Persistencia SQLite para el catálogo e inventario (dbInventory.sqlite)."""
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("INVENTORY_DB_PATH", Path(__file__).parent / "dbInventory.sqlite"))

_CARTA_INICIAL = [
    ("hummus", "Hummus Especial", 5200, "Garbanzos molidos con suave crema de sésamo, limón y toque de pimentón.", "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600", 50),
    ("falafel", "Falafel Wrap", 4900, "Wrap en pan pita con falafels crujientes, lechuga, tomate y salsa tahini.", "https://images.pexels.com/photos/6287525/pexels-photo-6287525.jpeg?auto=compress&cs=tinysrgb&w=600", 45),
    ("shawarma", "Shawarma Pollo", 6500, "Láminas de pollo marinado con especias finas, vegetales frescos y salsa especial.", "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=600", 40),
    ("parrilla", "Brochetas de Cordero Premium", 14500, "Tiernas brochetas de cordero marinadas a las brasas con pimientos y cebollas.", "https://images.pexels.com/photos/2233729/pexels-photo-2233729.jpeg?auto=compress&cs=tinysrgb&w=600", 30),
    ("pescados", "Pescado del Día", 12000, "Filete de pescado a la plancha con finas hierbas y limón marroquí.", "https://images.pexels.com/photos/262959/pexels-photo-262959.jpeg?auto=compress&cs=tinysrgb&w=600", 25),
    ("ensaladas", "Ensalada Griega", 5500, "Tomates frescos, pepino, aceitunas kalamata, cebolla morada y queso feta.", "https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?auto=compress&cs=tinysrgb&w=600", 35),
    ("hummus", "Hummus con Carne", 6800, "Hummus suave coronado con carne salteada de ternera y piñones tostados.", "https://images.pexels.com/photos/5938/food-salad-healthy-lunch.jpg?auto=compress&cs=tinysrgb&w=600", 20),
    ("falafel", "Falafel Plato", 7200, "8 piezas de falafel acompañadas de tabbouleh, hummus y pan pita caliente.", "https://images.pexels.com/photos/2092906/pexels-photo-2092906.jpeg?auto=compress&cs=tinysrgb&w=600", 30),
    ("shawarma", "Shawarma Ternera", 7200, "Cortes selectos de ternera especiada en pan lavash con un par de salsas.", "https://images.pexels.com/photos/299347/pexels-photo-299347.jpeg?auto=compress&cs=tinysrgb&w=600", 35),
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            nombre TEXT NOT NULL,
            precio INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            img TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 50,
            disponible INTEGER NOT NULL DEFAULT 1
        );
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) as c FROM products")
    if cur.fetchone()["c"] == 0:
        cur.executemany(
            "INSERT INTO products (categoria, nombre, precio, descripcion, img, stock, disponible) VALUES (?, ?, ?, ?, ?, ?, 1)",
            _CARTA_INICIAL,
        )
        conn.commit()
    conn.close()


def reset_test_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products")
    conn.commit()
    conn.close()
    init_db()


if __name__ == "__main__":
    init_db()
    print("dbInventory inicializada exitosamente.")
