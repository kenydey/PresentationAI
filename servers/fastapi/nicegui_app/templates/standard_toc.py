from __future__ import annotations

from typing import Any, Dict, List

from nicegui import ui

from .base import SlideLayout, SlideLayoutMeta, register_layout


class TableOfContentsLayout(SlideLayout):
  """Python 版 Table Of Contents 布局（简化自 standard/TableOfContentsLayout.tsx）。"""

  meta = SlideLayoutMeta(
    layout_id="table-of-contents-layout",
    name="Table Of Contents",
    description="包含标题与两列目录卡片的目录页。",
    group="standard",
  )

  def render(self) -> None:  # type: ignore[override]
    d: Dict[str, Any] = self.data or {}
    title: str = d.get("title") or "Table Of Contents"
    description: str = d.get("description") or (
      "Use this as a quick guide to navigate the presentation sections."
    )
    raw_items: List[Dict[str, Any]] = d.get("items") or []
    if not raw_items:
      raw_items = [
        {"title": "Introduction"},
        {"title": "Problem Statement"},
        {"title": "Solution"},
        {"title": "Market"},
        {"title": "Business Model"},
        {"title": "Roadmap"},
      ]

    with ui.column().classes(
      "w-full max-w-[1280px] max-h-[720px] aspect-video shadow-lg overflow-hidden rounded bg-white q-pa-xl gap-6"
    ):
      ui.label(title).classes("text-4xl font-bold")
      ui.label(description).classes("text-sm text-gray-600 max-w-[900px]")

      with ui.grid(columns=2).classes("gap-3 w-full"):
        for idx, item in enumerate(raw_items):
          t = item.get("title") or f"Section {idx+1}"
          with ui.row().classes(
            "items-center gap-3 border rounded-lg q-pa-sm shadow-sm bg-white"
          ):
            with ui.row().classes(
              "w-8 h-8 rounded-full items-center justify-center border text-sm font-semibold"
            ):
              ui.label(str(idx + 1))
            ui.label(t).classes("text-base font-medium truncate")


register_layout(TableOfContentsLayout())

