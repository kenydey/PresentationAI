# HTML/TSX 相关代码分析及正确调用方案

## 一、HTML/TSX 代码存放位置

### 1.1 后端 FastAPI（与 HTML/TSX 生成相关）

| 位置 | 行数 | 内容 |
|------|------|------|
| `api/v1/ppt/endpoints/slide_to_html.py` | **1043** | slide-to-html、html-to-react、html-edit、template-management 四个 Router 的全部逻辑 |
| `api/v1/ppt/endpoints/prompts.py` | 241 | HTML/React 生成的 System Prompt（GENERATE_HTML_SYSTEM_PROMPT、HTML_TO_REACT_SYSTEM_PROMPT、HTML_EDIT_SYSTEM_PROMPT） |
| `models/sql/presentation_layout_code.py` | - | 存储 TSX layout_code 的数据库模型 |
| `utils/template_registry.py` | - | 加载 `assets/template_registry.json`（从 TSX 提取的 layout 元数据） |
| `scripts/extract_templates.py` | ~138 | 从 Next.js TSX 源文件提取 layout 元数据到 template_registry.json |

**合计**：约 **1300+ 行** 与 HTML/TSX 生成与编辑相关，占 endpoints 总行数（4224）约 **25%**。

### 1.2 前端 TSX 布局（PresentationAI 子模块）

项目根目录下 `PresentationAI/servers/nextjs/app/presentation-templates/` 存放 **120+ 个 TSX 布局组件**（neo-modern、general、standard、modern、swift 等），约 **2600+ 行**。这些 TSX 源文件用于：

- `scripts/extract_templates.py` 提取 layout 元数据到 `template_registry.json`
- 原 Next.js 页面直接渲染这些 TSX 作为幻灯片布局

当前主部署为 **NiceGUI**，Next.js 已移除，这些 TSX 不再被运行时渲染，但 `template_registry.json` 仍被 DESIGN_AGENT、get_slide_content、slide_preview 等使用（仅用 layout 的 id、name、json_schema，不执行 TSX 代码）。

---

## 二、在 PPT 生成中的作用

### 2.1 当前主流程（实际在用）

```
用户输入 → RESEARCH_AGENT → DESIGN_AGENT → presentation_state
    → presentation_state_to_outline_and_structure
    → get_slide_content_from_type_and_outline（按 layout json_schema 生成 content JSON）
    → process_slide_and_fetch_assets（图片/图标）
    → export_presentation
        → convert_presentation_to_pptx_model（slide_to_pptx_converter）
        → PptxPresentationCreator
        → .pptx 文件
```

**该流程完全不经由 slide_to_html、html_to_react、html_edit**。PPT 生成仅使用：
- `slide_to_pptx_converter.py`（328 行）
- `services/pptx_presentation_creator.py`
- `template_registry.json`（仅用 layout 的 `json_schema` 做 LLM 输出约束）

### 2.2 HTML/TSX 流程（原设计用途）

```
PPTX 幻灯片截图 + OXML
    → POST /slide-to-html（generate_html_from_slide，LLM 视觉能力）
    → HTML 字符串
    → POST /html-to-react（generate_react_component_from_html）
    → TSX React 组件代码
    → 保存到 PresentationLayoutCodeModel（layout_code 字段）
    → 用户在前端编辑 HTML → POST /html-edit（AI 修改）
```

**设计目的**：为「自定义模板」提供可视化编辑——从已有 PPT 截图反推 HTML/TSX，再人工或 AI 编辑，最终作为可复用布局。

---

## 三、是否被正确调用

### 3.1 结论：**未被调用**

| API | 原调用方 | 当前状态 |
|-----|----------|----------|
| `POST /slide-to-html` | Next.js `useSlideProcessing.ts` | Next.js 已移除，**无前端调用** |
| `POST /html-to-react` | Next.js `useLayoutSaving.ts` | **无前端调用** |
| `POST /html-edit` | Next.js `useSlideEdit.ts` | **无前端调用** |
| `template-management/*` | Next.js custom-template | 仅 `summary`、`get-templates`、`delete-templates` 被 NiceGUI templates_mgmt 使用；**save_layouts**（存 TSX）未被触发 |

### 3.2 验证

