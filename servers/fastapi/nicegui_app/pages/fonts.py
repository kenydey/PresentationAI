"""字体管理 — 上传、列表、删除自定义字体。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post_form, api_delete
import aiohttp


@ui.page("/fonts")
def fonts_page():
    page_layout("字体管理")

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
                    ui.button(icon="delete", on_click=make_del_handler(fname)).props("flat round dense color=negative size=sm")
        log.push(f"已加载 {len(fonts)} 个字体")

    async def del_font(filename):
        status, _ = await api_delete(f"/api/v1/ppt/fonts/delete/{filename}")
        if status in (200, 204):
            log.push(f"已删除 {filename}")
            ui.notify('字体已删除', type='positive')
        else:
            log.push(f"删除失败")
        await load_fonts()

    def make_del_handler(filename):
        async def handler():
            await del_font(filename)
        return handler

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("字体管理").classes("text-2xl font-bold")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            with ui.card().classes("w-96"):
                ui.label("上传字体").classes("font-semibold mb-2")
                ui.label("支持 TTF、OTF、WOFF、WOFF2 格式").classes("text-xs text-gray-400 mb-2")

                async def handle_upload(e):
                    f = getattr(e, "file", e)
                    fd = aiohttp.FormData()
                    fd.add_field("font_file", f.read(), filename=getattr(f, "name", "font"), content_type="application/octet-stream")
                    status, data = await api_post_form("/api/v1/ppt/fonts/upload", fd)
                    if status == 200:
                        log.push(f"上传成功: {data}")
                        ui.notify('字体上传成功', type='positive')
                        await load_fonts()
                    else:
                        log.push(f"上传失败: {data}")
                        ui.notify('字体上传失败', type='negative')

                ui.upload(on_upload=handle_upload, auto_upload=True).props(
                    "accept='.ttf,.otf,.woff,.woff2' flat bordered"
                ).classes("w-full")

            with ui.card().classes("w-96"):
                ui.label("分析 PPTX 字体").classes("font-semibold mb-2")
                ui.label("上传 PPTX 可分析文档中使用的字体").classes("text-xs text-gray-400 mb-2")
                pptx_result = ui.label().classes("text-sm text-gray-600")
                async def handle_pptx_analyze(e):
                    pptx_result.set_text("分析中…")
                    f = getattr(e, "file", e)
                    fd = aiohttp.FormData()
                    fd.add_field("pptx_file", f.read(), filename=getattr(f, "name", "file.pptx"), content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
                    status, data = await api_post_form("/api/v1/ppt/pptx-fonts/process", fd)
                    if status == 200 and isinstance(data, dict) and data.get("success"):
                        fonts_info = data.get("fonts", {})
                        supported = fonts_info.get("internally_supported_fonts", [])
                        not_supported = fonts_info.get("not_supported_fonts", [])
                        lines = [f"✓ 系统支持: {len(supported)} 个", f"✗ 需安装: {len(not_supported)} 个"]
                        if not_supported:
                            lines.append("未支持: " + ", ".join(not_supported[:5]))
                        pptx_result.set_text("\n".join(lines))
                    else:
                        pptx_result.set_text(f"分析失败: {data}")
                ui.upload(on_upload=handle_pptx_analyze, auto_upload=True).props(
                    "accept='.pptx' flat bordered"
                ).classes("w-full")

            with ui.card().classes("flex-1 min-w-[400px]"):
                with ui.row().classes("items-center justify-between"):
                    ui.label("已上传字体").classes("font-semibold")
                    ui.button("刷新", icon="refresh", on_click=load_fonts).props("flat")

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

    ui.timer(0.3, load_fonts, once=True)
