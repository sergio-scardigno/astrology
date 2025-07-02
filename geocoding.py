import requests
import time
import sqlite3
import json
import asyncio
from typing import Dict, List, Optional, Tuple

DB_PATH = 'data/geocoding_cache.db'
CACHE_DURATION_SECONDS = 30 * 24 * 60 * 60  # 30 días

class GeocodingService:
    """Servicio para geocodificación usando Nominatim API con caché local."""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {
            'User-Agent': 'AstrologyAPI/1.0 (https://github.com/sergioscardigno82/astrology-api)'
        }
        self.db_conn = self._init_db()
        self.db_lock = asyncio.Lock()

    def _init_db(self):
        """Inicializa la base de datos de caché."""
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        # Cache para search_cities
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_search_cache (
                query TEXT PRIMARY KEY,
                results TEXT,
                timestamp REAL
            )
        ''')
        # Cache para get_coordinates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coordinates_cache (
                query TEXT PRIMARY KEY,
                coordinates TEXT,
                timestamp REAL
            )
        ''')
        conn.commit()
        return conn

    def _get_from_cache(self, table: str, query: str) -> Optional[any]:
        """Obtiene un resultado desde la caché si es válido."""
        cursor = self.db_conn.cursor()
        
        column_name = "coordinates" if table == "coordinates_cache" else "results"
        
        cursor.execute(f"SELECT {column_name}, timestamp FROM {table} WHERE query = ?", (query,))
        row = cursor.fetchone()
        if row:
            data, timestamp = row
            if time.time() - timestamp < CACHE_DURATION_SECONDS:
                return json.loads(data)
        return None

    async def _set_to_cache(self, table: str, query: str, results: any):
        """Guarda un resultado en la caché de forma segura usando un Lock."""
        async with self.db_lock:
            await asyncio.to_thread(self._write_db_sync, table, query, results)
    
    def _write_db_sync(self, table: str, query: str, data: any):
        """Función síncrona para escribir en la BD, para ser usada con to_thread."""
        cursor = self.db_conn.cursor()
        
        column_name = "coordinates" if table == "coordinates_cache" else "results"
        
        cursor.execute(
            f"INSERT OR REPLACE INTO {table} (query, {column_name}, timestamp) VALUES (?, ?, ?)",
            (query, json.dumps(data), time.time())
        )
        self.db_conn.commit()

    async def search_cities(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Buscar ciudades por nombre, usando caché.
        """
        # Normalizar el query para la caché
        cache_query = query.lower().strip()
        
        # Consultar caché
        cached_results = self._get_from_cache('city_search_cache', cache_query)
        if cached_results is not None:
            return cached_results

        # Si no está en caché, buscar en la API
        try:
            params = {
                'q': query,
                'format': 'json',
                'limit': limit,
                'addressdetails': 1,
                'countrycodes': '',
                'featuretype': 'city'
            }
            
            # Ejecutar la llamada bloqueante en un hilo separado
            response = await asyncio.to_thread(
                requests.get,
                f"{self.base_url}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            results = response.json()
            cities = []
            
            for result in results:
                address = result.get('address', {})
                city_info = {
                    'name': result.get('display_name', ''),
                    'lat': float(result.get('lat', 0)),
                    'lon': float(result.get('lon', 0)),
                    'city': address.get('city', address.get('town', address.get('village', ''))),
                    'state': address.get('state', ''),
                    'country': address.get('country', ''),
                    'country_code': address.get('country_code', ''),
                    'type': result.get('type', ''),
                    'importance': result.get('importance', 0)
                }
                cities.append(city_info)
            
            cities.sort(key=lambda x: x['importance'], reverse=True)
            
            # Guardar en caché
            await self._set_to_cache('city_search_cache', cache_query, cities)
            
            return cities
            
        except requests.RequestException as e:
            print(f"Error en búsqueda de ciudades: {e}")
            return []

    async def get_coordinates(self, city: str, country: str = "") -> Optional[Tuple[float, float]]:
        """
        Obtener coordenadas de una ciudad, usando caché.
        """
        query = f"{city.lower().strip()},{country.lower().strip()}"
        
        # Consultar caché
        cached_coords = self._get_from_cache('coordinates_cache', query)
        if cached_coords is not None:
            return tuple(cached_coords)

        # Si no está en caché, buscar en la API
        try:
            api_query = f"{city}, {country}" if country else city
            params = {
                'q': api_query,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            # Ejecutar la llamada bloqueante en un hilo separado
            response = await asyncio.to_thread(
                requests.get,
                f"{self.base_url}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            results = response.json()
            if results:
                result = results[0]
                coordinates = (
                    float(result.get('lat', 0)),
                    float(result.get('lon', 0))
                )
                # Guardar en caché
                await self._set_to_cache('coordinates_cache', query, coordinates)
                return coordinates
            
            return None
            
        except requests.RequestException as e:
            print(f"Error obteniendo coordenadas: {e}")
            return None
    
    def get_city_info(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Obtener información de una ciudad por coordenadas (reverse geocoding)
        
        Args:
            lat: Latitud
            lon: Longitud
            
        Returns:
            Información de la ciudad o None si no se encuentra
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1
            }
            
            response = requests.get(
                f"{self.base_url}/reverse",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            address = result.get('address', {})
            
            return {
                'display_name': result.get('display_name', ''),
                'city': address.get('city', address.get('town', address.get('village', ''))),
                'state': address.get('state', ''),
                'country': address.get('country', ''),
                'country_code': address.get('country_code', ''),
                'lat': lat,
                'lon': lon
            }
            
        except requests.RequestException as e:
            print(f"Error en reverse geocoding: {e}")
            return None

# Instancia global del servicio
geocoding_service = GeocodingService() 