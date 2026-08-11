# Actividad 1: Mapa de concerns — Mercado Libre

Aplicación analizada: **Mercado Libre**

A continuación se identifican 12 architectural concerns clasificados en las tres categorías del material (diseño/estructura, operación/runtime y transversales), cada uno con una decisión existente, una alternativa posible y una evidencia que permitiría compararlas.

## Diseño / Estructura

### 1. Estrategia de renderizado
- **Decisión existente:** SSR (o híbrido) en páginas de producto y listado, para indexación SEO y carga inicial rápida.
- **Alternativa:** CSR puro (SPA completa).
- **Evidencia:** tiempo de primera visualización, posicionamiento en buscadores de productos.

### 2. Gestión del estado
- **Decisión existente:** carrito y sesión persistentes entre dispositivos (estado de servidor + persistente).
- **Alternativa:** carrito solo en estado local/navegador.
- **Evidencia:** tasa de abandono de carrito, consistencia entre app y web.

### 3. Arquitectura de componentes
- **Decisión existente:** componentes reutilizables para tarjetas de producto (usados en home, búsqueda, categorías).
- **Alternativa:** implementación distinta por sección.
- **Evidencia:** consistencia visual, velocidad de desarrollo de nuevas features.

### 4. Comunicación con backend
- **Decisión existente:** APIs con reintentos y caché para stock/precio (dato muy cambiante).
- **Alternativa:** consulta directa sin caché en cada render.
- **Evidencia:** latencia de carga de ficha de producto, tasa de error en checkout.

### 5. Routing y carga
- **Decisión existente:** filtros de búsqueda representados en la URL (categoría, precio, envío gratis).
- **Alternativa:** filtros solo en estado de cliente, sin reflejarse en URL.
- **Evidencia:** capacidad de compartir/enlazar búsquedas, comportamiento del botón "atrás".

## Operación / Runtime

### 6. Rendimiento en producción
- **Decisión existente:** carga diferida (lazy load) de imágenes de producto en listados largos.
- **Alternativa:** cargar todas las imágenes de inmediato.
- **Evidencia:** peso de página, tiempo hasta interacción en dispositivos de gama baja.

### 7. Seguridad
- **Decisión existente:** tokenización de datos de pago, autorización en backend (no confiar en el cliente).
- **Alternativa:** manejar validaciones de pago solo en frontend.
- **Evidencia:** auditorías de seguridad, incidentes de fraude reportados.

### 8. Resiliencia y degradación
- **Decisión existente:** si falla el servicio de recomendaciones, se muestra el resto de la página igual (no bloquea la compra).
- **Alternativa:** bloquear toda la página si un servicio secundario falla.
- **Evidencia:** tasa de errores por servicio, disponibilidad del checkout aislada de otros módulos.

### 9. Despliegue y ciclo de vida
- **Decisión existente:** despliegues progresivos (rollout por porcentaje de usuarios) para nuevas features de checkout.
- **Alternativa:** despliegue total e inmediato a todos los usuarios.
- **Evidencia:** tasa de error post-despliegue, tiempo de reversión ante fallas.

## Transversales

### 10. Accesibilidad
- **Decisión existente:** navegación por teclado en el flujo de compra, etiquetas en formularios de pago/envío.
- **Alternativa:** interfaz optimizada solo para mouse/touch.
- **Evidencia:** auditoría de accesibilidad, pruebas con lector de pantalla en checkout.

### 11. Internacionalización
- **Decisión existente:** formatos de moneda y fecha adaptados por país (Mercado Libre opera en varios países de LATAM).
- **Alternativa:** un solo formato fijo para todos los países.
- **Evidencia:** errores de formato reportados por región, pruebas con distintos locales.

### 12. Estrategia de testing
- **Decisión existente:** pruebas end-to-end del flujo crítico completo (buscar → agregar al carrito → pagar).
- **Alternativa:** solo pruebas unitarias aisladas por componente.
- **Evidencia:** incidentes en producción relacionados al flujo de compra, cobertura de pruebas E2E.
