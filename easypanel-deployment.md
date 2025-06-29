# 🚀 Despliegue en EasyPanel - Solo Imagen Docker Hub

## Configuración para EasyPanel

### 1. Configuración Básica del Servicio

**Imagen Docker:**

```
sergioscardigno82/astrology-api:latest
```

**Puerto del contenedor:** `8000`

**Puerto externo:** El que te asigne EasyPanel (ej: 3000, 8080, etc.)

### 2. Variables de Entorno

Agrega estas variables de entorno en EasyPanel:

```
EPH_PATH=/opt/swisseph/ephe
PYTHONPATH=/app
PYTHONUNBUFFERED=1
HOST=0.0.0.0
PORT=8000
```

### 3. Volúmenes (Opcional)

Si necesitas montar las efemérides, agrega este volumen:

-   **Host path:** `/path/to/your/ephe` (ruta en tu servidor)
-   **Container path:** `/opt/swisseph/ephe`
-   **Read only:** ✅

### 4. Health Check

**Endpoint:** `/health`
**Intervalo:** 30s
**Timeout:** 10s
**Retries:** 3
**Start period:** 40s

### 5. Pasos en EasyPanel

1. **Crear nuevo servicio**
2. **Seleccionar "Docker Image"**
3. **Imagen:** `sergioscardigno82/astrology-api:latest`
4. **Puerto interno:** `8000`
5. **Puerto externo:** El que te asigne EasyPanel
6. **Agregar variables de entorno** (ver punto 2)
7. **Configurar health check** (ver punto 4)
8. **Deploy**

### 6. Verificación

Una vez desplegado, verifica estos endpoints:

-   `https://tu-dominio.easypanel.host/health` - Debe devolver: `{"status":"healthy","service":"astrology-api"}`
-   `https://tu-dominio.easypanel.host/status` - Debe devolver información del servicio
-   `https://tu-dominio.easypanel.host/` - Debe mostrar la interfaz principal

### 7. Troubleshooting

**Si el servicio no responde:**

1. **Verificar logs en EasyPanel**
2. **Comprobar que el puerto esté correctamente mapeado**
3. **Verificar que las variables de entorno estén configuradas**
4. **Revisar que el health check esté funcionando**

**Comandos útiles para debug:**

```bash
# Verificar que la imagen se descargó correctamente
docker images | grep astrology-api

# Verificar logs del contenedor
docker logs <container-name>

# Verificar que el puerto esté abierto
netstat -tulpn | grep 8000
```

### 8. Configuración de Dominio

Si tienes un dominio personalizado:

1. **Configurar DNS** para apuntar a tu servidor
2. **En EasyPanel**, agregar el dominio al servicio
3. **Configurar SSL** si es necesario

### 9. Ejemplo de Configuración Completa

```
Servicio: Astrology API
Imagen: sergioscardigno82/astrology-api:latest
Puerto interno: 8000
Puerto externo: 3000 (o el que asigne EasyPanel)

Variables de entorno:
- EPH_PATH=/opt/swisseph/ephe
- PYTHONPATH=/app
- PYTHONUNBUFFERED=1
- HOST=0.0.0.0
- PORT=8000

Health Check:
- URL: /health
- Intervalo: 30s
- Timeout: 10s
- Retries: 3
- Start period: 40s
```

### 10. URLs de Prueba

Una vez desplegado, prueba estas URLs:

```
https://tu-dominio.easypanel.host/health
https://tu-dominio.easypanel.host/status
https://tu-dominio.easypanel.host/
https://tu-dominio.easypanel.host/carta?anio=1990&mes=1&dia=1&hora=12&minuto=0&tz=0&lat=40.4168&lon=-3.7038
```
