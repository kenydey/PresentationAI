"""
Pipeline 文本生成模块：纯 LLM 内容生成，不包含图像或 pptx 逻辑。
封装现有 generate_presentation_stream 与 outline 生成能力。
"""

import json
from typing import AsyncIterator, Optional

from langchain_core.output_parsers import JsonOutputParser

# 兼容双路径：ppt_generator 流式生成 与 utils/llm_calls outline 生成
try:
    from ppt_generator.generator import generate_presentation_stream
    from ppt_generator.models.llm_models import LLMPresentationModel

    _HAS_PPT_GENERATOR = True
except ImportError:
    _HAS_PPT_GENERATOR = False

try:
    from utils.llm_calls.generate_presentation_outlines import (
        generate_ppt_outline as _generate_ppt_outline,
    )

    _HAS_OUTLINE = True
except ImportError:
    _HAS_OUTLINE = False


_output_parser = (
    JsonOutputParser(pydantic_object=LLMPresentationModel) if _HAS_PPT_GENERATOR else None
)


async def generate_presentation_text(
    titles: list[str],
    prompt: str,
    n_slides: int,
    language: str,
    summary: str = "",
) -> AsyncIterator[str]:
    """
    流式生成演示文稿 JSON 文本。
    数据流：Prompt -> LLM -> JSON 格式大纲/幻灯片内容。
    """
    if not _HAS_PPT_GENERATOR:
        raise ImportError("ppt_generator.generator is required for generate_presentation_text")

    async for chunk in generate_presentation_stream(
        titles, prompt, n_slides, language, summary
    ):
        if hasattr(chunk, "content"):
            yield chunk.content
        else:
            yield str(chunk)


def parse_presentation_json(text: str) -> dict:
    """解析 LLM 输出的 JSON 为字典。"""
    if not _output_parser:
        return json.loads(text)
    return _output_parser.parse(text)


async def generate_outline(
    content: str,
    n_slides: int,
    language: Optional[str] = None,
    additional_context: Optional[str] = None,
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
    include_title_slide: bool = True,
    web_search: bool = False,
):
    """
    流式生成大纲（Outline）。
    用于基于 outline 的生成流程。
    """
    if not _HAS_OUTLINE:
        raise ImportError(
            "utils.llm_calls.generate_presentation_outlines is required for generate_outline"
        )

    async for chunk in _generate_ppt_outline(
        content=content,
        n_slides=n_slides,
        language=language,
        additional_context=additional_context,
        tone=tone,
        verbosity=verbosity,
        instructions=instructions,
        include_title_slide=include_title_slide,
        web_search=web_search,
    ):
        yield chunk
