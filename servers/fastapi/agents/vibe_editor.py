"""VIBE_EDITOR — 根据自然语言指令修改 PresentationState。"""

from typing import List, Optional

from agents.prompts import VIBE_EDITOR_SYSTEM_PROMPT
from models.llm_message import LLMSystemMessage, LLMUserMessage
from models.presentation_state import PresentationState
from services.llm_client import LLMClient
from utils.llm_client_error_handler import handle_llm_client_exceptions
from utils.llm_provider import get_model_for_task


async def vibe_editor_run(
    state: PresentationState,
    instruction: str,
    language: str = "Chinese",
    allow_layout_change: bool = False,
    available_layout_ids: Optional[List[str]] = None,
) -> PresentationState:
    """
    根据自然语言指令修改 PresentationState。

    Args:
        state: 当前演示状态
        instruction: 用户自然语言指令
        language: 内容语言
        allow_layout_change: 若 True，允许按指令修改 layout_id（如「换成左右排版」）
        available_layout_ids: allow_layout_change 为 True 时，可选的 layout_id 列表
    """
    model = get_model_for_task("outline")
    client = LLMClient()

    schema = PresentationState.model_json_schema()
    schema["properties"]["slides"]["minItems"] = len(state.slides)
    schema["properties"]["slides"]["maxItems"] = len(state.slides)

    system = VIBE_EDITOR_SYSTEM_PROMPT + f"\n\n# 内容语言\n{language}"
    if allow_layout_change and available_layout_ids:
        system += f"\n\n# 排版变更\n当用户指令明确要求更换排版（如「换成左右排版」「改为三列布局」）时，可修改 layout_id。可选 layout_id 列表：{available_layout_ids}"

    layout_rule = (
        "可根据指令修改 layout_id。"
        if allow_layout_change
        else "保持 slides 数量和 layout_id 不变。"
    )
    user_content = f"""
## 当前 PresentationState (JSON)
{state.model_dump_json(indent=2, exclude_none=True)}

## 用户指令
{instruction}

请输出修改后的完整 JSON。保持 slides 数量和顺序不变。{layout_rule}
"""

    messages = [
        LLMSystemMessage(content=system.strip()),
        LLMUserMessage(content=user_content.strip()),
    ]

    try:
        response = await client.generate_structured(
            model=model,
            messages=messages,
            response_format=schema,
            strict=True,
        )
        return PresentationState.model_validate(response)
    except Exception as e:
        raise handle_llm_client_exceptions(e)
