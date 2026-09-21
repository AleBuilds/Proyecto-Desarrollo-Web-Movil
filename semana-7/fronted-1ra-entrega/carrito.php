<?php
$activo = '';

$items = [
    [
        'nombre' => 'Shawarma Ternera Especial',
        'precio_unitario' => 7200,
        'cantidad' => 1,
        'img' => 'https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=300'
    ],
    [
        'nombre' => 'Plato Falafel Grande',
        'precio_unitario' => 6200,
        'cantidad' => 2,
        'img' => 'https://images.pexels.com/photos/6287525/pexels-photo-6287525.jpeg?auto=compress&cs=tinysrgb&w=300'
    ],
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
    <title>Tu Carrito — El Mediterráneo</title>
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

    <!-- Contenido del Carrito -->
    <main class="container py-5 flex-grow-1">
        <h1 class="font-cinzel text-carbon fw-bold mb-4 text-uppercase text-center text-md-start">Tu Carrito de Compras</h1>

        <div class="row g-4">
            <!-- Lista de Productos -->
            <div class="col-12 col-lg-8">
                <?php foreach ($items as $index => $item): ?>
                    <div class="card border-0 shadow-sm mb-3 rounded-3 overflow-hidden p-3 bg-white">
                        <div class="d-flex align-items-center flex-wrap gap-3">
                            <!-- Imagen del producto -->
                            <img src="<?php echo $item['img']; ?>" class="rounded-3 img-cover" alt="<?php echo $item['nombre']; ?>" style="width: 85px; height: 85px;">
                            
                            <!-- Info Producto -->
                            <div class="flex-grow-1">
                                <h6 class="font-cinzel fw-bold text-carbon mb-1 fs-6"><?php echo $item['nombre']; ?></h6>
                                <small class="text-secondary">Precio unitario: <span class="text-fuego fw-bold"><?php echo clp($item['precio_unitario']); ?></span></small>
                            </div>
                            
                            <!-- Stepper de Cantidad -->
                            <div class="input-group rounded-2" style="width: 105px;">
                                <button class="btn btn-sm btn-outline-secondary font-bold" type="button">-</button>
                                <input type="text" class="form-control form-control-sm text-center bg-white fw-bold" value="<?php echo $item['cantidad']; ?>" readonly>
                                <button class="btn btn-sm btn-outline-secondary font-bold" type="button">+</button>
                            </div>
                            
                            <!-- Subtotal -->
                            <div class="fw-bold text-carbon fs-6 text-end px-2" style="min-width: 90px;">
                                <?php echo clp($item['precio_unitario'] * $item['cantidad']); ?>
                            </div>
                            
                            <!-- Eliminar -->
                            <button class="btn btn-link text-danger p-1" type="button" title="Eliminar producto">
                                <i class="fa fa-trash fs-5"></i>
                            </button>
                        </div>
                    </div>
                <?php endforeach; ?>

                <div class="d-flex justify-content-between align-items-center mt-4">
                    <a href="menu.php" class="btn btn-outline-carbon btn-sm text-uppercase fw-bold"><i class="fa fa-arrow-left me-2"></i> Seguir Comprando</a>
                </div>
            </div>

            <!-- Panel de Resumen -->
            <div class="col-12 col-lg-4">
                <aside class="card border-0 shadow-sm p-4 rounded-3 bg-white">
                    <h4 class="font-cinzel text-tierra fw-bold text-uppercase mb-4 pb-2 border-bottom">Resumen del Pedido</h4>
                    
                    <div class="d-flex justify-content-between mb-3 text-secondary">
                        <span>Subtotal de productos</span>
                        <span class="fw-bold text-carbon"><?php echo clp($subtotal); ?></span>
                    </div>
                    
                    <div class="d-flex justify-content-between mb-4 text-secondary">
                        <span>Envío estimado (Delivery)</span>
                        <span class="fw-bold text-carbon"><?php echo clp($envio); ?></span>
                    </div>
                    
                    <div class="d-flex justify-content-between mb-4 pt-3 border-top border-warning">
                        <h5 class="font-cinzel fw-bold text-carbon mb-0">Total</h5>
                        <h5 class="font-cinzel fw-bold text-fuego mb-0"><?php echo clp($total); ?></h5>
                    </div>
                    
                    <a href="entrega.php" class="btn btn-fuego w-100 rounded-3 text-uppercase fw-bold py-3 shadow">
                        Continuar a la Entrega <i class="fa fa-arrow-right ms-2"></i>
                    </a>
                </aside>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>