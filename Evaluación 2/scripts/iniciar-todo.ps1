# Script para iniciar todos los microservicios de la Evaluación 2 - El Mediterráneo
$raiz = Split-Path -Parent $PSScriptRoot
$py = "python"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO ARQUITECTURA EVALUACIÓN 2 - CASO 22           " -ForegroundColor Cyan
Write-Host "  Plataforma Comercial 'El Mediterráneo'                  " -ForegroundColor Cyan
Write-Host "  Integrantes: Alejandro Narváez y Silenay Sarmiento       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

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
Iniciar-Servicio "Auth Service :8100" "$raiz\auth_service" "$py -m uvicorn auth_service:app --host 127.0.0.1 --port 8100"
Iniciar-Servicio "Inventory :9001" "$raiz\services\inventory" "$py -m uvicorn inventory_service:app --host 127.0.0.1 --port 9001"
Iniciar-Servicio "Orders :9002" "$raiz\services\orders" "$py -m uvicorn orders_service:app --host 127.0.0.1 --port 9002"
Iniciar-Servicio "Clients :9003" "$raiz\services\clients" "$py -m uvicorn clients_service:app --host 127.0.0.1 --port 9003"
Iniciar-Servicio "Payments :9004" "$raiz\services\payments" "$py -m uvicorn payments_service:app --host 127.0.0.1 --port 9004"
Iniciar-Servicio "GraphQL Gateway :8050" "$raiz\graphql_gateway" "$py -m uvicorn server:app --host 127.0.0.1 --port 8050"
Iniciar-Servicio "gRPC Delivery :50051" "$raiz\services\delivery_telemetry" "$py grpc_server.py"

# Esperar 3 segundos para que los microservicios levanten
Start-Sleep -Seconds 3

# 3. Levantar API Gateway
Iniciar-Servicio "API Gateway :8000" "$raiz\gateway" "$py -m uvicorn gateway:app --host 127.0.0.1 --port 8000"

Write-Host ""
Write-Host "✓ Todos los servicios se han iniciado." -ForegroundColor Green
Write-Host "Accede a la aplicación en: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Cuentas de prueba: ana / 1234  |  silenay / silenay123  |  administrador1 / admin123" -ForegroundColor Gray
Write-Host "Para ejecutar las pruebas: powershell scripts\probar-todo.ps1" -ForegroundColor Yellow
