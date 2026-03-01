# Presenton 遗留代码分析报告

> 分析对象：`PresentationAI/` 子模块中未被当前 Presentation 程序使用的后端、前端代码  
> 生成日期：2026-02

---

## 一、现状概述

| 项目 | 当前使用 | 遗留未用 |
|------|----------|-----------|
| **前端** | NiceGUI (servers/fastapi/nicegui_app) | Next.js (PresentationAI/servers/nextjs) |
| **后端** | servers/fastapi (FastAPI + NiceGUI) | 部分与主仓库共享，Electron 启动逻辑独立 |
| **桌面** | app/ + forge.config.js (可选) | ~~PresentationAI/electron~~（已删除） |
| **启动** | start-local.js（仅 FastAPI） | start.js（FastAPI + Next.js 双进程） |

当前程序通过 `start-local.js` 仅启动 `servers/fastapi`，UI 全由 NiceGUI 提供。`PresentationAI` 子模块内的 Next.js 与 Electron 相关代码**未被运行时使用**。

---

## 二、遗留代码明细

### 2.1 Next.js 前端（约 323 个 TS/TSX 文件，~12MB）

**路径**：`PresentationAI/servers/nextjs/`

| 模块 | 功能 | 文件数/规模 |
|------|------|-------------|
| **presentation-templates/** | 120+ 个 TSX 幻灯片布局（neo-modern、general、standard、modern、swift） | ~80 个 TSX |
| **(presentation-generator)/** | 创建、大纲、演示、仪表板、custom-template、pdf-maker 等页面 | 多目录 |
| **app/api/** | Next.js API Routes：presentation_to_pptx_model、export-as-pdf、user-config、templates 等 | ~15 个 route |
| **hooks/** | useCustomTemplates、compileLayout、useRemoteSvgIcon 等 | 若干 |
| **components/** | UI 组件（Button、Card、Select 等） | 若干 |

**核心能力**：
- 用 React + Tailwind 渲染幻灯片，支持 120+ 种布局
- `pdf-maker` 页面：16:9 容器内渲染所有幻灯片
- `presentation_to_pptx_model`：Puppeteer 访问 pdf-maker → 采样 DOM → 转 PptxPresentationModel（高质量导出）
- custom-template：PPTX 导入 → slide-to-html → html-to-react → 保存 TSX 自定义模板
- Mixpanel 埋点、ConfigurationInitializer 等

### 2.2 Next.js API Routes（未使用）

**路径**：`PresentationAI/servers/nextjs/app/api/`

| 路由 | 功能 | 对应 FastAPI |
|------|------|-------------|
| `presentation_to_pptx_model` | Puppeteer 采样 pdf-maker → PPT 模型 | 已用 Playwright 在 `dom_sampling_export_service` 替代 |
| `export-as-pdf` | Puppeteer 渲染 pdf-maker → PDF | 现用 LibreOffice |
| `user-config` | 读写 userConfig.json | 已迁移到 `/api/v1/ppt/config` |
| `templates` | 模板 CRUD | 已迁移到 template-management |
| `has-required-key` | 校验 API Key | 无直接对应 |
| `telemetry-status` | 遥测状态 | 无 |
| `can-change-keys` | 是否允许改 Key | 无 |
| `upload-image` | 图片上传 | 已迁移到 images API |
| `save-layout` | 保存布局 | 已迁移到 template-management |
| `read-file` | 读文件 | 无 |

### 2.3 Electron 桌面端（已删除）

**原路径**：`PresentationAI/electron/`（约 341MB，已删除以减小体积）

| 模块 | 功能 | 状态 |
|------|------|------|
| `app/main.ts` | 启动 FastAPI + Next.js 双进程 | 依赖 Next.js，当前未用 |
| `app/utils/servers.ts` | 启动 Next.js build server | 未用 |
| `app/ipc/*` | IPC 处理器（presentation_to_pptx_model、template API 等） | 未用 |
| `servers/nextjs` | Electron 内嵌 Next.js 副本 | 未用 |
| `servers/fastapi` | 与主仓可能重复 | 未用 |
| `resources/` | 构建产物（nextjs、fastapi） | 未用 |
| `forge.config.js`、`package.json` | 构建配置 | 未用 |

### 2.4 TSX 布局模板（120+ 个）

**路径**：`PresentationAI/servers/nextjs/app/presentation-templates/`

| 组 | 布局数 | 说明 |
|----|--------|------|
| neo-modern | ~16 | 图表、表格、时间线等 |
| general | ~12 | 通用（intro、bullet、team、chart 等） |
| standard | ~14 | 标准（TOC、contact、chart 等） |
| modern | ~11 | 现代风格 |
| swift | ~10 | 简约风格 |

**当前利用**：`scripts/extract_templates.py` 从上述 TSX 提取元数据生成 `template_registry.json`。主仓 `extract_templates` 指向 `workspace/nextjs`，需改为 `PresentationAI/servers/nextjs` 才能正确执行。`template_registry.json` 已存在，供 DESIGN_AGENT、get_slide_content、slide_preview 使用。

---

## 三、功能对照与利用价值

### 3.1 已有替代或迁移

| 遗留功能 | 当前实现 | 说明 |
|----------|----------|------|
| 用户配置 | `/api/v1/ppt/config` | 已迁移 |
| 模板管理 | template-management | 已迁移 |
| 图片上传 | images API | 已迁移 |
| 高质量 PPT 导出 | Playwright DOM 采样 (dom_sampling_export_service) | 与 Puppeteer 方案等效 |
| 布局元数据 | template_registry.json | 从 TSX 提取，只读 |

### 3.2 有参考或复用价值

| 遗留模块 | 价值 | 建议 |
|----------|------|------|
| **TSX 布局组件** | 定义 120+ 种版式结构与样式 | 1) 保留作 extract_templates 数据源 2) 参考布局与 Tailwind 类，扩展 NiceGUI slide_preview |
| **presentation_to_pptx_model** | 完整 DOM 采样与 ElementAttributes 逻辑 | 已用 Playwright 重写，可作校验与回归参考 |
| **convertElementAttributesToPptxSlides** | DOM → Pptx 映射细节 | 可对照优化 dom_sampling_export_service 的转换 |
| **useCustomTemplates / compileLayout** | 动态编译并运行 TSX 布局 | 若要在浏览器端渲染 TSX，可移植思路 |
| **pdf-maker 页面结构** | `#presentation-slides-wrapper`、slide 容器 | 与当前 export-view 设计一致，可继续参考 |

### 3.3 依赖过重或不再必需

| 遗留模块 | 说明 |
|----------|------|
| **完整 Electron 包** | 341MB，依赖 Next.js，当前架构不需要 |
| **Next.js 全套** | 323 文件、约 12MB，需 Node/npm 构建，当前以 NiceGUI 为主 |
| **Mixpanel / 遥测** | 第三方埋点，按需保留或移除 |

---

## 四、建议

### 4.1 短期（保留与整理）

1. **保留 PresentationAI 子模块**：用于 extract_templates 与设计参考。
2. **修正 extract_templates 路径**：`TEMPLATES_DIR` 指向 `PresentationAI/servers/nextjs/app/presentation-templates`（或通过环境变量配置）。
3. **文档化**：在 README/AGENTS 中说明 PresentationAI 为「上游参考代码，非运行时依赖」。

### 4.2 中期（按需复用）

1. **扩展 slide_preview**：对照 TSX 中的 neo-modern、general 等布局，为 NiceGUI 增加更多版式。
2. **自定义模板流程**：若需「PPTX 导入 → HTML → TSX → 保存」，可参考 custom-template 与 slide-to-html 相关逻辑。
3. **DOM 采样质量**：对照 `pptx_models_utils.ts`、`element_attibutes` 完善 `dom_sampling_export_service` 的样式与布局解析。

### 4.3 长期（可选精简）

1. **移除 Electron**：已删除 `PresentationAI/electron` 以减小仓库体积（2026-02 实施）。
2. **只保留 TSX 布局**：若仅需 template_registry，可只保留 `presentation-templates/`，删除其余 Next.js 代码。
3. **改为 git submodule 或独立仓库**：将 PresentationAI 作为可选「参考实现」单独维护，主仓仅依赖其导出的 template_registry.json。

---

## 五、总结

| 类别 | 结论 |
|------|------|
| **运行依赖** | 当前程序不依赖 PresentationAI 中 Next.js 与 Electron |
| **参考价值** | 高：TSX 布局、DOM 采样与 Pptx 转换逻辑有持续参考价值 |
| **保留建议** | 建议保留 PresentationAI，用于 extract_templates 与设计参考 |
| **精简空间** | 可视需求删除 electron 或大部分 Next.js，仅保留 presentation-templates |
