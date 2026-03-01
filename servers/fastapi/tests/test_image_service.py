"""单元测试：image_service 图像处理中间件。"""

import io
import pytest
from PIL import Image

from services.image_service import resize_and_crop, remove_background


def _create_test_image(width: int, height: int, format: str = "PNG") -> bytes:
    """创建简单测试图（红蓝渐变）。"""
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            r = int(255 * x / max(1, width))
            b = int(255 * y / max(1, height))
            pixels[x, y] = (r, 128, b)
    out = io.BytesIO()
    img.save(out, format=format)
    return out.getvalue()


class TestResizeAndCrop:
    """resize_and_crop 测试。"""

    def test_basic_resize_crop(self):
        """等比例缩放 + 居中裁剪。"""
        img_bytes = _create_test_image(400, 300)
        result = resize_and_crop(img_bytes, 200, 150)
        assert result is not None
        assert isinstance(result, io.BytesIO)
        result.seek(0)
        img = Image.open(result)
        assert img.size == (200, 150)

    def test_scale_up_then_crop(self):
        """小图放大后裁剪。"""
        img_bytes = _create_test_image(100, 100)
        result = resize_and_crop(img_bytes, 200, 150)
        result.seek(0)
        img = Image.open(result)
        assert img.size == (200, 150)

    def test_invalid_dimensions(self):
        """非法目标尺寸应抛异常。"""
        img_bytes = _create_test_image(100, 100)
        with pytest.raises(ValueError):
            resize_and_crop(img_bytes, 0, 150)
        with pytest.raises(ValueError):
            resize_and_crop(img_bytes, 100, -1)

    def test_returns_bytes_io_seek_zero(self):
        """返回的 BytesIO 应 seek(0)，可直接 read。"""
        img_bytes = _create_test_image(50, 50)
        result = resize_and_crop(img_bytes, 25, 25)
        data = result.read()
        assert len(data) > 0


class TestRemoveBackground:
    """remove_background 测试（需要 rembg，可能较慢）。"""

    @pytest.mark.slow
    def test_remove_background_returns_png(self):
        """背景抠除应返回 PNG 字节流。"""
        img_bytes = _create_test_image(64, 64)
        result = remove_background(img_bytes)
        assert result is not None
        result.seek(0)
        img = Image.open(result)
        assert img.mode == "RGBA"
        assert img.format == "PNG"
