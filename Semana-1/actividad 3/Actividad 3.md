# Actividad 3 — Diseño de un template (Tienda en línea)

Dominio elegido: **tienda en línea**, coherente con la aplicación analizada en la Actividad 1
(Mercado Libre) y con el Figma medido en la Actividad 2.

## Medidas y columnas

Contenedor de referencia según Actividad 2: **1280–1282 px**.

| Bloque | Ancho medido | Proporción | Columnas | Clase Bootstrap 3 |
|---|---|---|---|---|
| Encabezado 1 — texto | 516 px | ~45 % | 8 | `col-lg-8` |
| Encabezado 1 — imagen | 624 px | ~55 % | 4 | `col-lg-4` |
| Encabezado 2 — imagen | 625 px | ~45 % | 5 | `col-lg-5` |
| Encabezado 2 — texto | 516 px | ~55 % | 7 | `col-lg-7` |
| Producto destacado | 735 px | 57,3 % | 7 | `col-lg-7` |
| Producto | 515 px | 40,2 % | 5 | `col-lg-5` |

Los pares no son simétricos (ver Encabezado 1 vs. 2) porque cada foto real tiene distinto peso
visual — decisión de diseño válida, no error de redondeo (mismo criterio que el Problema 3 del
material de estudio).

## Comportamiento por breakpoint

| Elemento | `xs` (<768px) | `md` (≥992px) | `lg` (≥1200px) |
|---|---|---|---|
| Navegación | Colapsa a ícono ☰ | Menú horizontal | igual |
| Encabezados | 12/12 apiladas | 6/6 | 8/4 y 5/7 |
| Productos | 12/12 apiladas | 6/6 | 7/5 |
| Footer | 12/12 apiladas | 4 columnas de 3 | igual |

## Navegación

`<nav>` con `navbar-toggle` de Bootstrap 3: en escritorio se ve el menú horizontal; en móvil se
transforma en ícono de hamburguesa (patrón **Transforma**, no solo escala o refluye).

## Estados de carga, vacío y error

La sección de productos no está escrita como HTML fijo: se controla con JavaScript y pasa por
tres estados posibles — carga (spinner), vacío (mensaje) y error (mensaje + botón "Reintentar").
Ver detalle de implementación en el `README` de la Actividad 4.

## Accesibilidad aplicada

- `alt` descriptivo en todas las imágenes.
- `aria-label` en la navegación y en cada sección.
- `role="alert"` en el bloque de error, `role="status"` en el spinner.
- Foco de teclado visible (`outline` reforzado en `:focus`).
- HTML5 semántico: `<nav>`, `<main>`, `<section>`, `<footer>` en vez de solo `<div>`.

## Evidencia de pruebas

Probado en 4 anchos:

- **375 px** — todo se apila 12/12, navegación colapsa a ícono ☰.
- **900 px** — sigue apilado (breakpoint `md` empieza en 992px, comportamiento esperado).
- **1200+ px** — layout final: 8/4, 5/7 y 7/5 lado a lado, menú horizontal visible.
- **1440 px** — sin desbordes de imagen ni texto cortado.
