"""配置 DeepSeek 为默认 LLM（OpenAI Compatible）。

用法:
  DEEPSEEK_API_KEY=sk-xxx uv run python scripts/configure_deepseek.py
  或在交互式环境中传入 api_key 参数。
"""

import json
import os
import sys


def configure_deepseek(
    api_key: str,
    model: str = "deepseek-chat",
    base_url: str = "https://api.deepseek.com",
) -> str:
    """将 DeepSeek 写入 userConfig.json，返回配置路径。"""
    # 确定 config 路径（与 get_user_config_path_env 一致）
    user_config_path = os.getenv("USER_CONFIG_PATH")
    if not user_config_path or not user_config_path.strip():
        app_data = os.getenv("APP_DATA_DIRECTORY") or os.path.join(os.getcwd(), "app_data")
        user_config_path = os.path.join(app_data, "userConfig.json")

    existing = {}
    if os.path.exists(user_config_path):
        try:
            with open(user_config_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            pass

    # 合并 DeepSeek 配置
    profiles = dict(existing.get("openai_compatible_configs") or {})
    profiles["deepseek"] = {
        "display_name": "DeepSeek",
        "base_url": base_url,
        "api_key": api_key,
        "default_model": model,
    }
    existing["openai_compatible_configs"] = profiles
    existing["active_openai_compatible"] = "deepseek"
    existing["default_llm_provider"] = "custom"
    existing["LLM"] = "custom"
    existing["default_llm_model"] = model
    # DeepSeek 不支持 response_format，需用 tool_calls 输出结构化 JSON
    existing["TOOL_CALLS"] = True

    os.makedirs(os.path.dirname(user_config_path), exist_ok=True)
    with open(user_config_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return user_config_path


if __name__ == "__main__":
    key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not key:
        print("请设置环境变量 DEEPSEEK_API_KEY")
        sys.exit(1)
    path = configure_deepseek(key)
    print(f"已配置 DeepSeek，配置已写入: {path}")
