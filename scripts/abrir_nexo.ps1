$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $projectRoot '.runtime'
New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
try { & (Join-Path $PSScriptRoot 'iniciar_ollama.ps1') } catch {
    Write-Warning 'Ollama local no está instalado. Se puede utilizar la consulta documental.'
}
$serverReady = $false
try {
    $page = Invoke-WebRequest 'http://127.0.0.1:8765' -UseBasicParsing -TimeoutSec 3
    if ($page.Content -notmatch 'Nexo') { throw 'El puerto 8765 está ocupado por otro programa.' }
    $serverReady = $true
} catch {
    if ($_.Exception.Message -like '*ocupado por otro programa*') { throw }
}
if (-not $serverReady) {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
    $process = Start-Process -FilePath $pythonExe -ArgumentList '-m','nexo','--serve' -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runtimeDir 'web-out.log') -RedirectStandardError (Join-Path $runtimeDir 'web-error.log')
    $process.Id | Set-Content (Join-Path $runtimeDir 'web.pid')
    for ($attempt = 0; $attempt -lt 15; $attempt++) {
        try { $null = Invoke-WebRequest 'http://127.0.0.1:8765' -UseBasicParsing -TimeoutSec 2; $serverReady = $true; break } catch { Start-Sleep -Seconds 1 }
    }
}
if (-not $serverReady) { throw 'Nexo no pudo iniciar. Revisa .runtime\web-error.log.' }
Start-Process 'http://127.0.0.1:8765'
Write-Output 'Nexo está abierto en el navegador. El servicio sigue funcionando en segundo plano.'
