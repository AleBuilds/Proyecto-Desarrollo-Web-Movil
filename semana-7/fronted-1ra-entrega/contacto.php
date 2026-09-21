<?php
$activo = 'contacto';

$datosContacto = [
    ['titulo' => 'Dirección', 'valor' => 'Av. Pajaritos 2100, Maipú, Santiago', 'icon' => 'fa-map-marker'],
    ['titulo' => 'Teléfono',  'valor' => '+56 9 8765 4321',                    'icon' => 'fa-phone'],
    ['titulo' => 'Email',     'valor' => 'contacto@elmediterraneo.cl',        'icon' => 'fa-envelope'],
    ['titulo' => 'Horarios',  'valor' => 'Lun a Dom: 12:30 - 23:30',          'icon' => 'fa-clock-o'],
];
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Contacto — El Mediterráneo</title>
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
        <div class="row g-5">
            <!-- Ubicación y Formulario -->
            <div class="col-12 col-lg-8">
                <!-- Bloque Mapa con imagen realista -->
                <h2 class="font-cinzel text-carbon fw-bold text-uppercase mb-3 fs-3">Ubicación</h2>
                <div class="rounded-3 overflow-hidden shadow-sm mb-5 position-relative" style="height: 320px;">
                    <img src="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=1000&q=80" class="img-cover w-100 h-100" alt="Mapa Ubicación">
                    <div class="position-absolute top-50 start-50 translate-middle bg-carbon text-sol px-4 py-2 rounded-3 shadow border border-warning fw-bold text-uppercase font-cinzel">
                        <i class="fa fa-map-marker text-fuego me-2"></i> El Mediterráneo - Maipú
                    </div>
                </div>

                <!-- Formulario -->
                <div class="card border-0 shadow-sm p-4 p-md-5 rounded-3 bg-white">
                    <h4 class="font-cinzel text-tierra fw-bold text-uppercase mb-4 pb-2 border-bottom">Deja tu mensaje</h4>
                    
                    <form action="contacto.php" method="post">
                        <div class="mb-3">
                            <label for="nombre" class="form-label text-uppercase fw-bold small text-tierra">Nombre Completo</label>
                            <input type="text" class="form-control form-control-med" id="nombre" name="nombre" placeholder="Ej. Alejandro Pérez" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label text-uppercase fw-bold small text-tierra">Email de Contacto</label>
                            <input type="email" class="form-control form-control-med" id="email" name="email" placeholder="Ej. alejandro@email.com" required>
                        </div>
                        <div class="mb-4">
                            <label for="mensaje" class="form-label text-uppercase fw-bold small text-tierra">Mensaje</label>
                            <textarea class="form-control form-control-med" id="mensaje" name="mensaje" rows="4" placeholder="Escribe tu consulta o sugerencia..." required></textarea>
                        </div>
                        <button type="submit" class="btn btn-fuego text-uppercase fw-bold px-5 py-3 shadow rounded-3">
                            Enviar Mensaje <i class="fa fa-paper-plane ms-2"></i>
                        </button>
                    </form>
                </div>
            </div>

            <!-- Datos de Contacto -->
            <div class="col-12 col-lg-4">
                <h2 class="font-cinzel text-carbon fw-bold text-uppercase mb-4 fs-3">Información</h2>
                
                <div class="d-flex flex-column gap-3">
                    <?php foreach ($datosContacto as $dato): ?>
                        <div class="card border-0 shadow-sm p-3 rounded-3 bg-white d-flex flex-row align-items-center gap-3">
                            <div class="bg-carbon text-sol rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 50px; height: 50px;">
                                <i class="fa <?php echo $dato['icon']; ?> fs-5"></i>
                            </div>
                            <div>
                                <h6 class="font-cinzel fw-bold text-carbon text-uppercase mb-1 fs-6"><?php echo $dato['titulo']; ?></h6>
                                <p class="text-secondary small mb-0"><?php echo $dato['valor']; ?></p>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>