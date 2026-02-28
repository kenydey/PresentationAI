"""创建演示文稿 — 完全对齐后端 /presentation/generate、/generate/async、/files/upload API。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_post, api_post_form, api_get, get_base_url
import aiohttp
import asyncio

# 后端枚举值 (enums/tone.py, enums/verbosity.py)
TONE_OPTIONS = {
    "default": "默认 (default)",
    "casual": "轻松 (casual)",
    "professional": "专业 (professional)",
    "funny": "幽默 (funny)",
    "educational": "教学 (educational)",
    "sales_pitch": "推销 (sales_pitch)",
}
VERBOSITY_OPTIONS = {
    "concise": "简洁 (concise)",
    "standard": "标准 (standard)",
    "text-heavy": "详细 (text-heavy)",
}
# 后端 constants/presentation.py DEFAULT_TEMPLATES
TEMPLATE_OPTIONS = {
    "general": "通用 (general)",
    "modern": "现代 (modern)",
    "standard": "标准 (standard)",
    "swift": "简约 (swift)",
}
EXPORT_OPTIONS = {"pptx": "PPTX", "pdf": "PDF"}


@ui.page("/create")
def create_page():
    page_layout("创建演示文稿")
    state = {"file_paths": [], "async_task_id": None}

    with ui.column().classes("w-full p-6 gap-4 max-w-6xl mx-auto"):
        ui.label("从提示词生成演示文稿").classes("text-2xl font-bold")
        ui.label(
            "至少填写「演示内容」、「Markdown 幻灯片」、「附件文档」三者之一。"
        ).classes("text-gray-500 text-sm")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            # ═══════════════════ 左栏：内容输入 ═══════════════════
            with ui.card().classes("flex-1 min-w-[420px]"):
                # ── 主要内容 ──
                ui.label("演示内容 (content)").classes("font-semibold mb-1")
                prompt = ui.textarea(
                    placeholder="例如：介绍人工智能的核心概念、发展历史与典型应用场景……"
                ).props("rows=5 outlined").classes("w-full")

                # ── Markdown 幻灯片（可选） ──
                with ui.expansion("Markdown 幻灯片 (slides_markdown)", icon="code").classes("w-full mt-2"):
                    ui.label("每行一页幻灯片的 Markdown 内容，留空则由 AI 自动生成").classes("text-xs text-gray-400 mb-1")
                    slides_md = ui.textarea(
                        placeholder="# 第一页标题\n内容要点…\n---\n# 第二页标题\n内容…"
                    ).props("rows=4 outlined").classes("w-full")

                # ── 附加指令 ──
                with ui.expansion("附加指令 (instructions)", icon="edit_note").classes("w-full"):
                    instructions_input = ui.textarea(
                        placeholder="例如：重点突出技术优势，使用图表说明市场数据……"
                    ).props("rows=3 outlined").classes("w-full")

                # ── 文件上传 ──
                ui.separator().classes("my-2")
                ui.label("附件文档 (files)").classes("font-semibold mb-1")
                ui.label("支持 PDF、DOCX、DOC、TXT、PPTX，单文件最大 100MB").classes("text-xs text-gray-400 mb-1")

                file_list_container = ui.column().classes("w-full gap-1")

                async def handle_upload(e):
                    fd = aiohttp.FormData()
                    fd.add_field(
                        "files", e.content.read(),
                        filename=e.name,
                        content_type=e.type or "application/octet-stream",
                    )
                    log.push(f"正在上传: {e.name} …")
                    status, data = await api_post_form("/api/v1/ppt/files/upload", fd)
                    if status == 200 and isinstance(data, list):
                        state["file_paths"].extend(data)
                        log.push(f"✓ 已上传: {e.name} → {data}")
                        ui.notify(f'{e.name} 上传成功', type='positive')
                        _refresh_file_list()
                    else:
                        detail = data.get("detail", data) if isinstance(data, dict) else data
                        log.push(f"✗ 上传失败 ({e.name}): {detail}")
                        ui.notify(f'上传失败: {detail}', type='negative')

                ui.upload(
                    on_upload=handle_upload, multiple=True, auto_upload=True
                ).props("accept='.pdf,.docx,.doc,.txt,.pptx' flat bordered").classes("w-full")

                def _refresh_file_list():
                    file_list_container.clear()
                    if not state["file_paths"]:
                        return
                    with file_list_container:
                        for idx, fp in enumerate(state["file_paths"]):
                            with ui.row().classes("items-center gap-2 bg-gray-50 rounded px-2 py-1"):
                                ui.icon("description").classes("text-[#6C63FF] text-sm")
                                ui.label(fp.split("/")[-1] if "/" in fp else fp).classes("text-sm flex-1 truncate")

                                def _remove(i=idx):
                                    state["file_paths"].pop(i)
                                    _refresh_file_list()

                                ui.button(icon="close", on_click=_remove).props("flat round dense size=xs color=negative")

                def _clear_files():
                    state["file_paths"].clear()
                    _refresh_file_list()
                    log.push("已清空附件列表")

                ui.button("清空附件", icon="delete_sweep", on_click=_clear_files).props("flat dense size=sm color=grey")

            # ═══════════════════ 右栏：参数配置 ═══════════════════
            with ui.card().classes("w-80"):
                ui.label("生成参数").classes("font-semibold mb-2")

                n_slides = ui.number("幻灯片数量 (n_slides)", value=8, min=1, max=50).classes("w-full")
                language = ui.input("语言 (language)", value="Chinese").classes("w-full")
                template = ui.select(TEMPLATE_OPTIONS, value="general", label="模板 (template)").classes("w-full")
                export_as = ui.select(EXPORT_OPTIONS, value="pptx", label="导出格式 (export_as)").classes("w-full")
                tone = ui.select(TONE_OPTIONS, value="default", label="语气 (tone)").classes("w-full")
                verbosity = ui.select(VERBOSITY_OPTIONS, value="standard", label="详略 (verbosity)").classes("w-full")

                ui.separator().classes("my-2")
                include_toc = ui.checkbox("包含目录页 (include_table_of_contents)", value=False)
                include_title = ui.checkbox("包含标题页 (include_title_slide)", value=True)
                web_search = ui.checkbox("启用联网检索 (web_search)", value=False)
                trigger_webhook = ui.checkbox("触发 Webhook (trigger_webhook)", value=False)

        # ═══════════════════ 操作按钮 ═══════════════════
        with ui.row().classes("gap-3 items-center flex-wrap"):
            gen_btn = ui.button("同步生成", icon="auto_awesome").props("color=primary")
            async_btn = ui.button("异步生成", icon="schedule").props("outline color=primary")
            status_btn = ui.button("查询异步状态", icon="sync").props("flat")
            task_id_input = ui.input("异步任务 ID").classes("w-64").bind_value_from(
                state, "async_task_id", lambda v: v or ""
            )

        # ═══════════════════ 日志和结果 ═══════════════════
        log = ui.log().classes("h-48 w-full")
        with ui.row().classes("gap-4 items-center"):
            result_label = ui.label().classes("text-green-600 font-medium")
            result_link = ui.link("", target="").classes("hidden")

        # ────────────── 构造请求体 ──────────────
        def _build_payload() -> dict | None:
            """根据表单构造 GeneratePresentationRequest，返回 None 表示校验失败。"""
            content_val = (prompt.value or "").strip()
            md_lines = [ln.strip() for ln in (slides_md.value or "").strip().split("---") if ln.strip()]
            files_val = state["file_paths"]

            if not content_val and not md_lines and not files_val:
                log.push("✗ 验证失败: 至少填写「演示内容」、「Markdown 幻灯片」、「附件文档」三者之一")
                return None

            ns = int(n_slides.value or 8)
            if ns <= 0:
                log.push("✗ 验证失败: 幻灯片数量必须 > 0")
                return None
            if include_toc.value and ns < 3:
                log.push("✗ 验证失败: 包含目录页时幻灯片数量不能少于 3")
                return None

            payload = {
                "content": content_val or " ",
                "n_slides": ns,
                "language": (language.value or "English").strip(),
                "template": template.value or "general",
                "export_as": export_as.value or "pptx",
                "tone": tone.value or "default",
                "verbosity": verbosity.value or "standard",
                "include_table_of_contents": bool(include_toc.value),
                "include_title_slide": bool(include_title.value),
                "web_search": bool(web_search.value),
                "trigger_webhook": bool(trigger_webhook.value),
            }
            if md_lines:
                payload["slides_markdown"] = md_lines
            if files_val:
                payload["files"] = files_val
            inst = (instructions_input.value or "").strip()
            if inst:
                payload["instructions"] = inst
            return payload

        def _show_result(data: dict):
            pid = data.get("presentation_id") or data.get("id")
            path = data.get("path", "")
            edit_path = data.get("edit_path", "")
            log.push(f"✓ 演示 ID = {pid}")
            if path:
                log.push(f"  文件路径: {path}")
            if edit_path:
                log.push(f"  编辑链接: {edit_path}")
            result_label.set_text("演示文稿已生成!")
            ui.notify('演示文稿生成成功', type='positive')
            if path:
                base = get_base_url()
                url = path if path.startswith("http") else base + ("/" if not path.startswith("/") else "") + path
                ui.run_javascript(f'window.open("{url}", "_blank")')

        # ────────────── 同步生成 ──────────────
        async def do_generate():
            log.clear()
            result_label.set_text("")
            payload = _build_payload()
            if payload is None:
                return
            gen_btn.props("disable loading")
            log.push(f"▶ 同步生成中… 模板={payload['template']}  页数={payload['n_slides']}  格式={payload['export_as']}")
            ui.notify('正在生成演示文稿，请稍候…', type='info')
            try:
                status, data = await api_post("/api/v1/ppt/presentation/generate", payload)
            except Exception as e:
                log.push(f"✗ 请求异常: {e}")
                ui.notify('请求异常', type='negative')
                gen_btn.props(remove="disable loading")
                return
            gen_btn.props(remove="disable loading")

            if status != 200:
                detail = data.get("detail", data) if isinstance(data, dict) else str(data)
                if isinstance(detail, list):
                    detail = "; ".join(str(d.get("msg", d)) for d in detail)
                log.push(f"✗ 生成失败 (HTTP {status}): {detail}")
                ui.notify(f'生成失败: {detail}', type='negative')
                result_label.set_text("生成失败，请查看日志")
                return
            _show_result(data)

        gen_btn.on_click(do_generate)

        # ────────────── 异步生成 ──────────────
        async def do_generate_async():
            log.clear()
            result_label.set_text("")
            payload = _build_payload()
            if payload is None:
                return
            async_btn.props("disable loading")
            log.push(f"▶ 异步生成中… 模板={payload['template']}  页数={payload['n_slides']}")
            try:
                status, data = await api_post("/api/v1/ppt/presentation/generate/async", payload)
            except Exception as e:
                log.push(f"✗ 请求异常: {e}")
                async_btn.props(remove="disable loading")
                return
            async_btn.props(remove="disable loading")

            if status != 200:
                detail = data.get("detail", data) if isinstance(data, dict) else str(data)
                if isinstance(detail, list):
                    detail = "; ".join(str(d.get("msg", d)) for d in detail)
                log.push(f"✗ 提交失败 (HTTP {status}): {detail}")
                ui.notify(f'提交失败: {detail}', type='negative')
                return

            task_id = data.get("id", "")
            task_status = data.get("status", "")
            state["async_task_id"] = task_id
            task_id_input.value = task_id
            log.push(f"✓ 异步任务已提交: id={task_id}  status={task_status}")
            ui.notify('异步任务已提交', type='positive')
            log.push("  点击「查询异步状态」按钮查看进度，或等待自动完成。")
            result_label.set_text(f"异步任务 {task_id} 已提交")

        async_btn.on_click(do_generate_async)

        # ────────────── 查询异步状态 ──────────────
        async def do_check_status():
            tid = (task_id_input.value or "").strip()
            if not tid:
                log.push("请输入或等待异步任务 ID")
                return
            status_btn.props("disable loading")
            log.push(f"▶ 查询任务 {tid} …")
            try:
                status, data = await api_get(f"/api/v1/ppt/presentation/status/{tid}")
            except Exception as e:
                log.push(f"✗ 查询异常: {e}")
                ui.notify('查询异常', type='negative')
                status_btn.props(remove="disable loading")
                return
            status_btn.props(remove="disable loading")

            if status != 200:
                log.push(f"✗ 查询失败 (HTTP {status}): {data}")
                ui.notify('查询失败', type='negative')
                return

            task_status = data.get("status", "")
            message = data.get("message", "")
            log.push(f"  状态: {task_status}  消息: {message}")

            if task_status == "completed":
                result_data = data.get("data", {})
                if isinstance(result_data, dict):
                    _show_result(result_data)
                else:
                    log.push(f"  完成数据: {result_data}")
                result_label.set_text("异步生成已完成!")
                ui.notify('异步生成已完成', type='positive')
            elif task_status == "error":
                error = data.get("error", {})
                log.push(f"  错误: {error}")
                result_label.set_text("异步生成出错")
                ui.notify('异步生成出错', type='negative')
            else:
                log.push(f"  任务仍在进行中…（可继续点击查询）")
                result_label.set_text(f"任务进行中: {message}")

        status_btn.on_click(do_check_status)
