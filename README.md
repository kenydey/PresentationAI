# PresentationAI
Python 原生的 AI 演示文稿生成器，基于 FastAPI + NiceGUI，本地优先集成多家 LLM/图片服务，一键生成并导出 PPTX/PDF。

一、运行方式概览
现在的架构是：
•	后端：servers/fastapi（FastAPI + NiceGUI，已集成前端 UI）
•	Web UI：NiceGUI 挂载在 FastAPI 上的 /ui
•	桌面端：Electron 只启动 FastAPI，然后加载 http://127.0.0.1:<port>/ui
•	旧的 Next.js 前端：已从启动路径和 Nginx 中移除，不再使用
因此，无论是 Docker、本机开发还是 Electron，界面入口都是 NiceGUI。
________________________________________
二、Docker 运行（推荐用于一键使用）
1. 前置条件
•	已安装 Docker
•	当前代码已经包含你的改动（默认端口等）
2. 构建镜像
在项目根目录：
cd "C:\Users\kenyd\OneDrive\OneDrive\Private Company\Presentation\presentation"
docker build -t presenton:local .
> 如只想开发用，也可以用 Dockerfile.dev 构建调试镜像，这里给的是最直接的生产风格构建。
3. 运行容器
docker run -it --name presenton-local -p 5000:80 -v "${PWD}\app_data:/app_data" presenton:local
•	宿主机访问地址：http://localhost:5000
•	Nginx 已改为：
•	http://容器:80/ → 反向代理到 http://localhost:8000/ui/（NiceGUI UI）
•	/api/v1/ → http://localhost:8000（FastAPI API）
•	/app_data/exports/ 等静态目录保持不变
4. 首次使用建议
1.	打开 http://localhost:5000/ui/settings
•	在页面中配置 OPENAI_API_KEY、LLM、IMAGE_PROVIDER 等（写入容器内的 USER_CONFIG_PATH）。
2.	之后访问：
•	http://localhost:5000/ui/presentation：从提示词直接生成 PPTX/PDF。
•	http://localhost:5000/ui/outline：大纲流 + 编辑 + 布局 + 立即导出。
•	http://localhost:5000/ui/dashboard：查看最近演示、一键导出。
________________________________________
三、本机开发运行（uv + FastAPI + NiceGUI）
适合你在 Windows 上调试 Python 逻辑、UI 和模板。
1. 前置条件
•	Python 3.11（必须）
•	uv
•	安装（PowerShell）：
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
•	（可选）Node.js 18+（用于 Electron 或旧脚本，单纯 Web 不强制）
2. 安装后端依赖
cd "C:\Users\kenyd\OneDrive\OneDrive\Private Company\Presentation\presentation\servers\fastapi"
uv sync
3. 启动 FastAPI + NiceGUI
uv run python server.py --port 8000 --reload true
•	Web UI 入口：http://localhost:8000/ui
•	API 文档：http://localhost:8000/docs
4. 使用入口
•	http://localhost:8000/ui/settings
配置 LLM / 图像等。
•	http://localhost:8000/ui/presentation
直接从提示词生成演示（对应 /api/v1/ppt/presentation/generate）。
•	http://localhost:8000/ui/outline
•	创建演示（/presentation/create）
•	流式生成大纲（/outlines/stream/{id}）
•	编辑每页大纲 + 选择 Python 模板（Intro / TOC / Contact / Chart 等）
•	调用 /presentation/prepare 保存
•	“立即导出” 按钮调用 /presentation/export 导出 PPTX/PDF
•	http://localhost:8000/ui/dashboard
最近演示列表 + 一键导出。> 注意：本机开发时不再需要启动 servers/nextjs，UI 全在 Python 里。
________________________________________
四、Electron 桌面应用运行
Electron 现在已经改为只依赖 FastAPI+NiceGUI，不再启动 Next.js。
1. 前置条件
•	Node.js 18+ 和 npm
•	Python 3.11 + uv（用于 Electron 内部 FastAPI）
2. 安装与环境准备
cd "C:\Users\kenyd\OneDrive\OneDrive\Private Company\Presentation\presentation\electron"
# 安装 Electron 依赖
npm install
# 为 Electron 所需的 FastAPI 后端和（已不再使用的）Next.js 准备环境
npm run setup:env
> setup:env 会：> - 在 electron/servers/fastapi 中执行 uv sync> - 在 electron/servers/nextjs 中 npm install（虽然前端已迁，但依赖无碍）
3. 开发模式运行桌面应用
npm run dev
•	程序会：
•	启动 Electron 主进程
•	启动打包在 electron/servers/fastapi 中的 FastAPI + NiceGUI
•	窗口加载 http://127.0.0.1:<fastApiPort>/ui
使用体验与浏览器访问 /ui 一致，只是封装在桌面窗口中。
4. 打包桌面安装包（可选）
在 electron 目录：
npm run build:all
npm run dist
•	输出安装包在 electron/dist 目录（根据 electron-builder 配置）。
________________________________________
五、快速问题排查小贴士
•	界面打不开：
•	确认 FastAPI 是否在 8000 端口（本机）或容器内正常启动。
•	浏览器直接访问 http://localhost:8000/docs（或容器内 curl http://localhost:8000/docs）看是否正常。
•	生成失败：
•	去 /ui/settings 确认 LLM 和 API Key 是否正确。
•	查看控制台或 Docker 日志，看 /api/v1/ppt/presentation/generate 返回的错误。
•	导出失败或打不开文件：
•	查看 /app_data/exports/ 下是否有生成的 .pptx / .pdf。
•	确认 Nginx 或本机是否能访问 /app_data/exports/...（Docker 映射的卷路径是否存在）。


