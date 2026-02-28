"""
Graphviz 流程图渲染服务：将 DOT 语法转为 PNG 图像，用于插入幻灯片。
借鉴 Chat2PPTX：LLM 输出标准 Graphviz DOT -> 解析 -> 渲染 -> 插入 pptx
"""

import io
from typing import Optional

# pygraphviz 需要系统安装 Graphviz
try:
    import pygraphviz as pgv

    _HAS_PYGRAPHVIZ = True
except ImportError:
    _HAS_PYGRAPHVIZ = False


def render_dot_to_png(
    dot_source: str,
    dpi: int = 150,
    bg_color: str = "transparent",
) -> Optional[bytes]:
    """
    将 Graphviz DOT 源码渲染为 PNG 字节流。
    dot_source: 标准 DOT 语法字符串
    dpi: 分辨率
    bg_color: 背景色，transparent 表示透明
    返回 PNG bytes 或 None（解析失败时）
    """
    if not _HAS_PYGRAPHVIZ:
        return None

    try:
        g = pgv.AGraph(string=dot_source)
        g.layout(prog="dot")
        buf = io.BytesIO()
        g.draw(buf, format="png", args=f"-Gdpi={dpi}")
        buf.seek(0)
        return buf.read()
    except Exception:
        return None


def render_dot_to_png_file(
    dot_source: str,
    output_path: str,
    dpi: int = 150,
) -> bool:
    """
    将 DOT 渲染为 PNG 并保存到文件。
    返回是否成功。
    """
    png_bytes = render_dot_to_png(dot_source, dpi=dpi)
    if not png_bytes:
        return False
    try:
        with open(output_path, "wb") as f:
            f.write(png_bytes)
        return True
    except Exception:
        return False


def is_graphviz_available() -> bool:
    """检查 Graphviz 是否可用。"""
    return _HAS_PYGRAPHVIZ
