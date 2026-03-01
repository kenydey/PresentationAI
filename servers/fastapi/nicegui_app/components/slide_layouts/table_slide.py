"""table — 表+说明版式。"""

import html as html_module


def render_table_slide(data: dict) -> str:
    """
    生成 table 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, table (rows/headers) 或 bullet_points 转为表格

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "表格"))
    desc = data.get("description") or ""
    desc = html_module.escape(str(desc)[:200]) if desc else ""

    table_data = data.get("table") or {}
    headers = table_data.get("headers") or table_data.get("columns") or []
    rows = table_data.get("rows") or table_data.get("data") or []

    if not isinstance(headers, list):
        headers = []
    if not isinstance(rows, list):
        rows = []

    # 若无可直接用数据，用 bullet_points 构造简单表格
    if not rows and headers:
        rows = []
    if not headers and not rows:
        bullets = data.get("bullet_points") or []
        for b in bullets[:5]:
            txt = str(b) if isinstance(b, str) else str(b.get("text", b))
            parts = [p.strip() for p in txt.split("|") or [txt]]
            if len(parts) >= 2:
                if not headers:
                    headers = [f"列{i+1}" for i in range(len(parts))]
                rows.append(parts[:len(headers)])
            else:
                if not headers:
                    headers = ["项目", "说明"]
                rows.append([txt[:50], ""])
        if not headers:
            headers = ["列1", "列2", "列3"]
        if not rows:
            rows = [["—", "—", "—"]]

    # 确保 headers 数量一致
    max_cols = max(len(headers), max((len(r) for r in rows), default=0), 2)
    while len(headers) < max_cols:
        headers.append(f"列{len(headers)+1}")
    headers = headers[:max_cols]

    th_html = "".join(f'<th class="px-4 py-2 text-left text-sm font-semibold text-gray-800 bg-indigo-100">{html_module.escape(str(h))}</th>' for h in headers)

    trs_html = ""
    for r in rows:
        cells = r if isinstance(r, (list, tuple)) else [r]
        cells = [str(c)[:50] for c in cells[:max_cols]]
        while len(cells) < max_cols:
            cells.append("")
        trs_html += "<tr>" + "".join(f'<td class="px-4 py-2 text-sm text-gray-700 border-b border-gray-200">{html_module.escape(c)}</td>' for c in cells) + "</tr>"

    desc_block = f'<p class="text-sm text-gray-600 mb-4">{desc}</p>' if desc else ""

    return f'''
<div class="flex flex-col min-h-full h-full w-full bg-white p-6">
  <h2 class="text-xl md:text-2xl font-bold text-gray-800 mb-2">{title}</h2>
  {desc_block}
  <div class="flex-1 overflow-auto">
    <table class="w-full border-collapse">
      <thead><tr>{th_html}</tr></thead>
      <tbody>{trs_html}</tbody>
    </table>
  </div>
</div>
'''
