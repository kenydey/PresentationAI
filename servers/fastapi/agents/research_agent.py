"""RESEARCH_AGENT — 从输入提取结构化 JSON 大纲。"""

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from agents.prompts import RESEARCH_AGENT_SYSTEM_PROMPT
from models.llm_message import LLMSystemMessage, LLMUserMessage
from models.presentation_state import PresentationState, SlideState
from services.llm_client import LLMClient
from utils.llm_client_error_handler import handle_llm_client_exceptions
from utils.llm_provider import get_model_for_task
from utils.llm_response_normalizer import normalize_presentation_state_response
from models.llm_tools import SearchWebTool


def _get_presentation_state_schema_for_n_slides(n_slides: int) -> dict:
    """生成约束幻灯片数量的 PresentationState JSON schema。"""
    schema = PresentationState.model_json_schema()
    schema["properties"]["slides"]["minItems"] = n_slides
    schema["properties"]["slides"]["maxItems"] = n_slides
    return schema


def _get_messages(
    content: str,
    n_slides: int,
    language: str,
    additional_context: Optional[str] = None,
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
    include_title_slide: bool = True,
) -> list:
    system = RESEARCH_AGENT_SYSTEM_PROMPT
    if instructions:
        system += f"\n\n# 用户附加指令\n{instructions}"
    if tone:
        system += f"\n\n# 语气\n{tone}"
    if verbosity:
        system += f"\n\n# 详略\n{verbosity}"

    user_content = f"""
## 输入
- 用户内容: {content or "请根据主题创建演示"}
- 输出语言: {language}
- 幻灯片数量: {n_slides}
- 当前时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- 额外上下文: {additional_context or "无"}
- 首页为标题页: {"是" if include_title_slide else "否"}
"""
    return [
        LLMSystemMessage(content=system.strip()),
        LLMUserMessage(content=user_content.strip()),
    ]


async def research_agent_run(
    content: str,
    n_slides: int,
    language: str = "Chinese",
    additional_context: Optional[str] = None,
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
    include_title_slide: bool = True,
    web_search: bool = False,
) -> PresentationState:
    """
    从用户输入提取结构化 JSON 大纲。
    返回 PresentationState，layout_id 为 "pending"，由 DESIGN_AGENT 后续填充。
    """
    model = get_model_for_task("outline")
    client = LLMClient()

    tools = [SearchWebTool] if (client.enable_web_grounding() and web_search) else None

    schema = _get_presentation_state_schema_for_n_slides(n_slides)
    messages = _get_messages(
        content,
        n_slides,
        language,
        additional_context,
        tone,
        verbosity,
        instructions,
        include_title_slide,
    )
    last_error = None
    for attempt in range(2):
        try:
            response = await client.generate_structured(
                model=model,
                messages=messages,
                response_format=schema,
                strict=True,
                tools=tools,
            )
            response = normalize_presentation_state_response(response)
            return PresentationState.model_validate(response)
        except Exception as e:
            last_error = e
            if attempt == 0 and "did not return any content" in str(e):
                continue
            raise handle_llm_client_exceptions(e)
    raise handle_llm_client_exceptions(last_error)
