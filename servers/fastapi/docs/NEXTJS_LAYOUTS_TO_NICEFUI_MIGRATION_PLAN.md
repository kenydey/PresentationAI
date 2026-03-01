# Next.js 120 布局迁移 NiceGUI 方案

> 目标：保留一套前端（NiceGUI），将 Next.js 下 8 组 120 个 layout 迁移到 NiceGUI 的 slide_preview

---

## 一、现状与约束

| 项目 | 说明 |
|------|------|
| **TSX 布局** | 120 个 React 组件，使用 Tailwind，输出 16:9 幻灯片 HTML |
| **数据源** | 各 layout 有 Zod Schema → 提取为 json_schema（title、description、metrics、chartData 等） |
| **差异点** | 布局差异主要在**视觉结构**（左右分栏、三列、卡片网格等），不是 schema |
| **NiceGUI 能力** | `ui.html(tailwind_html)` 可渲染任意 Tailwind HTML，与 TSX 输出等价 |

---

## 二、迁移策略：模式归纳 + Python 实现

### 2.1 核心思路

120 个 layout 按**视觉结构**归纳为 **15–20 种基础模式**，每种模式实现一个 Python 渲染函数，再通过 `layout_id → 模式` 映射覆盖全部 120 个。

| 模式 | 结构描述 | 典型 layout_id | 数据字段 |
|------|----------|----------------|----------|
| title_slide | 居中标题+副标题 | intro, title | title, subtitle |
| text_image_split | 左图右文 | basic-info, bullet-with-icons | title, bullet_points, image_url |
| three_column_grid | 三列卡片 | toc, grid | title, bullet_points |
| metrics | 指标卡片网格 | metrics, metrics-with-image | title, metrics |
| quote | 引用块+背景 | quote | title, quote |
| team | 成员卡片 | team | title, members |
| chart_bullets | 左图/表右要点 | chart-with-bullets | title, bullet_points |
| numbered_list | 有序列表 | numbered-bullets | title, bullet_points |
| two_column | 双列 | dual, two-column | title, bullet_points |
| contact | 联系信息 | contact | title, contact |
| table | 表+说明 | table-info | title, table, description |
| timeline | 时间线 | timeline | title, events |
| ... | ... | ... | ... |

### 2.2 实施步骤

#### 阶段 1：建立 layout_id → 模式 映射表

**文件**：`nicegui_app/components/slide_layouts/layout_mapping.py`

```python
# 从 template_registry + 命名规则生成
LAYOUT_TO_PREVIEW_TYPE = {
    "basic-info-slide": "text_image_split",
    "bullet-with-icons-slide": "text_image_split",
    "general-intro-slide": "title_slide",
    "metrics-slide": "metrics",
    "metrics-with-image-slide": "metrics",
    "quote-slide": "quote",
    "team-slide": "team",
    "numbered-bullets-slide": "numbered_list",
    "table-of-contents-slide": "three_column_grid",
    "chart-with-bullets-slide": "chart_bullets",
    # ... 其余 100+ 个按规则或手工映射
}
# 未命中时按 layout_id 关键词回退
def get_preview_type(layout_id: str) -> str:
    if layout_id in LAYOUT_TO_PREVIEW_TYPE:
        return LAYOUT_TO_PREVIEW_TYPE[layout_id]
    lid = (layout_id or "").lower()
    if "intro" in lid or "title" in lid: return "title_slide"
    if "metrics" in lid: return "metrics"
    if "quote" in lid: return "quote"
    if "team" in lid: return "team"
    if "toc" in lid or "grid" in lid: return "three_column_grid"
    if "chart" in lid: return "chart_bullets"
    if "numbered" in lid: return "numbered_list"
    if "contact" in lid: return "contact"
    if "table" in lid: return "table"
    return "text_image_split"  # 默认
```

#### 阶段 2：按模式实现 Python 渲染函数

**目录**：`nicegui_app/components/slide_layouts/`

每个模式一个文件，例如 `metrics_slide.py`、`quote_slide.py`，输出 Tailwind HTML 字符串，风格参考 TSX。

**参考 TSX 的方式**：直接打开对应 TSX，复制 `className` 与结构，用 Python f-string 插值：

```python
# metrics_slide.py 参考 MetricsSlideLayout.tsx
def render_metrics_slide(data: dict) -> str:
    title = html.escape(str(data.get("title") or "指标"))
    metrics = data.get("metrics") or [{"label": "", "value": "", "description": ""}]
    # 按 TSX 的 grid/卡片结构输出 HTML
    ...
```

#### 阶段 3：扩展 SlidePreviewData

在 `slide_to_preview_data` 中解析 `metrics`、`quote`、`members`、`contact` 等字段，使 Python 布局能拿到与 TSX 相同结构的数据。

#### 阶段 4：删除 Next.js（可选）

迁移完成且测试通过后，可删除 `PresentationAI/servers/nextjs`，仅保留：
- `PresentationAI/servers/nextjs/app/presentation-templates/` 作为设计参考，或
- 完全删除，仅依赖 `template_registry.json` 与 Python 实现

---

## 三、工作量估算

| 阶段 | 工作量 | 说明 |
|------|--------|------|
| 映射表 | 1–2 天 | 120 个 layout_id → 模式，可半自动从 registry + 命名推断 |
| 新增 10 种模式 | 3–5 天 | 每种约 50–100 行 Python，参考 TSX |
| SlidePreviewData | 0.5 天 | 补充 metrics、quote 等字段解析 |
| 联调与测试 | 1–2 天 | 确保 DESIGN_AGENT 选出的 layout 均有对应预览 |
| **合计** | **约 6–10 天** | 可分批迭代 |

---

## 四、推荐路径

1. **先做映射**：建立完整的 layout_id → 模式映射，未实现模式暂时回退到 `text_image_split`。
2. **按优先级实现**：metrics、quote、team、numbered_list、chart_bullets、contact、table、timeline。
3. **保持 TSX 一段时间**：迁移期间保留 `presentation-templates` 作参考，确认无遗漏后再删。
4. **可选**：写脚本从 TSX 批量抽取 `className` 和结构，辅助生成 Python 模板，减少手写量。

---

## 五、结论

- **可行性**：可以只保留 NiceGUI 一套前端，通过「模式归纳 + Python 实现」迁移 120 个布局。
- **推荐做法**：归纳为 15–20 种模式，逐种用 Python 实现，再用映射表覆盖全部 layout_id。
- **结果**：可删除 Next.js 运行时，仅保留 `presentation-templates` 作设计参考，或完全移除。
