import asyncio
from api.services.instances import temp_file_service
from pdf2image import convert_from_path


def get_page_images_from_pdf(document_path: str, temp_dir: str):
    images_temp_dir = temp_file_service.create_dir_in_dir(temp_dir)
    return convert_from_path(document_path, output_folder=images_temp_dir)


async def get_page_images_from_pdf_async(document_path: str, temp_dir: str):
    return await asyncio.to_thread(get_page_images_from_pdf, document_path, temp_dir)
