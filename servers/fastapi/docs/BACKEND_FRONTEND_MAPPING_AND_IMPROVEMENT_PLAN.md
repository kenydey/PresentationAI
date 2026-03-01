# Presentation AI 后端-前端对应关系与完善方案

## 一、架构概览

- **后端**: FastAPI（`api/v1/ppt/`），前缀 `/api/v1/ppt`
- **前端**: NiceGUI（`nicegui_app/`），挂载于 `/ui`
- **通信**: `api_client.py` 中的 `api_get`、`api_post`、`api_patch`、`api_delete`、`api_post_form`、`api_stream_sse`

---

## 二、后端-前端对应关系总表

| 后端模块/路由 | 完整 API 路径 | 前端页面 | 前端调用 | 状态 |
|---------------|---------------|----------|----------|------|
| **Presentation** | `/api/v1/ppt/presentation/*` | dashboard, create, outline, viewer | ✅ | 已对接 |
| **Files** | `/api/v1/ppt/files/*` | create | ✅ | 已对接 |
| **Fonts** | `/api/v1/ppt/fonts/*` | fonts | ✅ | 已对接 |
| **Outlines** | `/api/v1/ppt/outlines/*` | outline | ✅ | 已对接 |
| **Slide** | `/api/v1/ppt/slide/*` | viewer | ✅ | 已对接 |
| **Images** | `/api/v1/ppt/images/*` | images | ✅ | 已对接 |
| **Icons** | `/api/v1/ppt/icons/*` | icons | ✅ | 已对接 |
| **Layouts** | `/api/v1/ppt/layouts/*` | outline | ✅ | 已对接 |
| **Template Management** | `/api/v1/ppt/template-management/*` | templates_mgmt | ✅ | 已对接 |
| **Vibe** | `/api/v1/ppt/vibe/*` | viewer | ✅ | 已对接 |
| **OpenAI** | `/api/v1/ppt/openai/*` | settings | ✅ | 已对接 |
| **Config** | `/api/v1/ppt/config/*` | settings | ✅ | 已对接 |
| **Theme** | `/api/v1/ppt/theme/*` | settings | ✅ | 已对接 |
| **Footer** | `/api/v1/ppt/footer/*` | settings | ✅ | 已对接 |
| **Auth** | `/api/v1/ppt/auth/*` | - | ❌ | **无前端** |
| **Google** | `/api/v1/ppt/google/*` | settings | ✅ | 模型检测 |
| **Anthropic** | `/api/v1/ppt/anthropic/*` | settings | ✅ | 模型检测 |
| **Ollama** | `/api/v1/ppt/ollama/*` | settings | ✅ | 模型检测 |
| **PDF Slides** | `/api/v1/ppt/pdf-slides/*` | - | ❌ | **无前端** |
| **PPTX Slides** | `/api/v1/ppt/pptx-slides/*` | - | ❌ | **无前端** |
| **PPTX Fonts** | `/api/v1/ppt/pptx-fonts/*` | fonts | ✅ | 分析 PPTX 字体 |
| **Slide to HTML** | `/api/v1/ppt/slide-to-html/*` | - | ❌ | **无前端** |
| **HTML to React** | `/api/v1/ppt/html-to-react/*` | - | ❌ | **无前端** |
| **HTML Edit** | `/api/v1/ppt/html-edit/*` | - | ❌ | **无前端** |
| **Webhook** | `/api/v1/webhook/*` | - | ❌ | **无前端** |

---

## 三、已对接模块详情

### 3.1 仪表板（dashboard）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `GET /api/v1/ppt/presentation/all` | `PRESENTATION_ROUTER.get("/all")` | 获取所有演示列表 |
| `POST /api/v1/ppt/presentation/export` | `PRESENTATION_ROUTER.post("/export")` | 触发导出 |
| `GET /api/v1/ppt/presentation/{id}/export/download` | `PRESENTATION_ROUTER.get("/{id}/export/download")` | 下载文件 |
| `DELETE /api/v1/ppt/presentation/{id}` | `PRESENTATION_ROUTER.delete("/{id}")` | 删除演示 |

### 3.2 创建演示（create）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `POST /api/v1/ppt/files/upload` | `FILES_ROUTER.post("/upload")` | 上传附件 |
| `POST /api/v1/ppt/presentation/generate` | `PRESENTATION_ROUTER.post("/generate")` | 同步生成 |
| `POST /api/v1/ppt/presentation/generate/async` | `PRESENTATION_ROUTER.post("/generate/async")` | 异步生成 |
| `GET /api/v1/ppt/presentation/status/{tid}` | `PRESENTATION_ROUTER.get("/status/{tid}")` | 查询异步状态 |
| `GET /api/v1/ppt/presentation/{id}/export/download` | 同上 | 下载导出文件 |

