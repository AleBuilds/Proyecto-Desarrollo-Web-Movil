# Manual para grabar el video del Avance 1 (Evaluación 3)

**Proyecto:** El Mediterráneo (Caso 22) · **Equipo:** Silenay Sarmiento y Alejandro Narváez
**Entrega:** video en Canvas → Evaluaciones → "Video Seguimiento"
**Módulo que se demuestra:** **Realizar un pedido** (carrito → entrega → confirmación)

> Se eligió "Realizar pedido" porque es el único flujo que atraviesa **todas** las capas que pide el profe:
> frontend → API Gateway → Auth Service → Orders → (Inventory + Payments) → bases de datos SQLite.

---

## 1. Qué pide el profe y dónde se ve cada punto

| # | Lo que pide | Qué se muestra | Dónde |
|---|---|---|---|
| 1 | **Frontend**: en el navegador, pestaña *Red/Network*, que llamó al API Gateway | Petición `POST /api/orders` a `127.0.0.1:8000` con respuesta 201 y cabecera `X-Request-ID` | Chrome/Edge → F12 → Network |
| 2 | **API Gateway**: en su log, que pidió validación al Auth Service/gestor de secretos y enrutó al backend | Líneas `GATEWAY -> AUTH SERVICE`, `sesión VALIDADA`, `RBAC permitido`, `GATEWAY ENRUTA ... -> :9002/orders` | Ventana **API Gateway :8000** |
| 3 | **Auth Service**: en su log, que validó autenticación/autorización **antes** del enrutamiento | `secreto de introspección VERIFICADO`, `sesión activa user=... roles=...` | Ventana **Auth Service :8100** |
| 4 | **Backend**: en su log, que facilitó o impidió la llamada verificando secretos | `secreto interno VERIFICADO` (Orders, Inventory, Payments) y, en el caso de rechazo, `SECRETO INTERNO RECHAZADO -> 403` | Ventanas **Orders :9002**, **Inventory :9001**, **Payments :9004** |
| 5 | **Persistencia**: que consultó o modificó la base de datos | `DB dbOrders INSERT orders`, `DB dbInventory UPDATE products stock 50 -> 48`, `DB dbPayments INSERT payments` + consulta independiente a las bases | Mismas ventanas + script `verificar_persistencia.py` |

**Hilo conductor:** cada petición lleva un identificador de correlación (`rid=...`, cabecera `X-Request-ID`).
El mismo `rid` aparece en el navegador, en el Gateway, en Auth, en Orders, Inventory y Payments. Eso es lo que
permite decir "este clic produjo exactamente estas líneas".

### Aclaración importante sobre "contenedores"
Este equipo **no tiene Docker instalado** (`docker` no existe en el PowerShell). Los servicios se ejecutan
como procesos independientes, **uno por ventana**, cada uno con su propio puerto y su propia base de datos
(equivalente funcional a un contenedor por servicio). El repositorio incluye un `docker-compose.yml`, pero
**no fue probado en esta máquina**. En el video conviene decirlo con claridad: *"cada servicio corre aislado
en su propia ventana/proceso; el docker-compose está definido pero no lo usamos en esta demostración"*.
Si el profe exige Docker real, hay que instalar Docker Desktop y probarlo antes de grabar.

---

## 2. Cambios hechos en el código para poder demostrarlo (para mencionarlos en el video)

Antes solo el Gateway escribía logs propios. Se agregaron logs **sin exponer secretos, tokens ni cookies** en:

- `gateway/gateway.py`: registra la llamada a Auth (`/introspect` y `/login`), el resultado, la decisión RBAC y el destino del enrutamiento; ahora **propaga el `X-Request-ID` a Auth**.
- `auth_service/auth_service.py`: registra la verificación del secreto de introspección, la consulta a `dbIdentity` y el resultado de la sesión.
- `services/orders`, `inventory`, `payments`, `clients`: registran la verificación del secreto interno (aceptado o rechazado) y cada operación sobre su base de datos. Orders ahora **propaga el `rid`** a Inventory y Payments.
- Scripts nuevos en `scripts/`: `verificar_persistencia.py` (consulta de solo lectura a las bases) y `reiniciar_datos_demo.py` (restaura el estado inicial).

Verificación hecha al implementarlo: la suite automática **41/41 pruebas pasó** con estos cambios, y se comprobó
a mano que el `rid` aparece en las 5 capas.

> Los cambios están en `C:\xampp\htdocs\dwm2026\Proyecto-Desarrollo-Web-Movil\Evaluación 2`. Las carpetas
> `entrega de dwm` y `entrega evaluacion 1 y 2 ...` **no se tocaron** (son lo ya entregado).

