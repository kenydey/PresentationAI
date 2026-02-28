# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

PresentationAI is a Python-native AI presentation generator built on FastAPI + NiceGUI. The repo has two copies of the backend: `servers/fastapi/` (primary, with NiceGUI and additional deps) and `PresentationAI/servers/fastapi/` (upstream snapshot from [presenton/presenton](https://github.com/presenton/presenton)). Use `servers/fastapi/` for development. The Next.js frontend at `servers/nextjs/` is legacy (README says "no longer used") but its code is still in the repo.

### Core Service: FastAPI Backend

- **Location**: `servers/fastapi/`
- **Runtime**: Python 3.11, managed by `uv`
- **Start command**: `cd servers/fastapi && uv run python server.py --port 8000 --reload true`
- **Required env vars for dev**:
  - `APP_DATA_DIRECTORY=/tmp/app_data`
  - `TEMP_DIRECTORY=/tmp/presenton`
  - `DATABASE_URL=sqlite+aiosqlite:////tmp/app_data/fastapi.db`
  - `DISABLE_ANONYMOUS_TRACKING=true`
  - `DISABLE_IMAGE_GENERATION=true` (unless testing image generation with API keys)
- **Critical**: The `container_db_url` in `services/database.py` is hardcoded to `/app/container.db`. You must `sudo mkdir -p /app && sudo chmod 777 /app` before running the server.
- **API docs**: `http://localhost:8000/docs`
- **UI**: The project uses NiceGUI mounted on FastAPI, but NiceGUI UI routes are not present in the current upstream code. The FastAPI REST API is fully functional.
- **Hello world test**: Use `POST /api/v1/ppt/presentation/create` with `{"content":"test","n_slides":3,"language":"English"}` to create a presentation record, then `GET /api/v1/ppt/presentation/{id}` to retrieve it. The `/all` endpoint requires slides to exist (it does a JOIN), so newly created presentations without LLM-generated slides won't appear there.
- **PPTX generation** (without LLM): Import `PptxPresentationCreator` from `services.pptx_presentation_creator` with `PptxPresentationModel` from `models.pptx_models` to programmatically create PPTX files. Colors must be 6-hex-digit strings without `#` prefix.

### Running Tests

```bash
cd servers/fastapi
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

### Legacy Next.js Frontend

- **Location**: `servers/nextjs/`
- **Runtime**: Node.js 22+, npm (has `package-lock.json`)
- **Dev command**: `cd servers/nextjs && npx next dev -p 3000`
- `next build` fails with pre-existing issues (duplicate dashboard routes, missing sqlite3 module). Dev mode works fine.
- No ESLint config is present; `next lint` prompts interactively — avoid running it.

### Gotchas

- The first server startup downloads ~80MB of ChromaDB ONNX models — this is normal and takes a few seconds.
- LLM-dependent features (outline generation, presentation content generation) require `OPENAI_API_KEY` or equivalent provider keys configured via the settings API or environment.
- The project has no `.gitmodules` file despite having a submodule entry — the `PresentationAI` directory must be populated manually by cloning `presenton/presenton`.
- Python 3.11 is **required** (`>=3.11,<3.12`). The VM snapshot has it installed via deadsnakes PPA. If missing, install with `sudo apt-get install -y python3.11 python3.11-venv python3.11-dev` (after adding the PPA).
