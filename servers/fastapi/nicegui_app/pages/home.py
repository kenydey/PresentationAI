"""首页 — 快速导航入口。"""

from nicegui import ui
from nicegui_app.layout import page_layout


@ui.page("/")
def index_page():
    page_layout("首页")
    with ui.column().classes("items-center w-full pt-12 gap-6"):
        ui.icon("slideshow").classes("text-6xl text-[#6C63FF]")
        ui.label("Presenton").classes("text-4xl font-bold text-[#6C63FF]")
        ui.label("开源 AI 演示文稿生成器 · NiceGUI 前端").classes("text-gray-500 text-lg")
        ui.separator().classes("w-96 my-2")
        with ui.row().classes("gap-4 flex-wrap justify-center"):
            with ui.link(target="/create"):
                ui.button("创建演示文稿", icon="add_circle").props("color=primary size=lg")
            with ui.link(target="/dashboard"):
                ui.button("查看仪表板", icon="dashboard").props("outline size=lg")
            with ui.link(target="/settings"):
                ui.button("系统设置", icon="settings").props("outline size=lg")

        with ui.card().classes("w-full max-w-2xl mt-6"):
            ui.label("功能概览").classes("text-lg font-semibold mb-2")
            features = [
                ("add_circle", "创建演示", "输入主题、选择模板，一键生成 PPTX/PDF"),
                ("list_alt", "大纲编辑", "流式生成大纲，逐页编辑后保存"),
                ("slideshow", "演示查看", "查看幻灯片内容，编辑单页"),
                ("image", "图片管理", "AI 生成图片或上传自有图片"),
                ("text_fields", "字体管理", "上传和管理自定义字体"),
                ("widgets", "模板管理", "保存和复用演示文稿模板"),
                ("search", "图标搜索", "搜索并使用矢量图标"),
                ("settings", "系统设置", "配置 LLM 和图像生成服务"),
            ]
            for icon, title, desc in features:
                with ui.row().classes("items-center gap-3 py-1"):
                    ui.icon(icon).classes("text-[#6C63FF]")
                    ui.label(title).classes("font-medium w-24")
                    ui.label(desc).classes("text-gray-500 text-sm")
