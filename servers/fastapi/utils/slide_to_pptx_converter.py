"""Convert presentation slides (JSON content) to PptxPresentationModel.

Replaces the Next.js /api/presentation_to_pptx_model endpoint which used Puppeteer
to extract element attributes from rendered React components.

This pure-Python implementation builds the PPTX model directly from the slide
content JSON data stored in the database.
"""

from typing import List, Optional
from models.pptx_models import (
    PptxPresentationModel,
    PptxSlideModel,
    PptxTextBoxModel,
    PptxPictureBoxModel,
    PptxAutoShapeBoxModel,
    PptxPositionModel,
    PptxParagraphModel,
    PptxTextRunModel,
    PptxFontModel,
    PptxFillModel,
    PptxPictureModel,
)

SLIDE_W = 1280
SLIDE_H = 720


def _build_text_box(
    x: int, y: int, w: int, h: int,
    text: str, font_size: int = 18, color: str = "333333",
    bold: bool = False, alignment=None
) -> PptxTextBoxModel:
    return PptxTextBoxModel(
        position=PptxPositionModel(x=x, y=y, width=w, height=h),
        paragraphs=[
            PptxParagraphModel(
                text_runs=[PptxTextRunModel(
                    text=text,
                    font=PptxFontModel(size=font_size, color=color, bold=bold),
                )],
                alignment=alignment,
            )
        ],
    )


def _build_image_box(
    x: int, y: int, w: int, h: int, image_url: str
) -> PptxPictureBoxModel:
    return PptxPictureBoxModel(
        position=PptxPositionModel(x=x, y=y, width=w, height=h),
        picture=PptxPictureModel(path=image_url),
    )


def _convert_content_to_shapes(content: dict, index: int) -> list:
    """Convert slide content JSON to a list of PPTX shapes."""
    shapes = []

    title = content.get("title") or content.get("heading") or content.get("headline") or ""
    if title:
        shapes.append(_build_text_box(60, 40, SLIDE_W - 120, 80, str(title), font_size=36, bold=True, color="222222"))

    subtitle = content.get("subtitle") or content.get("subheading") or ""
    if subtitle:
        shapes.append(_build_text_box(60, 130, SLIDE_W - 120, 50, str(subtitle), font_size=20, color="666666"))

    description = content.get("description") or content.get("text") or content.get("content") or ""
    if description:
        y_pos = 200 if title else 60
        shapes.append(_build_text_box(60, y_pos, SLIDE_W - 120, 200, str(description), font_size=16, color="444444"))

    bullets = content.get("bullets") or content.get("items") or content.get("points") or content.get("bulletPoints") or []
    if isinstance(bullets, list):
        y_start = 420 if description else 200
        for i, bullet in enumerate(bullets):
            text = bullet if isinstance(bullet, str) else bullet.get("text", "") or bullet.get("title", "") or str(bullet)
            if text:
                shapes.append(_build_text_box(80, y_start + i * 40, SLIDE_W - 160, 36, f"• {text}", font_size=14, color="555555"))

    metrics = content.get("metrics") or content.get("stats") or content.get("numbers") or []
    if isinstance(metrics, list):
        metric_w = min(250, (SLIDE_W - 120) // max(len(metrics), 1))
        for i, metric in enumerate(metrics):
            if isinstance(metric, dict):
                value = str(metric.get("value", "") or metric.get("number", ""))
                label = str(metric.get("label", "") or metric.get("title", ""))
                x_pos = 60 + i * (metric_w + 20)
                if value:
                    shapes.append(_build_text_box(x_pos, 300, metric_w, 50, value, font_size=32, bold=True, color="6C63FF"))
                if label:
                    shapes.append(_build_text_box(x_pos, 355, metric_w, 30, label, font_size=12, color="888888"))

    image = content.get("image") or content.get("backgroundImage") or {}
    if isinstance(image, dict):
        img_url = image.get("__image_url__") or image.get("url") or image.get("path") or ""
        if img_url:
            shapes.append(_build_image_box(SLIDE_W - 460, 200, 400, 300, img_url))
    elif isinstance(image, str) and image:
        shapes.append(_build_image_box(SLIDE_W - 460, 200, 400, 300, image))

    quote = content.get("quote") or ""
    if quote:
        shapes.append(_build_text_box(100, 250, SLIDE_W - 200, 150, f'"{quote}"', font_size=24, color="6C63FF"))

    speaker_note = content.get("presenterName") or content.get("author") or ""
    if speaker_note:
        shapes.append(_build_text_box(100, 600, 400, 30, f"— {speaker_note}", font_size=14, color="999999"))

    if not shapes:
        shapes.append(_build_text_box(60, 300, SLIDE_W - 120, 60, f"Slide {index + 1}", font_size=24, color="AAAAAA"))

    return shapes


def convert_presentation_to_pptx_model(
    slides: list,
    title: Optional[str] = None,
) -> PptxPresentationModel:
    """Convert a list of SlideModel dicts to PptxPresentationModel."""
    pptx_slides = []
    for idx, slide in enumerate(slides):
        content = slide.get("content", {}) if isinstance(slide, dict) else {}
        if not isinstance(content, dict):
            content = {}

        shapes = _convert_content_to_shapes(content, idx)
        pptx_slides.append(PptxSlideModel(
            background=PptxFillModel(color="FFFFFF"),
            shapes=shapes,
            note=slide.get("speaker_note") if isinstance(slide, dict) else None,
        ))

    return PptxPresentationModel(
        name=title,
        slides=pptx_slides,
    )
