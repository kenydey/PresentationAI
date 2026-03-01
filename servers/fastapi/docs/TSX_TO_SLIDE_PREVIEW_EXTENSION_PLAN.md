# TSX 布局扩展 NiceGUI slide_preview 实施方案

> 目标：以 PresentationAI TSX 布局为数据源，为 NiceGUI 的 slide_preview 增加更多版式  
> 依赖：`extract_templates.py` 已修正 TEMPLATES_DIR 指向 `PresentationAI/servers/nextjs/app/presentation-templates`

---

## 一、现状

| 项目 | 说明 |
|------|------|
| **template_registry.json** | 8 组 120 个 layout，含 id、name、description、json_schema |
| **slide_preview 现有** | 3 种版式：title_slide、text_image_split、three_column_grid |
| **layout_id 映射** | `get_preview_layout_type()` 按关键词推断，多数 layout 落入 text_image_split |
| **TSX 布局分类** | general、standard、modern、swift、neo-general、neo-modern、neo-standard、neo-swift |

---

## 二、扩展策略

### 2.1 布局分类与映射

从 template_registry 和 TSX 分析，新增以下版式类型及映射规则：

| 版式类型 | 对应 TSX 布局关键词 | 数据字段 | 说明 |
|----------|---------------------|----------|------|
| title_slide | intro, title | title, subtitle | 已有 |
| text_image_split | basic, bullet, image, description | title, bullet_points, image_url | 已有 |
| three_column_grid | toc, grid, three, column | title, bullet_points (3 列) | 已有 |
| **metrics** | metrics | title, metrics (label/value/description) | 新增 |
| **quote** | quote | title, quote | 新增 |
| **team** | team | title, members (name/role) | 新增 |
| **chart_bullets** | chart-with-bullets | title, bullet_points, chart 占位 | 新增（图表暂占位） |
| **numbered_list** | numbered, bullets | title, bullet_points (有序) | 新增 |
| **two_column** | two-column, dual | title, bullet_points (2 列) | 新增 |
| **contact** | contact | title, contact 信息 | 新增 |

### 2.2 实施步骤

#### 阶段 1：扩展 get_preview_layout_type 映射（低风险）

**文件**：`nicegui_app/components/slide_preview.py`

```python
def get_preview_layout_type(layout_id: str) -> str:
    lid = (layout_id or "").lower()
    # 现有
    if "intro" in lid or "title" in lid or lid in ("general-intro-slide",):
        return "title_slide"
    if "toc" in lid or "grid" in lid or "three" in lid or "column" in lid:
        return "three_column_grid"
    # 新增
    if "metrics" in lid:
        return "metrics"
    if "quote" in lid:
        return "quote"
    if "team" in lid:
        return "team"
    if "chart" in lid and "bullet" in lid:
        return "chart_bullets"
    if "numbered" in lid or "number" in lid:
        return "numbered_list"
    if "contact" in lid:
        return "contact"
    if "two" in lid or "dual" in lid:
        return "two_column"
    return "text_image_split"
```

#### 阶段 2：新增布局渲染模块（按需分批）

**目录**：`nicegui_app/components/slide_layouts/`

| 新文件 | 参考 TSX | 输入字段 |
|--------|----------|----------|
| metrics_slide.py | MetricsSlideLayout.tsx | title, metrics |
| quote_slide.py | QuoteSlideLayout.tsx | title, quote |
| team_slide.py | TeamSlideLayout.tsx | title, members |
| chart_bullets_slide.py | ChartWithBulletsSlideLayout.tsx | title, bullet_points（图表占位） |
| numbered_list_slide.py | NumberedBulletsSlideLayout.tsx | title, bullet_points |
| two_column_slide.py | 参考 general 两列 | title, bullet_points |
| contact_slide.py | ContactLayout.tsx | title, contact 信息 |

**渲染函数签名**：`def render_xxx(data: dict) -> str`，返回 Tailwind HTML 字符串。

#### 阶段 3：扩展 SlidePreviewData 与 slide_preview_data

**文件**：`nicegui_app/utils/slide_preview_data.py`

- 在 `slide_to_preview_data()` 中，从 `content` 提取 metrics、quote、members 等字段
- 字段名与 TSX Schema / get_slide_content 输出保持一致

#### 阶段 4：slide_preview 主入口扩展

**文件**：`nicegui_app/components/slide_preview.py`

```python
from nicegui_app.components.slide_layouts import (
    render_title_slide,
    render_text_image_split,
    render_three_column_grid,
    render_metrics_slide,      # 新增
    render_quote_slide,        # 新增
    render_team_slide,        # 新增
    # ...
)

def render_slide_preview_html(data, layout_type=None):
    if layout_type is None:
        layout_type = get_preview_layout_type(data.get("layout_id") or "")
    # switch 补充新类型
    if layout_type == "metrics":
        return render_metrics_slide(data)
    # ...
```

---

## 三、TSX → Python 布局参考

### 3.1 Metrics 布局（MetricsSlideLayout.tsx）

- 结构：标题居中 + metrics 网格（label / value / description）
- Tailwind：`grid grid-cols-1 md:grid-cols-2` 或 `md:grid-cols-3`，卡片式 description
- 数据：`metrics: [{label, value, description}, ...]`

### 3.2 Quote 布局（QuoteSlideLayout.tsx）

- 结构：标题 + 引用块 + 可选的引用来源
- 数据：`quote` 或 `title` + `description` 作为引用

### 3.3 Team 布局（TeamSlideLayout.tsx）

- 结构：标题 + 成员卡片（头像占位 / name / role）
- 数据：`members` 或从 `content` 的 team 相关字段解析

### 3.4 通用原则

- 使用 Tailwind 类，保持 16:9 或 `aspect-video`
- 容器：`min-h-full w-full` 或 `max-w-[1280px]`
- 图片：`__image_url__` 或 `image_url`，缺省时显示占位
- 文本：统一 `html.escape()` 防 XSS

---

## 四、实施优先级

| 优先级 | 版式 | 工作量 | 价值 |
|--------|------|--------|------|
| 1 | metrics | 中 | 高，数据展示常用 |
| 2 | quote | 低 | 中 |
| 3 | team | 中 | 中 |
| 4 | numbered_list | 低 | 中 |
| 5 | two_column | 低 | 中 |
| 6 | contact | 低 | 低 |
| 7 | chart_bullets | 高 | 中（图表需占位或后续集成） |

---

## 五、已完成项

- [x] 修正 `extract_templates.py` 的 `TEMPLATES_DIR` 指向 `PresentationAI/servers/nextjs/app/presentation-templates`
- [x] 删除 `PresentationAI/electron` 以减小体积
- [ ] 按上述阶段实施 slide_preview 扩展（待执行）
