<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Inicio — El Mediterráneo</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <style>
            /* Paleta de colores base del Wireframe */
            .bg-carbon { background-color: #1A1A1A !important; }
            .bg-crema { background-color: #F3EFE6 !important; }
            .placeholder-line { background-color: #ccc; height: 12px; margin-bottom: 8px; border-radius: 4px; }
            .placeholder-box { background-color: #e9ecef; border: 1px solid #ced4da; display: flex; align-items: center; justify-content: center; color: #6c757d; }
        </style>
    </head>
    <body class="bg-white">
        <!-- Navbar -->
        <nav class="navbar navbar-expand-sm bg-white navbar-light border-bottom sticky-top">
            <div class="container">
                <a class="navbar-brand fw-bold" href="index.php">EL MEDITERRÁNEO</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-center" id="collapsibleNavbar">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" href="index.php">Inicio</a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="menu.php" role="button" data-bs-toggle="dropdown">Menú</a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="#">Todos</a></li>
                                <li><a class="dropdown-item" href="#">Hummus</a></li>
                                <li><a class="dropdown-item" href="#">Falafel</a></li>
                                <li><a class="dropdown-item" href="#">Shawarma</a></li>
                                <li><a class="dropdown-item" href="#">Parrilla</a></li>
                            </ul>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="nosotros.php">Nosotros</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="reservas.php">Reservas</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="contacto.php">Contacto</a>
                        </li>
                    </ul>
                </div>
                <!-- Ícono de carrito / Acceder modal -->
                <div class="d-flex align-items-center">
                    <button type="button" class="btn btn-outline-dark me-2" data-bs-toggle="modal" data-bs-target="#myModal">
                        <i class="fa fa-shopping-bag"></i> 2
                    </button>
                </div>
            </div>
        </nav>

        <!-- Sección 1: Hero (Reemplaza al carrusel) -->
        <div class="container-fluid bg-crema py-5 text-center d-flex flex-column justify-content-center align-items-center" style="min-height: 400px;">
            <div class="bg-white p-5 border shadow-sm w-75">
                <h1 class="display-4 fw-bold text-uppercase">Título Principal</h1>
                <div class="mx-auto mt-4" style="width: 50%;">
                    <div class="placeholder-line" style="width: 100%;"></div>
                    <div class="placeholder-line" style="width: 70%; margin: 0 auto;"></div>
                </div>
                <div class="mt-4">
                    <a href="menu.php" class="btn btn-dark btn-lg text-uppercase me-2" style="background-color: #1A1A1A;">Ver Menú</a>
                    <a href="reservas.php" class="btn btn-outline-dark btn-lg text-uppercase">Reservar</a>
                </div>
            </div>
        </div>

        <!-- Sección 2: Nuestras Especialidades (Proporción 4 columnas) -->
        <div class="container mt-5 pt-4">
            <h3 class="fw-bold mb-4 text-uppercase">Nuestras Especialidades</h3>
            <div class="row text-center">
                <div class="col-12 col-sm-6 col-md-3 mb-4">
                    <div class="placeholder-box mb-3" style="height: 180px;">
                        <span class="border bg-white px-2 py-1">X</span>
                    </div>
                    <h5 class="fw-bold text-uppercase">Hummus</h5>
                </div>
                <div class="col-12 col-sm-6 col-md-3 mb-4">
                    <div class="placeholder-box mb-3" style="height: 180px;">
                        <span class="border bg-white px-2 py-1">X</span>
                    </div>
                    <h5 class="fw-bold text-uppercase">Falafel</h5>
                </div>
                <div class="col-12 col-sm-6 col-md-3 mb-4">
                    <div class="placeholder-box mb-3" style="height: 180px;">
                        <span class="border bg-white px-2 py-1">X</span>
                    </div>
                    <h5 class="fw-bold text-uppercase">Shawarma</h5>
                </div>
                <div class="col-12 col-sm-6 col-md-3 mb-4">
                    <div class="placeholder-box mb-3" style="height: 180px;">
                        <span class="border bg-white px-2 py-1">X</span>
                    </div>
                    <h5 class="fw-bold text-uppercase">Parrilla</h5>
                </div>
            </div>
        </div>

        <!-- Sección 3: Productos Destacados (Proporción 3 columnas) -->
        <div class="container mt-5">
            <h3 class="fw-bold mb-4 text-uppercase">Productos Destacados</h3>
            <div class="row">
                <!-- Tarjeta 1 -->
                <div class="col-12 col-md-4 mb-4">
                    <div class="card border-0">
                        <div class="placeholder-box" style="height: 220px;">IMAGEN PRODUCTO</div>
                        <div class="card-body px-0">
                            <small class="text-muted text-uppercase fw-bold" style="font-size: 0.75rem;">Entradas</small>
                            <h5 class="card-title fw-bold">Hummus Clásico</h5>
                            <div class="placeholder-line" style="width: 100%;"></div>
                            <div class="placeholder-line" style="width: 60%;"></div>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <h5 class="mb-0 fw-bold">$4.500</h5>
                                <button class="btn btn-outline-dark text-uppercase rounded-0 px-4">Agregar</button>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Tarjeta 2 -->
                <div class="col-12 col-md-4 mb-4">
                    <div class="card border-0">
                        <div class="placeholder-box" style="height: 220px;">IMAGEN PRODUCTO</div>
                        <div class="card-body px-0">
                            <small class="text-muted text-uppercase fw-bold" style="font-size: 0.75rem;">Especiales</small>
                            <h5 class="card-title fw-bold">Plato Falafel</h5>
                            <div class="placeholder-line" style="width: 100%;"></div>
                            <div class="placeholder-line" style="width: 60%;"></div>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <h5 class="mb-0 fw-bold">$6.200</h5>
                                <button class="btn btn-outline-dark text-uppercase rounded-0 px-4">Agregar</button>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Tarjeta 3 -->
                <div class="col-12 col-md-4 mb-4">
                    <div class="card border-0">
                        <div class="placeholder-box" style="height: 220px;">IMAGEN PRODUCTO</div>
                        <div class="card-body px-0">
                            <small class="text-muted text-uppercase fw-bold" style="font-size: 0.75rem;">Sandwiches</small>
                            <h5 class="card-title fw-bold">Shawarma Mixto</h5>
                            <div class="placeholder-line" style="width: 100%;"></div>
                            <div class="placeholder-line" style="width: 60%;"></div>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <h5 class="mb-0 fw-bold">$7.800</h5>
                                <button class="btn btn-outline-dark text-uppercase rounded-0 px-4">Agregar</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sección 4: Promoción de la Semana (Banner horizontal) -->
        <div class="container mt-4 mb-5 pb-4">
            <div class="row bg-crema align-items-center border p-4 mx-0">
                <div class="col-md-3 text-center mb-3 mb-md-0">
                    <div class="placeholder-box bg-white mx-auto" style="height: 120px; width: 100%;">
                        <span class="border px-2 py-1 bg-white" style="font-size: 0.8rem;">PROMO BANNER</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <h4 class="fw-bold text-uppercase">Promoción de la Semana</h4>
                    <div class="placeholder-line" style="width: 90%;"></div>
                    <div class="placeholder-line" style="width: 50%;"></div>
                </div>
                <div class="col-md-3 text-md-end text-center mt-3 mt-md-0">
                    <a href="menu.php" class="btn btn-dark text-uppercase px-4" style="background-color: #1A1A1A;">Aprovechar</a>
                </div>
            </div>
        </div>

        <!-- Footer (Fondo oscuro, 3 columnas) -->
        <footer class="container-fluid bg-carbon text-white pt-5 pb-3">
            <div class="container">
                <div class="row mb-4">
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">El Mediterráneo</h6>
                        <div class="placeholder-line bg-secondary" style="width: 60%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 40%;"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">Horarios</h6>
                        <div class="placeholder-line bg-secondary" style="width: 50%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 30%;"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <h6 class="fw-bold text-uppercase mb-3">Contacto</h6>
                        <div class="placeholder-line bg-secondary" style="width: 70%;"></div>
                        <div class="placeholder-line bg-secondary" style="width: 50%;"></div>
                    </div>
                </div>
                <div class="row border-top border-secondary pt-3">
                    <div class="col-12 text-start" style="font-size: 0.8rem; color: #888;">
                        © 2026 El Mediterráneo. Todos los derechos reservados. Wireframe Layout.
                    </div>
                </div>
            </div>
        </footer>

        <!-- Modal (Sin alterar su funcionalidad, pero estilizado) -->
        <div class="modal fade" id="myModal">
            <div class="modal-dialog">
                <div class="modal-content rounded-0">
                    <!-- Modal Header -->
                    <div class="modal-header">
                        <h4 class="modal-title fw-bold">Acceso Clientes</h4>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <!-- Modal body -->
                    <div class="modal-body">
                        <form action="menu.php">
                            <div class="mb-3 mt-3">
                                <label for="email" class="form-label text-uppercase fw-bold" style="font-size: 0.8rem;">Email:</label>
                                <input type="email" class="form-control rounded-0" id="email" placeholder="Ingresa tu email" name="email">
                            </div>
                            <div class="mb-3">
                                <label for="pwd" class="form-label text-uppercase fw-bold" style="font-size: 0.8rem;">Contraseña:</label>
                                <input type="password" class="form-control rounded-0" id="pwd" placeholder="Ingresa tu contraseña" name="pswd">
                            </div>
                            <div class="form-check mb-3">
                                <label class="form-check-label">
                                    <input class="form-check-input" type="checkbox" name="remember"> Recordarme
                                </label>
                            </div>
                            <button type="submit" class="btn btn-dark w-100 rounded-0" style="background-color: #1A1A1A;">LOGIN</button>
                        </form>
                    </div>
                    <!-- Modal footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger rounded-0" data-bs-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>