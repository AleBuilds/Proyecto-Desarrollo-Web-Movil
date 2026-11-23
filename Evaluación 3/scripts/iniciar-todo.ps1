# Script para iniciar todos los microservicios de la Evaluación 2 - El Mediterráneo
$raiz = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "cargar-env.ps1")
$py = $global:PY

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO ARQUITECTURA EVALUACIÓN 2 - CASO 22           " -ForegroundColor Cyan
Write-Host "  Plataforma Comercial 'El Mediterráneo'                  " -ForegroundColor Cyan
Write-Host "  Integrantes: Alejandro Narváez y Silenay Sarmiento       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Puertos (sobrescribibles con PUERTO_<SERVICIO> si el equipo ya usa alguno, p. ej. un kernel de Jupyter)
function Puerto($nombre, $defecto) { $v = [Environment]::GetEnvironmentVariable("PUERTO_$nombre"); if ($v) { [int]$v } else { $defecto } }
$P = @{ GATEWAY = Puerto "GATEWAY" 8000; GRAPHQL = Puerto "GRAPHQL" 8050; AUTH = Puerto "AUTH" 8100
        INVENTORY = Puerto "INVENTORY" 9001; ORDERS = Puerto "ORDERS" 9002; CLIENTS = Puerto "CLIENTS" 9003
        PAYMENTS = Puerto "PAYMENTS" 9004 }
$ocupados = @()
foreach ($k in $P.Keys) {
    $c = Get-NetTCPConnection -State Listen -LocalPort $P[$k] -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($c) { $ocupados += "$k (:$($P[$k])) usado por PID $($c.OwningProcess)" }
}
if ($ocupados) {
    Write-Host "Puertos ocupados:" -ForegroundColor Red; $ocupados | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    Write-Host "Cierre el programa que los usa, ejecute scripts\detener-todo.ps1, o defina p. ej. `$env:PUERTO_INVENTORY=19001" -ForegroundColor Yellow
    exit 1
}
$env:AUTH_URL = "http://127.0.0.1:$($P.AUTH)"; $env:INVENTORY_URL = "http://127.0.0.1:$($P.INVENTORY)"
$env:ORDERS_URL = "http://127.0.0.1:$($P.ORDERS)"; $env:CLIENTS_URL = "http://127.0.0.1:$($P.CLIENTS)"
$env:PAYMENTS_URL = "http://127.0.0.1:$($P.PAYMENTS)"; $env:GRAPHQL_URL = "http://127.0.0.1:$($P.GRAPHQL)"
$env:PUERTOS_ALTERNATIVOS = (($P.Values + 50051) -join ',')

# 1. Sembrar bases de datos
& $py "$raiz\scripts\sembrar_datos.py"

function Iniciar-Servicio($titulo, $carpeta, $comando) {
    Write-Host "[Iniciando] $titulo..." -ForegroundColor Yellow
    $script = "`$Host.UI.RawUI.WindowTitle = '$titulo'; Set-Location '$carpeta'; $comando"
    $bytes = [Text.Encoding]::Unicode.GetBytes($script)
    $encoded = [Convert]::ToBase64String($bytes)
    Start-Process powershell -ArgumentList "-NoExit", "-EncodedCommand", $encoded
}

# 2. Levantar microservicios privados
Iniciar-Servicio "Auth Service :8100" "$raiz\auth_service" "$py -m uvicorn auth_service:app --host 127.0.0.1 --port $($P.AUTH)"
Iniciar-Servicio "Inventory :9001" "$raiz\services\inventory" "$py -m uvicorn inventory_service:app --host 127.0.0.1 --port $($P.INVENTORY)"
Iniciar-Servicio "Orders :9002" "$raiz\services\orders" "$py -m uvicorn orders_service:app --host 127.0.0.1 --port $($P.ORDERS)"
Iniciar-Servicio "Clients :9003" "$raiz\services\clients" "$py -m uvicorn clients_service:app --host 127.0.0.1 --port $($P.CLIENTS)"
Iniciar-Servicio "Payments :9004" "$raiz\services\payments" "$py -m uvicorn payments_service:app --host 127.0.0.1 --port $($P.PAYMENTS)"
Iniciar-Servicio "GraphQL Gateway :8050" "$raiz\graphql_gateway" "$py -m uvicorn server:app --host 127.0.0.1 --port $($P.GRAPHQL)"
Iniciar-Servicio "gRPC Delivery :50051" "$raiz\services\delivery_telemetry" "$py grpc_server.py"

# Esperar 3 segundos para que los microservicios levanten
Start-Sleep -Seconds 3

# 3. Levantar API Gateway
Iniciar-Servicio "API Gateway :8000" "$raiz\gateway" "$py -m uvicorn gateway:app --host 127.0.0.1 --port $($P.GATEWAY)"

Write-Host ""
Write-Host "✓ Todos los servicios se han iniciado." -ForegroundColor Green
Write-Host "Accede a la aplicación en: http://127.0.0.1:$($P.GATEWAY)" -ForegroundColor Cyan
Write-Host "Cuentas de prueba: ana / 1234  |  silenay / silenay123  |  administrador1 / admin123" -ForegroundColor Gray
Write-Host "Para ejecutar las pruebas: powershell scripts\probar-todo.ps1" -ForegroundColor Yellow
