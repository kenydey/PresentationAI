# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .


# Install build dependencies and pip packages in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    poppler-utils \
    ffmpeg \
    fonts-noto \
    fonts-dejavu \
    fonts-liberation \
    fonts-freefont-ttf \
    fonts-roboto \
    fonts-noto-core \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt 

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    poppler-utils \
    ffmpeg \
    fonts-noto \
    fonts-dejavu \
    fonts-liberation \
    fonts-freefont-ttf \
    fonts-roboto \
    fonts-noto-core \
    && rm -rf /var/lib/apt/lists/*


# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code and fonts
COPY . /app
COPY ./fonts /usr/share/fonts/
RUN fc-cache -fv

CMD ["python", "server.py"]