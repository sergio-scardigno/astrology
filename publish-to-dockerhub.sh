#!/bin/bash

# Script para publicar la imagen en Docker Hub
# Uso: ./publish-to-dockerhub.sh [version]

set -e

# Configuración
DOCKER_USERNAME="sergioscardigno82"
IMAGE_NAME="astrology-api"
VERSION=${1:-latest}

echo "🚀 Iniciando publicación de $IMAGE_NAME:$VERSION a Docker Hub..."

# Verificar que Docker esté ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose"
    exit 1
fi

# Verificar que el usuario esté logueado en Docker Hub
if ! docker info | grep -q "Username"; then
    echo "⚠️  No estás logueado en Docker Hub"
    echo "Ejecuta: docker login"
    exit 1
fi

# Construir la imagen
echo "📦 Construyendo imagen..."
docker build -t $IMAGE_NAME:$VERSION .
docker tag $IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:$VERSION

# Si es la versión latest, también etiquetar como latest
if [ "$VERSION" != "latest" ]; then
    docker tag $IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:latest
fi

# Subir la imagen
echo "⬆️  Subiendo imagen a Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION

if [ "$VERSION" != "latest" ]; then
    docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
fi

echo "✅ ¡Imagen publicada exitosamente!"
echo "📋 URLs de la imagen:"
echo "   $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
echo "   $DOCKER_USERNAME/$IMAGE_NAME:latest"
echo ""
echo "🔗 Para usar la imagen:"
echo "   docker pull $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
echo "   docker run -p 8000:8000 $DOCKER_USERNAME/$IMAGE_NAME:$VERSION" 