"""text_image_split — 左图右文版式。"""

import html as html_module


def render_text_image_split(data: dict) -> str:
    """
    生成 text_image_split 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, bullet_points, image_url, image_prompt

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "无标题"))
    bullets = data.get("bullet_points") or []
    image_url = data.get("image_url")
    image_prompt = data.get("image_prompt") or ""

    # 左侧：图片或占位
    left_content: str
    if image_url:
        # 简单校验已由 slide_preview_data 完成
        left_content = f'<img src="{html_module.escape(image_url)}" alt="" class="w-full h-full object-cover" />'
    else:
        prompt_text = html_module.escape(image_prompt[:80]) if image_prompt else "配图占位"
        left_content = f'''
<div class="flex flex-col items-center justify-center h-full bg-gray-200 text-gray-500 text-sm text-center p-4">
  <svg class="w-16 h-16 mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14"/>
  </svg>
  <span>{prompt_text}</span>
</div>'''

    bullets_html = ""
    for bp in bullets[:8]:
        text = html_module.escape(str(bp))
        bullets_html += f'    <li class="text-sm text-gray-700">{text}</li>\n'

    html = f'''
<div class="grid grid-cols-1 md:grid-cols-[2fr_3fr] gap-6 p-6 min-h-full h-full w-full bg-white">
  <div class="aspect-video md:aspect-auto bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
    {left_content}
  </div>
  <div class="flex flex-col gap-4 justify-center">
    <h2 class="text-xl md:text-2xl font-bold text-gray-800">{title}</h2>
    <ul class="list-disc list-inside space-y-1 text-gray-600">
{bullets_html}
    </ul>
  </div>
</div>
'''
    return html
