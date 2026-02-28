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

#### NiceGUI Frontend (mounted at /ui)

NiceGUI is mounted directly on the FastAPI server — no separate process needed. Access at http://localhost:8000/ui/

**Pages** (10 total, all under /ui):
- `/` 首页, `/dashboard` 仪表板, `/create` 创建演示, `/outline` 大纲编辑
- `/viewer` 演示查看, `/images` 图片管理, `/fonts` 字体管理
- `/templates` 模板管理, `/icons` 图标搜索, `/settings` 系统设置

**Code structure**: `servers/fastapi/nicegui_app/` — modular with `pages/`, `layout.py`, `api_client.py`

**Note**: The legacy Next.js frontend (`servers/nextjs/`) is still in the repo but no longer required.

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
