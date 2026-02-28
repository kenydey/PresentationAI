"""
Pipeline 模块：借鉴 slides_generator 的直线性数据流，将文本生成、图像请求、pptx 构造严格物理隔离。
为后续接入 Orchestrator 与多智能体提供清晰的接入点。
"""

from pipeline.pptx_constructor import build_pptx_from_model

from pipeline.text_generation import (
    generate_presentation_text,
    parse_presentation_json,
    generate_outline,
)
from pipeline.image_requests import fetch_slide_assets, allocate_asset_paths

__all__ = [
    "generate_presentation_text",
    "generate_outline",
    "parse_presentation_json",
    "fetch_slide_assets",
    "allocate_asset_paths",
    "build_pptx_from_model",
]
