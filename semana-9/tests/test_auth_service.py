import pytest
from fastapi.testclient import TestClient

import auth_service

SECRETO = {"X-Introspection-Secret": "gateway-auth-secret-789"}
client = TestClient(auth_service.app)


@pytest.fixture(autouse=True)
def sesiones_limpias():
    auth_service.SESSIONS.clear()
    yield
    auth_service.SESSIONS.clear()


def login(usuario="ana", password="1234"):
    return client.post("/login", json={"username": usuario, "password": password})


def test_login_valido_entrega_token():
    r = login()
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["token_type"] == "bearer"
    assert cuerpo["expires_in"] == 900
    assert len(cuerpo["access_token"]) >= 32


def test_login_con_password_incorrecta_no_crea_sesion():
    r = login(password="incorrecta")
    assert r.status_code == 401
    assert auth_service.SESSIONS == {}


def test_login_usuario_inexistente():
    assert login("nadie", "1234").status_code == 401


def test_las_passwords_no_se_guardan_en_texto_plano():
    for datos in auth_service.USERS.values():
        assert "1234" not in datos["password_hash"] and "admin123" not in datos["password_hash"]
    assert auth_service.verify_password("1234", auth_service.USERS["ana"]["password_hash"])
    assert not auth_service.verify_password("otra", auth_service.USERS["ana"]["password_hash"])


def test_introspection_de_token_valido():
    token = login().json()["access_token"]
    r = client.post("/introspect", json={"token": token}, headers=SECRETO)
    assert r.status_code == 200
    assert r.json() == {"active": True, "user_id": "USR-001", "username": "ana", "roles": ["user"]}


def test_ernesto_tiene_rol_admin():
    token = login("ernesto", "admin123").json()["access_token"]
    r = client.post("/introspect", json={"token": token}, headers=SECRETO).json()
    assert r["roles"] == ["user", "admin"] and r["user_id"] == "USR-003"


def test_introspection_de_token_inexistente():
    r = client.post("/introspect", json={"token": "no-existe"}, headers=SECRETO)
    assert r.status_code == 200 and r.json() == {"active": False}


@pytest.mark.parametrize("cabeceras", [{}, {"X-Introspection-Secret": "incorrecto"}, {"X-Introspection-Secret": b"\xf1and\xfa"}])
def test_introspect_y_logout_exigen_secreto_del_gateway(cabeceras):
    token = login().json()["access_token"]
    assert client.post("/introspect", json={"token": token}, headers=cabeceras).status_code == 403
    assert client.post("/logout", json={"token": token}, headers=cabeceras).status_code == 403
    assert token in auth_service.SESSIONS  # el logout rechazado no revocó nada


def test_logout_revoca_la_sesion():
    token = login().json()["access_token"]
    r = client.post("/logout", json={"token": token}, headers=SECRETO)
    assert r.status_code == 200 and r.json() == {"revoked": True}
    assert client.post("/introspect", json={"token": token}, headers=SECRETO).json() == {"active": False}


def test_token_expirado_deja_de_estar_activo(monkeypatch):
    token = login().json()["access_token"]
    ahora = auth_service.time.time()
    monkeypatch.setattr(auth_service.time, "time", lambda: ahora + 901)
    assert client.post("/introspect", json={"token": token}, headers=SECRETO).json() == {"active": False}
    assert token not in auth_service.SESSIONS
