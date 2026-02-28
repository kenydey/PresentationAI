import json
import os

from models.user_config import (
    OllamaConfig,
    OpenAICompatibleProviderConfig,
    ProviderConfig,
    UserConfig,
)
from utils.get_env import (
    get_anthropic_api_key_env,
    get_anthropic_model_env,
    get_comfyui_url_env,
    get_comfyui_workflow_env,
    get_custom_llm_api_key_env,
    get_custom_llm_url_env,
    get_custom_model_env,
    get_dall_e_3_quality_env,
    get_disable_image_generation_env,
    get_disable_thinking_env,
    get_google_api_key_env,
    get_google_model_env,
    get_gpt_image_1_5_quality_env,
    get_llm_provider_env,
    get_ollama_model_env,
    get_ollama_url_env,
    get_openai_api_key_env,
    get_openai_model_env,
    get_pexels_api_key_env,
    get_tool_calls_env,
    get_user_config_path_env,
    get_image_provider_env,
    get_pixabay_api_key_env,
    get_extended_reasoning_env,
    get_web_grounding_env,
)
from utils.parsers import parse_bool_or_none
from utils.set_env import (
    set_anthropic_api_key_env,
    set_anthropic_model_env,
    set_comfyui_url_env,
    set_comfyui_workflow_env,
    set_custom_llm_api_key_env,
    set_custom_llm_url_env,
    set_custom_model_env,
    set_dall_e_3_quality_env,
    set_disable_image_generation_env,
    set_disable_thinking_env,
    set_extended_reasoning_env,
    set_google_api_key_env,
    set_google_model_env,
    set_gpt_image_1_5_quality_env,
    set_llm_provider_env,
    set_ollama_model_env,
    set_ollama_url_env,
    set_openai_api_key_env,
    set_openai_model_env,
    set_pexels_api_key_env,
    set_image_provider_env,
    set_pixabay_api_key_env,
    set_tool_calls_env,
    set_web_grounding_env,
)


