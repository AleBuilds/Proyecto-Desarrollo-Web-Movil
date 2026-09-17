<?php
$activo = '';

$pedido = [
    'numero'          => '1042',
    'cantidad'        => '3 items',
    'metodo_entrega'  => 'Despacho a Domicilio',
    'tiempo_estimado' => '30 - 45 min',
    'total'           => 18500,
];

function clp($valor) {
    return '$' . number_format($valor, 0, ',', '.');
}
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Pedido confirmado — El Mediterráneo</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <style>
            /* Paleta de colores base del Wireframe */
            .bg-carbon { background-color: #1A1A1A !important; }
            .bg-crema { background-color: #F3EFE6 !important; }
            .placeholder-line { background-color: #ccc; height: 10px; margin-bottom: 0; border-radius: 4px; }
            
            /* Ícono circular de éxito */
            .success-circle { width: 80px; height: 80px; border-radius: 50%; background-color: #f8f9fa; border: 1px solid #ced4da; margin: 0 auto; display: flex; align-items: center; justify-content: center; }
            
            /* Tarjeta de Resumen */
            .resumen-card { max-width: 600px; width: 100%; border: 1px solid #ced4da; background-color: #f8f9fa; border-radius: 8px; margin: 0 auto; padding: 2rem 3rem; }
            
            /* Botones inferiores */
            .btn-action-group { max-width: 600px; width: 100%; margin: 0 auto; }
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
                        <li class="nav-item"><a class="nav-link" href="nosotros.php">Nosotros</a></li>
                        <li class="nav-item"><a class="nav-link" href="reservas.php">Reservas</a></li>
                        <li class="nav-item"><a class="nav-link" href="contacto.php">Contacto</a></li>
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

        <!-- Contenido Principal -->
        <main class="container mt-5 mb-5 pt-4 flex-grow-1 d-flex flex-column align-items-center text-center">
            
            <!-- Encabezado de Confirmación -->
            <div class="mb-5">
                <div class="success-circle mb-4"></div>
                <h1 class="fw-bold text-uppercase mb-2">Pedido Confirmado</h1>
                <p class="text-muted" style="font-size: 1.1rem;">¡Gracias por tu pedido! N° #<?php echo $pedido['numero']; ?></p>
            </div>

            <!-- Resumen de Compra (Tarjeta Central) -->
            <div class="resumen-card text-start mb-5">
                <h5 class="fw-bold text-uppercase mb-4 pb-2 border-bottom">Resumen de compra</h5>
                
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="text-muted text-uppercase fw-bold" style="font-size: 0.8rem;">Cantidad de productos:</span>
                    <span class="fw-bold text-dark text-end"><?php echo $pedido['cantidad']; ?></span>
                </div>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="text-muted text-uppercase fw-bold" style="font-size: 0.8rem;">Método de entrega:</span>
                    <span class="fw-bold text-dark text-end"><?php echo $pedido['metodo_entrega']; ?></span>
                </div>
                <div class="d-flex justify-content-between align-items-center mb-4 pb-2">
                    <span class="text-muted text-uppercase fw-bold" style="font-size: 0.8rem;">Tiempo estimado:</span>
                    <span class="fw-bold text-dark text-end"><?php echo $pedido['tiempo_estimado']; ?></span>
                </div>
                
                <div class="d-flex justify-content-between align-items-center border-top pt-4 mt-2">
                    <h5 class="fw-bold text-uppercase mb-0">Total pagado:</h5>
                    <h4 class="fw-bold text-dark mb-0"><?php echo clp($pedido['total']); ?></h4>
                </div>
            </div>

            <!-- Botones de Acción -->
            <div class="btn-action-group d-flex flex-column flex-sm-row gap-3">
                <a href="carrito.php" class="btn text-white text-uppercase fw-bold rounded-0 flex-grow-1 py-3" style="background-color: #1A1A1A; font-size: 0.9rem;">
                    Ver mis pedidos
                </a>
                <a href="index.php" class="btn btn-outline-dark text-uppercase fw-bold rounded-0 flex-grow-1 py-3 bg-white" style="font-size: 0.9rem;">
                    Volver al inicio
                </a>
            </div>
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