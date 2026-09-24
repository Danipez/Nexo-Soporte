# Instalación portable de la distribución oficial. Requiere varios GB libres.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $projectRoot '.runtime'
$archivePath = Join-Path $runtimeDir 'ollama-windows-amd64.zip'
$installDir = Join-Path $runtimeDir 'ollama'
New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
$release = Invoke-RestMethod 'https://api.github.com/repos/ollama/ollama/releases/tags/v0.34.4'
$asset = $release.assets | Where-Object name -eq 'ollama-windows-amd64.zip'
if (-not $asset) { throw 'No se encontró la distribución oficial esperada.' }
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $archivePath
if ($asset.digest -and $asset.digest.StartsWith('sha256:')) {
    $actual = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $asset.digest.Substring(7)) { throw 'La verificación de integridad falló.' }
}
Expand-Archive -LiteralPath $archivePath -DestinationPath $installDir -Force
& (Join-Path $PSScriptRoot 'iniciar_ollama.ps1')
$ready = $false
for ($attempt = 0; $attempt -lt 30; $attempt++) {
    try { $null = Invoke-RestMethod 'http://127.0.0.1:11434/api/version' -TimeoutSec 2; $ready = $true; break } catch { Start-Sleep -Seconds 1 }
}
if (-not $ready) { throw 'Ollama no inició. Revisa los registros en .runtime.' }
& (Join-Path $installDir 'ollama.exe') pull qwen3:4b
if ($LASTEXITCODE -ne 0) { throw 'Falló la descarga del modelo de chat.' }
& (Join-Path $installDir 'ollama.exe') pull embeddinggemma
if ($LASTEXITCODE -ne 0) { throw 'Falló la descarga del modelo de embeddings.' }
Write-Output 'Instalación completada. Ejecuta python -m nexo --serve.'
