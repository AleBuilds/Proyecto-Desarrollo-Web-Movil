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
    ['categoria' => 'hummus',    'label' => 'HUMMUS',    'nombre' => 'Hummus Especial',    'precio' => 5200,  'img' => 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Garbanzos molidos con suave crema de sésamo, limón y toque de pimentón.'],
    ['categoria' => 'falafel',   'label' => 'FALAFEL',   'nombre' => 'Falafel Wrap',       'precio' => 4900,  'img' => 'https://images.pexels.com/photos/6287525/pexels-photo-6287525.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Wrap en pan pita con falafels crujientes, lechuga, tomate y salsa tahini.'],
    ['categoria' => 'shawarma',  'label' => 'SHAWARMA',  'nombre' => 'Shawarma Pollo',     'precio' => 6500,  'img' => 'https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Láminas de pollo marinado con especias finas, vegetales frescos y salsa especial.'],
    ['categoria' => 'parrilla',  'label' => 'PARRILLA',  'nombre' => 'Brochetas de Cordero Premium', 'precio' => 14500, 'img' => 'https://images.pexels.com/photos/2233729/pexels-photo-2233729.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Tiernas brochetas de cordero marinadas a las brasas con pimientos y cebollas.'],
    ['categoria' => 'pescados',  'label' => 'PESCADOS',  'nombre' => 'Pescado del Día',    'precio' => 12000, 'img' => 'https://images.pexels.com/photos/262959/pexels-photo-262959.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Filete de pescado a la plancha con finas hierbas y limón marroquí.'],
    ['categoria' => 'ensaladas', 'label' => 'ENSALADAS', 'nombre' => 'Ensalada Griega',    'precio' => 5500,  'img' => 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Tomates frescos, pepino, aceitunas kalamata, cebolla morada y queso feta.'],
    ['categoria' => 'hummus',    'label' => 'HUMMUS',    'nombre' => 'Hummus con Carne',   'precio' => 6800,  'img' => 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Hummus suave coronado con carne salteada de ternera y piñones tostados.'],
    ['categoria' => 'falafel',   'label' => 'FALAFEL',   'nombre' => 'Falafel Plato',      'precio' => 7200,  'img' => 'https://images.pexels.com/photos/6287525/pexels-photo-6287525.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => '8 piezas de falafel acompanadas de tabbouleh, hummus y pan pita caliente.'],
    ['categoria' => 'shawarma',  'label' => 'SHAWARMA',  'nombre' => 'Shawarma Ternera',   'precio' => 7200,  'img' => 'https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=600', 'desc' => 'Cortes selectos de ternera especiada en pan lavash con parde de salsas.'],
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
    <link rel="stylesheet" href="style.css">
</head>
<body class="bg-crema d-flex flex-column min-vh-100">

    <!-- Navbar -->
    <?php include 'navbar.php'; ?>

    <!-- Banner Menú -->
    <section class="bg-tierra text-white py-4 mb-4 border-bottom border-warning border-3">
        <div class="container text-center">
            <h1 class="font-cinzel text-sol fw-bold text-uppercase mb-1">Nuestro Menú</h1>
            <p class="text-light small mb-0">Selecciona una categoría o explora nuestra carta gastronómica</p>
        </div>
    </section>

    <!-- Contenido Principal -->
    <main class="container mb-5 flex-grow-1">
        <!-- Filtros de Categoría -->
        <div class="filtros mb-4 text-center">
            <?php foreach ($categorias as $slug => $label): ?>
                <a class="filtro-pill <?php echo $categoriaSeleccionada === $slug ? 'activo' : ''; ?>"
                   href="menu.php<?php echo $slug === 'todos' ? '' : '?categoria=' . $slug; ?>">
                   <?php echo $label; ?>
                </a>
            <?php endforeach; ?>
        </div>

        <!-- Grilla de Productos -->
        <div class="row g-4">
            <?php foreach ($platos as $p): ?>
                <?php 
                    if ($categoriaSeleccionada !== 'todos' && $p['categoria'] !== $categoriaSeleccionada) { 
                        continue; 
                    } 
                ?>
                <div class="col-12 col-md-6 col-lg-4">
                    <article class="card h-100 border-0 shadow-sm card-hover rounded-3 overflow-hidden">
                        <a href="producto.php" class="text-decoration-none">
                            <img src="<?php echo $p['img']; ?>" class="card-img-top img-cover" alt="<?php echo $p['nombre']; ?>" style="height: 230px;">
                        </a>
                        <div class="card-body d-flex flex-column p-4 bg-white">
                            <small class="text-oliva text-uppercase fw-bold tracking-wider mb-1" style="font-size: 0.75rem;"><?php echo $p['label']; ?></small>
                            <h4 class="card-title font-cinzel fw-bold mt-1 mb-2">
                                <a href="producto.php" class="text-carbon text-decoration-none fs-5"><?php echo $p['nombre']; ?></a>
                            </h4>
                            <p class="text-secondary small mb-4 flex-grow-1"><?php echo $p['desc']; ?></p>
                            
                            <div class="d-flex justify-content-between align-items-center border-top pt-3 mt-auto">
                                <span class="fw-bold text-fuego fs-5"><?php echo clp($p['precio']); ?></span>
                                <a href="carrito.php" class="btn btn-fuego btn-sm text-uppercase px-3 fw-bold">Agregar</a>
                            </div>
                        </div>
                    </article>
                </div>
            <?php endforeach; ?>
        </div>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>