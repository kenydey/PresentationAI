from typing import Dict, Optional

from pydantic import BaseModel


class ProviderConfig(BaseModel):
    """通用 LLM 提供商配置"""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    default_model: Optional[str] = None


class OllamaConfig(BaseModel):
    """Ollama 配置（只需要 URL 与模型名）"""

    base_url: Optional[str] = None
    default_model: Optional[str] = None


class OpenAICompatibleProviderConfig(BaseModel):
    """OpenAI 兼容厂商配置，例如 DeepSeek、Kimi、302AI 等"""

    display_name: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    default_model: Optional[str] = None


class UserConfig(BaseModel):
    # 顶层通用 LLM 配置
    LLM: Optional[str] = None  # 旧字段，等价于 default_llm_provider
    default_llm_provider: Optional[str] = None
    default_llm_model: Optional[str] = None

    # 按任务类型区分的提供商与模型（可选）
    outline_provider: Optional[str] = None
    outline_model: Optional[str] = None
    content_provider: Optional[str] = None
    content_model: Optional[str] = None
    notes_provider: Optional[str] = None
    speaker_notes_model: Optional[str] = None
    research_provider: Optional[str] = None
    research_model: Optional[str] = None

    # OpenAI（平铺字段用于向后兼容已有环境变量）
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: Optional[str] = None

    # Google
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_MODEL: Optional[str] = None

    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: Optional[str] = None

    # Ollama
    OLLAMA_URL: Optional[str] = None
    OLLAMA_MODEL: Optional[str] = None

    # Custom LLM
    CUSTOM_LLM_URL: Optional[str] = None
    CUSTOM_LLM_API_KEY: Optional[str] = None
    CUSTOM_MODEL: Optional[str] = None

    # 结构化 provider 配置（新字段，供 LLM 客户端工厂使用）
    openai_config: Optional[ProviderConfig] = None
    anthropic_config: Optional[ProviderConfig] = None
    google_config: Optional[ProviderConfig] = None
    ollama_config: Optional[OllamaConfig] = None
    openai_compatible_configs: Optional[
        Dict[str, OpenAICompatibleProviderConfig]
    ] = None
    # 当前选中的 OpenAI 兼容厂商 key（如 deepseek、kimi、qwen、custom）
    active_openai_compatible: Optional[str] = None

    # Image Provider
    DISABLE_IMAGE_GENERATION: Optional[bool] = None
    IMAGE_PROVIDER: Optional[str] = None
    PEXELS_API_KEY: Optional[str] = None
    PIXABAY_API_KEY: Optional[str] = None

    # ComfyUI
    COMFYUI_URL: Optional[str] = None
    COMFYUI_WORKFLOW: Optional[str] = None

    # Dalle 3 Quality
    DALL_E_3_QUALITY: Optional[str] = None
    # Gpt Image 1.5 Quality
    GPT_IMAGE_1_5_QUALITY: Optional[str] = None

    # Reasoning
    TOOL_CALLS: Optional[bool] = None
    DISABLE_THINKING: Optional[bool] = None
    EXTENDED_REASONING: Optional[bool] = None

    # Web Search
    WEB_GROUNDING: Optional[bool] = None
