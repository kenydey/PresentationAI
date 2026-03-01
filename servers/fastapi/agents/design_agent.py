"""DESIGN_AGENT — 为大纲分配合适的 layout_id。"""

from typing import Optional

from agents.prompts import DESIGN_AGENT_SYSTEM_PROMPT
from models.llm_message import LLMSystemMessage, LLMUserMessage
from models.presentation_state import PresentationState
from services.llm_client import LLMClient
from utils.llm_client_error_handler import handle_llm_client_exceptions
from utils.llm_provider import get_model_for_task
from utils.template_registry import get_layout_by_group


def _build_layout_list(layout_group: str) -> str:
    """构建布局列表字符串，供 system prompt 使用。"""
    layout_model = get_layout_by_group(layout_group)
    if not layout_model:
        return "无可用布局"
    lines = []
    for s in layout_model.slides:
        desc = (s.description or "").strip() or "-"
        lines.append(f"- {s.id}: {s.name or s.id} — {desc}")
    return "\n".join(lines)


def _get_schema_with_layout_enum(layout_group: str, n_slides: int) -> dict:
    """生成 schema，将 layout_id 限制为指定组的 ID，并约束幻灯片数量。"""
    layout_model = get_layout_by_group(layout_group)
    schema = PresentationState.model_json_schema()
    schema["properties"]["slides"]["minItems"] = n_slides
    schema["properties"]["slides"]["maxItems"] = n_slides
    if layout_model and layout_model.slides:
        valid_ids = [s.id for s in layout_model.slides]
        items = schema.get("properties", {}).get("slides", {}).get("items", {})
        if isinstance(items, dict) and "properties" in items:
            items["properties"]["layout_id"] = {
                "type": "string",
                "description": "布局 ID，必须从可用列表选取",
                "enum": valid_ids,
            }
    return schema


async def design_agent_run(
    state: PresentationState,
    layout_group: str = "general",
    instructions: Optional[str] = None,
) -> PresentationState:
    """
    为每页幻灯片分配合适的 layout_id。
    layout_id 仅从指定 layout_group 的布局中选取。
    """
    layout_model = get_layout_by_group(layout_group)
    if not layout_model or not layout_model.slides:
        raise ValueError(f"Layout group '{layout_group}' not found or has no slides")

    model = get_model_for_task("outline")  # 复用 outline 任务模型
    client = LLMClient()

    layout_list = _build_layout_list(layout_group)
    system = DESIGN_AGENT_SYSTEM_PROMPT.format(layout_list=layout_list)
    if instructions:
        system += f"\n\n# 用户附加指令\n{instructions}"

    user_content = f"""
请为以下每页幻灯片分配合适的 layout_id。layout_id 必须从上述列表中选取。

{state.model_dump_json(indent=2, exclude_none=True)}
"""

    messages = [
        LLMSystemMessage(content=system.strip()),
        LLMUserMessage(content=user_content.strip()),
    ]

    schema = _get_schema_with_layout_enum(layout_group, len(state.slides))

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
