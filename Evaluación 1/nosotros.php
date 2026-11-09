<?php
$activo = 'nosotros';

$pilares = [
    ['titulo' => 'Fresco y Natural',   'desc' => 'Ingredientes seleccionados a diario en los mercados locales para garantizar el mejor sabor.', 'img' => 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=400'],
    ['titulo' => 'Receta Tradicional', 'desc' => 'Recetas ancestrales mediterráneas transmitidas de generación en generación con amor y sazón.', 'img' => 'https://images.pexels.com/photos/2233729/pexels-photo-2233729.jpeg?auto=compress&cs=tinysrgb&w=400'],
    ['titulo' => 'Pasión Familiar',    'desc' => 'Un restaurante familiar apasionado por ofrecer la mejor atención y experiencia gastronómica.', 'img' => 'https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&w=400'],
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
    <link rel="stylesheet" href="style.css">
</head>
<body class="bg-crema d-flex flex-column min-vh-100">

    <!-- Navbar -->
    <?php include 'navbar.php'; ?>

    <!-- Contenido Principal -->
    <main class="container py-5 flex-grow-1">
        
        <!-- Hero: Nuestra Historia -->
        <div class="row align-items-center g-5 mb-5">
            <div class="col-12 col-md-6">
                <div class="rounded-3 overflow-hidden shadow">
                    <img src="https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&w=800" class="img-cover w-100" alt="Restaurante El Mediterráneo" style="height: 380px;">
                </div>
            </div>
            
            <div class="col-12 col-md-6">
                <span class="text-oliva text-uppercase fw-bold tracking-wider" style="font-size: 0.8rem;">Conócenos</span>
                <h1 class="font-cinzel text-carbon fw-bold mb-3 fs-2 text-uppercase">Nuestra Historia</h1>
                <p class="text-secondary mb-3">
                    Nacimos del amor por los sabores auténticos de las costas del Mediterráneo. Desde hace más de 15 años preparamos cada plato respetando los métodos tradicionales: asados a las brasas, marinados naturales y pan pita horneado cada mañana.
                </p>
                <p class="text-secondary mb-4">
                    Nuestra misión es llevar a tu mesa la calidez de un festín familiar con la mejor selección de garbanzos, especias orientales y finos cortes de carne.
                </p>
                <a href="menu.php" class="btn btn-fuego text-uppercase fw-bold px-4 py-3 shadow">Descubrir el Menú</a>
            </div>
        </div>

        <!-- Sección: Nuestros Pilares -->
        <section class="pt-5 border-top border-warning">
            <div class="text-center mb-5">
                <h3 class="font-cinzel text-tierra fw-bold text-uppercase fs-2">Nuestros Pilares</h3>
                <div class="bg-fuego mx-auto" style="height: 3px; width: 60px;"></div>
            </div>
            
            <div class="row g-4">
                <?php foreach ($pilares as $pilar): ?>
                    <div class="col-12 col-md-4">
                        <div class="card border-0 shadow-sm h-100 text-center p-4 rounded-3 bg-white card-hover">
                            <img src="<?php echo $pilar['img']; ?>" class="rounded-circle mx-auto mb-3 img-cover" style="width: 100px; height: 100px;" alt="<?php echo $pilar['titulo']; ?>">
                            <h5 class="font-cinzel fw-bold text-carbon text-uppercase mb-2"><?php echo $pilar['titulo']; ?></h5>
                            <p class="text-secondary small mb-0"><?php echo $pilar['desc']; ?></p>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>