# 演示查看 — 基于 PresentationState 的实时预览组件实施计划

## 一、目标

在演示查看页面（`/ui/viewer`）实现：
1. 基于 `PresentationState` / `SlideState` 的 JSON 结构渲染预览
2. 使用 NiceGUI 动态生成 HTML + Tailwind 实用类
3. 三种基础版式：`title_slide`、`text_image_split`、`three_column_grid`
4. 16:9 固定比例容器
5. **后端 JSON 更新时无刷新实时渲染**

---

## 二、数据流与映射

### 2.1 数据来源

| 场景 | 数据源 | 结构 |
|------|--------|------|
| 演示查看（已生成） | `GET /api/v1/ppt/presentation/{id}` | `slides[]`，每项为 `SlideModel`（`content` dict + `layout`） |
| 大纲编辑 / 创建（未来） | RESEARCH + DESIGN Agent | `PresentationState`（`slides[]` 为 `SlideState`） |

### 2.2 统一预览输入格式

定义 **`SlidePreviewData`**（前端内部结构），与 `SlideState` 对齐，便于复用：

```python
# 类型定义（非 Pydantic，仅作说明）
{
    "title": str,
    "bullet_points": List[str],   # 0–8 条
    "image_prompt": Optional[str],
    "image_url": Optional[str],  # 若已生成图片，直接使用
    "layout_id": str,            # 用于选择版式
}
```

### 2.3 映射逻辑

**从 API 的 slide（content dict）→ SlidePreviewData：**

```python
# 伪代码
title = content.get("title") or content.get("heading") or content.get("headline") or ""
bullets = content.get("bullets") or content.get("items") or content.get("points") or []
bullet_points = [b if isinstance(b, str) else b.get("text", b.get("title", "")) for b in bullets[:8]]
image_prompt = content.get("imagePrompt") or content.get("image_description") or ""
image_url = (content.get("image") or {}).get("__image_url__") or (content.get("image") or {}).get("url") or ""
layout_id = slide.layout or "basic-info-slide"  # 来自 SlideModel.layout
```

**layout_id → 预览版式类型：**

| layout_id 模式 / 关键词 | 使用版式 |
|-------------------------|----------|
| `*intro*`, `*title*`, `general-intro-slide` | `title_slide` |
| `*toc*`, `*grid*`, `*three*`, `*column*` | `three_column_grid` |
| 其他 | `text_image_split` |

---

## 三、三种基础版式设计

### 3.1 title_slide（居中标题封面）

- 16:9 容器内垂直居中
- 主标题：大号、加粗、居中
- 可选副标题：较小字号、居中、灰色
- 无 bullets、无图片占位（或极简背景）

**Tailwind 结构示意：**
```
flex flex-col items-center justify-center min-h-full bg-gradient-to-br from-indigo-500 to-purple-600
  └─ h1.text-4xl.font-bold.text-white (主标题)
  └─ p.text-lg.text-white/80 (副标题，可选)
```

### 3.2 text_image_split（左图右文）

- 左右分栏：约 40% 图 / 60% 文
- 左侧：图片（有 `image_url` 则显示，否则占位 + `image_prompt` 文本）
- 右侧：标题 + 要点列表（bullet_points）
- 响应式：小屏可上下堆叠

**Tailwind 结构示意：**
```
flex flex-row gap-6 p-6 (或 grid grid-cols-[2fr_3fr])
  └─ div (左): aspect-video bg-gray-200 rounded-lg overflow-hidden
       └─ img 或 div.placeholder + image_prompt
  └─ div (右): flex flex-col gap-4
       └─ h2.text-2xl.font-bold
       └─ ul.list-disc (bullet_points)
```

### 3.3 three_column_grid（三列卡片布局）

- 三列等宽
- 每列：小标题 + 若干要点（将 bullet_points 均分或取前 3 条）
- 可选：每列顶部小图标或数字
- 适合目录、要点对比、三步流程等

