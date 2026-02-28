"""
Pipeline 图像请求模块：图像 API 调用与路径管理。
与文本生成、pptx 构造严格物理隔离。
封装现有 image_processor / services 逻辑。
"""

import os
import uuid
from typing import List, Tuple

# 兼容 image_processor
try:
    from image_processor.images_finder import generate_image as _generate_image_impl
    from image_processor.icons_vectorstore_utils import get_icons_vectorstore
    from image_processor.icons_finder import get_icon as _get_icon_impl
    from ppt_generator.slide_model_utils import SlideModelUtils

    _HAS_IMAGE_PROCESSOR = True
except ImportError:
    _HAS_IMAGE_PROCESSOR = False


async def fetch_slide_assets(
    slide_models: List,
    theme: str,
    presentation_dir: str,
) -> Tuple[List, List]:
    """
    拉取幻灯片所需图像与图标资产。
    返回 (image_results, icon_results)。
    封装 generate_stream 中 fetch_slide_assets 的直线性逻辑。
    """
    if not _HAS_IMAGE_PROCESSOR:
        raise ImportError("image_processor is required for fetch_slide_assets")

    image_prompts = []
    icon_queries = []
    image_paths = []
    icon_paths = []

    for each_slide_model in slide_models:
        slide_model_utils = SlideModelUtils(theme, each_slide_model)
        if getattr(each_slide_model, "images", None):
            prompts = slide_model_utils.get_image_prompts()
            image_prompts.extend(prompts)
            image_paths.extend(each_slide_model.images)
        if getattr(each_slide_model, "icons", None):
            icon_queries.extend(slide_model_utils.get_icon_queries())
            icon_paths.extend(each_slide_model.icons)

    if not image_prompts and not icon_queries:
        return [], []

    import asyncio

    coroutines = [
        _generate_image_impl(pp, path) for pp, path in zip(image_prompts, image_paths)
    ]
    if icon_queries:
        icon_vector_store = get_icons_vectorstore()
        coroutines.extend(
            _get_icon_impl(icon_vector_store, q, path)
            for q, path in zip(icon_queries, icon_paths)
        )

    results = await asyncio.gather(*coroutines)
    n_images = len(image_prompts)
    return list(results[:n_images]), list(results[n_images:])


def allocate_asset_paths(
    presentation_dir: str,
    slide_models: List,
    asset_type: str = "images",
) -> None:
    """
    为幻灯片预分配图像/图标路径。
    asset_type: 'images' | 'icons'
    """
    ext = "jpg" if asset_type == "images" else "png"
    base = os.path.join(presentation_dir, asset_type)
    os.makedirs(base, exist_ok=True)

    for slide_model in slide_models:
        if asset_type == "images" and getattr(slide_model, "images", None):
            for i in range(len(slide_model.images)):
                slide_model.images[i] = os.path.join(base, f"{uuid.uuid4()}.{ext}")
        elif asset_type == "icons" and getattr(slide_model, "icons", None):
            for i in range(len(slide_model.icons)):
                slide_model.icons[i] = os.path.join(base, f"{uuid.uuid4()}.{ext}")
