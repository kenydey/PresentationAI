"""
研究智能体 (Research Agent)：深度研究集成，输出高度结构化的 JSON 大纲。
推荐模型：Claude 3.5 / GLM-4
"""

from typing import AsyncIterator, Optional

from constants.prompt_constraints import TEXT_OVERFLOW_SYSTEM_HINT

try:
    from utils.llm_calls.generate_presentation_outlines import generate_ppt_outline

    _HAS_OUTLINE = True
except ImportError:
    _HAS_OUTLINE = False


class ResearchAgent:
    """研究智能体：从用户输入生成演示文稿大纲。"""

    def __init__(
        self,
        model_task: str = "outline",
    ):
        self.model_task = model_task

    @property
    def system_hint(self) -> str:
        return f"""
你是一名资深的数据分析师与演示文稿架构师。
请分析提供的文本材料并提取演示文稿大纲。
你的输出必须是符合给定 Pydantic 模式的纯 JSON 格式。
严禁在输出中包含任何 Markdown 代码块修饰符（如 ```json）或解释性的人类对话文本。

{TEXT_OVERFLOW_SYSTEM_HINT}
""".strip()

    async def run(
        self,
        content: str,
        n_slides: int,
        language: Optional[str] = None,
        additional_context: Optional[str] = None,
        tone: Optional[str] = None,
        verbosity: Optional[str] = None,
        instructions: Optional[str] = None,
        include_title_slide: bool = True,
        web_search: bool = False,
    ) -> AsyncIterator:
        """
        执行深度研究，流式输出大纲。
        """
        if not _HAS_OUTLINE:
            raise ImportError(
                "utils.llm_calls.generate_presentation_outlines is required"
            )

        async for chunk in generate_ppt_outline(
            content=content,
            n_slides=n_slides,
            language=language or "en",
            additional_context=additional_context,
            tone=tone,
            verbosity=verbosity,
            instructions=instructions,
            include_title_slide=include_title_slide,
            web_search=web_search,
        ):
            yield chunk
