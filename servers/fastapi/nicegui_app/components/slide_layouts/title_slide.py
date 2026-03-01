"""title_slide — 居中标题封面版式。"""

import html as html_module


def render_title_slide(data: dict) -> str:
    """
    生成 title_slide 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，至少含 title；可用 subtitle 或首条 bullet 作为副标题

    Returns:
        完整 HTML 字符串，使用 Tailwind 实用类
    """
    title = html_module.escape(str(data.get("title") or "无标题"))
    # 副标题：优先 subtitle，否则用首条 bullet
    bullets = data.get("bullet_points") or []
    subtitle = data.get("subtitle") or (bullets[0] if bullets else "")
    subtitle = html_module.escape(str(subtitle)) if subtitle else ""

    html = f'''
<div class="flex flex-col items-center justify-center min-h-full h-full w-full bg-gradient-to-br from-indigo-500 to-purple-600 px-8 py-12">
  <h1 class="text-3xl md:text-4xl font-bold text-white text-center leading-tight">{title}</h1>
'''
    if subtitle:
        html += f'  <p class="mt-4 text-lg text-white/90 text-center max-w-2xl">{subtitle}</p>\n'
    html += "</div>\n"
    return html
