#!/bin/bash

# Script para instalar Docker Compose
echo "📦 Instalando Docker Compose..."

# Verificar si ya está instalado
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose ya está instalado:"
    docker-compose --version
    exit 0
fi

if docker compose version &> /dev/null; then
    echo "✅ Docker Compose (nueva sintaxis) ya está disponible:"
    docker compose version
    exit 0
fi

# Detectar arquitectura
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    ARCH="x86_64"
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    ARCH="aarch64"
else
    echo "❌ Arquitectura no soportada: $ARCH"
    exit 1
fi

# Detectar sistema operativo
OS=$(uname -s)
if [ "$OS" = "Linux" ]; then
    OS="linux"
elif [ "$OS" = "Darwin" ]; then
    OS="darwin"
else
    echo "❌ Sistema operativo no soportado: $OS"
    exit 1
fi

echo "🔧 Detectado: $OS-$ARCH"

# Descargar Docker Compose
echo "📥 Descargando Docker Compose..."
COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
echo "📋 Versión: $COMPOSE_VERSION"

sudo curl -L "https://github.com/docker/compose/releases/download/$COMPOSE_VERSION/docker-compose-$OS-$ARCH" -o /usr/local/bin/docker-compose

# Hacer ejecutable
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
if docker-compose --version &> /dev/null; then
    echo "✅ Docker Compose instalado correctamente:"
    docker-compose --version
else
    echo "❌ Error al instalar Docker Compose"
    exit 1
fi

echo ""
echo "🎉 ¡Docker Compose instalado exitosamente!"
echo "📋 Ahora puedes ejecutar: ./start-local.sh" 