#!/bin/bash
set -e

# Start Nginx in background
nginx

# Start FastAPI + NiceGUI
cd /app/servers/fastapi
exec uv run python server.py --port 8000 --reload false
