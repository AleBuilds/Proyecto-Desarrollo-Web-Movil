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
            Hola Servicios<br>
            <a href="index.php">volver</a>
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
