"""导出预览页 — 供 Playwright DOM 采样使用，不显示导航。

渲染所有幻灯片于 #presentation-slides-wrapper，每页 1280x720 固定尺寸。
"""

import html as html_module
from nicegui import ui
from nicegui_app.api_client import api_get
from nicegui_app.utils.slide_preview_data import (
    slide_to_preview_data,
    slide_state_to_preview_data,
)
from nicegui_app.components.slide_preview import render_slide_preview_html
from utils.state_mapper import slides_to_presentation_state


@ui.page("/export-view")
def export_view_page(id: str = ""):
    """最小化页面：仅渲染幻灯片列表，供 Playwright 采样 DOM。"""
    # 无 page_layout，保持 DOM 简洁
    ui.add_head_html(
        '<script src="https://cdn.tailwindcss.com"></script>'
    )

    wrapper = ui.element("div").props("id=presentation-slides-wrapper").classes(
        "flex flex-col items-center gap-0 bg-gray-100"
    )

    async def load_and_render():
        wrapper.clear()
        pid = id.strip()
        if not pid:
            with wrapper:
                ui.html(
                    '<div class="p-8 text-gray-500">缺少演示 ID</div>',
                    sanitize=False,
                )
            return

        status, data = await api_get(f"/api/v1/ppt/presentation/{pid}")
        if status != 200:
            with wrapper:
                ui.html(
                    f'<div class="p-8 text-red-500">加载失败: {data}</div>',
                    sanitize=False,
                )
            return

        slides = data.get("slides", [])
        title = data.get("title", "演示文稿")
        try:
            ps = slides_to_presentation_state(slides, title=title).model_dump(
                exclude_none=True
            )
        except Exception:
            ps = None

        for idx, s in enumerate(slides):
            # 每页 1280x720，与 PPT 标准比例一致
            speaker_note = html_module.escape((s.get("speaker_note") or "").strip())
            with wrapper:
                with ui.element("div").props(
                    f'data-speaker-note="{speaker_note}"'
                ).classes("slide-container").style(
                    "width: 1280px; height: 720px; overflow: hidden; flex-shrink: 0;"
                ):
                    if ps and ps.get("slides") and idx < len(ps["slides"]):
                        ss = ps["slides"][idx]
                        img_url = None
                        content = s.get("content") or {}
                        img_obj = content.get("image") or content.get("backgroundImage") or {}
                        if isinstance(img_obj, dict):
                            img_url = img_obj.get("__image_url__") or img_obj.get("url")
                        preview_data = slide_state_to_preview_data(ss, image_url=img_url)
                    else:
                        preview_data = slide_to_preview_data(s)
                    html_content = render_slide_preview_html(preview_data)
                    ui.html(html_content, sanitize=False).classes(
                        "w-full h-full"
                    ).style("display: block;")

        # 标记就绪，供 Playwright 等待
        wrapper.props("data-export-ready=true")

    ui.timer(0.2, load_and_render, once=True)