**Tailwind 结构示意：**
```
grid grid-cols-3 gap-6 p-6
  └─ 每列: rounded-lg border bg-white p-4 shadow-sm
       └─ h3.text-lg.font-semibold (或序号)
       └─ ul.text-sm.space-y-1 (要点)
```

---

## 四、技术实现方案

### 4.1 前端模块划分

```
nicegui_app/
├── components/
│   ├── __init__.py
│   ├── slide_preview.py       # 预览组件入口
│   └── slide_layouts/         # 三种版式
│       ├── __init__.py
│       ├── title_slide.py     # 生成 title_slide 的 HTML 字符串
│       ├── text_image_split.py
│       └── three_column_grid.py
```

### 4.2 渲染方式

- 使用 **`ui.html()`** 输出完整 HTML 片段
- 所有样式使用 **Tailwind 实用类**（NiceGUI 默认集成 Tailwind v3）
- 通过 **`.content = new_html`** 更新，实现无刷新重渲染
- 容器：固定 `aspect-ratio: 16/9`，`max-width` 控制可视宽度

### 4.3 实时更新机制

| 触发场景 | 更新方式 |
|----------|----------|
| 切换幻灯片（点击列表） | `show_slide(idx)` 内：`preview_html.content = render_slide_html(slide_data)` |
| 加载新演示 | `load_pres()` 后调用 `show_slide(0)` |
| 未来：VIBE_EDITOR 更新 | 拿到新 `PresentationState` → 转为 `SlidePreviewData[]` → 更新 `preview_html.content` |

核心：**不刷新整页，只更新 `ui.html` 的 `content` 属性**。

### 4.4 layout_id → 版式映射

```python
def get_preview_layout_type(layout_id: str) -> str:
    lid = (layout_id or "").lower()
    if "intro" in lid or "title" in lid or lid in ("general-intro-slide",):
        return "title_slide"
    if "toc" in lid or "grid" in lid or "three" in lid or "column" in lid:
        return "three_column_grid"
    return "text_image_split"
```

---

## 五、实施步骤

| 步骤 | 任务 | 产出 |
|------|------|------|
| 1 | 创建 `slide_preview_data.py`：API slide → SlidePreviewData 映射函数 | `servers/fastapi/nicegui_app/utils/slide_preview_data.py` |
| 2 | 创建 `slide_layouts/`：三种版式的 HTML 渲染函数（入参：SlidePreviewData，返回 HTML 字符串） | `title_slide.py`, `text_image_split.py`, `three_column_grid.py` |
| 3 | 创建 `slide_preview.py`：统一入口 `render_slide_preview_html(data, layout_type)` + `get_preview_layout_type(layout_id)` | `components/slide_preview.py` |
| 4 | 在 viewer 页面：用 16:9 容器 + `ui.html` 替换现有 preview_display，改为调用 `render_slide_preview_html` | 修改 `pages/viewer.py` |
| 5 | 确保 `show_slide` 仅更新 `preview_html.content`，不触达整页刷新 | 验证无刷新 |
| 6 | （可选）为 HTML 引入内联 Tailwind 安全策略，或确认 `sanitize=False` 下 Tailwind 类正常生效 | 测试样式 |

---

## 六、安全与兼容

- `ui.html(..., sanitize=False)`：Tailwind 类需保留，但需避免用户输入未转义注入
- 所有文本内容使用 `html.escape()` 后插入 HTML
- 图片 URL 需校验为 `https?://` 或相对路径，避免 `javascript:` 等

---

## 七、后续扩展

1. **创建/大纲页面**：在生成大纲后展示 `PresentationState` 预览，支持 VIBE_EDITOR 编辑后实时刷新
2. **扩展版式**：将 `template_registry.json` 中更多 layout_id 映射到新布局
3. **主题/配色**：通过 CSS 变量或 Tailwind 主题扩展支持多套配色
