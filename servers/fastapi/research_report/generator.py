from typing import Optional

from fastapi import HTTPException
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from enums.llm_provider import LLMProvider
from utils.llm_provider import get_llm_provider, get_model_for_task

search_tool = DuckDuckGoSearchRun(
    api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=50)
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Use provided prompt and search results to create an elaborate and up-to-date research report in mentioned language.

            # Steps
            1. Analyze the prompt and search results.
            2. Extract topic of the report.
            3. Generate a report in markdown format.

            # Notes
            - If language is not mentioned, use language from prompt.
            - Format of report should be like *Research Report*.
            - Ignore formatting if mentioned in prompt.
            """,
        ),
        (
            "human",
            """
            - Prompt: {prompt}
            - Language: {language}
            - Search Results: {search_results}
            """,
        ),
    ]
)


def _get_chat_model():
    """根据研究报告任务配置选择用于研究报告的模型。"""
    provider = get_llm_provider()
    model_name = get_model_for_task("research")

    if provider == LLMProvider.OPENAI:
        return ChatOpenAI(model=model_name)
    if provider == LLMProvider.GOOGLE:
        return ChatGoogleGenerativeAI(model=model_name)

    raise HTTPException(
        status_code=400,
        detail="当前选择的 LLM 提供商暂不支持研究报告生成功能，请在设置中切换为 OpenAI 或 Google。",
    )


async def get_report(query: str, language: Optional[str]):
    model = _get_chat_model()
    chain = prompt_template | model

    search_results = await search_tool.ainvoke(query)
    response = await chain.ainvoke(
        {
            "prompt": query,
            "language": language,
            "search_results": search_results,
        }
    )
    return response.content
