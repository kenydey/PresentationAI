import asyncio
from dotenv import load_dotenv

from tests.test_image_generation import test_image_generation
from tests.test_get_icon import test_get_icon
from tests.test_research_report_generator import test_research_report_generator
from tests.test_summary_generator import test_generate_document_summary

load_dotenv()


async def run_test():
    # await test_generate_document_summary()
    # await test_research_report_generator()
    # await test_get_icon()
    await test_image_generation()


asyncio.run(run_test())
