# 表格、图表、Markdown 功能实现可行性方案

> 目标：表格与图表在 PowerPoint 中为**原生可编辑**，图表可二次编辑，优先选用 Python 现有依赖库方案。

---

## 零、可行性总结

| 维度 | 结论 | 说明 |
|------|------|------|
| **依赖** | ✅ 可行 | 仅用现有 `python-pptx>=1.0.2`，无需新增任何 Python 包 |
| **表格** | ✅ 可行 | `slide.shapes.add_table()` 生成原生表格，PowerPoint 中可编辑单元格 |
| **图表** | ✅ 可行 | `slide.shapes.add_chart()` 生成原生 Chart，支持柱状/折线/饼图等，数据可编辑 |
| **Markdown** | ✅ 可行 | 扩展 MIME + 前端 accept 即可，无新依赖 |
| **风险** | 低 | python-pptx 文档完善，项目内已有 `ppt_generator` 图表实现可参考 |

**总体结论**：全部功能在现有依赖下均可实现，且均为 PowerPoint 原生效果，图表可编辑。推荐采用渐进式实施方案。

---

## 一、技术选型概览

| 能力 | 推荐依赖 | 原生效果 | 可编辑性 | 备注 |
|------|----------|----------|----------|------|
| **表格** | python-pptx（已有） | ✅ 完全原生 | ✅ 单元格可编辑 | `slide.shapes.add_table()` |
| **柱状图/饼图/折线图** | python-pptx（已有） | ✅ 完全原生 | ✅ 数据可编辑 | `slide.shapes.add_chart()` |
| **Markdown 文件** | 无新增 | - | - | 扩展 MIME 与前端 accept |

**结论**：表格与图表均可完全基于 **python-pptx** 实现，无需新增 Python 依赖，均为 PowerPoint 原生对象，支持二次编辑。

---

## 二、方案 A：纯 python-pptx 全原生方案（推荐）

### 2.1 核心思路

- **表格**：使用 `slide.shapes.add_table(rows, cols, left, top, width, height)`，生成原生表格，通过 `table.cell(r,c).text` 写入内容。
- **图表**：使用 `slide.shapes.add_chart(chart_type, left, top, width, height, chart_data)`，复用项目内 `ppt_generator` 已有的 ChartData 构建逻辑。

### 2.2 新增模型（`models/pptx_models.py`）

```python
# 表格模型
class PptxTableCellModel(BaseModel):
    text: str = ""
    font: Optional[PptxFontModel] = None

class PptxTableBoxModel(PptxShapeModel):
    shape_type: Literal["table"] = "table"
    position: PptxPositionModel
    headers: List[str]  # 表头
    rows: List[List[str]]  # 数据行

# 图表模型 - 复用 graph_processor 的 GraphModel 或定义简化版
class PptxChartBoxModel(PptxShapeModel):
    shape_type: Literal["chart"] = "chart"
    position: PptxPositionModel
    chart_type: Literal["bar", "line", "pie"]
    title: Optional[str] = None
    categories: List[str]
    series: List[dict]  # [{"name": str, "data": List[float]}]
```

### 2.3 `services/pptx_presentation_creator.py` 新增方法

```python
def add_table(self, slide: Slide, model: PptxTableBoxModel):
    rows = 1 + len(model.rows)  # 表头 + 数据
    cols = len(model.headers)
    shape = slide.shapes.add_table(
        rows, cols,
        Pt(model.position.left), Pt(model.position.top),
        Pt(model.position.width), Pt(model.position.height)
    )
    table = shape.table
    for c, h in enumerate(model.headers):
        table.cell(0, c).text = h
    for r, row in enumerate(model.rows):
        for c, cell_text in enumerate(row[:cols]):
            table.cell(r+1, c).text = str(cell_text)

def add_chart(self, slide: Slide, model: PptxChartBoxModel):
    from pptx.chart.data import ChartData
    from pptx.enum.chart import XL_CHART_TYPE
    chart_data = ChartData()
    chart_data.categories = model.categories
    for s in model.series:
        chart_data.add_series(s["name"], s["data"])
    type_map = {"bar": XL_CHART_TYPE.COLUMN_CLUSTERED, "line": XL_CHART_TYPE.LINE, "pie": XL_CHART_TYPE.PIE}
    slide.shapes.add_chart(type_map[model.chart_type], *model.position.to_pt_list(), chart_data)
```

### 2.4 `slide_to_pptx_converter` 修改

