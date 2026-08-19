<!DOCTYPE html>
<html lang="es">
    <head>
        <title>primera pagina</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <body>
        <!--navbar-->
        <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="index.php"><i class="fa fa-star-half-o" style="font-size:48px;color:white"></i></a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="collapsibleNavbar">
                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="marcaderopa.php" role="button" data-bs-toggle="dropdown">Prendas</a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="marcaderopa.php">Poleras</a></li>
                            <li><a class="dropdown-item" href="marcaderopa.php">Polerones</a></li>
                            <li><a class="dropdown-item" href="marcaderopa.php">Pantalones</a></li>
                            <li><a class="dropdown-item" href="marcaderopa.php">Buzos</a></li>
                            <li><a class="dropdown-item" href="productos.php">Accesorios</a></li>
                        </ul>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="productos.php">Productos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="servicios.php">Servicios</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="contacto.php">Contacto</a>
                        </li>  
                    </ul>
                </div>
            </div>
        </nav>
        <!--container-->
        <div class="container-fluid bg-dark text-white p-3">
            Hola Ropa<br>
            <a href="index.php">volver</a>
        </div>
            <!-- Carousel -->
            <div class="container-fluid bg-dark text-white p-3">
            <div id="demo" class="carousel slide" data-bs-ride="carousel">

                <!-- Indicators/dots -->
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="1"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="2"></button>
                </div>

                <!-- The slideshow/carousel -->
                <div class="carousel-inner">
                    <div class="carousel-item active">
                    <img src="img/chico_poleron_blanco.jpg" alt="chico_poleron_blanco" class="d-block w-100">
                    </div>
                    <div class="carousel-item">
                    <img src="img/chica_afro.jpg" alt="chica_afro" class="d-block w-100">
                    </div>
                    <div class="carousel-item">
                    <img src="img/chica _con_bandana.jpg" alt="chica _con_bandana" class="d-block w-100">
                    </div>
                </div>

                <!-- Left and right controls/icons -->
                <button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
                </div>
            </div>
        </div>
        <!--footer-->
        <div class="container-fluid bg-dark">
            <div class="row">
                <div class="col-4"></div>
                <div class="col-4" style="color:white"><strong>MiMarcaDeRopa@2026</strong></div>
                <div class="col-4"></div>
            </div>
        </div>
        <!--modal-->
    </body>
</html>
