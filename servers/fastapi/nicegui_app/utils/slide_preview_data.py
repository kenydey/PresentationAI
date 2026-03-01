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

    # metrics（指标卡片）
    metrics = content.get("metrics") or []
    if isinstance(metrics, list):
        metrics = [_normalize_metric(m) for m in metrics[:9] if m]
    else:
        metrics = []

    # quote / author（引用）
    quote = content.get("quote") or ""
    quote = str(quote).strip() if quote else None
    author = content.get("author") or ""
    author = str(author).strip() if author else None
    heading = content.get("heading") or ""

    # members / teamMembers（团队成员）
    members = content.get("teamMembers") or content.get("members") or []
    if isinstance(members, list):
        members = [_normalize_member(m) for m in members[:6] if m]
    else:
        members = []

    # contact（联系信息）
    contact = content.get("contact") or content.get("contactItems") or []
    if isinstance(contact, list):
        contact = [_normalize_contact_item(c) for c in contact[:6] if c]
    else:
        contact = []

    # table（表格）
    table_data = content.get("table") or {}
    if isinstance(table_data, dict):
        headers = table_data.get("headers") or table_data.get("columns") or []
        rows = table_data.get("rows") or table_data.get("data") or []
    else:
        headers, rows = [], []

    # events / timeline（时间线）
    events = content.get("events") or content.get("timeline") or []
    if isinstance(events, list):
        events = [_normalize_event(e) for e in events[:7] if e]
    else:
        events = []

    # description（通用描述）
    description = content.get("description") or content.get("companyDescription") or ""
    description = str(description).strip() if description else None

    return {
        "title": title or "无标题",
        "subtitle": subtitle,
        "bullet_points": bullet_points,
        "image_prompt": image_prompt,
        "image_url": image_url,
        "layout_id": layout_id,
        "metrics": metrics,
        "quote": quote,
        "author": author,
        "heading": heading,
        "members": members,
        "contact": contact,
        "table": {"headers": headers, "rows": rows} if headers or rows else None,
        "events": events,
        "description": description,
    }


def _normalize_metric(m: Any) -> dict:
    if isinstance(m, dict):
        return {
            "label": str(m.get("label") or m.get("name") or "").strip()[:50],
            "value": str(m.get("value") or "").strip()[:20],
            "description": str(m.get("description") or m.get("desc") or "").strip()[:150],
        }
    return {"label": "", "value": str(m)[:20], "description": ""}


def _normalize_member(m: Any) -> dict:
    if isinstance(m, dict):
        img = m.get("image") or m.get("photo") or {}
        url = ""
        if isinstance(img, dict):
            url = img.get("__image_url__") or img.get("url") or ""
        elif isinstance(img, str):
            url = img
        return {
            "name": str(m.get("name") or "").strip()[:30],
            "position": str(m.get("position") or m.get("designation") or "").strip()[:40],
            "image_url": url,
            "summary": str(m.get("summary") or m.get("description") or "").strip()[:100],
        }
    return {"name": str(m)[:30], "position": "", "image_url": "", "summary": ""}


def _normalize_contact_item(c: Any) -> dict:
    if isinstance(c, dict):
        return {
            "icon": str(c.get("icon") or "📧").strip()[:2],
            "label": str(c.get("label") or c.get("type") or "").strip()[:30],
            "value": str(c.get("value") or c.get("text") or "").strip()[:80],
        }
    return {"icon": "•", "label": "", "value": str(c)[:80]}


def _normalize_event(e: Any) -> dict:
    if isinstance(e, dict):
        return {
            "date": str(e.get("date") or e.get("year") or "").strip()[:20],
            "title": str(e.get("title") or e.get("heading") or "").strip()[:80],
            "desc": str(e.get("description") or e.get("desc") or "").strip()[:120],
        }
    return {"date": "", "title": str(e)[:80], "desc": ""}


def slide_state_to_preview_data(
    slide: Dict[str, Any],
    image_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    将 SlideState（或 PresentationState.slides 中的项）转为 SlidePreviewData。
    用于 Vibe 编辑后的预览渲染。

    Args:
        slide: SlideState 或同结构字典，含 title, bullet_points, image_prompt, layout_id 等
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

    metrics = slide.get("metrics") or []
    metrics = [_normalize_metric(m) for m in (metrics if isinstance(metrics, list) else [])[:9] if m]

    quote = (slide.get("quote") or "").strip() or None
    author = (slide.get("author") or "").strip() or None
    heading = (slide.get("heading") or "").strip() or ""

    members = slide.get("members") or slide.get("teamMembers") or []
    members = [_normalize_member(m) for m in (members if isinstance(members, list) else [])[:6] if m]

    contact = slide.get("contact") or slide.get("contactItems") or []
    contact = [_normalize_contact_item(c) for c in (contact if isinstance(contact, list) else [])[:6] if c]

    table_data = slide.get("table") or {}
    headers = (table_data.get("headers") or table_data.get("columns") or []) if isinstance(table_data, dict) else []
    rows = (table_data.get("rows") or table_data.get("data") or []) if isinstance(table_data, dict) else []

    events_raw = slide.get("events") or slide.get("timeline") or []
    events = [_normalize_event(e) for e in (events_raw if isinstance(events_raw, list) else [])[:7] if e]

    description = (slide.get("description") or "").strip() or None

    return {
        "title": title or "无标题",
        "subtitle": subtitle,
        "bullet_points": bullet_points,
        "image_prompt": image_prompt,
        "image_url": image_url,
        "layout_id": layout_id,
        "metrics": metrics,
        "quote": quote,
        "author": author,
        "heading": heading,
        "members": members,
        "contact": contact,
        "table": {"headers": headers, "rows": rows} if headers or rows else None,
        "events": events,
        "description": description,
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
