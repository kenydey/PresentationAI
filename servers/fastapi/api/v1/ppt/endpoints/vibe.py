"""Vibe 对话式编辑 — HTTP API。"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agents.vibe_editor import vibe_editor_run
from models.presentation_state import PresentationState
from utils.state_mapper import slides_to_presentation_state
from utils.template_registry import get_all_layout_ids

VIBE_ROUTER = APIRouter(prefix="/vibe", tags=["Vibe"])


class VibeEditRequest(BaseModel):
    """Vibe 编辑请求。"""

    presentation_state: dict | None = Field(
        default=None,
        description="当前 PresentationState JSON；若未传则使用 slides 转换",
    )
    slides: list | None = Field(
        default=None,
        description="SlideModel 格式；当 presentation_state 未传时必填",
    )
    instruction: str = Field(..., min_length=1, description="用户自然语言指令")
    language: str = Field(default="Chinese", description="内容语言")


class VibeEditResponse(BaseModel):
    """Vibe 编辑响应。"""

    presentation_state: dict = Field(..., description="修改后的 PresentationState JSON")
    message: str = Field(default="已按指令修改", description="提示信息")


@VIBE_ROUTER.post("/edit", response_model=VibeEditResponse)
async def vibe_edit(request: VibeEditRequest) -> VibeEditResponse:
    """
    根据自然语言指令修改演示状态。
    支持内容与排版（layout_id）变更。
    """
    if request.presentation_state and request.presentation_state.get("slides"):
        try:
            state = PresentationState.model_validate(request.presentation_state)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"无效的 presentation_state: {e}")
    elif request.slides:
        try:
            state = slides_to_presentation_state(request.slides)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="请提供 presentation_state 或 slides")

    available_layout_ids = get_all_layout_ids()

    new_state = await vibe_editor_run(
        state=state,
        instruction=request.instruction.strip(),
        language=request.language,
        allow_layout_change=True,
        available_layout_ids=available_layout_ids,
    )

    return VibeEditResponse(
        presentation_state=new_state.model_dump(exclude_none=True),
        message="已按指令修改",
    )
