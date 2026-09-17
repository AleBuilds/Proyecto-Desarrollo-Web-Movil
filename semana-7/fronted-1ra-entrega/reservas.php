<?php
$activo = 'reservas';

$reserva = [
    'fecha'    => '14 Octubre, 2026',
    'hora'     => '20:30 hrs',
    'personas' => '4 Personas',
    'nombre'   => 'Juan Pérez',
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
        <style>
            /* Paleta de colores base del Wireframe */
            .bg-carbon { background-color: #1A1A1A !important; }
            .bg-crema { background-color: #F3EFE6 !important; }
            .placeholder-line { background-color: #ccc; height: 10px; margin-bottom: 0; border-radius: 4px; }
            
            /* Estilos de inputs */
            .form-control-minimal { border: 1px solid #ced4da; border-radius: 0; padding: 10px 15px; }
            .form-control-minimal:focus { border-color: #1A1A1A; box-shadow: none; }
            
            /* Avatar circular */
            .avatar-circle { width: 80px; height: 80px; border-radius: 50%; background-color: #ffffff; border: 1px solid #ced4da; margin: 0 auto 24px auto; }
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
                        <li class="nav-item"><a class="nav-link active fw-bold" href="reservas.php">Reservas</a></li>
                        <li class="nav-item"><a class="nav-link" href="contacto.php">Contacto</a></li>
                    </ul>
                </div>
                <!-- Ícono de carrito -->
                <div class="d-flex align-items-center">
                    <button type="button" class="btn btn-outline-dark me-2 rounded-0">
                        <i class="fa fa-shopping-bag"></i> 2
                    </button>
                </div>
            </div>
        </nav>

        <!-- Contenido de Reservas -->
        <main class="container mt-5 mb-5 pt-3 flex-grow-1">
            <div class="row">
                <!-- Columna Izquierda: Formulario -->
                <div class="col-12 col-lg-6 pe-lg-5 mb-5 mb-lg-0">
                    <h1 class="fw-bold mb-5 text-uppercase">Reservar Mesa</h1>
                    
                    <form action="reservas.php" method="post">
                        <div class="mb-4">
                            <label for="fecha" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Fecha</label>
                            <input type="date" class="form-control form-control-minimal" id="fecha" name="fecha">
                        </div>
                        <div class="mb-4">
                            <label for="hora" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Hora</label>
                            <input type="time" class="form-control form-control-minimal" id="hora" name="hora">
                        </div>
                        <div class="mb-4">
                            <label for="personas" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Número de personas</label>
                            <input type="number" class="form-control form-control-minimal" id="personas" name="personas" min="1" placeholder="Ej. 4">
                        </div>
                        <div class="mb-4">
                            <label for="nombre" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Nombre</label>
                            <input type="text" class="form-control form-control-minimal" id="nombre" name="nombre" placeholder="Ej. Juan Pérez">
                        </div>
                        <div class="mb-4">
                            <label for="telefono" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Teléfono</label>
                            <input type="tel" class="form-control form-control-minimal" id="telefono" name="telefono" placeholder="Ej. +56 9 1234 5678">
                        </div>
                        <div class="mb-4 pb-2">
                            <label for="email" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Email</label>
                            <input type="email" class="form-control form-control-minimal" id="email" name="email" placeholder="Ej. juan.perez@email.com">
                        </div>
                        
                        <button type="submit" class="btn text-white w-100 rounded-0 text-uppercase fw-bold py-3" style="background-color: #1A1A1A; font-size: 0.9rem;">
                            Reservar
                        </button>
                    </form>
                </div>

                <!-- Columna Derecha: Panel de Confirmación -->
                <div class="col-12 col-lg-6 ps-lg-4 d-flex flex-column mt-5 mt-lg-0">
                    <aside class="bg-crema border p-5 flex-grow-1 d-flex flex-column justify-content-center">
                        <div class="text-center mb-5">
                            <div class="avatar-circle"></div>
                            <h3 class="fw-bold text-uppercase mb-2">Reserva Confirmada</h3>
                            <p class="text-muted mb-0" style="font-size: 0.95rem;">Hemos registrado tu mesa con éxito.</p>
                        </div>
                        
                        <div class="border-top border-secondary pt-4 mb-5">
                            <div class="d-flex justify-content-between mb-3" style="font-size: 0.9rem;">
                                <span class="fw-bold text-muted text-uppercase" style="font-size: 0.8rem;">Fecha:</span>
                                <span class="text-dark"><?php echo $reserva['fecha']; ?></span>
                            </div>
                            <div class="d-flex justify-content-between mb-3" style="font-size: 0.9rem;">
                                <span class="fw-bold text-muted text-uppercase" style="font-size: 0.8rem;">Hora:</span>
                                <span class="text-dark"><?php echo $reserva['hora']; ?></span>
                            </div>
                            <div class="d-flex justify-content-between mb-3" style="font-size: 0.9rem;">
                                <span class="fw-bold text-muted text-uppercase" style="font-size: 0.8rem;">Personas:</span>
                                <span class="text-dark"><?php echo $reserva['personas']; ?></span>
                            </div>
                            <div class="d-flex justify-content-between" style="font-size: 0.9rem;">
                                <span class="fw-bold text-muted text-uppercase" style="font-size: 0.8rem;">A nombre de:</span>
                                <span class="text-dark"><?php echo $reserva['nombre']; ?></span>
                            </div>
                        </div>
                        
                        <a href="index.php" class="btn btn-outline-dark w-100 rounded-0 text-uppercase fw-bold py-3 bg-white mt-auto" style="font-size: 0.9rem;">
                            Volver al inicio
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