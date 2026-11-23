# Detiene únicamente los procesos de esta plataforma (uvicorn / grpc_server), identificados por línea de comandos.
$puertos = 8000, 8050, 8100, 9001, 9002, 9003, 9004, 50051
if ($env:PUERTOS_ALTERNATIVOS) { $puertos = $env:PUERTOS_ALTERNATIVOS -split ',' | ForEach-Object { [int]$_ } }
foreach ($p in $puertos) {
    Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue | ForEach-Object {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($_.OwningProcess)"
        if ($proc.CommandLine -match 'uvicorn|grpc_server\.py') {
            Stop-Process -Id $_.OwningProcess -Force
            Write-Host "[detenido] puerto $p (PID $($_.OwningProcess))" -ForegroundColor Yellow
        } elseif ($proc) {
            Write-Host "[omitido] puerto $p lo usa otro programa ($($proc.Name)); no se toca." -ForegroundColor DarkGray
        }
    }
}
# Cierra las ventanas de PowerShell que alojaban los servicios
Get-Process powershell -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -match ' :(8000|8050|8100|900\d|50051)$' } | Stop-Process -Force
Write-Host "Plataforma detenida." -ForegroundColor Green
