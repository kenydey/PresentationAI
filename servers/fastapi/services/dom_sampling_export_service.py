"""基于 Playwright DOM 采样的高质量 PPT 导出服务。

参考原 Presenton 的 presentation_to_pptx_model 流程：
渲染 HTML → 采样 DOM 属性 → 转为 PptxPresentationModel → 生成 .pptx
"""

from __future__ import annotations

import os
import re
from typing import Any, Optional

from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout

from models.pptx_models import (
    PptxPresentationModel,
    PptxSlideModel,
    PptxTextBoxModel,
    PptxAutoShapeBoxModel,
    PptxPictureBoxModel,
    PptxPositionModel,
    PptxParagraphModel,
    PptxFontModel,
    PptxFillModel,
    PptxStrokeModel,
    PptxShadowModel,
    PptxPictureModel,
    PptxObjectFitModel,
    PptxObjectFitEnum,
)
from pptx.enum.text import PP_ALIGN


EXTRACT_ELEMENTS_JS = """
(() => {
  function colorToHex(color) {
    if (!color || color === 'transparent' || color === 'rgba(0, 0, 0, 0)') return null;
    if (color.startsWith('#')) return color.substring(1).toUpperCase();
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;
    try {
      ctx.fillStyle = color;
      const hex = ctx.fillStyle;
      return hex.startsWith('#') ? hex.substring(1).toUpperCase() : hex;
    } catch (_) { return null; }
  }

  function parsePosition(el, rootRect) {
    const rect = el.getBoundingClientRect();
    return {
      left: Math.round(rect.left - rootRect.left),
      top: Math.round(rect.top - rootRect.top),
      width: Math.round(rect.width),
      height: Math.round(rect.height)
    };
  }

  function extractElement(el, rootRect, depth) {
    const tag = (el.tagName || '').toLowerCase();
    if (['style', 'script', 'link', 'meta', 'path'].includes(tag)) return null;
    const rect = el.getBoundingClientRect();
    if (!rect.width || !rect.height) return null;
    const pos = parsePosition(el, rootRect);
    if (pos.width <= 0 || pos.height <= 0) return null;

    const style = window.getComputedStyle(el);
    const colorHex = colorToHex(style.color);
    const bgHex = colorToHex(style.backgroundColor);
    const borderColorHex = colorToHex(style.borderColor);
    const borderWidth = parseFloat(style.borderWidth) || 0;
    let fontSize = parseFloat(style.fontSize);
    if (isNaN(fontSize)) fontSize = 16;
    const fontFamily = (style.fontFamily || '').split(',')[0].trim().replace(/['"]/g, '') || 'Inter';
    const fontWeight = parseInt(style.fontWeight) || 400;
    const textAlign = style.textAlign || 'left';
    let innerText = '';
    const childNodes = el.childNodes;
    let hasOnlyTextOrInline = true;
    for (let i = 0; i < childNodes.length; i++) {
      const n = childNodes[i];
      if (n.nodeType === Node.ELEMENT_NODE) {
        const tn = (n.tagName || '').toLowerCase();
        if (!['span', 'strong', 'em', 'u', 'b', 'i', 'code', 's'].includes(tn)) hasOnlyTextOrInline = false;
      }
    }
    if (hasOnlyTextOrInline && el.textContent) {
      innerText = (el.textContent || '').trim();
    }
    let imageSrc = el.src || undefined;
    if (!imageSrc && style.backgroundImage && style.backgroundImage !== 'none') {
      const m = style.backgroundImage.match(/url\\(['"]?([^'")]+)['"]?\\)/);
      if (m) imageSrc = m[1];
    }
    const borderParts = (style.borderRadius || '0').split(' ').map(p => parseFloat(p) || 0);
    const borderRadius = borderParts.length ? borderParts : undefined;
    const zIndex = parseInt(style.zIndex) || 0;
    const opacity = parseFloat(style.opacity);
    const objFit = style.objectFit || 'contain';

    return {
      tagName: tag,
      position: pos,
      innerText: innerText || undefined,
      font: (innerText || colorHex) ? { name: fontFamily, size: fontSize, weight: fontWeight, color: colorHex || '000000', italic: style.fontStyle === 'italic' } : undefined,
      background: bgHex ? { color: bgHex, opacity: 1 } : undefined,
      border: borderWidth > 0 && borderColorHex ? { color: borderColorHex, width: borderWidth } : undefined,
      imageSrc,
      textAlign: textAlign !== 'left' ? textAlign : undefined,
      borderRadius,
      zIndex: isNaN(zIndex) ? 0 : zIndex,
      opacity: isNaN(opacity) ? undefined : opacity,
      objectFit: objFit,
      textWrap: style.whiteSpace !== 'nowrap'
    };
  }

  function collectSlideElements(container, rootRect, results, maxDepth) {
    if (maxDepth <= 0) return;
    const children = container.children || [];
    for (let i = 0; i < children.length; i++) {
      const child = children[i];
      const tag = (child.tagName || '').toLowerCase();
      if (['style', 'script', 'link', 'meta'].includes(tag)) continue;
      const el = extractElement(child, rootRect, 0);
      if (el) {
        const hasText = el.innerText && el.innerText.trim().length > 0;
        const hasImage = el.imageSrc;
        const hasBg = el.background && el.background.color;
        const hasBorder = el.border && el.border.color;
        const isSvg = el.tagName === 'svg';
        const isCanvas = el.tagName === 'canvas';
        const isTable = el.tagName === 'table';
        const occupiesRoot = el.position.left === 0 && el.position.top === 0 &&
          el.position.width >= rootRect.width - 2 && el.position.height >= rootRect.height - 2;
        if ((hasText || hasImage || hasBg || hasBorder || isSvg || isCanvas || isTable) && !(occupiesRoot && !hasText && !hasImage)) {
          results.push(el);
        }
        if (!isSvg && !isCanvas && !isTable && (el.tagName !== 'img')) {
          collectSlideElements(child, rootRect, results, maxDepth - 1);
        }
      }
    }
  }

  const wrapper = document.getElementById('presentation-slides-wrapper');
  if (!wrapper) return { slides: [], error: 'presentation-slides-wrapper not found' };
  const slideContainers = wrapper.querySelectorAll('.slide-container');
  const slides = [];
  for (let i = 0; i < slideContainers.length; i++) {
    const sc = slideContainers[i];
    const rootRect = sc.getBoundingClientRect();
    const speakerNote = sc.getAttribute('data-speaker-note') || '';
    const elements = [];
    collectSlideElements(sc, rootRect, elements, 8);
    elements.sort((a, b) => (b.zIndex || 0) - (a.zIndex || 0));
    slides.push({ speakerNote, elements, rootRect: { width: rootRect.width, height: rootRect.height } });
  }
  return { slides };
})();
"""


