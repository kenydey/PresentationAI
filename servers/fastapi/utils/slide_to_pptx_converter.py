"""Convert presentation slides (JSON content) to PptxPresentationModel.

Handles all field types the LLM may generate:
- text fields: title, heading, description, subtitle, quote, presenterName, etc.
- list fields: bullets, items, points, metrics, stats, sections, team, members
- image fields: image, backgroundImage (with __image_url__)
- icon fields: icon (with __icon_url__ or __icon_query__)
- chart/table fields: chart, chartData, table, tableData, rows, columns
- speaker note: __speaker_note__

Layout strategy: auto-position elements based on type detection.
"""

from typing import List, Optional
from pptx.enum.text import PP_ALIGN
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
    PptxSpacingModel,
)

W = 1280
H = 720
PAD = 60
ACCENT = "6C63FF"

# ── Field classification ──
_TITLE_KEYS = {"title", "heading", "headline", "slideTitle"}
_SUBTITLE_KEYS = {"subtitle", "subheading", "presenterName", "author", "presentationDate", "date"}
_DESC_KEYS = {"description", "text", "content", "body", "paragraph", "summary"}
_QUOTE_KEYS = {"quote", "testimonial", "quoteText"}
_BULLET_KEYS = {"bullets", "items", "points", "bulletPoints", "features", "steps", "benefits", "challenges", "outcomes", "list"}
_METRIC_KEYS = {"metrics", "stats", "numbers", "kpis", "figures", "counters"}
_IMAGE_KEYS = {"image", "backgroundImage", "photo", "illustration", "coverImage"}
_IMAGES_KEYS = {"images", "photos", "illustrations", "gallery"}
_ICON_KEYS = {"icon", "separatorIcon"}
_TABLE_KEYS = {"table", "tableData", "rows", "tableRows"}
_CHART_KEYS = {"chart", "chartData", "graphData"}
_SECTION_KEYS = {"sections", "tableOfContents", "toc", "agenda", "topics"}
_TEAM_KEYS = {"team", "members", "teamMembers", "people"}
_SKIP_KEYS = {"__speaker_note__", "speakerNote", "speaker_note"}


def _txt(x, y, w, h, text, size=18, color="333333", bold=False, align=None):
    return PptxTextBoxModel(
        position=PptxPositionModel(x=x, y=y, width=w, height=h),
        paragraphs=[PptxParagraphModel(
            text_runs=[PptxTextRunModel(text=str(text), font=PptxFontModel(size=size, color=color, bold=bold))],
            alignment=align,
        )],
    )


def _multi_para(x, y, w, h, lines, size=14, color="555555", bullet_prefix="• "):
    paras = []
    for line in lines:
        text = str(line) if isinstance(line, str) else str(line.get("text", "") or line.get("title", "") or line.get("name", "") or line)
        desc = ""
        if isinstance(line, dict):
            desc = str(line.get("description", "") or line.get("subtitle", "") or line.get("detail", "") or "")
        runs = [PptxTextRunModel(text=f"{bullet_prefix}{text}", font=PptxFontModel(size=size, color=color))]
        if desc:
            runs.append(PptxTextRunModel(text=f"  {desc}", font=PptxFontModel(size=max(size - 2, 10), color="888888")))
        paras.append(PptxParagraphModel(text_runs=runs, spacing=PptxSpacingModel(after=4)))
    return PptxTextBoxModel(
        position=PptxPositionModel(x=x, y=y, width=w, height=h),
        paragraphs=paras,
    )


def _img(x, y, w, h, url, remove_background: bool = False):
    is_net = url.startswith("http://") or url.startswith("https://")
    return PptxPictureBoxModel(
        position=PptxPositionModel(x=x, y=y, width=w, height=h),
        picture=PptxPictureModel(path=url, is_network=is_net, remove_background=remove_background),
    )


def _extract_image_url(val) -> str:
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        return val.get("__image_url__") or val.get("url") or val.get("path") or val.get("src") or ""
    return ""


