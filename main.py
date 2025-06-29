from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from util import get_chart

app = FastAPI(title="Astrology API", version="1.0.0")

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return FileResponse("index.html")

@app.get("/health")
async def health_check():
    """Endpoint para health check del contenedor"""
    return {"status": "healthy", "service": "astrology-api"}

@app.get("/status")
async def status():
    """Endpoint para verificar el estado de la API"""
    return {
        "status": "running",
        "service": "astrology-api",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "carta": "/carta",
            "root": "/"
        }
    }

@app.get("/carta")
def carta(
    anio: int = Query(..., ge=1500),
    mes: int = Query(..., ge=1, le=12),
    dia: int = Query(..., ge=1, le=31),
    hora: int = 12,
    minuto: int = 0,
    tz: int = 0,
    lat: str = Query("0.0"),
    lon: str = Query("0.0")
):
    # Convertir strings a float, manejando comas y puntos
    try:
        lat_float = float(lat.replace(',', '.'))
        lon_float = float(lon.replace(',', '.'))
    except ValueError:
        lat_float = 0.0
        lon_float = 0.0
    
    return get_chart(anio, mes, dia, hora, minuto, 0, tz, lat_float, lon_float)
