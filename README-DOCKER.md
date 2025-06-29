# 🐳 Ejecución con Docker y HTTPS

Este proyecto ha sido configurado para ejecutarse fácilmente con Docker, incluyendo soporte para HTTPS con certificados SSL auto-firmados.

## 🚀 Ejecución Rápida

### En Linux/macOS:

```bash
# Dar permisos de ejecución al script
chmod +x run.sh

# Ejecutar la aplicación
./run.sh
```

### En Windows (PowerShell):

```powershell
# Ejecutar la aplicación
.\run.ps1
```

## 📋 Comandos Manuales

Si prefieres ejecutar los comandos manualmente:

### 1. Construir la imagen

```bash
docker build -t astrology-app .
```

### 2. Ejecutar el contenedor

```bash
docker run -d \
    --name astrology-app \
    --restart unless-stopped \
    -p 80:80 \
    -p 443:443 \
    -v "$(pwd)/ephe:/opt/swisseph/ephe:ro" \
    astrology-app
```

### 3. Verificar el estado

```bash
# Verificar que el contenedor esté corriendo
docker ps

# Ver logs
docker logs -f astrology-app

# Verificar health check
curl -k https://localhost/health
```

## 🌐 Acceso a la Aplicación

Una vez que la aplicación esté corriendo, puedes acceder a ella a través de:

-   **HTTP**: http://localhost (redirige automáticamente a HTTPS)
-   **HTTPS**: https://localhost
-   **Health Check**: https://localhost/health
-   **Status**: https://localhost/status
-   **API Carta**: https://localhost/carta

## 🔒 Certificado SSL

La aplicación incluye un certificado SSL auto-firmado que se genera automáticamente durante la construcción de la imagen Docker.

**⚠️ Importante**: Como el certificado es auto-firmado, tu navegador mostrará una advertencia de seguridad. Para acceder:

1. Haz clic en "Avanzado"
2. Haz clic en "Continuar hacia localhost (no seguro)"

## 🛠️ Gestión del Contenedor

### Detener la aplicación

```bash
# Con script
./run.sh --stop  # Linux/macOS
.\run.ps1 -Stop  # Windows

# Manualmente
docker stop astrology-app
docker rm astrology-app
```

### Ver logs

```bash
# Con script
./run.sh --logs  # Linux/macOS
.\run.ps1 -Logs  # Windows

# Manualmente
docker logs -f astrology-app
```

### Reconstruir imagen

```bash
# Con script
./run.sh --build  # Linux/macOS
.\run.ps1 -Build  # Windows

# Manualmente
docker build -t astrology-app .
```

## 📁 Estructura del Proyecto

```
astrology-ap/
├── Dockerfile              # Configuración de la imagen Docker
├── nginx.conf              # Configuración de Nginx con SSL
├── supervisord.conf        # Configuración de Supervisor
├── run.sh                  # Script de ejecución (Linux/macOS)
├── run.ps1                 # Script de ejecución (Windows)
├── .dockerignore           # Archivos a excluir del build
├── main.py                 # Aplicación FastAPI
├── util.py                 # Utilidades de astrología
├── index.html              # Interfaz web
├── requirements.txt        # Dependencias de Python
└── ephe/                   # Archivos de efemérides
```

## 🔧 Configuración Técnica

### Servicios Incluidos

-   **FastAPI**: Servidor de la aplicación (puerto 8000 interno)
-   **Nginx**: Proxy reverso con SSL (puertos 80 y 443)
-   **Supervisor**: Gestión de procesos

### Variables de Entorno

-   `EPH_PATH=/opt/swisseph/ephe`: Ruta a los archivos de efemérides
-   `PYTHONPATH=/app`: Ruta del código Python
-   `PYTHONUNBUFFERED=1`: Salida no bufferizada de Python

### Puertos

-   **80**: HTTP (redirige a HTTPS)
-   **443**: HTTPS
-   **8000**: FastAPI (interno)

## 🐛 Solución de Problemas

### Error de certificado SSL

Si tienes problemas con el certificado SSL:

```bash
# Verificar que el certificado se generó correctamente
docker exec astrology-app ls -la /etc/nginx/ssl/
```

### Problemas de permisos

```bash
# Verificar permisos del usuario astrology
docker exec astrology-app id
```

### Logs detallados

```bash
# Ver logs de Nginx
docker exec astrology-app tail -f /var/log/nginx/error.log

# Ver logs de FastAPI
docker exec astrology-app tail -f /var/log/supervisor/fastapi.log

# Ver logs de Supervisor
docker exec astrology-app tail -f /var/log/supervisor/supervisord.log
```

### Reiniciar servicios

```bash
# Reiniciar Nginx
docker exec astrology-app supervisorctl restart nginx

# Reiniciar FastAPI
docker exec astrology-app supervisorctl restart fastapi
```

## 🔄 Actualizaciones

Para actualizar la aplicación:

1. Detener el contenedor actual
2. Reconstruir la imagen con los cambios
3. Ejecutar el nuevo contenedor

```bash
# Detener
docker stop astrology-app
docker rm astrology-app

# Reconstruir y ejecutar
./run.sh --build  # o .\run.ps1 -Build
```

## 📝 Notas Adicionales

-   La aplicación se ejecuta con un usuario no-root (`astrology`) por seguridad
-   Los archivos de efemérides se montan como volumen de solo lectura
-   El contenedor se reinicia automáticamente a menos que se detenga manualmente
-   Los logs se mantienen dentro del contenedor
-   La configuración SSL incluye headers de seguridad modernos
