"""图片管理 — AI 生成、上传、浏览、删除图片。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post_form, api_delete, get_base_url
import aiohttp


@ui.page("/images")
def images_page():
    page_layout("图片管理")

    async def gen_image():
        prompt_text = gen_prompt.value.strip()
        if not prompt_text:
            log.push("请输入图片描述")
            return
        gen_btn.props("disable loading")
        log.push(f"正在生成: {prompt_text}")
        status, data = await api_get(f"/api/v1/ppt/images/generate?prompt={prompt_text}")
        gen_btn.props(remove="disable loading")
        if status != 200:
            log.push(f"生成失败: {data}")
            ui.notify('图片生成失败', type='negative')
            return
        log.push(f"生成成功")
        ui.notify('图片生成成功', type='positive')
        gen_result.clear()
        url = data.get("url", "") or data.get("path", "") if isinstance(data, dict) else str(data)
        if url:
            with gen_result:
                base = get_base_url()
                full_url = url if url.startswith("http") else base + ("/" if not url.startswith("/") else "") + url
                ui.image(full_url).classes("w-64 rounded shadow")
        await load_images()

    async def load_images():
        generated_grid.clear()
        uploaded_grid.clear()

        status_g, data_g = await api_get("/api/v1/ppt/images/generated")
        if status_g == 200 and isinstance(data_g, list):
            base = get_base_url()
            for img in data_g:
                url = img.get("url", "") or img.get("path", "")
                img_id = img.get("id", "")
                with generated_grid:
                    with ui.card().classes("w-40"):
                        full = url if url.startswith("http") else base + ("/" if not url.startswith("/") else "") + url
                        ui.image(full).classes("w-full h-32 object-cover rounded")
                        with ui.row().classes("justify-between items-center"):
                            ui.label(str(img_id)[:8]).classes("text-xs text-gray-400")
                            ui.button(icon="delete", on_click=make_del_handler(img_id)).props("flat round dense color=negative size=sm")

        status_u, data_u = await api_get("/api/v1/ppt/images/uploaded")
        if status_u == 200 and isinstance(data_u, list):
            base = get_base_url()
            for img in data_u:
                url = img.get("url", "") or img.get("path", "")
                img_id = img.get("id", "")
                with uploaded_grid:
                    with ui.card().classes("w-40"):
                        full = url if url.startswith("http") else base + ("/" if not url.startswith("/") else "") + url
                        ui.image(full).classes("w-full h-32 object-cover rounded")
                        with ui.row().classes("justify-between items-center"):
                            ui.label(str(img_id)[:8]).classes("text-xs text-gray-400")
                            ui.button(icon="delete", on_click=make_del_handler(img_id)).props("flat round dense color=negative size=sm")

    async def del_img(img_id):
        status, _ = await api_delete(f"/api/v1/ppt/images/{img_id}")
        if status in (200, 204):
            log.push(f"已删除 {img_id}")
            ui.notify('图片已删除', type='positive')
        else:
            log.push(f"删除失败")
        await load_images()

    def make_del_handler(img_id):
        async def handler():
            await del_img(img_id)
        return handler

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("图片管理").classes("text-2xl font-bold")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            # AI 生成图片
            with ui.card().classes("w-96"):
                ui.label("AI 生成图片").classes("font-semibold mb-2")
                gen_prompt = ui.input("图片描述", placeholder="例如：未来科技城市全景").classes("w-full")
                gen_btn = ui.button("生成", icon="auto_awesome", on_click=gen_image).props("color=primary")
                gen_result = ui.column().classes("w-full mt-2")

            # 上传图片
            with ui.card().classes("w-96"):
                ui.label("上传图片").classes("font-semibold mb-2")

                async def handle_upload(e):
                    fd = aiohttp.FormData()
                    fd.add_field("file", e.content.read(), filename=e.name, content_type=e.type or "image/png")
                    status, data = await api_post_form("/api/v1/ppt/images/upload", fd)
                    if status == 200:
                        log.push(f"上传成功: {data}")
                        ui.notify('图片上传成功', type='positive')
                        await load_images()
                    else:
                        log.push(f"上传失败: {data}")
                        ui.notify('图片上传失败', type='negative')

                ui.upload(on_upload=handle_upload, auto_upload=True).props(
                    "accept='image/*' flat bordered"
                ).classes("w-full")

        # 浏览已有图片
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between"):
                ui.label("已有图片").classes("font-semibold")
                ui.button("刷新", icon="refresh", on_click=load_images).props("flat")

            with ui.tabs().classes("w-full") as img_tabs:
                tab_gen = ui.tab("AI 生成")
                tab_up = ui.tab("已上传")

            with ui.tab_panels(img_tabs, value=tab_gen).classes("w-full"):
                with ui.tab_panel(tab_gen):
                    generated_grid = ui.row().classes("w-full flex-wrap gap-4")
                with ui.tab_panel(tab_up):
                    uploaded_grid = ui.row().classes("w-full flex-wrap gap-4")

        log = ui.log().classes("h-24 w-full")

    ui.timer(0.3, load_images, once=True)
