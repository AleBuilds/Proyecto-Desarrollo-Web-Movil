# EL MEDITERRÁNEO — Documentación de Wireframe (UI/UX)

**Proyecto:** Prototipo de página web para restaurante mediterráneo ficticio "El Mediterráneo" (hummus, falafel, shawarma, parrilla, pescados, ensaladas).
**Etapa actual:** Wireframe en escala de grises — sin fotografías ni colores de marca aplicados todavía.
**Herramienta:** Figma.

---

## 1. Paleta de colores (Design System)

| Nombre | HEX | Uso previsto |
|---|---|---|
| Carbón | `#1A1A1A` | Fondos oscuros, navbar, footer |
| Tierra | `#3B2A20` | Fondos secundarios / detalles cálidos |
| Fuego | `#A63B1E` | Botones principales (CTA), precios |
| Llama | `#E07A1F` | Acentos, hover |
| Sol | `#F2C94C` | Destacados, detalles de fuego |
| Arena | `#DCC7A1` | Bordes, separadores |
| Oliva | `#5E6B3D` | Categorías, iconos de ingredientes |
| Crema | `#F3EFE6` | Fondo principal |
| Blanco | `#FFFFFF` | Texto sobre fondo oscuro, tarjetas |

## 2. Tipografía

| Uso | Fuente |
|---|---|
| Títulos | Cinzel |
| Texto / cuerpo | Montserrat |
| Detalles decorativos | Playfair Display |

## 3. Componentes reutilizables (usados en todas las pantallas)

- **Navbar** (fija, parte superior): logo "EL MEDITERRÁNEO" (izq.) + menú Inicio / Menú / Nosotros / Reservas / Contacto (centro-der.) + ícono de carrito con contador de items (der.).
- **Footer** (fondo oscuro, 3 columnas): EL MEDITERRÁNEO (logo + líneas placeholder) · HORARIOS · CONTACTO, con línea de copyright "© 2026 El Mediterráneo. Todos los derechos reservados. Wireframe Layout." al pie.
- **Card de producto**: imagen placeholder ("X" diagonal) + categoría (mayúsculas, pequeña) + nombre + descripción (líneas grises) + precio + botón "AGREGAR".
- **Botón primario**: fondo oscuro sólido, texto blanco, mayúsculas.
- **Botón secundario**: fondo blanco/transparente con borde.
- **Input de formulario**: label en mayúsculas arriba + campo con placeholder gris claro.

---

## 4. Pantallas

### 01 — INICIO
![Pantalla Inicio](img/01%20inicio.png)
- **Hero**: bloque destacado con "TÍTULO PRINCIPAL", subtítulo (2 líneas placeholder) y dos botones: **VER MENÚ** (primario) y **RESERVAR** (secundario, borde).
- **Nuestras Especialidades**: 4 tarjetas de categoría (imagen placeholder con "X" + etiqueta): HUMMUS, FALAFEL, SHAWARMA, PARRILLA.
- **Productos Destacados**: 3 cards de producto — Hummus Clásico ($4.500, categoría "Entradas"), Plato Falafel ($6.200, "Especiales"), Shawarma Mixto ($7.800, "Sandwiches") — cada una con botón "AGREGAR".
- **Promoción de la Semana**: banner horizontal con imagen placeholder, título "PROMOCIÓN DE LA SEMANA", texto placeholder y botón "APROVECHAR".

### 02 — MENÚ
![Pantalla Menú](img/02%20menu.png)
- Título "MENÚ".
- **Filtros de categoría** (pills horizontales): Todos (seleccionado), Hummus, Falafel, Shawarma, Parrilla, Pescados, Ensaladas.
- **Grilla de productos** (3 columnas × 3 filas = 9 productos de ejemplo):
  - Hummus Especial — $5.200
  - Falafel Wrap — $4.900
  - Shawarma Pollo — $6.500
  - Brocheta de Carne — $8.900
  - Pescado del Día — $12.000
  - Ensalada Griega — $5.500
  - Hummus con Carne — $6.800
  - Falafel Plato — $7.200
  - Shawarma Ternera — $7.200
- Cada card: imagen placeholder, categoría, nombre, descripción, precio, botón "AGREGAR".

### 03 — PRODUCTO (detalle)
![Pantalla Producto](img/03%20producto.png)
- Ejemplo mostrado: **Brochetas de Cordero Premium** — Categoría: Parrilla — $14.500.
- Layout dos columnas: imagen grande a la izquierda ("IMAGEN PRODUCTO PRINCIPAL"), info a la derecha.
- **Descripción**: texto placeholder (2 líneas).
- **Ingredientes** (lista con viñetas): Carne de cordero tierna maridada / Especias mediterráneas tradicionales / Pimientos y cebollas asadas / Salsa tahini artesanal de acompañamiento.
- Selector de cantidad **[- 1 +]** + botón **AGREGAR AL CARRITO**.
- **También te puede gustar**: 3 cards adicionales — Salsa de Ajo ($1.500), Pan Pita Adicional ($800), Té de Menta Frío ($2.200).

### 04 — CARRITO
![Pantalla Carrito](img/04%20carrito.png)
- Título "TU CARRITO".
- Lista de productos (cada fila: imagen placeholder, nombre, precio unitario, selector de cantidad [- n +], subtotal de línea, ícono eliminar):
  - Shawarma Ternera Especial — 1 × $7.200 = $7.200
  - Plato Falafel Grande — 2 × $6.200 = $12.400
