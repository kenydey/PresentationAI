"""系统设置 — LLM 提供商和图像生成配置。对接 Config API。"""

from nicegui import ui
from nicegui_app.layout import page_layout
from nicegui_app.api_client import api_get, api_post
from utils.get_env import get_can_change_keys_env
from models.user_config import OpenAICompatibleProviderConfig, UserConfig

PROVIDERS = {"openai": "OpenAI", "google": "Google", "anthropic": "Anthropic", "ollama": "Ollama", "custom": "自定义 (OpenAI Compatible)"}
IMAGE_PROVIDERS = {"dall-e-3": "DALL-E 3", "gpt-image-1.5": "GPT Image 1.5", "gemini_flash": "Gemini Flash", "pexels": "Pexels", "pixabay": "Pixabay", "comfyui": "ComfyUI"}
COMPAT_OPTIONS = {"deepseek": "DeepSeek", "kimi": "Kimi", "qwen": "Qwen", "custom": "自定义"}


def _norm_select_value(val: str | None, options: dict) -> str | None:
    """将配置值规范化为 options 的 key，支持大小写模糊匹配。"""
    if not val or not isinstance(val, str):
        return None
    val = val.strip().lower()
    for k, v in options.items():
        if k.lower() == val or (isinstance(v, str) and v.lower() == val):
            return k
    return val if val in options else (list(options.keys())[0] if options else None)


