# Despliegue con Docker - API de Astrología

Este proyecto incluye configuración completa para desplegar la aplicación de astrología usando Docker.

## Requisitos Previos

-   Docker instalado en tu sistema
-   Docker Compose (incluido con Docker Desktop)

## Opciones de Despliegue

### Opción 1: Usando Docker Compose (Recomendado)

1. **Construir y ejecutar la aplicación:**

    ```bash
    docker-compose up --build
    ```

2. **Ejecutar en segundo plano:**

    ```bash
    docker-compose up -d --build
    ```

3. **Detener la aplicación:**
    ```bash
    docker-compose down
    ```

### Opción 2: Usando Docker directamente

1. **Construir la imagen:**

    ```bash
    docker build -t astrology-api .
    ```

2. **Ejecutar el contenedor:**

    ```bash
    docker run -p 8000:8000 astrology-api
    ```

3. **Ejecutar en segundo plano:**
    ```bash
    docker run -d -p 8000:8000 --name astrology-api astrology-api
    ```

### Opción 3: Usando la imagen desde Docker Hub

La imagen está disponible en Docker Hub: `sergioscardigno82/astrology-api`

```bash
# Descargar y ejecutar la imagen
docker run -p 8000:8000 sergioscardigno82/astrology-api:latest

# O usar una versión específica
docker run -p 8000:8000 sergioscardigno82/astrology-api:v1.0.0
```

## Publicar en Docker Hub

### Paso 1: Loguearse en Docker Hub

```bash
docker login
# Ingresa tu usuario y contraseña de Docker Hub
```

### Paso 2: Usar el script automatizado (Recomendado)

```bash
# Dar permisos de ejecución al script
chmod +x publish-to-dockerhub.sh

# Publicar versión latest
./publish-to-dockerhub.sh

# Publicar versión específica
./publish-to-dockerhub.sh v1.0.0
```

### Paso 3: Publicar manualmente

```bash
# Construir la imagen
docker build -t astrology-api .

# Etiquetar para Docker Hub
docker tag astrology-api sergioscardigno82/astrology-api:latest
docker tag astrology-api sergioscardigno82/astrology-api:v1.0.0

# Subir a Docker Hub
docker push sergioscardigno82/astrology-api:latest
docker push sergioscardigno82/astrology-api:v1.0.0
```

## Verificación del Despliegue

Una vez desplegada, puedes verificar que la aplicación funciona correctamente:

-   **Interfaz web:** http://localhost:8000
-   **Health check:** http://localhost:8000/health
-   **Status API:** http://localhost:8000/status
-   **API de carta astral:** http://localhost:8000/carta?anio=1990&mes=1&dia=1

## Variables de Entorno

La aplicación utiliza las siguientes variables de entorno:

-   `EPH_PATH`: Ruta a los archivos de efemérides (por defecto: `/app/ephe`)
-   `PYTHONUNBUFFERED`: Configuración de Python para logs en tiempo real
-   `PYTHONDONTWRITEBYTECODE`: Evita la generación de archivos .pyc

## Características del Dockerfile

-   **Imagen base:** Python 3.11-slim (optimizada para tamaño)
-   **Seguridad:** Usuario no-root para ejecutar la aplicación
-   **Optimización:** Aprovecha la caché de Docker para dependencias
-   **Dependencias:** Incluye compiladores necesarios para Swiss Ephemeris
-   **Health check:** Verificación automática del estado de la aplicación

## Logs y Monitoreo

Para ver los logs de la aplicación:

```bash
# Con Docker Compose
docker-compose logs -f

# Con Docker directamente
docker logs -f astrology-api
```

## Troubleshooting

### Problema: Error al compilar Swiss Ephemeris

**Solución:** El Dockerfile ya incluye los compiladores necesarios (gcc, g++, make).

### Problema: No encuentra archivos de efemérides

**Solución:** Verifica que la carpeta `ephe/` esté presente en el directorio del proyecto.

### Problema: Puerto 8000 ocupado

**Solución:** Cambia el puerto en `docker-compose.yml` o usa otro puerto:

```bash
docker run -p 8080:8000 astrology-api
```

### Problema: Error al subir a Docker Hub

**Solución:** Verifica que estés logueado con `docker login` y que tengas permisos para el repositorio.

## Producción

Para despliegue en producción, considera:

1. **Variables de entorno:** Usar un archivo `.env` para configuraciones sensibles
2. **Reverse proxy:** Usar nginx o similar para SSL y balanceo de carga
3. **Monitoreo:** Implementar logging estructurado y métricas
4. **Backup:** Configurar backup de los archivos de efemérides
