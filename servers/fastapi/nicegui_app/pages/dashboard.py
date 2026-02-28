"""仪表板 — 所有演示文稿列表，支持搜索、查看、导出、删除。"""

from nicegui import ui, events
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post, api_delete


@ui.page("/dashboard")
def dashboard_page():
    page_layout("仪表板")
    state = {"selected": None, "all_rows": []}

    async def load():
        log.clear()
        status, data = await api_get("/api/v1/ppt/presentation/all")
        if status != 200:
            log.push(f"加载失败: {data}")
            ui.notify("加载失败", type="negative")
            return
        rows = []
        for item in data:
            content_raw = item.get("content") or ""
            rows.append({
                "id": item.get("id"),
                "title": item.get("title") or content_raw[:30] or str(item.get("id", ""))[:8],
                "content_preview": content_raw[:60] + ("…" if len(content_raw) > 60 else ""),
                "language": item.get("language", ""),
                "n_slides": item.get("n_slides", ""),
                "created_at": (item.get("created_at") or "").replace("T", " ").split(".")[0],
            })
        state["all_rows"] = rows
        _apply_filter()
        ui.notify(f"已加载 {len(rows)} 个演示文稿", type="positive")

    def _open_viewer():
        if state["selected"]:
            ui.navigate.to(f'/viewer?id={state["selected"]["id"]}')
        else:
            ui.notify("请先选择一条演示文稿", type="warning")

    async def _export_pptx():
        await _export("pptx")

    async def _export_pdf():
        await _export("pdf")

    async def _export(fmt: str):
        if not state["selected"]:
            ui.notify("请先选择一条演示文稿", type="warning")
            return
        pid = state["selected"]["id"]
        log.push(f"正在导出 {pid} 为 {fmt}…")
        status, data = await api_post("/api/v1/ppt/presentation/export", {"id": pid, "export_as": fmt})
        if status != 200:
            log.push(f"导出失败: {data}")
            ui.notify("导出失败", type="negative")
            return
        path = data.get("path", "")
        log.push(f"导出成功: {path}")
        ui.notify("导出成功", type="positive")
        from nicegui_app.api_client import get_base_url
        url = path if path.startswith("http") else get_base_url() + ("/" if not path.startswith("/") else "") + path
        ui.run_javascript(f'window.open("{url}", "_blank")')

    async def _delete():
        if not state["selected"]:
            ui.notify("请先选择一条演示文稿", type="warning")
            return
        pid = state["selected"]["id"]
        status, _ = await api_delete(f"/api/v1/ppt/presentation/{pid}")
        if status in (200, 204):
            ui.notify("删除成功", type="positive")
            await load()
        else:
            ui.notify("删除失败", type="negative")

    with ui.column().classes("w-full p-6 gap-4 max-w-6xl mx-auto"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("所有演示文稿").classes("text-2xl font-bold")
            with ui.row().classes("gap-2 items-center"):
                search_input = ui.input(placeholder="搜索标题/内容…").props("outlined dense clearable").classes("w-64")
                ui.button("刷新", icon="refresh", on_click=load).props("flat")
                with ui.link(target="/create"):
                    ui.button("新建", icon="add").props("color=primary")

        count_label = ui.label().classes("text-sm text-gray-500")

        table = ui.table(
            columns=[
                {"name": "title", "label": "标题", "field": "title", "align": "left", "sortable": True},
                {"name": "content_preview", "label": "内容摘要", "field": "content_preview", "align": "left"},
                {"name": "language", "label": "语言", "field": "language", "sortable": True},
                {"name": "n_slides", "label": "页数", "field": "n_slides", "sortable": True},
                {"name": "created_at", "label": "创建时间", "field": "created_at", "sortable": True},
            ],
            rows=[],
            row_key="id",
            selection="single",
            on_select=lambda e: _on_select(e),
            pagination={"rowsPerPage": 10, "sortBy": "created_at", "descending": True},
        ).props("dense flat bordered").classes("w-full")

        with ui.row().classes("gap-2"):
            ui.button("查看/编辑", icon="visibility", on_click=_open_viewer).props("outline")
            ui.button("导出 PPTX", icon="download", on_click=_export_pptx).props("outline")
            ui.button("导出 PDF", icon="picture_as_pdf", on_click=_export_pdf).props("outline")
            ui.button("删除", icon="delete", on_click=_delete).props("outline color=negative")

        log = ui.log().classes("h-20 w-full")

    def _on_select(e: events.TableSelectionEventArguments):
        state["selected"] = (e.selection or [None])[0] if e.selection else None

    def _apply_filter():
        q = (search_input.value or "").strip().lower()
        if not q:
            table.rows = state["all_rows"]
        else:
            table.rows = [r for r in state["all_rows"] if q in (r.get("title", "") + r.get("content_preview", "")).lower()]
        count_label.set_text(f"显示 {len(table.rows)} / {len(state['all_rows'])} 条")

    search_input.on("update:model-value", lambda: _apply_filter())

    ui.timer(0.2, load, once=True)