- `nicegui_app/` 下无 `slide-to-html`、`html-to-react`、`html-edit` 调用
- PPT 导出路径不经过上述任一接口
- `template-management/save` 仅在设计「保存自定义 TSX 布局」时使用，当前 NiceGUI 无对应功能

---

## 四、如何正确调用（实施方案）

### 方案 A：在 NiceGUI 中实现「自定义模板编辑」流程（完整对接）

在 `/ui/templates` 或新增 `/ui/custom-template` 页面实现：

1. **从 PPTX 导入**  
   - 调用 `POST /pptx-slides/process` 得到幻灯片截图与 XML  
   - 对每个 slide 调用 `POST /slide-to-html`，得到 HTML  

2. **HTML → TSX**  
   - 用户确认 HTML 后，调用 `POST /html-to-react` 生成 TSX  

3. **保存布局**  
   - 调用 `POST /template-management/save`，将 TSX 写入 `PresentationLayoutCodeModel`  

4. **AI 编辑**  
   - 提供输入框，用户输入自然语言指令，调用 `POST /html-edit`，用 AI 修改 HTML  

**优点**：完整恢复原 Next.js custom-template 能力  
**缺点**：实现量大，依赖 OpenAI Responses API（gpt-5 等），需重写/移植 Next.js 的 UI 与交互

---

### 方案 B：将 HTML 能力用于「单页可视化编辑」（简化版）

在 viewer 页面增强：

1. **单页截图转 HTML**  
   - 对当前页渲染结果（或服务端生成截图）调用 `POST /slide-to-html`  
   - 用 `ui.html()` 展示返回的 HTML，支持预览  

2. **自然语言修改**  
   - 用户输入指令，调用 `POST /html-edit`  
   - 将返回的 HTML 写回当前页预览  

3. **不生成 TSX**  
   - 不调用 html-to-react，不落库 layout_code  
   - 仅用于实时编辑与预览  

**优点**：改动小，能利用现有 slide-to-html、html-edit  
**缺点**：编辑结果不自动沉淀为可复用模板

---

### 方案 C：保留为纯 API，供外部或未来使用

- 保持现有实现，不接 NiceGUI  
- 在 `/docs` 中补充说明这些 API 的用途与调用示例  
- 供未来 Electron、CLI 或外部集成使用  

---

### 方案 D：将 layout_code 纳入 PPT 导出（若已存在）

若 `PresentationLayoutCodeModel` 中已有针对某 presentation 的 layout_code：

- 在 `slide_to_pptx_converter` 或 `pptx_presentation_creator` 中，优先使用 layout_code 描述的布局信息  
- 当前实现未读取 layout_code，仅用固定坐标逻辑  

该方案需要对 TSX/React 服务端渲染或逻辑层做较大改造，建议单独评估。

---

## 五、推荐实施顺序

| 优先级 | 方案 | 工作量 | 建议 |
|--------|------|--------|------|
| 1 | **方案 B** | 中 | 在 viewer 增加「当前页 → HTML 预览 + AI 编辑」，快速打通 slide-to-html、html-edit |
| 2 | **方案 A** | 高 | 若有完整自定义模板需求，再实现完整导入→HTML→TSX→保存流程 |
| 3 | **方案 C** | 低 | 无论如何，补充 API 文档，明确用途与调用方式 |
| 4 | **方案 D** | 高 | 视业务需求决定是否在导出链路中使用 layout_code |

---

## 六、Presenton 原项目的 HTML/TSX 质量保障机制（重要借鉴）

### 6.1 原 Presenton 的导出流程

```
用户编辑的幻灯片（由 TSX/React + Tailwind 渲染为 HTML）
    → 前端打开 /pdf-maker?id={presentation_id} 页面
    → Puppeteer 无头浏览器访问该页面
    → 遍历 #presentation-slides-wrapper 下每页 DOM
    → getElementAttributes()：读取每元素 computed style（position、font、background、shadow、border 等）
    → convertElementAttributesToPptxSlides()：将 DOM 属性转为 PptxPresentationModel.shapes
    → 对 img/canvas/table 等元素做截图，其余用原生文本/形状
    → 返回 PptxPresentationModel 给后端生成 .pptx
```

