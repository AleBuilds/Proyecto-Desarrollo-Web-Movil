# INFORME DE EVALUACIÓN 1: PROTOTIPO FRONT-END RESPONSIVO Y DINÁMICO
## Caso 22: Comida Mediterránea “El Mediterráneo” (hummus, falafel y shawarma)

---

### Portada y Datos Generales
* **Asignatura:** Desarrollo Web y Móvil
* **Evaluación:** Evaluación 1 — Prototipo Front-End Responsivo y Dinámico
* **Integrantes del Equipo:**
  1. **Alejandro Narváez**
  2. **Silenay Sarmiento**
* **Caso de Negocio:** **Caso 22 — "El Mediterráneo"** (especialidades: hummus, falafel, shawarma, carnes a la parrilla, pescados y ensaladas mediterráneas)
* **Actor Principal:** Cliente / Comensal web
* **Objetivo de Usuario:** Explorar la carta gastronómica, filtrar por categoría, seleccionar platos, gestionar el carrito de compra en tiempo real y completar el flujo de pedido y reserva con actualización dinámica del DOM.

---

### 1. Selección del Flujo y Architectural Concerns del Front-End (Criterio C1)
* **Flujo Seleccionado:**
  $$\text{Inicio} \longrightarrow \text{Menú / Filtros} \longrightarrow \text{Detalle Producto} \longrightarrow \text{Carrito Dinámico} \longrightarrow \text{Método de Entrega / Reserva} \longrightarrow \text{Confirmación}$$
* **Concerns de Front-End Identificados:**
  1. **Compatibilidad y Responsividad Multi-dispositivo:** Necesidad de soportar pantallas desde móviles compactos (390px) hasta escritorios amplios (1440px) sin pérdida de jerarquía visual.
  2. **Rendimiento y Carga Visual:** Optimización del peso de imágenes mediante URLs CDN y layout sin shifts acumulativos (CLS).
  3. **Gestión del Estado en Cliente (State Management):** Persistencia del carrito en `localStorage` sincronizado con la interfaz para que el usuario no pierda su selección al cambiar de página.
  4. **Resiliencia de Interfaz:** Manejo de estados de carga, estados vacíos ("Tu carrito está vacío") y mensajes claros de validación.

---

### 2. Evidencia de Diseño Previo y Explicación Visual (Criterio C2)
El diseño previo se estructuró a partir de wireframes detallados en escala de grises y un sistema de diseño consistente:
* **Archivo de especificación:** `EL-MEDITERRANEO-Bosquejo-y-Paleta-de-colores.md`
* **Wireframes incluidos en la carpeta `img/`:**
  - `01 inicio.png`: Hero, categorías destacadas y promociones.
  - `02 menu.png`: Grilla de 9 productos con barra de filtros horizontales.
  - `03 producto.png`: Ficha de detalle, ingredientes y selector de porciones.
  - `04 carrito.png`: Lista de líneas con botones dinámicos de cantidad y panel de resumen.
  - `05 entrega.png`: Formulario de despacho a domicilio o retiro en local.
  - `06 reservas.png`: Formulario de reserva de mesa con confirmación lateral.
  - `07 nosotros.png`: Historia y pilares gastronómicos.
  - `08 contacto.png`: Ubicación, mapa y formulario de contacto.
  - `09 confirmacion.png`: Resumen del pedido procesado y número de orden.

---

### 3. Grid System y Comportamiento Responsivo (Criterio C3)
Se utilizó el sistema de grilla de 12 columnas (Bootstrap) para estructurar el layout:
* **Fórmula de proporción aplicada:**
  $$\text{Columnas} = 12 \times \frac{\text{Ancho del Elemento}}{\text{Ancho del Contenedor}}$$
