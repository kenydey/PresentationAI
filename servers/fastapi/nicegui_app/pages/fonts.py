"""字体管理 — 上传、列表、删除自定义字体。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post_form, api_delete
import aiohttp


@ui.page("/fonts")
def fonts_page():
    page_layout("字体管理")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("字体管理").classes("text-2xl font-bold")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            with ui.card().classes("w-96"):
                ui.label("上传字体").classes("font-semibold mb-2")
                ui.label("支持 TTF、OTF、WOFF、WOFF2 格式").classes("text-xs text-gray-400 mb-2")

                async def handle_upload(e):
                    fd = aiohttp.FormData()
                    fd.add_field("font_file", e.content.read(), filename=e.name, content_type="application/octet-stream")
                    status, data = await api_post_form("/api/v1/ppt/fonts/upload", fd)
                    if status == 200:
                        log.push(f"上传成功: {data}")
                        await load_fonts()
                    else:
                        log.push(f"上传失败: {data}")

                ui.upload(on_upload=handle_upload, auto_upload=True).props(
                    "accept='.ttf,.otf,.woff,.woff2' flat bordered"
                ).classes("w-full")

            with ui.card().classes("flex-1 min-w-[400px]"):
                with ui.row().classes("items-center justify-between"):
                    ui.label("已上传字体").classes("font-semibold")
                    ui.button("刷新", icon="refresh", on_click=lambda: load_fonts()).props("flat")

                font_table = ui.table(
                    columns=[
                        {"name": "filename", "label": "文件名", "field": "filename", "align": "left"},
                        {"name": "actions", "label": "操作", "field": "actions"},
                    ],
                    rows=[],
                    row_key="filename",
                ).props("dense flat bordered").classes("w-full")

                font_list = ui.column().classes("w-full gap-2")

        log = ui.log().classes("h-24 w-full")

    async def load_fonts():
        log.clear()
        status, data = await api_get("/api/v1/ppt/fonts/list")
        if status != 200:
            log.push(f"加载失败: {data}")
            return
        fonts = data.get("fonts", []) if isinstance(data, dict) else []
        font_list.clear()
        for f in fonts:
            fname = f if isinstance(f, str) else f.get("filename", str(f))
            with font_list:
                with ui.row().classes("items-center justify-between w-full px-2 py-1 bg-gray-50 rounded"):
                    ui.icon("text_fields").classes("text-[#6C63FF]")
                    ui.label(fname).classes("flex-1")
                    ui.button(icon="delete", on_click=lambda fn=fname: del_font(fn)).props("flat round dense color=negative size=sm")
        log.push(f"已加载 {len(fonts)} 个字体")

    async def del_font(filename):
        status, _ = await api_delete(f"/api/v1/ppt/fonts/delete/{filename}")
        if status in (200, 204):
            log.push(f"已删除 {filename}")
        else:
            log.push(f"删除失败")
        await load_fonts()

    ui.timer(0.3, load_fonts, once=True)