**关键点**：PPT 的视觉质量来源于 **已渲染的 HTML**，而不是固定坐标逻辑。TSX 布局（含 Tailwind）负责排版与样式，导出时通过 **采样渲染结果** 获得精确的位置、字体、颜色、阴影等。

### 6.2 当前复刻项目与原版的差异

| 环节       | 原 Presenton                         | 当前项目（NiceGUI 版）                     |
|------------|--------------------------------------|--------------------------------------------|
| 幻灯片展示 | TSX/React + Tailwind 渲染 HTML       | NiceGUI `slide_preview` 的 Tailwind HTML   |
| 导出数据源 | Puppeteer 采样渲染后的 DOM           | `slide_to_pptx_converter` 根据 JSON 用固定坐标 |
| 布局信息   | 来自 TSX 的 computed style          | W=1280、H=720、PAD=60 等固定逻辑            |

因此，**原版的高质量主要来自「所见即所得」：HTML 渲染什么样，导出就按什么样采样**。

---

## 七、HTML/TSX 能否扮演二次编辑提升角色？可借鉴价值

### 7.1 结论：可以，且有明确借鉴价值

1. **二次编辑**：slide-to-html、html-edit 可在用户对单页内容做「自然语言修改」时提供 AI 编辑能力，但当前未被调用。
2. **质量提升**：原 Presenton 的高质量来自 **「HTML 渲染 → Puppeteer 采样 → PPT 导出」** 这套链路，而不是 slide-to-html 接口本身。真正有用的是：**以渲染后的 HTML 作为导出的数据源**。

### 7.2 可借鉴的三条路径

| 路径 | 思路 | 工作量 | 效果 |
|------|------|--------|------|
| **E：Puppeteer 采样现有预览** | 在导出时，用 Puppeteer 访问 NiceGUI 的 viewer 预览页，采样 DOM 转 PptxPresentationModel | 中 | 高，接近原版「所见即所得」 |
| **F：桥接预览输出到 converter** | 让 `slide_preview` 在渲染时输出结构化布局 JSON（位置、字体等），`slide_to_pptx_converter` 消费该 JSON | 中 | 中高，无需 Puppeteer，但需改造预览组件 |
| **G：复用 presentation_to_pptx_model 路由** | 保留/移植 Next.js 的 `presentation_to_pptx_model` API，用 Puppeteer 访问 pdf-maker 或等效预览页 | 高 | 高，完全沿用原版流程 |

### 7.3 推荐顺序

1. **方案 E**：在 FastAPI 侧增加「Puppeteer 采样 viewer 预览」的导出分支，作为可选高质量导出路径。
2. **方案 F**：让 slide_preview 输出布局 JSON，逐步替代固定坐标逻辑。
3. **方案 B**：打通 slide-to-html、html-edit，用于单页的 AI 二次编辑（提升交互，对导出质量是间接帮助）。

---

## 八、小结

1. **存放位置**：HTML/TSX 相关逻辑集中在 `slide_to_html.py`（约 1043 行）及 `prompts.py` 中的生成提示。
2. **在 PPT 生成中的角色**：当前主流程不走 HTML；原 Presenton 中，**HTML 渲染是导出的质量基石**，通过 Puppeteer 采样 DOM 实现「所见即所得」。
3. **调用情况**：Next.js 移除后，slide-to-html、html-to-react、html-edit 均无前端调用。
4. **借鉴价值**：原版的高质量来自 **「TSX 渲染 → Puppeteer 采样 DOM → 转 PPT 模型」**，可借鉴实现方案 E 或 F，将 HTML/TSX 的渲染结果纳入导出链路。

---

## 九、方案 E 实施完成（Playwright DOM 采样）

已按方案 E 完成实现：

- **导出预览页**：`/ui/export-view?id={presentation_id}`，渲染所有幻灯片于 `#presentation-slides-wrapper`
- **DOM 采样服务**：`services/dom_sampling_export_service.py`，使用 Playwright 访问预览页、提取元素属性、转为 PptxPresentationModel
- **导出集成**：`export_presentation(..., use_dom_sampling=True)`，仪表板提供「高质量 PPTX」按钮
- **环境变量**：`EXPORT_PREVIEW_BASE_URL` 默认 `http://127.0.0.1:8000`，Docker/反向代理时需显式设置
