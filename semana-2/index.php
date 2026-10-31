<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Primera pagina</title>
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
                        <li class="nav-item">
                            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">Acceder</button> 
                        </li> 
            </div>
        </nav>
        <!--container-->
        <div class="container-fluid bg-dark text-white p-3">
            <a href="marcaderopa.php">ir a marca ropa</a><br>
            <a href="productos.php">ir a productos</a><br>
            <a href="servicios.php">ir a servicios</a><br>
            <a href="contacto.php">ir a contacto</a><br>
        </div>
<div class="container bg-dark text-white ">
        <!-- Carousel -->
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
        <!--footer-->
        <div class="container-fluid bg-dark">
            <div class="row">
                <div class="col-4"></div>
                <div class="col-4" style="color:white"><strong>MiMarcaDeRopa@2026</strong></div>
                <div class="col-4"></div>
            </div>
        </div>
        <!--modal-->
            <div class="modal fade" id="myModal">
                <div class="modal-dialog">
                    <div class="modal-content">
                    <!-- Modal Header -->
                    <div class="modal-header">
                        <h4 class="modal-title">Autenticación</h4>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <!-- Modal body -->
                    <div class="modal-body">
                        <form action="marcaderopa.php">
                        <div class="mb-3 mt-3">
                            <label for="email" class="form-label">Email:</label>
                            <input type="email" class="form-control" id="email" placeholder="Enter email" name="email">
                        </div>
                        <div class="mb-3">
                            <label for="pwd" class="form-label">Password:</label>
                            <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="pswd">
                        </div>
                        <div class="form-check mb-3">
                            <label class="form-check-label">
                            <input class="form-check-input" type="checkbox" name="remember"> Remember me
                            </label>
                        </div>
                        <button type="submit" class="btn btn-primary">Login</button>
                        </form>
                    </div>
                    <!-- Modal footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Close</button>
                    </div>
                    </div>
                </div>
                
            </div>
    </body>
</html>
