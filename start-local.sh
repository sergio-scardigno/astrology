#!/bin/bash

# Script para iniciar Astrology API localmente
echo "🚀 Iniciando Astrology API localmente..."

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose -f docker-compose.local.yml down 2>/dev/null || true

# Construir y ejecutar
echo "🔨 Construyendo y ejecutando..."
docker-compose -f docker-compose.local.yml up --build -d

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
    echo "📋 Para ver logs: docker-compose -f docker-compose.local.yml logs -f"
    echo "🛑 Para detener: docker-compose -f docker-compose.local.yml down"
else
    echo "❌ Error: El servicio no responde"
    echo "📋 Revisando logs..."
    docker-compose -f docker-compose.local.yml logs --tail=20
fi 