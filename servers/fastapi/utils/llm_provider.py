from fastapi import HTTPException

from constants.llm import (
    DEFAULT_ANTHROPIC_MODEL,
    DEFAULT_GOOGLE_MODEL,
    DEFAULT_OPENAI_MODEL,
)
from enums.llm_provider import LLMProvider
from utils.get_env import (
    get_anthropic_model_env,
    get_custom_model_env,
    get_google_model_env,
    get_llm_provider_env,
    get_ollama_model_env,
    get_openai_model_env,
)
from utils.user_config import get_user_config


def get_llm_provider():
    """返回当前 LLM 提供商；优先使用环境变量 LLM，未设置时从 userConfig 读取。"""
    env_val = get_llm_provider_env()
    if env_val:
        try:
            return LLMProvider(env_val)
        except ValueError:
            pass
    # 回退到 userConfig（确保配置了 DeepSeek 等 custom 时无需预置 LLM 环境变量）
    cfg = get_user_config()
    provider_val = cfg.default_llm_provider or cfg.LLM
    if provider_val:
        try:
            return LLMProvider(provider_val)
        except ValueError:
            pass
    raise HTTPException(
        status_code=500,
        detail=(
            "Invalid or missing LLM provider. Please select one of: openai, google, anthropic, ollama, custom. "
            "Configure in Settings (系统设置) or set LLM environment variable."
        ),
    )


def is_openai_selected():
    return get_llm_provider() == LLMProvider.OPENAI


def is_google_selected():
    return get_llm_provider() == LLMProvider.GOOGLE


def is_anthropic_selected():
    return get_llm_provider() == LLMProvider.ANTHROPIC


def is_ollama_selected():
    return get_llm_provider() == LLMProvider.OLLAMA


def is_custom_llm_selected():
    return get_llm_provider() == LLMProvider.CUSTOM


def _get_default_model_for_provider(provider: LLMProvider):
    if provider == LLMProvider.OPENAI:
        return get_openai_model_env() or DEFAULT_OPENAI_MODEL
    if provider == LLMProvider.GOOGLE:
        return get_google_model_env() or DEFAULT_GOOGLE_MODEL
    if provider == LLMProvider.ANTHROPIC:
        return get_anthropic_model_env() or DEFAULT_ANTHROPIC_MODEL
    if provider == LLMProvider.OLLAMA:
        return get_ollama_model_env()
    if provider == LLMProvider.CUSTOM:
        return get_custom_model_env()
    raise HTTPException(
        status_code=500,
        detail=(
            "Invalid LLM provider. Please select one of: "
            "openai, google, anthropic, ollama, custom"
        ),
    )


def get_model():
    """保持旧接口行为：返回当前 provider 下的默认模型。"""
    selected_llm = get_llm_provider()
    return _get_default_model_for_provider(selected_llm)


def get_model_for_task(task: str | None) -> str:
    """根据任务类型（outline/content/notes/research）返回合适的模型名。"""
    cfg = get_user_config()
    provider = get_llm_provider()

    if task == "outline":
        if cfg.outline_model:
            return cfg.outline_model
    elif task == "content":
        if cfg.content_model:
            return cfg.content_model
    elif task == "notes":
        if cfg.research_model and task == "research":
            # 兼容旧字段名（若未来拆分可重构）
            return cfg.research_model
    if task == "research":
        if cfg.research_model:
            return cfg.research_model

    # 任务级别未配置时，回退到全局默认模型
    if cfg.default_llm_model:
        return cfg.default_llm_model

    return _get_default_model_for_provider(provider)
