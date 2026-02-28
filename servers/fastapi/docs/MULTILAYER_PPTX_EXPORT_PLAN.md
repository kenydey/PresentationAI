# 多图层可编辑 PPTX 导出 — 现有能力分析与升级实施计划

## 一、需求对照

| 需求项 | 说明 | 现有实现 | 缺口 |
|--------|------|----------|------|
| 遍历 JSON 状态树每页 | 将 slide content 转为 shapes | ✅ `slide_to_pptx_converter._convert()` 遍历 content，生成 shapes 列表 | 无 |
| 配图作为底层背景图层 | rembg 透明图 + `add_picture()` 先插入 | ⚠️ 部分：add_picture 存在，但 (1) 未强制背景抠除 (2) 图层顺序由 shapes 顺序决定，当前可能先文本后图 | 需：1) 启用 remove_background 2) 强制图片先于文本插入 |
| 标题/要点为表层原生文本 | `add_textbox()` 覆盖在图上 | ✅ `add_textbox()` 已实现 | 无 |
| word_wrap = True | 文本框自动换行 | ✅ `services` 版：`textbox.word_wrap = textbox_model.text_wrap` (默认 True) | 无 |
| auto_size = SHAPE_TO_FIT_TEXT | 防止溢出 | ❌ `services/pptx_presentation_creator.py` 未设置 | 需添加 |
| 百分比/相对位置 → Pt/Inches | 坐标转换 | ⚠️ 部分：slide_to_pptx_converter 使用固定逻辑坐标 (W=1280,H=720,PAD=60)，直接作为 Pt；template_registry 无布局坐标定义 | 若未来从 Tailwind/TSX 读取百分比，需新增转换层 |
| FastAPI 端点返回 PPTX 文件流 | 安全下载 | ❌ 当前返回 `path` 字符串，前端用 `get_base_url()+path` 打开；path 多为本地绝对路径，无法直接 HTTP 访问 | 需新增 `FileResponse` 或 `StreamingResponse` 端点 |

---

## 二、现有流程概览

```
export_presentation()
  → convert_presentation_to_pptx_model(slides)
  → PptxPresentationCreator(pptx_model, temp_dir)
  → create_ppt() → fetch_network_assets() → add_and_populate_slide()
  → save(pptx_path)
  → 返回 PresentationAndPath(path=pptx_path)
```

**add_and_populate_slide 顺序**：按 `slide_model.shapes` 顺序依次添加，**先添加的在底层**。当前 `_convert()` 产出顺序多为：title → subtitle → … → image → bullets，即**文本先于图片**，导致图片压住文本，与需求（图在底、文在上）相反。

---

## 三、实施计划

### 步骤 1：图层顺序 — 图片底层、文本表层

**位置**：`utils/slide_to_pptx_converter.py` 或 `services/pptx_presentation_creator.py`

**做法**：在 `add_and_populate_slide` 中，先添加所有 `PptxPictureBoxModel`，再添加 `PptxTextBoxModel` 和 `PptxAutoShapeBoxModel`。

```python
# 伪代码
picture_shapes = [s for s in slide_model.shapes if isinstance(s, PptxPictureBoxModel)]
other_shapes = [s for s in slide_model.shapes if not isinstance(s, PptxPictureBoxModel)]
for s in picture_shapes:
    self.add_picture(slide, s)
for s in other_shapes:
    # add_textbox, add_autoshape, add_connector
```

---

### 步骤 2：配图背景抠除（rembg）

**位置**：`services/pptx_presentation_creator.py` 中 `add_picture()`

**做法**：为配图增加可选 `remove_background` 开关。若 `PptxPictureModel` 支持该字段，则先调用 `image_service.remove_background()`；否则可通过配置或按 layout 类型统一开启。

可选实现：
- 在 `PptxPictureModel` 增加 `remove_background: bool = False`
- 在 `slide_to_pptx_converter._img()` 中根据 layout 或规则设置该字段
- 在 `add_picture` 中若 `remove_background` 为 True，先对 `img_bytes` 调用 `remove_background`，再 `resize_and_crop`

