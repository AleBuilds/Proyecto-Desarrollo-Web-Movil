"""Pruebas de endurecimiento: secretos fuera del código, rate limit y correlación de logs."""
import os
import re
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

import gateway

RAIZ = Path(__file__).resolve().parent.parent


def test_no_hay_secretos_incrustados_en_codigo_ni_configuracion():
    """Ningún .py/.yml/.md/.ps1 entregado contiene un valor de secreto literal."""
    patron = re.compile(r"""(SECRET\s*[=:]\s*["']?(?!\$|<|os\.|["']))[A-Za-z0-9_\-]{12,}""")
    culpables = []
    for ruta in RAIZ.rglob("*"):
        if ruta.suffix not in {".py", ".yml", ".md", ".ps1", ".js", ".html"} or ".pytest_cache" in ruta.parts:
            continue
        if ruta.name in {"test_hardening.py"}:
            continue
        for n, linea in enumerate(ruta.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if patron.search(linea) and "environ" not in linea and "getenv" not in linea:
                culpables.append(f"{ruta.relative_to(RAIZ)}:{n}")
    assert culpables == []
    assert "gateway-api-secret" not in "".join(
        p.read_text(encoding="utf-8", errors="ignore") for p in RAIZ.rglob("*.py") if p.name != "test_hardening.py"
    )


def test_servicio_falla_al_arrancar_sin_secreto():
    """Fail-fast: sin INTERNAL_SERVICE_SECRET el servicio no levanta con un valor por defecto."""
    entorno = {k: v for k, v in os.environ.items() if k != "INTERNAL_SERVICE_SECRET"}
    r = subprocess.run(
        [sys.executable, "-I", "-c", "import sys; sys.path.insert(0, r'%s'); import inventory_service"
         % (RAIZ / "services" / "inventory")],
        env=entorno, capture_output=True, text=True,
    )
    assert r.returncode != 0
    assert "INTERNAL_SERVICE_SECRET" in r.stderr


def test_rate_limit_de_login_devuelve_429(monkeypatch):
    monkeypatch.setattr(gateway, "RATE_LIMIT_LOGIN_POR_MIN", 3)
    gateway._solicitudes.clear()
    cliente = TestClient(gateway.app)
    codigos = [
        cliente.post("/auth/login", json={"username": "ana", "password": "mala"}).status_code for _ in range(5)
    ]
    assert codigos[:3] == [401, 401, 401]
    assert codigos[3:] == [429, 429]
    r = cliente.post("/auth/login", json={"username": "ana", "password": "mala"})
    assert r.status_code == 429 and int(r.headers["Retry-After"]) >= 1
    gateway._solicitudes.clear()


def test_respuestas_llevan_x_request_id_y_se_respeta_el_valido():
    cliente = TestClient(gateway.app)
    r = cliente.get("/public/menu")
    assert re.fullmatch(r"[0-9a-f]{32}", r.headers["X-Request-ID"])
    r2 = cliente.get("/public/menu", headers={"X-Request-ID": "trace-abc-12345"})
    assert r2.headers["X-Request-ID"] == "trace-abc-12345"
    # Un identificador malicioso se descarta y se genera uno nuevo
    r3 = cliente.get("/public/menu", headers={"X-Request-ID": "x\r\n<script>"})
    assert re.fullmatch(r"[0-9a-f]{32}", r3.headers["X-Request-ID"])


def test_logs_no_contienen_secretos_ni_cookies(caplog):
    import logging
    cliente = TestClient(gateway.app)
    with caplog.at_level(logging.INFO, logger="gateway"):
        cliente.post("/auth/login", json={"username": "ana", "password": "Clave-Incorrecta-Zx9"})
        cliente.post("/auth/login", json={"username": "ana", "password": "1234"})
        token = cliente.cookies.get("session_token")
        cliente.get("/api/orders?secreto=consulta-sensible")
    assert token
    texto = caplog.text
    assert "rid=" in texto
    for prohibido in ("Clave-Incorrecta-Zx9", token, "consulta-sensible",
                      os.environ["INTERNAL_SERVICE_SECRET"], os.environ["AUTH_INTROSPECTION_SECRET"]):
        assert prohibido not in texto
