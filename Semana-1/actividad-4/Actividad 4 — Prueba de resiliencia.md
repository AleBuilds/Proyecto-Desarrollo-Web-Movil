# Actividad 4 — Prueba de resiliencia

Sobre el template de la Actividad 3, se simulan los dos escenarios de falla que pide el
enunciado: la API tarda 10 segundos, o responde con error.

## Concern

Resiliencia y degradación (sección 4.5 del material) + comunicación con backend (sección 3.4).

## Decisión

La sección de "Productos" se trata como un **estado de servidor** independiente del resto de
la página. Si la API falla o se demora, **solo esa sección** cambia de estado — la navegación,
el hero y el resto del contenido siguen funcionando con normalidad. No se bloquea la página
completa.

## Cómo probarlo

En la página hay 3 controles (radio buttons) sobre la sección de productos:

- **Normal** — muestra los productos con normalidad.
- **Simular demora de 10s en la API** — muestra un spinner de carga durante 10 segundos reales
  (no una animación corta) y luego se recupera solo, sin recargar la página.
- **Simular error de API** — reemplaza las imágenes de producto por un bloque de error con
  mensaje claro y botón **Reintentar**, que puede recuperar el estado exitoso sin recargar.

## Qué se evitó a propósito

No se ocultó el error ni se dejó una tarjeta vacía sin explicación. El mensaje dice qué falló
y ofrece una acción de recuperación — esto sigue el concepto de **degradación elegante** del
material: conservar las funciones esenciales, evitar pérdida de información y comunicar el
estado con claridad, no simplemente esconder la falla.

## Evidencia obtenida

- Con la **demora de 10s**: se confirmó que el resto del sitio (menú, encabezados) sigue siendo
  usable mientras la sección de productos muestra el spinner, y que se recupera automáticamente
  al terminar el tiempo de espera.
- Con el **error**: se confirmó que "Reintentar" restaura correctamente los productos originales,
  y que el resto de la página nunca se congela ni se bloquea mientras el error está visible.
