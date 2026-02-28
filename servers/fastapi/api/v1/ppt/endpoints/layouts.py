"""Layout endpoints — now served from local template registry (no Next.js dependency)."""

from fastapi import APIRouter, HTTPException
from utils.get_layout_by_name import get_layout_by_name
from utils.template_registry import get_template_groups
from models.presentation_layout import PresentationLayoutModel

LAYOUTS_ROUTER = APIRouter(prefix="/layouts", tags=["Layouts"])


@LAYOUTS_ROUTER.get("/", summary="Get available template groups")
async def get_layouts():
    return get_template_groups()


@LAYOUTS_ROUTER.get("/{layout_name}", summary="Get layout details by group name")
async def get_layout_detail(layout_name: str) -> PresentationLayoutModel:
    return await get_layout_by_name(layout_name)