---

## 3. Preparación (hacer ANTES de grabar)

Carpeta de trabajo: `C:\xampp\htdocs\dwm2026\Proyecto-Desarrollo-Web-Movil\Evaluación 2`

### 3.1 Dejar todo limpio
```powershell
cd "C:\xampp\htdocs\dwm2026\Proyecto-Desarrollo-Web-Movil\Evaluación 2"
powershell -ExecutionPolicy Bypass -File scripts\detener-todo.ps1
py scripts\reiniciar_datos_demo.py
```
Así el pedido de la demo será el **#1** y el stock del *Hummus Especial* partirá en **50**.

### 3.2 Iniciar la plataforma
```powershell
powershell -ExecutionPolicy Bypass -File scripts\iniciar-todo.ps1
```
Se abren **8 ventanas de PowerShell**, cada una con su título:

`Auth Service :8100` · `Inventory :9001` · `Orders :9002` · `Clients :9003` · `Payments :9004` · `GraphQL Gateway :8050` · `gRPC Delivery :50051` · `API Gateway :8000`

Si dice "Puertos ocupados", ejecutar `scripts\detener-todo.ps1` y repetir.
Comprobar que responde: abrir `http://127.0.0.1:8000/health` → `{"status":"ok","servicio":"api_gateway"}`.

### 3.3 Cuentas de prueba (datos ficticios)
| Rol | Usuario | Contraseña |
|---|---|---|
| Cliente (`user`) | `ana` | `1234` |
| Administrador (`admin`) | `administrador1` | `admin123` |

### 3.4 Distribución de pantalla (para que se vea todo sin cambiar de programa)
- **Izquierda (50 %)**: navegador (Chrome o Edge) en `http://127.0.0.1:8000` con **F12 → pestaña Network** abierta, "Preserve log" activado y el filtro en **Fetch/XHR**.
- **Derecha**: las ventanas de logs, apiladas en dos columnas (Win + flechas). Orden sugerido: API Gateway, Auth Service, Orders, Inventory, Payments.
- Subir el tamaño de letra del terminal (Ctrl + rueda del mouse) para que se lea en el video.
- Una novena ventana de PowerShell libre, en la carpeta del proyecto, para `verificar_persistencia.py`.

### 3.5 Higiene de seguridad (el profe lo valora y el enunciado de la Eval. 3 lo exige)
- **No abrir** `.env` ni mostrarlo en pantalla (contiene los secretos).
- En Network, **no expandir** la sección *Cookies* ni la cabecera `Cookie` (contiene el token de sesión). La cookie es `HttpOnly` y no la ve JavaScript; eso se puede mencionar como control de seguridad.
- Antes de grabar, cerrar WhatsApp, correo y cualquier notificación.

### 3.6 Ensayo
Hacer **un ensayo completo sin grabar**, y luego repetir 3.1 y 3.2 (el ensayo deja un pedido en la base y baja el stock).

---

## 4. Guion de grabación (duración objetivo: 6 a 8 minutos)

Grabar con la barra de juegos de Windows (Win + G) o OBS, pantalla completa, con micrófono.
*Cursiva = lo que se puede decir.*

### Escena 0 — Introducción (30 s)
Mostrar las 8 ventanas y el navegador.
*"Somos Silenay Sarmiento y Alejandro Narváez. Este es el Avance 1 de la Evaluación 3 del caso El Mediterráneo. Voy a demostrar el módulo 'Realizar pedido' atravesando todas las capas: frontend, API Gateway, Auth Service, backend y persistencia. Cada servicio corre aislado en su propia ventana y su propia base de datos. No usamos Docker en esta máquina; el docker-compose está definido pero esta demostración es con procesos independientes."*

### Escena 1 — Frontend inicia sesión y hace el pedido (1 min 30 s)
1. En el navegador, clic en **Ingresar** → usuario `ana`, contraseña `1234`.
2. Ir a **Menú**, abrir *Hummus Especial*, subir la cantidad a **2** con el botón `+` y pulsar **Agregar al Carrito**.
3. **Carrito → Continuar** (llega a Entrega): método **Retiro en Local**, nombre "Ana Demo", teléfono `+56911112222` → **Confirmar Pedido y Pagar**.
4. Llegará a la pantalla de confirmación.

*"Al iniciar sesión el navegador no guarda ningún token en localStorage: la sesión va en una cookie HttpOnly que emite el servidor."*

