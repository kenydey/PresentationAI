from __future__ import annotations

from typing import Any, Dict, Optional

from nicegui import ui

from .base import SlideLayout, SlideLayoutMeta, register_layout


class IntroSlideLayout(SlideLayout):
  """Python 版 Intro Slide 布局（对应 standard/IntroSlideLayout.tsx 的简化版）。"""

  meta = SlideLayoutMeta(
    layout_id="header-counter-two-column-image-text-slide",
    name="Intro Slide",
    description=(
      "左图右文的开场页，包含标题、副文案，可选的引导卡片。"
    ),
    group="standard",
  )

  def render(self) -> None:  # type: ignore[override]
    d: Dict[str, Any] = self.data or {}
    title: str = d.get("title") or "Introduction Our Pitchdeck"
    br_index: int = int(d.get("titleBreakAfter") or 12)
    title_first = title[:br_index]
    title_second = title[br_index:]

    paragraph: str = d.get("paragraph") or (
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
      "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    )

    media = d.get("media") or {}
    image_data = media.get("image") or {}
    image_url: str = image_data.get("__image_url__") or (
      "https://images.unsplash.com/photo-1557426272-fc759fdf7a8d"
    )

    intro = d.get("introCard") or {}
    intro_enabled: bool = bool(intro.get("enabled", True))
    intro_initials: str = intro.get("initials") or "PDT"
    intro_name: str = intro.get("name") or "Pitch Deck Team"
    intro_date: str = intro.get("date") or "December 22, 2025"

    with ui.row().classes(
      "w-full max-w-[1280px] max-h-[720px] aspect-video shadow-lg overflow-hidden rounded bg-white"
    ):
      # 左侧图片
      with ui.column().classes("w-1/2 h-full"):
        ui.image(image_url).classes("w-full h-full object-cover")

      # 右侧文本
      with ui.column().classes("w-1/2 h-full justify-start items-start q-pa-xl gap-4"):
        ui.label(f"{title_first}\n{title_second}").classes(
          "text-4xl font-bold whitespace-pre-line"
        )
        ui.label(paragraph).classes("text-sm text-gray-600 leading-relaxed")

        if intro_enabled:
          with ui.row().classes(
            "items-center gap-4 q-mt-md border rounded-lg q-pa-md shadow-sm"
          ):
            with ui.column().classes(
              "w-16 h-16 rounded-full items-center justify-center bg-emerald-600 text-white font-bold text-lg"
            ):
              ui.label(intro_initials)
            with ui.column().classes("gap-1"):
              ui.label(intro_name).classes("text-base font-semibold")
              ui.label(intro_date).classes("text-xs text-emerald-700")


# 注册一个无需数据的默认实例，后续通过 create_layout_instance 复制
register_layout(IntroSlideLayout())

