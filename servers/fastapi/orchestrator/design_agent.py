"""
设计智能体 (Design Agent)：将研究智能体输出的 JSON 大纲映射到布局 ID。
推荐模型：Gemini 1.5 Pro（擅长自由形态视觉设计）
"""

from typing import Optional

from constants.prompt_constraints import LAYOUT_CHAR_LIMITS, TEXT_OVERFLOW_SYSTEM_HINT

try:
    from utils.llm_calls.generate_presentation_structure import (
        generate_presentation_structure,
    )
    from models.presentation_outline_model import PresentationOutlineModel
    from models.presentation_layout import PresentationLayoutModel
    from models.presentation_structure_model import PresentationStructureModel

    _HAS_STRUCTURE = True
except ImportError:
    _HAS_STRUCTURE = False


class DesignAgent:
    """设计智能体：为大纲分配布局 ID。"""

    @property
    def layout_rules(self) -> str:
        return """
# 布局选择规则
- 如果内容包含超过 4 个项目符号，必须选择双列布局（layout_id: dual_column_list）
- 如果当前幻灯片包含数据对比，选择图表布局
- 内容驱动选择：开场/结束用 Title，流程用 Visual process，对比用 Side-by-side
"""

    async def run(
        self,
        outline: "PresentationOutlineModel",
        presentation_layout: "PresentationLayoutModel",
        instructions: Optional[str] = None,
        using_slides_markdown: bool = False,
    ) -> "PresentationStructureModel":
        """
        将大纲映射到布局 ID。
        """
        if not _HAS_STRUCTURE:
            raise ImportError(
                "utils.llm_calls.generate_presentation_structure is required"
            )

        enhanced_instructions = (instructions or "") + "\n" + self.layout_rules
        return await generate_presentation_structure(
            outline,
            presentation_layout,
            instructions=enhanced_instructions,
            using_slides_markdown=using_slides_markdown,
        )
