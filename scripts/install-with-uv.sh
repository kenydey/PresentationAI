#!/bin/bash
# Presenton - uv 安装脚本 (Linux/macOS)
# 前置: 安装 uv (curl -LsSf https://astral.sh/uv/install.sh | sh)
# 使用: ./scripts/install-with-uv.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Presenton uv 安装"
echo "    项目路径: $PROJECT_ROOT"
echo ""

# 检查 uv
if ! command -v uv &> /dev/null; then
    echo "错误: 未找到 uv，请先安装:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

# 安装 FastAPI 依赖
echo "==> 安装 Python 依赖 (FastAPI)..."
cd "$PROJECT_ROOT/servers/fastapi"
uv sync

# 安装 Next.js 依赖
echo "==> 安装 Next.js 依赖..."
cd "$PROJECT_ROOT/servers/nextjs"
npm install

# 下载 NLTK 数据
echo "==> 下载 NLTK 数据..."
cd "$PROJECT_ROOT/servers/fastapi"
uv run python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')" 2>/dev/null || true

echo ""
echo "==> 安装完成!"
echo ""
echo "运行方式:"
echo "  node start-local.js          # 开发模式 (无 nginx)"
echo "  node start-local.js --dev    # 开发模式 + 热重载"
echo ""
echo "然后打开 http://localhost:5000"
echo ""