### Escena 2 — Punto 1: Network del navegador (1 min)
En F12 → Network, seleccionar la petición **`orders`** (`POST`):
- **Headers → General**: *Request URL* `http://127.0.0.1:8000/api/orders` → "el frontend llama al **API Gateway**, puerto 8000; nunca a los microservicios".
- **Headers → Response Headers**: copiar/mostrar **`X-Request-ID`** (ej. `3f9c…`). **Anotar o dejar visible este valor.**
- Status **201 Created**.
- **Payload**: se ve que el navegador envía solo `id` y `cantidad` de cada producto, **no precios** ("el precio lo calcula el servidor").
- **Response**: pedido `id: 1`, `total: 10400`, `status: confirmed`.
- Mostrar también la petición `me` y `login` anteriores.

*"Este X-Request-ID es el identificador de correlación. Lo voy a seguir por todas las capas."*

### Escena 3 — Punto 2: log del API Gateway (1 min)
Ir a la ventana **API Gateway :8000** y buscar las líneas con el mismo `rid`. Deben verse en este orden:
```
GATEWAY -> AUTH SERVICE: solicita validación de sesión (POST http://127.0.0.1:8100/introspect, secreto adjunto no registrado)
AUTH SERVICE -> GATEWAY: respuesta 200
sesión VALIDADA por Auth Service: user=ana roles=['user']
RBAC permitido user=ana POST /orders
GATEWAY ENRUTA POST /api/orders -> http://127.0.0.1:9002/orders (inyecta secreto interno y contexto de identidad)
BACKEND http://127.0.0.1:9002 respondió 201
```
*"El Gateway no confía en el navegador: primero pregunta al Auth Service si la sesión es válida, luego aplica la matriz de permisos por rol, y recién entonces enruta a Orders agregando el secreto interno. El valor del secreto no aparece en el log."*

### Escena 4 — Punto 3: log del Auth Service (45 s)
Ventana **Auth Service :8100**, mismo `rid`:
```
secreto de introspección VERIFICADO (llamante autorizado: gateway) POST /introspect
DB dbIdentity SELECT sessions (consulta por token, valor no registrado)
AUTENTICACION/AUTORIZACION: sesión activa user=ana roles=['user'] -> active=true
```
*"Fíjense en la hora: esta validación ocurre **antes** de la línea 'GATEWAY ENRUTA' del Gateway. Además, el Auth Service solo atiende al Gateway porque exige su propio secreto."*

### Escena 5 — Punto 4: log del backend verificando secretos (1 min)
Ventanas **Orders**, **Inventory** y **Payments**, mismo `rid`:
```
[orders]    secreto interno VERIFICADO POST /orders
[orders]    identidad recibida del gateway user=ana roles=user
[inventory] secreto interno VERIFICADO POST /inventory/reserve
[payments]  secreto de payments VERIFICADO POST /payments/process
```
*"Cada servicio privado verifica un secreto antes de actuar. Payments usa un secreto distinto, que solo posee Orders: el Gateway ni siquiera puede llamarlo."*

### Escena 6 — Punto 5: persistencia (1 min 30 s)
**a) En los logs** (mismo `rid`):
```
[orders]    DB dbOrders SELECT idempotency_records -> clave nueva
[inventory] DB dbInventory UPDATE products id=1 'Hummus Especial' stock 50 -> 48
[inventory] DB dbInventory COMMIT reserva de stock (1 productos)
[orders]    DB dbOrders INSERT orders id=1 total=10400 status=pending
[orders]    DB dbOrders INSERT order_items (1 filas) order_id=1
[payments]  DB dbPayments INSERT payments id=1 order_id=1 monto=10400 estado=approved COMMIT
[orders]    DB dbOrders UPDATE orders id=1 status=confirmed
[orders]    DB dbOrders COMMIT pedido id=1 status=confirmed
```
**b) Verificación independiente** (sin pasar por el frontend), en la ventana libre:
```powershell
py scripts\verificar_persistencia.py
```
Debe mostrar: el pedido #1 (`total=10400`, `confirmed`), su ítem, el pago `approved` con código `TX-MED-1-...` y el stock del *Hummus Especial* en **48**.

*"Esto lee las bases SQLite directamente en modo solo lectura. El pedido existe, el pago está aprobado y el stock bajó de 50 a 48. Coincide con lo que mostró la pantalla."*

