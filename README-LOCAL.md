# 🌟 Astrology API - Desarrollo Local

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

```bash
# En Windows (PowerShell)
./start-local.sh

# En Linux/Mac
chmod +x start-local.sh
./start-local.sh
```

### Opción 2: Docker Compose Manual

```bash
# Construir y ejecutar
docker-compose -f docker-compose.local.yml up --build -d

# Ver logs
docker-compose -f docker-compose.local.yml logs -f

# Detener
docker-compose -f docker-compose.local.yml down
```

### Opción 3: Docker Run Directo

```bash
# Construir imagen
docker build -t astrology-api .

# Ejecutar contenedor
docker run -d \
  --name astrology-local \
  -p 8000:8000 \
  -v ./ephe:/opt/swisseph/ephe:ro \
  -e EPH_PATH=/opt/swisseph/ephe \
  -e PYTHONPATH=/app \
  -e PYTHONUNBUFFERED=1 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  astrology-api
```

## 🌐 URLs de Acceso

Una vez ejecutado, accede a:

-   **Health Check:** http://localhost:8000/health
-   **Status:** http://localhost:8000/status
-   **Interfaz Principal:** http://localhost:8000/
-   **API Carta:** http://localhost:8000/carta?anio=1990&mes=1&dia=1&hora=12&minuto=0&tz=0&lat=40.4168&lon=-3.7038

## 📋 Comandos Útiles

### Ver logs en tiempo real:

```bash
docker-compose -f docker-compose.local.yml logs -f
```

### Detener el servicio:

```bash
docker-compose -f docker-compose.local.yml down
```

### Reiniciar el servicio:

```bash
docker-compose -f docker-compose.local.yml restart
```

### Verificar estado:

```bash
docker ps | grep astrology
```

### Probar endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/status
curl http://localhost:8000/
```

## 🔧 Troubleshooting

### Si el puerto 8000 está ocupado:

```bash
# Cambiar puerto en docker-compose.local.yml
ports:
  - '8001:8000'  # Usar puerto 8001 en lugar de 8000
```

### Si hay problemas de permisos:

```bash
# En Linux/Mac
sudo chown -R $USER:$USER ./ephe
```

### Si el contenedor no inicia:

```bash
# Ver logs detallados
docker-compose -f docker-compose.local.yml logs

# Reconstruir sin cache
docker-compose -f docker-compose.local.yml build --no-cache
```

## 📁 Estructura del Proyecto

```
astrology-ap/
├── main.py                 # Aplicación principal
├── util.py                 # Utilidades de astrología
├── index.html             # Interfaz web
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Configuración Docker
├── docker-compose.local.yml  # Configuración local
├── start-local.sh        # Script de inicio
├── ephe/                 # Archivos de efemérides
└── README-LOCAL.md       # Este archivo
```

## 🎯 Desarrollo

### Modificar código:

1. Edita los archivos Python/HTML
2. El contenedor se reconstruye automáticamente
3. Los cambios se reflejan inmediatamente

### Agregar dependencias:

1. Edita `requirements.txt`
2. Reconstruye: `docker-compose -f docker-compose.local.yml build`

### Debug:

```bash
# Ejecutar en modo interactivo
docker-compose -f docker-compose.local.yml run --rm astrology bash
```

## ✅ Verificación

El servicio está funcionando correctamente si:

1. ✅ `curl http://localhost:8000/health` devuelve `{"status":"healthy","service":"astrology-api"}`
2. ✅ `curl http://localhost:8000/status` devuelve información del servicio
3. ✅ `curl http://localhost:8000/` devuelve el HTML de la interfaz
4. ✅ `docker ps` muestra el contenedor `astrology-local` corriendo
