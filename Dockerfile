# PresentationAI Docker — FastAPI + NiceGUI (no Next.js)
# Build:  docker build -t presenton .
# Run:    docker run -p 5000:80 -v ./app_data:/app_data presenton

FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    libreoffice \
    poppler-utils \
    ffmpeg \
    fontconfig \
    fonts-noto fonts-dejavu fonts-liberation fonts-freefont-ttf fonts-roboto fonts-noto-core \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy FastAPI application
COPY servers/fastapi/ /app/servers/fastapi/

# Install Python dependencies
WORKDIR /app/servers/fastapi
RUN uv sync --no-dev

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy custom fonts if any
COPY servers/fastapi/fonts/ /usr/share/fonts/ 2>/dev/null || true
RUN fc-cache -fv 2>/dev/null || true

# Create data directories
RUN mkdir -p /app_data/exports /app_data/images /app_data/uploads /app_data/fonts /app/container_db /tmp/presenton

# Environment
ENV APP_DATA_DIRECTORY=/app_data \
    TEMP_DIRECTORY=/tmp/presenton \
    DATABASE_URL=sqlite+aiosqlite:////app_data/presenton.db \
    USER_CONFIG_PATH=/app_data/userConfig.json \
    CAN_CHANGE_KEYS=true \
    DISABLE_ANONYMOUS_TRACKING=true \
    PYTHONUNBUFFERED=1

EXPOSE 80

# Start Nginx + FastAPI
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

CMD ["/app/docker-entrypoint.sh"]
