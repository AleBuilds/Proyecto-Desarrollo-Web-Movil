import os
import secrets

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:9000")
VAULT_TIMEOUT = 5.0
BACKEND_TIMEOUT = 10.0

if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no está configurado")

app = FastAPI(title="El Mediterráneo - API Gateway")
security = HTTPBearer(auto_error=False)


async def get_gateway_secrets() -> dict:
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
    if credentials is None:
        raise HTTPException(status_code=401, detail="Token requerido")

    vault_secrets = await get_gateway_secrets()
    token = credentials.credentials

    if secrets.compare_digest(token, vault_secrets.get("administrador_token", "")):
        role, client_id = "administrador", "admin-client"
    elif secrets.compare_digest(token, vault_secrets.get("usuario_token", "")):
        role, client_id = "usuario", "student-client"
    else:
        raise HTTPException(status_code=401, detail="Token inválido")

    return {
        "client_id": client_id,
        "role": role,
        "backend_secret": vault_secrets["backend_secret"],
    }


def autorizar(role: str, path: str, method: str) -> None:
    if role == "administrador":
        return

    if role == "usuario" and method == "GET" and path == "productos":
        return

    raise HTTPException(
        status_code=403,
        detail="El rol no tiene permisos para realizar esta operación",
    )

@app.get("/health")
async def health():
    return {"status": "ok", "servicio": "gateway"}


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request, auth: dict = Depends(authenticate_client)):
    if ".." in path.split("/"):
        raise HTTPException(status_code=400, detail="Ruta inválida")

    autorizar(auth["role"], path, request.method)

    target_url = f"{BACKEND_URL}/{path}"
    body = await request.body()

    headers = {
        "X-Gateway-Secret": auth["backend_secret"],
        "X-Client-Id": auth["client_id"],
        "X-Client-Role": auth["role"],
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
