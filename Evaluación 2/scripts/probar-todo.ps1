# Script para ejecutar la suite completa de pruebas automáticas de la Evaluación 2
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  EJECUTANDO PRUEBAS AUTOMATIZADAS - EVALUACIÓN 2         " -ForegroundColor Cyan
Write-Host "  Caso 22: El Mediterráneo                                " -ForegroundColor Cyan
Write-Host "  Alejandro Narváez & Silenay Sarmiento                   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

python -m pytest tests -v --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ TODAS LAS PRUEBAS DE LA EVALUACIÓN 2 PASARON CON ÉXITO." -ForegroundColor Green
    Write-Host "Cobertura completa: Seguridad, RBAC, Idempotencia, GraphQL, gRPC y E2E." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ Se detectaron fallos en la suite de pruebas." -ForegroundColor Red
    exit 1
}
