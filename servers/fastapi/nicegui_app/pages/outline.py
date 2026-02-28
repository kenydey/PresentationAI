"""大纲编辑 — 完全对齐后端 API：
  POST /presentation/create
  GET  /outlines/stream/{id}  (SSE: status / chunk / error / complete)
  GET  /layouts/{layout_name}
  POST /presentation/prepare
  POST /presentation/export
  GET  /presentation/{id}
"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_post, api_get, get_base_url
import aiohttp
import json

# 后端枚举值
TONE_OPTIONS = {
    "default": "默认", "casual": "轻松", "professional": "专业",
    "funny": "幽默", "educational": "教学", "sales_pitch": "推销",
}
VERBOSITY_OPTIONS = {"concise": "简洁", "standard": "标准", "text-heavy": "详细"}
TEMPLATE_OPTIONS = {"general": "通用", "modern": "现代", "standard": "标准", "swift": "简约"}


@ui.page("/outline")
def outline_page():
    page_layout("大纲编辑")
    state = {"pid": None, "editors": [], "presentation_data": None}

    with ui.column().classes("w-full p-6 gap-4 max-w-6xl mx-auto"):
        ui.label("演示大纲生成与编辑").classes("text-2xl font-bold")

        # ── 步骤提示 ──
        with ui.row().classes("gap-2 items-center text-sm text-gray-500"):
            for i, step in enumerate(["① 创建演示", "② 流式生成大纲", "③ 编辑每页大纲", "④ 保存并导出"], 1):
                ui.label(step).classes("bg-gray-100 rounded px-2 py-1")
                if i < 4:
                    ui.icon("arrow_forward").classes("text-gray-300")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            # ═══════════════ 左栏：创建与生成大纲 ═══════════════
            with ui.card().classes("flex-1 min-w-[420px]"):
                ui.label("步骤 1: 输入内容并生成大纲").classes("font-semibold text-[#6C63FF]")
                ui.separator().classes("mb-2")

                content_input = ui.textarea(
                    label="演示内容 (content) *",
                    placeholder="例如：介绍公司新产品的核心亮点、目标用户与市场机会……",
                ).props("rows=4 outlined").classes("w-full")

                with ui.row().classes("gap-4 w-full"):
                    n_slides = ui.number("页数 (n_slides)", value=8, min=1, max=50).classes("w-28")
                    lang = ui.input("语言 (language)", value="Chinese").classes("w-28")
                    tone = ui.select(TONE_OPTIONS, value="default", label="语气 (tone)").classes("w-36")

                with ui.row().classes("gap-4 w-full"):
                    verbosity = ui.select(VERBOSITY_OPTIONS, value="standard", label="详略 (verbosity)").classes("w-36")

                with ui.expansion("高级选项", icon="tune").classes("w-full"):
                    instructions_input = ui.textarea(
                        label="附加指令 (instructions)", placeholder="可选：对大纲生成的特殊要求…"
                    ).props("rows=2 outlined").classes("w-full")
                    include_toc = ui.checkbox("包含目录页 (include_table_of_contents)", value=False)
                    include_title = ui.checkbox("包含标题页 (include_title_slide)", value=True)
                    web_search = ui.checkbox("启用联网检索 (web_search)", value=False)

                # ── 日志区 ──
                stream_log = ui.log().classes("h-40 w-full mt-3")
                stream_status = ui.label().classes("text-sm")

            # ═══════════════ 右栏：编辑大纲与保存 ═══════════════
            with ui.card().classes("flex-1 min-w-[420px]"):
                ui.label("步骤 2: 编辑大纲并保存").classes("font-semibold text-[#6C63FF]")
                ui.separator().classes("mb-2")

                title_input = ui.input("演示标题 (title, 可选，留空自动推断)").classes("w-full")
                layout_select = ui.select(
                    TEMPLATE_OPTIONS, value="general", label="布局模板 (layout)"
                ).classes("w-48")

                # ── 大纲编辑容器 ──
                ui.label("编辑每页大纲内容:").classes("text-sm text-gray-500 mt-2")
                outline_container = ui.column().classes("w-full gap-2 max-h-[380px] overflow-auto border rounded p-2")
                with outline_container:
                    outline_placeholder = ui.label("尚未生成大纲，请先点击「生成大纲」").classes("text-gray-400 italic")

                # ── 保存日志区 ──
                prepare_log = ui.log().classes("h-28 w-full mt-3")
                prepare_status = ui.label().classes("text-sm")

        # ═══════════════ 操作按钮行 ═══════════════
        with ui.row().classes("gap-3 items-center flex-wrap"):
            stream_btn = ui.button("① 生成大纲", icon="bolt").props("color=primary")
            save_btn = ui.button("② 保存大纲", icon="save").props("outline")
            export_select = ui.select({"pptx": "PPTX", "pdf": "PDF"}, value="pptx").classes("w-28")
            export_btn = ui.button("③ 导出", icon="download").props("color=positive")
            with ui.row().classes("gap-2 items-center ml-4"):
                ui.label("演示 ID:").classes("text-xs text-gray-400")
                pid_label = ui.label("—").classes("text-xs font-mono text-gray-600")

    # ───────────── 生成大纲 (步骤 1) ─────────────
    async def do_stream_outlines():
        stream_log.clear()
        stream_status.set_text("")
        outline_container.clear()
        state["pid"] = None
        state["editors"] = []
        state["presentation_data"] = None
        pid_label.set_text("—")

        content_val = (content_input.value or "").strip()
        if not content_val:
            stream_log.push("✗ 请输入演示内容")
            return

        ns = int(n_slides.value or 8)
        if ns <= 0:
            stream_log.push("✗ 页数必须 > 0")
            return
        if include_toc.value and ns < 3:
            stream_log.push("✗ 包含目录页时页数不能少于 3")
            return

        stream_btn.props("disable loading")
        stream_status.set_text("正在创建演示…")

        # 1) POST /presentation/create
        create_payload = {
            "content": content_val,
            "n_slides": ns,
            "language": (lang.value or "Chinese").strip(),
            "tone": tone.value or "default",
            "verbosity": verbosity.value or "standard",
            "include_table_of_contents": bool(include_toc.value),
            "include_title_slide": bool(include_title.value),
            "web_search": bool(web_search.value),
        }
        inst = (instructions_input.value or "").strip()
        if inst:
            create_payload["instructions"] = inst

        stream_log.push(f"▶ POST /presentation/create  页数={ns} 语气={create_payload['tone']}")
        status, created = await api_post("/api/v1/ppt/presentation/create", create_payload)
        if status != 200:
            detail = created.get("detail", created) if isinstance(created, dict) else created
            stream_log.push(f"✗ 创建失败 (HTTP {status}): {detail}")
            stream_btn.props(remove="disable loading")
            stream_status.set_text("创建失败")
            return

        pid = created.get("id")
        state["pid"] = pid
        pid_label.set_text(str(pid)[:12] + "…")
        stream_log.push(f"✓ 演示已创建 ID = {pid}")

        # 2) GET /outlines/stream/{id} (SSE)
        stream_status.set_text("正在流式生成大纲…")
        stream_log.push(f"▶ SSE /outlines/stream/{pid}")

        base_url = get_base_url()
        sse_url = base_url + f"/api/v1/ppt/outlines/stream/{pid}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(sse_url) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        stream_log.push(f"✗ SSE 连接失败 (HTTP {resp.status}): {text[:200]}")
                        stream_btn.props(remove="disable loading")
                        stream_status.set_text("SSE 连接失败")
                        return

                    buf = ""
                    chunk_count = 0
                    async for raw_chunk, _ in resp.content.iter_chunks():
                        if not raw_chunk:
                            continue
                        buf += raw_chunk.decode("utf-8", errors="ignore")

                        while "\n\n" in buf:
                            block, buf = buf.split("\n\n", 1)
                            lines = [ln for ln in block.splitlines() if ln.strip()]
                            data_line = next((ln for ln in lines if ln.startswith("data:")), None)
                            if not data_line or len(data_line) <= 5:
                                continue
                            try:
                                data = json.loads(data_line[5:].strip())
                            except Exception:
                                continue

                            evt_type = data.get("type", "")

                            if evt_type == "status":
                                stream_log.push(f"  [状态] {data.get('status', '')}")
                                stream_status.set_text(data.get("status", ""))

                            elif evt_type == "chunk":
                                chunk_count += 1
                                if chunk_count <= 3 or chunk_count % 5 == 0:
                                    stream_log.push(f"  [片段 #{chunk_count}] {(data.get('chunk',''))[:60]}…")
                                stream_status.set_text(f"已收到 {chunk_count} 个片段…")

                            elif evt_type == "error":
                                detail = data.get("detail", "")
                                stream_log.push(f"✗ [错误] {detail}")
                                stream_status.set_text("生成出错")
                                stream_btn.props(remove="disable loading")
                                return

                            elif evt_type == "complete":
                                presentation = data.get("presentation", {})
                                state["presentation_data"] = presentation
                                outlines_obj = presentation.get("outlines") or {}
                                outlines = outlines_obj.get("slides") or []
                                auto_title = presentation.get("title", "")

                                if auto_title and not title_input.value:
                                    title_input.value = auto_title

                                _render_outline_editors(outlines)
                                stream_log.push(f"✓ 大纲生成完成，共 {len(outlines)} 页")
                                stream_status.set_text(f"大纲完成 ({len(outlines)} 页)")
                                stream_btn.props(remove="disable loading")
                                return

        except Exception as e:
            stream_log.push(f"✗ SSE 异常: {e}")
            stream_status.set_text("SSE 连接异常")

        stream_btn.props(remove="disable loading")

    def _render_outline_editors(outlines: list):
        outline_container.clear()
        state["editors"] = []
        if not outlines:
            with outline_container:
                ui.label("大纲为空").classes("text-gray-400 italic")
            return

        for idx, slide in enumerate(outlines):
            content = slide.get("content", "")
            with outline_container:
                with ui.row().classes("items-center gap-2 w-full"):
                    ui.badge(f"{idx+1}", color="primary").classes("text-xs")
                    ui.label(f"第 {idx+1} 页").classes("text-sm font-semibold")
                ta = ui.textarea(value=content).props("rows=3 outlined dense").classes("w-full")
                state["editors"].append(ta)

    stream_btn.on_click(do_stream_outlines)

    # ───────────── 保存大纲 (步骤 2) ─────────────
    async def do_save_outlines():
        prepare_log.clear()
        prepare_status.set_text("")

        if not state["pid"]:
            prepare_log.push("✗ 请先生成大纲（步骤 1）")
            return
        if not state["editors"]:
            prepare_log.push("✗ 无可编辑大纲内容")
            return

        empty_count = sum(1 for e in state["editors"] if not (e.value or "").strip())
        if empty_count:
            prepare_log.push(f"⚠ 有 {empty_count} 页大纲为空，将一并提交")

        save_btn.props("disable loading")
        prepare_status.set_text("正在保存…")

        new_outlines = [{"content": (e.value or "").strip()} for e in state["editors"]]
        prepare_log.push(f"▶ 收集大纲 {len(new_outlines)} 页")

        # 获取布局
        layout_name = layout_select.value or "general"
        prepare_log.push(f"▶ GET /layouts/{layout_name}")
        layout_payload = None

        status_l, layout_json = await api_get(f"/api/v1/ppt/layouts/{layout_name}")
        if status_l == 200 and isinstance(layout_json, dict) and layout_json.get("name"):
            layout_payload = layout_json
            prepare_log.push(f"  ✓ 布局已获取: {layout_json.get('name')} ({len(layout_json.get('slides',[]))} 种幻灯片)")
        else:
            prepare_log.push(f"  ⚠ 获取布局失败 (HTTP {status_l})，使用最小回退布局")
            layout_payload = {"name": layout_name, "ordered": False, "slides": []}

        # POST /presentation/prepare
        payload = {
            "presentation_id": state["pid"],
            "outlines": new_outlines,
            "layout": layout_payload,
            "title": (title_input.value or "").strip() or None,
        }
        prepare_log.push(f"▶ POST /presentation/prepare  title={payload['title']}")

        status, data = await api_post("/api/v1/ppt/presentation/prepare", payload)
        save_btn.props(remove="disable loading")

        if status != 200:
            detail = data.get("detail", data) if isinstance(data, dict) else data
            prepare_log.push(f"✗ 保存失败 (HTTP {status}): {detail}")
            prepare_status.set_text("保存失败")
            return

        state["presentation_data"] = data
        prepare_log.push("✓ 大纲与布局已保存到后端!")
        new_title = data.get("title", "")
        if new_title:
            prepare_log.push(f"  标题: {new_title}")
        prepare_status.set_text("已保存")

    save_btn.on_click(do_save_outlines)

    # ───────────── 导出 (步骤 3) ─────────────
    async def do_export():
        prepare_log.clear()
        prepare_status.set_text("")

        if not state["pid"]:
            prepare_log.push("✗ 请先创建演示并保存大纲")
            return

        fmt = export_select.value or "pptx"
        export_btn.props("disable loading")
        prepare_status.set_text(f"正在导出为 {fmt}…")
        prepare_log.push(f"▶ POST /presentation/export  id={state['pid']}  format={fmt}")

        status, data = await api_post(
            "/api/v1/ppt/presentation/export",
            {"id": state["pid"], "export_as": fmt},
        )
        export_btn.props(remove="disable loading")

        if status != 200:
            detail = data.get("detail", data) if isinstance(data, dict) else data
            prepare_log.push(f"✗ 导出失败 (HTTP {status}): {detail}")
            prepare_status.set_text("导出失败")
            return

        path = data.get("path", "")
        edit_path = data.get("edit_path", "")
        prepare_log.push(f"✓ 导出成功!")
        if path:
            prepare_log.push(f"  文件: {path}")
        if edit_path:
            prepare_log.push(f"  编辑: {edit_path}")
        prepare_status.set_text("导出完成")

        if path:
            base = get_base_url()
            url = path if path.startswith("http") else base + ("/" if not path.startswith("/") else "") + path
            ui.run_javascript(f'window.open("{url}", "_blank")')

    export_btn.on_click(do_export)
