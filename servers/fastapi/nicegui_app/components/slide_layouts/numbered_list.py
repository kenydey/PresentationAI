"""numbered_list — 有序列表版式。"""

import html as html_module


def render_numbered_list(data: dict) -> str:
    """
    生成 numbered_list 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, bullet_points 或 steps；可选 image_url

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "步骤"))
    bullets = data.get("bullet_points") or data.get("steps") or []
    if not isinstance(bullets, list):
        bullets = []
    # 支持 steps 为 dict 列表 {title, description}
    items: list = []
    for b in bullets[:6]:
        if isinstance(b, dict):
            items.append({
                "title": str(b.get("title") or b.get("heading") or "").strip()[:80],
                "desc": str(b.get("description") or b.get("desc") or "").strip()[:120],
            })
        else:
            txt = str(b)
            items.append({"title": txt[:80], "desc": ""})
    if not items:
        items = [{"title": "步骤 1", "desc": ""}]

    image_url = data.get("image_url")
    left_content = ""
    if image_url and (image_url.startswith("http") or image_url.startswith("/")):
        left_content = f'<img src="{html_module.escape(image_url)}" alt="" class="w-full h-48 object-cover rounded-lg" />'
    else:
        left_content = '''
<div class="w-full h-48 bg-gray-200 rounded-lg flex items-center justify-center">
  <span class="text-gray-400 text-sm">配图</span>
</div>'''

    list_html = ""
    for i, it in enumerate(items, 1):
        t = html_module.escape(it["title"])
        d = html_module.escape(it["desc"])
        list_html += f'''
<div class="flex gap-4 items-start">
  <span class="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold">{i}</span>
  <div>
    <p class="font-semibold text-gray-800">{t}</p>
    <p class="text-sm text-gray-600 mt-1">{d}</p>
  </div>
</div>'''

    return f'''
<div class="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-6 p-6 min-h-full h-full w-full bg-white">
  <div class="flex flex-col gap-4">
    <h2 class="text-xl md:text-2xl font-bold text-gray-800">{title}</h2>
    {left_content}
  </div>
  <div class="flex flex-col gap-4 justify-center">
    {list_html}
  </div>
</div>
'''
