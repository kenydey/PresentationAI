"""PresentationState — 结构化演示状态，供 Research/Design/VibeEditor Agent 使用。"""

from typing import List, Optional

from pydantic import BaseModel, Field


class SlideState(BaseModel):
    """单页幻灯片状态。"""

    title: str = Field(description="幻灯片标题")
    bullet_points: List[str] = Field(
        description="核心要点列表，每个 1–2 行，标题页可为空",
        min_length=0,
        max_length=8,
    )
    image_prompt: Optional[str] = Field(
        default=None,
        description="配图描述，用于 AI 生成或图片搜索",
    )
    layout_id: str = Field(
        description="Tailwind 布局 ID，对应 template_registry 中的 id",
    )


class PresentationState(BaseModel):
    """演示文稿完整状态。"""

    title: Optional[str] = Field(
        default=None,
        description="演示标题",
    )
    slides: List[SlideState] = Field(
        description="幻灯片列表",
        min_length=1,
    )
