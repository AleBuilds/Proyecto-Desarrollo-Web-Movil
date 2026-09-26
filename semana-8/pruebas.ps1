$GW      = "http://127.0.0.1:8000"
$BACK    = "http://127.0.0.1:9000"
$TOKEN   = if ($env:CLIENT_TOKEN)   { $env:CLIENT_TOKEN }   else { "student-token-123" }
$SECRET  = if ($env:BACKEND_SECRET) { $env:BACKEND_SECRET } else { "gateway-api-secret-456" }
$pedido  = '{"nombre":"Juan Perez","telefono":"+56912345678","email":"juan@correo.cl","metodo_entrega":"delivery","direccion":"Av. Pajaritos 1234","items":[{"producto_id":3,"cantidad":2},{"producto_id":6,"cantidad":1}]}'

# PowerShell 5.1 pierde las comillas al pasar JSON a curl.exe, por eso se envía desde un archivo.
$pedidoArchivo = Join-Path $env:TEMP "pedido-prueba.json"
[IO.File]::WriteAllText($pedidoArchivo, $pedido)

$script:fallos = 0
function Probar($nombre, $esperado, [string[]]$curlArgs) {
    $codigo = & curl.exe -s -o NUL -w "%{http_code}" @curlArgs
    $ok = ($codigo -eq "$esperado")
    if (-not $ok) { $script:fallos++ }
    "{0,-6} {1,-58} esperado {2}  obtenido {3}" -f $(if ($ok) {"OK"} else {"FALLA"}), $nombre, $esperado, $codigo
}

Probar "Gateway sin token"                              401 @("$GW/api/productos")
Probar "Gateway con token falso"                        401 @("-H", "Authorization: Bearer token-falso", "$GW/api/productos")
Probar "Backend directo sin secreto"                    403 @("$BACK/productos")
Probar "Backend directo con secreto incorrecto"         403 @("-H", "X-Gateway-Secret: incorrecto", "$BACK/productos")
Probar "Gateway con token valido -> GET /productos"     200 @("-H", "Authorization: Bearer $TOKEN", "$GW/api/productos")
Probar "Gateway con token valido -> filtro categoria"   200 @("-H", "Authorization: Bearer $TOKEN", "$GW/api/productos?categoria=Hummus")
Probar "Gateway con token valido -> producto inexistente" 404 @("-H", "Authorization: Bearer $TOKEN", "$GW/api/productos/999")
Probar "Gateway con token valido -> POST /pedidos"      201 @("-X", "POST", "-H", "Authorization: Bearer $TOKEN", "-H", "Content-Type: application/json", "--data-binary", "@$pedidoArchivo", "$GW/api/pedidos")
Probar "Gateway: ruta con .. rechazada"                 400 @("--path-as-is", "-H", "Authorization: Bearer $TOKEN", "$GW/api/../health")
Probar "Backend directo con secreto correcto (solo prueba)" 200 @("-H", "X-Gateway-Secret: $SECRET", "$BACK/health")

Remove-Item $pedidoArchivo -ErrorAction SilentlyContinue
""
if ($script:fallos -eq 0) { "Todas las pruebas pasaron." } else { "$script:fallos prueba(s) fallaron."; exit 1 }
