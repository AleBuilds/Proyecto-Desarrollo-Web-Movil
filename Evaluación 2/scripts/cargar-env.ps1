# Proveedor de secretos local (SecretProvider): crea .env con secretos aleatorios si no existe
# y lo carga en el entorno del proceso; los servicios hijos heredan las variables.
# Los secretos nunca viven en el código ni en el navegador.
param([string]$Raiz = (Split-Path -Parent $PSScriptRoot))

$envFile = Join-Path $Raiz ".env"
function Nuevo-Secreto { -join ((1..48) | ForEach-Object { '{0:x}' -f (Get-Random -Maximum 16) }) }

if (-not (Test-Path $envFile)) {
    Write-Host "[secretos] Generando .env con secretos aleatorios (no se versiona)..." -ForegroundColor Yellow
    $ejemplo = Get-Content (Join-Path $Raiz ".env.example") -Encoding utf8
    $ejemplo = $ejemplo | ForEach-Object {
        if ($_ -match '^(INTERNAL_SERVICE_SECRET|AUTH_INTROSPECTION_SECRET|PAYMENTS_SERVICE_SECRET|GRPC_SERVICE_SECRET)=') { "$($Matches[1])=$(Nuevo-Secreto)" } else { $_ }
    }
    Set-Content -Path $envFile -Value $ejemplo -Encoding utf8
}
foreach ($clave in 'INTERNAL_SERVICE_SECRET','AUTH_INTROSPECTION_SECRET','PAYMENTS_SERVICE_SECRET','GRPC_SERVICE_SECRET') {
    if (-not (Select-String -Path $envFile -Pattern "^$clave=" -Quiet)) { Add-Content -Path $envFile -Value "$clave=$(Nuevo-Secreto)" -Encoding utf8 }
}
Get-Content $envFile -Encoding utf8 | ForEach-Object {
    if ($_ -match '^\s*([A-Z_]+)=(.*)$') { Set-Item -Path "Env:$($Matches[1])" -Value $Matches[2].Trim() }
}

# Intérprete de Python disponible (algunos equipos solo tienen el lanzador 'py')
$global:PY = "python"
try { & python --version *> $null; if ($LASTEXITCODE -ne 0) { throw } } catch { $global:PY = "py" }
