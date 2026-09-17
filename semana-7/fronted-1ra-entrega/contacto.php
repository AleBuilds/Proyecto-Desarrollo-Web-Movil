<?php
$activo = 'contacto';

$datosContacto = [
    ['titulo' => 'Dirección', 'valor' => 'Av. del Mar 1042, Barcelona'],
    ['titulo' => 'Teléfono',  'valor' => '+34 93 123 4567'],
    ['titulo' => 'Email',     'valor' => 'hola@elmediterraneo.com'],
    ['titulo' => 'Horarios',  'valor' => 'Lun a Dom: 12:30 - 23:30'],
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
        <style>
            /* Paleta de colores base del Wireframe */
            .bg-carbon { background-color: #1A1A1A !important; }
            .bg-crema { background-color: #F3EFE6 !important; }
            .placeholder-line { background-color: #ccc; height: 10px; margin-bottom: 0; border-radius: 4px; }
            
            /* Inputs del formulario */
            .form-control-minimal { border: 1px solid #ced4da; border-radius: 0; padding: 12px 16px; background-color: #ffffff; }
            .form-control-minimal:focus { border-color: #1A1A1A; box-shadow: none; }
            
            /* Caja de Mapa con cruz simulada */
            .placeholder-box { background-color: #f8f9fa; border: 1px solid #ced4da; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }
            .placeholder-box::before, .placeholder-box::after { content: ''; position: absolute; width: 200%; height: 1px; background-color: #ced4da; top: 50%; left: -50%; }
            .placeholder-box::before { transform: rotate(20deg); }
            .placeholder-box::after { transform: rotate(-20deg); }
            .placeholder-label { background: white; padding: 4px 16px; border: 1px solid #ced4da; z-index: 1; text-transform: uppercase; font-size: 0.8rem; font-weight: bold; color: #6c757d; }
            
            /* Íconos circulares de contacto */
            .icon-circle { width: 56px; height: 56px; border-radius: 50%; background-color: #f8f9fa; border: 1px solid #ced4da; flex-shrink: 0; }
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
                        <li class="nav-item"><a class="nav-link active fw-bold" href="contacto.php">Contacto</a></li>
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

        <!-- Contenido Principal -->
        <main class="container mt-5 mb-5 pt-3 flex-grow-1">
            <div class="row">
                
                <!-- Columna Izquierda: Ubicación y Formulario -->
                <div class="col-12 col-lg-8 pe-lg-5 mb-5 mb-lg-0">
                    
                    <!-- Bloque Mapa -->
                    <h2 class="fw-bold text-uppercase mb-4" style="font-size: 1.25rem;">Ubicación</h2>
                    <div class="placeholder-box w-100 mb-5" style="height: 350px;">
                        <span class="placeholder-label">Mapa</span>
                    </div>

                    <!-- Bloque Formulario -->
                    <div class="bg-crema border p-4 p-md-5">
                        <h4 class="fw-bold text-uppercase mb-4 pb-2">Deja tu mensaje</h4>
                        
                        <form action="contacto.php" method="post">
                            <div class="mb-4">
                                <label for="nombre" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Nombre</label>
                                <input type="text" class="form-control form-control-minimal" id="nombre" name="nombre">
                            </div>
                            <div class="mb-4">
                                <label for="email" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Email</label>
                                <input type="email" class="form-control form-control-minimal" id="email" name="email">
                            </div>
                            <div class="mb-4">
                                <label for="mensaje" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Mensaje</label>
                                <textarea class="form-control form-control-minimal" id="mensaje" name="mensaje" rows="4"></textarea>
                            </div>
                            <button type="submit" class="btn text-white text-uppercase fw-bold rounded-0 px-5 py-2 mt-2" style="background-color: #1A1A1A; font-size: 0.9rem;">
                                Enviar
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Columna Derecha: Datos de Contacto -->
                <div class="col-12 col-lg-4">
                    <h2 class="fw-bold text-uppercase mb-4" style="font-size: 1.25rem;">Datos de contacto</h2>
                    
                    <div class="d-flex flex-column gap-4 pt-2">
                        <?php foreach ($datosContacto as $dato): ?>
                            <div class="d-flex align-items-center">
                                <!-- Ícono circular placeholder -->
                                <div class="icon-circle me-4"></div>
                                
                                <!-- Textos -->
                                <div>
                                    <h6 class="fw-bold text-uppercase mb-1" style="font-size: 0.85rem; color: #333;"><?php echo $dato['titulo']; ?></h6>
                                    <p class="text-muted mb-0" style="font-size: 0.9rem;"><?php echo $dato['valor']; ?></p>
                                </div>
                            </div>
                        <?php endforeach; ?>
                    </div>
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