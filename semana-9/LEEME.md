# El Mediterráneo — Semana 9: Autenticación, Autorización, API Gateway, Vault, Backend y Frontend

Flujo: **Navegador → Gateway (cookie HttpOnly) → Auth Service (introspección) → Vault → Backend**.

| Servicio | Puerto | Archivo |
|---|---|---|
| Gateway + frontend | 8000 | `gateway/gateway.py`, `gateway/static/` |
| Auth Service | 8100 | `auth/auth_service.py` |
| Backend | 9000 | `backend/backend_api.py` |
| Vault (modo dev) | 8200 | `vault-setup.ps1` carga los secretos |

Usuarios simulados: `ana / 1234` (cliente, rol user) y `ernesto / admin123` (admin).

## Qué hace cada rol
- **Sin sesión:** inicio y carta (`GET /public/menu`), carrito.
- **Cliente (user):** confirmar pedidos, reservar mesa, ver *sus* pedidos y reservas.
- **Admin:** además crea/elimina platos y ve todos los pedidos y reservas.
- El total de un pedido lo calcula el backend con los precios de la carta; el cliente nunca envía precios.

El frontend es una página HTML (`gateway/static/`) servida por el Gateway en el mismo origen, por eso la cookie HttpOnly funciona sin CORS.

## Arranque (sin Docker)

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt   # solo la primera vez
.\iniciar-todo.ps1                                            # abre 4 ventanas
```
Luego abre http://localhost:8000

## Pruebas

```powershell
.venv\Scripts\python.exe -m pytest tests -q                 # unitarias (no necesitan el sistema levantado)
.venv\Scripts\python.exe -m pytest e2e\test_stack.py -q     # integración (sistema levantado)
# Navegador (sistema levantado): pip install pytest-playwright ; playwright install chromium
.venv\Scripts\python.exe -m pytest e2e\test_frontend.py --headed
```

Nota: el backend guarda carta, pedidos y reservas en memoria (se pierden al reiniciarlo). 
