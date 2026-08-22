<?php

header('Content-Type: application/json; charset=utf-8');

$productos = [
    [
        "id"          => 1,
        "nombre"      => "Chaqueta",
        "descripcion" => "Some example text.",
        "imagen"      => "img/mark-adriane-bO3S03I2Aw8-unsplash.jpg"
    ],
    [
        "id"          => 2,
        "nombre"      => "Polera",
        "descripcion" => "Some example text.",
        "imagen"      => "img/jc-gellidon-4TQJPykwpR0-unsplash.jpg"
    ],
    [
        "id"          => 3,
        "nombre"      => "Set Verano",
        "descripcion" => "Some example text.",
        "imagen"      => "img/mike-von-YsiSAp3ccvk-unsplash.jpg"
    ],
    [
        "id"          => 4,
        "nombre"      => "Lentes",
        "descripcion" => "Some example text.",
        "imagen"      => "img/producto-lentes-sol-street.jpg"
    ],
    [
        "id"          => 5,
        "nombre"      => "Conjunto Blazer",
        "descripcion" => "Some example text.",
        "imagen"      => "img/producto-blazer-negro-premium.jpg"
    ],
    [
        "id"          => 6,
        "nombre"      => "Conjunto Drip",
        "descripcion" => "Some example text.",
        "imagen"      => "img/producto-set-streetwear-oscuro.jpg"
    ],
];

$respuesta = [
    "status"  => 200,
    "message" => "Productos obtenidos",
    "data"    => $productos
];

echo json_encode($respuesta, JSON_UNESCAPED_UNICODE);
