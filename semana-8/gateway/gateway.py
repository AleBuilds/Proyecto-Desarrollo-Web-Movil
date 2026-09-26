import os
import secrets

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:9000")

# El timeout global del gateway debe ser mayor al de sus dependencias (Vault).
VAULT_TIMEOUT = 5.0
BACKEND_TIMEOUT = 10.0

if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no está configurado")

app = FastAPI(title="El Mediterráneo - API Gateway")
security = HTTPBearer(auto_error=False)


async def get_gateway_secrets() -> dict:
    """Lee client_token y backend_secret desde Vault (KV v2, ruta secret/gateway)."""
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    try:
        async with httpx.AsyncClient(timeout=VAULT_TIMEOUT) as client:
            response = await client.get(url, headers={"X-Vault-Token": VAULT_TOKEN})
        if response.status_code != 200:
            raise ValueError(f"Vault respondió {response.status_code}")
        return response.json()["data"]["data"]
    except (httpx.RequestError, ValueError, KeyError):
        raise HTTPException(status_code=500, detail="No fue posible acceder a Vault")


async def authenticate_client(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    """Autentica al cliente (front) comparando su token con el guardado en Vault."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Token requerido")

    vault_secrets = await get_gateway_secrets()
    valid = secrets.compare_digest(
        credentials.credentials, vault_secrets.get("client_token", "")
    )
    if not valid:
        raise HTTPException(status_code=401, detail="Token inválido")

    return {
        "client_id": "student-client",
        "backend_secret": vault_secrets["backend_secret"],
    }


@app.get("/health")
async def health():
    """Liveness del gateway; no requiere token ni consulta Vault."""
    return {"status": "ok", "servicio": "gateway"}


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request, auth: dict = Depends(authenticate_client)):
    if ".." in path.split("/"):
        raise HTTPException(status_code=400, detail="Ruta inválida")

    target_url = f"{BACKEND_URL}/{path}"
    body = await request.body()

    headers = {
        "X-Gateway-Secret": auth["backend_secret"],
        "X-Client-Id": auth["client_id"],
    }
    content_type = request.headers.get("content-type")
    if content_type:
        headers["Content-Type"] = content_type

    try:
        async with httpx.AsyncClient(timeout=BACKEND_TIMEOUT) as client:
            backend_response = await client.request(
                method=request.method,
                url=target_url,
                params=list(request.query_params.multi_items()),
                content=body,
                headers=headers,
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Backend no disponible")

    response_headers = {}
    if "content-type" in backend_response.headers:
        response_headers["Content-Type"] = backend_response.headers["content-type"]

    return Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        headers=response_headers,
    )