### 3.3 大纲编辑（outline）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `POST /api/v1/ppt/presentation/create` | `PRESENTATION_ROUTER.post("/create")` | 创建演示 |
| `GET /api/v1/ppt/outlines/stream/{id}` | `OUTLINES_ROUTER.get("/stream/{id}")` | SSE 流式大纲 |
| `GET /api/v1/ppt/layouts/{name}` | `LAYOUTS_ROUTER.get("/{layout_name}")` | 获取布局 |
| `POST /api/v1/ppt/presentation/prepare` | `PRESENTATION_ROUTER.post("/prepare")` | 准备演示 |
| `POST /api/v1/ppt/presentation/export` | 同上 | 导出 |

### 3.4 演示查看（viewer）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `GET /api/v1/ppt/presentation/{id}` | `PRESENTATION_ROUTER.get("/{id}")` | 获取演示详情 |
| `POST /api/v1/ppt/slide/edit` | `SLIDE_ROUTER.post("/edit")` | 幻灯片编辑 |
| `POST /api/v1/ppt/vibe/edit` | `VIBE_ROUTER.post("/edit")` | Vibe 对话编辑 |

### 3.5 图片管理（images）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `GET /api/v1/ppt/images/generate` | `IMAGES_ROUTER.get("/generate")` | AI 生成图片 |
| `GET /api/v1/ppt/images/generated` | `IMAGES_ROUTER.get("/generated")` | 已生成图片列表 |
| `GET /api/v1/ppt/images/uploaded` | `IMAGES_ROUTER.get("/uploaded")` | 已上传图片列表 |
| `DELETE /api/v1/ppt/images/{id}` | `IMAGES_ROUTER.delete("/{id}")` | 删除图片 |
| `POST /api/v1/ppt/images/upload` | `IMAGES_ROUTER.post("/upload")` | 上传图片 |

### 3.6 字体管理（fonts）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `GET /api/v1/ppt/fonts/list` | `FONTS_ROUTER.get("/list")` | 字体列表 |
| `DELETE /api/v1/ppt/fonts/delete/{filename}` | `FONTS_ROUTER.delete("/delete/{filename}")` | 删除字体 |
| `POST /api/v1/ppt/fonts/upload` | `FONTS_ROUTER.post("/upload")` | 上传字体 |

### 3.7 模板管理（templates_mgmt）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `GET /api/v1/ppt/template-management/summary` | `LAYOUT_MANAGEMENT_ROUTER.get("/summary")` | 模板概览 |
| `GET /api/v1/ppt/template-management/get-templates/{pid}` | `LAYOUT_MANAGEMENT_ROUTER.get("/get-templates/{pid}")` | 获取模板 |
| `DELETE /api/v1/ppt/template-management/delete-templates/{id}` | `LAYOUT_MANAGEMENT_ROUTER.delete("/delete-templates/{id}")` | 删除模板 |

### 3.8 图标搜索（icons）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `GET /api/v1/ppt/icons/search` | `ICONS_ROUTER.get("/search")` | 搜索图标 |

### 3.9 系统设置（settings）

| 前端 API 调用 | 后端路由 | 功能 |
|---------------|----------|------|
| `POST /api/v1/ppt/openai/models/available` | `OPENAI_ROUTER.post("/models/available")` | 检测 OpenAI 模型 |

**注意**: settings 页的配置加载/保存主要通过本地 `get_user_config`、`update_env_with_user_config` 实现，**未调用** `/api/v1/ppt/config`。

---

## 四、仅后端、无前端接口的模块

### 4.1 配置类（建议接入 settings）

| 模块 | 路径 | 功能 | 建议 |
|------|------|------|------|
| **Config** | `/api/v1/ppt/config` | 读写用户配置、has-key、can-change、telemetry | 将 settings 改为调用 config API，统一服务端存储 |
| **Theme** | `/api/v1/ppt/theme` | 主题获取/保存 | 在 settings 或独立「主题」页中接入 |
| **Footer** | `/api/v1/ppt/footer` | 页脚获取/保存 | 可并入 settings 或模板配置 |

### 4.2 LLM 提供商检测（建议接入 settings）

| 模块 | 路径 | 功能 | 建议 |
|------|------|------|------|
| **Google** | `/api/v1/ppt/google/models/available` | 检测 Google 模型 | 在 settings 中增加「检测」按钮 |
| **Anthropic** | `/api/v1/ppt/anthropic/models/available` | 检测 Anthropic 模型 | 同上 |
| **Ollama** | `/api/v1/ppt/ollama/models/available` 等 | Ollama 模型/拉取 | 在 settings 的 Ollama 区块中接入 |

### 4.3 文档转换（可选前端）

