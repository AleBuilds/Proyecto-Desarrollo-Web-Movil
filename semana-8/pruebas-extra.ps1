$GW          = "http://127.0.0.1:8000"
$USER_TOKEN  = if ($env:USER_TOKEN)  { $env:USER_TOKEN }  else { "student-token-123" }
$ADMIN_TOKEN = if ($env:ADMIN_TOKEN) { $env:ADMIN_TOKEN } else { "admin-token-456" }
$SECRET      = if ($env:BACKEND_SECRET) { $env:BACKEND_SECRET } else { "gateway-api-secret-456" }
$env:VAULT_ADDR  = if ($env:VAULT_ADDR)  { $env:VAULT_ADDR }  else { "http://127.0.0.1:8200" }
$env:VAULT_TOKEN = if ($env:VAULT_TOKEN) { $env:VAULT_TOKEN } else { "dev-only-token" }

$script:fallos = 0
function Codigo([string[]]$curlArgs) { & curl.exe -s -o NUL -w "%{http_code}" @curlArgs }
function Resultado($nombre, $esperado, $codigo) {
    $ok = ($codigo -eq "$esperado")
    if (-not $ok) { $script:fallos++ }
    "{0,-6} {1,-58} esperado {2}  obtenido {3}" -f $(if ($ok) {"OK"} else {"FALLA"}), $nombre, $esperado, $codigo
}

# --- Prueba 7: rotación del token en Vault ---
try {
    vault kv patch secret/gateway usuario_token="nuevo-token-789" | Out-Null
    Resultado "Rotación: token anterior" 401 (Codigo @("-H","Authorization: Bearer $USER_TOKEN","$GW/api/productos"))
    Resultado "Rotación: token nuevo"    200 (Codigo @("-H","Authorization: Bearer nuevo-token-789","$GW/api/productos"))
} finally {
    vault kv patch secret/gateway usuario_token="$USER_TOKEN" | Out-Null
}

# --- Prueba 8: secreto interno incorrecto (el 403 lo da el backend) ---
try {
    vault kv patch secret/gateway backend_secret="secreto-incorrecto" | Out-Null
    Resultado "Secreto interno incorrecto" 403 (Codigo @("-H","Authorization: Bearer $ADMIN_TOKEN","$GW/api/productos"))
} finally {
    vault kv patch secret/gateway backend_secret="$SECRET" | Out-Null
}

# --- Prueba 6: backend apagado (manual) ---
Read-Host "Detén el backend (Ctrl+C en su terminal) y presiona Enter"
Resultado "Backend apagado" 502 (Codigo @("-H","Authorization: Bearer $ADMIN_TOKEN","$GW/api/productos"))
Read-Host "Vuelve a levantar el backend y presiona Enter"

# --- Prueba 5: Vault apagado (manual) ---
Read-Host "Detén Vault (Ctrl+C en su terminal) y presiona Enter"
Resultado "Vault apagado (tarda ~5 s)" 500 (Codigo @("-H","Authorization: Bearer $ADMIN_TOKEN","$GW/api/productos"))
Write-Host "Vuelve a levantar Vault y ejecuta .\vault-setup.ps1"

""
if ($script:fallos -eq 0) { "Todas las pruebas pasaron." } else { "$script:fallos prueba(s) fallaron."; exit 1 }