- 遇到 `table` / `tableData` 等：解析 `headers` + `rows`，生成 `PptxTableBoxModel`，加入 `shapes`。
- 遇到 `chart` / `chartData`：解析 `type`、`categories`、`series`，生成 `PptxChartBoxModel`。

### 2.5 依赖

- **无新增**，仅用现有 `python-pptx>=1.0.2`。

### 2.6 优缺点

| 优点 | 缺点 |
|------|------|
| 无新依赖 | 需在 services 中实现图表逻辑 |
| 表格、图表均为原生，可二次编辑 | 图表样式需自行封装（字体、图例等） |
| 与现有 `PptxPresentationCreator` 风格一致 | - |

---

## 三、方案 B：复用 ppt_generator 图表逻辑，统一导出入口

### 3.1 核心思路

- **图表**：直接复用 `ppt_generator/pptx_presentation_creator.py` 中的 `add_graph()`、`ChartData`、`GraphModel` 等实现。
- **表格**：在 `services/pptx_presentation_creator.py` 中新增 `add_table()`（方案 A 的表格逻辑）。

### 3.2 实现方式

1. **统一 PptxPresentationCreator**：让 `utils/export_utils.py` 使用 `ppt_generator` 的 creator，或把 `ppt_generator` 的 chart 相关方法移植到 `services/pptx_presentation_creator.py`。
2. **PptxSlideModel 支持新 shape 类型**：在 `PptxSlideModel.shapes` 的 Union 中加入 `PptxTableBoxModel`、`PptxGraphBoxModel`（或 `PptxChartBoxModel`）。
3. **slide_to_pptx_converter**：将 JSON 中 chart/table 转为 `GraphModel`（图表）或 `PptxTableBoxModel`（表格）。

### 3.3 数据格式映射

LLM / 内容 JSON 的 chart 格式示例：

```json
{
  "chart": {
    "type": "bar",
    "title": "销售数据",
    "categories": ["Q1", "Q2", "Q3", "Q4"],
    "series": [
      {"name": "产品A", "data": [120, 180, 150, 200]},
      {"name": "产品B", "data": [80, 95, 110, 130]}
    ]
  }
}
```

映射到 `graph_processor.models.GraphModel` / `BarGraphDataModel`：

```python
GraphModel(
    name=val["title"],
    type=GraphTypeEnum.bar,
    data=BarGraphDataModel(
        categories=val["categories"],
        series=[BarSeriesModel(name=s["name"], data=s["data"]) for s in val["series"]]
    )
)
```

### 3.4 依赖

- **无新增**，使用现有 `graph_processor`、`ppt_generator`。

### 3.5 优缺点

| 优点 | 缺点 |
|------|------|
| 图表逻辑已存在，样式较完善 | ppt_generator 与 services 两套 creator 需统一/选一 |
| 支持 bar/line/pie/scatter/bubble | 需处理 `ppt_generator` 与 `services` 的模型差异 |
| 表格可单独按方案 A 实现 | - |

---

## 四、方案 C：渐进式混合方案（分阶段实施）

### 4.1 阶段划分

| 阶段 | 内容 | 工作量 | 优先级 |
|------|------|--------|--------|
| **1** | 表格：PptxTableBoxModel + add_table | 小 | 高 |
| **2** | 图表：复用 ppt_generator 的 add_chart 逻辑 | 中 | 高 |
| **3** | 内容生成：扩展 Schema，让 LLM 输出 table/chart | 中 | 高 |
| **4** | Markdown 文件上传 | 小 | 中 |

### 4.2 阶段 1：表格

1. 在 `models/pptx_models.py` 中增加 `PptxTableBoxModel`。
2. 在 `services/pptx_presentation_creator.py` 中实现 `add_table()`，调用 `slide.shapes.add_table()`。
3. 在 `slide_to_pptx_converter` 中，对 `_TABLE_KEYS` 生成 `PptxTableBoxModel` 而非文本框。
4. 在 `PptxSlideModel.shapes` 的 Union 中加入 `PptxTableBoxModel`。

### 4.3 阶段 2：图表

1. 在 `services/pptx_presentation_creator.py` 中实现 `add_chart()`，逻辑参考 `ppt_generator` 的 `add_graph`。
2. 在 `models/pptx_models.py` 中增加 `PptxChartBoxModel`（或直接引入 `PptxGraphBoxModel`）。
3. 在 `slide_to_pptx_converter` 中，对 `_CHART_KEYS` 解析并生成 chart shape。
4. 支持 `bar`、`line`、`pie` 三种基础类型。

