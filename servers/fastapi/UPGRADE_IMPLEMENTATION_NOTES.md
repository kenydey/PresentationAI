# 升级实施说明

基于《PresentationAI_软件升级实施方案》已完成阶段一、二、四的核心实现。

## 已实施内容

### 阶段一：基础加固

1. **pipeline/** 模块
   - `text_generation.py`：封装 `generate_presentation_stream`、`generate_outline`、`parse_presentation_json`
   - `image_requests.py`：封装 `fetch_slide_assets`、`allocate_asset_paths`
   - `pptx_constructor.py`：封装 `build_pptx_from_model`

2. **图像处理增强**
   - `utils/image_utils.py`：新增 `align_image_to_theme_colors(image, theme_hex_list, strength)`
   - `ppt_generator/utils.py`：同步添加

3. **文本溢出防护**
   - `utils/text_autofit.py`：`apply_text_frame_autofit_properties`、`compute_text_fitting_font_size`
   - `ppt_generator/pptx_presentation_creator.py`：所有 textbox 设置 `word_wrap=True`、`auto_size=SHAPE_TO_FIT_TEXT`
   - `constants/prompt_constraints.py`：`LAYOUT_CHAR_LIMITS`、`TEXT_OVERFLOW_SYSTEM_HINT`

### 阶段二：Orchestrator 与多智能体

1. **orchestrator/**
   - `research_agent.py`：Research Agent，封装 `generate_ppt_outline`
   - `design_agent.py`：Design Agent，封装 `generate_presentation_structure`
   - `orchestrator.py`：`PresentationOrchestrator` 主控调度器

### 阶段四：Graphviz

1. **services/graphviz_renderer.py**
   - `render_dot_to_png(dot_source)`：DOT → PNG bytes
   - `render_dot_to_png_file(dot_source, output_path)`
   - `is_graphviz_available()`

## 使用方式

### Pipeline（逐步迁移）

```python
from pipeline import generate_presentation_text, parse_presentation_json, fetch_slide_assets, build_pptx_from_model
```

### Orchestrator（多智能体）

```python
from orchestrator import PresentationOrchestrator, ResearchAgent, DesignAgent

orc = PresentationOrchestrator()
async for chunk in orc.run_outline_pipeline(content, n_slides, layout_model, ...):
    ...
```

### Graphviz

```python
from services.graphviz_renderer import render_dot_to_png, is_graphviz_available

if is_graphviz_available():
    png_bytes = render_dot_to_png("digraph G { A -> B; }")
```

### 图像色彩对齐

```python
from utils.image_utils import align_image_to_theme_colors

img = align_image_to_theme_colors(img, ["#1a1a2e", "#16213e"], strength=0.3)
```

## 依赖

- **numpy**：已加入 pyproject（align_image_to_theme_colors）
- **pygraphviz**：可选，`pip install .[graphviz]`，需系统安装 Graphviz

## 后续集成建议

1. 在 `generate_stream` 中逐步替换为 `pipeline.fetch_slide_assets`
2. 在 outline 流程中接入 `PresentationOrchestrator`
3. 研究智能体检测到流程图内容时，调用 `graphviz_renderer` 生成 PNG 并插入幻灯片
