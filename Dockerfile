# ────────────────────────── Dockerfile para Producción con HTTPS ──────────────────────────
FROM python:3.12-slim

# Crear usuario no-root para seguridad
RUN groupadd -r astrology && useradd -r -g astrology astrology

# Instalar dependencias del sistema incluyendo nginx y openssl
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        pkg-config \
        curl \
        nginx \
        openssl \
        supervisor \
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

# Crear directorios para nginx y SSL
RUN mkdir -p /etc/nginx/ssl /var/log/nginx /var/cache/nginx && \
    chown -R astrology:astrology /etc/nginx /var/log/nginx /var/cache/nginx

# Generar certificado SSL auto-firmado
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=ES/ST=Madrid/L=Madrid/O=Astrology/OU=IT/CN=localhost" && \
    chown astrology:astrology /etc/nginx/ssl/*

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Cambiar al usuario no-root
USER astrology

# Variables de entorno
ENV EPH_PATH=/opt/swisseph/ephe
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Exponer puertos HTTP y HTTPS
EXPOSE 80 443 8000

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para ejecutar con supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


