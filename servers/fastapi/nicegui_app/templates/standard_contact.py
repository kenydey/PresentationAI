from __future__ import annotations

from typing import Any, Dict, List

from nicegui import ui

from .base import SlideLayout, SlideLayoutMeta, register_layout


class ContactLayout(SlideLayout):
  """Python 版联系人页布局（简化自 standard/ContactLayout.tsx）。"""

  meta = SlideLayoutMeta(
    layout_id="header-left-media-contact-info-slide",
    name="Contact",
    description="左图右侧为联系信息列表的收尾页。",
    group="standard",
  )

  def render(self) -> None:  # type: ignore[override]
    d: Dict[str, Any] = self.data or {}
    left = d.get("leftPanel") or {}
    bg = left.get("backgroundImage") or {}
    image_url: str = bg.get("__image_url__") or (
      "https://images.pexels.com/photos/326576/pexels-photo-326576.jpeg"
    )

    right = d.get("rightContent") or {}
    title: str = right.get("title") or "Let’s Get in\nTouch with Us"
    sections: List[Dict[str, Any]] = right.get("sections") or [
      {
        "label": "Address",
        "value": "Boston, Downtown Main Street 233, New York, US",
        "showDivider": True,
      },
      {
        "label": "Phone",
        "value": "+1234 2345 1234",
        "showDivider": True,
      },
      {
        "label": "E-mail",
        "value": "mail@company.com",
        "showDivider": False,
      },
    ]

    with ui.row().classes(
      "w-full max-w-[1280px] max-h-[720px] aspect-video shadow-lg overflow-hidden rounded bg-white"
    ):
      with ui.column().classes("w-1/2 h-full"):
        ui.image(image_url).classes("w-full h-full object-cover")

      with ui.column().classes(
        "w-1/2 h-full q-px-xl q-py-xl justify-start items-start gap-6"
      ):
        ui.label(title).classes(
          "text-4xl font-bold whitespace-pre-line"
        )
        for sec in sections:
          label = sec.get("label") or ""
          value = sec.get("value") or ""
          show_div = bool(sec.get("showDivider", False))

          with ui.column().classes("gap-1 w-full"):
            ui.label(label).classes("text-lg font-semibold")
            ui.label(value).classes("text-sm text-gray-600")
            if show_div:
              ui.separator().classes("q-my-sm")


register_layout(ContactLayout())