* **Comportamiento en 4 anchos de Viewport evaluados:**
  1. **Móvil (390 px - `col-12`):**
     - Las tarjetas de producto se apilan en 1 columna vertical.
     - El menú de navegación se contrae en hamburguesa.
     - En el carrito, cada ítem ocupa el ancho completo y el resumen pasa debajo.
  2. **Tablet vertical (768 px - `col-md-6`):**
     - La grilla del menú se reordena en 2 columnas por fila.
     - El formulario de entrega y reservas se divide en 2 columnas equilibradas.
  3. **Escritorio Estándar (1024 px - `col-lg-4`):**
     - Grilla de 3 columnas de productos destacados y carta.
     - El carrito presenta el desglose de productos al 65% y el panel de totales fijo al 35%.
  4. **Escritorio Amplio (1440 px - `col-xl-4` / Container centrado):**
     - Máximo ancho contenido para evitar líneas de texto excesivamente largas y preservar la legibilidad.

---

### 4. Box Model y Flex Model (Criterios C4 y C5)
* **Box Model:**
  - `box-sizing: border-box` en todos los elementos.
  - Control riguroso de `margin` y `padding` (clases utilitarias `p-3`, `p-4`, `mb-3`, `gap-3`) para garantizar zonas de toque cómodas en pantallas táctiles ($\ge 44 \times 44\text{ px}$).
* **Flexbox:**
  - Utilizado internamente en las tarjetas (`d-flex flex-column h-100`) para que el botón "Agregar" y el precio queden siempre alineados en la base (`mt-auto`).
  - Filas de productos del carrito con `d-flex align-items-center flex-wrap gap-3` permitiendo que los selectores de cantidad y precio fluyan naturalmente si la pantalla se estrecha.

---

### 5. Manipulación del DOM mediante JavaScript (Criterio C7)
La lógica en `carrito.js` y `main.js` manipula dinámicamente el árbol DOM sin recargar la página completa:
* **Selectores:** `document.querySelector` y `querySelectorAll`.
* **Event Listeners:** Delegación de eventos en clics para `[data-agregar]`, `[data-mod]` y `[data-del]`.
* **Modificación Dinámica:**
  - Inserción de nodos HTML para cada ítem agregado al carrito.
  - Actualización del contador en la insignia del navbar (`.carrito-badge`).
  - Cálculo instantáneo en cliente de subtotales por línea y total final con costo de despacho.
  - Alternancia entre estado vacío (alerta con botón a Menú) y estado con datos.

---

### 6. Simulación de Servicios (Servicios Dummy / Criterio C8)
* **Consulta:** Carga dinámica del listado de platos con precios, categorías y descripciones.
* **Acción Simulada:** Confirmación de pedido en `entrega.php` / `carrito.js`, almacenando el estado transaccional en `sessionStorage` para alimentar la vista de `confirmacion.php`.
* **Estados contemplados:**
  - **Cargando:** Indicador en botones durante el procesamiento.
  - **Éxito:** Redirección automática con número de orden asignado.
  - **Vacío:** Pantalla de carrito vacío cuando no hay ítems seleccionados.
  - **Error/Validación:** Avisos comprensibles si faltan campos obligatorios (como dirección en delivery).

---

### 7. Instrucciones para Ejecutar y Visualizar el Prototipo

1. **Abrir en Navegador Local:**
   - Puedes abrir directamente cualquiera de las páginas con un servidor local de desarrollo (por ejemplo, con la extensión *Live Server* de VS Code o ejecutando `php -S localhost:8080` dentro de esta carpeta).
2. **Navegación del flujo:**
   - Inicia en `index.php` (o `index.html`).
   - Haz clic en **"VER MENÚ"** $\rightarrow$ filtra por categoría (Hummus, Falafel, Shawarma, etc.).
   - Agrega platos al carrito con el botón **"AGREGAR"**.
   - Haz clic en el ícono del carrito en el navbar $\rightarrow$ ajusta cantidades con `+` y `-`.
   - Haz clic en **"CONTINUAR COMPRA"** $\rightarrow$ completa datos de entrega $\rightarrow$ **"CONFIRMAR PEDIDO"**.
   - Visualiza la pantalla de confirmación final con el número de pedido generado.
