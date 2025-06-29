#!/bin/bash

# Script para iniciar Astrology API localmente
echo "🚀 Iniciando Astrology API localmente..."

# Detectar si usar docker-compose o docker compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Error: Docker Compose no está instalado"
    echo "📦 Instalando Docker Compose..."
    
    # Instalar Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Verificar instalación
    if docker-compose --version &> /dev/null; then
        COMPOSE_CMD="docker-compose"
        echo "✅ Docker Compose instalado correctamente"
    else
        echo "❌ Error al instalar Docker Compose"
        exit 1
    fi
fi

echo "🔧 Usando: $COMPOSE_CMD"

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
$COMPOSE_CMD -f docker-compose.local.yml down 2>/dev/null || true

# Construir y ejecutar
echo "🔨 Construyendo y ejecutando..."
$COMPOSE_CMD -f docker-compose.local.yml up --build -d

# Esperar a que esté listo
echo "⏳ Esperando a que el servicio esté listo..."
sleep 10

# Verificar que funciona
echo "🔍 Verificando que funciona..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ ¡Servicio funcionando correctamente!"
    echo ""
    echo "🌐 URLs de acceso:"
    echo "   Health: http://localhost:8000/health"
    echo "   Status: http://localhost:8000/status"
    echo "   Interfaz: http://localhost:8000/"
    echo ""
    echo "📋 Para ver logs: $COMPOSE_CMD -f docker-compose.local.yml logs -f"
    echo "🛑 Para detener: $COMPOSE_CMD -f docker-compose.local.yml down"
else
    echo "❌ Error: El servicio no responde"
    echo "📋 Revisando logs..."
    $COMPOSE_CMD -f docker-compose.local.yml logs --tail=20
fi 