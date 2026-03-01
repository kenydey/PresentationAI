"""three_column_grid — 三列卡片布局。"""

import html as html_module


def render_three_column_grid(data: dict) -> str:
    """
    生成 three_column_grid 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, bullet_points；标题放顶部，要点均分三列

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "无标题"))
    bullets = data.get("bullet_points") or []

    # 均分三列
    n = len(bullets)
    col_size = max(1, (n + 2) // 3)
    cols = [
        bullets[i * col_size : (i + 1) * col_size]
        for i in range(3)
    ]
    # 若不足三列，补空
    while len(cols) < 3:
        cols.append([])

    def col_html(items: list, idx: int) -> str:
        labels = ["一", "二", "三"]
        label = labels[idx] if idx < 3 else ""
        lis = "".join(
            f'<li class="text-sm text-gray-600">{html_module.escape(str(b))}</li>'
            for b in items
        )
        return f'''
<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
  <h3 class="text-base font-semibold text-gray-800 mb-2">{label}</h3>
  <ul class="space-y-1 list-disc list-inside">
    {lis}
  </ul>
</div>'''

    cols_html = "".join(col_html(cols[i], i) for i in range(3))

    html = f'''
<div class="flex flex-col min-h-full h-full w-full bg-gray-50 p-6">
  <h2 class="text-xl md:text-2xl font-bold text-gray-800 mb-6 text-center">{title}</h2>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 flex-1">
    {cols_html}
  </div>
</div>
'''
    return html
