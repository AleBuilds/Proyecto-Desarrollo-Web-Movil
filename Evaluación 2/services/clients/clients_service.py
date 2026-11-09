"""Microservicio Clients (:9003): Gestión de perfiles y datos personales de clientes.
Persistencia en dbClients.sqlite.
Aplica principio de menor privilegio: solo entrega datos al titular o al rol admin.
"""
import os
import secrets
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from db_clients import get_connection, init_db, reset_test_data

INTERNAL_SERVICE_SECRET = os.getenv("INTERNAL_SERVICE_SECRET", "gateway-api-secret-456")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Clients Microservice - El Mediterráneo", lifespan=lifespan)


def verify_internal_secret(x_internal_secret: str | None = Header(default=None)):
    if x_internal_secret is None or not secrets.compare_digest(
        x_internal_secret.encode("utf-8"), INTERNAL_SERVICE_SECRET.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Acceso no autorizado al servicio privado clients")


class PerfilUpdateIn(BaseModel):
    nombre_completo: str = Field(min_length=1, max_length=100)
    telefono: str = Field(min_length=6, max_length=25)
    direccion_frecuente: str = Field(min_length=3, max_length=200)
    notas_preferencias: str = Field(default="", max_length=300)


@app.get("/health")
def health():
    return {"status": "ok", "servicio": "clients"}


@app.post("/reset-data")
def reset_endpoint(_: None = Depends(verify_internal_secret)):
    reset_test_data()
    return {"status": "reset_completed"}


@app.get("/clients/me")
def get_my_profile(
    x_authenticated_user: str | None = Header(default=None),
    _: None = Depends(verify_internal_secret),
):
    if not x_authenticated_user:
        raise HTTPException(status_code=401, detail="Contexto de usuario no provisto")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, username, nombre_completo, email, telefono, direccion_frecuente, notas_preferencias FROM clients WHERE user_id = ?",
        (x_authenticated_user,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Perfil de cliente no encontrado")
    return dict(row)


@app.put("/clients/me")
def update_my_profile(
    datos: PerfilUpdateIn,
    x_authenticated_user: str | None = Header(default=None),
    _: None = Depends(verify_internal_secret),
):
    if not x_authenticated_user:
        raise HTTPException(status_code=401, detail="Contexto de usuario no provisto")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """UPDATE clients SET nombre_completo = ?, telefono = ?, direccion_frecuente = ?, notas_preferencias = ?
           WHERE user_id = ?""",
        (datos.nombre_completo, datos.telefono, datos.direccion_frecuente, datos.notas_preferencias, x_authenticated_user),
    )
    conn.commit()
    conn.close()
    return {"status": "updated", **datos.model_dump()}


@app.get("/clients/{user_id}")
def get_client_by_id(
    user_id: str,
    x_authenticated_roles: str | None = Header(default=None),
    _: None = Depends(verify_internal_secret),
):
    roles = [r.strip() for r in (x_authenticated_roles or "").split(",") if r.strip()]
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Solo administradores pueden consultar otros clientes")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, username, nombre_completo, email, telefono, direccion_frecuente, notas_preferencias FROM clients WHERE user_id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return dict(row)
