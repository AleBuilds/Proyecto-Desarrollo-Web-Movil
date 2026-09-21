<?php
$activo = '';

$pedido = [
    'numero'          => '1042',
    'cantidad'        => '3 productos',
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
    <title>Pedido Confirmado — El Mediterráneo</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="bg-crema d-flex flex-column min-vh-100">

    <!-- Navbar -->
    <?php include 'navbar.php'; ?>

    <!-- Contenido Principal -->
    <main class="container py-5 flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center">
        
        <div class="mb-4">
            <div class="bg-fuego text-white rounded-circle d-inline-flex align-items-center justify-content-center shadow mb-3" style="width: 90px; height: 90px;">
                <i class="fa fa-check fs-1"></i>
            </div>
            <h1 class="font-cinzel text-carbon fw-bold text-uppercase mb-2">¡Pedido Confirmado!</h1>
            <p class="text-secondary fs-5">Gracias por tu compra. Tu orden <strong>#<?php echo $pedido['numero']; ?></strong> ha sido recibida con éxito.</p>
        </div>

        <!-- Resumen de Compra -->
        <div class="card border-0 shadow-sm p-4 p-md-5 rounded-3 bg-white w-100 text-start mb-4" style="max-width: 600px;">
            <h5 class="font-cinzel text-tierra fw-bold text-uppercase mb-4 pb-2 border-bottom">Resumen de la Compra</h5>
            
            <div class="d-flex justify-content-between mb-3 text-secondary">
                <span class="fw-bold text-uppercase small">Cantidad de productos:</span>
                <span class="fw-bold text-carbon"><?php echo $pedido['cantidad']; ?></span>
            </div>
            <div class="d-flex justify-content-between mb-3 text-secondary">
                <span class="fw-bold text-uppercase small">Método de entrega:</span>
                <span class="fw-bold text-carbon"><?php echo $pedido['metodo_entrega']; ?></span>
            </div>
            <div class="d-flex justify-content-between mb-4 text-secondary">
                <span class="fw-bold text-uppercase small">Tiempo estimado:</span>
                <span class="fw-bold text-carbon"><?php echo $pedido['tiempo_estimado']; ?></span>
            </div>
            
            <div class="d-flex justify-content-between align-items-center border-top border-warning pt-3">
                <h5 class="font-cinzel fw-bold text-carbon mb-0">Total Pagado:</h5>
                <h4 class="font-cinzel fw-bold text-fuego mb-0"><?php echo clp($pedido['total']); ?></h4>
            </div>
        </div>

        <!-- Botones de Acción -->
        <div class="d-flex flex-column flex-sm-row gap-3 w-100 justify-content-center" style="max-width: 600px;">
            <a href="carrito.php" class="btn btn-fuego text-uppercase fw-bold py-3 flex-grow-1 shadow rounded-3">
                <i class="fa fa-list-alt me-2"></i> Ver Mis Pedidos
            </a>
            <a href="index.php" class="btn btn-outline-carbon text-uppercase fw-bold py-3 flex-grow-1 rounded-3">
                <i class="fa fa-home me-2"></i> Volver al Inicio
            </a>
        </div>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>