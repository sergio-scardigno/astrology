# Script para ejecutar la aplicación de astrología con Docker en Windows
# Incluye configuración para HTTPS

param(
    [switch]$Build,
    [switch]$Stop,
    [switch]$Logs
)

# Colores para output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = $White
    )
    Write-Host $Message -ForegroundColor $Color
}

Write-ColorOutput "=== Aplicación de Astrología con HTTPS ===" $Blue

# Verificar si Docker está instalado
try {
    docker --version | Out-Null
} catch {
    Write-ColorOutput "Error: Docker no está instalado. Por favor, instala Docker Desktop primero." $Red
    exit 1
}

# Función para detener contenedor
if ($Stop) {
    Write-ColorOutput "Deteniendo contenedor..." $Yellow
    docker stop astrology-app 2>$null
    docker rm astrology-app 2>$null
    Write-ColorOutput "Contenedor detenido." $Green
    exit 0
}

# Función para mostrar logs
if ($Logs) {
    Write-ColorOutput "Mostrando logs del contenedor..." $Blue
    docker logs -f astrology-app
    exit 0
}

# Verificar si la imagen existe, si no, construirla
$imageExists = docker images -q astrology-app 2>$null
if (-not $imageExists -or $Build) {
    Write-ColorOutput "Construyendo imagen Docker..." $Yellow
    docker build -t astrology-app .
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "Error al construir la imagen Docker." $Red
        exit 1
    }
}

# Detener contenedor existente si está corriendo
$containerRunning = docker ps -q -f name=astrology-app 2>$null
if ($containerRunning) {
    Write-ColorOutput "Deteniendo contenedor existente..." $Yellow
    docker stop astrology-app
    docker rm astrology-app
}

# Ejecutar el contenedor
Write-ColorOutput "Iniciando aplicación..." $Green
docker run -d `
    --name astrology-app `
    --restart unless-stopped `
    -p 80:80 `
    -p 443:443 `
    -v "${PWD}\ephe:/opt/swisseph/ephe:ro" `
    astrology-app

if ($LASTEXITCODE -ne 0) {
    Write-ColorOutput "Error al iniciar el contenedor." $Red
    exit 1
}

# Esperar a que la aplicación esté lista
Write-ColorOutput "Esperando a que la aplicación esté lista..." $Yellow
Start-Sleep -Seconds 10

# Verificar que la aplicación esté funcionando
try {
    $response = Invoke-WebRequest -Uri "https://localhost/health" -SkipCertificateCheck -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-ColorOutput "✅ Aplicación iniciada correctamente!" $Green
        Write-ColorOutput "📱 URLs de acceso:" $Blue
        Write-ColorOutput "   🌐 HTTP:  http://localhost" $White
        Write-ColorOutput "   🔒 HTTPS: https://localhost" $White
        Write-ColorOutput "   📊 Health: https://localhost/health" $White
        Write-ColorOutput "   📋 Status: https://localhost/status" $White
        Write-ColorOutput "" $White
        Write-ColorOutput "⚠️  Nota: El certificado SSL es auto-firmado." $Yellow
        Write-ColorOutput "   Tu navegador mostrará una advertencia de seguridad." $White
        Write-ColorOutput "   Puedes hacer clic en 'Avanzado' y 'Continuar' para acceder." $White
        Write-ColorOutput "" $White
        Write-ColorOutput "Para detener la aplicación:" $Blue
        Write-ColorOutput "   docker stop astrology-app" $White
        Write-ColorOutput "   o ejecutar: .\run.ps1 -Stop" $White
        Write-ColorOutput "" $White
        Write-ColorOutput "Para ver los logs:" $Blue
        Write-ColorOutput "   docker logs -f astrology-app" $White
        Write-ColorOutput "   o ejecutar: .\run.ps1 -Logs" $White
    } else {
        throw "Status code: $($response.StatusCode)"
    }
} catch {
    Write-ColorOutput "❌ Error: La aplicación no se inició correctamente." $Red
    Write-ColorOutput "Revisando logs..." $Yellow
    docker logs astrology-app
    exit 1
} 