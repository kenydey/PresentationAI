"""图标搜索 — 搜索矢量图标。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, get_base_url


@ui.page("/icons")
def icons_page():
    page_layout("图标搜索")

    async def search_icons():
        q = query_input.value.strip()
        if not q:
            log.push("请输入搜索关键词")
            return
        results_grid.clear()
        limit = int(limit_input.value or 20)
        search_btn.props("disable loading")
        log.push(f"搜索: {q} (limit={limit})")

        status, data = await api_get(f"/api/v1/ppt/icons/search?query={q}&limit={limit}")
        search_btn.props(remove="disable loading")

        if status != 200:
            log.push(f"搜索失败: {data}")
            ui.notify('搜索失败', type='negative')
            return

        icons_list = data if isinstance(data, list) else data.get("icons", []) if isinstance(data, dict) else []
        base = get_base_url()
        for icon_item in icons_list:
            if isinstance(icon_item, dict):
                name = icon_item.get("name", "")
                url = icon_item.get("url", "") or icon_item.get("path", "")
                svg = icon_item.get("svg", "")
            elif isinstance(icon_item, str):
                name = icon_item
                url = ""
                svg = ""
            else:
                continue

            with results_grid:
                with ui.card().classes("w-32 items-center p-2"):
                    if svg:
                        ui.html(svg).classes("w-12 h-12")
                    elif url:
                        full = url if url.startswith("http") else base + ("/" if not url.startswith("/") else "") + url
                        ui.image(full).classes("w-12 h-12")
                    else:
                        ui.icon("image").classes("text-3xl text-gray-300")
                    ui.label(name[:20]).classes("text-xs text-gray-600 text-center truncate w-full")

        log.push(f"找到 {len(icons_list)} 个图标")
        ui.notify(f'找到 {len(icons_list)} 个图标', type='info')

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("图标搜索").classes("text-2xl font-bold")

        with ui.row().classes("gap-3 items-center"):
            query_input = ui.input("搜索关键词", placeholder="例如：chart, arrow, person…").classes("w-96")
            limit_input = ui.number("数量限制", value=20, min=1, max=100).classes("w-28")
            search_btn = ui.button("搜索", icon="search", on_click=search_icons).props("color=primary")

        results_grid = ui.row().classes("w-full flex-wrap gap-4")
        log = ui.log().classes("h-20 w-full")
