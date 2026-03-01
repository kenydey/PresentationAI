# 图像处理中间件 (image_service) 实施计划

## 一、目标

实现企业级图像预处理与背景抠除中间件 `image_service.py`，供 PPT 生成工作流使用：

1. **resize_and_crop**：Lanczos 等比例缩放 + 居中硬裁剪，无留白
2. **remove_background**：基于 rembg 的精准背景抠除，输出带透明通道的 PNG
3. 所有输出返回 `io.BytesIO()`，避免落盘

---

## 二、API 设计

### 2.1 `resize_and_crop(image_bytes: bytes, target_width: int, target_height: int) -> io.BytesIO`

| 步骤 | 说明 |
|------|------|
| 1 | 使用 Pillow 打开 `image_bytes` |
| 2 | 计算最大缩放因子：`scale = max(target_w/w, target_h/h)`，确保缩放后至少一条边等于目标，另一条边不小于目标（保证覆盖无留白） |
| 3 | 使用 `Image.LANCZOS`（PIL 9.1+ 为 `Image.Resampling.LANCZOS`）等比例缩放 |
| 4 | 居中裁剪：从缩放后图像中心取 `target_width × target_height` 区域 |
| 5 | 输出格式：PNG（支持透明通道）或 JPEG（无透明时），写入 `BytesIO` 并 `seek(0)` 返回 |

### 2.2 `remove_background(image_bytes: bytes) -> io.BytesIO`

| 步骤 | 说明 |
|------|------|
| 1 | 使用 `from rembg import remove`，传入 `Image.open(io.BytesIO(image_bytes))` |
| 2 | rembg 返回 RGBA 图像，背景为透明 |
| 3 | 保存为 PNG 到 `BytesIO`，`seek(0)` 返回 |

---

## 三、依赖

| 依赖 | 用途 | 备注 |
|------|------|------|
| Pillow | 缩放、裁剪、格式转换 | 项目已有（通过 docling 等） |
| rembg | 背景抠除 | 需新增至 `pyproject.toml` |

```toml
# pyproject.toml 新增
"Pillow>=10.0.0",
"rembg>=2.0.0",
```

---

## 四、集成位置

### 4.1 当前 PPT 图片流程

```
ImageGenerationService.generate_image()
    → 返回 path (本地) 或 URL
process_slide_and_fetch_assets()
    → 设置 slide.content.__image_url__
PptxPresentationCreator.fetch_network_assets()
    → 下载 URL 到 temp_dir，path 改为本地
PptxPresentationCreator.add_picture(slide, picture_model)
    → Image.open(path)，可选 clip/fit/radius，保存到 temp，add_picture(path)
```

### 4.2 集成点

**推荐位置**：`PptxPresentationCreator.add_picture()` 内部，在打开图片后、应用 clip/fit 之前。

| 顺序 | 操作 |
|------|------|
| 1 | 读取图片：`path` → `bytes`（若为 URL 已下载则为本地 path） |
| 2 | **[NEW] 可选**：若 `picture_model.remove_background` 为 True，调用 `remove_background(bytes)` |
| 3 | **[NEW]**：调用 `resize_and_crop(bytes, position.width, position.height)`，统一预处理为目标尺寸 |
| 4 | 原有逻辑：border_radius、shape（circle）、invert、opacity、object_fit（若仍有需要可简化） |
| 5 | `slide.shapes.add_picture(stream, left, top, width, height)`，传入 `BytesIO`（`.seek(0)`） |

### 4.3 模型扩展（可选）

如需按图控制背景抠除，可在 `PptxPictureModel` 增加字段：

```python
# models/pptx_models.py
remove_background: bool = False  # 是否对该图执行背景抠除
```

若暂不扩展模型，可对所有配图统一执行 `resize_and_crop`，背景抠除可通过配置或后续迭代按需开启。

---

## 五、实施步骤

| 步骤 | 任务 | 产出 |
|------|------|------|
| 1 | 新增 `rembg`、确保 `Pillow` 依赖 | `pyproject.toml` |
| 2 | 实现 `services/image_service.py`：`resize_and_crop`、`remove_background` | `image_service.py` |
| 3 | 在 `PptxPresentationCreator.add_picture` 中集成：读取 → resize_and_crop → （可选）remove_background → add_picture(stream) | 修改 `services/pptx_presentation_creator.py` |
| 4 | （可选）扩展 `PptxPictureModel` 支持 `remove_background` 开关 | 修改 `models/pptx_models.py`、`utils/slide_to_pptx_converter.py` |
| 5 | 单元测试：`resize_and_crop`、`remove_background` 输入输出校验 | `tests/test_image_service.py` |

---

## 六、实现细节

### 6.1 resize_and_crop 算法

```python
# 伪代码
w, h = img.size
scale = max(target_width / w, target_height / h)
new_w = int(w * scale)
new_h = int(h * scale)
resized = img.resize((new_w, new_h), Image.LANCZOS)
left = (new_w - target_width) // 2
top = (new_h - target_height) // 2
cropped = resized.crop((left, top, left + target_width, top + target_height))
# 输出到 BytesIO
```

### 6.2 边界与异常

- `target_width` 或 `target_height` ≤ 0：抛出 `ValueError`
- 图片无法解码：捕获并抛出明确异常或返回 `None`
- rembg 首次调用会下载模型（~200MB），可考虑在服务启动时预加载

---

## 七、与现有 image_utils 的关系

- `utils/image_utils.py` 已有 `clip_image`、`fit_image` 等，基于 PIL Image 对象。
- `resize_and_crop` 与 `clip_image` 行为类似（等比例缩放+居中裁剪），但：
  - `resize_and_crop` 接收/返回 **bytes/BytesIO**，便于无落盘流水线
  - 作为统一预处理入口，可替代部分 `clip_image` 使用场景
- 集成时优先使用 `image_service.resize_and_crop`，原有 `clip_image` 在无特殊需求时可逐步收敛。
