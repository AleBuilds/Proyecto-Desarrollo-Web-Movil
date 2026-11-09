"""Auth Service (:8100): verifica credenciales, emite sesiones opacas con scrypt, introspecciona y revoca.
Persistencia en dbIdentity.sqlite.
"""
import hashlib
import hmac
import os
import secrets
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from db_auth import get_connection, init_db, hash_password

AUTH_INTROSPECTION_SECRET = os.getenv("AUTH_INTROSPECTION_SECRET", "gateway-auth-secret-789")
SESSION_TTL = int(os.getenv("SESSION_TTL", "900"))  # 15 minutos


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Auth Service - El Mediterráneo", lifespan=lifespan)


def verify_password(password: str, almacenado: str) -> bool:
    try:
        algoritmo, n, r, p, sal_hex, hash_hex = almacenado.split("$")
        if algoritmo != "scrypt":
            return False
        esperada = bytes.fromhex(hash_hex)
        derivada = hashlib.scrypt(
            password.encode("utf-8"),
            salt=bytes.fromhex(sal_hex),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(esperada),
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(derivada, esperada)


_HASH_FALSO = "scrypt$16384$8$1$c61e72e49e7878eee0624f718278ab79$31956daeccf4db080d25441142e77c7ba158083211c1bb040f705e8b2221d10f"


def verificar_secreto_introspeccion(
    x_introspection_secret: str | None = Header(default=None),
) -> None:
    if x_introspection_secret is None or not secrets.compare_digest(
        x_introspection_secret.encode("utf-8"), AUTH_INTROSPECTION_SECRET.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada para introspección")


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class TokenIn(BaseModel):
    token: str = Field(min_length=1, max_length=512)


def limpiar_expiradas():
    ahora = time.time()
    conn = get_connection()
    conn.execute("DELETE FROM sessions WHERE expires_at <= ?", (ahora,))
    conn.commit()
    conn.close()


@app.get("/health")
def health():
    return {"status": "ok", "servicio": "auth_service"}


@app.post("/login")
def login(datos: LoginIn):
    limpiar_expiradas()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, password_hash, roles FROM identities WHERE username = ?", (datos.username,))
    usuario = cur.fetchone()

    hash_a_probar = usuario["password_hash"] if usuario else _HASH_FALSO
    valido = verify_password(datos.password, hash_a_probar)

    if usuario is None or not valido:
        conn.close()
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = secrets.token_hex(32)
    ahora = time.time()
    expira = ahora + SESSION_TTL

    cur.execute(
        "INSERT INTO sessions (token, user_id, username, roles, expires_at) VALUES (?, ?, ?, ?, ?)",
        (token, usuario["user_id"], usuario["username"], usuario["roles"], expira),
    )
    conn.commit()
    conn.close()

    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": SESSION_TTL,
        "user_id": usuario["user_id"],
        "username": usuario["username"],
        "roles": [r.strip() for r in usuario["roles"].split(",") if r.strip()],
    }


@app.post("/introspect")
def introspect(datos: TokenIn, _: None = Depends(verificar_secreto_introspeccion)):
    limpiar_expiradas()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, username, roles, expires_at FROM sessions WHERE token = ?",
        (datos.token,),
    )
    sesion = cur.fetchone()
    conn.close()

    if not sesion or sesion["expires_at"] <= time.time():
        return {"active": False}

    roles_list = [r.strip() for r in sesion["roles"].split(",") if r.strip()]
    return {
        "active": True,
        "user_id": sesion["user_id"],
        "username": sesion["username"],
        "roles": roles_list,
        "exp": int(sesion["expires_at"]),
    }


@app.post("/logout")
def logout(datos: TokenIn, _: None = Depends(verificar_secreto_introspeccion)):
    conn = get_connection()
    conn.execute("DELETE FROM sessions WHERE token = ?", (datos.token,))
    conn.commit()
    conn.close()
    return {"status": "logged_out"}
