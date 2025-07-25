# Astrology API

Aplicación web de astrología que permite calcular cartas natales, posiciones planetarias, cúspides de casas y aspectos, con soporte para geocodificación y despliegue en Docker.

## Características

- Calcula posiciones planetarias y cúspides de casas (Placidus).
- Determina el ascendente, aspectos y balance de elementos.
- Geocodificación automática de ciudades y cálculo de zona horaria según lugar y fecha.
- Interfaz web moderna y API REST.
- Despliegue sencillo con Docker y Docker Compose.

## Instalación local

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/astrology-api.git
    cd astrology-api
    ```
2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3. Ejecuta la aplicación:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
4. Accede a la app en [http://localhost:8000](http://localhost:8000)

## Uso con Docker

### Docker Compose (recomendado)

```bash
docker-compose up --build
```

- Accede a la app en [http://localhost:8000](http://localhost:8000)

### Docker manual

```bash
docker build -t astrology-api .
docker run -p 8000:8000 astrology-api
```

### Imagen en Docker Hub

```bash
docker run -p 8000:8000 sergioscardigno82/astrology-api:latest
```

## Endpoints principales

- `/` — Interfaz web
- `/carta` — Calcula la carta astral (GET, requiere parámetros de fecha, hora, lugar)
- `/buscar_ciudades` — Busca ciudades por nombre
- `/coordenadas` — Devuelve coordenadas de una ciudad
- `/timezone` — Devuelve el offset horario para lat/lon y fecha
- `/health` — Health check
- `/status` — Estado de la API

### Ejemplo de consulta a `/carta`

```
/carta?anio=1982&mes=6&dia=6&hora=6&minuto=30&tz=-3&lat=-35.5667&lon=-58.0167
```

## Variables de entorno

- `EPH_PATH`: Ruta a los archivos de efemérides (por defecto: `/app/ephe`)

## Dependencias principales

- fastapi
- uvicorn[standard]
- pyswisseph
- python-dotenv
- requests
- timezonefinder
- pytz

## Notas sobre la zona horaria y la hora local

- **La hora de nacimiento debe ser la hora civil local** (la que figura en la partida de nacimiento).
- La zona horaria se calcula automáticamente según la ciudad/latitud y la fecha, pero puedes ajustarla manualmente si lo deseas.
- La app muestra la conversión a UTC para máxima transparencia.

## Créditos y Licencia

Desarrollado por Sergio Scardigno y colaboradores. Licencia MIT.