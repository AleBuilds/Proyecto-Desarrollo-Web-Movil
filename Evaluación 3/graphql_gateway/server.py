"""GraphQL Gateway (:8050): Servidor FastAPI con Strawberry GraphQL.
Provee agregaciones seguras entre Orders, Inventory y Clients.
Aplica validación de profundidad y autorización por campo.
"""
import os
import secrets
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter

from schema import schema

INTERNAL_SERVICE_SECRET = os.environ["INTERNAL_SERVICE_SECRET"]
MAX_QUERY_DEPTH = 6


def calcular_profundidad_query(query_str: str) -> int:
    """Validador C3 de consultas: evita ataques de profundidad excesiva (DSL D_F04_GraphQL_Limite_C3)."""
    profundidad_max = 0
    actual = 0
    for char in query_str:
        if char == "{":
            actual += 1
            if actual > profundidad_max:
                profundidad_max = actual
        elif char == "}":
            actual = max(0, actual - 1)
    return profundidad_max


async def get_context(request: Request, response: Response):
    return {"request": request, "response": response}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="GraphQL Gateway - El Mediterráneo")


@app.middleware("http")
async def depth_limit_middleware(request: Request, call_next):
    # Servicio privado: solo el API Gateway (que porta el secreto interno) puede invocarlo.
    if request.url.path.startswith("/graphql"):
        recibido = request.headers.get("X-Internal-Secret", "")
        if not secrets.compare_digest(recibido.encode("utf-8"), INTERNAL_SERVICE_SECRET.encode("utf-8")):
            return JSONResponse(status_code=403, content={"detail": "Acceso no autorizado al GraphQL Gateway privado"})
    if request.url.path == "/graphql" and request.method == "POST":
        body_bytes = await request.body()
        try:
            import json
            data = json.loads(body_bytes.decode("utf-8"))
            query = data.get("query", "")
            if query:
                prof = calcular_profundidad_query(query)
                if prof > MAX_QUERY_DEPTH:
                    return JSONResponse(
                        status_code=400,
                        content={"detail": f"Consulta rechazada: la profundidad ({prof}) supera el límite permitido ({MAX_QUERY_DEPTH})"},
                    )
        except Exception:
            pass
        # Re-inyectar el body
        async def receive():
            return {"type": "http.request", "body": body_bytes}
        request = Request(request.scope, receive=receive)
    return await call_next(request)


app.include_router(graphql_app, prefix="/graphql")


@app.get("/health")
def health():
    return {"status": "ok", "servicio": "graphql_gateway"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8050, reload=False)
