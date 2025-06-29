# 🌟 Astrology API - Carta Astral Completa

API de astrología que calcula cartas astrales completas con planetas, casas, aspectos y balance de elementos.

## ✨ Características

-   **Planetas principales**: Sol, Luna, Mercurio, Venus, Marte, Júpiter, Saturno, Urano, Neptuno, Plutón
-   **Casas astrológicas**: Las 12 casas con grados y signos
-   **Aspectos planetarios**: Conjunción, oposición, trígono, cuadratura, sextil
-   **Balance de elementos**: Análisis de fuego, tierra, aire y agua
-   **Interfaz web**: Visualización interactiva de la carta astral
-   **API REST**: Endpoint para integración con otras aplicaciones

## 🚀 Despliegue Rápido

### Opción 1: Docker Hub (Recomendado)

```bash
# En tu VPS
docker run -d \
  --name astrology-app \
  -p 8000:8000 \
  -v $(pwd)/ephe:/opt/swisseph/ephe:ro \
  tu-usuario-dockerhub/astrology-api:latest
```

### Opción 2: Docker Compose

```bash
# Descargar docker-compose.prod.yml
wget https://raw.githubusercontent.com/tu-usuario/astrology-api/main/docker-compose.prod.yml

# Configurar variables de entorno
export DOCKER_USERNAME=tu-usuario-dockerhub
export VERSION=latest

# Ejecutar
docker-compose -f docker-compose.prod.yml up -d
```

### Opción 3: Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/astrology-api.git
cd astrology-api

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📦 Subir a Docker Hub

### 1. Preparar la imagen

```bash
# Hacer el script ejecutable
chmod +x deploy.sh

# Ejecutar despliegue
./deploy.sh v1.0.0 tu-usuario-dockerhub
```

### 2. Configurar en VPS

```bash
# En tu VPS, crear archivo .env
echo "DOCKER_USERNAME=tu-usuario-dockerhub" > .env
echo "VERSION=v1.0.0" >> .env

# Ejecutar con docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Configuración de VPS

### Requisitos Mínimos

-   **RAM**: 1GB
-   **CPU**: 1 vCore
-   **Disco**: 10GB
-   **OS**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+

### Instalación de Docker

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

### Configuración de Firewall

```bash
# Abrir puertos necesarios
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # API (opcional)
sudo ufw enable
```

## 🌐 Configuración de Dominio

### Con Nginx (Recomendado)

```bash
# Instalar Nginx
sudo apt update
sudo apt install nginx

# Configurar proxy reverso
sudo cp nginx.conf /etc/nginx/sites-available/astrology
sudo ln -s /etc/nginx/sites-available/astrology /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Con SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com

# Renovar automáticamente
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoreo

### Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f astrology

# Ver logs específicos
docker logs astrology-app
```

### Health Check

```bash
# Verificar estado
curl http://localhost:8000/

# Health check endpoint
curl http://localhost:8000/health
```

### Métricas

```bash
# Uso de recursos
docker stats astrology-app

# Espacio en disco
df -h
```

## 🔒 Seguridad

### Variables de Entorno

```bash
# Crear archivo .env
cat > .env << EOF
DOCKER_USERNAME=tu-usuario-dockerhub
VERSION=latest
EPH_PATH=/opt/swisseph/ephe
PYTHONPATH=/app
PYTHONUNBUFFERED=1
EOF
```

### Firewall

```bash
# Configurar UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 📈 Escalabilidad

### Con Docker Swarm

```bash
# Inicializar swarm
docker swarm init

# Desplegar stack
docker stack deploy -c docker-compose.yml astrology
```

### Con Kubernetes

```bash
# Crear deployment
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## 🐛 Troubleshooting

### Problemas Comunes

1. **Error de efemérides**

    ```bash
    # Verificar que el directorio ephe existe
    ls -la ephe/
    ```

2. **Puerto ocupado**

    ```bash
    # Verificar puertos en uso
    sudo netstat -tulpn | grep :8000
    ```

3. **Permisos de Docker**
    ```bash
    # Agregar usuario al grupo docker
    sudo usermod -aG docker $USER
    newgrp docker
    ```

### Logs de Error

```bash
# Ver logs detallados
docker-compose logs --tail=100 astrology

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

## 📝 API Documentation

### Endpoint Principal

```
GET /carta?anio=1982&mes=6&dia=6&hora=6&minuto=30&tz=-3&lat=-35.5728&lon=-58.0096
```

### Parámetros

-   `anio`: Año de nacimiento (1500-2100)
-   `mes`: Mes (1-12)
-   `dia`: Día (1-31)
-   `hora`: Hora (0-23)
-   `minuto`: Minuto (0-59)
-   `tz`: Zona horaria (-12 a 12)
-   `lat`: Latitud (-90 a 90)
-   `lon`: Longitud (-180 a 180)

### Respuesta

```json
{
    "planetas": {
        "sol": { "signo": "Géminis", "grado": 75.3549 },
        "luna": { "signo": "Sagitario", "grado": 252.4059 }
    },
    "casas": {
        "1": { "grado": 56.6642, "signo": "Tauro" }
    },
    "aspectos": [
        {
            "planeta1": "sol",
            "planeta2": "luna",
            "aspecto": "oposición",
            "orbe": 0.5
        }
    ],
    "balance_elementos": {
        "elementos": {
            "Fuego": { "cantidad": 3, "porcentaje": 30.0 },
            "Tierra": { "cantidad": 4, "porcentaje": 40.0 }
        },
        "dominante": "Tierra",
        "balance_general": "Balanceado"
    }
}
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

-   [Swiss Ephemeris](https://www.astro.com/swisseph/) - Cálculos astronómicos precisos
-   [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
-   [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI de alto rendimiento
