"""演示查看/编辑 — 查看幻灯片列表，编辑单页内容。"""

from nicegui import ui, app
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post, api_patch
import json


@ui.page("/viewer")
def viewer_page(id: str = ""):
    page_layout("演示查看")
    state = {"pid": id, "slides": [], "current": 0}

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("演示文稿查看/编辑").classes("text-2xl font-bold")

        with ui.row().classes("gap-3 items-center"):
            pid_input = ui.input("演示 ID", value=id).classes("w-96")
            load_btn = ui.button("加载", icon="download", on_click=lambda: load_pres()).props("color=primary")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            # 左栏：幻灯片列表
            with ui.card().classes("w-64"):
                ui.label("幻灯片列表").classes("font-semibold mb-2")
                slide_list = ui.column().classes("w-full gap-1 max-h-[500px] overflow-auto")

            # 右栏：当前幻灯片详情
            with ui.card().classes("flex-1 min-w-[400px]"):
                slide_title = ui.label("选择一个幻灯片").classes("font-semibold text-lg")
                slide_meta = ui.label().classes("text-xs text-gray-400")

                with ui.tabs().classes("w-full") as tabs:
                    tab_content = ui.tab("内容")
                    tab_html = ui.tab("HTML")
                    tab_raw = ui.tab("原始 JSON")
                    tab_note = ui.tab("讲稿")

                with ui.tab_panels(tabs, value=tab_content).classes("w-full"):
                    with ui.tab_panel(tab_content):
                        content_display = ui.column().classes("w-full gap-2")
                    with ui.tab_panel(tab_html):
                        html_display = ui.html("", sanitize=False).classes("w-full border rounded p-4 bg-white")
                    with ui.tab_panel(tab_raw):
                        raw_display = ui.code("", language="json").classes("w-full max-h-80 overflow-auto")
                    with ui.tab_panel(tab_note):
                        note_display = ui.label("").classes("w-full whitespace-pre-wrap")

                with ui.row().classes("gap-2 mt-3"):
                    edit_prompt = ui.input("编辑指令（如：让内容更简洁）").classes("flex-1")
                    edit_btn = ui.button("AI 编辑此页", icon="edit", on_click=lambda: edit_slide()).props("outline")

        log = ui.log().classes("h-24 w-full")

    async def load_pres():
        log.clear()
        pid = pid_input.value.strip()
        if not pid:
            log.push("请输入演示 ID")
            return
        state["pid"] = pid
        log.push(f"加载 {pid}…")
        status, data = await api_get(f"/api/v1/ppt/presentation/{pid}")
        if status != 200:
            log.push(f"加载失败: {data}")
            ui.notify('加载失败', type='negative')
            return
        slides = data.get("slides", [])
        state["slides"] = slides
        slide_list.clear()

        for idx, s in enumerate(slides):
            lbl = s.get("layout", "") or f"Slide {idx+1}"
            with slide_list:
                ui.button(
                    f"{idx+1}. {lbl[:25]}",
                    on_click=lambda i=idx: show_slide(i),
                ).props("flat dense align=left").classes("w-full text-left")

        log.push(f"已加载 {len(slides)} 页幻灯片")
        ui.notify(f'已加载 {len(slides)} 页幻灯片', type='positive')
        if slides:
            show_slide(0)

    def show_slide(idx: int):
        if idx >= len(state["slides"]):
            return
        state["current"] = idx
        s = state["slides"][idx]
        slide_title.set_text(f"第 {idx+1} 页 — {s.get('layout', '')}")
        slide_meta.set_text(f"ID: {s.get('id', '')}  |  布局组: {s.get('layout_group', '')}  |  索引: {s.get('index', '')}")

        # content tab
        content_display.clear()
        content = s.get("content", {})
        if isinstance(content, dict):
            for key, val in content.items():
                with content_display:
                    ui.label(key).classes("font-medium text-sm text-gray-600")
                    if isinstance(val, str):
                        ui.label(val).classes("text-sm mb-2")
                    elif isinstance(val, list):
                        for item in val:
                            if isinstance(item, dict):
                                ui.label(f"  • {json.dumps(item, ensure_ascii=False)[:120]}").classes("text-xs text-gray-500")
                            else:
                                ui.label(f"  • {item}").classes("text-sm")
                    else:
                        ui.label(str(val)[:200]).classes("text-xs text-gray-500")
        else:
            with content_display:
                ui.label(str(content)[:500]).classes("text-sm")

        # HTML tab
        html_content = s.get("html_content", "") or ""
        html_display.content = html_content if html_content else "<p class='text-gray-400'>暂无 HTML 内容</p>"

        # raw JSON tab
        raw_display.content = json.dumps(s, indent=2, ensure_ascii=False)[:5000]

        # speaker note tab
        note_display.set_text(s.get("speaker_note", "") or "暂无讲稿")

    async def edit_slide():
        if not state["slides"]:
            log.push("请先加载演示")
            return
        prompt_text = edit_prompt.value.strip()
        if not prompt_text:
            log.push("请输入编辑指令")
            return
        s = state["slides"][state["current"]]
        sid = s.get("id")
        log.push(f"正在编辑第 {state['current']+1} 页…")

        status, data = await api_post("/api/v1/ppt/slide/edit", {"id": sid, "prompt": prompt_text})
        if status != 200:
            log.push(f"编辑失败: {data}")
            ui.notify('编辑失败', type='negative')
            return
        log.push("编辑成功，重新加载…")
        ui.notify('编辑成功', type='positive')
        await load_pres()

    if id:
        ui.timer(0.3, load_pres, once=True)
