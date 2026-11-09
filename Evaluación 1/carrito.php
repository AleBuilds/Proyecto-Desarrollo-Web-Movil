<?php
$activo = '';
$envio = 2500;
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Tu Carrito — El Mediterráneo</title>
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

    <!-- Contenido del Carrito -->
    <main class="container py-5 flex-grow-1">
        <h1 class="font-cinzel text-carbon fw-bold mb-4 text-uppercase text-center text-md-start">Tu Carrito de Compras</h1>

        <div class="row g-4">
            <!-- Lista de Productos -->
            <div class="col-12 col-lg-8">
                <div id="contenedor-items">
                    <!-- Los items se cargan dinámicamente mediante JavaScript -->
                </div>

                <div class="d-flex justify-content-between align-items-center mt-4">
                    <a href="menu.php" class="btn btn-outline-carbon btn-sm text-uppercase fw-bold"><i class="fa fa-arrow-left me-2"></i> Seguir Comprando</a>
                </div>
            </div>

            <!-- Panel de Resumen -->
            <div class="col-12 col-lg-4">
                <aside class="card border-0 shadow-sm p-4 rounded-3 bg-white">
                    <h4 class="font-cinzel text-tierra fw-bold text-uppercase mb-4 pb-2 border-bottom">Resumen del Pedido</h4>
                    
                    <div class="d-flex justify-content-between mb-3 text-secondary">
                        <span>Subtotal de productos</span>
                        <span class="fw-bold text-carbon" id="subtotal-txt">$0</span>
                    </div>
                    
                    <div class="d-flex justify-content-between mb-4 text-secondary">
                        <span>Envío estimado (Delivery)</span>
                        <span class="fw-bold text-carbon" id="envio-txt">$<?php echo number_format($envio, 0, ',', '.'); ?></span>
                    </div>
                    
                    <div class="d-flex justify-content-between mb-4 pt-3 border-top border-warning">
                        <h5 class="font-cinzel fw-bold text-carbon mb-0">Total</h5>
                        <h5 class="font-cinzel fw-bold text-fuego mb-0" id="total-txt">$0</h5>
                    </div>
                    
                    <a href="entrega.php" id="btn-continuar" class="btn btn-fuego w-100 rounded-3 text-uppercase fw-bold py-3 shadow">
                        Continuar a la Entrega <i class="fa fa-arrow-right ms-2"></i>
                    </a>
                </aside>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <?php include 'footer.php'; ?>

    <script src="carrito.js"></script>
    <script>
        const ENVIO_COST = <?php echo $envio; ?>;

        function clp(valor) {
            return '$' + new Intl.NumberFormat('es-CL').format(valor);
        }

        function renderCarrito() {
            const items = CarritoStorage.obtener();
            const contenedor = document.getElementById('contenedor-items');
            const subtotalTxt = document.getElementById('subtotal-txt');
            const totalTxt = document.getElementById('total-txt');
            const btnContinuar = document.getElementById('btn-continuar');

            if (items.length === 0) {
                contenedor.innerHTML = `
                    <div class="card border-0 shadow-sm p-5 rounded-3 text-center bg-white mb-3">
                        <i class="fa fa-shopping-basket text-muted fs-1 mb-3"></i>
                        <h5 class="font-cinzel text-carbon fw-bold mb-2">Tu carrito está vacío</h5>
                        <p class="text-secondary small mb-4">Aún no has agregado ningún plato de nuestro menú.</p>
                        <div>
                            <a href="menu.php" class="btn btn-fuego rounded-3 text-uppercase fw-bold px-4 py-2">Explorar el Menú</a>
                        </div>
                    </div>
                `;
                subtotalTxt.textContent = clp(0);
                totalTxt.textContent = clp(0);
                btnContinuar.classList.add('disabled');
                return;
            }

            btnContinuar.classList.remove('disabled');
            let subtotal = 0;
            let html = '';

            items.forEach((item, index) => {
                const itemSubtotal = item.precio * item.cantidad;
                subtotal += itemSubtotal;

                html += `
                    <div class="card border-0 shadow-sm mb-3 rounded-3 overflow-hidden p-3 bg-white">
                        <div class="d-flex align-items-center flex-wrap gap-3">
                            <img src="${item.img}" class="rounded-3 img-cover" alt="${item.nombre}" style="width: 85px; height: 85px; object-fit: cover;">
                            
                            <div class="flex-grow-1">
                                <h6 class="font-cinzel fw-bold text-carbon mb-1 fs-6">${item.nombre}</h6>
                                <small class="text-secondary">Precio unitario: <span class="text-fuego fw-bold">${clp(item.precio)}</span></small>
                            </div>
                            
                            <div class="input-group rounded-2" style="width: 105px;">
                                <button class="btn btn-sm btn-outline-secondary font-bold" type="button" onclick="modificarCantidad(${index}, -1)">-</button>
                                <input type="text" class="form-control form-control-sm text-center bg-white fw-bold" value="${item.cantidad}" readonly>
                                <button class="btn btn-sm btn-outline-secondary font-bold" type="button" onclick="modificarCantidad(${index}, 1)">+</button>
                            </div>
                            
                            <div class="fw-bold text-carbon fs-6 text-end px-2" style="min-width: 90px;">
                                ${clp(itemSubtotal)}
                            </div>
                            
                            <button class="btn btn-link text-danger p-1 border-0" type="button" title="Eliminar producto" onclick="eliminarProducto(${index})">
                                <i class="fa fa-trash fs-5"></i>
                            </button>
                        </div>
                    </div>
                `;
            });

            contenedor.innerHTML = html;
            subtotalTxt.textContent = clp(subtotal);
            totalTxt.textContent = clp(subtotal + ENVIO_COST);
        }

        function modificarCantidad(index, delta) {
            CarritoStorage.modificarCantidad(index, delta);
            renderCarrito();
        }

        function eliminarProducto(index) {
            CarritoStorage.eliminar(index);
            renderCarrito();
        }

        document.addEventListener('DOMContentLoaded', renderCarrito);
    </script>
</body>
</html>