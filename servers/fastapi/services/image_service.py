"""图像处理中间件 — 预处理与背景抠除，供 PPT 生成使用。所有输出为 io.BytesIO，避免落盘。"""

import io

from PIL import Image

# Pillow 9.1+ 使用 Resampling.LANCZOS，旧版用 LANCZOS
try:
    _LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    _LANCZOS = Image.LANCZOS


def resize_and_crop(
    image_bytes: bytes,
    target_width: int,
    target_height: int,
) -> io.BytesIO:
    """
    等比例 Lanczos 缩放后居中硬裁剪至目标尺寸，确保无留白。

    算法：计算最大缩放因子使图像至少覆盖目标区域，再居中裁剪。

    Args:
        image_bytes: 原始图片字节
        target_width: 目标宽度
        target_height: 目标高度

    Returns:
        io.BytesIO 内存流，PNG 格式（若含透明通道）或 JPEG

    Raises:
        ValueError: target_width 或 target_height <= 0
    """
    if target_width <= 0 or target_height <= 0:
        raise ValueError("target_width 和 target_height 必须大于 0")

    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    w, h = img.size

    if w == 0 or h == 0:
        raise ValueError("图片尺寸无效")

    scale = max(target_width / w, target_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    if new_w == 0 or new_h == 0:
        raise ValueError("缩放后尺寸无效")

    resized = img.resize((new_w, new_h), _LANCZOS)
    left = (new_w - target_width) // 2
    top = (new_h - target_height) // 2
    cropped = resized.crop(
        (left, top, left + target_width, top + target_height)
    )

    out = io.BytesIO()
    if cropped.mode == "RGBA" and cropped.getextrema()[3] != (255, 255):
        cropped.save(out, format="PNG", optimize=True)
    else:
        cropped.convert("RGB").save(out, format="JPEG", quality=90, optimize=True)
    out.seek(0)
    return out


def remove_background(image_bytes: bytes) -> io.BytesIO:
    """
    使用 rembg 精准擦除图片背景，输出带透明通道的 PNG。

    Args:
        image_bytes: 原始图片字节

    Returns:
        io.BytesIO 内存流，PNG 格式（RGBA）
    """
    from rembg import remove as rembg_remove

    img = Image.open(io.BytesIO(image_bytes))
    out_img = rembg_remove(img)

    if out_img.mode != "RGBA":
        out_img = out_img.convert("RGBA")

    out = io.BytesIO()
    out_img.save(out, format="PNG", optimize=True)
    out.seek(0)
    return out


def preprocess_for_slide(
    image_bytes: bytes,
    target_width: int,
    target_height: int,
    remove_bg: bool = False,
) -> io.BytesIO:
    """
    幻灯片图片统一预处理：可选背景抠除 + resize_and_crop。

    Args:
        image_bytes: 原始图片字节
        target_width: 目标宽度
        target_height: 目标高度
        remove_bg: 是否先执行背景抠除

    Returns:
        io.BytesIO 内存流
    """
    data = image_bytes
    if remove_bg:
        data = remove_background(data).read()
    return resize_and_crop(data, target_width, target_height)
