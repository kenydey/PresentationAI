"""metrics — 指标卡片网格版式。"""

import html as html_module


def render_metrics_slide(data: dict) -> str:
    """
    生成 metrics 版式的 HTML 字符串。

    Args:
        data: SlidePreviewData，含 title, metrics (列表，每项含 label, value, description)

    Returns:
        完整 HTML 字符串
    """
    title = html_module.escape(str(data.get("title") or "指标"))
    metrics_raw = data.get("metrics") or []
    if not isinstance(metrics_raw, list):
        metrics_raw = []

    # 若 metrics 为空，尝试用 bullet_points 构造
    metrics: list = []
    for m in metrics_raw[:9]:
        if isinstance(m, dict):
            metrics.append({
                "label": str(m.get("label") or m.get("name") or "").strip()[:50],
                "value": str(m.get("value") or "").strip()[:20],
                "description": str(m.get("description") or m.get("desc") or "").strip()[:150],
            })
        else:
            metrics.append({"label": "", "value": str(m)[:20], "description": ""})

    if not metrics:
        bullets = data.get("bullet_points") or []
        for i, b in enumerate(bullets[:6]):
            txt = str(b) if isinstance(b, str) else str(b.get("text", b))
            parts = txt.split(":", 1)
            value = parts[0].strip()[:20] if parts else txt[:20]
            desc = parts[1].strip()[:80] if len(parts) > 1 else ""
            metrics.append({"label": str(i + 1), "value": value, "description": desc})
        if not metrics:
            metrics = [{"label": "指标", "value": "—", "description": "暂无数据"}]

    # 网格布局：1–3 列
    n = len(metrics)
    if n <= 2:
        grid_cls = "grid-cols-1 md:grid-cols-2"
    elif n <= 4:
        grid_cls = "grid-cols-2 md:grid-cols-4"
    else:
        grid_cls = "grid-cols-2 md:grid-cols-3"

    cards_html = ""
    for m in metrics:
        lbl = html_module.escape(m["label"] or "")
        val = html_module.escape(m["value"] or "—")
        desc = html_module.escape(m["description"] or "")
        cards_html += f'''
<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
  <p class="text-3xl font-bold text-indigo-600">{val}</p>
  <p class="mt-1 text-sm font-semibold text-gray-800">{lbl}</p>
  <p class="mt-2 text-xs text-gray-600">{desc}</p>
</div>'''

    return f'''
<div class="flex flex-col min-h-full h-full w-full bg-gray-50 p-6">
  <h2 class="text-xl md:text-2xl font-bold text-gray-800 mb-6 text-center">{title}</h2>
  <div class="grid {grid_cls} gap-4 flex-1 place-content-start">
    {cards_html}
  </div>
</div>
'''
