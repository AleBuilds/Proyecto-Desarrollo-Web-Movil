"""Auth Service (:8100): verifica credenciales, emite sesiones opacas con scrypt, introspecciona y revoca.
Persistencia en dbIdentity.sqlite.
"""
import hashlib
import hmac
import logging
import os
import secrets
import time
import sqlite3
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from db_auth import get_connection, init_db, hash_password

AUTH_INTROSPECTION_SECRET = os.environ["AUTH_INTROSPECTION_SECRET"]
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


logger = logging.getLogger("auth")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [auth] %(message)s"))
    logger.addHandler(_h)
logger.setLevel(logging.INFO)


def verificar_secreto_introspeccion(
    request: Request,
    x_introspection_secret: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
) -> None:
    # Nunca se registra el valor del secreto, solo el resultado de la verificación.
    if x_introspection_secret is None or not secrets.compare_digest(
        x_introspection_secret.encode("utf-8"), AUTH_INTROSPECTION_SECRET.encode("utf-8")
    ):
        logger.warning("rid=%s SECRETO DE INTROSPECCION RECHAZADO %s %s -> 403", x_request_id, request.method, request.url.path)
        raise HTTPException(status_code=403, detail="Solicitud no autorizada para introspección")
    logger.info("rid=%s secreto de introspección VERIFICADO (llamante autorizado: gateway) %s %s",
                x_request_id, request.method, request.url.path)


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class RegistroIn(BaseModel):
    """El rol NO es un campo: toda cuenta nueva nace con rol `user` (campos extra se ignoran)."""
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)


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
def login(datos: LoginIn, x_request_id: str | None = Header(default=None)):
    limpiar_expiradas()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, password_hash, roles FROM identities WHERE username = ?", (datos.username,))
    usuario = cur.fetchone()
    logger.info("rid=%s DB dbIdentity SELECT identities username=%s", x_request_id, datos.username)

    hash_a_probar = usuario["password_hash"] if usuario else _HASH_FALSO
    valido = verify_password(datos.password, hash_a_probar)

    if usuario is None or not valido:
        conn.close()
        logger.warning("rid=%s LOGIN FALLIDO username=%s -> 401", x_request_id, datos.username)
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
    logger.info("rid=%s LOGIN OK username=%s roles=%s; DB dbIdentity INSERT sessions (token opaco no se registra) ttl=%ss",
                x_request_id, usuario["username"], usuario["roles"], SESSION_TTL)

    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": SESSION_TTL,
        "user_id": usuario["user_id"],
        "username": usuario["username"],
        "roles": [r.strip() for r in usuario["roles"].split(",") if r.strip()],
    }


@app.post("/introspect")
def introspect(
    datos: TokenIn,
    _: None = Depends(verificar_secreto_introspeccion),
    x_request_id: str | None = Header(default=None),
):
    limpiar_expiradas()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, username, roles, expires_at FROM sessions WHERE token = ?",
        (datos.token,),
    )
    sesion = cur.fetchone()
    conn.close()
    logger.info("rid=%s DB dbIdentity SELECT sessions (consulta por token, valor no registrado)", x_request_id)

    if not sesion or sesion["expires_at"] <= time.time():
        logger.warning("rid=%s AUTENTICACION: sesión inexistente o expirada -> active=false", x_request_id)
        return {"active": False}

    roles_list = [r.strip() for r in sesion["roles"].split(",") if r.strip()]
    logger.info("rid=%s AUTENTICACION/AUTORIZACION: sesión activa user=%s roles=%s -> active=true",
                x_request_id, sesion["username"], roles_list)
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


@app.post("/register", status_code=201)
def register(datos: RegistroIn, _: None = Depends(verificar_secreto_introspeccion)):
    """Crea una identidad con hash scrypt y sal única. Siempre rol `user`."""
    if datos.password.lower() == datos.username:
        raise HTTPException(status_code=422, detail="La contraseña no puede ser igual al usuario")
    user_id = "USR-" + secrets.token_hex(4).upper()
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO identities (user_id, username, password_hash, roles) VALUES (?, ?, ?, 'user')",
            (user_id, datos.username, hash_password(datos.password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
    finally:
        conn.close()
    return {"user_id": user_id, "username": datos.username, "roles": ["user"]}


@app.delete("/identities/{user_id}")
def delete_identity(user_id: str, _: None = Depends(verificar_secreto_introspeccion)):
    """Compensación del registro: si no se pudo crear el perfil, se revierte la identidad."""
    conn = get_connection()
    conn.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM identities WHERE user_id = ? AND roles = 'user'", (user_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}