### Escena 7 — Rechazo controlado (1 min 30 s) *(recomendada: demuestra que el sistema también impide)*
**a) Sin permiso por rol.** En la consola del navegador (F12 → Console), con la sesión de `ana`:
```js
fetch('/api/products/1', {method:'DELETE', credentials:'include'}).then(r => r.status)
```
Resultado **403**. En el log del Gateway: `RBAC DENEGADO user=ana roles=['user'] DELETE /products/1 -> 403`.
*"Un cliente no puede borrar platos. Se rechaza en el Gateway y la petición nunca llega a Inventory."*

**b) Llamada directa al backend con secreto incorrecto**, en la ventana libre:
```powershell
curl.exe -s -w " -> %{http_code}`n" -H "X-Internal-Secret: incorrecto" http://127.0.0.1:9002/orders
```
Resultado **403**. En la ventana **Orders**: `SECRETO INTERNO RECHAZADO GET /orders -> 403`.
*"Aunque alguien llegue al puerto del servicio, sin el secreto no obtiene nada. El valor enviado tampoco queda registrado."*

### Escena 8 — Cierre (20 s)
*"Con un solo identificador de correlación quedó demostrado: el navegador llamó al Gateway, el Gateway validó con Auth antes de enrutar, el backend verificó secretos y la base de datos registró el cambio. Pendiente para la evaluación final: la matriz de trazabilidad, ejecuciones repetidas, pruebas en viewport móvil y el informe de incidencias."*

---

## 5. Si algo sale mal

| Síntoma | Causa probable | Solución |
|---|---|---|
| "Puertos ocupados" al iniciar | Quedaron servicios de un intento previo | `scripts\detener-todo.ps1` y volver a iniciar |
| Una ventana se cierra sola | Falta una dependencia | `py -m pip install -r requirements.txt` |
| Al pedir aparece "Sesión requerida" | Expiró la sesión (dura 15 min) | Volver a ingresar con `ana` |
| El pedido queda `pending` | Payments no respondió | Ver ventana Payments; reiniciar la plataforma |
| 429 "Demasiadas solicitudes" | Más de 5 logins por minuto | Esperar 1 minuto |
| No encuentro el `rid` en un log | La ventana ya hizo scroll | Aumentar el buffer o repetir el pedido; el `rid` nuevo aparece en Network |
| Stock no es 50 al empezar | Quedaron pedidos de ensayos | Repetir 3.1 y 3.2 |
| `py` no se reconoce | Python no está en el PATH | Usar `python` o `py -3` |

Sin sesión (otro rechazo útil): cerrar sesión y abrir `http://127.0.0.1:8000/panel#/pedidos` → en Network `orders` devuelve **401** y el Gateway registra `SIN SESION: no hay cookie session_token -> 401`.

---

## 6. Lista de verificación antes de subir a Canvas

- [ ] Se ve el **Network** con la llamada al Gateway (:8000) y el `X-Request-ID`.
- [ ] El mismo `rid` se muestra en Gateway, Auth, Orders, Inventory y Payments.
- [ ] Se ve que la validación en Auth ocurre **antes** de "GATEWAY ENRUTA".
- [ ] Se muestra `secreto ... VERIFICADO` en el backend, y un caso de `RECHAZADO`.
- [ ] Se muestran los `DB ... INSERT/UPDATE` y la consulta independiente `verificar_persistencia.py`.
- [ ] **No** se mostró `.env`, la cookie ni ningún secreto/token.
- [ ] Se dijo explícitamente que no se usa Docker en esta demostración.
- [ ] El audio se entiende y el texto de las ventanas se lee.
- [ ] Duración razonable; el archivo respeta el límite de Canvas.

## 7. Qué NO afirmar en el video (para no sobreprometer)
- Que el sistema está "totalmente seguro" o "listo para producción": solo se probó un flujo en un entorno local.
- Que hay contenedores Docker corriendo (no es así en esta máquina).
- Que el pago es real: Payments es un **simulador propio** que aprueba siempre; no hay integración con un proveedor real. Si lo mencionan, deben decir que es un doble de prueba.
- Que las demás secciones (reservas, contacto, panel admin, GraphQL, gRPC) están validadas: no son parte de esta demostración.

## 8. Referencia rápida de la arquitectura demostrada
```
Navegador ──(HTTPS/HTTP, cookie HttpOnly)──► API Gateway :8000
                                              │  1) POST /introspect + secreto ──► Auth Service :8100 ── dbIdentity
                                              │  2) RBAC (rol vs. método+recurso)
                                              │  3) enruta + X-Internal-Secret + identidad
                                              ▼
                                         Orders :9002 ── dbOrders
                                              │  X-Internal-Secret ──► Inventory :9001 ── dbInventory (reserva stock)
                                              │  secreto propio    ──► Payments  :9004 ── dbPayments (cobro simulado)
```
