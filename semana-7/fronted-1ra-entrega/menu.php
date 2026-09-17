<?php
$activo = 'menu';
$categoriaSeleccionada = isset($_GET['categoria']) ? $_GET['categoria'] : 'todos';

$categorias = [
    'todos'    => 'Todos',
    'hummus'   => 'Hummus',
    'falafel'  => 'Falafel',
    'shawarma' => 'Shawarma',
    'parrilla' => 'Parrilla',
    'pescados' => 'Pescados',
    'ensaladas'=> 'Ensaladas',
];

$platos = [
    ['categoria' => 'hummus',    'label' => 'HUMMUS',    'nombre' => 'Hummus Especial',    'precio' => 5200],
    ['categoria' => 'falafel',   'label' => 'FALAFEL',   'nombre' => 'Falafel Wrap',       'precio' => 4900],
    ['categoria' => 'shawarma',  'label' => 'SHAWARMA',  'nombre' => 'Shawarma Pollo',     'precio' => 6500],
    ['categoria' => 'parrilla',  'label' => 'PARRILLA',  'nombre' => 'Brocheta de Carne',  'precio' => 8900],
    ['categoria' => 'pescados',  'label' => 'PESCADOS',  'nombre' => 'Pescado del Día',    'precio' => 12000],
    ['categoria' => 'ensaladas', 'label' => 'ENSALADAS', 'nombre' => 'Ensalada Griega',    'precio' => 5500],
    ['categoria' => 'hummus',    'label' => 'HUMMUS',    'nombre' => 'Hummus con Carne',   'precio' => 6800],
    ['categoria' => 'falafel',   'label' => 'FALAFEL',   'nombre' => 'Falafel Plato',      'precio' => 7200],
    ['categoria' => 'shawarma',  'label' => 'SHAWARMA',  'nombre' => 'Shawarma Ternera',   'precio' => 7200],
];

function clp($valor) {
    return '$' . number_format($valor, 0, ',', '.');
}
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Menú — El Mediterráneo</title>
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
            /* Filtros */
            .filtro-pill { padding: 8px 20px; border: 1px solid #ccc; color: #333; text-decoration: none; display: inline-block; margin-right: 5px; margin-bottom: 10px; font-size: 0.9rem; }
            .filtro-pill.activo { background-color: #1A1A1A; color: white; border-color: #1A1A1A; font-weight: bold; }
            .filtro-pill:hover:not(.activo) { background-color: #f8f9fa; }
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
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle active fw-bold" href="menu.php" role="button" data-bs-toggle="dropdown">Menú</a>
                            <ul class="dropdown-menu rounded-0">
                                <?php foreach ($categorias as $slug => $label): ?>
                                    <li><a class="dropdown-item" href="menu.php<?php echo $slug === 'todos' ? '' : '?categoria=' . $slug; ?>"><?php echo $label; ?></a></li>
                                <?php endforeach; ?>
                            </ul>
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

        <!-- Contenido Principal -->
        <main class="container mt-5 mb-5">
            <!-- Título -->
            <h1 class="fw-bold mb-4 text-uppercase">Menú</h1>

            <!-- Filtros de Categoría -->
            <div class="filtros mb-5 d-flex flex-wrap">
                <?php foreach ($categorias as $slug => $label): ?>
                    <a class="filtro-pill rounded-0 <?php echo $categoriaSeleccionada === $slug ? 'activo' : ''; ?>"
                       href="menu.php<?php echo $slug === 'todos' ? '' : '?categoria=' . $slug; ?>">
                       <?php echo $label; ?>
                    </a>
                <?php endforeach; ?>
            </div>

            <!-- Grilla de Productos (Proporción 3 columnas) -->
            <div class="row">
                <?php foreach ($platos as $p): ?>
                    <?php 
                        // Lógica de filtrado: si no es 'todos' y la categoría no coincide, saltamos el producto
                        if ($categoriaSeleccionada !== 'todos' && $p['categoria'] !== $categoriaSeleccionada) { 
                            continue; 
                        } 
                    ?>
                    <!-- Tarjeta de Producto -->
                    <div class="col-12 col-md-4 mb-5">
                        <article class="card border-0">
                            <a href="producto.php" aria-label="Ver <?php echo $p['nombre']; ?>" class="text-decoration-none">
                                <div class="placeholder-box mb-3" style="height: 240px;">
                                    <span class="border bg-white px-2 py-1 text-muted">IMAGEN PRODUCTO</span>
                                </div>
                            </a>
                            <div class="card-body px-0 pt-0">
                                <small class="text-muted text-uppercase fw-bold" style="font-size: 0.75rem;"><?php echo $p['label']; ?></small>
                                <h4 class="card-title fw-bold mt-1 mb-3">
                                    <a href="producto.php" class="text-dark text-decoration-none"><?php echo $p['nombre']; ?></a>
                                </h4>
                                <!-- Descripción Simulada (Líneas grises) -->
                                <div class="placeholder-line" style="width: 100%;"></div>
                                <div class="placeholder-line" style="width: 50%; margin-bottom: 24px;"></div>
                                
                                <!-- Precio y Botón -->
                                <div class="d-flex justify-content-between align-items-center border-top pt-3">
                                    <span class="fw-bold fs-5 text-dark"><?php echo clp($p['precio']); ?></span>
                                    <button class="btn btn-outline-dark text-uppercase rounded-0 px-4 fw-bold" style="font-size: 0.85rem;" type="button">Agregar</button>
                                </div>
                            </div>
                        </article>
                    </div>
                <?php endforeach; ?>
            </div>
        </main>

        <!-- Footer -->
        <footer class="container-fluid bg-carbon text-white pt-5 pb-3 mt-auto">
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