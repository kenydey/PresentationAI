# Presenton - pip 安装脚本 (Windows PowerShell)
# 前置: Python 3.11, pip, Node.js 18+
# 使用: .\scripts\install-with-pip.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "==> Presenton pip 安装" -ForegroundColor Cyan
Write-Host "   项目路径: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# 检查 Python
$PythonCmd = $null
if (Get-Command python3 -ErrorAction SilentlyContinue) { $PythonCmd = "python3" }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $PythonCmd = "python" }
if (-not $PythonCmd) {
    Write-Host "错误: 未找到 Python，请安装 Python 3.11" -ForegroundColor Red
    exit 1
}

# 检查 pip
try {
    & $PythonCmd -m pip --version | Out-Null
} catch {
    Write-Host "错误: 未找到 pip，请先安装 pip" -ForegroundColor Red
    exit 1
}

# 检查 Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到 Node.js，请先安装 Node.js 18+" -ForegroundColor Red
    exit 1
}

# 创建虚拟环境
$VenvDir = "$ProjectRoot\servers\fastapi\.venv"
if (-not (Test-Path $VenvDir)) {
    Write-Host "==> 创建 Python 虚拟环境..." -ForegroundColor Cyan
    & $PythonCmd -m venv $VenvDir
}
$PipExe = "$VenvDir\Scripts\pip.exe"

# 安装 FastAPI 依赖
Write-Host "==> 安装 Python 依赖 (FastAPI)..." -ForegroundColor Cyan
Push-Location "$ProjectRoot\servers\fastapi"
try {
    & $PipExe install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
} finally {
    Pop-Location
}

# 安装 Next.js 依赖
Write-Host "==> 安装 Next.js 依赖..." -ForegroundColor Cyan
Push-Location "$ProjectRoot\servers\nextjs"
try {
    npm install
} finally {
    Pop-Location
}

# 下载 NLTK 数据
Write-Host "==> 下载 NLTK 数据..." -ForegroundColor Cyan
Push-Location "$ProjectRoot\servers\fastapi"
try {
    & "$VenvDir\Scripts\python.exe" -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')" 2>$null
} catch {
    # NLTK 下载失败不阻断安装
}
Pop-Location

Write-Host ""
Write-Host "==> 安装完成!" -ForegroundColor Green
Write-Host ""
Write-Host "运行方式 (请先激活虚拟环境):" -ForegroundColor Cyan
Write-Host "  .\servers\fastapi\.venv\Scripts\Activate.ps1  # Windows" -ForegroundColor White
Write-Host "  node start-local.js --pip                   # 使用 pip 环境" -ForegroundColor White
Write-Host ""
Write-Host "然后打开 http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
