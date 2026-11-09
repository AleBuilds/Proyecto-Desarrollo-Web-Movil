"""Persistencia SQLite para identidades y sesiones (dbIdentity.sqlite)."""
import os
import sqlite3
import hashlib
from pathlib import Path

DB_PATH = Path(os.getenv("AUTH_DB_PATH", Path(__file__).parent / "dbIdentity.sqlite"))


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    derivada = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return f"scrypt${2**14}$8$1${salt.hex()}${derivada.hex()}"


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS identities (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            roles TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            username TEXT NOT NULL,
            roles TEXT NOT NULL,
            expires_at REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES identities(user_id)
        );
    """)
    conn.commit()

    # Sembrar usuarios iniciales si la tabla está vacía
    cur.execute("SELECT COUNT(*) as c FROM identities")
    if cur.fetchone()["c"] == 0:
        usuarios = [
            ("USR-001", "ana", hash_password("1234"), "user"),
            ("USR-002", "silenay", hash_password("silenay123"), "user"),
            ("USR-003", "administrador1", hash_password("admin123"), "user,admin"),
            ("USR-004", "alejandro", hash_password("alejandro123"), "user,admin"),
        ]
        cur.executemany(
            "INSERT INTO identities (user_id, username, password_hash, roles) VALUES (?, ?, ?, ?)",
            usuarios,
        )
        conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("dbIdentity inicializada exitosamente.")
