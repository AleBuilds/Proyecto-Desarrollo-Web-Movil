# Manual para grabar el video del Avance 1 (Evaluación 3)

**Proyecto:** El Mediterráneo (Caso 22) · **Equipo:** Alejandro Narváez y Silenay Sarmiento
**Entrega:** video en Canvas → Evaluaciones → "Video Seguimiento"
**Módulo que se demuestra:** **Realizar un pedido** (carrito → entrega → confirmación)

> Se eligió "Realizar pedido" porque es el único flujo que atraviesa **todas** las capas que pide el profesor:
> frontend → API Gateway → Auth Service → Orders → (Inventory + Payments) → bases de datos SQLite.

---

## 1. Qué pide el profesor y dónde se ve cada punto

| # | Lo que pide | Qué se muestra | Dónde |
|---|---|---|---|
| 1 | **Frontend**: en el navegador, pestaña *Red/Network*, que llamó al API Gateway | Petición `POST /api/orders` a `127.0.0.1:8000` con respuesta 201 y cabecera `X-Request-ID` | Chrome/Edge → F12 → Network |
| 2 | **API Gateway**: en su log, que pidió validación al Auth Service/gestor de secretos y enrutó al backend | Líneas `GATEWAY -> AUTH SERVICE`, `sesión VALIDADA`, `RBAC permitido`, `GATEWAY ENRUTA ... -> :9002/orders` | Ventana **API Gateway :8000** |
| 3 | **Auth Service**: en su log, que validó autenticación/autorización **antes** del enrutamiento | `secreto de introspección VERIFICADO`, `sesión activa user=... roles=...` | Ventana **Auth Service :8100** |
| 4 | **Backend**: en su log, que facilitó o impidió la llamada verificando secretos | `secreto interno VERIFICADO` (Orders, Inventory, Payments) y, en el caso de rechazo, `SECRETO INTERNO RECHAZADO -> 403` | Ventanas **Orders :9002**, **Inventory :9001**, **Payments :9004** |
| 5 | **Persistencia**: que consultó o modificó la base de datos | `DB dbOrders INSERT orders`, `DB dbInventory UPDATE products stock 50 -> 48`, `DB dbPayments INSERT payments` + consulta independiente a las bases | Mismas ventanas + script `verificar_persistencia.py` |

**Hilo conductor:** cada petición lleva un identificador de correlación (`rid=...`, cabecera `X-Request-ID`).
El mismo `rid` aparece en el navegador, en el Gateway, en Auth, en Orders, Inventory y Payments. Eso es lo que
permite demostrar fehacientemente que una acción de usuario en el frontend generó esa secuencia exacta entre contenedores/servicios.

### Aclaración importante sobre "contenedores"
Si los servicios se ejecutan como procesos independientes en Windows, **uno por ventana**, cada uno con su propio puerto y su propia base de datos (equivalente funcional a un contenedor por servicio). El repositorio incluye además `docker-compose.yml` para despliegue en contenedores reales. En el video se puede aclarar según la modalidad que usen:
*"cada servicio corre aislado con su puerto y base de datos propia; el docker-compose está provisto en el repositorio"*.

---

## 2. Implementación de observabilidad y seguridad para la demostración

Se configuraron los registros de auditoría y trazabilidad distribuida **sin exponer secretos, tokens ni cookies**:

- `gateway/gateway.py`: registra la llamada a Auth (`/introspect` y `/login`), el resultado, la decisión RBAC y el destino del enrutamiento; **propaga el `X-Request-ID` a Auth y al backend**.
- `auth_service/auth_service.py`: registra la verificación del secreto de introspección, la consulta a `dbIdentity` y el resultado de la sesión.
- `services/orders`, `inventory`, `payments`, `clients`: registran la verificación del secreto interno (aceptado o rechazado con código 403) y cada operación sobre su base de datos. Orders **propaga el `rid`** a Inventory y Payments.
- Scripts en `scripts/`: `verificar_persistencia.py` (consulta de solo lectura a las bases) y `reiniciar_datos_demo.py` (restaura el estado inicial).

---

## 3. Preparación (hacer ANTES de grabar)

Carpeta de trabajo: `Evaluación 3`