def _convert(content: dict, idx: int) -> list:
    shapes = []
    has_title = False
    has_image = False
    y_cursor = 50
    right_col_x = W // 2 + 20
    content_w = W - PAD * 2

    for key, val in content.items():
        if key in _SKIP_KEYS or val is None:
            continue
        low = key.lower() if isinstance(key, str) else key

        # ── Title ──
        if low in _TITLE_KEYS or key in _TITLE_KEYS:
            shapes.append(_txt(PAD, y_cursor, content_w, 70, val, size=34, bold=True, color="222222"))
            y_cursor += 80
            has_title = True
            continue

        # ── Subtitle / meta ──
        if low in _SUBTITLE_KEYS or key in _SUBTITLE_KEYS:
            shapes.append(_txt(PAD, y_cursor, content_w, 40, val, size=18, color="777777"))
            y_cursor += 48
            continue

        # ── Quote ──
        if low in _QUOTE_KEYS or key in _QUOTE_KEYS:
            shapes.append(_txt(PAD + 40, y_cursor, content_w - 80, 120,
                               f'"{val}"', size=22, color=ACCENT))
            y_cursor += 130
            continue

        # ── Description ──
        if low in _DESC_KEYS or key in _DESC_KEYS:
            text = str(val)
            est_h = max(60, min(200, len(text) // 2))
            text_w = content_w if not has_image else W // 2 - PAD
            shapes.append(_txt(PAD, y_cursor, text_w, est_h, text, size=15, color="444444"))
            y_cursor += est_h + 10
            continue

        # ── Single image ──
        if low in _IMAGE_KEYS or key in _IMAGE_KEYS:
            url = _extract_image_url(val)
            if url:
                img_w, img_h = 400, 280
                remove_bg = key in ("backgroundImage",) or low == "backgroundimage"
                shapes.append(_img(W - img_w - PAD, 160, img_w, img_h, url, remove_background=remove_bg))
                has_image = True
            continue

        # ── Multiple images ──
        if low in _IMAGES_KEYS or key in _IMAGES_KEYS:
            if isinstance(val, list):
                per_w = min(350, (content_w - 20 * len(val)) // max(len(val), 1))
                for i, img in enumerate(val[:4]):
                    url = _extract_image_url(img)
                    if url:
                        shapes.append(_img(PAD + i * (per_w + 20), y_cursor, per_w, 200, url, remove_background=True))
                y_cursor += 220
            continue

        # ── Icon ──
        if low in _ICON_KEYS or key in _ICON_KEYS:
            continue  # icons need SVG rendering, skip for PPTX

        # ── Bullets / items ──
        if low in _BULLET_KEYS or key in _BULLET_KEYS:
            if isinstance(val, list) and val:
                est_h = min(350, len(val) * 36 + 10)
                text_w = content_w if not has_image else W // 2 - PAD
                shapes.append(_multi_para(PAD, y_cursor, text_w, est_h, val, size=14, color="444444"))
                y_cursor += est_h + 10
            continue

        # ── Metrics ──
        if low in _METRIC_KEYS or key in _METRIC_KEYS:
            if isinstance(val, list) and val:
                per_w = min(250, (content_w - 20) // max(len(val), 1))
                for i, m in enumerate(val[:6]):
                    if isinstance(m, dict):
                        v = str(m.get("value", "") or m.get("number", "") or m.get("metric", ""))
                        lb = str(m.get("label", "") or m.get("title", "") or m.get("name", ""))
                        x = PAD + i * (per_w + 15)
                        if v:
                            shapes.append(_txt(x, y_cursor, per_w, 45, v, size=30, bold=True, color=ACCENT))
                        if lb:
                            shapes.append(_txt(x, y_cursor + 48, per_w, 28, lb, size=11, color="888888"))
                y_cursor += 90
            continue

        # ── Sections / TOC ──
        if low in _SECTION_KEYS or key in _SECTION_KEYS:
            if isinstance(val, list) and val:
                est_h = min(400, len(val) * 32 + 10)
                shapes.append(_multi_para(PAD, y_cursor, content_w, est_h, val, size=14, color="444444", bullet_prefix=""))
                y_cursor += est_h + 10
            continue

        # ── Team / members ──
        if low in _TEAM_KEYS or key in _TEAM_KEYS:
            if isinstance(val, list) and val:
                per_w = min(280, (content_w - 20) // max(len(val), 1))
                for i, member in enumerate(val[:5]):
                    if isinstance(member, dict):
                        name = str(member.get("name", "") or member.get("title", ""))
                        role = str(member.get("role", "") or member.get("position", "") or member.get("description", ""))
                        x = PAD + i * (per_w + 15)
                        if name:
                            shapes.append(_txt(x, y_cursor, per_w, 30, name, size=16, bold=True, color="333333"))
                        if role:
                            shapes.append(_txt(x, y_cursor + 32, per_w, 24, role, size=11, color="888888"))
                        img_url = _extract_image_url(member.get("image") or member.get("photo") or {})
                        if img_url:
                            shapes.append(_img(x + per_w // 2 - 40, y_cursor + 60, 80, 80, img_url))
                y_cursor += 160
            continue

        # ── Table ──
        if low in _TABLE_KEYS or key in _TABLE_KEYS:
            if isinstance(val, list) and val:
                shapes.append(_multi_para(PAD, y_cursor, content_w, min(300, len(val) * 28 + 10), val, size=12, color="555555", bullet_prefix=""))
                y_cursor += min(300, len(val) * 28 + 20)
            elif isinstance(val, dict):
                headers = val.get("headers", val.get("columns", []))
                rows = val.get("rows", val.get("data", []))
                lines = []
                if headers:
                    lines.append(" | ".join(str(h) for h in headers))
                for row in rows[:10]:
                    if isinstance(row, list):
                        lines.append(" | ".join(str(c) for c in row))
                    elif isinstance(row, dict):
                        lines.append(" | ".join(str(v) for v in row.values()))
                if lines:
                    shapes.append(_multi_para(PAD, y_cursor, content_w, min(300, len(lines) * 26), lines, size=12, color="555555", bullet_prefix=""))
                    y_cursor += min(300, len(lines) * 26 + 10)
            continue

        # ── Chart ──
        if low in _CHART_KEYS or key in _CHART_KEYS:
            if isinstance(val, dict):
                chart_type = val.get("type", "bar")
                chart_title = val.get("title", "Chart")
                shapes.append(_txt(PAD, y_cursor, content_w, 30, f"[{chart_type.upper()} CHART: {chart_title}]", size=14, color="AAAAAA"))
                data = val.get("data", val.get("datasets", []))
                if isinstance(data, list):
                    for d in data[:5]:
                        if isinstance(d, dict):
                            label = str(d.get("label", "") or d.get("name", ""))
                            value = str(d.get("value", "") or d.get("y", ""))
                            if label or value:
                                shapes.append(_txt(PAD + 20, y_cursor + 35, content_w - 40, 22, f"{label}: {value}", size=12, color="666666"))
                                y_cursor += 24
                y_cursor += 50
            continue

        # ── Fallback: unknown string field ──
        if isinstance(val, str) and val.strip():
            est_h = max(30, min(80, len(val) // 3))
            shapes.append(_txt(PAD, y_cursor, content_w, est_h, val, size=14, color="555555"))
            y_cursor += est_h + 8

    if not shapes:
        shapes.append(_txt(PAD, H // 2 - 30, content_w, 60, f"Slide {idx + 1}", size=24, color="CCCCCC", align=PP_ALIGN.CENTER))

    return shapes


def convert_presentation_to_pptx_model(
    slides: list,
    title: Optional[str] = None,
) -> PptxPresentationModel:
    pptx_slides = []
    for idx, slide in enumerate(slides):
        content = slide.get("content", {}) if isinstance(slide, dict) else {}
        if not isinstance(content, dict):
            content = {}
        shapes = _convert(content, idx)
        pptx_slides.append(PptxSlideModel(
            background=PptxFillModel(color="FFFFFF"),
            shapes=shapes,
            note=slide.get("speaker_note") if isinstance(slide, dict) else None,
        ))
    return PptxPresentationModel(name=title, slides=pptx_slides)
