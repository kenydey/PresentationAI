import io
import os
import subprocess
from typing import List

from image_processor.utils import get_page_images_from_pdf


def get_pdf_from_pptx(pptx_path: str, temp_dir: str) -> str:
    base_name = os.path.splitext(os.path.basename(pptx_path))[0]

    subprocess.run(
        f"{os.getenv('LIBREOFFICE')} --headless --invisible --convert-to pdf {pptx_path} --outdir {temp_dir}",
        shell=True,
        capture_output=True,
    )

    pdf_filename = f"{base_name}.pdf"
    pdf_path = os.path.join(temp_dir, pdf_filename)

    return pdf_path


def get_images_from_pptx(pptx_path: str) -> List[str]:
    temp_dir = os.path.dirname(pptx_path)
    pdf_path = get_pdf_from_pptx(pptx_path, temp_dir)

    return get_page_images_from_pdf(pdf_path, temp_dir)
