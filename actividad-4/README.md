Actividad 4 — Resiliencia
Concern: comunicación con backend y resiliencia.
Decisión: la sección de productos es un estado de servidor aislado. Ante demora (10s) se muestra un indicador de carga sin bloquear el resto de la página; ante error, se reemplaza por un mensaje claro con botón "Reintentar" que puede recuperar el estado exitoso sin recargar.
Evidencia: se probaron ambos escenarios por separado — con la demora de 10s confirmé que la navegación y el resto del contenido permanecen usables mientras se espera; con el error confirmé que "Reintentar" restaura los productos correctamente.