@ui.page("/settings")
def settings_page():
    page_layout("系统设置")

    can_change = get_can_change_keys_env() != "false"

    async def check_openai():
        key = oai_key.value
        if not key:
            oai_models_label.set_text("请先输入 API Key")
            return
        status, data = await api_post("/api/v1/ppt/openai/models/available", {"api_key": key, "url": None})
        if status == 200 and isinstance(data, list):
            oai_models_label.set_text(f"可用模型: {', '.join(m.get('id','') if isinstance(m,dict) else str(m) for m in data[:10])}")
        else:
            oai_models_label.set_text(f"检测失败: {data}")

    async def check_google():
        key = google_key.value
        if not key:
            google_models_label.set_text("请先输入 API Key")
            return
        status, data = await api_post("/api/v1/ppt/google/models/available", {"api_key": key})
        if status == 200 and isinstance(data, list):
            google_models_label.set_text(f"可用模型: {', '.join(str(m) for m in data[:10])}")
        else:
            google_models_label.set_text(f"检测失败: {data}")

    async def check_anthropic():
        key = ant_key.value
        if not key:
            ant_models_label.set_text("请先输入 API Key")
            return
        status, data = await api_post("/api/v1/ppt/anthropic/models/available", {"api_key": key})
        if status == 200 and isinstance(data, list):
            ant_models_label.set_text(f"可用模型: {', '.join(str(m) for m in data[:10])}")
        else:
            ant_models_label.set_text(f"检测失败: {data}")

    async def check_ollama():
        url = ollama_url.value or "http://localhost:11434"
        ollama_models_label.set_text("检测中…")
        status, data = await api_get("/api/v1/ppt/ollama/models/available")
        if status == 200 and isinstance(data, list):
            names = [m.get("name", m) if isinstance(m, dict) else str(m) for m in data[:10]]
            ollama_models_label.set_text(f"已拉取模型: {', '.join(names)}" if names else "无已拉取模型")
        else:
            ollama_models_label.set_text(f"检测失败（请确保 Ollama 已启动）: {data}")

    async def load_config():
        log.clear()
        status, data = await api_get("/api/v1/ppt/config")
        if status != 200 or not isinstance(data, dict):
            log.push(f"加载失败: {data}")
            ui.notify('配置加载失败', type='negative')
            return
        cfg = data
        llm_provider.value = _norm_select_value(cfg.get("default_llm_provider") or cfg.get("LLM"), PROVIDERS)
        default_model.value = cfg.get("default_llm_model") or ""
        outline_prov.value = _norm_select_value(cfg.get("outline_provider"), PROVIDERS)
        outline_mod.value = cfg.get("outline_model") or ""
        content_prov.value = _norm_select_value(cfg.get("content_provider"), PROVIDERS)
        content_mod.value = cfg.get("content_model") or ""
        notes_prov.value = _norm_select_value(cfg.get("notes_provider"), PROVIDERS)
        notes_mod.value = cfg.get("speaker_notes_model") or ""
        research_prov.value = _norm_select_value(cfg.get("research_provider"), PROVIDERS)
        research_mod.value = cfg.get("research_model") or ""
        oai_key.value = cfg.get("OPENAI_API_KEY") or ""
        oai_model.value = cfg.get("OPENAI_MODEL") or ""
        google_key.value = cfg.get("GOOGLE_API_KEY") or ""
        google_model.value = cfg.get("GOOGLE_MODEL") or ""
        ant_key.value = cfg.get("ANTHROPIC_API_KEY") or ""
        ant_model.value = cfg.get("ANTHROPIC_MODEL") or ""
        ollama_url.value = cfg.get("OLLAMA_URL") or ""
        ollama_model.value = cfg.get("OLLAMA_MODEL") or ""
        profiles = cfg.get("openai_compatible_configs") or {}
        compat_active.value = _norm_select_value(cfg.get("active_openai_compatible"), COMPAT_OPTIONS) or "custom"
        dsc = profiles.get("deepseek") or {}
        if isinstance(dsc, dict): ds_url.value, ds_key.value, ds_model.value = dsc.get("base_url") or "", dsc.get("api_key") or "", dsc.get("default_model") or ""
        kc = profiles.get("kimi") or {}
        if isinstance(kc, dict): kimi_url.value, kimi_key.value, kimi_model.value = kc.get("base_url") or "", kc.get("api_key") or "", kc.get("default_model") or ""
        qc = profiles.get("qwen") or {}
        if isinstance(qc, dict): qwen_url.value, qwen_key.value, qwen_model.value = qc.get("base_url") or "", qc.get("api_key") or "", qc.get("default_model") or ""
        cc = profiles.get("custom") or {}
        cust_url.value = (cc.get("base_url") if isinstance(cc, dict) else None) or cfg.get("CUSTOM_LLM_URL") or ""
        cust_key.value = (cc.get("api_key") if isinstance(cc, dict) else None) or cfg.get("CUSTOM_LLM_API_KEY") or ""
        cust_model.value = (cc.get("default_model") if isinstance(cc, dict) else None) or cfg.get("CUSTOM_MODEL") or ""
        disable_img.value = bool(cfg.get("DISABLE_IMAGE_GENERATION"))
        img_provider.value = _norm_select_value(cfg.get("IMAGE_PROVIDER"), IMAGE_PROVIDERS)
        pexels_key.value = cfg.get("PEXELS_API_KEY") or ""
        pixabay_key.value = cfg.get("PIXABAY_API_KEY") or ""
        comfy_url.value = cfg.get("COMFYUI_URL") or ""
        comfy_wf.value = cfg.get("COMFYUI_WORKFLOW") or ""
        dalle_q.value = cfg.get("DALL_E_3_QUALITY") or ""
        gpt_img_q.value = cfg.get("GPT_IMAGE_1_5_QUALITY") or ""
        tool_calls.value = bool(cfg.get("TOOL_CALLS"))
        disable_think.value = bool(cfg.get("DISABLE_THINKING"))
        extended_reason.value = bool(cfg.get("EXTENDED_REASONING"))
        web_ground.value = bool(cfg.get("WEB_GROUNDING"))
        log.push("配置已加载（来自 Config API）")
        ui.notify('配置已加载', type='positive')
        await load_theme_footer()

    async def save_config():
        log.clear()
        status, existing_data = await api_get("/api/v1/ppt/config")
        existing = existing_data if isinstance(existing_data, dict) else {}

        def _prof(url, key, model, name):
            if not (url or key or model): return None
            return OpenAICompatibleProviderConfig(display_name=name, base_url=url or None, api_key=key or None, default_model=model or None)

        profiles = dict(existing.get("openai_compatible_configs") or {})
        for k, n, u, ky, m in [("deepseek","DeepSeek",ds_url,ds_key,ds_model),("kimi","Kimi",kimi_url,kimi_key,kimi_model),("qwen","Qwen",qwen_url,qwen_key,qwen_model),("custom","Custom",cust_url,cust_key,cust_model)]:
            p = _prof(u.value, ky.value, m.value, n)
            if p: profiles[k] = p

        merged = UserConfig(
            LLM=llm_provider.value, default_llm_provider=llm_provider.value, default_llm_model=default_model.value or None,
            outline_provider=outline_prov.value, outline_model=outline_mod.value or None,
            content_provider=content_prov.value, content_model=content_mod.value or None,
            notes_provider=notes_prov.value, speaker_notes_model=notes_mod.value or None,
            research_provider=research_prov.value, research_model=research_mod.value or None,
            openai_compatible_configs=profiles or None, active_openai_compatible=compat_active.value,
            OPENAI_API_KEY=oai_key.value or None, OPENAI_MODEL=oai_model.value or None,
            GOOGLE_API_KEY=google_key.value or None, GOOGLE_MODEL=google_model.value or None,
            ANTHROPIC_API_KEY=ant_key.value or None, ANTHROPIC_MODEL=ant_model.value or None,
            OLLAMA_URL=ollama_url.value or None, OLLAMA_MODEL=ollama_model.value or None,
            CUSTOM_LLM_URL=cust_url.value or None, CUSTOM_LLM_API_KEY=cust_key.value or None, CUSTOM_MODEL=cust_model.value or None,
            DISABLE_IMAGE_GENERATION=disable_img.value, IMAGE_PROVIDER=img_provider.value or None,
            PEXELS_API_KEY=pexels_key.value or None, PIXABAY_API_KEY=pixabay_key.value or None,
            COMFYUI_URL=comfy_url.value or None, COMFYUI_WORKFLOW=comfy_wf.value or None,
            DALL_E_3_QUALITY=dalle_q.value or None, GPT_IMAGE_1_5_QUALITY=gpt_img_q.value or None,
            TOOL_CALLS=tool_calls.value, DISABLE_THINKING=disable_think.value,
            EXTENDED_REASONING=extended_reason.value, WEB_GROUNDING=web_ground.value,
        )
        status, data = await api_post("/api/v1/ppt/config", merged.model_dump(exclude_none=True))
        if status != 200:
            log.push(f"保存失败: {data}")
            ui.notify('配置保存失败', type='negative')
            return
        result_label.set_text("配置已保存!")
        ui.notify('配置保存成功', type='positive')
        log.push("已通过 Config API 保存")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("LLM 与图像提供商配置").classes("text-2xl font-bold")
        if not can_change:
            ui.label("当前部署禁止修改配置 (CAN_CHANGE_KEYS=false)").classes("text-red-500")
            return

        with ui.row().classes("w-full gap-6 items-start flex-wrap"):
            # ── 左栏: LLM 配置 ──
            with ui.card().classes("flex-1 min-w-[450px]"):
                ui.label("LLM 基础配置").classes("font-semibold mb-2")
                llm_provider = ui.select(PROVIDERS, label="默认 LLM 提供商").classes("w-72")
                default_model = ui.input("默认模型（可选）").classes("w-full")

                with ui.expansion("任务级别模型", icon="tune").classes("w-full"):
                    outline_prov = ui.select(PROVIDERS, label="大纲提供商").classes("w-64")
                    outline_mod = ui.input("大纲模型").classes("w-full")
                    content_prov = ui.select(PROVIDERS, label="内容提供商").classes("w-64")
                    content_mod = ui.input("内容模型").classes("w-full")
                    notes_prov = ui.select(PROVIDERS, label="讲稿提供商").classes("w-64")
                    notes_mod = ui.input("讲稿模型").classes("w-full")
                    research_prov = ui.select(PROVIDERS, label="研究提供商").classes("w-64")
                    research_mod = ui.input("研究模型").classes("w-full")

                with ui.expansion("OpenAI", icon="smart_toy").classes("w-full"):
                    oai_key = ui.input("API Key").props("type=password").classes("w-full")
                    oai_model = ui.input("模型 (如 gpt-4.1)").classes("w-full")
                    oai_check = ui.button("检测可用模型", on_click=check_openai).props("flat dense")
                    oai_models_label = ui.label().classes("text-xs text-gray-400")

                with ui.expansion("Google Gemini", icon="psychology").classes("w-full"):
                    google_key = ui.input("API Key").props("type=password").classes("w-full")
                    google_model = ui.input("模型 (如 gemini-2.0-flash)").classes("w-full")
                    ui.button("检测可用模型", on_click=check_google).props("flat dense")
                    google_models_label = ui.label().classes("text-xs text-gray-400")

                with ui.expansion("Anthropic", icon="auto_awesome").classes("w-full"):
                    ant_key = ui.input("API Key").props("type=password").classes("w-full")
                    ant_model = ui.input("模型 (如 claude-3-5-sonnet)").classes("w-full")
                    ui.button("检测可用模型", on_click=check_anthropic).props("flat dense")
                    ant_models_label = ui.label().classes("text-xs text-gray-400")

                with ui.expansion("Ollama (本地)", icon="computer").classes("w-full"):
                    ollama_url = ui.input("URL (如 http://localhost:11434)").classes("w-full")
                    ollama_model = ui.input("模型 (如 llama3.2:3b)").classes("w-full")
                    ui.button("检测已拉取模型", on_click=check_ollama).props("flat dense")
                    ollama_models_label = ui.label().classes("text-xs text-gray-400")

                with ui.expansion("自定义 OpenAI Compatible", icon="extension").classes("w-full"):
                    compat_active = ui.select(COMPAT_OPTIONS, value="custom", label="当前厂商").classes("w-64")
                    for name in ["DeepSeek", "Kimi", "Qwen", "自定义"]:
                        ui.label(name).classes("text-sm font-semibold mt-2")
                    ds_url = ui.input("DeepSeek URL").classes("w-full")
                    ds_key = ui.input("DeepSeek Key").props("type=password").classes("w-full")
                    ds_model = ui.input("DeepSeek 模型").classes("w-full")
                    kimi_url = ui.input("Kimi URL").classes("w-full")
                    kimi_key = ui.input("Kimi Key").props("type=password").classes("w-full")
                    kimi_model = ui.input("Kimi 模型").classes("w-full")
                    qwen_url = ui.input("Qwen URL").classes("w-full")
                    qwen_key = ui.input("Qwen Key").props("type=password").classes("w-full")
                    qwen_model = ui.input("Qwen 模型").classes("w-full")
                    cust_url = ui.input("自定义 URL").classes("w-full")
                    cust_key = ui.input("自定义 Key").props("type=password").classes("w-full")
                    cust_model = ui.input("自定义模型").classes("w-full")

            # ── 右栏: 图像与高级 ──
            with ui.card().classes("w-80"):
                ui.label("图像配置").classes("font-semibold mb-2")
                disable_img = ui.checkbox("禁用图像生成")
                img_provider = ui.select(IMAGE_PROVIDERS, label="图像提供商").classes("w-full")
                pexels_key = ui.input("Pexels Key").props("type=password").classes("w-full")
                pixabay_key = ui.input("Pixabay Key").props("type=password").classes("w-full")

                with ui.expansion("ComfyUI", icon="brush").classes("w-full"):
                    comfy_url = ui.input("ComfyUI URL").classes("w-full")
                    comfy_wf = ui.textarea("Workflow JSON").props("rows=3").classes("w-full")

                with ui.expansion("图像质量").classes("w-full"):
                    dalle_q = ui.input("DALL-E 3 质量 (standard/hd)").classes("w-full")
                    gpt_img_q = ui.input("GPT Image 1.5 质量 (low/medium/high)").classes("w-full")

                ui.label("高级选项").classes("font-semibold mt-4 mb-2")
                tool_calls = ui.checkbox("启用工具调用")
                disable_think = ui.checkbox("禁用思考")
                extended_reason = ui.checkbox("扩展推理")
                web_ground = ui.checkbox("联网检索")

                with ui.expansion("主题与页脚", icon="palette").classes("w-full"):
                    theme_primary = ui.input("主题主色 (hex 如 #6C63FF)").classes("w-full")
                    footer_text = ui.input("页脚文字").classes("w-full")

                    async def load_theme_footer():
                        st, td = await api_get("/api/v1/ppt/theme/?userId=default")
                        sf, fd = await api_get("/api/v1/ppt/footer/?userId=default")
                        if st == 200 and isinstance(td, dict):
                            theme_data = td.get("themeData") or {}
                            theme_primary.value = theme_data.get("primaryColor") or theme_data.get("primary") or "#6C63FF"
                        if sf == 200 and isinstance(fd, dict):
                            props = fd.get("properties") or {}
                            footer_text.value = props.get("text") or props.get("footerText") or ""

                    async def save_theme_footer():
                        await api_post("/api/v1/ppt/theme/", {"userId": "default", "themeData": {"primaryColor": theme_primary.value or "#6C63FF"}})
                        await api_post("/api/v1/ppt/footer/", {"userId": "default", "properties": {"text": footer_text.value or ""}})
                        ui.notify("主题与页脚已保存", type="positive")

                    with ui.row().classes("gap-2"):
                        ui.button("加载", on_click=load_theme_footer).props("flat dense size=sm")
                        ui.button("保存", on_click=save_theme_footer).props("flat dense size=sm color=primary")

        log = ui.log().classes("h-28 w-full")
        result_label = ui.label().classes("text-green-600")

        # ── 操作按钮 ──
        with ui.row().classes("gap-3"):
            ui.button("保存配置", icon="save", on_click=save_config).props("color=primary")
            ui.button("重新加载", icon="refresh", on_click=load_config).props("flat")

    ui.timer(0.2, load_config, once=True)
