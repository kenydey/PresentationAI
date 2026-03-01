"""LLM 结构化响应规范化 — 处理多种返回格式。"""

import json
from typing import Any


def normalize_presentation_state_response(raw: Any) -> dict:
    """
    将 LLM 多种返回格式规范为 {title?, slides}。
    支持:
    - {"response": "{\"title\":...}"} — JSON 字符串
    - {"presentation": {"title": "...", "slides": [...]}}
    - {"title": "...", "slides": [...]} — 直接格式
    """
    if not isinstance(raw, dict):
        return raw

    # 1. {"response": "{\"title\":...}"} — JSON 字符串
    resp_val = raw.get("response")
    if isinstance(resp_val, str) and resp_val.strip().startswith("{"):
        try:
            raw = json.loads(resp_val)
        except json.JSONDecodeError:
            pass

    # 2. {"presentation": {"title": "...", "slides": [...]}}
    if "presentation" in raw and "slides" not in raw:
        inner = raw.get("presentation")
        if isinstance(inner, dict) and "slides" in inner:
            return inner

    return raw
