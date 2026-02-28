from research_report.generator import get_report


async def test_research_report_generator():
    query = "global warming"
    language = "English"
    report = await get_report(query, language)
    print(report)
