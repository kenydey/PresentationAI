"""演示查看/编辑 — 查看幻灯片列表，编辑单页内容，Vibe 对话式编辑。"""

from nicegui import ui, app
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post, api_patch
from nicegui_app.utils.slide_preview_data import (
    slide_to_preview_data,
    slide_state_to_preview_data,
)
from nicegui_app.components.slide_preview import render_slide_preview_html
from utils.state_mapper import slides_to_presentation_state
import json


@ui.page("/viewer")
def viewer_page(id: str = ""):
    page_layout("演示查看")
    state = {
        "pid": id,
        "slides": [],
        "presentation_state": None,
        "current": 0,
        "_vibe_history": [],
    }

    def _refresh_slide_list():
        slide_list.clear()
        ps = state.get("presentation_state")
        slides = state.get("slides") or []
        n = len(slides) if slides else (len(ps.get("slides", [])) if ps else 0)
        for idx in range(n):
            if ps and ps.get("slides") and idx < len(ps["slides"]):
                lbl = (ps["slides"][idx].get("title") or "")[:25] or ps["slides"][idx].get("layout_id", "")
            elif idx < len(slides):
                s = slides[idx]
                content = s.get("content") or {}
                lbl = (content.get("title") or content.get("heading") or s.get("layout") or "")[:25]
            else:
                lbl = f"Slide {idx+1}"
            with slide_list:
                ui.button(
                    f"{idx+1}. {lbl}" if lbl else f"{idx+1}. Slide",
                    on_click=lambda i=idx: show_slide(i),
                ).props("flat dense align=left").classes("w-full text-left")

    async def load_pres():
        log.clear()
        vibe_chat_container.clear()
        state["presentation_state"] = None
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
        try:
            state["presentation_state"] = slides_to_presentation_state(
                slides, title=data.get("title")
            ).model_dump(exclude_none=True)
        except Exception as e:
            log.push(f"构建状态失败: {e}")
        _refresh_slide_list()

        log.push(f"已加载 {len(slides)} 页幻灯片")
        ui.notify(f'已加载 {len(slides)} 页幻灯片', type='positive')
        vibe_send_btn.set_enabled(True)
        if slides:
            show_slide(0)

    def _get_preview_data(idx: int):
        ps = state.get("presentation_state")
        slides = state.get("slides") or []
        if ps and ps.get("slides") and idx < len(ps["slides"]):
            ss = ps["slides"][idx]
            img_url = None
            if idx < len(slides):
                content = slides[idx].get("content") or {}
                img_obj = content.get("image") or content.get("backgroundImage") or {}
                if isinstance(img_obj, dict):
                    img_url = img_obj.get("__image_url__") or img_obj.get("url")
            return slide_state_to_preview_data(ss, image_url=img_url)
        if idx < len(slides):
            return slide_to_preview_data(slides[idx])
        return {"title": "无标题", "bullet_points": [], "layout_id": "basic-info-slide"}

    def show_slide(idx: int):
        slides = state.get("slides") or []
        ps = state.get("presentation_state")
        n = len(ps.get("slides", [])) if ps else len(slides)
        if idx >= n:
            return
        state["current"] = idx
        s = slides[idx] if idx < len(slides) else {}
        slide_title.set_text(
            f"第 {idx+1} 页 — "
            + (ps["slides"][idx].get("layout_id", "") if ps and ps.get("slides") and idx < len(ps["slides"]) else s.get("layout", ""))
        )
        slide_meta.set_text(f"ID: {s.get('id', '')}  |  布局组: {s.get('layout_group', '')}  |  索引: {s.get('index', '')}")

        # preview tab — 基于 PresentationState 的实时预览（无刷新更新）
        preview_data = _get_preview_data(idx)
        preview_html.content = render_slide_preview_html(preview_data)

        # content tab (field list)
        content = (s.get("content") or {}) if s else {}
        content_display.clear()
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
        html_content = (s.get("html_content") or "") if s else ""
        html_display.content = html_content if html_content else "<p class='text-gray-400'>暂无 HTML 内容</p>"

        # raw JSON tab
        raw_display.content = json.dumps(s or {}, indent=2, ensure_ascii=False)[:5000]

        # speaker note tab
        note_display.set_text((s.get("speaker_note") or "暂无讲稿") if s else "暂无讲稿")

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

    async def send_vibe():
        if not state.get("presentation_state") and not state.get("slides"):
            ui.notify("请先加载演示", type="warning")
            return
        inst = (vibe_input.value or "").strip()
        if not inst:
            ui.notify("请输入编辑指令", type="warning")
            return
        vibe_send_btn.set_enabled(False)
        with vibe_chat_container:
            ui.chat_message(inst, name="我", sent=True)
            ui.chat_message("正在处理…", name="Vibe")
        vibe_input.value = ""

        payload = {
            "instruction": inst,
            "language": "Chinese",
        }
        if state.get("presentation_state"):
            payload["presentation_state"] = state["presentation_state"]
        else:
            payload["slides"] = state.get("slides", [])

        status, data = await api_post("/api/v1/ppt/vibe/edit", payload)

        if status != 200:
            err_msg = data.get("detail", str(data)) if isinstance(data, dict) else str(data)
            state["_vibe_history"] = state.get("_vibe_history", []) + [
                {"text": inst, "name": "我", "sent": True},
                {"text": f"❌ 修改失败: {err_msg}", "name": "Vibe"},
            ]
            vibe_chat_container.clear()
            for entry in state["_vibe_history"]:
                with vibe_chat_container:
                    ui.chat_message(entry["text"], name=entry["name"], sent=entry.get("sent", False))
            vibe_send_btn.set_enabled(True)
            ui.notify("修改失败", type="negative")
            return

        new_ps = data.get("presentation_state", {})
        state["presentation_state"] = new_ps
        state["_vibe_history"] = state.get("_vibe_history", []) + [
            {"text": inst, "name": "我", "sent": True},
            {"text": "✓ 已按指令修改", "name": "Vibe"},
        ]
        vibe_chat_container.clear()
        for entry in state["_vibe_history"]:
            with vibe_chat_container:
                ui.chat_message(entry["text"], name=entry["name"], sent=entry.get("sent", False))
        _refresh_slide_list()
        show_slide(state["current"])
        vibe_send_btn.set_enabled(True)
        ui.notify("已按指令修改", type="positive")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("演示文稿查看/编辑").classes("text-2xl font-bold")

        with ui.row().classes("gap-3 items-center"):
            pid_input = ui.input("演示 ID", value=id).classes("w-96")
            load_btn = ui.button("加载", icon="download", on_click=load_pres).props("color=primary")

        with ui.row().classes("w-full gap-6 items-start"):
            # 左栏：幻灯片列表
            with ui.card().classes("w-64 shrink-0"):
                ui.label("幻灯片列表").classes("font-semibold mb-2")
                slide_list = ui.column().classes("w-full gap-1 max-h-[600px] overflow-auto")

            # 主区域：预览（放大） + 其他标签页
            with ui.card().classes("flex-1 min-w-0"):
                slide_title = ui.label("选择一个幻灯片").classes("font-semibold text-lg")
                slide_meta = ui.label().classes("text-xs text-gray-400")

                with ui.tabs().classes("w-full") as tabs:
                    tab_preview = ui.tab("预览")
                    tab_content = ui.tab("字段")
                    tab_html = ui.tab("HTML")
                    tab_raw = ui.tab("JSON")
                    tab_note = ui.tab("讲稿")

                with ui.tab_panels(tabs, value=tab_preview).classes("w-full"):
                    with ui.tab_panel(tab_preview):
                        _empty_html = (
                            '<div class="flex items-center justify-center w-full min-h-[480px] '
                            'bg-gray-100 text-gray-400 rounded-xl">选择幻灯片以预览</div>'
                        )
                        preview_html = ui.html(_empty_html, sanitize=False).classes(
                            "w-full overflow-hidden rounded-xl shadow-lg bg-white"
                        ).style("aspect-ratio: 16/9; min-height: 420px;")
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
                    edit_btn = ui.button("AI 编辑此页", icon="edit", on_click=edit_slide).props("outline")

        # Vibe 编辑：移到预览区域下方
        with ui.card().classes("w-full mt-4"):
            ui.label("Vibe 编辑").classes("font-semibold mb-2")
            ui.label("用自然语言修改演示，如：「把第三页改成案例分析并换成左右排版」").classes(
                "text-xs text-gray-500 mb-2"
            )
            vibe_chat_container = ui.column().classes(
                "w-full gap-2 max-h-[200px] overflow-auto border rounded p-2 bg-gray-50"
            )
            with ui.row().classes("w-full gap-2 mt-2"):
                vibe_input = ui.input(placeholder="输入编辑指令").classes("flex-1")
                vibe_send_btn = ui.button("发送", icon="send", on_click=send_vibe).props(
                    "color=primary flat"
                )
            vibe_send_btn.set_enabled(False)

        log = ui.log().classes("h-24 w-full")

    if id:
        ui.timer(0.3, load_pres, once=True)
