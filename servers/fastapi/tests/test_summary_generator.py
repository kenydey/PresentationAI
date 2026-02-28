import asyncio
from dotenv import load_dotenv

load_dotenv()

from document_processor.loader import DocumentsLoader
from ppt_config_generator.document_summary_generator import generate_document_summary
from api.services.instances import temp_file_service


async def test_generate_document_summary():
    documents_loader = DocumentsLoader(
        [
            "tests/assets/the_sun.pdf",
        ]
    )
    temp_dir = temp_file_service.create_temp_dir()
    await documents_loader.load_documents(temp_dir)

    summary = await generate_document_summary(documents_loader.documents)
    print(summary)
    assert summary is not None
