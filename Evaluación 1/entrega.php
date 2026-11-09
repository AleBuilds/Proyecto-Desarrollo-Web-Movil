<?php
$activo = '';
$metodo = isset($_GET['metodo']) ? $_GET['metodo'] : 'delivery';
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Método de Entrega — El Mediterráneo</title>
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
        <h1 class="font-cinzel text-carbon fw-bold mb-4 text-uppercase text-center text-md-start">Método de Entrega</h1>

        <!-- Opciones de Entrega -->
        <div class="row g-4 mb-4">
            <!-- Opción Delivery -->
            <div class="col-12 col-md-6">
                <a href="entrega.php?metodo=delivery" class="card border-2 p-4 text-decoration-none h-100 shadow-sm rounded-3 d-flex flex-row align-items-center justify-content-between <?php echo $metodo === 'delivery' ? 'border-danger bg-white' : 'border-secondary bg-light text-muted'; ?>">
                    <div class="d-flex align-items-center gap-3">
                        <div class="rounded-circle p-3 <?php echo $metodo === 'delivery' ? 'bg-fuego text-white' : 'bg-secondary text-white'; ?>">
                            <i class="fa fa-motorcycle fs-3"></i>
                        </div>
                        <div>
                            <h5 class="font-cinzel fw-bold mb-1 text-carbon text-uppercase">Delivery a Domicilio</h5>
                            <small class="text-secondary">Recibe tu pedido fresco en 30-45 min.</small>
                        </div>
                    </div>
                    <i class="fa <?php echo $metodo === 'delivery' ? 'fa-check-circle text-fuego fs-3' : 'fa-circle-o text-muted fs-3'; ?>"></i>
                </a>
            </div>

            <!-- Opción Retiro -->
            <div class="col-12 col-md-6">
                <a href="entrega.php?metodo=retiro" class="card border-2 p-4 text-decoration-none h-100 shadow-sm rounded-3 d-flex flex-row align-items-center justify-content-between <?php echo $metodo === 'retiro' ? 'border-danger bg-white' : 'border-secondary bg-light text-muted'; ?>">
                    <div class="d-flex align-items-center gap-3">
                        <div class="rounded-circle p-3 <?php echo $metodo === 'retiro' ? 'bg-fuego text-white' : 'bg-secondary text-white'; ?>">
                            <i class="fa fa-shopping-bag fs-3"></i>
                        </div>
                        <div>
                            <h5 class="font-cinzel fw-bold mb-1 text-carbon text-uppercase">Retiro en Local</h5>
                            <small class="text-secondary">Pasa a buscar tu pedido sin costo de envío.</small>
                        </div>
                    </div>
                    <i class="fa <?php echo $metodo === 'retiro' ? 'fa-check-circle text-fuego fs-3' : 'fa-circle-o text-muted fs-3'; ?>"></i>
                </a>
            </div>
        </div>

        <!-- Formulario de Despacho / Contacto -->
        <div class="card border-0 shadow-sm p-4 p-md-5 rounded-3 bg-white">
            <h4 class="font-cinzel text-tierra fw-bold text-uppercase mb-4 pb-2 border-bottom">Datos de Despacho y Contacto</h4>
            <form action="confirmacion.php" method="post">
                <div class="row g-4">
                    <div class="col-md-6">
                        <label for="nombre" class="form-label text-uppercase fw-bold small text-tierra">Nombre completo</label>
                        <input type="text" class="form-control form-control-med" id="nombre" name="nombre" placeholder="Ej. Alejandro Pérez" required>
                    </div>
                    <div class="col-md-6">
                        <label for="direccion" class="form-label text-uppercase fw-bold small text-tierra">Dirección de entrega</label>
                        <input type="text" class="form-control form-control-med" id="direccion" name="direccion" placeholder="Ej. Av. Pajaritos 1230, Maipú" required>
                    </div>
                    <div class="col-md-6">
                        <label for="telefono" class="form-label text-uppercase fw-bold small text-tierra">Teléfono de contacto</label>
                        <input type="tel" class="form-control form-control-med" id="telefono" name="telefono" placeholder="Ej. +56 9 1234 5678" required>
                    </div>
                    <div class="col-md-6">
                        <label for="email" class="form-label text-uppercase fw-bold small text-tierra">Email</label>
                        <input type="email" class="form-control form-control-med" id="email" name="email" placeholder="Ej. alejandro@email.com" required>
                    </div>
                    <div class="col-12">
                        <label for="notas" class="form-label text-uppercase fw-bold small text-tierra">Notas e Indicaciones</label>
                        <textarea class="form-control form-control-med" id="notas" name="notas" rows="3" placeholder="Ej. Tocar el timbre de la izquierda o sin salsa picante..."></textarea>
                    </div>
                </div>

                <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mt-5 pt-4 border-top">
                    <div class="text-secondary d-flex align-items-center mb-3 mb-md-0 small">
                        <i class="fa fa-lock text-oliva fs-5 me-2"></i> Pago 100% seguro y encriptado
                    </div>
                    <button type="submit" class="btn btn-fuego text-uppercase fw-bold px-5 py-3 shadow rounded-3">
                        Confirmar Pedido y Pagar <i class="fa fa-check-circle ms-2"></i>
                    </button>
                </div>
            </form>
        </div>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>