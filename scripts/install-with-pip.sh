#!/bin/bash
# Presenton - pip 安装脚本 (Linux/macOS)
# 前置: Python 3.11, pip, Node.js 18+
# 使用: ./scripts/install-with-pip.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Presenton pip 安装"
echo "    项目路径: $PROJECT_ROOT"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "错误: 未找到 Python，请安装 Python 3.11"
    exit 1
fi
PYTHON_CMD="$(command -v python3 2>/dev/null || command -v python)"

# 检查 pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "错误: 未找到 pip，请先安装 pip"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

# 创建虚拟环境 (推荐)
VENV_DIR="$PROJECT_ROOT/servers/fastapi/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "==> 创建 Python 虚拟环境..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# 安装 FastAPI 依赖 (docling 需 PyTorch 源)
echo "==> 安装 Python 依赖 (FastAPI)..."
cd "$PROJECT_ROOT/servers/fastapi"
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# 安装 Next.js 依赖
echo "==> 安装 Next.js 依赖..."
cd "$PROJECT_ROOT/servers/nextjs"
npm install

# 下载 NLTK 数据
echo "==> 下载 NLTK 数据..."
cd "$PROJECT_ROOT/servers/fastapi"
$PYTHON_CMD -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')" 2>/dev/null || true

echo ""
echo "==> 安装完成!"
echo ""
echo "运行方式 (请先激活虚拟环境):"
echo "  source servers/fastapi/.venv/bin/activate  # Linux/macOS"
echo "  node start-local.js --pip                   # 使用 pip 环境"
echo ""
echo "或直接:"
echo "  node start-local.js --pip  # 会自动使用 .venv 中的 python"
echo ""
echo "然后打开 http://localhost:5000"
echo ""
