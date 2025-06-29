# ────────────────────────── Dockerfile para Producción ──────────────────────────
FROM python:3.12-slim

# Crear usuario no-root para seguridad
RUN groupadd -r astrology && useradd -r -g astrology astrology

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        pkg-config \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para efemérides y cambiar permisos
RUN mkdir -p /opt/swisseph/ephe && \
    chown -R astrology:astrology /app /opt/swisseph

# Cambiar al usuario no-root
USER astrology

# Variables de entorno
ENV EPH_PATH=/opt/swisseph/ephe
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Exponer puerto
EXPOSE 8000

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]


