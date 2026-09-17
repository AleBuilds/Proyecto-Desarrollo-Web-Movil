<?php
$activo = 'menu';

$producto = [
    'categoria'    => 'Parrilla',
    'nombre'       => 'Brochetas de Cordero Premium',
    'precio'       => 14500,
    'descripcion'  => 'Brochetas de cordero marinadas con especias mediterráneas, asadas a la parrilla y servidas con acompañamientos tradicionales de la casa.',
    'ingredientes' => [
        'Carne de cordero tierna maridada',
        'Especias mediterráneas tradicionales',
        'Pimientos y cebollas asadas',
        'Salsa tahini artesanal de acompañamiento',
    ],
];

$relacionados = [
    ['categoria' => 'Salsas',          'label' => 'SALSAS',          'nombre' => 'Salsa de Ajo',       'precio' => 1500],
    ['categoria' => 'Acompañamientos', 'label' => 'ACOMPAÑAMIENTOS', 'nombre' => 'Pan Pita Adicional', 'precio' => 800],
    ['categoria' => 'Bebidas',         'label' => 'BEBIDAS',         'nombre' => 'Té de Menta Frío',   'precio' => 2200],
];

function clp($valor) {
    return '$' . number_format($valor, 0, ',', '.');
}
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <title><?php echo $producto['nombre']; ?> — El Mediterráneo</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <style>
            /* Paleta de colores base del Wireframe */
            .bg-carbon { background-color: #1A1A1A !important; }
            .bg-crema { background-color: #F3EFE6 !important; }
            .placeholder-line { background-color: #ccc; height: 12px; margin-bottom: 8px; border-radius: 4px; }
            .placeholder-box { background-color: #e9ecef; border: 1px solid #ced4da; display: flex; align-items: center; justify-content: center; color: #6c757d; font-size: 0.8rem; font-weight: bold; }
        </style>
    </head>
    <body class="bg-white">
        <!-- Navbar -->
        <nav class="navbar navbar-expand-sm bg-white navbar-light border-bottom sticky-top">
            <div class="container">
                <a class="navbar-brand fw-bold" href="index.php">EL MEDITERRÁNEO</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-center" id="collapsibleNavbar">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="index.php">Inicio</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active fw-bold" href="menu.php">Menú</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="nosotros.php">Nosotros</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="reservas.php">Reservas</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="contacto.php">Contacto</a>
                        </li>
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

        <!-- Detalle del Producto -->
        <main class="container mt-5 mb-5 pt-3">
            <div class="row">
                <!-- Columna Izquierda: Imagen Principal -->
                <div class="col-12 col-md-6 mb-4 mb-md-0">
                    <div class="placeholder-box w-100" style="height: 500px;">
                        <span class="border bg-white px-3 py-2 text-muted">IMAGEN PRODUCTO PRINCIPAL</span>
                    </div>
                </div>
                
                <!-- Columna Derecha: Información y Acciones -->
                <div class="col-12 col-md-6 ps-md-5 d-flex flex-column justify-content-center">
                    <small class="text-muted text-uppercase fw-bold mb-2" style="font-size: 0.8rem;">Categoría · <?php echo $producto['categoria']; ?></small>
                    <h1 class="fw-bold mb-3"><?php echo $producto['nombre']; ?></h1>
                    <h3 class="fw-bold text-dark mb-4"><?php echo clp($producto['precio']); ?></h3>
                    
                    <!-- Descripción simulada (Líneas grises) -->
                    <h6 class="fw-bold text-uppercase mb-3 mt-2" style="font-size: 0.85rem;">Descripción</h6>
                    <div class="placeholder-line" style="width: 100%;"></div>
                    <div class="placeholder-line" style="width: 100%;"></div>
                    <div class="placeholder-line" style="width: 40%; margin-bottom: 24px;"></div>

                    <!-- Ingredientes reales desde el array -->
                    <h6 class="fw-bold text-uppercase mb-3" style="font-size: 0.85rem;">Ingredientes</h6>
                    <ul class="text-muted ps-3 mb-5" style="font-size: 0.95rem; color: #555;">
                        <?php foreach ($producto['ingredientes'] as $ingrediente): ?>
                            <li class="mb-2"><?php echo $ingrediente; ?></li>
                        <?php endforeach; ?>
                    </ul>

                    <!-- Controles de Carrito (Stepper + Botón) -->
                    <div class="d-flex align-items-stretch mt-auto">
                        <!-- Stepper de cantidad -->
                        <div class="input-group rounded-0 me-3" style="width: 140px; border: 1px solid #ced4da;">
                            <button class="btn btn-light rounded-0 border-0 px-3 text-dark fw-bold bg-white" type="button" aria-label="Restar cantidad">-</button>
                            <input type="text" class="form-control border-0 text-center rounded-0 fw-bold bg-white px-0" value="1" readonly aria-label="Cantidad">
                            <button class="btn btn-light rounded-0 border-0 px-3 text-dark fw-bold bg-white" type="button" aria-label="Sumar cantidad">+</button>
                        </div>
                        <!-- Botón Agregar -->
                        <button class="btn text-white rounded-0 flex-grow-1 text-uppercase fw-bold" style="background-color: #1A1A1A; font-size: 0.9rem;" type="button">Agregar al carrito</button>
                    </div>
                </div>
            </div>
        </main>

        <!-- Sección de Productos Relacionados -->
        <section class="container-fluid border-top pt-5 pb-5 bg-white">
            <div class="container">
                <h3 class="fw-bold mb-4 text-uppercase">También te puede gustar</h3>
                <div class="row">
                    <?php foreach ($relacionados as $p): ?>
                        <div class="col-12 col-md-4 mb-4">
                            <article class="card border-0">
                                <a href="#" aria-label="Ver <?php echo $p['nombre']; ?>" class="text-decoration-none">
                                    <div class="placeholder-box mb-3" style="height: 220px;">
                                        <span class="border bg-white px-2 py-1 text-muted">IMAGEN PRODUCTO</span>
                                    </div>
                                </a>
                                <div class="card-body px-0 pt-0">
                                    <small class="text-muted text-uppercase fw-bold" style="font-size: 0.75rem;"><?php echo $p['label']; ?></small>
                                    <h5 class="card-title fw-bold mt-1 mb-3 text-dark">
                                        <?php echo $p['nombre']; ?>
                                    </h5>
                                    <div class="placeholder-line" style="width: 100%;"></div>
                                    <div class="placeholder-line" style="width: 50%; margin-bottom: 20px;"></div>
                                    
                                    <div class="d-flex justify-content-between align-items-center border-top pt-3">
                                        <span class="fw-bold fs-6 text-dark"><?php echo clp($p['precio']); ?></span>
                                        <button class="btn btn-outline-dark text-uppercase rounded-0 px-4 fw-bold" style="font-size: 0.8rem;" type="button">Agregar</button>
                                    </div>
                                </div>
                            </article>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="container-fluid bg-carbon text-white pt-5 pb-3">
            <div class="container">
                <div class="row mb-4">
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">El Mediterráneo</h6>
                        <div class="placeholder-line bg-secondary" style="width: 60%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 40%;"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">Horarios</h6>
                        <div class="placeholder-line bg-secondary" style="width: 50%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 30%;"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">Contacto</h6>
                        <div class="placeholder-line bg-secondary" style="width: 70%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 50%;"></div>
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