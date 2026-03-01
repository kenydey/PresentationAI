"""三种基础预览版式：title_slide、text_image_split、three_column_grid。"""

from nicegui_app.components.slide_layouts.title_slide import render_title_slide
from nicegui_app.components.slide_layouts.text_image_split import render_text_image_split
from nicegui_app.components.slide_layouts.three_column_grid import render_three_column_grid

__all__ = ["render_title_slide", "render_text_image_split", "render_three_column_grid"]