### 3.1 Dejar todo limpio
```powershell
cd "Evaluación 3"
powershell -ExecutionPolicy Bypass -File scripts\detener-todo.ps1
python scripts\reiniciar_datos_demo.py
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

### 3.5 Higiene de seguridad (evaluado positivamente por el docente)
- **No abrir** `.env` ni mostrarlo en pantalla (contiene los secretos en texto claro).
- En Network, **no expandir** la sección *Cookies* ni la cabecera `Cookie` (contiene el token de sesión). La cookie es `HttpOnly` y no la ve JavaScript; eso se puede mencionar como control de seguridad.
- Antes de grabar, silenciar notificaciones y cerrar aplicaciones secundarias.

### 3.6 Ensayo
Hacer un ensayo rápido previo, y luego ejecutar `python scripts\reiniciar_datos_demo.py` para que el pedido del video definitivo parta de cero.

---

## 4. Guion de grabación paso a paso (6 a 8 minutos)

### Escena 0 — Introducción (30 s)
Mostrar las ventanas de los servicios y el navegador.
*"Somos Alejandro Narváez y Silenay Sarmiento. Este es el Avance 1 de la Evaluación 3 del caso El Mediterráneo. Vamos a demostrar el módulo 'Realizar pedido' atravesando todas las capas requeridas: frontend, API Gateway, Auth Service, microservicios backend y persistencia en base de datos. Cada servicio corre aislado con su propio puerto y su propia base de datos."*

### Escena 1 — Frontend: inicio de sesión y pedido (1 min 30 s)
1. En el navegador, ir a **Ingresar** → usuario `ana`, contraseña `1234`.
2. Ir a **Menú**, abrir *Hummus Especial*, subir la cantidad a **2** con el botón `+` y pulsar **Agregar al Carrito**.
3. **Carrito → Continuar** (pasa a Entrega): método **Retiro en Local**, nombre "Ana Demo", teléfono `+56911112222` → pulsar **Confirmar Pedido y Pagar**.
4. Llega a la pantalla de confirmación exitosa con número de pedido.

*"Al iniciar sesión el navegador no guarda ningún token en localStorage: la sesión viaja en una cookie HttpOnly emitida por el servidor."*

### Escena 2 — Requisito 1: Inspección de Red en Frontend (1 min)
En F12 → pestaña **Network / Red**, seleccionar la petición `POST /api/orders`:
- **Headers → General**: *Request URL* `http://127.0.0.1:8000/api/orders` → "el frontend se comunica exclusivamente con el **API Gateway** (puerto 8000), nunca directamente con los microservicios privados".
- **Response Headers**: mostrar y copiar el valor de **`X-Request-ID`** (ej. `a1b2c3d4...`).
- Status **201 Created**.
- **Payload**: se aprecia que el navegador solo envía `id` y `cantidad` de cada ítem, **sin precios** (el backend calcula precios oficiales).
- **Response**: confirma el pedido con `status: confirmed` y el total calculado por el servidor.

*"Este X-Request-ID es nuestro identificador de correlación que vincula todos los logs entre contenedores."*

### Escena 3 — Requisito 2: Log del API Gateway (1 min)
En la ventana **API Gateway :8000**, ubicar las líneas con ese mismo `rid`:
```
GATEWAY -> AUTH SERVICE: solicita validación de sesión (POST http://127.0.0.1:8100/introspect, secreto adjunto no registrado)
AUTH SERVICE -> GATEWAY: respuesta 200
sesión VALIDADA por Auth Service: user=ana roles=['user']
RBAC permitido user=ana POST /orders
GATEWAY ENRUTA POST /api/orders -> http://127.0.0.1:9002/orders (inyecta secreto interno y contexto de identidad)
BACKEND http://127.0.0.1:9002 respondió 201
```
*"El Gateway no confía ciegamente en la petición: primero solicita introspección al Auth Service, valida el rol con RBAC, y solo entonces enruta a Orders inyectando el secreto interno y los encabezados de identidad."*

### Escena 4 — Requisito 3: Log del Auth Service (45 s)
En la ventana **Auth Service :8100**, verificar el mismo `rid`:
```
secreto de introspección VERIFICADO (llamante autorizado: gateway) POST /introspect
DB dbIdentity SELECT sessions (consulta por token, valor no registrado)
AUTENTICACION/AUTORIZACION: sesión activa user=ana roles=['user'] -> active=true
```
*"Se observa en la marca de tiempo que la validación en Auth ocurre estrictamente ANTES del enrutamiento en el Gateway. Además, Auth comprueba el secreto de introspección para asegurarse de responder solo al Gateway."*