| 模块 | 路径 | 功能 | 建议 |
|------|------|------|------|
| **PDF Slides** | `/api/v1/ppt/pdf-slides/process` | PDF 转幻灯片 | 在 create/outline 增加「从 PDF 生成」入口 |
| **PPTX Slides** | `/api/v1/ppt/pptx-slides/process` | PPTX 转幻灯片 | 同上，增加「从 PPTX 导入」入口 |
| **PPTX Fonts** | `/api/v1/ppt/pptx-fonts/install` | 安装 PPTX 字体 | 可在 fonts 页增加「从 PPTX 安装字体」 |

### 4.4 高级编辑（多为 Next.js 遗留）

| 模块 | 路径 | 功能 | 建议 |
|------|------|------|------|
| **Slide to HTML** | `/api/v1/ppt/slide-to-html` | 幻灯片截图转 HTML | 原 Next.js 功能，NiceGUI 暂无对应；可长期保留作 API |
| **HTML to React** | `/api/v1/ppt/html-to-react` | HTML 转 TSX | 同上 |
| **HTML Edit** | `/api/v1/ppt/html-edit` | AI 编辑 HTML | 同上 |

### 4.5 认证与 Webhook

| 模块 | 路径 | 功能 | 建议 |
|------|------|------|------|
| **Auth** | `/api/v1/ppt/auth/*` | 注册/登录/用户管理 | 若有登录需求，需新增登录/注册页 |
| **Webhook** | `/api/v1/webhook/*` | 订阅/取消订阅 | 可在 settings 或独立「集成」页中接入 |

---

## 五、遗留/未使用代码

- **`api/routers/presentation/`**：另一套 presentation 路由（handlers、mixins 等），**未被 `api/main.py` 挂载**，属于遗留实现，功能已由 `api/v1/ppt/endpoints/presentation.py` 覆盖。

---

## 六、完善方案（按优先级）

### 阶段 1：高优先级（配置与模型检测）

| 序号 | 任务 | 改动 |
|------|------|------|
| 1 | **Settings 接入 Config API** | settings 改为调用 `GET/POST /api/v1/ppt/config`，配置落库或统一存储 |
| 2 | **Settings 接入 Google/Anthropic/Ollama 检测** | 为对应提供商增加「检测模型」按钮，调用各自 `models/available` 接口 |
| 3 | **Theme/Footer 接入** | 在 settings 或新建「外观」页中，调用 theme/footer API |

### 阶段 2：中优先级（文档导入）

| 序号 | 任务 | 改动 |
|------|------|------|
| 4 | **PDF/PPTX 导入入口** | 在 create 或 outline 增加「从 PDF 生成」「从 PPTX 导入」选项，调用 pdf-slides、pptx-slides |
| 5 | **PPTX 字体安装** | 在 fonts 页增加「从 PPTX 安装字体」，调用 pptx-fonts API |

### 阶段 3：低优先级（可选）

| 序号 | 任务 | 改动 |
|------|------|------|
| 6 | **Auth 登录页** | 若启用认证，新增 `/login`、`/register` 页，调用 auth API |
| 7 | **Webhook 配置页** | 新增「集成/Webhook」页，管理 webhook 订阅 |
| 8 | **Slide-to-HTML 流程** | 若需在 NiceGUI 中复刻原 Next.js 的高级编辑，再设计对应页面与流程 |

### 阶段 4：代码清理

| 序号 | 任务 | 改动 |
|------|------|------|
| 9 | **移除或归档 api/routers/presentation** | 确认无引用后，删除或移至 `_legacy` 目录 |

---

## 七、前端页面与路由一览

| 页面 | 路由 | 导航名 |
|------|------|--------|
| home | `/` | 首页 |
| dashboard | `/dashboard` | 仪表板 |
| create | `/create` | 创建演示 |
| outline | `/outline` | 大纲编辑 |
| viewer | `/viewer` | 演示查看 |
| images | `/images` | 图片管理 |
| fonts | `/fonts` | 字体管理 |
| templates_mgmt | `/templates` | 模板管理 |
| icons | `/icons` | 图标搜索 |
| settings | `/settings` | 系统设置 |

---

## 八、总结

- **已对接**: 10 个后端模块，对应 10 个前端页面，覆盖演示创建、编辑、导出、资源管理等核心流程。
- **未对接**: 配置 (config)、主题 (theme)、页脚 (footer)、认证 (auth)、Webhook、各 LLM 检测、PDF/PPTX 导入、PPTX 字体、Slide-to-HTML 等高级功能。
- **建议**: 优先完成 settings 与 config/theme/footer/LLM 检测的对接，再按需补齐 PDF/PPTX 导入、Auth、Webhook 等能力。
