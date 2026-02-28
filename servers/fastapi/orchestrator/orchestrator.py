"""
主控调度器 (Orchestrator)：调度 Research -> Design 管线。
可选扩展 Review Agent。
"""

from typing import Optional

from orchestrator.research_agent import ResearchAgent
from orchestrator.design_agent import DesignAgent


class PresentationOrchestrator:
    """
    多智能体编排器：Research Agent -> Design Agent -> (可选) Review Agent
    """

    def __init__(
        self,
        enable_review: bool = False,
    ):
        self.research_agent = ResearchAgent()
        self.design_agent = DesignAgent()
        self.enable_review = enable_review

    async def run_outline_pipeline(
        self,
        content: str,
        n_slides: int,
        presentation_layout,  # PresentationLayoutModel
        language: Optional[str] = None,
        additional_context: Optional[str] = None,
        tone: Optional[str] = None,
        verbosity: Optional[str] = None,
        instructions: Optional[str] = None,
        include_title_slide: bool = True,
        web_search: bool = False,
        using_slides_markdown: bool = False,
    ):
        """
        执行完整管线：Research(流式大纲) -> Design(布局结构)
        返回 (outline, structure) 或流式 yield outline chunks 后返回 structure。
        """
        outline_chunks = []
        async for chunk in self.research_agent.run(
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
            outline_chunks.append(chunk)
            yield chunk

        # 解析完整 outline（此处需根据 chunk 类型聚合）
        # 简化：假设调用方会解析，这里只做设计步骤的占位
        # 实际集成时需要将 outline_chunks 转为 PresentationOutlineModel
        outline_model = None  # 由调用方从流式结果构建
        if outline_model and presentation_layout:
            structure = await self.design_agent.run(
                outline_model,
                presentation_layout,
                instructions=instructions,
                using_slides_markdown=using_slides_markdown,
            )
            yield structure
