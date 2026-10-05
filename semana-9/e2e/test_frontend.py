"""Pruebas de navegador (Playwright) sobre la web de El Mediterráneo, con el sistema ya levantado.

    pip install pytest-playwright ; playwright install chromium
    pytest e2e/test_frontend.py --headed        (sin --headed corre en segundo plano)
"""
import os
import re

import httpx
import pytest
from playwright.sync_api import Page, expect

BASE = os.getenv("GATEWAY_URL", "http://localhost:8000")


@pytest.fixture(scope="module", autouse=True)
def sistema_levantado():
    try:
        httpx.get(f"{BASE}/health", timeout=3).raise_for_status()
    except Exception:
        pytest.skip(f"El Gateway no responde en {BASE}: levanta el sistema antes de correr estas pruebas")


@pytest.fixture
def errores(page: Page):
    """Errores de consola y bloqueos de la política de seguridad (ignora fotos externas sin red)."""
    lista = []
    page.on("pageerror", lambda e: lista.append(str(e)))
    page.on("console", lambda m: lista.append(m.text) if m.type == "error" and "ERR_" not in m.text and "Failed to load resource" not in m.text else None)
    return lista


def carta():
    return httpx.get(f"{BASE}/public/menu").json()["products"]


def entrar(page: Page, usuario: str, password: str, esperar: bool = True):
    page.goto(f"{BASE}/#/login")
    page.fill("input[name=username]", usuario)
    page.fill("input[name=password]", password)
    page.click("#f-login button[type=submit]")
    if esperar:
        expect(page.locator("#nav")).to_contain_text(usuario)  # esperar a que la sesión esté lista


def test_carta_publica_sin_sesion(page: Page, errores):
    page.goto(f"{BASE}/#/menu")
    productos = carta()  # el backend guarda en memoria: otras pruebas pueden haber eliminado platos
    expect(page.locator(".card")).to_have_count(len(productos))
    page.click("text=Hummus >> nth=0")  # filtro por categoría
    expect(page.locator(".card")).to_have_count(len([p for p in productos if p["categoria"] == "hummus"]))
    assert errores == []


def test_cliente_pide_reserva_y_no_ve_admin(page: Page, errores):
    primero = carta()[0]
    page.goto(f"{BASE}/#/menu")
    page.click("button[data-agregar] >> nth=0")
    expect(page.locator("#nav")).to_contain_text("Carrito (1)")
    page.goto(f"{BASE}/#/carrito")
    expect(page.locator("#vista")).to_contain_text("Inicia sesión")  # sin sesión no se confirma

    entrar(page, "ana", "1234")
    expect(page.locator("#nav")).to_contain_text("ana")
    # El token no es accesible desde JavaScript: ni en document.cookie ni en localStorage
    assert "session_token" not in page.evaluate("document.cookie")
    assert "tok" not in page.evaluate("JSON.stringify(localStorage)").lower()
    cookie = next(c for c in page.context.cookies() if c["name"] == "session_token")
    assert cookie["httpOnly"] is True

    page.goto(f"{BASE}/#/carrito")
    page.select_option("select[name=metodo]", "delivery")
    page.fill("input[name=nombre]", "Ana Pérez")
    page.fill("input[name=telefono]", "+56912345678")
    page.fill("input[name=direccion]", "Av. Pajaritos 2100, Maipú")
    page.click("#f-pedido button[type=submit]")
    expect(page.locator("#aviso")).to_contain_text(re.compile(r"Pedido #\d+ confirmado"))
    total = f"{primero['precio'] + 2500:,}".replace(",", ".")  # primer plato + envío del delivery
    expect(page.locator("#vista")).to_contain_text(f"Total ${total}")

    page.goto(f"{BASE}/#/reservas")
    page.fill("input[name=fecha]", "2026-10-14")
    page.fill("input[name=hora]", "20:30")
    page.fill("input[name=personas]", "4")
    page.fill("input[name=nombre]", "Ana Pérez")
    page.fill("input[name=telefono]", "+56912345678")
    page.click("#f-reserva button[type=submit]")
    expect(page.locator("#aviso")).to_contain_text("Reserva confirmada")

    expect(page.locator("#nav a", has_text="Admin")).to_have_count(0)
    page.goto(f"{BASE}/#/admin")
    expect(page.locator("#vista")).to_contain_text("403")

    page.click("button[data-salir]")
    expect(page.locator("#nav")).to_contain_text("Ingresar")
    assert httpx.get(f"{BASE}/auth/me", cookies={"session_token": cookie["value"]}).status_code == 401  # sesión revocada
    assert errores == []


def test_login_incorrecto(page: Page):
    entrar(page, "ana", "incorrecta", esperar=False)
    expect(page.locator("#aviso")).to_contain_text("incorrectos")
    expect(page.locator("#nav")).to_contain_text("Ingresar")


def test_admin_gestiona_la_carta(page: Page, errores):
    entrar(page, "ernesto", "admin123")
    page.goto(f"{BASE}/#/admin")
    page.fill("#f-plato input[name=nombre]", "Dorada a la sal")
    page.fill("#f-plato input[name=precio]", "13500")
    page.click("#f-plato button[type=submit]")
    expect(page.locator("#aviso")).to_contain_text("Plato agregado")
    expect(page.locator("#vista")).to_contain_text("Dorada a la sal")
    page.click("div.fila:has-text('Dorada a la sal') button")
    expect(page.locator("#aviso")).to_contain_text("Plato eliminado")
    expect(page.locator("#vista")).not_to_contain_text("Dorada a la sal")
    assert errores == []
