# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

PresentationAI (Presenton) is an open-source AI presentation generator. The project is a full-stack application:
- **FastAPI backend**: `servers/fastapi/` — Python 3.11, managed by `uv`
- **Next.js frontend**: `servers/nextjs/` — React/Next.js 14, managed by `npm`
- **Electron desktop**: root-level `app/`, `forge.config.js` (optional, not needed for web dev)

The recommended local dev entry point is `node start-local.js` (or run each server separately).

### Starting Services

#### FastAPI Backend (port 8000)
```bash
cd servers/fastapi
APP_DATA_DIRECTORY=/tmp/app_data TEMP_DIRECTORY=/tmp/presenton \
  DATABASE_URL="sqlite+aiosqlite:////tmp/app_data/fastapi.db" \
  DISABLE_ANONYMOUS_TRACKING=true DISABLE_IMAGE_GENERATION=true \
  uv run python server.py --port 8000 --reload true
```

**Pre-requisites**:
- `sudo mkdir -p /app && sudo chmod 777 /app` — the `container_db_url` in `services/database.py` is hardcoded to `/app/container.db`
- `mkdir -p /tmp/app_data /tmp/presenton`

**API docs**: http://localhost:8000/docs

#### Next.js Frontend (port 5000)
```bash
cd servers/nextjs
FASTAPI_URL=http://127.0.0.1:8000 npx next dev -p 5000
```

**UI**: http://localhost:5000 — Shows the Presenton settings/upload page. The Next.js `next.config.mjs` has rewrites that proxy `/api/v1/*` to the FastAPI backend.

### Running Tests

```bash
cd servers/fastapi
mkdir -p debug
APP_DATA_DIRECTORY=/tmp/app_data TEMP_DIRECTORY=/tmp/presenton \
  DATABASE_URL="sqlite+aiosqlite:////tmp/app_data/fastapi.db" \
  DISABLE_ANONYMOUS_TRACKING=true DISABLE_IMAGE_GENERATION=true \
  uv run python -m pytest tests/test_pptx_creator.py tests/test_pptx_slides_processing.py -v
```

- Several test files have import errors (`test_mcp_server.py`, `test_gemini_schema_support.py`, `test_slide_to_html.py`) — these are pre-existing upstream issues
- `test_pptx_slides_processing::test_pptx_slides_processing` may fail due to LibreOffice conversion

### Linting

```bash
cd servers/nextjs && npx next lint
```

Requires `.eslintrc.json` with `{"extends":"next/core-web-vitals"}` and `eslint@8` + `eslint-config-next@14` installed. Only warnings (no errors) are expected.

The FastAPI backend has no linter configured.

### Gotchas

- The first FastAPI startup downloads ~80MB of ChromaDB ONNX models — this is normal.
- LLM-dependent features require `OPENAI_API_KEY` or equivalent provider keys (configurable in the UI settings page or via environment).
- The user's `origin/main` push contained pre-existing merge conflict markers in ~48 Next.js files. These were resolved by keeping the HEAD (upstream presenton) content. If re-merging, be aware of this.
- The `pyproject.toml` in `servers/fastapi/` includes `nicegui>=2.0.0` — NiceGUI is available but its UI routes are not currently wired in the server.
- Colors in `PptxPresentationModel` must be 6-hex-digit strings without `#` prefix (e.g., `"ffffff"` not `"#ffffff"`).
