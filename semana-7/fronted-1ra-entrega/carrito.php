<?php
$activo = '';

$items = [
    ['nombre' => 'Shawarma Ternera Especial', 'precio_unitario' => 7200, 'cantidad' => 1],
    ['nombre' => 'Plato Falafel Grande',      'precio_unitario' => 6200, 'cantidad' => 2],
];

$envio = 2500;

function clp($valor) {
    return '$' . number_format($valor, 0, ',', '.');
}

$subtotal = 0;
foreach ($items as $item) {
    $subtotal += $item['precio_unitario'] * $item['cantidad'];
}
$total = $subtotal + $envio;
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Tu carrito — El Mediterráneo</title>
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
                        <li class="nav-item">
                            <a class="nav-link" href="index.php">Inicio</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="menu.php">Menú</a>
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
                    <button type="button" class="btn btn-dark me-2 rounded-0" style="background-color: #1A1A1A;">
                        <i class="fa fa-shopping-bag"></i> 2
                    </button>
                </div>
            </div>
        </nav>

        <!-- Contenido del Carrito -->
        <main class="container mt-5 mb-5 pt-3 flex-grow-1">
            <h1 class="fw-bold mb-5 text-uppercase">Tu carrito</h1>

            <div class="row">
                <!-- Columna Izquierda: Lista de Productos -->
                <div class="col-12 col-lg-8 mb-4 mb-lg-0">
                    <?php foreach ($items as $item): ?>
                        <div class="d-flex align-items-center border p-3 mb-3 bg-white">
                            <!-- Imagen Placeholder -->
                            <div class="placeholder-box me-4" style="width: 80px; height: 80px; flex-shrink: 0;">
                                <span class="border bg-white px-2 py-1 text-muted" style="font-size: 0.7rem;">X</span>
                            </div>
                            
                            <!-- Info Producto -->
                            <div class="flex-grow-1">
                                <h6 class="fw-bold mb-1"><?php echo $item['nombre']; ?></h6>
                                <small class="text-muted" style="font-size: 0.8rem;">Precio unitario: <?php echo clp($item['precio_unitario']); ?></small>
                            </div>
                            
                            <!-- Stepper de Cantidad -->
                            <div class="input-group ms-3 me-4 rounded-0" style="width: 100px; border: 1px solid #ced4da; flex-shrink: 0;">
                                <button class="btn btn-sm btn-light border-0 px-2 bg-white fw-bold text-muted" type="button" aria-label="Restar cantidad">-</button>
                                <input type="text" class="form-control form-control-sm border-0 text-center bg-white fw-bold px-0" value="<?php echo $item['cantidad']; ?>" readonly aria-label="Cantidad">
                                <button class="btn btn-sm btn-light border-0 px-2 bg-white fw-bold text-muted" type="button" aria-label="Sumar cantidad">+</button>
                            </div>
                            
                            <!-- Subtotal de Línea -->
                            <div class="fw-bold ms-2 me-4 text-end" style="width: 80px; flex-shrink: 0;">
                                <?php echo clp($item['precio_unitario'] * $item['cantidad']); ?>
                            </div>
                            
                            <!-- Botón Eliminar -->
                            <button class="btn btn-link text-dark p-0" type="button" aria-label="Eliminar producto">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="3 6 5 6 21 6"></polyline>
                                    <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                                    <path d="M10 11v6"></path>
                                    <path d="M14 11v6"></path>
                                </svg>
                            </button>
                        </div>
                    <?php endforeach; ?>
                </div>

                <!-- Columna Derecha: Panel de Resumen -->
                <div class="col-12 col-lg-4 ps-lg-4">
                    <aside class="bg-crema p-4 border">
                        <h4 class="fw-bold text-uppercase mb-4">Resumen</h4>
                        
                        <div class="d-flex justify-content-between mb-3" style="font-size: 0.9rem;">
                            <span class="text-muted">Subtotal</span>
                            <span class="fw-bold text-dark"><?php echo clp($subtotal); ?></span>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-4" style="font-size: 0.9rem;">
                            <span class="text-muted">Envío estimado</span>
                            <span class="fw-bold text-dark"><?php echo clp($envio); ?></span>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-4 pt-3 border-top border-secondary">
                            <h5 class="fw-bold mb-0">Total</h5>
                            <h5 class="fw-bold mb-0"><?php echo clp($total); ?></h5>
                        </div>
                        
                        <a href="entrega.php" class="btn text-white w-100 rounded-0 text-uppercase fw-bold" style="background-color: #1A1A1A; font-size: 0.9rem; padding: 12px 0;">
                            Continuar compra
                        </a>
                    </aside>
                </div>
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