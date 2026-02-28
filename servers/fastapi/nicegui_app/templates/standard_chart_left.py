from __future__ import annotations

from typing import Any, Dict, List

from nicegui import ui

from .base import SlideLayout, SlideLayoutMeta, register_layout


class ChartLeftTextRightLayout(SlideLayout):
  """Python 版图表左、文字右布局（简化自 standard/ChartLeftTextRightLayout.tsx）。

  不使用 Recharts，而是用简单的水平条模拟图表效果。
  """

  meta = SlideLayoutMeta(
    layout_id="chart-left-text-right-layout",
    name="Chart Left Text Right",
    description="左侧为简单条形“图表”，右侧为标题+说明文字。",
    group="standard",
  )

  def render(self) -> None:  # type: ignore[override]
    d: Dict[str, Any] = self.data or {}
    title: str = d.get("title") or "Insights At A Glance"
    paragraph: str = d.get("paragraph") or (
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
      "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    )
    chart = d.get("chart") or {}
    points: List[Dict[str, Any]] = chart.get("data") or [
      {"label": "A", "value": 60},
      {"label": "B", "value": 42},
      {"label": "C", "value": 75},
      {"label": "D", "value": 30},
    ]

    with ui.row().classes(
      "w-full max-w-[1280px] max-h-[720px] aspect-video shadow-lg overflow-hidden rounded bg-white"
    ):
      # Left: simple bar chart
      with ui.column().classes("w-1/2 h-full q-pa-xl justify-center"):
        ui.label("Chart").classes("text-sm text-gray-500 q-mb-sm")
        max_val = max((p.get("value") or 0) for p in points) or 1
        for p in points:
          label = str(p.get("label") or "")
          val = float(p.get("value") or 0)
          width_pct = max(2, min(100, int(val / max_val * 100)))
          with ui.row().classes("items-center gap-2 q-mb-xs w-full"):
            ui.label(label).classes("text-xs text-gray-500 w-6")
            with ui.row().classes("h-3 rounded bg-gray-200 flex-1 overflow-hidden"):
              ui.row().classes("h-full bg-emerald-500").style(
                f"width: {width_pct}%;"
              )
            ui.label(f"{int(val)}").classes("text-xs text-gray-600 w-8 text-right")

      # Right: text
      with ui.column().classes("w-1/2 h-full q-pa-xl justify-center gap-4"):
        ui.label(title).classes("text-4xl font-bold")
        ui.label(paragraph).classes("text-sm text-gray-600 leading-relaxed")


register_layout(ChartLeftTextRightLayout())

