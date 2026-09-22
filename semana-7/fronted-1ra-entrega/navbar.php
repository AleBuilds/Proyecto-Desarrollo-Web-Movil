<?php
// $activo debe definirse en la página que incluye este archivo, ej: $activo = 'inicio';
if (!isset($activo)) { $activo = ''; }
$enlaces = [
    'inicio'   => ['label' => 'Inicio',    'href' => 'index.php'],
    'menu'     => ['label' => 'Menú',      'href' => 'menu.php'],
    'nosotros' => ['label' => 'Nosotros',  'href' => 'nosotros.php'],
    'reservas' => ['label' => 'Reservas',  'href' => 'reservas.php'],
    'contacto' => ['label' => 'Contacto',  'href' => 'contacto.php'],
];
?>
<nav class="navbar navbar-expand-lg bg-carbon navbar-dark sticky-top shadow-sm py-3">
    <div class="container">
        <a class="navbar-brand font-cinzel fw-bold fs-4 text-uppercase tracking-wide" href="index.php" style="color: var(--sol);">
            <i class="fa fa-cutlery me-2 text-fuego"></i>EL MEDITERRÁNEO
        </a>
        <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar" aria-label="Abrir navegación">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-center" id="collapsibleNavbar">
            <ul class="navbar-nav gap-lg-3">
                <?php foreach ($enlaces as $clave => $enlace): ?>
                    <li class="nav-item">
                        <a class="nav-link text-uppercase fw-semibold px-3 <?php echo $activo === $clave ? 'active text-sol border-bottom border-2 border-warning' : 'text-light'; ?>" href="<?php echo $enlace['href']; ?>">
                            <?php echo $enlace['label']; ?>
                        </a>
                    </li>
                <?php endforeach; ?>
            </ul>
        </div>
        <!-- Botón interactivo al carrito -->
        <div class="d-flex align-items-center">
            <a href="carrito.php" class="btn btn-fuego rounded-pill px-4 py-2 d-flex align-items-center gap-2 shadow-sm text-decoration-none">
                <i class="fa fa-shopping-cart"></i>
                <span class="d-none d-sm-inline">Carrito</span>
                <span class="badge badge-fuego carrito-badge rounded-circle bg-white text-fuego px-2 py-1 fs-7">0</span>
            </a>
        </div>
    </div>
</nav>
<script src="carrito.js"></script>
