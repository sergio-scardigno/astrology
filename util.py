import os
import swisseph as swe
from datetime import datetime, timezone, timedelta
from timezonefinder import TimezoneFinder
import pytz

EPH_PATH = os.getenv("EPH_PATH", "./ephe")
swe.set_ephe_path(EPH_PATH)

SIGNS = ["Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo",
         "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"]

ELEMENTOS = {
    "Aries": "Fuego", "Leo": "Fuego", "Sagitario": "Fuego",
    "Tauro": "Tierra", "Virgo": "Tierra", "Capricornio": "Tierra",
    "Géminis": "Aire", "Libra": "Aire", "Acuario": "Aire",
    "Cáncer": "Agua", "Escorpio": "Agua", "Piscis": "Agua"
}

CUALIDADES = {
    "Aries": "Cardinal", "Cáncer": "Cardinal", "Libra": "Cardinal", "Capricornio": "Cardinal",
    "Tauro": "Fijo", "Leo": "Fijo", "Escorpio": "Fijo", "Acuario": "Fijo",
    "Géminis": "Mutable", "Virgo": "Mutable", "Sagitario": "Mutable", "Piscis": "Mutable"
}

PLANETAS = {
    "sol": swe.SUN,
    "luna": swe.MOON,
    "mercurio": swe.MERCURY,
    "venus": swe.VENUS,
    "marte": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturno": swe.SATURN,
    "urano": swe.URANUS,
    "neptuno": swe.NEPTUNE,
    "pluton": swe.PLUTO
}

ASPECTOS = [
    (0, "conjunción", 8),
    (60, "sextil", 6),
    (90, "cuadratura", 8),
    (120, "trígono", 8),
    (180, "oposición", 8)
]

def _sign(deg):
    deg = deg % 360
    index = int(deg // 30)
    return SIGNS[index]

def get_sign_info(signo):
    return {
        "elemento": ELEMENTOS[signo],
        "cualidad": CUALIDADES[signo]
    }

def calcular_balance_elementos(planetas):
    """Calcula el balance de elementos basado en las posiciones planetarias"""
    elementos = {"Fuego": 0, "Tierra": 0, "Aire": 0, "Agua": 0}
    total_planetas = len(planetas)
    
    for planeta, info in planetas.items():
        signo = info["signo"]
        elemento = ELEMENTOS[signo]
        if elemento == "Fuego":
            elementos["Fuego"] += 1
        elif elemento == "Tierra":
            elementos["Tierra"] += 1
        elif elemento == "Aire":
            elementos["Aire"] += 1
        elif elemento == "Agua":
            elementos["Agua"] += 1
    
    # Calcular porcentajes
    balance = {}
    for elemento, cantidad in elementos.items():
        porcentaje = round((cantidad / total_planetas) * 100, 1)
        balance[elemento] = {
            "cantidad": cantidad,
            "porcentaje": porcentaje
        }
    
    # Determinar elemento dominante
    elemento_dominante = max(elementos.items(), key=lambda x: x[1])[0]
    
    # Determinar balance general
    max_cantidad = max(elementos.values())
    min_cantidad = min(elementos.values())
    diferencia = max_cantidad - min_cantidad
    
    if diferencia <= 1:
        balance_general = "Muy Balanceado"
    elif diferencia <= 2:
        balance_general = "Balanceado"
    elif diferencia <= 3:
        balance_general = "Poco Balanceado"
    else:
        balance_general = "Desbalanceado"
    
    return {
        "elementos": balance,
        "dominante": elemento_dominante,
        "balance_general": balance_general,
        "resumen": f"Elemento dominante: {elemento_dominante} ({balance[elemento_dominante]['porcentaje']}%) - {balance_general}"
    }

def get_chart(y, m, d, h=12, mi=0, s=0, tz=0, lat=0.0, lon=0.0):
    ut_hours = h + mi / 60 + s / 3600 - tz
    jd_ut = swe.julday(y, m, d, ut_hours)

    # Planetas
    planetas = {}
    posiciones = {}
    for nombre, id_planeta in PLANETAS.items():
        res = swe.calc_ut(jd_ut, id_planeta)
        grado = res[0][0]
        signo = _sign(grado)
        planetas[nombre] = {"signo": signo, "grado": round(grado, 4)}
        posiciones[nombre] = grado

    # Casas
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'P')
    casas = {}
    for i in range(12):
        grado = cusps[i]
        signo = _sign(grado)
        casas[str(i+1)] = {"grado": round(grado, 4), "signo": signo}

    # Ascendente (casa 1)
    asc_long = ascmc[0]
    asc_sign = _sign(asc_long)

    # Elemento y cualidad para Sol, Luna y Ascendente
    sol_sign = planetas["sol"]["signo"]
    luna_sign = planetas["luna"]["signo"]

    # Aspectos
    aspectos = []
    nombres = list(PLANETAS.keys())
    for i in range(len(nombres)):
        for j in range(i+1, len(nombres)):
            p1, p2 = nombres[i], nombres[j]
            g1, g2 = posiciones[p1], posiciones[p2]
            diff = abs(g1 - g2)
            diff = diff if diff <= 180 else 360 - diff
            for angulo, nombre_asp, orbe in ASPECTOS:
                if abs(diff - angulo) <= orbe:
                    aspectos.append({
                        "planeta1": p1,
                        "planeta2": p2,
                        "aspecto": nombre_asp,
                        "orbe": round(abs(diff - angulo), 2)
                    })

    # Calcular balance de elementos
    balance_elementos = calcular_balance_elementos(planetas)

    return {
        "planetas": planetas,
        "casas": casas,
        "ascendente": asc_sign,
        "sol_info": get_sign_info(sol_sign),
        "luna_info": get_sign_info(luna_sign),
        "ascendente_info": get_sign_info(asc_sign),
        "aspectos": aspectos,
        "balance_elementos": balance_elementos
    }

def get_timezone_offset(lat, lon, dt=None):
    """
    Dada una latitud, longitud y una fecha (datetime), devuelve el offset horario en horas.
    Si no se pasa fecha, usa la fecha y hora actual.
    """
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    if not timezone_str:
        return None
    tz = pytz.timezone(timezone_str)
    if dt is None:
        dt = datetime.utcnow()
    # Hacer que dt sea 'aware' en la zona horaria local
    if dt.tzinfo is None:
        dt = tz.localize(dt, is_dst=None)
    offset = dt.utcoffset()
    if offset is None:
        return None
    return offset.total_seconds() / 3600

