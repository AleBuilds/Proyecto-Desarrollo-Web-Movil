<?php
$activo = 'nosotros';

$pilares = [
    ['titulo' => 'Fresco y Natural',   'texto' => ['Ingredientes seleccionados', 'a diario en el mercado local']],
    ['titulo' => 'Receta Tradicional', 'texto' => ['Recetas transmitidas de', 'generación en generación']],
    ['titulo' => 'Pasión Familiar',    'texto' => ['Un negocio familiar con', 'más de 20 años de historia']],
];
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Nosotros — El Mediterráneo</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <style>
            /* Paleta de colores base del Wireframe */
            .bg-carbon { background-color: #1A1A1A !important; }
            .bg-crema { background-color: #F3EFE6 !important; }
            .placeholder-line { background-color: #ccc; height: 12px; margin-bottom: 12px; border-radius: 6px; }
            .placeholder-box { background-color: #f8f9fa; border: 1px solid #ced4da; display: flex; align-items: center; justify-content: center; color: #6c757d; font-size: 0.8rem; font-weight: bold; position: relative; overflow: hidden; }
            
            /* Simulación del aspa en las imágenes (X) */
            .placeholder-box::before, .placeholder-box::after { content: ''; position: absolute; width: 200%; height: 1px; background-color: #ced4da; top: 50%; left: -50%; }
            .placeholder-box::before { transform: rotate(35deg); }
            .placeholder-box::after { transform: rotate(-35deg); }
            .placeholder-label { background: white; padding: 4px 12px; border: 1px solid #ced4da; z-index: 1; text-transform: uppercase; }

            /* Íconos circulares de pilares */
            .pilar-icono { width: 64px; height: 64px; border-radius: 50%; background-color: #ccc; margin: 0 auto 24px auto; }
        </style>
    </head>
    <body class="bg-white d-flex flex-column min-vh-100">
        <!-- Navbar -->
        <nav class="navbar navbar-expand-sm bg-white navbar-light border-bottom sticky-top">
            <div class="container">
                <a class="navbar-brand fw-bold" href="index.php">EL MEDITERRÁNEO</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-center" id="collapsibleNavbar">
                    <ul class="navbar-nav">
                        <li class="nav-item"><a class="nav-link" href="index.php">Inicio</a></li>
                        <li class="nav-item"><a class="nav-link" href="menu.php">Menú</a></li>
                        <li class="nav-item"><a class="nav-link active fw-bold" href="nosotros.php">Nosotros</a></li>
                        <li class="nav-item"><a class="nav-link" href="reservas.php">Reservas</a></li>
                        <li class="nav-item"><a class="nav-link" href="contacto.php">Contacto</a></li>
                    </ul>
                </div>
                <!-- Ícono de carrito -->
                <div class="d-flex align-items-center">
                    <button type="button" class="btn btn-outline-dark me-2 rounded-0">
                        <i class="fa fa-shopping-bag"></i> 2
                    </button>
                </div>
            </div>
        </nav>

        <!-- Contenido Principal -->
        <main class="container mt-5 mb-5 pt-4 flex-grow-1">
            
            <!-- Hero: Nuestra Historia (Layout 2 columnas) -->
            <div class="row align-items-center mb-5 pb-5">
                <!-- Columna Izquierda: Imagen -->
                <div class="col-12 col-md-6 mb-4 mb-md-0">
                    <div class="placeholder-box w-100" style="height: 400px;">
                        <span class="placeholder-label">Imagen Restaurante</span>
                    </div>
                </div>
                
                <!-- Columna Derecha: Textos y Botón -->
                <div class="col-12 col-md-6 ps-md-5">
                    <h1 class="fw-bold text-uppercase mb-4">Nuestra Historia</h1>
                    
                    <!-- Párrafo placeholder -->
                    <div class="placeholder-line" style="width: 100%;"></div>
                    <div class="placeholder-line" style="width: 100%;"></div>
                    <div class="placeholder-line" style="width: 70%;"></div>
                    <div class="placeholder-line" style="width: 100%;"></div>
                    <div class="placeholder-line" style="width: 100%;"></div>
                    <div class="placeholder-line" style="width: 40%; margin-bottom: 32px;"></div>
                    
                    <a href="#" class="btn text-white text-uppercase fw-bold rounded-0 px-4 py-2" style="background-color: #1A1A1A; font-size: 0.9rem;">
                        Conocer más
                    </a>
                </div>
            </div>

            <!-- Sección: Nuestros Pilares -->
            <section class="mt-4 pt-5 border-top">
                <h3 class="fw-bold text-uppercase mb-4">Nuestros Pilares</h3>
                
                <div class="row">
                    <?php foreach ($pilares as $pilar): ?>
                        <div class="col-12 col-md-4 mb-4">
                            <!-- Tarjeta de Pilar -->
                            <div class="card border bg-light h-100 p-4 p-lg-5 text-center rounded-0" style="background-color: #f8f9fa !important;">
                                <!-- Ícono circular -->
                                <div class="pilar-icono"></div>
                                
                                <!-- Título -->
                                <h5 class="fw-bold text-uppercase mb-4" style="font-size: 1.1rem;"><?php echo $pilar['titulo']; ?></h5>
                                
                                <!-- Líneas placeholder generadas desde el array -->
                                <div class="mt-auto">
                                    <?php foreach ($pilar['texto'] as $i => $linea): ?>
                                        <div class="placeholder-line" style="width: <?php echo $i === count($pilar['texto']) - 1 ? '55%' : '90%'; ?>; margin: 0 auto 12px;"></div>
                                    <?php endforeach; ?>
                                </div>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="container-fluid bg-carbon text-white pt-5 pb-3 mt-auto">
            <div class="container">
                <div class="row mb-4">
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">El Mediterráneo</h6>
                        <div class="placeholder-line bg-secondary" style="width: 60%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 40%; margin-top: 8px;"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">Horarios</h6>
                        <div class="placeholder-line bg-secondary" style="width: 50%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 30%; margin-top: 8px;"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">Contacto</h6>
                        <div class="placeholder-line bg-secondary" style="width: 70%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 50%; margin-top: 8px;"></div>
                    </div>
                </div>
                <div class="row border-top border-secondary pt-3">
                    <div class="col-12 text-start" style="font-size: 0.8rem; color: #888;">
                        © 2026 El Mediterráneo. Todos los derechos reservados. Wireframe Layout.
                    </div>
                </div>
            </div>
        </footer>
    </body>
</html>