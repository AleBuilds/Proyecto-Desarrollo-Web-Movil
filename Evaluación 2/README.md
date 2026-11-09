# Evaluación 2: Diseño e Implementación de un Backend Seguro Completo
**Caso 22:** Comida Mediterránea “El Mediterráneo” (hummus, falafel, shawarma, carnes a la brasa, pescados, ensaladas)  
**Integrantes:** Alejandro Narváez y Silenay Sarmiento  
**Curso:** Desarrollo Web y Móvil  
**Fecha:** Noviembre 2026  

---

## 1. Resumen de la Arquitectura

Siguiendo el modelo C4 especificado en `architecture/PlataformaComercial_Despliegue.dsl`:
- **API Gateway (:8000)**: Único punto de entrada expuesto. Gestiona sesiones en cookies seguras (`HttpOnly`, `SameSite=lax`), aplica control de acceso basado en roles (RBAC), CSP estricto y enruta peticiones inyectando el secreto interno de servicio.
- **Auth Service (:8100)**: Autenticación segura con hashing adaptativo (`scrypt` con sal única por usuario), generación de sesiones opacas e introspección protegida. Persistencia en `dbIdentity.sqlite`.
- **Microservicio Inventory (:9001)**: Catálogo, consulta de disponibilidad y reservas atómicas de stock. Persistencia en `dbInventory.sqlite`.
- **Microservicio Orders (:9002)**: Ciclo de vida de pedidos, validación estricta de pertenencia de recursos (recurso propio vs ajeno), control de idempotencia mediante `X-Idempotency-Key` y reservas. Persistencia en `dbOrders.sqlite`.
- **Microservicio Clients (:9003)**: Custodia de datos personales de clientes (direcciones, teléfonos, preferencias) con autorización por titular y admin. Persistencia en `dbClients.sqlite`.
- **Microservicio Payments (:9004)**: Procesamiento de cobros con prevención de transacciones duplicadas y verificación con proveedor. Persistencia en `dbPayments.sqlite`.
- **GraphQL Gateway (:8050)**: Servicio de agregación privada que compone datos de Orders, Inventory y Clients en una sola consulta (`resumenPedido`), con límites de profundidad para evitar ataques de denegación de servicio.
- **Delivery & Telemetry gRPC (:50051)**: Contratos fuertemente tipados en Protobuf (`delivery.proto`), llamadas Unary de alta velocidad, streaming en tiempo real de seguimiento y analítica operativa de cocina.

---

## 2. Puesta en Marcha Rápida (Windows / PowerShell)

### Requisitos Previos
1. Python 3.10+
2. Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

### Inicialización y Arranque
1. **Sembrar bases de datos SQLite:**
   ```powershell
   python scripts\sembrar_datos.py
   ```
2. **Iniciar toda la arquitectura con un solo comando:**
   ```powershell
   powershell scripts\iniciar-todo.ps1
   ```
3. **Acceder a la aplicación web:**
   - Navegar a: `http://localhost:8000`
   - O al panel administrativo: `http://localhost:8000/panel`

### Cuentas de Prueba Pre-cargadas
| Usuario | Contraseña | Rol | Descripción |
|---|---|---|---|
| `ana` | `1234` | `user` | Cliente registrado (pedidos y reservas) |
| `silenay` | `silenay123` | `user` | Cliente registrado (pedidos y reservas) |
| `administrador1` | `admin123` | `user,admin` | Administrador de catálogo y operaciones |
| `alejandro` | `alejandro123` | `user,admin` | Administrador de catálogo y operaciones |

---

## 3. Ejecución de Pruebas Automatizadas

Para ejecutar la suite completa de 19 pruebas de integración, seguridad, RBAC, idempotencia, GraphQL y gRPC:
```powershell
powershell scripts\probar-todo.ps1
```
o directamente con pytest:
```powershell
python -m pytest tests -v
```

Para ejecutar el benchmark de carga gRPC del Módulo 9:
```powershell
python services\delivery_telemetry\load_test.py
```

---

## 4. Despliegue en Contenedores (Docker Compose)
Para desplegar la arquitectura completa en redes aisladas (red pública para Gateway y red interna privada para los microservicios):
```bash
docker-compose up --build
```
