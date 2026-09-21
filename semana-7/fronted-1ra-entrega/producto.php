<?php
$activo = 'menu';

$producto = [
    'categoria'    => 'Parrilla',
    'nombre'       => 'Brochetas de Cordero Premium',
    'precio'       => 14500,
    'imagen'       => 'https://images.pexels.com/photos/2233729/pexels-photo-2233729.jpeg?auto=compress&cs=tinysrgb&w=800',
    'descripcion'  => 'Jugosas brochetas de cordero tierno marinadas durante 24 horas con finas especias mediterráneas, pimientos rojos y cebollas asadas a fuego directo de carbón vegetal. Acompañadas de salsa tahini artesanal y pan pita recién horneado.',
    'ingredientes' => [
        'Carne de cordero tierna maridada en finas hierbas',
        'Especias mediterráneas tradicionales (comino, zaatar, sumac)',
        'Pimientos dulces y cebollas asadas al carbón',
        'Salsa tahini artesanal de sésamo con toque de limón',
        'Porción de pan pita artesanal tibio'
    ],
];

$relacionados = [
    ['categoria' => 'Salsas',          'label' => 'SALSAS',          'nombre' => 'Salsa de Ajo',       'precio' => 1500, 'img' => 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=400'],
    ['categoria' => 'Acompañamientos', 'label' => 'ACOMPAÑAMIENTOS', 'nombre' => 'Pan Pita Adicional', 'precio' => 800,  'img' => 'https://images.pexels.com/photos/6287525/pexels-photo-6287525.jpeg?auto=compress&cs=tinysrgb&w=400'],
    ['categoria' => 'Bebidas',         'label' => 'BEBIDAS',         'nombre' => 'Té de Menta Frío',   'precio' => 2200, 'img' => 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?auto=compress&cs=tinysrgb&w=400'],
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
    <link rel="stylesheet" href="style.css">
</head>
<body class="bg-crema d-flex flex-column min-vh-100">

    <!-- Navbar -->
    <?php include 'navbar.php'; ?>

    <!-- Detalle del Producto -->
    <main class="container py-5 my-auto flex-grow-1">
        <div class="row bg-white rounded-3 shadow-sm p-4 p-md-5 g-4 align-items-center">
            <!-- Imagen Principal -->
            <div class="col-12 col-md-6">
                <div class="rounded-3 overflow-hidden shadow-sm" style="max-height: 480px;">
                    <img src="<?php echo $producto['imagen']; ?>" class="img-cover w-100" alt="<?php echo $producto['nombre']; ?>" style="object-fit: cover; height: 420px;">
                </div>
            </div>
            
            <!-- Información y Acciones -->
            <div class="col-12 col-md-6 ps-md-4">
                <small class="text-oliva text-uppercase fw-bold tracking-wider" style="font-size: 0.8rem;">Categoría · <?php echo $producto['categoria']; ?></small>
                <h1 class="font-cinzel text-carbon fw-bold my-2 fs-2"><?php echo $producto['nombre']; ?></h1>
                <h3 class="fw-bold text-fuego fs-3 mb-3"><?php echo clp($producto['precio']); ?></h3>
                
                <!-- Descripción Real -->
                <h6 class="font-cinzel text-tierra text-uppercase fw-bold mb-2">Descripción</h6>
                <p class="text-secondary small mb-4"><?php echo $producto['descripcion']; ?></p>

                <!-- Ingredientes reales -->
                <h6 class="font-cinzel text-tierra text-uppercase fw-bold mb-2">Ingredientes Reales</h6>
                <ul class="text-secondary ps-3 mb-4 small">
                    <?php foreach ($producto['ingredientes'] as $ingrediente): ?>
                        <li class="mb-1"><i class="fa fa-check text-oliva me-2"></i><?php echo $ingrediente; ?></li>
                    <?php endforeach; ?>
                </ul>

                <!-- Controles de Carrito -->
                <div class="d-flex align-items-stretch gap-3 mt-4 pt-2 border-top">
                    <!-- Stepper -->
                    <div class="input-group" style="width: 130px;">
                        <button class="btn btn-outline-secondary font-bold" type="button" onclick="var el=document.getElementById('cant'); if(parseInt(el.value)>1) el.value=parseInt(el.value)-1;">-</button>
                        <input type="text" id="cant" class="form-control text-center bg-white fw-bold" value="1" readonly>
                        <button class="btn btn-outline-secondary font-bold" type="button" onclick="var el=document.getElementById('cant'); el.value=parseInt(el.value)+1;">+</button>
                    </div>
                    <!-- Botón Agregar -->
                    <a href="carrito.php" class="btn btn-fuego text-uppercase fw-bold flex-grow-1 d-flex align-items-center justify-content-center">
                        <i class="fa fa-cart-plus me-2"></i> Agregar al Carrito
                    </a>
                </div>
            </div>
        </div>
    </main>

    <!-- Sección de Productos Relacionados -->
    <section class="bg-white py-5 border-top border-warning">
        <div class="container">
            <h3 class="font-cinzel text-tierra fw-bold mb-4 text-uppercase text-center">También te puede gustar</h3>
            <div class="row g-4">
                <?php foreach ($relacionados as $p): ?>
                    <div class="col-12 col-md-4">
                        <div class="card border-0 shadow-sm card-hover h-100 rounded-3 overflow-hidden">
                            <a href="#" class="text-decoration-none">
                                <img src="<?php echo $p['img']; ?>" class="card-img-top img-cover" alt="<?php echo $p['nombre']; ?>" style="height: 180px;">
                            </a>
                            <div class="card-body p-3 d-flex flex-column">
                                <small class="text-oliva text-uppercase fw-bold" style="font-size: 0.75rem;"><?php echo $p['label']; ?></small>
                                <h5 class="font-cinzel fw-bold text-carbon mt-1 mb-3 fs-6"><?php echo $p['nombre']; ?></h5>
                                
                                <div class="d-flex justify-content-between align-items-center border-top pt-2 mt-auto">
                                    <span class="fw-bold text-fuego fs-6"><?php echo clp($p['precio']); ?></span>
                                    <a href="carrito.php" class="btn btn-fuego btn-sm text-uppercase px-3 fw-bold">Agregar</a>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <?php include 'footer.php'; ?>