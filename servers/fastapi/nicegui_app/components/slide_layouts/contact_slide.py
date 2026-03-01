"""contact — 联系信息版式。"""

import html as html_module


def render_contact_slide(data: dict) -> str:
    """
    生成 contact 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, contact 或 contactItems；或 bullet_points 作为联系项

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "联系我们"))
    desc = data.get("description") or ""
    desc = html_module.escape(str(desc)[:200]) if desc else ""

    contact_raw = data.get("contact") or data.get("contactItems") or []
    if not isinstance(contact_raw, list):
        contact_raw = []

    items: list = []
    for c in contact_raw[:6]:
        if isinstance(c, dict):
            items.append({
                "icon": str(c.get("icon") or "📧").strip()[:2],
                "label": str(c.get("label") or c.get("type") or "").strip()[:30],
                "value": str(c.get("value") or c.get("text") or "").strip()[:80],
            })
        else:
            items.append({"icon": "•", "label": "", "value": str(c)[:80]})

    if not items:
        bullets = data.get("bullet_points") or []
        labels = ["邮箱", "电话", "网站", "地址"]
        for i, b in enumerate(bullets[:4]):
            txt = str(b) if isinstance(b, str) else str(b.get("text", b))
            items.append({
                "icon": ["📧", "📞", "🌐", "📍"][i % 4],
                "label": labels[i] if i < len(labels) else "联系",
                "value": txt[:80],
            })
        if not items:
            items = [
                {"icon": "📧", "label": "邮箱", "value": "contact@example.com"},
                {"icon": "📞", "label": "电话", "value": "+86 000 0000 0000"},
                {"icon": "🌐", "label": "网站", "value": "www.example.com"},
            ]

    cards_html = ""
    for it in items:
        lbl = html_module.escape(it["label"])
        val = html_module.escape(it["value"])
        icon = html_module.escape(it["icon"])
        cards_html += f'''
<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
  <span class="text-2xl">{icon}</span>
  <p class="mt-2 text-sm font-semibold text-gray-800">{lbl}</p>
  <p class="text-gray-600">{val}</p>
</div>'''

    desc_block = f'<p class="text-gray-600 mb-6">{desc}</p>' if desc else ""

    return f'''
<div class="flex flex-col min-h-full h-full w-full bg-gray-50 p-8">
  <h2 class="text-2xl md:text-3xl font-bold text-gray-800 mb-2">{title}</h2>
  {desc_block}
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 flex-1 place-content-start">
    {cards_html}
  </div>
</div>
'''
