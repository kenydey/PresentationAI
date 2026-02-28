"""API slide → SlidePreviewData 映射，供预览组件使用。"""

from typing import Any, Dict, List, Optional


def slide_to_preview_data(slide: Dict[str, Any]) -> Dict[str, Any]:
    """
    将 API 返回的 slide（SlideModel 序列化）转为 SlidePreviewData。

    Args:
        slide: 包含 layout, layout_group, content 等字段的字典

    Returns:
        SlidePreviewData: {
            "title": str,
            "bullet_points": List[str],
            "image_prompt": Optional[str],
            "image_url": Optional[str],
            "layout_id": str,
        }
    """
    content = slide.get("content") or {}
    if not isinstance(content, dict):
        content = {}

    # 标题
    title = (
        content.get("title")
        or content.get("heading")
        or content.get("headline")
        or ""
    )
    if isinstance(title, str):
        title = title.strip()
    else:
        title = str(title)[:200]

    # 要点列表
    bullets_raw = (
        content.get("bullets")
        or content.get("items")
        or content.get("points")
        or content.get("bulletPoints")
        or []
    )
    if not isinstance(bullets_raw, list):
        bullets_raw = []
    bullet_points: List[str] = []
    for b in bullets_raw[:8]:
        if isinstance(b, str):
            bullet_points.append(b.strip()[:150])
        elif isinstance(b, dict):
            txt = b.get("text") or b.get("title") or ""
            bullet_points.append(str(txt).strip()[:150])
        else:
            bullet_points.append(str(b)[:150])

    # 配图描述
    image_prompt = (
        content.get("imagePrompt")
        or content.get("image_description")
        or content.get("image_prompt")
        or ""
    )
    image_prompt = str(image_prompt).strip() if image_prompt else None

    # 已生成图片 URL
    img_obj = content.get("image") or content.get("backgroundImage") or {}
    image_url = ""
    if isinstance(img_obj, dict):
        image_url = img_obj.get("__image_url__") or img_obj.get("url") or ""
    elif isinstance(img_obj, str):
        image_url = img_obj
    image_url = _safe_image_url(image_url) if image_url else None

    # 副标题（用于 title_slide）
    subtitle = (
        content.get("subtitle")
        or content.get("subheading")
        or content.get("presenterName")
        or ""
    )
    subtitle = str(subtitle).strip() if subtitle else None

    # layout_id（来自 SlideModel.layout）
    layout_id = slide.get("layout") or "basic-info-slide"
    if not isinstance(layout_id, str):
        layout_id = "basic-info-slide"

    return {
        "title": title or "无标题",
        "subtitle": subtitle,
        "bullet_points": bullet_points,
        "image_prompt": image_prompt,
        "image_url": image_url,
        "layout_id": layout_id,
    }


def slide_state_to_preview_data(
    slide: Dict[str, Any],
    image_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    将 SlideState（或 PresentationState.slides 中的项）转为 SlidePreviewData。
    用于 Vibe 编辑后的预览渲染。

    Args:
        slide: SlideState 或同结构字典，含 title, bullet_points, image_prompt, layout_id
        image_url: 可选，从原 slides 按 index 保留的图片 URL

    Returns:
        SlidePreviewData
    """
    title = str(slide.get("title") or "无标题").strip()[:200]
    bullets = slide.get("bullet_points") or slide.get("bullets") or []
    if not isinstance(bullets, list):
        bullets = []
    bullet_points = [str(b)[:150] for b in bullets[:8]]
    image_prompt = slide.get("image_prompt") or ""
    image_prompt = str(image_prompt).strip() if image_prompt else None
    layout_id = slide.get("layout_id") or slide.get("layout") or "basic-info-slide"
    if not isinstance(layout_id, str):
        layout_id = "basic-info-slide"
    subtitle = slide.get("subtitle")
    subtitle = str(subtitle).strip() if subtitle else None
    if image_url:
        image_url = _safe_image_url(image_url) if isinstance(image_url, str) else None

    return {
        "title": title or "无标题",
        "subtitle": subtitle,
        "bullet_points": bullet_points,
        "image_prompt": image_prompt,
        "image_url": image_url,
        "layout_id": layout_id,
    }


def _safe_image_url(url: str) -> Optional[str]:
    """校验图片 URL，避免 javascript: 等危险协议。"""
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    lower = url.lower()
    if lower.startswith("http://") or lower.startswith("https://"):
        return url
    if url.startswith("/"):
        return url
    return None
