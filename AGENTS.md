# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

PresentationAI (Presenton) is an open-source AI presentation generator. Architecture:
- **FastAPI backend + NiceGUI frontend**: `servers/fastapi/` — Python 3.11, managed by `uv`
- **Electron desktop** (optional): root-level `app/`, `forge.config.js`

Next.js has been fully removed. All frontend is served by NiceGUI mounted at `/ui` on the FastAPI server.

### Starting the Server

```bash
cd servers/fastapi
APP_DATA_DIRECTORY=/tmp/app_data TEMP_DIRECTORY=/tmp/presenton \
  DATABASE_URL="sqlite+aiosqlite:////tmp/app_data/fastapi.db" \
  DISABLE_ANONYMOUS_TRACKING=true CAN_CHANGE_KEYS=true \
  USER_CONFIG_PATH=/tmp/app_data/userConfig.json \
  uv run python server.py --port 8000 --reload true
```

Or use: `node start-local.js` (handles env setup automatically)

**Pre-requisites**:
- `sudo mkdir -p /app && sudo chmod 777 /app`
- `mkdir -p /tmp/app_data /tmp/presenton`

**URLs**:
- UI: http://localhost:8000/ui/
- API docs: http://localhost:8000/docs

### NiceGUI Pages (10 total, under /ui)

`/` 首页, `/dashboard` 仪表板, `/create` 创建演示, `/outline` 大纲编辑,
`/viewer` 演示查看, `/images` 图片管理, `/fonts` 字体管理,
`/templates` 模板管理, `/icons` 图标搜索, `/settings` 系统设置

Code: `servers/fastapi/nicegui_app/` — `pages/`, `layout.py`, `api_client.py`

### Template System

Templates are pre-extracted from the original TSX sources into `servers/fastapi/assets/template_registry.json` (8 groups, 120 layouts). The `GET /api/v1/ppt/layouts/{group}` endpoint serves layouts from this local registry — no external dependency.

To re-extract after modifying TSX templates: `uv run python scripts/extract_templates.py`

### Running Tests

```bash
cd servers/fastapi && mkdir -p debug
APP_DATA_DIRECTORY=/tmp/app_data TEMP_DIRECTORY=/tmp/presenton \
  DATABASE_URL="sqlite+aiosqlite:////tmp/app_data/fastapi.db" \
  DISABLE_ANONYMOUS_TRACKING=true DISABLE_IMAGE_GENERATION=true \
  uv run python -m pytest tests/test_pptx_creator.py tests/test_pptx_slides_processing.py -v
```

### Gotchas

- First startup downloads ~80MB ChromaDB ONNX models
- LLM features require API keys (configure via `/ui/settings` or environment)
- `container_db_url` in `services/database.py` is hardcoded to `/app/container.db`
- Colors in PptxPresentationModel: 6-hex digits without `#` prefix
- PPTX export uses pure Python converter (`utils/slide_to_pptx_converter.py`); PDF export requires LibreOffice
