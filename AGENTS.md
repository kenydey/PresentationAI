# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

PresentationAI is a Python-native AI presentation generator built on FastAPI + NiceGUI. The actual source code lives in the `PresentationAI/` directory (cloned from [presenton/presenton](https://github.com/presenton/presenton)). The main repo only contains `README.md` and a broken submodule reference — you must clone the upstream repo into `PresentationAI/` if it's not present.

### Core Service: FastAPI Backend

- **Location**: `PresentationAI/servers/fastapi/`
- **Runtime**: Python 3.11, managed by `uv`
- **Start command**: `cd PresentationAI/servers/fastapi && uv run python server.py --port 8000 --reload true`
- **Required env vars for dev**:
  - `APP_DATA_DIRECTORY=/tmp/app_data`
  - `TEMP_DIRECTORY=/tmp/presenton`
  - `DATABASE_URL=sqlite+aiosqlite:////tmp/app_data/fastapi.db`
  - `DISABLE_ANONYMOUS_TRACKING=true`
  - `DISABLE_IMAGE_GENERATION=true` (unless testing image generation with API keys)
- **Critical**: The `container_db_url` in `services/database.py` is hardcoded to `/app/container.db`. You must `sudo mkdir -p /app && sudo chmod 777 /app` before running the server.
- **API docs**: `http://localhost:8000/docs`
- **UI**: The project uses NiceGUI mounted on FastAPI, but the NiceGUI UI routes are not active in the current upstream code without additional setup. The FastAPI REST API is fully functional.

### Running Tests

```bash
cd PresentationAI/servers/fastapi
mkdir -p debug
APP_DATA_DIRECTORY=/tmp/app_data TEMP_DIRECTORY=/tmp/presenton \
  DATABASE_URL="sqlite+aiosqlite:////tmp/app_data/fastapi.db" \
  DISABLE_ANONYMOUS_TRACKING=true DISABLE_IMAGE_GENERATION=true \
  uv run python -m pytest tests/test_pptx_creator.py tests/test_pptx_slides_processing.py -v
```

- `test_mcp_server.py` requires `app_mcp` module which is not yet in the repo
- `test_gemini_schema_support.py` and `test_openai_schema_support.py` have import issues with current code
- `test_slide_to_html.py` tries to import `app` from `server.py` which doesn't export it
- `test_pptx_slides_processing::test_pptx_slides_processing` may fail due to LibreOffice conversion issues
- No linter is configured in the project

### Gotchas

- The first server startup downloads ~80MB of ChromaDB ONNX models — this is normal and takes a few seconds.
- LLM-dependent features (outline generation, presentation content generation) require `OPENAI_API_KEY` or equivalent provider keys configured via the settings API or environment.
- The project has no `.gitmodules` file despite having a submodule entry — the `PresentationAI` directory must be populated manually by cloning `presenton/presenton`.
