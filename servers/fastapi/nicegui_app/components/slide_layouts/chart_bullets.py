"""chart_bullets — 左图/表右要点版式（图表占位）。"""

import html as html_module


def render_chart_bullets(data: dict) -> str:
    """
    生成 chart_bullets 版式的 HTML 字符串。
    左侧为图表占位或图片，右侧为要点列表。

    Args:
        data: SlidePreviewData，含 title, bullet_points, image_url；可选 description

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "数据与要点"))
    bullets = data.get("bullet_points") or []
    if not isinstance(bullets, list):
        bullets = []
    description = data.get("description") or ""
    description = html_module.escape(str(description)[:200]) if description else ""
    image_url = data.get("image_url")

    left_content: str
    if image_url and (image_url.startswith("http") or image_url.startswith("/")):
        left_content = f'<img src="{html_module.escape(image_url)}" alt="" class="w-full h-full object-contain" />'
    else:
        # 图表占位
        left_content = '''
<div class="flex flex-col items-center justify-center h-full bg-gray-100 rounded-lg border-2 border-dashed border-gray-300">
  <svg class="w-20 h-20 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
  </svg>
  <span class="text-sm text-gray-500">图表区域</span>
</div>'''

    bullets_html = ""
    for bp in bullets[:8]:
        text = html_module.escape(str(bp))
        bullets_html += f'<li class="text-sm text-gray-700">{text}</li>\n'

    desc_block = f'<p class="text-sm text-gray-600 mb-4">{description}</p>' if description else ""

    return f'''
<div class="grid grid-cols-1 md:grid-cols-[3fr_2fr] gap-6 p-6 min-h-full h-full w-full bg-white">
  <div class="flex flex-col gap-4">
    <h2 class="text-xl md:text-2xl font-bold text-gray-800">{title}</h2>
    {desc_block}
    <div class="flex-1 min-h-[200px]">
      {left_content}
    </div>
  </div>
  <div class="flex flex-col gap-4 justify-center">
    <h3 class="text-base font-semibold text-gray-800">要点</h3>
    <ul class="list-disc list-inside space-y-1 text-gray-600">
      {bullets_html}
    </ul>
  </div>
</div>
'''
