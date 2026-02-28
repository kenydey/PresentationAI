"""模板管理 — 保存、查看、删除演示文稿模板。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post, api_delete


@ui.page("/templates")
def templates_page():
    page_layout("模板管理")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("模板管理").classes("text-2xl font-bold")

        with ui.row().classes("items-center gap-3"):
            ui.button("刷新", icon="refresh", on_click=lambda: load_summary()).props("flat")

        # 模板概要
        with ui.card().classes("w-full"):
            summary_label = ui.label().classes("text-gray-500")
            template_container = ui.column().classes("w-full gap-3 mt-2")

        # 查看特定演示的模板
        with ui.card().classes("w-full"):
            ui.label("查看演示的布局模板").classes("font-semibold mb-2")
            with ui.row().classes("gap-3 items-center"):
                pres_id_input = ui.input("演示 ID").classes("w-96")
                ui.button("加载布局", icon="search", on_click=lambda: load_layouts()).props("outline")
            layout_container = ui.column().classes("w-full gap-2 mt-2 max-h-96 overflow-auto")

        log = ui.log().classes("h-24 w-full")

    async def load_summary():
        log.clear()
        status, data = await api_get("/api/v1/ppt/template-management/summary")
        if status != 200:
            log.push(f"加载失败: {data}")
            ui.notify('加载失败', type='negative')
            return
        total_p = data.get("total_presentations", 0)
        total_l = data.get("total_layouts", 0)
        summary_label.set_text(f"共 {total_p} 个演示文稿，{total_l} 个布局模板")

        presentations = data.get("presentations", [])
        template_container.clear()
        for p in presentations:
            with template_container:
                with ui.card().classes("w-full").props("flat bordered"):
                    with ui.row().classes("items-center justify-between"):
                        ui.label(p.get("name", "") or p.get("id", "")[:12]).classes("font-medium")
                        ui.label(f'{p.get("layout_count", 0)} 个布局').classes("text-sm text-gray-400")
                    if p.get("description"):
                        ui.label(p["description"]).classes("text-sm text-gray-500")
                    pid = p.get("id", "")
                    if pid:
                        ui.button("删除", icon="delete",
                                  on_click=lambda tid=pid: del_template(tid)).props("flat dense color=negative size=sm")

        log.push(f"已加载 {len(presentations)} 个模板")
        ui.notify(f'已加载 {len(presentations)} 个模板', type='positive')

    async def load_layouts():
        layout_container.clear()
        pid = pres_id_input.value.strip()
        if not pid:
            log.push("请输入演示 ID")
            return
        status, data = await api_get(f"/api/v1/ppt/template-management/get-templates/{pid}")
        if status != 200:
            log.push(f"加载布局失败: {data}")
            ui.notify('加载布局失败', type='negative')
            return
        layouts = data if isinstance(data, list) else data.get("layouts", []) if isinstance(data, dict) else []
        for idx, layout in enumerate(layouts):
            with layout_container:
                with ui.card().classes("w-full").props("flat bordered"):
                    ui.label(f"布局 {idx+1}").classes("font-semibold text-sm")
                    import json
                    ui.code(json.dumps(layout, indent=2, ensure_ascii=False)[:500], language="json").classes("text-xs")
        log.push(f"已加载 {len(layouts)} 个布局")

    async def del_template(template_id):
        status, _ = await api_delete(f"/api/v1/ppt/template-management/delete-templates/{template_id}")
        if status in (200, 204):
            log.push(f"已删除模板 {template_id}")
            ui.notify('模板已删除', type='positive')
            await load_summary()
        else:
            log.push(f"删除失败")

    ui.timer(0.3, load_summary, once=True)
