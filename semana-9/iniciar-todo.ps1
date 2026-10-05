# Levanta Vault, Auth Service, Backend y Gateway, cada uno en su propia ventana (sin Docker).
# Uso:  .\iniciar-todo.ps1
$raiz = $PSScriptRoot
$py = Join-Path $raiz ".venv\Scripts\python.exe"

if (-not (Test-Path $py)) {
    Write-Host "Falta el entorno virtual. Crealo una vez con:"
    Write-Host "  python -m venv .venv"
    Write-Host "  .venv\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}

function Abrir($titulo, $carpeta, $comando) {
    $script = "`$Host.UI.RawUI.WindowTitle = '$titulo'; Set-Location '$carpeta'; $comando"
    $codificado = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($script))
    Start-Process powershell -ArgumentList "-NoExit", "-EncodedCommand", $codificado
}

Abrir "Vault :8200" $raiz 'vault server -dev -dev-root-token-id="dev-only-token"'
Start-Sleep -Seconds 4
& "$raiz\vault-setup.ps1"

Abrir "Auth :8100" "$raiz\auth" "`$env:AUTH_INTROSPECTION_SECRET='gateway-auth-secret-789'; & '$py' -m uvicorn auth_service:app --host 127.0.0.1 --port 8100"
Abrir "Backend :9000" "$raiz\backend" "`$env:INTERNAL_GATEWAY_SECRET='gateway-api-secret-456'; & '$py' -m uvicorn backend_api:app --host 127.0.0.1 --port 9000"
Abrir "Gateway :8000" "$raiz\gateway" "`$env:VAULT_ADDR='http://127.0.0.1:8200'; `$env:VAULT_TOKEN='dev-only-token'; `$env:BACKEND_URL='http://127.0.0.1:9000'; `$env:AUTH_URL='http://127.0.0.1:8100'; & '$py' -m uvicorn gateway:app --host 127.0.0.1 --port 8000"

Write-Host ""
Write-Host "Listo. Abre http://localhost:8000 (ana / 1234  o  ernesto / admin123)."
Write-Host "Pruebas: .venv\Scripts\python.exe -m pytest tests -q   y   .venv\Scripts\python.exe -m pytest e2e\test_stack.py -q"
