import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for carpeta in ("auth", "backend", "gateway"):
    sys.path.insert(0, str(RAIZ / carpeta))

# Secretos de prueba (deben fijarse antes de importar los servicios)
os.environ["AUTH_INTROSPECTION_SECRET"] = "gateway-auth-secret-789"
os.environ["INTERNAL_GATEWAY_SECRET"] = "gateway-api-secret-456"
os.environ["VAULT_TOKEN"] = "dev-only-token"