def _color_to_hex(value: Any) -> str:
    """确保颜色为 6 位 hex，无 # 前缀。"""
    if value is None or value == "":
        return "000000"
    s = str(value).strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) == 6 and re.match(r"^[0-9A-Fa-f]+$", s):
        return s.upper()
    return "000000"


def _element_to_pptx_shape(el: dict) -> Optional[Any]:
    """将提取的 DOM 元素转为 Pptx 形状。"""
    pos = el.get("position") or {}
    left = int(pos.get("left", 0) or 0)
    top = int(pos.get("top", 0) or 0)
    width = max(1, int(pos.get("width", 0) or 1))
    height = max(1, int(pos.get("height", 0) or 1))
    position = PptxPositionModel(left=left, top=top, width=width, height=height)

    tag = (el.get("tagName") or "").lower()
    inner_text = (el.get("innerText") or "").strip()
    image_src = el.get("imageSrc")

    # 图片：仅当有有效 imageSrc 时创建
    if tag == "img" or (image_src and str(image_src).strip()):
        pic_path = (image_src or "").strip()
        is_network = bool(pic_path and (pic_path.startswith("http://") or pic_path.startswith("https://") or pic_path.startswith("//")))
        obj_fit = (el.get("objectFit") or "cover").lower()
        fit_enum = PptxObjectFitEnum.COVER if obj_fit == "cover" else PptxObjectFitEnum.CONTAIN
        return PptxPictureBoxModel(
            shape_type="picture",
            position=position,
            picture=PptxPictureModel(is_network=is_network, path=pic_path),
            object_fit=PptxObjectFitModel(fit=fit_enum),
            border_radius=el.get("borderRadius"),
        )

    # 文本
    if inner_text:
        font_el = el.get("font") or {}
        font = PptxFontModel(
            name=str(font_el.get("name") or "Inter")[:100],
            size=int(font_el.get("size") or 16),
            font_weight=int(font_el.get("weight") or 400),
            color=_color_to_hex(font_el.get("color")),
            italic=bool(font_el.get("italic")),
        )
        align_map = {"center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT, "justify": PP_ALIGN.JUSTIFY}
        alignment = align_map.get((el.get("textAlign") or "left").lower(), PP_ALIGN.LEFT)
        para = PptxParagraphModel(text=inner_text, font=font, alignment=alignment)
        fill = None
        bg = el.get("background")
        if bg and bg.get("color"):
            fill = PptxFillModel(color=_color_to_hex(bg.get("color")), opacity=float(bg.get("opacity", 1) or 1))
        if bg and bg.get("color") and el.get("borderRadius") and any((el.get("borderRadius") or [0])):
            stroke = None
            b = el.get("border")
            if b and b.get("color"):
                stroke = PptxStrokeModel(color=_color_to_hex(b.get("color")), thickness=float(b.get("width", 1) or 1), opacity=1.0)
            shadow = None
            sh = el.get("shadow")
            if sh and sh.get("color"):
                shadow = PptxShadowModel(radius=int(sh.get("radius", 4)), color=_color_to_hex(sh.get("color")), opacity=float(sh.get("opacity", 0.5)))
            radius = 0
            for r in (el.get("borderRadius") or []):
                if r and r > 0:
                    radius = max(radius, int(r))
            return PptxAutoShapeBoxModel(
                shape_type="autoshape",
                position=position,
                fill=fill,
                stroke=stroke,
                shadow=shadow,
                border_radius=radius if radius > 0 else None,
                text_wrap=el.get("textWrap", True),
                paragraphs=[para],
            )
        return PptxTextBoxModel(
            shape_type="textbox",
            position=position,
            fill=fill,
            text_wrap=el.get("textWrap", True),
            paragraphs=[para],
        )

    return None


def _slide_attrs_to_pptx_slide(slide_data: dict, bg_color: Optional[str] = None) -> PptxSlideModel:
    """将单页采样数据转为 PptxSlideModel。"""
    elements = slide_data.get("elements") or []
    shapes = []
    for el in elements:
        shape = _element_to_pptx_shape(el)
        if shape:
            shapes.append(shape)
    background = None
    if bg_color:
        background = PptxFillModel(color=_color_to_hex(bg_color), opacity=1.0)
    return PptxSlideModel(
        shapes=shapes,
        background=background,
        note=(slide_data.get("speakerNote") or "").strip() or None,
    )


async def export_via_dom_sampling(
    presentation_id: str,
    title: str,
    base_url: Optional[str] = None,
    timeout_ms: int = 60000,
) -> PptxPresentationModel:
    """
    通过 Playwright 访问导出预览页，采样 DOM 后转为 PptxPresentationModel。

    Args:
        presentation_id: 演示 ID
        title: 演示标题
        base_url: 预览页基础 URL，默认从 EXPORT_PREVIEW_BASE_URL 或 http://127.0.0.1:8000
        timeout_ms: 页面加载超时毫秒数

    Returns:
        PptxPresentationModel 用于生成 .pptx

    Raises:
        RuntimeError: 预览页加载失败或采样失败
    """
    url_base = base_url or os.environ.get("EXPORT_PREVIEW_BASE_URL", "http://127.0.0.1:8000")
    url = f"{url_base.rstrip('/')}/ui/export-view?id={presentation_id}"

    browser: Optional[Browser] = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
            page: Page = await browser.new_page()
            await page.set_viewport_size({"width": 1280, "height": 720})
            await page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            await page.wait_for_selector("#presentation-slides-wrapper[data-export-ready]", timeout=timeout_ms)
            result = await page.evaluate(EXTRACT_ELEMENTS_JS)
    except PlaywrightTimeout as e:
        raise RuntimeError(f"导出预览页加载超时: {e}")
    except Exception as e:
        raise RuntimeError(f"Playwright 采样失败: {e}")
    finally:
        if browser:
            await browser.close()

    if not result or not isinstance(result, dict):
        raise RuntimeError("DOM 采样返回格式异常")
    if result.get("error"):
        raise RuntimeError(f"DOM 采样错误: {result.get('error')}")

    slides_data = result.get("slides") or []
    pptx_slides = []
    for sd in slides_data:
        pptx_slides.append(_slide_attrs_to_pptx_slide(sd))

    return PptxPresentationModel(name=title or "演示文稿", slides=pptx_slides)
