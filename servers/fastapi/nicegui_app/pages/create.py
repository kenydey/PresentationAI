"""创建演示文稿 — 输入主题、上传文件、选择参数后生成。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_post, api_post_form, get_base_url
import aiohttp
import json


@ui.page("/create")
def create_page():
    page_layout("创建演示文稿")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("从提示词生成演示文稿").classes("text-2xl font-bold")

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            # ── 左栏：输入参数 ──
            with ui.card().classes("flex-1 min-w-[400px]"):
                ui.label("演示内容").classes("font-semibold mb-1")
                prompt = ui.textarea(
                    placeholder="例如：介绍人工智能的核心概念、发展历史与典型应用……"
                ).props("rows=5 outlined").classes("w-full")

                ui.label("附件文档（可选）").classes("font-semibold mt-4 mb-1")
                ui.label("支持 PDF、DOCX、TXT、PPTX").classes("text-xs text-gray-400")
                file_paths_state = {"paths": []}

                async def handle_upload(e):
                    for f in e.files if hasattr(e, 'files') else [e]:
                        fd = aiohttp.FormData()
                        fd.add_field("files", f.content.read(), filename=f.name, content_type=f.type or "application/octet-stream")
                        status, data = await api_post_form("/api/v1/ppt/files/upload", fd)
                        if status == 200 and isinstance(data, list):
                            file_paths_state["paths"].extend(data)
                            log.push(f"已上传: {f.name}")
                        else:
                            log.push(f"上传失败: {data}")

                ui.upload(on_upload=handle_upload, multiple=True, auto_upload=True).props(
                    "accept='.pdf,.docx,.doc,.txt,.pptx' flat bordered"
                ).classes("w-full")

            # ── 右栏：参数配置 ──
            with ui.card().classes("w-80"):
                ui.label("生成参数").classes("font-semibold mb-2")

                n_slides = ui.number("幻灯片数量", value=8, min=1, max=30).classes("w-full")
                language = ui.input("语言", value="Chinese").classes("w-full")
                template = ui.select(
                    {"general": "通用 (general)", "modern": "现代 (modern)", "neo-general": "新通用", "neo-modern": "新现代"},
                    value="general", label="模板风格",
                ).classes("w-full")
                export_as = ui.select({"pptx": "PPTX", "pdf": "PDF"}, value="pptx", label="导出格式").classes("w-full")
                tone = ui.select(
                    {"default": "默认", "casual": "轻松", "professional": "专业", "funny": "幽默", "educational": "教学", "sales_pitch": "推销"},
                    value="default", label="语气",
                ).classes("w-full")
                verbosity = ui.select(
                    {"concise": "简洁", "standard": "标准", "text-heavy": "详细"},
                    value="standard", label="详略程度",
                ).classes("w-full")

                with ui.column().classes("gap-1 mt-2"):
                    include_toc = ui.checkbox("包含目录页", value=False)
                    include_title = ui.checkbox("包含标题页", value=True)
                    web_search = ui.checkbox("启用联网检索", value=False)

        # ── 生成按钮与日志 ──
        gen_btn = ui.button("生成演示文稿", icon="auto_awesome").props("color=primary size=lg")
        log = ui.log().classes("h-48 w-full")
        result = ui.label().classes("text-green-600 font-medium")

        async def generate():
            log.clear()
            result.set_text("")
            if not (prompt.value or "").strip():
                log.push("请输入演示内容")
                return
            gen_btn.props("disable loading")
            payload = {
                "content": prompt.value.strip(),
                "n_slides": int(n_slides.value or 8),
                "language": (language.value or "Chinese").strip(),
                "export_as": export_as.value or "pptx",
                "template": template.value or "general",
                "tone": tone.value or "default",
                "verbosity": verbosity.value or "standard",
                "include_table_of_contents": bool(include_toc.value),
                "include_title_slide": bool(include_title.value),
                "web_search": bool(web_search.value),
            }
            if file_paths_state["paths"]:
                payload["file_paths"] = file_paths_state["paths"]

            log.push(f"正在生成… 模板={payload['template']}  页数={payload['n_slides']}")
            status, data = await api_post("/api/v1/ppt/presentation/generate", payload)
            gen_btn.props(remove="disable loading")

            if status != 200:
                detail = data.get("detail", data) if isinstance(data, dict) else data
                if isinstance(detail, list):
                    detail = "; ".join(str(d.get("msg", d)) for d in detail)
                log.push(f"生成失败 (HTTP {status}): {detail}")
                result.set_text("生成失败，请查看日志")
                return

            pid = data.get("presentation_id") or data.get("id")
            path = data.get("path", "")
            log.push(f"生成成功! ID = {pid}")
            if path:
                log.push(f"文件路径: {path}")
                base = get_base_url()
                url = path if path.startswith("http") else base + ("/" if not path.startswith("/") else "") + path
                ui.run_javascript(f'window.open("{url}", "_blank")')
            result.set_text("演示文稿已生成!")

        gen_btn.on_click(generate)
