# Inicia la distribución local de Ollama sin exponer el servicio a la red.
$projectRoot = Split-Path -Parent $PSScriptRoot
$ollamaExe = Join-Path $projectRoot '.runtime\ollama\ollama.exe'
if (-not (Test-Path -LiteralPath $ollamaExe)) {
    throw 'No se encontró Ollama local. Ejecuta scripts\instalar_ollama.ps1 o instala Ollama desde su sitio oficial.'
}
$env:OLLAMA_MODELS = Join-Path $projectRoot '.runtime\models'
$env:OLLAMA_HOST = '127.0.0.1:11434'
$env:OLLAMA_NO_CLOUD = '1'
try {
    $null = Invoke-RestMethod 'http://127.0.0.1:11434/api/version' -TimeoutSec 3
    Write-Output 'Ollama ya está disponible en el puerto local 11434.'
} catch {
    Start-Process -FilePath $ollamaExe -ArgumentList 'serve' -WindowStyle Hidden -RedirectStandardOutput (Join-Path $projectRoot '.runtime\ollama-out.log') -RedirectStandardError (Join-Path $projectRoot '.runtime\ollama-error.log')
    Write-Output 'Ollama iniciado. El servicio utiliza únicamente localhost.'
}
