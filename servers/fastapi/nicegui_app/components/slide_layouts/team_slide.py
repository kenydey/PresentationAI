"""team — 成员卡片版式。"""

import html as html_module


def render_team_slide(data: dict) -> str:
    """
    生成 team 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, members 或 teamMembers (列表，每项含 name, position, image_url, summary/description)

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "团队成员"))
    desc = data.get("description") or data.get("companyDescription") or ""
    desc = html_module.escape(str(desc)[:200]) if desc else ""

    members_raw = data.get("members") or data.get("teamMembers") or []
    if not isinstance(members_raw, list):
        members_raw = []

    # 若 members 为空，尝试用 bullet_points 构造简单列表
    members: list = []
    for m in members_raw[:6]:
        if isinstance(m, dict):
            img = m.get("image") or m.get("photo") or {}
            url = ""
            if isinstance(img, dict):
                url = img.get("__image_url__") or img.get("url") or ""
            elif isinstance(img, str):
                url = img
            members.append({
                "name": str(m.get("name") or "").strip()[:30],
                "position": str(m.get("position") or m.get("designation") or "").strip()[:40],
                "image_url": url,
                "summary": str(m.get("summary") or m.get("description") or "").strip()[:100],
            })
        else:
            members.append({"name": str(m)[:30], "position": "", "image_url": "", "summary": ""})

    if not members:
        bullets = data.get("bullet_points") or []
        for b in bullets[:4]:
            txt = str(b) if isinstance(b, str) else str(b.get("text", b))
            parts = txt.split("—", 1) or txt.split("-", 1) or [txt]
            members.append({
                "name": parts[0].strip()[:30],
                "position": parts[1].strip()[:40] if len(parts) > 1 else "",
                "image_url": "",
                "summary": "",
            })
        if not members:
            members = [{"name": "成员", "position": "职位", "image_url": "", "summary": ""}]

    n = len(members)
    grid_cls = "grid-cols-1 md:grid-cols-2" if n <= 2 else "grid-cols-2 md:grid-cols-4"

    cards_html = ""
    for mem in members:
        name = html_module.escape(mem["name"])
        pos = html_module.escape(mem["position"])
        summary = html_module.escape(mem["summary"])
        url = mem["image_url"]
        if url and (url.startswith("http") or url.startswith("/")):
            img_html = f'<img src="{html_module.escape(url)}" alt="" class="w-full h-32 object-cover rounded-t-lg" />'
        else:
            img_html = '''
<div class="w-full h-32 bg-indigo-100 rounded-t-lg flex items-center justify-center">
  <span class="text-4xl text-indigo-400">👤</span>
</div>'''
        cards_html += f'''
<div class="rounded-lg border border-gray-200 bg-white overflow-hidden shadow-sm">
  {img_html}
  <div class="p-3">
    <p class="font-semibold text-gray-800">{name}</p>
    <p class="text-sm text-indigo-600">{pos}</p>
    <p class="mt-1 text-xs text-gray-600">{summary}</p>
  </div>
</div>'''

    desc_block = f'<p class="text-sm text-gray-600 mb-6">{desc}</p>' if desc else ""

    return f'''
<div class="flex flex-col min-h-full h-full w-full bg-gray-50 p-6">
  <h2 class="text-xl md:text-2xl font-bold text-gray-800 mb-2">{title}</h2>
  {desc_block}
  <div class="grid {grid_cls} gap-4 flex-1">
    {cards_html}
  </div>
</div>
'''