def get_user_config() -> UserConfig:
    user_config_path = get_user_config_path_env()

    existing_config = UserConfig()
    try:
        if os.path.exists(user_config_path):
            with open(user_config_path, "r") as f:
                existing_config = UserConfig(**json.load(f))
    except Exception:
        print("Error while loading user config")
        pass

    # 推断默认 provider 与模型（支持旧字段 LLM 与 OPENAI_MODEL）
    inferred_provider = (
        existing_config.default_llm_provider
        or existing_config.LLM
        or get_llm_provider_env()
    )
    inferred_default_model = (
        existing_config.default_llm_model
        or existing_config.OPENAI_MODEL
        or get_openai_model_env()
    )

    # 结构化 provider 配置（优先使用已有结构化字段，否则从平铺字段和环境变量推断）
    openai_config = existing_config.openai_config or ProviderConfig(
        api_key=existing_config.OPENAI_API_KEY or get_openai_api_key_env(),
        base_url=None,
        default_model=existing_config.OPENAI_MODEL or get_openai_model_env(),
    )
    anthropic_config = existing_config.anthropic_config or ProviderConfig(
        api_key=existing_config.ANTHROPIC_API_KEY or get_anthropic_api_key_env(),
        base_url=None,
        default_model=existing_config.ANTHROPIC_MODEL or get_anthropic_model_env(),
    )
    google_config = existing_config.google_config or ProviderConfig(
        api_key=existing_config.GOOGLE_API_KEY or get_google_api_key_env(),
        base_url=None,
        default_model=existing_config.GOOGLE_MODEL or get_google_model_env(),
    )
    ollama_config = existing_config.ollama_config or OllamaConfig(
        base_url=existing_config.OLLAMA_URL or get_ollama_url_env(),
        default_model=existing_config.OLLAMA_MODEL or get_ollama_model_env(),
    )

    # OpenAI 兼容厂商配置：保持已有值，并自动为 legacy CUSTOM_* 字段补充 custom profile
    openai_compatible_configs = dict(
        existing_config.openai_compatible_configs or {}
    )

    # 从 legacy CUSTOM_* 字段与环境变量构造/补全 "custom" 配置
    legacy_custom_url = existing_config.CUSTOM_LLM_URL or get_custom_llm_url_env()
    legacy_custom_key = (
        existing_config.CUSTOM_LLM_API_KEY or get_custom_llm_api_key_env()
    )
    legacy_custom_model = existing_config.CUSTOM_MODEL or get_custom_model_env()

    if legacy_custom_url or legacy_custom_key or legacy_custom_model:
        custom_cfg = openai_compatible_configs.get("custom") or OpenAICompatibleProviderConfig(
            display_name="Custom"
        )
        if not custom_cfg.base_url:
            custom_cfg.base_url = legacy_custom_url
        if not custom_cfg.api_key:
            custom_cfg.api_key = legacy_custom_key
        if not custom_cfg.default_model:
            custom_cfg.default_model = legacy_custom_model
        openai_compatible_configs["custom"] = custom_cfg

    # 选中活动的 openai_compatible profile
    active_openai_compatible = (
        existing_config.active_openai_compatible
        or ("deepseek" if "deepseek" in openai_compatible_configs else None)
        or ("kimi" if "kimi" in openai_compatible_configs else None)
        or ("qwen" if "qwen" in openai_compatible_configs else None)
        or ("custom" if "custom" in openai_compatible_configs else None)
    )

    return UserConfig(
        # 顶层 LLM 配置
        LLM=inferred_provider,
        default_llm_provider=inferred_provider,
        default_llm_model=inferred_default_model,
        outline_provider=existing_config.outline_provider,
        outline_model=existing_config.outline_model,
        content_provider=existing_config.content_provider,
        content_model=existing_config.content_model,
        notes_provider=existing_config.notes_provider,
        speaker_notes_model=existing_config.speaker_notes_model,
        research_provider=existing_config.research_provider,
        research_model=existing_config.research_model,
        # 平铺字段（向后兼容）
        OPENAI_API_KEY=openai_config.api_key,
        OPENAI_MODEL=openai_config.default_model,
        GOOGLE_API_KEY=google_config.api_key,
        GOOGLE_MODEL=google_config.default_model,
        ANTHROPIC_API_KEY=anthropic_config.api_key,
        ANTHROPIC_MODEL=anthropic_config.default_model,
        OLLAMA_URL=ollama_config.base_url,
        OLLAMA_MODEL=ollama_config.default_model,
        CUSTOM_LLM_URL=existing_config.CUSTOM_LLM_URL or get_custom_llm_url_env(),
        CUSTOM_LLM_API_KEY=existing_config.CUSTOM_LLM_API_KEY
        or get_custom_llm_api_key_env(),
        CUSTOM_MODEL=existing_config.CUSTOM_MODEL or get_custom_model_env(),
        # 结构化 provider 配置
        openai_config=openai_config,
        anthropic_config=anthropic_config,
        google_config=google_config,
        ollama_config=ollama_config,
        openai_compatible_configs=openai_compatible_configs,
        active_openai_compatible=active_openai_compatible,
        # Image Provider
        IMAGE_PROVIDER=existing_config.IMAGE_PROVIDER or get_image_provider_env(),
        DISABLE_IMAGE_GENERATION=(
            existing_config.DISABLE_IMAGE_GENERATION
            if existing_config.DISABLE_IMAGE_GENERATION is not None
            else (parse_bool_or_none(get_disable_image_generation_env()) or False)
        ),
        PIXABAY_API_KEY=existing_config.PIXABAY_API_KEY or get_pixabay_api_key_env(),
        PEXELS_API_KEY=existing_config.PEXELS_API_KEY or get_pexels_api_key_env(),
        # ComfyUI
        COMFYUI_URL=existing_config.COMFYUI_URL or get_comfyui_url_env(),
        COMFYUI_WORKFLOW=existing_config.COMFYUI_WORKFLOW or get_comfyui_workflow_env(),
        # 其它高级设置
        DALL_E_3_QUALITY=existing_config.DALL_E_3_QUALITY or get_dall_e_3_quality_env(),
        GPT_IMAGE_1_5_QUALITY=existing_config.GPT_IMAGE_1_5_QUALITY
        or get_gpt_image_1_5_quality_env(),
        TOOL_CALLS=(
            existing_config.TOOL_CALLS
            if existing_config.TOOL_CALLS is not None
            else (parse_bool_or_none(get_tool_calls_env()) or False)
        ),
        DISABLE_THINKING=(
            existing_config.DISABLE_THINKING
            if existing_config.DISABLE_THINKING is not None
            else (parse_bool_or_none(get_disable_thinking_env()) or False)
        ),
        EXTENDED_REASONING=(
            existing_config.EXTENDED_REASONING
            if existing_config.EXTENDED_REASONING is not None
            else (parse_bool_or_none(get_extended_reasoning_env()) or False)
        ),
        WEB_GROUNDING=(
            existing_config.WEB_GROUNDING
            if existing_config.WEB_GROUNDING is not None
            else (parse_bool_or_none(get_web_grounding_env()) or False)
        ),
    )


