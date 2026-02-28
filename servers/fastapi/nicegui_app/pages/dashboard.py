"""仪表板 — 所有演示文稿列表，支持查看、导出、删除。"""

from nicegui import ui, events
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post, api_delete


@ui.page("/dashboard")
def dashboard_page():
    page_layout("仪表板")
    state = {"selected": None}

    with ui.column().classes("w-full p-6 gap-4"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("所有演示文稿").classes("text-2xl font-bold")
            with ui.row().classes("gap-2"):
                ui.button("刷新", icon="refresh", on_click=lambda: load()).props("flat")
                with ui.link(target="/create"):
                    ui.button("新建", icon="add").props("color=primary")

        table = ui.table(
            columns=[
                {"name": "title", "label": "标题", "field": "title", "align": "left", "sortable": True},
                {"name": "language", "label": "语言", "field": "language", "sortable": True},
                {"name": "n_slides", "label": "页数", "field": "n_slides", "sortable": True},
                {"name": "created_at", "label": "创建时间", "field": "created_at", "sortable": True},
            ],
            rows=[],
            row_key="id",
            selection="single",
            on_select=lambda e: _on_select(e),
        ).props("dense flat bordered").classes("w-full")

        with ui.row().classes("gap-2"):
            ui.button("查看/编辑", icon="visibility", on_click=lambda: _open_viewer()).props("outline")
            ui.button("导出 PPTX", icon="download", on_click=lambda: _export("pptx")).props("outline")
            ui.button("导出 PDF", icon="picture_as_pdf", on_click=lambda: _export("pdf")).props("outline")
            ui.button("删除", icon="delete", on_click=lambda: _delete()).props("outline color=negative")

        log = ui.log().classes("h-28 w-full")

    def _on_select(e: events.TableSelectionEventArguments):
        state["selected"] = (e.selection or [None])[0] if e.selection else None

    async def load():
        log.clear()
        log.push("正在加载…")
        status, data = await api_get("/api/v1/ppt/presentation/all")
        if status != 200:
            log.push(f"加载失败: {data}")
            return
        rows = []
        for item in data:
            rows.append({
                "id": item.get("id"),
                "title": item.get("title") or (item.get("content") or "")[:40] or str(item.get("id"))[:8],
                "language": item.get("language", ""),
                "n_slides": item.get("n_slides", ""),
                "created_at": (item.get("created_at") or "").replace("T", " ").split(".")[0],
            })
        table.rows = rows
        log.push(f"已加载 {len(rows)} 个演示文稿")

    def _open_viewer():
        if state["selected"]:
            ui.navigate.to(f'/viewer?id={state["selected"]["id"]}')
        else:
            log.push("请先选择一条演示文稿")

    async def _export(fmt: str):
        if not state["selected"]:
            log.push("请先选择一条演示文稿")
            return
        pid = state["selected"]["id"]
        log.push(f"正在导出 {pid} 为 {fmt}…")
        status, data = await api_post("/api/v1/ppt/presentation/export", {"id": pid, "export_as": fmt})
        if status != 200:
            log.push(f"导出失败: {data}")
            return
        path = data.get("path", "")
        log.push(f"导出成功: {path}")
        from nicegui_app.api_client import get_base_url
        url = path if path.startswith("http") else get_base_url() + ("/" if not path.startswith("/") else "") + path
        ui.run_javascript(f'window.open("{url}", "_blank")')

    async def _delete():
        if not state["selected"]:
            log.push("请先选择一条演示文稿")
            return
        pid = state["selected"]["id"]
        status, _ = await api_delete(f"/api/v1/ppt/presentation/{pid}")
        if status in (200, 204):
            log.push(f"已删除 {pid}")
            await load()
        else:
            log.push(f"删除失败")

    ui.timer(0.2, load, once=True)
