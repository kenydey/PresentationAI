from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from nicegui import ui


@dataclass
class SlideLayoutMeta:
  layout_id: str
  name: str
  description: str
  group: str = "standard"


class SlideLayout(ABC):
  """Python 侧的模板基类，用于在 NiceGUI 中预览/编辑布局。"""

  meta: SlideLayoutMeta

  def __init__(self, data: Optional[Dict[str, Any]] = None) -> None:
    self.data: Dict[str, Any] = data or {}

  @abstractmethod
  def render(self) -> None:
    """在当前 NiceGUI 容器中渲染该布局。"""
    raise NotImplementedError


_REGISTRY: Dict[str, SlideLayout] = {}


def register_layout(layout: SlideLayout) -> None:
  """注册布局实例，按 layout_id 存储。"""
  _REGISTRY[layout.meta.layout_id] = layout


def get_registered_layouts() -> List[SlideLayoutMeta]:
  return [l.meta for l in _REGISTRY.values()]


def create_layout_instance(layout_id: str, data: Optional[Dict[str, Any]] = None) -> Optional[SlideLayout]:
  base = _REGISTRY.get(layout_id)
  if not base:
    return None
  # 以同类重新构造实例，传入数据
  cls = base.__class__
  return cls(data=data or {})

