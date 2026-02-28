# Presenton - uv 安装脚本 (Windows PowerShell)
# 前置: 安装 uv (powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex")
# 使用: .\scripts\install-with-uv.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "==> Presenton uv 安装" -ForegroundColor Cyan
Write-Host "   项目路径: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# 检查 uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到 uv，请先安装:" -ForegroundColor Red
    Write-Host "  powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`"" -ForegroundColor Yellow
    exit 1
}

# 检查 Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到 Node.js，请先安装 Node.js 18+" -ForegroundColor Red
    exit 1
}

# 安装 FastAPI 依赖
Write-Host "==> 安装 Python 依赖 (FastAPI)..." -ForegroundColor Cyan
Push-Location "$ProjectRoot\servers\fastapi"
try {
    uv sync
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
    uv run python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')" 2>$null
} catch {}
Pop-Location

Write-Host ""
Write-Host "==> 安装完成!" -ForegroundColor Green
Write-Host ""
Write-Host "运行方式:" -ForegroundColor Cyan
Write-Host "  node start-local.js          # 开发模式 (无 nginx)" -ForegroundColor White
Write-Host "  node start-local.js --dev     # 开发模式 + 热重载" -ForegroundColor White
Write-Host ""
Write-Host "然后打开 http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
