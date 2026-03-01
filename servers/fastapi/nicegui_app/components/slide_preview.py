"""幻灯片预览组件 — 统一入口，根据 layout_id 选择版式并渲染 HTML。"""

from nicegui_app.components.slide_layouts import (
    get_preview_type,
    render_title_slide,
    render_text_image_split,
    render_three_column_grid,
    render_metrics_slide,
    render_quote_slide,
    render_team_slide,
    render_numbered_list,
    render_chart_bullets,
    render_contact_slide,
    render_table_slide,
    render_timeline_slide,
    render_two_column,
)


def get_preview_layout_type(layout_id: str) -> str:
    """
    根据 layout_id 返回预览版式类型。
    委托给 layout_mapping.get_preview_type。
    """
    return get_preview_type(layout_id)


def render_slide_preview_html(
    data: dict,
    layout_type: str | None = None,
) -> str:
    """
    根据版式类型渲染幻灯片预览 HTML。

    Args:
        data: SlidePreviewData（含 title, bullet_points, image_url, metrics, quote 等）
        layout_type: 可选，若未传则从 data["layout_id"] 推断

    Returns:
        完整 HTML 字符串，可直接赋值给 ui.html().content
    """
    if layout_type is None:
        layout_type = get_preview_type(data.get("layout_id") or "")

    if layout_type == "title_slide":
        return render_title_slide(data)
    if layout_type == "three_column_grid":
        return render_three_column_grid(data)
    if layout_type == "metrics":
        return render_metrics_slide(data)
    if layout_type == "quote":
        return render_quote_slide(data)
    if layout_type == "team":
        return render_team_slide(data)
    if layout_type == "numbered_list":
        return render_numbered_list(data)
    if layout_type == "chart_bullets":
        return render_chart_bullets(data)
    if layout_type == "contact":
        return render_contact_slide(data)
    if layout_type == "table":
        return render_table_slide(data)
    if layout_type == "timeline":
        return render_timeline_slide(data)
    if layout_type == "two_column":
        return render_two_column(data)
    # 默认 text_image_split
    return render_text_image_split(data)