### Escena 5 — Requisito 4: Log del Backend y Verificación de Secretos (1 min)
En las ventanas **Orders :9002**, **Inventory :9001** y **Payments :9004**, mismo `rid`:
```
[orders]    secreto interno VERIFICADO POST /orders
[orders]    identidad recibida del gateway user=ana roles=['user']
[inventory] secreto interno VERIFICADO POST /inventory/reserve
[payments]  secreto de payments VERIFICADO POST /payments/process
```
*"Cada microservicio privado exige y verifica su secreto. Payments utiliza un secreto independiente que solo conoce Orders, impidiendo llamadas directas desde el exterior o desde otros servicios."*

### Escena 6 — Requisito 5: Persistencia en Base de Datos (1 min 30 s)
**a) En los logs de los microservicios** (mismo `rid`):
```
[orders]    DB dbOrders SELECT idempotency_records -> no existe
[inventory] DB dbInventory UPDATE products id=1 'Hummus Especial' stock 50 -> 48
[inventory] DB dbInventory COMMIT reserva de stock (1 productos)
[orders]    DB dbOrders INSERT orders id=1 total=10400 status=pending
[orders]    DB dbOrders INSERT order_items (1 filas) order_id=1
[payments]  DB dbPayments SELECT payments order_id=1 -> sin pago previo
[payments]  DB dbPayments INSERT payments id=1 order_id=1 monto=10400 estado=approved COMMIT
[orders]    DB dbOrders UPDATE orders id=1 status=confirmed
[orders]    DB dbOrders COMMIT pedido id=1 status=confirmed
```

**b) Comprobación independiente de base de datos** (en la terminal libre):
```powershell
python scripts\verificar_persistencia.py
```
Muestra en pantalla el pedido recién registrado en `dbOrders`, su desglose en `order_items`, el registro de cobro aprobado en `dbPayments` y el stock actualizado en `dbInventory` (de 50 a 48 unidades).
*"Esta consulta se hace en modo de solo lectura conectando directamente a los archivos SQLite, comprobando la persistencia real del flujo sin pasar por la capa web."*

### Escena 7 — Demostración de Control de Acceso y Rechazo de Secretos (1 min)
Para evidenciar que el backend también **impide** accesos indebidos verificando secretos:
Ejecutar en la terminal libre:
```powershell
curl.exe -s -w " -> %{http_code}`n" -H "X-Internal-Secret: incorrecto" http://127.0.0.1:9002/orders
```
Resultado en consola: `-> 403`.
En la ventana de **Orders :9002** se observa en el log:
`SECRETO INTERNO RECHAZADO GET /orders -> 403`.
*"Cualquier intento de conexión sin el secreto legítimo es denegado con código 403 y registrado en la auditoría sin almacenar datos sensibles."*

### Escena 8 — Cierre (20 s)
*"Demostramos con un identificador de correlación unificado los 5 requisitos solicitados: llamada desde frontend al Gateway, validación previa en Auth Service, verificación de secretos en backend, persistencia y control de rechazo."*

---

## 5. Solución de incidencias comunes

| Problema | Causa | Solución |
|---|---|---|
| "Puertos ocupados" al iniciar | Procesos activos de ejecuciones previas | Ejecutar `powershell scripts\detener-todo.ps1` |
| "Sesión requerida" al hacer pedido | Expiró la cookie (TTL 15 min) | Iniciar sesión nuevamente con `ana` / `1234` |
| El pedido queda en `pending` | Payments no completó respuesta | Revisar ventana Payments; reiniciar con `scripts\iniciar-todo.ps1` |
| HTTP 429 Too Many Requests | Límite de rate limit alcanzado | Aguardar 60 segundos |
| Stock inicial distinto de 50 | Pedidos previos sin limpiar | Ejecutar `python scripts\reiniciar_datos_demo.py` |

---

## 6. Lista de comprobación antes de la entrega

- [x] Petición visible en Network apuntando al Gateway (:8000) con `X-Request-ID`.
- [x] Mismo `rid` trazable en Gateway, Auth, Orders, Inventory y Payments.
- [x] Validación en Auth Service comprobada antes del enrutamiento.
- [x] Logs de secretos `VERIFICADO` y caso `RECHAZADO -> 403` demostrados.
- [x] Persistencia en BD demostrada en logs y con script `verificar_persistencia.py`.
- [x] Secretos y contraseñas protegidos sin aparecer en pantalla ni en logs.