---

### 步骤 3：文本框极限控制 — auto_size

**位置**：`services/pptx_presentation_creator.py` 中 `add_textbox()` 和 `add_autoshape()`

**做法**：

```python
textbox.word_wrap = True
textbox.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
```

需添加：`from pptx.enum.text import MSO_AUTO_SIZE`。

---

### 步骤 4：坐标转换层（可选扩展）

**当前**：`slide_to_pptx_converter` 使用 W=1280、H=720、PAD=60 等固定值，输出即 `PptxPositionModel(left, top, width, height)`，`to_pt_list()` 直接转 Pt。

**若需支持 Tailwind 百分比**：
- 在 `template_registry` 或布局定义中增加坐标 schema（如 `left: "10%", top: "20%", width: "80%"`）
- 新增 `utils/coordinate_converter.py`：`percent_to_pt(percent_str, slide_width_pt)` → 返回 Pt 值
- 在 `slide_to_pptx_converter` 或布局解析阶段调用该转换

当前无百分比定义可暂不实现，预留接口即可。

---

### 步骤 5：PPTX 文件流下载端点

**位置**：`api/v1/ppt/endpoints/presentation.py` 或新建 `files.py`

**做法**：新增端点，根据 `presentation_id` 或 `path` 读取 PPTX 文件，以 `FileResponse` 返回。

```python
from fastapi.responses import FileResponse

@router.get("/export/download/{presentation_id}")
async def download_pptx(presentation_id: UUID, export_as: str = "pptx"):
    # 1. 调用 export_presentation 或直接读取已生成文件
    # 2. 校验 path 在 exports 目录内，避免路径遍历
    # 3. return FileResponse(path, filename="xxx.pptx", media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
```

或改造现有 `/export`：在返回 `PresentationAndPath` 的同时，提供 `download_url` 指向新下载端点，前端通过该 URL 触发下载。

---

### 步骤 6：统一 PptxPresentationCreator 使用方

**现状**：
- `utils/export_utils.py`：使用 `services.pptx_presentation_creator`
- `api/routers/presentation/handlers/export_as_pptx.py`：使用 `ppt_generator.pptx_presentation_creator`（另一实现，含 MSO_AUTO_SIZE）

**建议**：统一改为 `services.pptx_presentation_creator`，并在其中完成所有升级（图层顺序、auto_size、rembg 等），避免双实现不一致。

---

## 四、实施优先级

| 优先级 | 步骤 | 工作量 | 收益 |
|--------|------|--------|------|
| P0 | 步骤 1：图层顺序 | 小 | 图在底、文在上，满足基本可编辑 |
| P0 | 步骤 3：auto_size | 小 | 防止文本溢出 |
| P1 | 步骤 5：下载端点 | 中 | 安全、可靠的文件下载 |
| P2 | 步骤 2：rembg 集成 | 中 | 透明背景图，专业感更强 |
| P3 | 步骤 4：百分比坐标 | 大 | 需布局 schema 配合，可后期迭代 |
| P3 | 步骤 6：统一 Creator | 中 | 降低维护成本 |

---

## 五、文件改动清单

| 文件 | 改动类型 |
|------|----------|
| `services/pptx_presentation_creator.py` | 修改：图层顺序、auto_size、可选 rembg |
| `utils/slide_to_pptx_converter.py` | 可选：为图片设置 `remove_background` |
| `models/pptx_models.py` | 可选：`PptxPictureModel.remove_background` |
| `api/v1/ppt/endpoints/presentation.py` | 新增：`GET /export/download/{id}` 或改造 export 响应 |
| `api/routers/presentation/handlers/export_as_pptx.py` | 可选：改用 services 版 Creator |
| `utils/coordinate_converter.py` | 新建（步骤 4）：百分比 → Pt |
