# PresentationAI 项目现状与开发计划

> 最后更新: 2026-02-28

---

## 一、系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                    用户浏览器                              │
│              http://localhost:8000/ui/                    │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 FastAPI 服务器 (:8000)                     │
│                                                          │
│  ┌──────────────┐  ┌──────────────────────────────────┐  │
│  │  NiceGUI 前端 │  │      REST API (/api/v1/ppt/)     │  │
│  │  挂载于 /ui   │  │                                  │  │
│  │              │  │  presentation  files    fonts     │  │
│  │  10 个页面    │──▶│  outlines     images   icons    │  │
│  │  layout.py   │  │  layouts      slide    templates │  │
│  │  api_client  │  │  openai/google/anthropic/ollama  │  │
│  └──────────────┘  └──────────┬───────────────────────┘  │
│                               │                          │
│  ┌────────────────────────────▼──────────────────────┐   │
│  │                  业务逻辑层                         │   │
│  │  llm_client        image_generation_service       │   │
│  │  pptx_creator      documents_loader               │   │
│  │  template_registry slide_to_pptx_converter        │   │
│  │  export_utils      webhook_service                │   │
│  └────────────────────────────┬──────────────────────┘   │
│                               │                          │
│  ┌────────────────────────────▼──────────────────────┐   │
│  │                  数据存储层                         │   │
│  │  SQLite (aiosqlite)    文件系统 (/app_data/)       │   │
│  │  9 个数据模型           template_registry.json     │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │              外部服务（按需连接）                     │   │
│  │  OpenAI  │ Google Gemini │ Anthropic │ Ollama     │   │
│  │  Pexels  │ Pixabay      │ ComfyUI   │ DALL-E     │   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## 二、已实现功能清单

### 后端 API（46 个端点，全部可用）

| 模块 | 端点数 | 状态 | 说明 |
|------|--------|------|------|
| 演示文稿 CRUD | 15 | ✅ 完成 | create/get/update/delete/export/generate(同步+异步) |
| 幻灯片编辑 | 2 | ✅ 完成 | AI 编辑内容 / HTML |
| 大纲生成 | 1 | ✅ 完成 | SSE 流式生成（需 LLM API Key） |
| 布局/模板 | 2 | ✅ 完成 | 本地注册表，8 组 120 个布局 |
| 模板管理 | 4 | ✅ 完成 | 保存/查询/删除自定义模板 |
| 文件处理 | 3 | ✅ 完成 | 上传/解析/更新（PDF/DOCX/TXT/PPTX） |
| 图片管理 | 5 | ✅ 完成 | AI 生成/上传/浏览/删除 |
| 字体管理 | 3 | ✅ 完成 | 上传/列表/删除 |
| 图标搜索 | 1 | ✅ 完成 | 矢量图标搜索 |
| PPTX/PDF 处理 | 3 | ✅ 完成 | PPTX 幻灯片提取、PDF 处理、字体分析 |
| HTML 转换 | 3 | ✅ 完成 | slide→HTML / HTML→React / HTML 编辑 |
| LLM 提供商 | 6 | ✅ 完成 | OpenAI/Google/Anthropic/Ollama 模型检测 |
| Webhook | 2 | ✅ 完成 | 订阅/取消订阅 |
| 导出系统 | — | ✅ 完成 | 纯 Python PPTX 导出 + LibreOffice PDF 转换 |

### NiceGUI 前端（10 个页面）

