"""
Pipeline pptx 构造模块：封装 PptxPresentationCreator，将 JSON/Model 转为 .pptx 文件。
与文本生成、图像请求严格物理隔离。
"""

import os
from typing import Optional

try:
    from ppt_generator.pptx_presentation_creator import PptxPresentationCreator
    from ppt_generator.models.pptx_models import PptxPresentationModel

    _HAS_PPT_GENERATOR = True
except ImportError:
    _HAS_PPT_GENERATOR = False


def build_pptx_from_model(
    ppt_model: "PptxPresentationModel",
    temp_dir: str,
    output_path: Optional[str] = None,
) -> str:
    """
    从 PptxPresentationModel 构建 .pptx 文件。
    数据流：JSON 大纲 + 资产 -> PptxPresentationModel -> python-pptx 渲染 -> 文件。
    返回生成的 pptx 文件路径。
    """
    if not _HAS_PPT_GENERATOR:
        raise ImportError("ppt_generator is required for build_pptx_from_model")

    creator = PptxPresentationCreator(ppt_model, temp_dir)
    creator.create_ppt()

    if output_path:
        creator.save(output_path)
        return output_path

    # 若未指定路径，保存到 temp_dir
    path = os.path.join(temp_dir, "presentation.pptx")
    creator.save(path)
    return path
