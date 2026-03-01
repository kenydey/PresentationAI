"""幻灯片预览组件 — 统一入口，根据 layout_id 选择版式并渲染 HTML。"""

from nicegui_app.components.slide_layouts import (
    render_title_slide,
    render_text_image_split,
    render_three_column_grid,
)


def get_preview_layout_type(layout_id: str) -> str:
    """
    根据 layout_id 返回预览版式类型。

    Args:
        layout_id: 来自 template_registry 或 SlideModel.layout

    Returns:
        "title_slide" | "text_image_split" | "three_column_grid"
    """
    lid = (layout_id or "").lower()
    if "intro" in lid or "title" in lid or lid in ("general-intro-slide",):
        return "title_slide"
    if "toc" in lid or "grid" in lid or "three" in lid or "column" in lid:
        return "three_column_grid"
    return "text_image_split"


def render_slide_preview_html(
    data: dict,
    layout_type: str | None = None,
) -> str:
    """
    根据版式类型渲染幻灯片预览 HTML。

    Args:
        data: SlidePreviewData（含 title, bullet_points, image_url, image_prompt, layout_id）
        layout_type: 可选，若未传则从 data["layout_id"] 推断

    Returns:
        完整 HTML 字符串，可直接赋值给 ui.html().content
    """
    if layout_type is None:
        layout_type = get_preview_layout_type(data.get("layout_id") or "")

    if layout_type == "title_slide":
        return render_title_slide(data)
    if layout_type == "three_column_grid":
        return render_three_column_grid(data)
    # 默认 text_image_split
    return render_text_image_split(data)
