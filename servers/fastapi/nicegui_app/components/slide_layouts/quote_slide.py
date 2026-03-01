"""quote — 引用块+背景版式。"""

import html as html_module


def render_quote_slide(data: dict) -> str:
    """
    生成 quote 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 heading/title, quote, author；可选 image_url 作为背景

    Returns:
        完整 HTML 字符串
    """
    heading = data.get("heading") or data.get("title") or "金句"
    quote_text = data.get("quote") or ""
    author = data.get("author") or ""
    image_url = data.get("image_url")

    # 若无 quote，用首条 bullet 作为引用
    if not quote_text:
        bullets = data.get("bullet_points") or []
        quote_text = bullets[0] if bullets else ""

    heading = html_module.escape(str(heading))
    quote_text = html_module.escape(str(quote_text)[:300])
    author = html_module.escape(str(author)[:80])

    bg_style = ""
    if image_url:
        bg_style = f'background-image: url("{html_module.escape(image_url)}"); background-size: cover;'

    return f'''
<div class="flex flex-col items-center justify-center min-h-full h-full w-full relative overflow-hidden px-12 py-16" style="{bg_style}">
  <div class="absolute inset-0 bg-gradient-to-br from-indigo-900/85 to-purple-900/85"></div>
  <div class="relative z-10 text-center max-w-3xl">
    <p class="text-indigo-200 text-sm font-medium uppercase tracking-wider mb-4">{heading}</p>
    <svg class="w-12 h-12 mx-auto text-indigo-300 mb-4" fill="currentColor" viewBox="0 0 24 24">
      <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
    </svg>
    <blockquote class="text-xl md:text-2xl lg:text-3xl font-medium text-white leading-relaxed italic">"{quote_text}"</blockquote>
    <p class="mt-6 text-indigo-200 font-medium">— {author}</p>
  </div>
</div>
'''