| 页面 | 路径 | 状态 | 对接后端 API |
|------|------|------|-------------|
| 首页 | `/ui/` | ✅ 完成 | 导航入口 + 功能概览 |
| 仪表板 | `/ui/dashboard` | ✅ 完成 | presentation/all, export, delete |
| 创建演示 | `/ui/create` | ✅ 完成 | generate(同步+异步), files/upload, status |
| 大纲编辑 | `/ui/outline` | ✅ 完成 | create, outlines/stream(SSE), prepare, export |
| 演示查看 | `/ui/viewer` | ✅ 完成 | presentation/{id}, slide/edit |
| 图片管理 | `/ui/images` | ✅ 完成 | images/* (生成/上传/浏览/删除) |
| 字体管理 | `/ui/fonts` | ✅ 完成 | fonts/* (上传/列表/删除) |
| 模板管理 | `/ui/templates` | ✅ 完成 | template-management/* |
| 图标搜索 | `/ui/icons` | ✅ 完成 | icons/search |
| 系统设置 | `/ui/settings` | ✅ 完成 | 读写 UserConfig JSON（全部 LLM/图像配置） |

### 基础设施

| 项目 | 状态 | 说明 |
|------|------|------|
| Next.js 替换 | ✅ 完成 | 已完全删除，0 处残留引用 |
| 模板注册表 | ✅ 完成 | TSX → JSON 提取，120 个布局 |
| PPTX 导出 | ✅ 完成 | 纯 Python（不依赖 Puppeteer） |
| PDF 导出 | ✅ 完成 | LibreOffice headless 转换 |
| 数据库 | ✅ 完成 | SQLite + aiosqlite，9 个模型 |
| 启动脚本 | ✅ 完成 | start-local.js 仅启动 FastAPI |

---

## 三、需要继续完成的部分

### 🔴 优先级高（核心功能缺口）

| 编号 | 任务 | 说明 | 涉及文件 |
|------|------|------|----------|
| H1 | **PPTX 导出质量提升** | 当前 `slide_to_pptx_converter.py` 是简化版，仅提取 title/description/bullets/image 等基础字段。需要支持完整的幻灯片元素（图表、表格、多图、图标等）匹配每种布局 schema | `utils/slide_to_pptx_converter.py` |
| H2 | **PDF 导出完善** | 当前 LibreOffice 转换在某些环境下不稳定。需要备选方案（如 Playwright/Chromium 渲染 HTML → PDF） | `utils/export_utils.py` |
| H3 | **前端日志/反馈机制** | `ui.log()` 组件在浏览器中日志可能不可见（需向下滚动），按钮操作的结果反馈体验需优化（改用 notification/dialog） | `nicegui_app/pages/*.py` |
| H4 | **用户配置 API 端点** | Next.js 原有 `/api/user-config` 的 GET/POST 端点未迁移到 FastAPI REST API（当前仅 NiceGUI 页面直接读写文件） | 新增端点 |

### 🟡 优先级中（体验和完整性）

| 编号 | 任务 | 说明 |
|------|------|------|
| M1 | **演示查看器幻灯片预览** | viewer 页面目前只显示 JSON/文本内容，缺少可视化幻灯片预览（HTML 渲染效果） |
| M2 | **大纲编辑器增强** | 支持拖拽排序、添加/删除单页、每页选择不同布局 |
| M3 | **仪表板展示优化** | 添加缩略图预览、搜索/筛选、分页 |
| M4 | **主题/配色系统** | Next.js 原有 `/api/theme` 和 `/api/footer` (SQLite) 功能未迁移 |
| M5 | **Electron 桌面端适配** | 更新 `app/main.ts` 和 `app/servers.ts` 不再启动 Next.js 进程 |
| M6 | **MCP Server 集成测试** | `mcp_server.py` 和 `app_mcp/` 模块的完整测试 |

### 🟢 优先级低（增强功能）

| 编号 | 任务 | 说明 |
|------|------|------|
| L1 | **自定义模板上传** | 支持用户上传 PPTX/PDF 作为自定义模板（原 Next.js `/api/save-layout`） |
| L2 | **文档预览页** | 上传文档后的 Markdown 预览（原 Next.js documents-preview） |
| L3 | **国际化** | 当前 UI 为中文，添加英文支持 |
| L4 | **单元测试补全** | 12 个测试文件中部分因 import 错误无法运行 |
| L5 | **Docker 部署** | 更新 Dockerfile 和 docker-compose.yml 适配新架构 |
| L6 | **Webhook 前端页面** | 添加 Webhook 订阅管理 UI |
| L7 | **用户认证** | 多用户支持和权限管理 |

---

## 四、技术栈总览

```
语言:        Python 3.11
后端框架:     FastAPI 0.116+
前端框架:     NiceGUI 3.2.0（挂载于 FastAPI）
数据库:       SQLite + aiosqlite + SQLModel
包管理:       uv (Astral)
LLM 集成:    OpenAI / Google Gemini / Anthropic / Ollama / 自定义兼容
图像生成:     DALL-E 3 / GPT Image 1.5 / Gemini Flash / Pexels / Pixabay / ComfyUI
文件处理:     python-pptx / pdfplumber / docling
导出:        python-pptx (PPTX) + LibreOffice (PDF)
模板:        120 个布局，JSON schema 注册表
```

---

## 五、文件结构

```
/workspace/
├── AGENTS.md                 # 开发环境说明
├── PROJECT_STATUS.md         # 本文档
├── package.json              # Node.js 启动入口
├── start-local.js            # 本地启动脚本（仅 FastAPI）
├── nginx.conf                # Nginx 配置（Docker 用）
│
├── servers/fastapi/          # ← 核心代码
│   ├── server.py             # 入口：uvicorn 启动
│   ├── pyproject.toml        # Python 依赖
│   ├── uv.lock               # 锁文件
│   │
│   ├── api/                  # API 路由层
│   │   ├── main.py           # FastAPI app + NiceGUI mount
│   │   ├── lifespan.py       # 启动初始化
│   │   ├── middlewares.py    # 中间件
│   │   └── v1/ppt/
│   │       ├── router.py     # 路由注册（19 个 Router）
│   │       └── endpoints/    # 46 个端点
│   │
│   ├── nicegui_app/          # NiceGUI 前端
│   │   ├── __init__.py       # app 创建
│   │   ├── layout.py         # 共享导航布局
│   │   ├── api_client.py     # 异步 HTTP 工具
│   │   ├── pages/            # 10 个页面模块
│   │   └── templates/        # NiceGUI 幻灯片模板
│   │
│   ├── models/               # 数据模型
│   │   ├── sql/              # 9 个 SQLModel 表
│   │   ├── pptx_models.py    # PPTX 结构模型
│   │   ├── user_config.py    # 用户配置模型
│   │   └── ...               # 其他 Pydantic 模型
│   │
│   ├── services/             # 14 个业务服务
│   ├── utils/                # 工具函数
│   │   ├── template_registry.py    # 本地模板注册表
│   │   ├── slide_to_pptx_converter.py  # 幻灯片→PPTX
│   │   ├── export_utils.py          # 导出工具
│   │   └── get_layout_by_name.py    # 布局获取
│   │
│   ├── assets/
│   │   └── template_registry.json   # 120 个布局 schema
│   │
│   ├── scripts/
│   │   └── extract_templates.py     # TSX→JSON 提取工具
│   │
│   └── tests/                # 12 个测试文件
│
├── app/                      # Electron 主进程（可选）
├── electron/                 # Electron 构建配置
└── PresentationAI/           # 上游 presenton 参考代码
```

---

## 六、后续开发路线图

```
Phase 1 (当前 → v1.1) — 核心打磨
  ├── H1: PPTX 导出质量（支持图表/表格/多图）
  ├── H3: 前端反馈体验（notification 替代 log）
  └── H4: 用户配置 REST API

Phase 2 (v1.2) — 体验提升
  ├── M1: 幻灯片可视化预览
  ├── M2: 大纲拖拽排序
  ├── M3: 仪表板搜索/分页/缩略图
  └── M4: 主题配色系统

Phase 3 (v1.3) — 部署与扩展
  ├── L5: Docker 部署更新
  ├── M5: Electron 适配
  ├── L1: 自定义模板上传
  └── L4: 测试覆盖率提升

Phase 4 (v2.0) — 高级功能
  ├── L7: 多用户认证
  ├── L3: 国际化
  └── L6: Webhook 管理 UI
```