### 4.4 阶段 3：内容生成

1. 在 `PresentationState` / `SlideState` 中增加可选字段：`table_data`、`chart_data`。
2. 在 RESEARCH_AGENT prompt 中说明：数据类内容应输出结构化 table/chart 数据。
3. 在 `get_slide_content_from_type_and_outline` 使用的 layout json_schema 中，为 chart/table 布局增加对应字段定义。
4. 在 `state_mapper` 或后续 pipeline 中，将 `table_data`/`chart_data` 写入 slide content。

### 4.5 阶段 4：Markdown 文件

1. 在 `constants/documents.py` 中增加 `TEXT_MIME_TYPES = ["text/plain", "text/markdown"]`。
2. 在 `create.py` 的 `ui.upload` 中增加 `.md`。
3. 在 `DocumentsLoader` 中，对 `text/markdown` 走 `load_text` 流程（按纯文本/Markdown 解析均可）。

---

## 五、LLM 输出格式规范

为让表格和图表可被正确解析，需约定 LLM 输出的 JSON 结构。

### 5.1 表格

```json
{
  "title": "季度对比",
  "table": {
    "headers": ["指标", "Q1", "Q2", "Q3", "Q4"],
    "rows": [
      ["收入(万)", "120", "150", "180", "210"],
      ["成本(万)", "80", "95", "110", "125"]
    ]
  }
}
```

### 5.2 图表

```json
{
  "title": "销售趋势",
  "chart": {
    "type": "bar",
    "title": "季度销售",
    "categories": ["Q1", "Q2", "Q3", "Q4"],
    "series": [
      {"name": "产品A", "data": [120, 180, 150, 200]},
      {"name": "产品B", "data": [80, 95, 110, 130]}
    ]
  }
}
```

`type` 支持：`bar`、`line`、`pie`。

---

## 六、方案对比与推荐

| 维度 | 方案 A | 方案 B | 方案 C |
|------|--------|--------|--------|
| **新增依赖** | 无 | 无 | 无 |
| **实现复杂度** | 中 | 中高（需统一两套 creator） | 低（分步实施） |
| **表格原生可编辑** | ✅ | ✅ | ✅ |
| **图表原生可编辑** | ✅ | ✅ | ✅ |
| **图表样式** | 需自实现 | 可直接复用 | 分阶段完善 |
| **可维护性** | 高（逻辑集中） | 中（两套代码） | 高（渐进式） |

**推荐**：

- **首选**：**方案 C**（渐进式），先做表格，再做图表，最后扩展内容生成与 Markdown。
- **若希望一次性打通**：采用**方案 A**，在 `services/pptx_presentation_creator.py` 中完整实现表格与图表，逻辑集中、易维护。

---

## 七、Markdown 文件支持（独立子项）

| 步骤 | 修改位置 | 内容 |
|------|----------|------|
| 1 | `constants/documents.py` | `TEXT_MIME_TYPES = ["text/plain", "text/markdown"]` |
| 2 | `api/v1/ppt/endpoints/files.py` | 上传校验增加 `text/markdown`（若按 content_type 校验） |
| 3 | `nicegui_app/pages/create.py` | `accept='.pdf,.docx,.doc,.txt,.pptx,.md'` |
| 4 | `services/documents_loader.py` | 对 `text/markdown` 调用 `load_text()` |

**依赖**：无新增。部分环境下 `.md` 的 MIME 可能为 `text/x-markdown`，可一并加入 `TEXT_MIME_TYPES` 或做兼容判断。

---

## 八、现有依赖验证（pyproject.toml）

```toml
"python-pptx>=1.0.2"  # 已存在，支持：
# - slide.shapes.add_table(rows, cols, left, top, width, height) → 原生表格
# - slide.shapes.add_chart(chart_type, left, top, width, height, chart_data) → 原生图表
# - XL_CHART_TYPE: COLUMN_CLUSTERED(柱状), LINE(折线), PIE(饼图), XY_SCATTER(散点) 等
```

项目内已有 `ppt_generator/pptx_presentation_creator.py` 的 `add_graph()` 实现，可作为图表逻辑参考，无需引入新库。

---

## 九、参考资料

- [python-pptx Tables](https://python-pptx.readthedocs.io/en/stable/user/table.html)
- [python-pptx Charts](https://python-pptx.readthedocs.io/en/stable/user/charts.html)
- 项目内：`ppt_generator/pptx_presentation_creator.py`（add_graph）、`graph_processor/models.py`（GraphModel）
