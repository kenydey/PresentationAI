"""Shared layout with left-drawer navigation for all NiceGUI pages."""

from nicegui import ui

NAV_ITEMS = [
    ("home",       "首页",         "/"),
    ("dashboard",  "仪表板",       "/dashboard"),
    ("add_circle", "创建演示",     "/create"),
    ("list_alt",   "大纲编辑",     "/outline"),
    ("slideshow",  "演示查看",     "/viewer"),
    ("image",      "图片管理",     "/images"),
    ("text_fields","字体管理",     "/fonts"),
    ("widgets",    "模板管理",     "/templates"),
    ("search",     "图标搜索",     "/icons"),
    ("settings",   "系统设置",     "/settings"),
]


def page_layout(title: str = "Presentation AI"):
    """Call at the top of every page to render the shared header + drawer."""
    ui.colors(primary="#6C63FF")

    with ui.header().classes("items-center justify-between bg-[#6C63FF] px-6"):
        with ui.row().classes("items-center gap-3"):

            def _toggle():
                drawer.toggle()

            ui.button(icon="menu", on_click=_toggle).props("flat round color=white")
            ui.label("Presentation AI").classes("text-xl font-bold text-white tracking-wide")
        ui.label(title).classes("text-white/80 text-sm")

    drawer = ui.left_drawer(value=True).classes("bg-gray-50 border-r")
    with drawer:
        ui.label("导航").classes("text-xs text-gray-400 uppercase tracking-wider px-4 pt-4 pb-1")
        for icon, label, target in NAV_ITEMS:
            with ui.link(target=target).classes("no-underline"):
                with ui.row().classes(
                    "items-center gap-3 px-4 py-2 rounded-lg hover:bg-violet-50 "
                    "transition cursor-pointer w-full"
                ):
                    ui.icon(icon).classes("text-[#6C63FF] text-lg")
                    ui.label(label).classes("text-gray-700 text-sm")

    return drawer
