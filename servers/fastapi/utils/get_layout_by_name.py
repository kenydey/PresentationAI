"""Get layout by template group name — uses local registry instead of Next.js."""

from fastapi import HTTPException
from models.presentation_layout import PresentationLayoutModel
from utils.template_registry import get_layout_by_group


async def get_layout_by_name(layout_name: str) -> PresentationLayoutModel:
    layout = get_layout_by_group(layout_name)
    if not layout:
        raise HTTPException(
            status_code=404,
            detail=f"Template '{layout_name}' not found in local registry"
        )
    return layout
