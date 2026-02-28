"""大纲编辑 — 创建演示 → 流式生成大纲 → 编辑 → 保存。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_post, api_get, api_stream_sse, get_base_url
import aiohttp
import json


@ui.page("/outline")
def outline_page():
    page_layout("大纲编辑")
    state = {"pid": None, "editors": []}

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("演示大纲生成与编辑").classes("text-2xl font-bold")
        ui.label("步骤：创建演示 → 流式生成大纲 → 编辑每页 → 保存并导出").classes("text-gray-500 text-sm mb-2")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            # 左栏
            with ui.card().classes("flex-1 min-w-[400px]"):
                ui.label("1. 输入内容并生成大纲").classes("font-semibold")
                content_input = ui.textarea(placeholder="输入演示主题…").props("rows=4 outlined").classes("w-full")
                with ui.row().classes("gap-4"):
                    n_slides = ui.number("页数", value=8, min=1, max=30).classes("w-32")
                    lang = ui.input("语言", value="Chinese").classes("w-32")
                tone = ui.select(
                    {"default": "默认", "professional": "专业", "casual": "轻松", "educational": "教学"},
                    value="default", label="语气"
                ).classes("w-40")
                stream_log = ui.log().classes("h-36 w-full mt-2")

            # 右栏
            with ui.card().classes("flex-1 min-w-[400px]"):
                ui.label("2. 编辑大纲并保存").classes("font-semibold")
                title_input = ui.input("演示标题（可选）").classes("w-full")
                outline_container = ui.column().classes("w-full gap-2 max-h-[400px] overflow-auto")
                prepare_log = ui.log().classes("h-28 w-full mt-2")

        with ui.row().classes("gap-3"):
            stream_btn = ui.button("生成大纲", icon="bolt", on_click=lambda: stream_outlines()).props("color=primary")
            save_btn = ui.button("保存大纲", icon="save", on_click=lambda: save_outlines()).props("outline")
            export_select = ui.select({"pptx": "PPTX", "pdf": "PDF"}, value="pptx").classes("w-28")
            export_btn = ui.button("导出", icon="download", on_click=lambda: export_now()).props("color=positive")

    async def stream_outlines():
        stream_log.clear()
        outline_container.clear()
        state["pid"] = None
        state["editors"] = []

        if not (content_input.value or "").strip():
            stream_log.push("请输入内容")
            return

        stream_btn.props("disable loading")
        payload = {
            "content": content_input.value.strip(),
            "n_slides": int(n_slides.value or 8),
            "language": (lang.value or "Chinese").strip(),
            "tone": tone.value or "default",
            "verbosity": "standard",
            "include_table_of_contents": False,
            "include_title_slide": True,
            "web_search": False,
        }

        stream_log.push("创建演示…")
        status, created = await api_post("/api/v1/ppt/presentation/create", payload)
        if status != 200:
            stream_log.push(f"创建失败: {created}")
            stream_btn.props(remove="disable loading")
            return

        pid = created.get("id")
        state["pid"] = pid
        stream_log.push(f"ID = {pid}，正在流式生成大纲…")

        async for data in api_stream_sse(f"/api/v1/ppt/outlines/stream/{pid}"):
            if data.get("type") == "chunk":
                stream_log.push("收到大纲片段…")
                continue
            if data.get("key") == "presentation" and "value" in data:
                presentation = data["value"]
                outlines = (presentation.get("outlines") or {}).get("slides") or []
                state["editors"] = []
                outline_container.clear()
                for idx, slide in enumerate(outlines):
                    with outline_container:
                        ui.label(f"第 {idx+1} 页").classes("text-sm font-semibold mt-1")
                        ta = ui.textarea(value=slide.get("content", "")).props("rows=3 outlined").classes("w-full")
                        state["editors"].append(ta)
                stream_log.push(f"大纲生成完成，共 {len(outlines)} 页")
                break

        stream_btn.props(remove="disable loading")

    async def save_outlines():
        prepare_log.clear()
        if not state["pid"]:
            prepare_log.push("请先生成大纲")
            return
        if not state["editors"]:
            prepare_log.push("无可编辑大纲")
            return

        new_outlines = [{"content": e.value or ""} for e in state["editors"]]
        layout_payload = {"name": "general", "ordered": False, "slides": []}

        status_l, layout_json = await api_get("/api/v1/ppt/layouts/general")
        if status_l == 200 and isinstance(layout_json, dict):
            layout_payload = layout_json

        payload = {
            "presentation_id": state["pid"],
            "outlines": new_outlines,
            "layout": layout_payload,
            "title": title_input.value or None,
        }
        prepare_log.push("正在保存…")
        status, data = await api_post("/api/v1/ppt/presentation/prepare", payload)
        if status != 200:
            prepare_log.push(f"保存失败: {data}")
        else:
            prepare_log.push("大纲已保存!")

    async def export_now():
        if not state["pid"]:
            prepare_log.push("请先创建演示")
            return
        fmt = export_select.value or "pptx"
        prepare_log.push(f"正在导出为 {fmt}…")
        status, data = await api_post("/api/v1/ppt/presentation/export", {"id": state["pid"], "export_as": fmt})
        if status != 200:
            prepare_log.push(f"导出失败: {data}")
            return
        path = data.get("path", "")
        prepare_log.push(f"导出成功: {path}")
        base = get_base_url()
        url = path if path.startswith("http") else base + ("/" if not path.startswith("/") else "") + path
        ui.run_javascript(f'window.open("{url}", "_blank")')
