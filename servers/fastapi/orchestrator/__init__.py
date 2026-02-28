"""
多智能体编排层：借鉴 PPTAgent 的 Research -> Design -> Review 工作流。
主控调度器将任务派发给各专业智能体，输出高度结构化的 JSON 大纲与布局。
"""

from orchestrator.orchestrator import PresentationOrchestrator
from orchestrator.research_agent import ResearchAgent
from orchestrator.design_agent import DesignAgent

__all__ = [
    "PresentationOrchestrator",
    "ResearchAgent",
    "DesignAgent",
]
