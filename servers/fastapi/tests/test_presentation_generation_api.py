from unittest.mock import patch, AsyncMock, MagicMock
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from models.presentation_layout import PresentationLayoutModel
from models.presentation_structure_model import PresentationStructureModel
from api.v1.ppt.endpoints.presentation import PRESENTATION_ROUTER

class MockAiohttpResponse:
    def __init__(self, status=200, json_data=None):
        self.status = status
        self._json_data = json_data or {"path": "/tmp/exports/test.pdf"}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def json(self):
        return self._json_data

    async def text(self):
        return str(self._json_data)

class MockAiohttpSession:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def post(self, *args, **kwargs):
        return MockAiohttpResponse()

    def get(self, *args, **kwargs):
        pptx_model_data = {
            "slides": [],
            "title": "Test",
            "notes": [],
            "layout": {},
            "structure": {},
        }
        return MockAiohttpResponse(json_data=pptx_model_data)

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(PRESENTATION_ROUTER, prefix="/api/v1/ppt")
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def mock_get_layout():
    async def _mock_get_layout_by_name(layout_name: str):
        mock_slide = MagicMock()
        mock_slide.id = "basic-info-slide"
        mock_slide.name = "Mock Slide"
        mock_slide.json_schema = {"title": "Mock Slide Title"}
        mock_slide.description = "Mock slide description"
        mock_layout = MagicMock(spec=PresentationLayoutModel)
        mock_layout.name = layout_name
        mock_layout.ordered = True
        mock_layout.slides = [mock_slide]
        mock_layout.model_dump = lambda: {}
        mock_layout.to_presentation_structure = lambda: PresentationStructureModel(
            slides=[index for index in range(len(mock_layout.slides))]
        )
        def to_string():
            message = f"## Presentation Layout\n\n"
            for index, slide in enumerate(mock_layout.slides):
                message += f"### Slide Layout: {index}: \n"
                message += f"- Name: {slide.name or slide.json_schema.get('title')} \n"
                message += f"- Description: {slide.description} \n\n"
            return message
        mock_layout.to_string = to_string
        return mock_layout
    return _mock_get_layout_by_name

from models.presentation_state import PresentationState, SlideState


async def mock_research_agent_run(*args, **kwargs):
    """Mock RESEARCH_AGENT: 返回简单的 PresentationState。"""
    n_slides = kwargs.get("n_slides", 5)
    slides = []
    for i in range(n_slides):
        slides.append(
            SlideState(
                title=f"Slide {i + 1}",
                bullet_points=["要点 1", "要点 2"],
                image_prompt="professional business" if i > 0 else None,
                layout_id="pending",
            )
        )
    return PresentationState(title="Test", slides=slides)


async def mock_design_agent_run(state, *args, **kwargs):
    """Mock DESIGN_AGENT: 为每页分配 basic-info-slide。"""
    layout = kwargs.get("layout_group", "general")
    from utils.template_registry import get_layout_by_group
    layout_model = get_layout_by_group(layout)
    layout_id = layout_model.slides[0].id if layout_model and layout_model.slides else "basic-info-slide"
    new_slides = [
        SlideState(
            title=s.title,
            bullet_points=s.bullet_points,
            image_prompt=s.image_prompt,
            layout_id=layout_id,
        )
        for s in state.slides
    ]
    return PresentationState(title=state.title, slides=new_slides)


@pytest.fixture(autouse=True)
def patch_presentation_api(monkeypatch, mock_get_layout):
    import os
    os.makedirs("/tmp/mockdir", exist_ok=True)
    os.makedirs("/tmp/exports", exist_ok=True)
    # Patch all dependencies used in the API
    patches = [
        patch('api.v1.ppt.endpoints.presentation.get_layout_by_name', new=AsyncMock(side_effect=mock_get_layout)),
        patch('api.v1.ppt.endpoints.presentation.TEMP_FILE_SERVICE.create_temp_dir', return_value='/tmp/mockdir'),
        patch('api.v1.ppt.endpoints.presentation.DocumentsLoader'),
        patch('api.v1.ppt.endpoints.presentation.research_agent_run', side_effect=mock_research_agent_run),
        patch('api.v1.ppt.endpoints.presentation.design_agent_run', side_effect=mock_design_agent_run),
        patch('api.v1.ppt.endpoints.presentation.get_slide_content_from_type_and_outline', new_callable=AsyncMock, return_value={"mock": "slide_content"}),
        patch('api.v1.ppt.endpoints.presentation.process_slide_and_fetch_assets', new_callable=AsyncMock),
        patch('api.v1.ppt.endpoints.presentation.get_exports_directory', return_value='/tmp/exports'),
        patch('api.v1.ppt.endpoints.presentation.PptxPresentationCreator'),
    ]
    mocks = [p.start() for p in patches]

    # Setup DocumentsLoader mock
    docs_loader = mocks[2]
    docs_loader.return_value.load_documents = AsyncMock()
    docs_loader.return_value.documents = []

    # Setup PptxPresentationCreator mock for pptx test
    pptx_creator = mocks[8]  # index 8 = PptxPresentationCreator
    pptx_creator.return_value.create_ppt = AsyncMock()
    pptx_creator.return_value.save = MagicMock()

    yield

    for p in patches:
        p.stop()

class TestPresentationGenerationAPI:
    def test_generate_presentation_export_as_pdf(self, client):
        response = client.post(
            "/api/v1/ppt/presentation/generate",
            json={
                "content": "Create a presentation about artificial intelligence and machine learning",
                "n_slides": 5,
                "language": "English",
                "export_as": "pdf",
                "template": "general"
            }
        )
        assert response.status_code == 200
        assert "presentation_id" in response.json()
        assert "pdf" in response.json()["path"]

    def test_generate_presentation_export_as_pptx(self, client):
        response = client.post(
            "/api/v1/ppt/presentation/generate",
            json={
                "content": "Create a presentation about artificial intelligence and machine learning",
                "n_slides": 5,
                "language": "English",
                "export_as": "pptx",
                "template": "general"
            }
        )
        assert response.status_code == 200
        assert "presentation_id" in response.json()
        assert "pptx" in response.json()["path"]

    def test_generate_presentation_with_no_content(self, client):
        response = client.post(
            "/api/v1/ppt/presentation/generate",
            json={
                "n_slides": 5,
                "language": "English",
                "export_as": "pdf",
                "template": "general"
            }
        )
        assert response.status_code == 422


    def test_generate_presentation_with_n_slides_less_than_one(self, client):
        response = client.post(
            "/api/v1/ppt/presentation/generate",
            json={
                "content": "Create a presentation about artificial intelligence and machine learning",
                "n_slides": 0,
                "language": "English",
                "export_as": "pdf",
                "template": "general"
            }
        )
        assert response.status_code >= 400  # 验证失败 (400/422/500 等)

    def test_generate_presentation_with_invalid_export_type(self, client):
        response = client.post(
            "/api/v1/ppt/presentation/generate",
            json={
                "content": "Create a presentation about artificial intelligence and machine learning",
                "n_slides": 5,
                "language": "English",
                "export_as": "invalid_type",
                "template": "general"
            }
        )
        assert response.status_code == 422
