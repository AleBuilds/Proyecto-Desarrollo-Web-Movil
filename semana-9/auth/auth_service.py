"""Auth Service (:8100): verifica credenciales, emite tokens opacos, los introspecciona y los revoca."""
import hashlib
import hmac
import os
import secrets
import time

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

AUTH_INTROSPECTION_SECRET = os.getenv("AUTH_INTROSPECTION_SECRET")
if not AUTH_INTROSPECTION_SECRET:
    raise RuntimeError("AUTH_INTROSPECTION_SECRET no está configurado")

SESSION_TTL = int(os.getenv("SESSION_TTL", "900"))  # segundos (15 min)

app = FastAPI(title="Auth Service")


# ---------- contraseñas ----------
def hash_password(password: str, salt: bytes | None = None) -> str:
    """scrypt con sal por usuario (stdlib). En producción: Argon2 u otro algoritmo dedicado."""
    salt = salt or os.urandom(16)
    derivada = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return f"scrypt${2**14}$8$1${salt.hex()}${derivada.hex()}"


def verify_password(password: str, almacenado: str) -> bool:
    try:
        algoritmo, n, r, p, sal_hex, hash_hex = almacenado.split("$")
        if algoritmo != "scrypt":
            return False
        esperada = bytes.fromhex(hash_hex)
        derivada = hashlib.scrypt(
            password.encode("utf-8"), salt=bytes.fromhex(sal_hex),
            n=int(n), r=int(r), p=int(p), dklen=len(esperada),
        )
    except ValueError:
        return False
    return hmac.compare_digest(derivada, esperada)


# Usuarios simulados (contraseñas: ana -> 1234, administrador1 -> admin123). Solo se guarda el hash.
USERS = {
    "ana": {
        "user_id": "USR-001",
        "password_hash": "scrypt$16384$8$1$539355c655133337e84eb3cbc31d6fdf$d34fc116a55e1c47569ef2bba40e04258ee5a9523ac2c1e87587c54f267fd174",
        "roles": ["user"],
    },
    "administrador1": {
        "user_id": "USR-003",
        "password_hash": "scrypt$16384$8$1$e6309ed0eee01f72b8fc45c91e522490$65a971106ba86842b54ddb132e24920c6770b509b4f7f76d8ccda6015199f96d",
        "roles": ["user", "admin"],
    },
}
# Hash de un usuario inexistente: se verifica igual para no revelar por tiempo qué usuarios existen.
_HASH_FALSO = "scrypt$16384$8$1$c61e72e49e7878eee0624f718278ab79$31956daeccf4db080d25441142e77c7ba158083211c1bb040f705e8b2221d10f"

# token -> sesión (en memoria; en producción: almacenamiento persistente y compartido)
SESSIONS: dict[str, dict] = {}


# ---------- seguridad entre servicios ----------
def verificar_secreto(x_introspection_secret: str | None = Header(default=None)) -> None:
    """Solo el Gateway (que conoce el secreto guardado en Vault) puede introspeccionar o revocar."""
    if x_introspection_secret is None or not secrets.compare_digest(
        x_introspection_secret.encode("utf-8"), AUTH_INTROSPECTION_SECRET.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada")


# ---------- modelos ----------
class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class TokenIn(BaseModel):
    token: str = Field(min_length=1, max_length=512)


def _limpiar_expiradas() -> None:
    ahora = time.time()
    for token in [t for t, s in SESSIONS.items() if s["expires_at"] <= ahora]:
        del SESSIONS[token]


# ---------- rutas ----------
@app.get("/health")
def health():
    return {"status": "ok", "servicio": "auth"}


@app.post("/login")
def login(datos: LoginIn):
    usuario = USERS.get(datos.username)
    valido = verify_password(datos.password, usuario["password_hash"] if usuario else _HASH_FALSO)
    if usuario is None or not valido:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    _limpiar_expiradas()
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {
        "user_id": usuario["user_id"],
        "username": datos.username,
        "roles": list(usuario["roles"]),
        "expires_at": time.time() + SESSION_TTL,
    }
    return {"access_token": token, "token_type": "bearer", "expires_in": SESSION_TTL}


@app.post("/introspect", dependencies=[Depends(verificar_secreto)])
def introspect(datos: TokenIn):
    sesion = SESSIONS.get(datos.token)
    if sesion is None:
        return {"active": False}
    if sesion["expires_at"] <= time.time():
        del SESSIONS[datos.token]
        return {"active": False}
    return {
        "active": True,
        "user_id": sesion["user_id"],
        "username": sesion["username"],
        "roles": sesion["roles"],
    }


@app.post("/logout", dependencies=[Depends(verificar_secreto)])
def logout(datos: TokenIn):
    return {"revoked": SESSIONS.pop(datos.token, None) is not None}
