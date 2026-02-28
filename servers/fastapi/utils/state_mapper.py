"""PresentationState ↔ Outline/Structure/Slides 映射。"""

from typing import Any, Dict, List

from models.presentation_outline_model import PresentationOutlineModel, SlideOutlineModel
from models.presentation_state import PresentationState, SlideState
from models.presentation_structure_model import PresentationStructureModel
from models.presentation_layout import PresentationLayoutModel


def extract_title_from_outline_content(content: str) -> str:
    """从 outline content 中提取标题（支持 Title: xxx 格式）。"""
    if not content:
        return ""
    for line in content.split("\n"):
        line = line.strip()
        if line.lower().startswith("title:"):
            return line[6:].strip()[:100]
    return content[:100].replace("\n", " ")


def slide_state_to_outline_content(slide_state) -> str:
    """
    将 SlideState 转为 SlideOutlineModel 的 content 字符串。
    get_slide_content_from_type_and_outline 会将该 content 作为 outline 使用。
    """
    parts = [f"Title: {slide_state.title}"]
    if slide_state.bullet_points:
        parts.append("Bullet points:")
        for bp in slide_state.bullet_points:
            parts.append(f"- {bp}")
    if slide_state.image_prompt:
        parts.append(f"Image prompt: {slide_state.image_prompt}")
    return "\n".join(parts)


def presentation_state_to_outline_and_structure(
    state: PresentationState,
    layout_model: PresentationLayoutModel,
) -> tuple[PresentationOutlineModel, PresentationStructureModel, str | None]:
    """
    将 PresentationState 转为 PresentationOutlineModel 和 PresentationStructureModel。
    供现有流水线使用。
    """
    outline_slides = []
    structure_indices = []

    for s in state.slides:
        content = slide_state_to_outline_content(s)
        outline_slides.append(SlideOutlineModel(content=content))
        idx = -1
        for i, lm in enumerate(layout_model.slides):
            if lm.id == s.layout_id:
                idx = i
                break
        if idx < 0:
            idx = 0  # fallback to first layout
        structure_indices.append(idx)

    outline = PresentationOutlineModel(slides=outline_slides)
    structure = PresentationStructureModel(slides=structure_indices)
    title = state.title or (
        extract_title_from_outline_content(outline_slides[0].content)
        if outline_slides
        else None
    )
    return outline, structure, title


def slides_to_presentation_state(
    slides: List[Dict[str, Any]],
    title: str | None = None,
) -> PresentationState:
    """
    将 API 返回的 slides（SlideModel 序列化）转为 PresentationState。
    供 Vibe 对话式编辑使用。

    Args:
        slides: 包含 layout, layout_group, content 等字段的字典列表
        title: 可选演示标题，默认从第一页提取

    Returns:
        PresentationState
    """
    if not slides:
        raise ValueError("slides 不能为空")

    slide_states: List[SlideState] = []
    for s in slides:
        content = s.get("content") or {}
        if not isinstance(content, dict):
            content = {}

        stitle = (
            content.get("title")
            or content.get("heading")
            or content.get("headline")
            or "无标题"
        )
        stitle = str(stitle).strip()[:200] if stitle else "无标题"

        bullets_raw = (
            content.get("bullets")
            or content.get("items")
            or content.get("points")
            or content.get("bulletPoints")
            or []
        )
        if not isinstance(bullets_raw, list):
            bullets_raw = []
        bullet_points: List[str] = []
        for b in bullets_raw[:8]:
            if isinstance(b, str):
                bullet_points.append(str(b).strip()[:150])
            elif isinstance(b, dict):
                txt = b.get("text") or b.get("title") or ""
                bullet_points.append(str(txt).strip()[:150])
            else:
                bullet_points.append(str(b)[:150])

        image_prompt = (
            content.get("imagePrompt")
            or content.get("image_description")
            or content.get("image_prompt")
            or ""
        )
        image_prompt = str(image_prompt).strip() if image_prompt else None

        layout_id = s.get("layout") or "basic-info-slide"
        if not isinstance(layout_id, str):
            layout_id = "basic-info-slide"

        slide_states.append(
            SlideState(
                title=stitle,
                bullet_points=bullet_points,
                image_prompt=image_prompt,
                layout_id=layout_id,
            )
        )

    pres_title = title
    if not pres_title and slide_states:
        pres_title = slide_states[0].title

    return PresentationState(title=pres_title, slides=slide_states)
