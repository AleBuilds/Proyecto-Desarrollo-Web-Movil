<?php
$activo = 'reservas';

$reserva = [
    'fecha'    => '14 Octubre, 2026',
    'hora'     => '20:30 hrs',
    'personas' => '4 Personas',
    'nombre'   => 'Alejandro Pérez',
];
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Reservas — El Mediterráneo</title>
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

    <!-- Contenido de Reservas -->
    <main class="container py-5 flex-grow-1">
        <div class="row g-5">
            <!-- Formulario -->
            <div class="col-12 col-lg-6">
                <h1 class="font-cinzel text-carbon fw-bold mb-4 text-uppercase">Reservar Mesa</h1>
                
                <form action="reservas.php" method="post" class="card border-0 shadow-sm p-4 p-md-5 rounded-3 bg-white">
                    <div class="mb-3">
                        <label for="fecha" class="form-label text-uppercase fw-bold small text-tierra">Fecha de la Reserva</label>
                        <input type="date" class="form-control form-control-med" id="fecha" name="fecha" required>
                    </div>
                    <div class="mb-3">
                        <label for="hora" class="form-label text-uppercase fw-bold small text-tierra">Hora</label>
                        <input type="time" class="form-control form-control-med" id="hora" name="hora" required>
                    </div>
                    <div class="mb-3">
                        <label for="personas" class="form-label text-uppercase fw-bold small text-tierra">Número de Personas</label>
                        <input type="number" class="form-control form-control-med" id="personas" name="personas" min="1" placeholder="Ej. 4" required>
                    </div>
                    <div class="mb-3">
                        <label for="nombre" class="form-label text-uppercase fw-bold small text-tierra">Nombre</label>
                        <input type="text" class="form-control form-control-med" id="nombre" name="nombre" placeholder="Ej. Alejandro Pérez" required>
                    </div>
                    <div class="mb-3">
                        <label for="telefono" class="form-label text-uppercase fw-bold small text-tierra">Teléfono</label>
                        <input type="tel" class="form-control form-control-med" id="telefono" name="telefono" placeholder="Ej. +56 9 1234 5678" required>
                    </div>
                    <div class="mb-4">
                        <label for="email" class="form-label text-uppercase fw-bold small text-tierra">Email</label>
                        <input type="email" class="form-control form-control-med" id="email" name="email" placeholder="Ej. alejandro@email.com" required>
                    </div>
                    
                    <button type="submit" class="btn btn-fuego w-100 rounded-3 text-uppercase fw-bold py-3 shadow">
                        Confirmar Reserva <i class="fa fa-calendar-check-o ms-2"></i>
                    </button>
                </form>
            </div>

            <!-- Panel de Ejemplo de Confirmación -->
            <div class="col-12 col-lg-6 d-flex flex-column">
                <aside class="card border-0 shadow-sm p-4 p-md-5 rounded-3 bg-white h-100 d-flex flex-column justify-content-center text-center">
                    <div class="mb-4">
                        <div class="bg-oliva text-white rounded-circle d-inline-flex align-items-center justify-content-center shadow-sm mb-3" style="width: 80px; height: 80px;">
                            <i class="fa fa-cutlery fs-2"></i>
                        </div>
                        <h3 class="font-cinzel text-carbon fw-bold text-uppercase mb-2">Reserva Confirmada</h3>
                        <p class="text-secondary small">Tu mesa estará lista esperándote.</p>
                    </div>
                    
                    <div class="border-top border-bottom border-warning py-4 my-3 text-start">
                        <div class="d-flex justify-content-between mb-2">
                            <span class="fw-bold text-tierra text-uppercase small">Fecha:</span>
                            <span class="text-carbon fw-bold"><?php echo $reserva['fecha']; ?></span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="fw-bold text-tierra text-uppercase small">Hora:</span>
                            <span class="text-carbon fw-bold"><?php echo $reserva['hora']; ?></span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="fw-bold text-tierra text-uppercase small">Personas:</span>
                            <span class="text-carbon fw-bold"><?php echo $reserva['personas']; ?></span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span class="fw-bold text-tierra text-uppercase small">A nombre de:</span>
                            <span class="text-carbon fw-bold"><?php echo $reserva['nombre']; ?></span>
                        </div>
                    </div>
                    
                    <a href="index.php" class="btn btn-outline-carbon w-100 rounded-3 text-uppercase fw-bold py-3 mt-auto">
                        Volver al Inicio
                    </a>
                </aside>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>