- **Panel Resumen** (lateral derecho): Subtotal $19.600 + Envío estimado $2.500 = **Total $22.100**. Botón "CONTINUAR COMPRA".

### 05 — ENTREGA (Método de entrega)
![Pantalla Entrega](img/05%20entrega.png)
- Título "MÉTODO DE ENTREGA".
- Dos opciones tipo radio-card: **DELIVERY** (seleccionada, con ícono camión) y **RETIRO EN LOCAL** (ícono bolsa).
- **Formulario "Datos de Despacho / Contacto"**: Nombre completo, Dirección de entrega, Teléfono, Email (2 columnas) + campo de texto "Notas / Indicaciones".
- Nota de seguridad "Pago 100% seguro y encriptado" + botón **CONFIRMAR PEDIDO Y PAGAR**.

### 06 — RESERVAS
![Pantalla Reservas](img/06%20reservas.png)
- Título "RESERVAR MESA".
- **Formulario** (columna izquierda): Fecha, Hora, Número de personas, Nombre, Teléfono, Email + botón "RESERVAR".
- **Panel de confirmación** (columna derecha, ejemplo ya completado): "RESERVA CONFIRMADA" — Fecha: 14 Octubre 2026, Hora: 20:30 hrs, Personas: 4, A nombre de: Juan Pérez + botón "VOLVER AL INICIO".

### 07 — NOSOTROS
![Pantalla Nosotros](img/07%20nosotros.png)
- Layout dos columnas: imagen placeholder ("IMAGEN RESTAURANTE") a la izquierda, texto a la derecha.
- Título "NUESTRA HISTORIA" + párrafo placeholder + botón "CONOCER MÁS".
- **Nuestros Pilares**: 3 tarjetas con ícono circular + título — Fresco y Natural / Receta Tradicional / Pasión Familiar — cada una con texto placeholder.

### 08 — CONTACTO
![Pantalla Contacto](img/08%20contacto.png)
- Layout dos columnas.
- Izquierda: "UBICACIÓN" — bloque de mapa placeholder (etiqueta "MAPA").
- Derecha: "DATOS DE CONTACTO" — Dirección (Av. del Mar 1042, Barcelona), Teléfono (+34 93 123 4567), Email (hola@elmediterraneo.com), Horarios (Lun a Dom: 12:30 – 23:30), cada uno con ícono circular placeholder.
- Debajo (ancho completo bajo el mapa): formulario "Deja tu mensaje" — Nombre, Email, Mensaje + botón "ENVIAR".
- *Nota: los datos de contacto usan formato español (Barcelona, +34) como placeholder — conviene ajustarlos a Chile/Maipú antes de la entrega final si el profesor lo requiere.*

### 09 — CONFIRMACIÓN
![Pantalla Confirmación](img/09%20confirmacion.png)
- Ícono circular de éxito (placeholder) + título "PEDIDO CONFIRMADO".
- Subtítulo "¡Gracias por tu pedido! N° #1042".
- **Resumen de Compra** (card): Cantidad de productos (3 items), Método de entrega (Despacho a Domicilio), Tiempo estimado (30–45 min), Total pagado ($18.500).
- Dos botones: **VER MIS PEDIDOS** y **VOLVER AL INICIO**.

---

## 5. Flujo de navegación (prototipo)

```
INICIO
 ├── VER MENÚ ──────────→ MENÚ
 │                          │
 │                          └── clic en producto ──→ PRODUCTO (detalle)
 │                                                       │
 │                                                       └── AGREGAR AL CARRITO ──→ CARRITO
 │                                                                                    │
 │                                                                                    └── CONTINUAR COMPRA ──→ ENTREGA
 │                                                                                                                │
 │                                                                                                                └── CONFIRMAR PEDIDO Y PAGAR ──→ CONFIRMACIÓN
 │                                                                                                                                                     │
 │                                                                                                                                                     ├── VER MIS PEDIDOS ──→ vuelve a mostrar CARRITO (vista de solo lectura del pedido)
 │                                                                                                                                                     └── VOLVER AL INICIO ──→ INICIO
 │
 ├── RESERVAR ──────────→ RESERVAS ──→ (formulario) ──→ Reserva Confirmada ──→ VOLVER AL INICIO
 ├── NOSOTROS ──────────→ NOSOTROS
 └── CONTACTO ──────────→ CONTACTO
```

**Decisión de flujo — botón "VER MIS PEDIDOS" (pantalla 09):** en vez de crear una pantalla nueva de tracking/estado de pedido, este botón redirige a la pantalla **04 — CARRITO**, reutilizando el mismo componente pero en modo solo lectura (sin poder modificar cantidades). Esto simplifica el prototipo y mantiene coherencia visual sin agregar una pantalla adicional.

---

## 6. Estado del proyecto

- [x] Wireframes en escala de grises de las 9 pantallas completados.
- [ ] Aplicar Design System (paleta de colores + tipografías + fotografías) — Paso 2.
- [ ] Crear versiones responsive mobile (390×844) con Auto Layout — Paso 3.
- [ ] Conectar prototipo interactivo completo en Figma.