def update_env_with_user_config() -> None:
    user_config = get_user_config()
    # 统一同步默认 provider
    provider = user_config.default_llm_provider or user_config.LLM
    if provider:
        set_llm_provider_env(provider)

    # OpenAI
    openai_cfg = user_config.openai_config or ProviderConfig()
    if openai_cfg.api_key:
        set_openai_api_key_env(openai_cfg.api_key)
    elif user_config.OPENAI_API_KEY:
        set_openai_api_key_env(user_config.OPENAI_API_KEY)
    if openai_cfg.default_model:
        set_openai_model_env(openai_cfg.default_model)
    elif user_config.OPENAI_MODEL:
        set_openai_model_env(user_config.OPENAI_MODEL)

    # Google
    google_cfg = user_config.google_config or ProviderConfig()
    if google_cfg.api_key:
        set_google_api_key_env(google_cfg.api_key)
    elif user_config.GOOGLE_API_KEY:
        set_google_api_key_env(user_config.GOOGLE_API_KEY)
    if google_cfg.default_model:
        set_google_model_env(google_cfg.default_model)
    elif user_config.GOOGLE_MODEL:
        set_google_model_env(user_config.GOOGLE_MODEL)

    # Anthropic
    anthropic_cfg = user_config.anthropic_config or ProviderConfig()
    if anthropic_cfg.api_key:
        set_anthropic_api_key_env(anthropic_cfg.api_key)
    elif user_config.ANTHROPIC_API_KEY:
        set_anthropic_api_key_env(user_config.ANTHROPIC_API_KEY)
    if anthropic_cfg.default_model:
        set_anthropic_model_env(anthropic_cfg.default_model)
    elif user_config.ANTHROPIC_MODEL:
        set_anthropic_model_env(user_config.ANTHROPIC_MODEL)

    # Ollama
    ollama_cfg = user_config.ollama_config or OllamaConfig()
    if ollama_cfg.base_url:
        set_ollama_url_env(ollama_cfg.base_url)
    elif user_config.OLLAMA_URL:
        set_ollama_url_env(user_config.OLLAMA_URL)
    if ollama_cfg.default_model:
        set_ollama_model_env(ollama_cfg.default_model)
    elif user_config.OLLAMA_MODEL:
        set_ollama_model_env(user_config.OLLAMA_MODEL)

    # 自定义 / OpenAI 兼容 LLM
    active_key = user_config.active_openai_compatible
    profile = None
    if user_config.openai_compatible_configs:
        if active_key and active_key in user_config.openai_compatible_configs:
            profile = user_config.openai_compatible_configs[active_key]
        elif user_config.openai_compatible_configs:
            # 退回第一个配置
            profile = next(iter(user_config.openai_compatible_configs.values()))

    if profile:
        if profile.base_url:
            set_custom_llm_url_env(profile.base_url)
        if profile.api_key:
            set_custom_llm_api_key_env(profile.api_key)
        if profile.default_model:
            set_custom_model_env(profile.default_model)
    else:
        # 兼容旧逻辑：直接使用散列的 CUSTOM_* 字段
        if user_config.CUSTOM_LLM_URL:
            set_custom_llm_url_env(user_config.CUSTOM_LLM_URL)
        if user_config.CUSTOM_LLM_API_KEY:
            set_custom_llm_api_key_env(user_config.CUSTOM_LLM_API_KEY)
        if user_config.CUSTOM_MODEL:
            set_custom_model_env(user_config.CUSTOM_MODEL)
    if user_config.DISABLE_IMAGE_GENERATION is not None:
        set_disable_image_generation_env(str(user_config.DISABLE_IMAGE_GENERATION))
    if user_config.IMAGE_PROVIDER:
        set_image_provider_env(user_config.IMAGE_PROVIDER)
    if user_config.PIXABAY_API_KEY:
        set_pixabay_api_key_env(user_config.PIXABAY_API_KEY)
    if user_config.PEXELS_API_KEY:
        set_pexels_api_key_env(user_config.PEXELS_API_KEY)
    if user_config.COMFYUI_URL:
        set_comfyui_url_env(user_config.COMFYUI_URL)
    if user_config.COMFYUI_WORKFLOW:
        set_comfyui_workflow_env(user_config.COMFYUI_WORKFLOW)
    if user_config.DALL_E_3_QUALITY:
        set_dall_e_3_quality_env(user_config.DALL_E_3_QUALITY)
    if user_config.GPT_IMAGE_1_5_QUALITY:
        set_gpt_image_1_5_quality_env(user_config.GPT_IMAGE_1_5_QUALITY)
    if user_config.TOOL_CALLS is not None:
        set_tool_calls_env(str(user_config.TOOL_CALLS))
    if user_config.DISABLE_THINKING is not None:
        set_disable_thinking_env(str(user_config.DISABLE_THINKING))
    if user_config.EXTENDED_REASONING is not None:
        set_extended_reasoning_env(str(user_config.EXTENDED_REASONING))
    if user_config.WEB_GROUNDING is not None:
        set_web_grounding_env(str(user_config.WEB_GROUNDING))
