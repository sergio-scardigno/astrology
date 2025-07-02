from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from util import get_chart, get_timezone_offset
from geocoding import geocoding_service
from typing import Optional
import asyncio

app = FastAPI(title="Astrology API", version="1.0.0")

# Lista de ciudades para precargar en la caché al inicio
CITIES_TO_PRELOAD = [
    # Argentina
    "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata", "Gualeguaychú", "Adolfo Gonzales Chaves",
    # Mundo
    "Madrid", "Mexico City", "New York", "London", "Paris", "Tokyo", "Sao Paulo"
]

async def preload_cities_cache():
    """Precarga la caché de ciudades en segundo plano."""
    print("🚀 Iniciando precarga de caché de ciudades...")
    await asyncio.sleep(5) # Esperar un poco a que todo arranque
    for city in CITIES_TO_PRELOAD:
        try:
            print(f" caching... {city}")
            await geocoding_service.search_cities(city)
            await asyncio.sleep(2)  # Pausa para no sobrecargar la API de Nominatim
        except Exception as e:
            print(f"❌ Error cacheando {city}: {e}")
    print("✅ Precarga de caché de ciudades completada.")


@app.on_event("startup")
async def startup_event():
    """Al iniciar la app, crea la tarea de precarga en segundo plano."""
    asyncio.create_task(preload_cities_cache())

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
            "buscar_ciudades": "/buscar_ciudades",
            "coordenadas": "/coordenadas",
            "root": "/"
        }
    }

@app.get("/buscar_ciudades")
async def buscar_ciudades(q: str = Query(..., min_length=2, description="Término de búsqueda")):
    """
    Buscar ciudades por nombre
    
    Args:
        q: Término de búsqueda (mínimo 2 caracteres)
        
    Returns:
        Lista de ciudades encontradas
    """
    ciudades = await geocoding_service.search_cities(q, limit=15)
    return {
        "query": q,
        "results": ciudades,
        "total": len(ciudades)
    }

@app.get("/coordenadas")
async def obtener_coordenadas(
    ciudad: str = Query(..., description="Nombre de la ciudad"),
    pais: str = Query("", description="Nombre del país (opcional)")
):
    """
    Obtener coordenadas de una ciudad específica
    
    Args:
        ciudad: Nombre de la ciudad
        pais: Nombre del país (opcional)
        
    Returns:
        Coordenadas de la ciudad
    """
    coords = await geocoding_service.get_coordinates(ciudad, pais)
    if coords:
        return {
            "ciudad": ciudad,
            "pais": pais,
            "latitud": coords[0],
            "longitud": coords[1],
            "encontrado": True
        }
    else:
        return {
            "ciudad": ciudad,
            "pais": pais,
            "encontrado": False,
            "error": "Ciudad no encontrada"
        }

@app.get("/carta")
async def carta(
    anio: int = Query(..., ge=1500),
    mes: int = Query(..., ge=1, le=12),
    dia: int = Query(..., ge=1, le=31),
    hora: int = 12,
    minuto: int = 0,
    tz: Optional[float] = None,
    lat: Optional[str] = Query(None, description="Latitud (opcional si se usa ciudad)"),
    lon: Optional[str] = Query(None, description="Longitud (opcional si se usa ciudad)"),
    ciudad: Optional[str] = Query(None, description="Nombre de la ciudad (opcional)"),
    pais: Optional[str] = Query(None, description="Nombre del país (opcional)")
):
    """
    Generar carta astral
    
    Args:
        anio: Año de nacimiento
        mes: Mes de nacimiento
        dia: Día de nacimiento
        hora: Hora de nacimiento (opcional, default: 12)
        minuto: Minuto de nacimiento (opcional, default: 0)
        tz: Zona horaria (opcional, default: 0)
        lat: Latitud (opcional si se usa ciudad)
        lon: Longitud (opcional si se usa ciudad)
        ciudad: Nombre de la ciudad (opcional)
        pais: Nombre del país (opcional)
    """
    lat_float = 0.0
    lon_float = 0.0
    ciudad_info = None
    tz_offset = tz
    
    # Si se proporciona ciudad, obtener coordenadas
    if ciudad:
        coords = await geocoding_service.get_coordinates(ciudad, pais or "")
        if coords:
            lat_float, lon_float = coords
            ciudad_info = geocoding_service.get_city_info(lat_float, lon_float)
            # Si no se especificó tz, obtenerla automáticamente
            if tz is None:
                from datetime import datetime
                tz_offset = get_timezone_offset(lat_float, lon_float, datetime(anio, mes, dia, hora, minuto))
                if tz_offset is None:
                    tz_offset = -3  # Default Buenos Aires
        else:
            return {
                "error": f"No se pudo encontrar la ciudad: {ciudad}",
                "sugerencia": "Verifica el nombre de la ciudad o usa coordenadas directamente"
            }
    else:
        # Usar coordenadas proporcionadas
        if lat and lon:
            try:
                lat_float = float(lat.replace(',', '.'))
                lon_float = float(lon.replace(',', '.'))
                # Si no se especificó tz, obtenerla automáticamente
                if tz is None:
                    from datetime import datetime
                    tz_offset = get_timezone_offset(lat_float, lon_float, datetime(anio, mes, dia, hora, minuto))
                    if tz_offset is None:
                        tz_offset = -3  # Default Buenos Aires
            except ValueError:
                return {
                    "error": "Coordenadas inválidas",
                    "sugerencia": "Proporciona coordenadas válidas o usa el parámetro 'ciudad'"
                }
        else:
            # Si no hay ciudad ni coordenadas, usar Buenos Aires por defecto
            lat_float = -34.6037
            lon_float = -58.3816
            ciudad_info = {"city": "Buenos Aires", "country": "Argentina", "state": "CABA", "display_name": "Buenos Aires, Argentina"}
            if tz is None:
                tz_offset = -3
    
    # Generar carta astral
    carta_result = get_chart(anio, mes, dia, hora, minuto, 0, tz_offset, lat_float, lon_float)
    
    # Agregar información de la ciudad si está disponible
    if ciudad_info:
        carta_result["ubicacion"] = {
            "ciudad": ciudad_info.get("city", ciudad),
            "pais": ciudad_info.get("country", pais or ""),
            "estado": ciudad_info.get("state", ""),
            "latitud": lat_float,
            "longitud": lon_float,
            "display_name": ciudad_info.get("display_name", "")
        }
    else:
        carta_result["ubicacion"] = {
            "latitud": lat_float,
            "longitud": lon_float
        }
    
    carta_result["zona_horaria"] = tz_offset
    return carta_result
