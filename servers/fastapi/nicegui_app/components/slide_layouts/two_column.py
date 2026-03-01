"""two_column — 双列对比版式。"""

import html as html_module


def render_two_column(data: dict) -> str:
    """
    生成 two_column 版式的 HTML 字符串。
    适用于 problem/solution、before/after 等对比场景。

    Args:
        data: SlidePreviewData，含 title, bullet_points 或 left/right 区块

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "对比"))
    left_block = data.get("left") or data.get("block1") or {}
    right_block = data.get("right") or data.get("block2") or {}

    def block_content(block: dict, default_title: str) -> str:
        if isinstance(block, dict):
            t = block.get("title") or block.get("heading") or default_title
            bullets = block.get("bullets") or block.get("items") or []
        else:
            t = default_title
            bullets = []
        t = html_module.escape(str(t))
        lis = ""
        for b in (bullets or [])[:6]:
            txt = str(b) if isinstance(b, str) else str(b.get("text", b))
            lis += f'<li class="text-sm text-gray-700">{html_module.escape(txt)}</li>\n'
        return f'<h3 class="text-lg font-semibold text-gray-800 mb-3">{t}</h3><ul class="list-disc list-inside space-y-1">{lis}</ul>'

    bullets = data.get("bullet_points") or []
    if left_block or right_block:
        left_html = block_content(left_block, "左侧")
        right_html = block_content(right_block, "右侧")
    else:
        # 均分 bullet_points 到两列
        n = len(bullets)
        mid = (n + 1) // 2
        left_items = bullets[:mid]
        right_items = bullets[mid:mid + 6]
        left_html = block_content({"title": "要点一", "bullets": left_items}, "要点一")
        right_html = block_content({"title": "要点二", "bullets": right_items}, "要点二")
        if not left_items and not right_items:
            left_html = '<h3 class="text-lg font-semibold text-gray-800 mb-3">左侧</h3><p class="text-sm text-gray-600">—</p>'
            right_html = '<h3 class="text-lg font-semibold text-gray-800 mb-3">右侧</h3><p class="text-sm text-gray-600">—</p>'

    return f'''
<div class="flex flex-col min-h-full h-full w-full bg-white p-6">
  <h2 class="text-xl md:text-2xl font-bold text-gray-800 mb-6 text-center">{title}</h2>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 flex-1">
    <div class="rounded-lg border border-indigo-200 bg-indigo-50/30 p-6">
      {left_html}
    </div>
    <div class="rounded-lg border border-purple-200 bg-purple-50/30 p-6">
      {right_html}
    </div>
  </div>
</div>
'''
