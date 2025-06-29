#!/bin/bash

# Script para ejecutar directamente el Dockerfile
echo "🚀 Ejecutando Astrology API directamente con Docker..."

# Variables
CONTAINER_NAME="astrology-api"
IMAGE_NAME="astrology-api"
PORT="8000"

# Detener contenedor existente si existe
echo "🛑 Deteniendo contenedor existente..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Construir imagen desde Dockerfile
echo "🔨 Construyendo imagen desde Dockerfile..."
docker build -t $IMAGE_NAME .

# Ejecutar contenedor
echo "🚀 Ejecutando contenedor..."
docker run -d \
    --name $CONTAINER_NAME \
    -p $PORT:8000 \
    -v $(pwd)/ephe:/opt/swisseph/ephe:ro \
    -e EPH_PATH=/opt/swisseph/ephe \
    -e PYTHONPATH=/app \
    -e PYTHONUNBUFFERED=1 \
    -e HOST=0.0.0.0 \
    -e PORT=8000 \
    --restart unless-stopped \
    $IMAGE_NAME

# Esperar a que esté listo
echo "⏳ Esperando a que el servicio esté listo..."
sleep 15

# Verificar que funciona
echo "🔍 Verificando que funciona..."
if curl -f http://localhost:$PORT/health > /dev/null 2>&1; then
    echo "✅ ¡Servicio funcionando correctamente!"
    echo ""
    echo "🌐 URLs de acceso:"
    echo "   Health: http://localhost:$PORT/health"
    echo "   Status: http://localhost:$PORT/status"
    echo "   Interfaz: http://localhost:$PORT/"
    echo ""
    echo "📋 Para ver logs: docker logs -f $CONTAINER_NAME"
    echo "🛑 Para detener: docker stop $CONTAINER_NAME"
    echo "🗑️  Para eliminar: docker rm $CONTAINER_NAME"
else
    echo "❌ Error: El servicio no responde"
    echo "📋 Revisando logs..."
    docker logs $CONTAINER_NAME --tail=20
fi 