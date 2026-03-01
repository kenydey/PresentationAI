"""多种预览版式，覆盖 120 个 TSX 布局。"""

from nicegui_app.components.slide_layouts.title_slide import render_title_slide
from nicegui_app.components.slide_layouts.text_image_split import render_text_image_split
from nicegui_app.components.slide_layouts.three_column_grid import render_three_column_grid
from nicegui_app.components.slide_layouts.metrics_slide import render_metrics_slide
from nicegui_app.components.slide_layouts.quote_slide import render_quote_slide
from nicegui_app.components.slide_layouts.team_slide import render_team_slide
from nicegui_app.components.slide_layouts.numbered_list import render_numbered_list
from nicegui_app.components.slide_layouts.chart_bullets import render_chart_bullets
from nicegui_app.components.slide_layouts.contact_slide import render_contact_slide
from nicegui_app.components.slide_layouts.table_slide import render_table_slide
from nicegui_app.components.slide_layouts.timeline_slide import render_timeline_slide
from nicegui_app.components.slide_layouts.two_column import render_two_column
from nicegui_app.components.slide_layouts.layout_mapping import get_preview_type

__all__ = [
    "render_title_slide",
    "render_text_image_split",
    "render_three_column_grid",
    "render_metrics_slide",
    "render_quote_slide",
    "render_team_slide",
    "render_numbered_list",
    "render_chart_bullets",
    "render_contact_slide",
    "render_table_slide",
    "render_timeline_slide",
    "render_two_column",
    "get_preview_type",
]
