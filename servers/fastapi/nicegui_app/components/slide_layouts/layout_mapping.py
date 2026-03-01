"""layout_id → 预览模式映射表，覆盖 120 个 TSX 布局。"""

from typing import Dict

# 显式映射：layout_id -> 预览模式
LAYOUT_TO_PREVIEW_TYPE: Dict[str, str] = {
    # title_slide — 居中标题封面
    "general-intro-slide": "title_slide",
    "intro-pitchdeck-slide": "title_slide",
    "IntroSlideLayout": "title_slide",
    "header-counter-two-column-image-text-slide": "title_slide",
    # text_image_split — 左图右文
    "basic-info-slide": "text_image_split",
    "bullet-icons-only-slide": "text_image_split",
    "bullet-with-icons-slide": "text_image_split",
    "bullet-with-icons": "text_image_split",
    "bullet-with-icons-description-grid": "text_image_split",
    "image-and-description": "text_image_split",
    "image-list-with-description": "text_image_split",
    "images-with-description": "text_image_split",
    "headline-description-with-image-layout": "text_image_split",
    "headline-description-with-double-image-layout": "text_image_split",
    "title-description-image-right": "text_image_split",
    "title-description-large-image-right": "text_image_split",
    "bullet-with-icons-title-description": "text_image_split",
    "image-list-description-slide": "text_image_split",
    "split-left-strip-header-title-subtitle-cards-slide": "text_image_split",
    "header-bullets-title-description-image-slide": "text_image_split",
    "header-bullets-image-split-slide": "text_image_split",
    "chart-left-text-right-layout": "text_image_split",
    # three_column_grid — 三列卡片 / TOC
    "table-of-contents-slide": "three_column_grid",
    "table-of-contents": "three_column_grid",
    "table-of-contents-layout": "three_column_grid",
    "SwiftTableOfContents": "three_column_grid",
    "title-three-columns-with-labels": "three_column_grid",
    "title-three-column-risk-constraints-slide-layout": "three_column_grid",
    "title-six-card-grid-slide-layout": "three_column_grid",
    "header-tagline-cards-grid-slide": "three_column_grid",
    # metrics — 指标卡片网格
    "metrics-slide": "metrics",
    "metrics-with-image-slide": "metrics",
    "metrics-with-description-image": "metrics",
    "performance-grid-snapshot-slide": "metrics",
    "layout-text-block-with-metric-cards": "metrics",
    "headline-text-with-stats-layout": "metrics",
    "title-description-eight-metrics-grid": "metrics",
    "title-description-metrics-grid-large-image": "metrics",
    "title-description-dual-metrics-grid": "metrics",
    "title-kpi-snapshot-grid": "metrics",
    "title-kpi-grid": "metrics",
    "title-three-by-three-metrics-grid": "metrics",
    "title-label-description-cascading-stats": "metrics",
    "MetricsNumbers": "metrics",
    "visual-metrics": "metrics",
    "chart-with-metrics": "metrics",
    "title-metrics-with-chart": "metrics",
    "title-chart-metrics-sidebar": "metrics",
    "title-description-metrics-chart": "metrics",
    "title-description-metrics-image": "metrics",
    "title-description-six-charts-four-metrics": "metrics",
    "title-metrics-chart": "metrics",
    "title-metrics-image": "metrics",
    # quote — 引用块
    "quote-slide": "quote",
    "left-align-quote": "quote",
    # team — 成员卡片
    "team-slide": "team",
    "title-description-team-grid": "team",
    "title-subtitle-four-team-member-cards": "team",
    "header-smallbar-title-team-cards-slide": "team",
    # chart_bullets — 左图/表右要点
    "chart-with-bullets-slide": "chart_bullets",
    "chart-or-table-with-description": "chart_bullets",
    "title-description-multi-chart-grid": "chart_bullets",
    "title-description-multi-chart-grid-bullets": "chart_bullets",
    "title-description-multi-chart-grid-metrics": "chart_bullets",
    "title-description-multi-chart-grid": "chart_bullets",
    "title-description-four-charts-six-bullets": "chart_bullets",
    "title-description-six-charts-grid": "chart_bullets",
    "multi-chart-grid-slide": "chart_bullets",
    "title-with-full-width-chart": "chart_bullets",
    "title-centered-chart": "chart_bullets",
    "title-badge-chart": "chart_bullets",
    "title-subtitles-chart": "chart_bullets",
    "title-dual-charts-comparison": "chart_bullets",
    "title-dual-comparison-charts": "chart_bullets",
    "tableorChart": "chart_bullets",
    # numbered_list — 有序列表
    "numbered-bullets-slide": "numbered_list",
    "title-two-column-numbered-list": "numbered_list",
    "title-tagline-description-numbered-steps": "numbered_list",
    "header-bullets-image-split-slide": "numbered_list",
    # contact — 联系信息
    "header-left-media-contact-info-slide": "contact",
    "title-description-contact-list": "contact",
    "title-description-contact-cards": "contact",
    "thank-you-contact-info-footer-image-slide-layout": "contact",
    # table — 表+说明
    "table-info-slide": "table",
    "title-description-table": "table",
    "title-description-three-columns-table": "table",
    "title-description-three-column-table": "table",
    # timeline — 时间线
    "timeline-alternating-cards-slide": "timeline",
    "title-horizontal-alternating-timeline": "timeline",
    "title-description-icon-timeline": "timeline",
    "title-description-timeline": "timeline",
    "Timeline": "timeline",
    # two_column / dual comparison
    "title-dual-comparison-cards": "two_column",
    "title-dual-comparison-blocks-numbered": "two_column",
    "title-side-insight-slide": "two_column",
    "title-challenge-outcome-customer-card": "two_column",
    # bullet list
    "title-description-bullet-list": "text_image_split",
    "title-description-icon-list": "text_image_split",
    "title-description-bullet-list": "text_image_split",
    "simple-bullet-points-layout": "text_image_split",
    "icon-bullet-list-description-slide": "text_image_split",
    # radial / donut
    "title-description-radial-cards": "three_column_grid",
    "title-points-donut-grid": "three_column_grid",
}


def get_preview_type(layout_id: str) -> str:
    """
    根据 layout_id 返回预览版式类型。

    Args:
        layout_id: 来自 template_registry 或 SlideModel.layout

    Returns:
        模式名: title_slide | text_image_split | three_column_grid | metrics |
                quote | team | chart_bullets | numbered_list | contact |
                table | timeline | two_column
    """
    if not layout_id or not isinstance(layout_id, str):
        return "text_image_split"
    if layout_id in LAYOUT_TO_PREVIEW_TYPE:
        return LAYOUT_TO_PREVIEW_TYPE[layout_id]
    lid = layout_id.lower()
    if "intro" in lid or lid == "general-intro-slide":
        return "title_slide"
    if "metrics" in lid or "kpi" in lid or "metric" in lid:
        return "metrics"
    if "quote" in lid:
        return "quote"
    if "team" in lid or "member" in lid:
        return "team"
    if "toc" in lid or "contents" in lid or "grid" in lid or "three" in lid or "column" in lid:
        return "three_column_grid"
    if "chart" in lid:
        return "chart_bullets"
    if "numbered" in lid or "number" in lid:
        return "numbered_list"
    if "contact" in lid:
        return "contact"
    if "table" in lid:
        return "table"
    if "timeline" in lid:
        return "timeline"
    if "dual" in lid or "comparison" in lid or "two-column" in lid:
        return "two_column"
    return "text_image_split"
