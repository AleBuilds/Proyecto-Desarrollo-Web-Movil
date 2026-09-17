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
<nav class="navbar" aria-label="Navegación principal">
  <div class="container">
    <a class="navbar-brand" href="index.php">
      <span class="navbar-logo" aria-hidden="true"></span>
      EL MEDITERRÁNEO
    </a>
    <button class="navbar-toggle" type="button" aria-label="Abrir menú de navegación" aria-expanded="false">
      <span></span>
    </button>
    <ul class="navbar-links">
      <?php foreach ($enlaces as $clave => $enlace): ?>
        <li>
          <a href="<?php echo $enlace['href']; ?>"<?php echo $activo === $clave ? ' aria-current="page"' : ''; ?>>
            <?php echo $enlace['label']; ?>
          </a>
        </li>
      <?php endforeach; ?>
    </ul>
    <a class="navbar-cart" href="carrito.php" aria-label="Ver carrito, 2 productos">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
      <span class="navbar-cart-badge" aria-hidden="true">2</span>
    </a>
  </div>
</nav>
