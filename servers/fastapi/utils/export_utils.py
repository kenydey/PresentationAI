"""Export presentation to PPTX or PDF — no Next.js dependency.

PPTX: converts slide content JSON → PptxPresentationModel → .pptx file
      或 use_dom_sampling=True 时：Playwright 采样预览页 DOM → PptxPresentationModel（高质量）
PDF:  converts PPTX → PDF via LibreOffice headless
"""

import os
import subprocess
import uuid
from typing import Literal

from fastapi import HTTPException
from pathvalidate import sanitize_filename
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.pptx_models import PptxPresentationModel
from models.presentation_and_path import PresentationAndPath
from models.sql.presentation import PresentationModel
from models.sql.slide import SlideModel
from services.pptx_presentation_creator import PptxPresentationCreator
from services.temp_file_service import TEMP_FILE_SERVICE
from utils.asset_directory_utils import get_exports_directory
from utils.slide_to_pptx_converter import convert_presentation_to_pptx_model


async def export_presentation(
    presentation_id: uuid.UUID,
    title: str,
    export_as: Literal["pptx", "pdf"],
    sql_session: AsyncSession | None = None,
    slides: list | None = None,
    use_dom_sampling: bool = False,
    export_preview_base_url: str | None = None,
) -> PresentationAndPath:
    """Export a presentation as PPTX or PDF.

    If *slides* is not provided, fetch from DB via *sql_session*.

    When use_dom_sampling=True and export_as=pptx: uses Playwright to sample the
    export preview page DOM for higher visual fidelity (what-you-see-is-what-you-get).
    """
    pptx_model: PptxPresentationModel
    if use_dom_sampling and export_as == "pptx":
        try:
            from services.dom_sampling_export_service import export_via_dom_sampling

            pptx_model = await export_via_dom_sampling(
                str(presentation_id),
                title or str(presentation_id),
                base_url=export_preview_base_url,
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"高质量导出失败 (DOM 采样): {e!s}",
            )
    else:
        if slides is None and sql_session is not None:
            result = await sql_session.scalars(
                select(SlideModel)
                .where(SlideModel.presentation == presentation_id)
                .order_by(SlideModel.index)
            )
            slides = [s.model_dump(mode="json") for s in result.all()]

        if not slides:
            slides = []

        pptx_model = convert_presentation_to_pptx_model(slides, title=title)

    temp_dir = TEMP_FILE_SERVICE.create_temp_dir()
    pptx_creator = PptxPresentationCreator(pptx_model, temp_dir)
    await pptx_creator.create_ppt()

    export_directory = get_exports_directory()
    safe_name = sanitize_filename(title or str(uuid.uuid4()))

    if export_as == "pptx":
        pptx_path = os.path.join(export_directory, f"{safe_name}.pptx")
        pptx_creator.save(pptx_path)
        return PresentationAndPath(presentation_id=presentation_id, path=pptx_path)

    # PDF: save temp PPTX then convert via LibreOffice
    tmp_pptx = os.path.join(temp_dir, f"{safe_name}.pptx")
    pptx_creator.save(tmp_pptx)

    try:
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", export_directory, tmp_pptx],
            check=True, capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="LibreOffice not installed — cannot convert to PDF")
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"PDF conversion failed: {e.stderr}")
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="PDF conversion timed out")

    pdf_path = os.path.join(export_directory, f"{safe_name}.pdf")
    if not os.path.exists(pdf_path):
        pdf_files = [f for f in os.listdir(export_directory) if f.endswith(".pdf")]
        if pdf_files:
            pdf_path = os.path.join(export_directory, pdf_files[-1])
        else:
            raise HTTPException(status_code=500, detail="PDF file not generated")

    return PresentationAndPath(presentation_id=presentation_id, path=pdf_path)
