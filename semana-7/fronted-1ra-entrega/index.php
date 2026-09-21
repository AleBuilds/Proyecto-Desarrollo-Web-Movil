<?php
$activo = 'inicio';
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Inicio — El Mediterráneo</title>
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

    <!-- Hero Section -->
    <section class="position-relative py-5 overflow-hidden text-center text-white bg-carbon" style="background: linear-gradient(rgba(26,26,26,0.7), rgba(59,42,32,0.85)), url('https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1400&q=80') center/cover no-repeat; min-height: 480px;">
        <div class="container py-5 my-auto position-relative z-1">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <span class="text-sol font-cinzel text-uppercase tracking-widest fw-bold mb-2 d-block">Sabor Tradicional & Artesanal</span>
                    <h1 class="display-3 font-cinzel fw-bold mb-3 text-uppercase">El Mediterráneo</h1>
                    <p class="lead text-light mb-4 px-md-5 font-monospace fs-5">
                        Descubre los mejores sabores de la cocina mediterránea: hummus suave, falafel crujiente, shawarmas jugosos y carnes a la parrilla.
                    </p>
                    <div class="d-flex justify-content-center gap-3 flex-wrap">
                        <a href="menu.php" class="btn btn-fuego btn-lg px-4 py-3 text-uppercase shadow">Ver Menú Completo</a>
                        <a href="reservas.php" class="btn btn-outline-light btn-lg px-4 py-3 text-uppercase fw-bold">Reservar Mesa</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Nuestras Especialidades -->
    <section class="container py-5">
        <div class="text-center mb-5">
            <h2 class="font-cinzel text-tierra fw-bold text-uppercase fs-2">Nuestras Especialidades</h2>
            <div class="bg-fuego mx-auto" style="height: 3px; width: 60px;"></div>
        </div>
        
        <div class="row g-4 text-center">
            <div class="col-6 col-md-3">
                <a href="menu.php?categoria=hummus" class="card border-0 shadow-sm h-100 text-decoration-none card-hover overflow-hidden rounded-3">
                    <img src="https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600" class="card-img-top img-cover" alt="Hummus" style="height: 180px;">
                    <div class="card-body bg-white py-3">
                        <h5 class="font-cinzel fw-bold text-carbon text-uppercase mb-0 fs-6">Hummus</h5>
                    </div>
                </a>
            </div>
            <div class="col-6 col-md-3">
                <a href="menu.php?categoria=falafel" class="card border-0 shadow-sm h-100 text-decoration-none card-hover overflow-hidden rounded-3">
                    <img src="https://images.pexels.com/photos/6287525/pexels-photo-6287525.jpeg?auto=compress&cs=tinysrgb&w=600" class="card-img-top img-cover" alt="Falafel" style="height: 180px;">
                    <div class="card-body bg-white py-3">
                        <h5 class="font-cinzel fw-bold text-carbon text-uppercase mb-0 fs-6">Falafel</h5>
                    </div>
                </a>
            </div>
            <div class="col-6 col-md-3">
                <a href="menu.php?categoria=shawarma" class="card border-0 shadow-sm h-100 text-decoration-none card-hover overflow-hidden rounded-3">
                    <img src="https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=600" class="card-img-top img-cover" alt="Shawarma" style="height: 180px;">
                    <div class="card-body bg-white py-3">
                        <h5 class="font-cinzel fw-bold text-carbon text-uppercase mb-0 fs-6">Shawarma</h5>
                    </div>
                </a>
            </div>
            <div class="col-6 col-md-3">
                <a href="menu.php?categoria=parrilla" class="card border-0 shadow-sm h-100 text-decoration-none card-hover overflow-hidden rounded-3">
                    <img src="https://images.pexels.com/photos/2233729/pexels-photo-2233729.jpeg?auto=compress&cs=tinysrgb&w=600" class="card-img-top img-cover" alt="Parrilla" style="height: 180px;">
                    <div class="card-body bg-white py-3">
                        <h5 class="font-cinzel fw-bold text-carbon text-uppercase mb-0 fs-6">Parrilla</h5>
                    </div>
                </a>
            </div>
        </div>
    </section>

    <!-- Productos Destacados -->
    <section class="bg-white py-5 border-top border-bottom border-warning">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="font-cinzel text-tierra fw-bold text-uppercase fs-2">Productos Destacados</h2>
                <div class="bg-fuego mx-auto" style="height: 3px; width: 60px;"></div>
            </div>

            <div class="row g-4">
                <!-- Tarjeta 1 -->
                <div class="col-12 col-md-4">
                    <div class="card h-100 border-0 shadow-sm card-hover rounded-3 overflow-hidden">
                        <img src="https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600" class="card-img-top img-cover" alt="Hummus Clásico" style="height: 220px;">
                        <div class="card-body d-flex flex-column p-4">
                            <small class="text-oliva text-uppercase fw-bold tracking-wider mb-1" style="font-size: 0.75rem;">Entradas</small>
                            <h5 class="font-cinzel fw-bold text-carbon mb-2">Hummus Clásico</h5>
                            <p class="text-secondary small mb-4">Crema suave de garbanzos con tahini casero, aceite de oliva virgen y pimentón dulce.</p>
                            <div class="d-flex justify-content-between align-items-center mt-auto border-top pt-3">
                                <span class="fw-bold text-fuego fs-5">$4.500</span>
                                <a href="carrito.php" class="btn btn-fuego btn-sm text-uppercase px-3">Agregar</a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tarjeta 2 -->
                <div class="col-12 col-md-4">
                    <div class="card h-100 border-0 shadow-sm card-hover rounded-3 overflow-hidden">
                        <img src="https://images.pexels.com/photos/6287525/pexels-photo-6287525.jpeg?auto=compress&cs=tinysrgb&w=600" class="card-img-top img-cover" alt="Plato Falafel" style="height: 220px;">
                        <div class="card-body d-flex flex-column p-4">
                            <small class="text-oliva text-uppercase fw-bold tracking-wider mb-1" style="font-size: 0.75rem;">Especiales</small>
                            <h5 class="font-cinzel fw-bold text-carbon mb-2">Plato Falafel</h5>
                            <p class="text-secondary small mb-4">6 croquetas crujientes de garbanzo con hierbas frescas, servidas con ensalada y salsa tahini.</p>
                            <div class="d-flex justify-content-between align-items-center mt-auto border-top pt-3">
                                <span class="fw-bold text-fuego fs-5">$6.200</span>
                                <a href="carrito.php" class="btn btn-fuego btn-sm text-uppercase px-3">Agregar</a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tarjeta 3 -->
                <div class="col-12 col-md-4">
                    <div class="card h-100 border-0 shadow-sm card-hover rounded-3 overflow-hidden">
                        <img src="https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=600" class="card-img-top img-cover" alt="Shawarma Mixto" style="height: 220px;">
                        <div class="card-body d-flex flex-column p-4">
                            <small class="text-oliva text-uppercase fw-bold tracking-wider mb-1" style="font-size: 0.75rem;">Sandwiches</small>
                            <h5 class="font-cinzel fw-bold text-carbon mb-2">Shawarma Mixto</h5>
                            <p class="text-secondary small mb-4">Carne de ternera y pollo sazonada en pan pita recién horneado con vegetales y salsa de ajo.</p>
                            <div class="d-flex justify-content-between align-items-center mt-auto border-top pt-3">
                                <span class="fw-bold text-fuego fs-5">$7.800</span>
                                <a href="carrito.php" class="btn btn-fuego btn-sm text-uppercase px-3">Agregar</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Banner Promocional -->
    <section class="container py-5">
        <div class="card bg-carbon text-white border-0 shadow-lg overflow-hidden rounded-3">
            <div class="row g-0 align-items-center">
                <div class="col-md-5">
                    <img src="https://images.pexels.com/photos/2233729/pexels-photo-2233729.jpeg?auto=compress&cs=tinysrgb&w=700" class="img-cover h-100" style="min-height: 250px;" alt="Promoción de la semana">
                </div>
                <div class="col-md-7 p-4 p-md-5">
                    <span class="badge bg-fuego text-uppercase mb-2 px-3 py-2">Oferta Especial</span>
                    <h3 class="font-cinzel text-sol fw-bold text-uppercase mb-3">Promoción de la Semana</h3>
                    <p class="text-light mb-4">
                        Pide tus **Brochetas Premium** con 20% de descuento al agregar cualquier entrada o bebida natural. ¡Aprovecha la sazón mediterránea en tu hogar!
                    </p>
                    <a href="menu.php" class="btn btn-fuego text-uppercase px-4 py-3 fw-bold">Aprovechar Promo</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <?php include 'footer.php'; ?>