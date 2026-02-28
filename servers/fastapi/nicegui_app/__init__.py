from fastapi import FastAPI
from nicegui import ui, events
import os
import aiohttp
import json
from utils.get_env import get_can_change_keys_env, get_user_config_path_env
from models.user_config import OpenAICompatibleProviderConfig, UserConfig
from utils.user_config import get_user_config, update_env_with_user_config
from nicegui_app.templates.base import create_layout_instance, get_registered_layouts
from constants.presentation import DEFAULT_TEMPLATES
# 导入具体模板模块以触发注册
import nicegui_app.templates.standard_intro  # noqa: F401


def _get_base_url() -> str:
    """后端 API 根地址，用于 NiceGUI 服务端请求同一 FastAPI 实例。"""
    return (
        os.getenv("FASTAPI_URL")
        or os.getenv("NEXT_PUBLIC_FAST_API")
        or f"http://127.0.0.1:{os.getenv('FASTAPI_PORT', '8000')}"
    ).rstrip("/")
import nicegui_app.templates.standard_toc  # noqa: F401
import nicegui_app.templates.standard_contact  # noqa: F401
import nicegui_app.templates.standard_chart_left  # noqa: F401


def create_nicegui_app() -> FastAPI:
  """
  Create and configure the NiceGUI application.

  This app will be mounted into the existing FastAPI backend under a path
  such as `/ui`, so it must NOT call `ui.run()`. We only define pages here.
  """

  app = FastAPI()

  @ui.page("/")
  def index_page() -> None:
    with ui.column().classes("items-center justify-center min-h-screen gap-4"):
      ui.label("Presenton (Python UI)").classes("text-2xl font-bold")
      ui.label("基于 NiceGUI 的新前端，正在逐步替换原有 Next.js/TypeScript 界面。").classes(
        "text-gray-500"
      )
      with ui.row().classes("gap-4"):
        # 使用相对路径，在挂载到 /ui 时解析为 /ui/dashboard、/ui/presentation，避免 404
        with ui.link(target="dashboard"):
          ui.button("进入仪表盘").props("color=primary")
        with ui.link(target="presentation"):
          ui.button("打开演示编辑器").props("outline")

  @ui.page("/dashboard")
  def dashboard_page() -> None:
    from datetime import datetime

    with ui.header().classes("justify-between"):
      ui.label("Dashboard").classes("text-xl font-bold")
      ui.label(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).classes("text-sm")

    with ui.row().classes("q-pa-md gap-4 items-start"):
      with ui.card().classes("w-72"):
        ui.label("快速开始").classes("text-md font-semibold")
        ui.label("从提示词生成新的演示文稿。").classes("text-sm text-gray-500 q-mb-sm")
        ui.button(
          "从提示词创建",
          on_click=lambda: ui.navigate.to("/presentation"),
        ).props("color=primary")

      with ui.card().classes("flex-1 min-w-[400px]"):
        ui.label("最近演示文稿").classes("text-md font-semibold q-mb-sm")

        state = {"selected": None}

        def handle_select(e: events.TableSelectionEventArguments) -> None:
          selection = e.selection or []
          state["selected"] = selection[0] if selection else None
          if state["selected"]:
            selected_label.text = (
              f'已选演示：{state["selected"].get("title") or state["selected"].get("id")}'
            )
          else:
            selected_label.text = "未选择演示"

        table = ui.table(
          columns=[
            {"name": "title", "label": "标题", "field": "title"},
            {"name": "language", "label": "语言", "field": "language"},
            {"name": "n_slides", "label": "页数", "field": "n_slides"},
            {"name": "created_at", "label": "创建时间", "field": "created_at"},
          ],
          rows=[],
          row_key="id",
          selection="single",
          on_select=handle_select,
        ).props("dense flat").classes("w-full")

        selected_label = ui.label("未选择演示").classes("text-sm text-gray-500 q-mt-sm")

        async def do_export_pptx() -> None:
          if state["selected"]:
            await export_and_open(str(state["selected"]["id"]), "pptx")
          else:
            log.push("请先选择一条演示文稿")

        async def do_export_pdf() -> None:
          if state["selected"]:
            await export_and_open(str(state["selected"]["id"]), "pdf")
          else:
            log.push("请先选择一条演示文稿")

        with ui.row().classes("q-mt-sm q-gutter-sm"):
          ui.button("导出 PPTX", on_click=do_export_pptx).props("dense outline")
          ui.button("导出 PDF", on_click=do_export_pdf).props("dense outline")

        log = ui.log().classes("q-mt-md h-32")

        async def load_presentations() -> None:
          log.clear()
          base_url = _get_base_url()
          url = base_url + "/api/v1/ppt/presentation/all"
          log.push(f"加载最近演示列表: {url}")

          try:
            async with aiohttp.ClientSession() as session:
              async with session.get(url) as resp:
                text = await resp.text()
                if resp.status != 200:
                  log.push(f"加载失败，HTTP {resp.status}: {text}")
                  return
                data = await resp.json()
          except Exception as e:  # noqa: BLE001
            log.push(f"调用后端接口异常: {e}")
            return

          rows = []
          for item in data:
            pid = item.get("id")
            title = item.get("title") or (item.get("content") or "")[0:32] or str(pid)
            language = item.get("language") or ""
            n_slides = item.get("n_slides") or ""
            created_at = (item.get("created_at") or "").replace("T", " ").split(".")[0]

            rows.append(
              {
                "id": pid,
                "title": title,
                "language": language,
                "n_slides": n_slides,
                "created_at": created_at,
              }
            )

          table.rows = rows
          log.push(f"已加载 {len(rows)} 个演示文稿。")

        async def export_and_open(presentation_id: str, export_as: str) -> None:
          base_url = _get_base_url()
          url = base_url + "/api/v1/ppt/presentation/export"
          log.push(f"导出 {presentation_id} 为 {export_as}: {url}")

          try:
            async with aiohttp.ClientSession() as session:
              async with session.post(
                url,
                json={"id": presentation_id, "export_as": export_as},
              ) as resp:
                text = await resp.text()
                if resp.status != 200:
                  log.push(f"导出失败，HTTP {resp.status}: {text}")
                  return
                data = await resp.json()
          except Exception as e:  # noqa: BLE001
            log.push(f"导出接口异常: {e}")
            return

          path = data.get("path")
          if not path:
            log.push("导出成功，但未返回路径。")  # 理论上不会发生
            return

          log.push(f"导出完成，文件路径: {path}")
          # 若 path 为可访问的 URL 则新开标签页；否则仅提示路径（需部署静态或下载接口）
          if path.startswith("http"):
            ui.run_javascript(f'window.open("{path}", "_blank")')
          else:
            # 尝试用后端根路径拼接相对路径，供静态或挂载目录场景使用
            public_url = base_url + path if path.startswith("/") else base_url + "/" + path
            ui.run_javascript(f'window.open("{public_url}", "_blank")')

        ui.button("刷新列表", on_click=load_presentations).props("flat dense").classes(
          "q-mt-sm"
        )
        # 页面加载时立即拉取列表
        ui.timer(0.1, load_presentations, once=True)

  @ui.page("/presentation")
  def presentation_page() -> None:
    ui.label("从提示词生成演示文稿").classes("text-xl font-bold q-mb-md")
    ui.label(
      "在下方输入主题和要求，后台将通过 FastAPI 的 /api/v1/ppt/presentation/generate 完成大纲、内容与导出。"
    ).classes("text-sm text-gray-500 q-mb-lg")

    with ui.card().classes("w-full max-w-3xl q-pa-md"):
      prompt = ui.textarea(
        "演示主题与要求（content）",
        placeholder="例如：介绍人工智能与机器学习的基础概念、历史发展与典型应用场景……",
      ).props("rows=6").classes("w-full")

      with ui.row().classes("w-full q-col-gutter-md q-mt-md"):
        slides_input = ui.number("幻灯片数量（n_slides）", value=8, min=1, max=30)
        language = ui.input("语言（language）", value="Chinese").classes("w-40")

      with ui.row().classes("w-full q-col-gutter-md q-mt-md"):
        layout = ui.select(
          {t: t if t != "general" else "general（通用模板）" for t in DEFAULT_TEMPLATES},
          value="general",
          label="模板（template）",
        ).classes("w-56")
        export_as = ui.select(
          {"pptx": "PPTX", "pdf": "PDF"},
          value="pptx",
          label="导出格式（export_as）",
        ).classes("w-40")

      with ui.row().classes("w-full q-col-gutter-md q-mt-md"):
        tone = ui.select(
          {
            "default": "default",
            "casual": "casual",
            "professional": "professional",
            "funny": "funny",
            "educational": "educational",
            "sales_pitch": "sales_pitch",
          },
          label="语气（tone，可选）",
          value="default",
        ).classes("w-56")
        verbosity = ui.select(
          {"concise": "concise", "standard": "standard", "text-heavy": "text-heavy"},
          label="详略程度（verbosity，可选）",
          value="standard",
        ).classes("w-56")

      with ui.row().classes("items-center q-mt-md q-gutter-md"):
        include_toc = ui.checkbox("包含目录页（include_table_of_contents）", value=False)
        include_title = ui.checkbox("包含标题页（include_title_slide）", value=True)
        web_search = ui.checkbox("启用联网检索（web_search）", value=False)

      log = ui.log().classes("q-mt-md h-40 w-full")
      result_label = ui.label().classes("q-mt-md text-positive")
      gen_btn_ref: list = []

      async def generate_presentation() -> None:
        import traceback
        log.clear()
        result_label.set_text("")
        if gen_btn_ref:
          gen_btn_ref[0].props("disable")
        log.push("生成中…")
        try:
          if not (prompt.value and prompt.value.strip()):
            log.push("请输入演示主题与要求（content）")
            return

          try:
            n_slides = int(slides_input.value or 8)
          except Exception:
            n_slides = 8

          payload = {
            "content": prompt.value.strip(),
            "n_slides": n_slides,
            "language": (language.value or "Chinese").strip(),
            "export_as": export_as.value or "pptx",
            "template": layout.value or "general",
            "tone": tone.value or "default",
            "verbosity": verbosity.value or "standard",
            "include_table_of_contents": bool(include_toc.value),
            "include_title_slide": bool(include_title.value),
            "web_search": bool(web_search.value),
          }

          base_url = _get_base_url()
          url = base_url + "/api/v1/ppt/presentation/generate"

          log.push(f"请求: {url}")
          log.push(f"参数: n_slides={n_slides}, template={payload['template']}, export_as={payload['export_as']}")

          try:
            async with aiohttp.ClientSession() as session:
              async with session.post(url, json=payload) as resp:
                text = await resp.text()
                if resp.status != 200:
                  log.push(f"HTTP {resp.status}")
                  try:
                    err = json.loads(text)
                    detail = err.get("detail", text)
                    if isinstance(detail, list):
                      detail = "; ".join(str(d.get("msg", d)) for d in detail)
                    log.push(f"错误: {detail}")
                  except Exception:
                    log.push(f"响应: {text[:500]}")
                  result_label.set_text("生成失败，请查看上方日志。")
                  return
                data = await resp.json()
          except Exception as e:  # noqa: BLE001
            log.push(f"请求异常: {e}")
            try:
              log.push(traceback.format_exc())
            except Exception:
              pass
            result_label.set_text("请求失败，请查看日志。")
            return

          presentation_id = data.get("presentation_id") or data.get("id")
          path = data.get("path")
          edit_path = data.get("edit_path")

          log.push(f"生成成功，presentation_id = {presentation_id}")
          if path:
            log.push(f"导出文件路径: {path}")
          if edit_path:
            log.push(f"可在原前端编辑链接: {edit_path}")

          result_label.set_text("演示文稿已生成，请根据日志中的路径/链接打开或下载。")
        except Exception as e:  # noqa: BLE001
          log.push(f"未预期的错误: {e}")
          try:
            log.push(traceback.format_exc())
          except Exception:
            pass
          result_label.set_text("发生错误，请查看日志。")
        finally:
          if gen_btn_ref:
            gen_btn_ref[0].props(remove="disable")

      gen_btn = ui.button(
        "生成演示文稿",
        on_click=generate_presentation,
      ).props("color=primary").classes("q-mt-md")
      gen_btn_ref.append(gen_btn)

  @ui.page("/settings")
  def settings_page() -> None:
    """LLM 与图像配置页：基于 UserConfig JSON 与现有 user_config 工具。"""

    can_change_keys = get_can_change_keys_env() != "false"
    user_config_path = get_user_config_path_env()

    ui.label("LLM 与图像提供商配置").classes("text-xl font-bold q-mb-md")
    if not can_change_keys:
      ui.label(
        "当前部署禁止在 UI 中修改敏感配置（CAN_CHANGE_KEYS=false）。"
      ).classes("text-sm text-red-500 q-mb-lg")
      return

    with ui.row().classes("q-gutter-lg items-start w-full"):
      with ui.card().classes("w-full max-w-2xl q-pa-md"):
        ui.label("基础配置").classes("text-md font-semibold q-mb-sm")

        llm_select = ui.select(
          {
            "openai": "OpenAI",
            "google": "Google",
            "anthropic": "Anthropic",
            "ollama": "Ollama（本地模型）",
            "custom": "自定义兼容 OpenAI API",
          },
          label="首选 LLM 提供商（default_llm_provider）",
        ).classes("w-72 q-mb-sm")

        default_model_input = ui.input(
          "默认文本模型（default_llm_model，可选，留空则使用各提供商默认值）"
        ).classes("w-full q-mb-md")

        with ui.expansion("任务级别模型配置").classes("w-full q-mb-sm"):
          ui.label("可以为不同任务指定单独的模型，未填写则回退到默认模型。").classes(
            "text-xs text-gray-500 q-mb-sm"
          )
          with ui.row().classes("q-gutter-md q-mb-sm"):
            outline_provider = ui.select(
              {
                "openai": "OpenAI",
                "google": "Google",
                "anthropic": "Anthropic",
                "ollama": "Ollama",
                "custom": "OpenAI Compatible（自定义）",
              },
              label="大纲生成提供商（outline_provider，可选）",
            ).classes("w-64")
            outline_model = ui.input(
              "大纲生成模型（outline_model，可选）"
            ).classes("w-full")

          with ui.row().classes("q-gutter-md q-mb-sm"):
            content_provider = ui.select(
              {
                "openai": "OpenAI",
                "google": "Google",
                "anthropic": "Anthropic",
                "ollama": "Ollama",
                "custom": "OpenAI Compatible（自定义）",
              },
              label="内容填充提供商（content_provider，可选）",
            ).classes("w-64")
            content_model = ui.input(
              "内容填充模型（content_model，可选）"
            ).classes("w-full")

          with ui.row().classes("q-gutter-md q-mb-sm"):
            notes_provider = ui.select(
              {
                "openai": "OpenAI",
                "google": "Google",
                "anthropic": "Anthropic",
                "ollama": "Ollama",
                "custom": "OpenAI Compatible（自定义）",
              },
              label="讲稿生成提供商（notes_provider，可选）",
            ).classes("w-64")
            notes_model = ui.input(
              "讲稿生成模型（speaker_notes_model，可选）"
            ).classes("w-full")

          with ui.row().classes("q-gutter-md"):
            research_provider = ui.select(
              {
                "openai": "OpenAI",
                "google": "Google",
                "anthropic": "Anthropic",
                "ollama": "Ollama",
                "custom": "OpenAI Compatible（自定义）",
              },
              label="研究报告提供商（research_provider，可选）",
            ).classes("w-64")
            research_model = ui.input(
              "研究报告模型（research_model，可选）"
            ).classes("w-full")

        with ui.expansion("OpenAI 配置").classes("w-full q-mb-sm"):
          openai_key = ui.input("OPENAI_API_KEY").props("type=password").classes(
            "w-full"
          )
          openai_model = ui.input("OPENAI_MODEL（如 gpt-4.1）").classes("w-full")

        with ui.expansion("Google Gemini 配置").classes("w-full q-mb-sm"):
          google_key = ui.input("GOOGLE_API_KEY").props("type=password").classes(
            "w-full"
          )
          google_model = ui.input("GOOGLE_MODEL（如 models/gemini-2.0-flash）").classes(
            "w-full"
          )

        with ui.expansion("Anthropic 配置").classes("w-full q-mb-sm"):
          anthropic_key = ui.input("ANTHROPIC_API_KEY").props(
            "type=password"
          ).classes("w-full")
          anthropic_model = ui.input(
            "ANTHROPIC_MODEL（如 claude-3-5-sonnet-20241022）"
          ).classes("w-full")

        with ui.expansion("Ollama 配置").classes("w-full q-mb-sm"):
          ollama_url = ui.input("OLLAMA_URL（如 http://localhost:11434）").classes(
            "w-full"
          )
          ollama_model = ui.input("OLLAMA_MODEL（如 llama3.2:3b）").classes("w-full")

        with ui.expansion("自定义兼容 OpenAI API（多厂商）").classes("w-full q-mb-sm"):
          compatible_provider_select = ui.select(
            {
              "deepseek": "DeepSeek",
              "kimi": "Kimi",
              "qwen": "Qwen",
              "custom": "自定义（任意 OpenAI Compatible）",
            },
            label="当前使用的兼容厂商（active_openai_compatible）",
            value="custom",
          ).classes("w-72 q-mb-sm")

          ui.label("DeepSeek 配置").classes("text-sm font-semibold q-mt-sm")
          deepseek_url = ui.input("DeepSeek Base URL").classes("w-full")
          deepseek_key = ui.input("DeepSeek API Key").props("type=password").classes(
            "w-full"
          )
          deepseek_model = ui.input("DeepSeek 模型名").classes("w-full")

          ui.separator().classes("q-my-sm")
          ui.label("Kimi 配置").classes("text-sm font-semibold q-mt-sm")
          kimi_url = ui.input("Kimi Base URL").classes("w-full")
          kimi_key = ui.input("Kimi API Key").props("type=password").classes("w-full")
          kimi_model = ui.input("Kimi 模型名").classes("w-full")

          ui.separator().classes("q-my-sm")
          ui.label("Qwen 配置").classes("text-sm font-semibold q-mt-sm")
          qwen_url = ui.input("Qwen Base URL").classes("w-full")
          qwen_key = ui.input("Qwen API Key").props("type=password").classes("w-full")
          qwen_model = ui.input("Qwen 模型名").classes("w-full")

          ui.separator().classes("q-my-sm")
          ui.label("自定义 OpenAI Compatible").classes("text-sm font-semibold q-mt-sm")
          custom_url = ui.input("CUSTOM_LLM_URL").classes("w-full")
          custom_key = ui.input("CUSTOM_LLM_API_KEY").props("type=password").classes(
            "w-full"
          )
          custom_model = ui.input("CUSTOM_MODEL").classes("w-full")

      with ui.card().classes("flex-1 q-pa-md min-w-[320px]"):
        ui.label("图像与高级选项").classes("text-md font-semibold q-mb-sm")

        disable_image = ui.checkbox("禁用图像生成（DISABLE_IMAGE_GENERATION）")
        image_provider = ui.select(
          {
            "dall-e-3": "dall-e-3",
            "gpt-image-1.5": "gpt-image-1.5",
            "gemini_flash": "gemini_flash",
            "nanobanana_pro": "nanobanana_pro",
            "pexels": "pexels",
            "pixabay": "pixabay",
            "comfyui": "comfyui",
          },
          label="IMAGE_PROVIDER",
        ).classes("w-56 q-mb-md")

        pexels_key = ui.input("PEXELS_API_KEY").props("type=password").classes(
          "w-full"
        )
        pixabay_key = ui.input("PIXABAY_API_KEY").props("type=password").classes(
          "w-full"
        )

        with ui.expansion("ComfyUI 配置").classes("w-full q-mb-sm"):
          comfy_url = ui.input("COMFYUI_URL").classes("w-full")
          comfy_workflow = ui.textarea("COMFYUI_WORKFLOW").props(
            "rows=3"
          ).classes("w-full")

        with ui.expansion("思考/工具调用选项").classes("w-full q-mb-sm"):
          tool_calls = ui.checkbox("启用工具调用（TOOL_CALLS）")
          disable_thinking = ui.checkbox("禁用思考（DISABLE_THINKING）")
          extended_reasoning = ui.checkbox("启用扩展推理（EXTENDED_REASONING）")
          web_grounding = ui.checkbox("启用联网检索（WEB_GROUNDING）")

        with ui.expansion("图像质量").classes("w-full q-mb-sm"):
          dalle_quality = ui.input("DALL_E_3_QUALITY（standard / hd）").classes(
            "w-full"
          )
          gpt_image_quality = ui.input(
            "GPT_IMAGE_1_5_QUALITY（low / medium / high）"
          ).classes("w-full")

        settings_log = ui.log().classes("q-mt-md h-40 w-full")
        result_label = ui.label().classes("q-mt-md text-positive")

        async def load_user_config() -> None:
          settings_log.clear()
          try:
            cfg = get_user_config()
          except Exception as e:  # noqa: BLE001
            settings_log.push(f"加载配置失败: {e}")
            return

          llm_select.value = cfg.default_llm_provider or cfg.LLM or None
          default_model_input.value = cfg.default_llm_model or ""
          # 任务级别 provider/model
          outline_provider.value = cfg.outline_provider or None
          outline_model.value = cfg.outline_model or ""
          content_provider.value = cfg.content_provider or None
          content_model.value = cfg.content_model or ""
          notes_provider.value = cfg.notes_provider or None
          notes_model.value = cfg.speaker_notes_model or ""
          research_provider.value = cfg.research_provider or None
          research_model.value = cfg.research_model or ""
          openai_key.value = cfg.OPENAI_API_KEY or ""
          openai_model.value = cfg.OPENAI_MODEL or ""
          google_key.value = cfg.GOOGLE_API_KEY or ""
          google_model.value = cfg.GOOGLE_MODEL or ""
          anthropic_key.value = cfg.ANTHROPIC_API_KEY or ""
          anthropic_model.value = cfg.ANTHROPIC_MODEL or ""
          ollama_url.value = cfg.OLLAMA_URL or ""
          ollama_model.value = cfg.OLLAMA_MODEL or ""
          # 兼容 OpenAI API 厂商配置
          active_key = cfg.active_openai_compatible or "custom"
          compatible_provider_select.value = active_key
          profiles = cfg.openai_compatible_configs or {}
          deepseek_cfg = profiles.get("deepseek")
          if deepseek_cfg:
            deepseek_url.value = deepseek_cfg.base_url or ""
            deepseek_key.value = deepseek_cfg.api_key or ""
            deepseek_model.value = deepseek_cfg.default_model or ""
          kimi_cfg = profiles.get("kimi")
          if kimi_cfg:
            kimi_url.value = kimi_cfg.base_url or ""
            kimi_key.value = kimi_cfg.api_key or ""
            kimi_model.value = kimi_cfg.default_model or ""
          qwen_cfg = profiles.get("qwen")
          if qwen_cfg:
            qwen_url.value = qwen_cfg.base_url or ""
            qwen_key.value = qwen_cfg.api_key or ""
            qwen_model.value = qwen_cfg.default_model or ""
          custom_cfg = profiles.get("custom")
          # 自定义 profile 与 legacy CUSTOM_* 字段双向兼容
          custom_url.value = (
            (custom_cfg.base_url if custom_cfg else None)
            or cfg.CUSTOM_LLM_URL
            or ""
          )
          custom_key.value = (
            (custom_cfg.api_key if custom_cfg else None)
            or cfg.CUSTOM_LLM_API_KEY
            or ""
          )
          custom_model.value = (
            (custom_cfg.default_model if custom_cfg else None)
            or cfg.CUSTOM_MODEL
            or ""
          )

          disable_image.value = bool(cfg.DISABLE_IMAGE_GENERATION)
          image_provider.value = cfg.IMAGE_PROVIDER or None
          pexels_key.value = cfg.PEXELS_API_KEY or ""
          pixabay_key.value = cfg.PIXABAY_API_KEY or ""
          comfy_url.value = cfg.COMFYUI_URL or ""
          comfy_workflow.value = cfg.COMFYUI_WORKFLOW or ""
          tool_calls.value = bool(cfg.TOOL_CALLS)
          disable_thinking.value = bool(cfg.DISABLE_THINKING)
          extended_reasoning.value = bool(cfg.EXTENDED_REASONING)
          web_grounding.value = bool(cfg.WEB_GROUNDING)
          dalle_quality.value = cfg.DALL_E_3_QUALITY or ""
          gpt_image_quality.value = cfg.GPT_IMAGE_1_5_QUALITY or ""

          settings_log.push(
            f"配置已从 {user_config_path or 'USER_CONFIG_PATH 未设置'} 加载。"
          )

        async def save_user_config() -> None:
          settings_log.clear()
          try:
            existing = get_user_config()
          except Exception:
            existing = UserConfig()

          # 组装 OpenAI 兼容厂商配置列表
          def build_profile(
            key: str, display_name: str, url: str, api_key: str, model: str
          ) -> OpenAICompatibleProviderConfig | None:
            if not (url or api_key or model):
              return None
            return OpenAICompatibleProviderConfig(
              display_name=display_name,
              base_url=url or None,
              api_key=api_key or None,
              default_model=model or None,
            )

          profiles: dict[str, OpenAICompatibleProviderConfig] = dict(
            existing.openai_compatible_configs or {}
          )

          ds = build_profile(
            "deepseek",
            "DeepSeek",
            deepseek_url.value,
            deepseek_key.value,
            deepseek_model.value,
          )
          if ds:
            profiles["deepseek"] = ds

          km = build_profile(
            "kimi",
            "Kimi",
            kimi_url.value,
            kimi_key.value,
            kimi_model.value,
          )
          if km:
            profiles["kimi"] = km

          qw = build_profile(
            "qwen",
            "Qwen",
            qwen_url.value,
            qwen_key.value,
            qwen_model.value,
          )
          if qw:
            profiles["qwen"] = qw

          custom_profile = build_profile(
            "custom",
            "Custom",
            custom_url.value,
            custom_key.value,
            custom_model.value,
          )
          if custom_profile:
            profiles["custom"] = custom_profile

          merged = UserConfig(
            # 顶层 LLM 配置
            LLM=llm_select.value or existing.LLM,
            default_llm_provider=llm_select.value
            or existing.default_llm_provider
            or existing.LLM,
            default_llm_model=default_model_input.value
            or existing.default_llm_model
            or existing.OPENAI_MODEL,
            outline_provider=outline_provider.value or existing.outline_provider,
            outline_model=outline_model.value or existing.outline_model,
            content_provider=content_provider.value or existing.content_provider,
            content_model=content_model.value or existing.content_model,
            notes_provider=notes_provider.value or existing.notes_provider,
            speaker_notes_model=notes_model.value or existing.speaker_notes_model,
            research_provider=research_provider.value or existing.research_provider,
            research_model=research_model.value or existing.research_model,
            openai_compatible_configs=profiles or None,
            active_openai_compatible=compatible_provider_select.value
            or existing.active_openai_compatible,
            # 平铺 provider 字段（向后兼容）
            OPENAI_API_KEY=openai_key.value or existing.OPENAI_API_KEY,
            OPENAI_MODEL=openai_model.value or existing.OPENAI_MODEL,
            GOOGLE_API_KEY=google_key.value or existing.GOOGLE_API_KEY,
            GOOGLE_MODEL=google_model.value or existing.GOOGLE_MODEL,
            ANTHROPIC_API_KEY=anthropic_key.value or existing.ANTHROPIC_API_KEY,
            ANTHROPIC_MODEL=anthropic_model.value or existing.ANTHROPIC_MODEL,
            OLLAMA_URL=ollama_url.value or existing.OLLAMA_URL,
            OLLAMA_MODEL=ollama_model.value or existing.OLLAMA_MODEL,
            CUSTOM_LLM_URL=custom_url.value or existing.CUSTOM_LLM_URL,
            CUSTOM_LLM_API_KEY=custom_key.value or existing.CUSTOM_LLM_API_KEY,
            CUSTOM_MODEL=custom_model.value or existing.CUSTOM_MODEL,
            DISABLE_IMAGE_GENERATION=disable_image.value,
            IMAGE_PROVIDER=image_provider.value or existing.IMAGE_PROVIDER,
            PEXELS_API_KEY=pexels_key.value or existing.PEXELS_API_KEY,
            PIXABAY_API_KEY=pixabay_key.value or existing.PIXABAY_API_KEY,
            COMFYUI_URL=comfy_url.value or existing.COMFYUI_URL,
            COMFYUI_WORKFLOW=comfy_workflow.value or existing.COMFYUI_WORKFLOW,
            DALL_E_3_QUALITY=dalle_quality.value or existing.DALL_E_3_QUALITY,
            GPT_IMAGE_1_5_QUALITY=gpt_image_quality.value
            or existing.GPT_IMAGE_1_5_QUALITY,
            TOOL_CALLS=tool_calls.value,
            DISABLE_THINKING=disable_thinking.value,
            EXTENDED_REASONING=extended_reasoning.value,
            WEB_GROUNDING=web_grounding.value,
          )

          path = user_config_path or ""
          if not path:
            settings_log.push("USER_CONFIG_PATH 未设置，无法保存配置。")
            return

          try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
              json.dump(merged.model_dump(), f)
          except Exception as e:  # noqa: BLE001
            settings_log.push(f"写入配置文件失败: {e}")
            return

          # 将配置同步到环境变量，便于 FastAPI 在当前进程中立即生效
          try:
            update_env_with_user_config()
          except Exception as e:  # noqa: BLE001
            settings_log.push(f"更新环境变量时出错（可忽略）: {e}")

          result_label.set_text("配置已保存。")
          settings_log.push(f"配置已写入 {path}")

        ui.button("保存配置", on_click=save_user_config).props("color=primary").classes(
          "q-mt-md"
        )

        ui.timer(0.1, load_user_config, once=True)

  @ui.page("/outline")
  def outline_page() -> None:
    """大纲生成与编辑页面：基于 /presentation/create + /outlines/stream + /presentation/prepare。"""

    ui.label("演示大纲生成与编辑").classes("text-xl font-bold q-mb-md")
    ui.label(
      "步骤：1）创建空演示 2）流式生成大纲 3）在下方编辑每一页大纲 4）提交保存以用于后续生成内容与导出。"
    ).classes("text-sm text-gray-500 q-mb-lg")

    with ui.row().classes("items-start q-gutter-lg w-full"):
      # 左侧：创建与流式大纲
      with ui.card().classes("w-full max-w-xl q-pa-md"):
        ui.label("1. 创建演示并生成大纲").classes("text-md font-semibold q-mb-sm")
        content_input = ui.textarea(
          "演示主题与要求（content）",
          placeholder="例如：介绍公司新产品的核心亮点、目标用户与市场机会……",
        ).props("rows=4").classes("w-full")

        with ui.row().classes("w-full q-col-gutter-md q-mt-md"):
          outline_slides_input = ui.number(
            "预计幻灯片数量（n_slides）", value=8, min=1, max=30
          )
          outline_language = ui.input("语言（language）", value="Chinese").classes("w-40")

        with ui.row().classes("w-full q-col-gutter-md q-mt-md"):
          outline_tone = ui.select(
            {
              "default": "default",
              "casual": "casual",
              "professional": "professional",
              "funny": "funny",
              "educational": "educational",
              "sales_pitch": "sales_pitch",
            },
            label="语气（tone，可选）",
            value="default",
          ).classes("w-56")
          outline_verbosity = ui.select(
            {"concise": "concise", "standard": "standard", "text-heavy": "text-heavy"},
            label="详略程度（verbosity，可选）",
            value="standard",
          ).classes("w-56")

        with ui.row().classes("items-center q-mt-md q-gutter-md"):
          outline_include_toc = ui.checkbox(
            "包含目录页（include_table_of_contents）", value=False
          )
          outline_include_title = ui.checkbox(
            "包含标题页（include_title_slide）", value=True
          )
          outline_web_search = ui.checkbox("启用联网检索（web_search）", value=False)

        outline_log = ui.log().classes("q-mt-md h-40 w-full")

        # 右侧：可编辑大纲与布局选择
      with ui.card().classes("flex-1 q-pa-md min-w-[400px]"):
        ui.label("2. 编辑每一页大纲并应用布局").classes(
          "text-md font-semibold q-mb-sm"
        )
        title_input = ui.input("演示标题（可选，留空则自动从大纲推断）").classes("w-full q-mb-sm")

        layouts_meta = get_registered_layouts()
        layout_options = {
          meta.layout_id: f"{meta.group} / {meta.name}" for meta in layouts_meta
        } or {"header-counter-two-column-image-text-slide": "standard / Intro Slide"}
        layout_select = ui.select(
          layout_options,
          value=next(iter(layout_options.keys())),
          label="布局模板（layout_id）",
        ).classes("w-72 q-mb-md")

        ui.label("当前布局预览").classes("text-sm text-gray-500 q-mb-xs")
        preview_container = ui.column().classes(
          "w-full max-h-[260px] overflow-auto border rounded q-pa-sm q-mb-md"
        )

        outline_container = ui.column().classes(
          "w-full gap-2 max-h-[420px] overflow-auto"
        )
        prepare_log = ui.log().classes("q-mt-md h-32 w-full")

      state = {"presentation_id": None, "outlines": [], "outline_editors": []}  # 简单状态容器

      async def create_and_stream_outlines() -> None:
        outline_log.clear()
        prepare_log.clear()
        # 预览当前选择的布局
        preview_container.clear()
        try:
          layout_id = layout_select.value or ""
          inst = create_layout_instance(layout_id, data=None)
          if inst:
            with preview_container:
              inst.render()
        except Exception as e:  # noqa: BLE001
          prepare_log.push(f"布局预览失败（不影响保存）: {e}")
        outline_container.clear()
        state["presentation_id"] = None
        state["outlines"] = []

        if not (content_input.value and content_input.value.strip()):
          outline_log.push("请输入演示主题与要求（content）")
          return

        try:
          n_slides = int(outline_slides_input.value or 8)
        except Exception:
          n_slides = 8

        base_url = _get_base_url()

        # 1) 创建演示（/presentation/create）
        create_url = base_url + "/api/v1/ppt/presentation/create"
        payload = {
          "content": content_input.value.strip(),
          "n_slides": n_slides,
          "language": (outline_language.value or "Chinese").strip(),
          "file_paths": None,
          "tone": outline_tone.value or "default",
          "verbosity": outline_verbosity.value or "standard",
          "instructions": None,
          "include_table_of_contents": bool(outline_include_toc.value),
          "include_title_slide": bool(outline_include_title.value),
          "web_search": bool(outline_web_search.value),
        }

        outline_log.push(f"创建演示: {create_url}")
        try:
          async with aiohttp.ClientSession() as session:
            async with session.post(create_url, json=payload) as resp:
              text = await resp.text()
              if resp.status != 200:
                outline_log.push(f"创建失败，HTTP {resp.status}: {text}")
                return
              created = await resp.json()
        except Exception as e:  # noqa: BLE001
          outline_log.push(f"创建演示接口异常: {e}")
          return

        pid = created.get("id")
        if not pid:
          outline_log.push("创建成功但未返回 ID。")
          return

        state["presentation_id"] = pid
        outline_log.push(f"演示已创建，ID = {pid}，开始流式生成大纲…")

        # 2) 流式生成大纲（/outlines/stream/{id}，SSE）
        stream_url = base_url + f"/api/v1/ppt/outlines/stream/{pid}"
        outline_log.push(f"连接 SSE 流: {stream_url}")

        try:
          async with aiohttp.ClientSession() as session:
            async with session.get(stream_url) as resp:
              if resp.status != 200:
                text = await resp.text()
                outline_log.push(f"SSE 连接失败，HTTP {resp.status}: {text}")
                return

              buffer = ""
              async for chunk, _ in resp.content.iter_chunks():
                if not chunk:
                  continue
                buffer += chunk.decode("utf-8", errors="ignore")
                while "\n\n" in buffer:
                  event_block, buffer = buffer.split("\n\n", 1)
                  lines = [ln for ln in event_block.splitlines() if ln.strip()]
                  data_line = next((ln for ln in lines if ln.startswith("data:")), None)
                  if not data_line or len(data_line) <= 5:
                    continue
                  try:
                    data_json = json.loads(data_line[5:].strip())
                  except Exception:
                    continue

                  # chunk 事件：只做日志展示
                  if data_json.get("type") == "chunk":
                    outline_log.push("收到大纲片段…")
                    continue

                  # complete 事件：key = presentation，value 为完整演示对象
                  if data_json.get("key") == "presentation" and "value" in data_json:
                    presentation = data_json["value"]
                    outlines = (
                      (presentation.get("outlines") or {}).get("slides") or []
                    )

                    state["outlines"] = outlines

                    outline_container.clear()
                    state["outline_editors"] = []
                    for idx, slide in enumerate(outlines):
                      content = slide.get("content") or ""
                      with outline_container:
                        ui.label(f"Slide {idx + 1}").classes(
                          "text-sm font-semibold q-mt-sm"
                        )
                        ta = ui.textarea().props("rows=3").classes("w-full")
                        ta.value = content
                        state["outline_editors"].append(ta)

                    outline_log.push("大纲生成完成，可在右侧编辑每一页内容。")
                    return
        except Exception as e:  # noqa: BLE001
          outline_log.push(f"SSE 流异常: {e}")
          return

      async def prepare_presentation_from_outlines() -> None:
        prepare_log.clear()
        pid = state.get("presentation_id")
        if not pid:
          prepare_log.push("请先创建演示并生成大纲。")
          return

        # 从 outline_container 中收集最新内容
        if not state["outline_editors"]:
          prepare_log.push("当前无可编辑大纲，请先生成。")
          return

        new_outlines = [
          {"content": editor.value or ""} for editor in state["outline_editors"]
        ]

        base_url = _get_base_url()

        # 获取布局详情（layout_name 需为后端支持的 group，如 general）
        layout_name = layout_select.value or "general"
        layout_url = base_url + f"/api/v1/ppt/layouts/{layout_name}"
        prepare_log.push(f"获取布局: {layout_url}")

        try:
          async with aiohttp.ClientSession() as session:
            async with session.get(layout_url) as resp:
              text = await resp.text()
              if resp.status != 200:
                prepare_log.push(f"获取布局失败，HTTP {resp.status}: {text}")
                return
              layout_json = await resp.json()
        except Exception as e:  # noqa: BLE001
          prepare_log.push(f"获取布局接口异常: {e}")
          return

        # 调用 /presentation/prepare
        prepare_url = base_url + "/api/v1/ppt/presentation/prepare"
        payload = {
          "presentation_id": pid,
          "outlines": new_outlines,
          "layout": layout_json,
          "title": (title_input.value or None),
        }

        prepare_log.push(f"提交大纲与布局: {prepare_url}")
        try:
          async with aiohttp.ClientSession() as session:
            async with session.post(prepare_url, json=payload) as resp:
              text = await resp.text()
              if resp.status != 200:
                prepare_log.push(f"保存失败，HTTP {resp.status}: {text}")
                return
              _ = await resp.json()
        except Exception as e:  # noqa: BLE001
          prepare_log.push(f"提交接口异常: {e}")
          return

        prepare_log.push("大纲与布局已保存，可在其它页面继续生成内容与导出。")

      export_select = ui.select(
        {"pptx": "PPTX", "pdf": "PDF"},
        value="pptx",
        label="立即导出格式（export_as）",
      ).classes("w-40")

      async def export_from_outline() -> None:
        pid = state.get("presentation_id")
        if not pid:
          prepare_log.push("请先创建演示并保存大纲。")
          return

        base_url = _get_base_url()
        url = base_url + "/api/v1/ppt/presentation/export"
        export_as = export_select.value or "pptx"
        prepare_log.push(f"导出演示 {pid} 为 {export_as}: {url}")

        try:
          async with aiohttp.ClientSession() as session:
            async with session.post(
              url, json={"id": pid, "export_as": export_as}
            ) as resp:
              text = await resp.text()
              if resp.status != 200:
                prepare_log.push(f"导出失败，HTTP {resp.status}: {text}")
                return
              data = await resp.json()
        except Exception as e:  # noqa: BLE001
          prepare_log.push(f"导出接口异常: {e}")
          return

        path = data.get("path")
        if not path:
          prepare_log.push("导出成功，但未返回路径。")
          return

        prepare_log.push(f"导出完成，文件路径: {path}")
        if path.startswith("http"):
          ui.run_javascript(f'window.open("{path}", "_blank")')
        else:
          public_url = base_url + path if path.startswith("/") else base_url + "/" + path
          ui.run_javascript(f'window.open("{public_url}", "_blank")')

        with ui.row().classes("q-mt-md q-gutter-md"):
          ui.button("创建并流式生成大纲", on_click=create_and_stream_outlines).props(
            "color=primary"
          )
          ui.button(
            "保存当前大纲并应用布局",
            on_click=prepare_presentation_from_outlines,
          ).props("outline")
          ui.button("立即导出", on_click=export_from_outline).props("color=positive")

  # 将 NiceGUI 绑定到本地 FastAPI 应用
  ui.run_with(app)
  return app
