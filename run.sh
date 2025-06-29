#!/bin/bash

# Script para ejecutar la aplicación de astrología con Docker
# Incluye configuración para HTTPS

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Aplicación de Astrología con HTTPS ===${NC}"

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker no está instalado. Por favor, instala Docker primero.${NC}"
    exit 1
fi

# Verificar si la imagen existe, si no, construirla
if [[ "$(docker images -q astrology-app 2> /dev/null)" == "" ]]; then
    echo -e "${YELLOW}Construyendo imagen Docker...${NC}"
    docker build -t astrology-app .
fi

# Detener contenedor existente si está corriendo
if docker ps -q -f name=astrology-app | grep -q .; then
    echo -e "${YELLOW}Deteniendo contenedor existente...${NC}"
    docker stop astrology-app
    docker rm astrology-app
fi

# Ejecutar el contenedor
echo -e "${GREEN}Iniciando aplicación...${NC}"
docker run -d \
    --name astrology-app \
    --restart unless-stopped \
    -p 80:80 \
    -p 443:443 \
    -v "$(pwd)/ephe:/opt/swisseph/ephe:ro" \
    astrology-app

# Esperar a que la aplicación esté lista
echo -e "${YELLOW}Esperando a que la aplicación esté lista...${NC}"
sleep 10

# Verificar que la aplicación esté funcionando
if curl -f -k https://localhost/health &> /dev/null; then
    echo -e "${GREEN}✅ Aplicación iniciada correctamente!${NC}"
    echo -e "${BLUE}📱 URLs de acceso:${NC}"
    echo -e "   🌐 HTTP:  http://localhost"
    echo -e "   🔒 HTTPS: https://localhost"
    echo -e "   📊 Health: https://localhost/health"
    echo -e "   📋 Status: https://localhost/status"
    echo -e ""
    echo -e "${YELLOW}⚠️  Nota: El certificado SSL es auto-firmado.${NC}"
    echo -e "   Tu navegador mostrará una advertencia de seguridad."
    echo -e "   Puedes hacer clic en 'Avanzado' y 'Continuar' para acceder."
    echo -e ""
    echo -e "${BLUE}Para detener la aplicación:${NC}"
    echo -e "   docker stop astrology-app"
    echo -e ""
    echo -e "${BLUE}Para ver los logs:${NC}"
    echo -e "   docker logs -f astrology-app"
else
    echo -e "${RED}❌ Error: La aplicación no se inició correctamente.${NC}"
    echo -e "${YELLOW}Revisando logs...${NC}"
    docker logs astrology-app
    exit 1
fi 