"""timeline — 时间线版式。"""

import html as html_module


def render_timeline_slide(data: dict) -> str:
    """
    生成 timeline 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, events 或 bullet_points

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "时间线"))
    events_raw = data.get("events") or data.get("timeline") or []
    if not isinstance(events_raw, list):
        events_raw = []

    events: list = []
    for e in events_raw[:7]:
        if isinstance(e, dict):
            d = str(e.get("description") or e.get("desc") or "").strip()[:120]
            events.append({
                "date": str(e.get("date") or e.get("year") or "").strip()[:20],
                "title": str(e.get("title") or e.get("heading") or "").strip()[:80],
                "desc": d,
            })
        else:
            events.append({"date": "", "title": str(e)[:80], "desc": ""})

    if not events:
        bullets = data.get("bullet_points") or []
        for b in bullets[:6]:
            txt = str(b) if isinstance(b, str) else str(b.get("text", b))
            parts = txt.split(":", 1) or txt.split(" ", 1) or [txt]
            events.append({
                "date": parts[0].strip()[:20] if parts else "",
                "title": parts[1].strip()[:80] if len(parts) > 1 else txt[:80],
                "desc": "",
            })
        if not events:
            events = [{"date": "2024", "title": "里程碑", "desc": ""}]

    items_html = ""
    for i, ev in enumerate(events):
        date = html_module.escape(ev["date"])
        tit = html_module.escape(ev["title"])
        d = html_module.escape(ev["desc"])
        side = "md:flex-row" if i % 2 == 0 else "md:flex-row-reverse"
        items_html += f'''
<div class="flex {side} gap-4 items-start mb-6">
  <div class="flex-shrink-0 w-16 text-right md:text-left">
    <span class="inline-block px-2 py-1 rounded bg-indigo-100 text-indigo-800 text-sm font-medium">{date}</span>
  </div>
  <div class="flex-1 border-l-2 border-indigo-200 pl-4 -ml-2">
    <p class="font-semibold text-gray-800">{tit}</p>
    <p class="text-sm text-gray-600 mt-1">{d}</p>
  </div>
</div>'''

    return f'''
<div class="flex flex-col min-h-full h-full w-full bg-gray-50 p-6 overflow-auto">
  <h2 class="text-xl md:text-2xl font-bold text-gray-800 mb-6 text-center">{title}</h2>
  <div class="flex-1">
    {items_html}
  </div>
</div>
'''
