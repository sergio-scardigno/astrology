# 🖥️ Despliegue en VPS - Astrology API

## Opción 1: Docker Run (Más Simple)

### Comando básico:

```bash
docker run -d \
  --name astrology-api \
  -p 8000:8000 \
  -e EPH_PATH=/opt/swisseph/ephe \
  -e PYTHONPATH=/app \
  -e PYTHONUNBUFFERED=1 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  --restart unless-stopped \
  sergioscardigno82/astrology-api:latest
```

### Comando con volumen para efemérides:

```bash
docker run -d \
  --name astrology-api \
  -p 8000:8000 \
  -v /ruta/a/tu/ephe:/opt/swisseph/ephe:ro \
  -e EPH_PATH=/opt/swisseph/ephe \
  -e PYTHONPATH=/app \
  -e PYTHONUNBUFFERED=1 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  --restart unless-stopped \
  sergioscardigno82/astrology-api:latest
```

## Opción 2: Docker Compose (Recomendado)

### 1. Crear archivo docker-compose.yml:

```yaml
version: '3.9'

services:
    astrology:
        image: sergioscardigno82/astrology-api:latest
        container_name: astrology-api
        restart: unless-stopped
        ports:
            - '8000:8000'
        volumes:
            - ./ephe:/opt/swisseph/ephe:ro # Si tienes efemérides
        environment:
            - EPH_PATH=/opt/swisseph/ephe
            - PYTHONPATH=/app
            - PYTHONUNBUFFERED=1
            - HOST=0.0.0.0
            - PORT=8000
        healthcheck:
            test: ['CMD', 'curl', '-f', 'http://localhost:8000/health']
            interval: 30s
            timeout: 10s
            retries: 3
            start_period: 40s
```

### 2. Ejecutar:

```bash
docker-compose up -d
```

## Opción 3: Script de Despliegue

### 1. Crear script deploy-vps.sh:

```bash
#!/bin/bash

# Detener contenedor existente si existe
docker stop astrology-api 2>/dev/null || true
docker rm astrology-api 2>/dev/null || true

# Descargar la imagen más reciente
docker pull sergioscardigno82/astrology-api:latest

# Ejecutar el contenedor
docker run -d \
  --name astrology-api \
  -p 8000:8000 \
  -e EPH_PATH=/opt/swisseph/ephe \
  -e PYTHONPATH=/app \
  -e PYTHONUNBUFFERED=1 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  --restart unless-stopped \
  sergioscardigno82/astrology-api:latest

echo "✅ Astrology API desplegada en puerto 8000"
echo "🔍 Health check: http://tu-ip:8000/health"
echo "📊 Status: http://tu-ip:8000/status"
echo "🌐 Interfaz: http://tu-ip:8000/"
```

### 2. Hacer ejecutable y ejecutar:

```bash
chmod +x deploy-vps.sh
./deploy-vps.sh
```

## 🔧 Pasos en tu VPS:

### 1. Conectar a tu VPS:

```bash
ssh usuario@tu-ip-del-vps
```

### 2. Instalar Docker (si no está instalado):

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# CentOS/RHEL
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### 3. Descargar y ejecutar la imagen:

```bash
# Descargar la imagen
docker pull sergioscardigno82/astrology-api:latest

# Ejecutar (elige una de las opciones anteriores)
docker run -d --name astrology-api -p 8000:8000 \
  -e EPH_PATH=/opt/swisseph/ephe \
  -e PYTHONPATH=/app \
  -e PYTHONUNBUFFERED=1 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  --restart unless-stopped \
  sergioscardigno82/astrology-api:latest
```

## 🔍 Verificación:

### 1. Verificar que el contenedor está corriendo:

```bash
docker ps | grep astrology
```

### 2. Verificar logs:

```bash
docker logs astrology-api
```

### 3. Probar endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Status
curl http://localhost:8000/status

# Interfaz principal
curl http://localhost:8000/
```

### 4. Verificar desde el exterior:

```bash
# Reemplaza TU_IP con la IP de tu VPS
curl http://TU_IP:8000/health
```

## 🌐 Configuración de Firewall:

### Abrir puerto 8000:

```bash
# UFW (Ubuntu)
sudo ufw allow 8000

# iptables
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

## 📋 Comandos útiles:

### Gestionar el contenedor:

```bash
# Ver logs
docker logs -f astrology-api

# Detener
docker stop astrology-api

# Iniciar
docker start astrology-api

# Reiniciar
docker restart astrology-api

# Eliminar
docker rm -f astrology-api
```

### Actualizar la aplicación:

```bash
# Detener y eliminar contenedor actual
docker stop astrology-api
docker rm astrology-api

# Descargar nueva imagen
docker pull sergioscardigno82/astrology-api:latest

# Ejecutar con nueva imagen
docker run -d --name astrology-api -p 8000:8000 \
  -e EPH_PATH=/opt/swisseph/ephe \
  -e PYTHONPATH=/app \
  -e PYTHONUNBUFFERED=1 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  --restart unless-stopped \
  sergioscardigno82/astrology-api:latest
```

## 🎯 URLs de acceso:

Una vez desplegado, podrás acceder a:

-   `http://TU_IP:8000/health` - Health check
-   `http://TU_IP:8000/status` - Estado de la API
-   `http://TU_IP:8000/` - Interfaz principal
-   `http://TU_IP:8000/carta?anio=1990&mes=1&dia=1&hora=12&minuto=0&tz=0&lat=40.4168&lon=-3.7038` - Ejemplo de carta
