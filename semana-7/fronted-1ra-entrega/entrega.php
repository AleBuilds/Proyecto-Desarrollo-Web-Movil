<?php
$activo = '';
$metodo = isset($_GET['metodo']) ? $_GET['metodo'] : 'delivery';
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Método de entrega — El Mediterráneo</title>
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
            
            /* Estilos específicos para los inputs del formulario */
            .form-control-filled { background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 0; padding: 12px 16px; }
            .form-control-filled:focus { background-color: #fff; border-color: #1A1A1A; box-shadow: none; }
            
            /* Tarjetas de Selección */
            .metodo-card { text-decoration: none; display: block; height: 100%; transition: all 0.2s ease; }
            .metodo-card.activo { border: 2px solid #1A1A1A !important; background-color: #fff !important; color: #1A1A1A !important; }
            .metodo-card.inactivo { border: 1px solid #ced4da; background-color: #f8f9fa; color: #6c757d; }
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
                        <li class="nav-item"><a class="nav-link" href="contacto.php">Contacto</a></li>
                    </ul>
                </div>
                <!-- Ícono de carrito -->
                <div class="d-flex align-items-center">
                    <button type="button" class="btn btn-dark me-2 rounded-0" style="background-color: #1A1A1A;">
                        <i class="fa fa-shopping-bag"></i> 2
                    </button>
                </div>
            </div>
        </nav>

        <!-- Contenido Principal -->
        <main class="container mt-5 mb-5 pt-3 flex-grow-1">
            <h1 class="fw-bold mb-4 text-uppercase">Método de entrega</h1>

            <!-- Opciones de Entrega -->
            <div class="row mb-5">
                <!-- Opción Delivery -->
                <div class="col-12 col-md-6 mb-3 mb-md-0">
                    <a href="entrega.php?metodo=delivery" class="metodo-card p-4 d-flex align-items-center <?php echo $metodo === 'delivery' ? 'activo' : 'inactivo'; ?>">
                        <div class="border bg-white p-2 me-4 d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle>
                            </svg>
                        </div>
                        <div class="flex-grow-1">
                            <h5 class="fw-bold mb-2 text-uppercase">Delivery</h5>
                            <div class="placeholder-line" style="width: 160px; <?php echo $metodo === 'delivery' ? 'background-color: #ccc;' : 'background-color: #e9ecef;'; ?>"></div>
                        </div>
                        <div class="ms-3">
                            <!-- Indicador circular lleno o vacío -->
                            <?php if($metodo === 'delivery'): ?>
                                <svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#1A1A1A"/></svg>
                            <?php else: ?>
                                <svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="#ccc" stroke-width="2"/></svg>
                            <?php endif; ?>
                        </div>
                    </a>
                </div>

                <!-- Opción Retiro -->
                <div class="col-12 col-md-6">
                    <a href="entrega.php?metodo=retiro" class="metodo-card p-4 d-flex align-items-center <?php echo $metodo === 'retiro' ? 'activo' : 'inactivo'; ?>">
                        <div class="border bg-white p-2 me-4 d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M6 2l1.5 5h9L18 2"></path><path d="M3 7h18l-1.5 12a2 2 0 0 1-2 2H6.5a2 2 0 0 1-2-2L3 7z"></path><path d="M9 12v3"></path><path d="M15 12v3"></path>
                            </svg>
                        </div>
                        <div class="flex-grow-1">
                            <h5 class="fw-bold mb-2 text-uppercase">Retiro en local</h5>
                            <div class="placeholder-line" style="width: 160px; <?php echo $metodo === 'retiro' ? 'background-color: #ccc;' : 'background-color: #e9ecef;'; ?>"></div>
                        </div>
                        <div class="ms-3">
                            <!-- Indicador circular lleno o vacío -->
                            <?php if($metodo === 'retiro'): ?>
                                <svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#1A1A1A"/></svg>
                            <?php else: ?>
                                <svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="#ccc" stroke-width="2"/></svg>
                            <?php endif; ?>
                        </div>
                    </a>
                </div>
            </div>

            <!-- Formulario de Despacho / Contacto -->
            <div class="border p-4 p-md-5">
                <h4 class="fw-bold text-uppercase mb-4 pb-2">Datos de despacho / contacto</h4>
                <form action="confirmacion.php" method="post">
                    <div class="row">
                        <!-- Fila 1 -->
                        <div class="col-md-6 mb-4">
                            <label for="nombre" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Nombre completo</label>
                            <input type="text" class="form-control form-control-filled" id="nombre" name="nombre" placeholder="Ej. Juan Pérez">
                        </div>
                        <div class="col-md-6 mb-4">
                            <label for="direccion" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Dirección de entrega</label>
                            <input type="text" class="form-control form-control-filled" id="direccion" name="direccion" placeholder="Ej. Av. Vitacura 1230">
                        </div>
                        <!-- Fila 2 -->
                        <div class="col-md-6 mb-4">
                            <label for="telefono" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Teléfono</label>
                            <input type="tel" class="form-control form-control-filled" id="telefono" name="telefono" placeholder="Ej. +56 9 1234 5678">
                        </div>
                        <div class="col-md-6 mb-4">
                            <label for="email" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Email</label>
                            <input type="email" class="form-control form-control-filled" id="email" name="email" placeholder="Ej. juan.perez@email.com">
                        </div>
                        <!-- Fila 3 -->
                        <div class="col-12 mb-4">
                            <label for="notas" class="form-label text-uppercase fw-bold text-muted" style="font-size: 0.8rem;">Notas / indicaciones</label>
                            <textarea class="form-control form-control-filled" id="notas" name="notas" rows="4" placeholder="Indicaciones para el repartidor o cocina..."></textarea>
                        </div>
                    </div>

                    <!-- Footer del formulario -->
                    <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mt-3 pt-4 border-top">
                        <div class="text-muted d-flex align-items-center mb-4 mb-md-0" style="font-size: 0.9rem;">
                            <svg width="20" height="20" class="me-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                            </svg>
                            Pago 100% seguro y encriptado
                        </div>
                        <button type="submit" class="btn text-white text-uppercase fw-bold rounded-0 px-5 py-2" style="background-color: #1A1A1A; font-size: 0.9rem;">
                            Confirmar pedido y pagar
                        </button>
                    </div>
                </form>
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