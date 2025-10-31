# ==========================================
# PowerShell 部署脚本 - Windows 版本
# ==========================================

param(
    [string]$Env = "production",
    [string]$Platform = "vercel",
    [switch]$Test,
    [switch]$SkipBuild,
    [switch]$Help
)

# 显示帮助信息
function Show-Help {
    Write-Host ""
    Write-Host "Usage: .\deploy.ps1 [OPTIONS]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Env ENV              Environment (production|preview|development)"
    Write-Host "  -Platform PLAT        Platform (vercel|netlify|both)"
    Write-Host "  -Test                 Run tests before deploy"
    Write-Host "  -SkipBuild            Skip build step"
    Write-Host "  -Help                 Show this help message"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\deploy.ps1 -Env production -Platform vercel -Test"
    Write-Host "  .\deploy.ps1 -Env preview -Platform netlify"
    exit 0
}

if ($Help) {
    Show-Help
}

# 日志函数
function Log-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Log-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Log-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Log-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# 错误处理
$ErrorActionPreference = "Stop"

try {
    # 开始部署
    Log-Info "Starting deployment process..."
    Log-Info "Environment: $Env"
    Log-Info "Platform: $Platform"

    # 检查 Node.js
    Log-Info "Checking Node.js version..."
    $nodeVersion = node -v
    Log-Success "Node.js version: $nodeVersion"

    # 检查 npm
    Log-Info "Checking npm version..."
    $npmVersion = npm -v
    Log-Success "npm version: $npmVersion"

    # 清理旧文件
    Log-Info "Cleaning old build files..."
    if (Test-Path dist) { Remove-Item -Recurse -Force dist }
    if (Test-Path .vercel) { Remove-Item -Recurse -Force .vercel }
    if (Test-Path .netlify) { Remove-Item -Recurse -Force .netlify }
    Log-Success "Cleaned successfully"

    # 安装依赖
    Log-Info "Installing dependencies..."
    npm ci --prefer-offline --no-audit
    Log-Success "Dependencies installed"

    # 运行 lint
    Log-Info "Running lint..."
    npm run lint
    Log-Success "Lint passed"

    # 运行类型检查
    Log-Info "Running type check..."
    npx tsc --noEmit
    Log-Success "Type check passed"

    # 运行测试
    if ($Test) {
        Log-Info "Running tests..."
        npm run test:coverage
        Log-Success "Tests passed"
    }

    # 构建应用
    if (-not $SkipBuild) {
        Log-Info "Building application for $Env..."
        
        $env:NODE_ENV = if ($Env -eq "production") { "production" } else { "development" }
        npm run build
        
        Log-Success "Build completed"
        
        # 显示构建大小
        Log-Info "Build size:"
        $distSize = (Get-ChildItem -Path dist -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "  dist: $([math]::Round($distSize, 2)) MB"
    }
    else {
        Log-Warning "Skipping build step"
    }

    # 部署函数
    function Deploy-ToVercel {
        Log-Info "Deploying to Vercel..."
        
        if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
            Log-Error "Vercel CLI not found. Install with: npm install -g vercel"
            exit 1
        }
        
        if ($Env -eq "production") {
            vercel --prod --yes
        }
        else {
            vercel --yes
        }
        
        Log-Success "Deployed to Vercel successfully"
    }

    function Deploy-ToNetlify {
        Log-Info "Deploying to Netlify..."
        
        if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
            Log-Error "Netlify CLI not found. Install with: npm install -g netlify-cli"
            exit 1
        }
        
        if ($Env -eq "production") {
            netlify deploy --prod --dir=dist
        }
        else {
            netlify deploy --dir=dist
        }
        
        Log-Success "Deployed to Netlify successfully"
    }

    # 根据平台部署
    switch ($Platform) {
        "vercel" {
            Deploy-ToVercel
        }
        "netlify" {
            Deploy-ToNetlify
        }
        "both" {
            Deploy-ToVercel
            Deploy-ToNetlify
        }
        default {
            Log-Error "Unknown platform: $Platform"
            exit 1
        }
    }

    # 完成
    Log-Success "🎉 Deployment completed successfully!"
    Log-Info "Environment: $Env"
    Log-Info "Platform: $Platform"

    # 显示部署信息
    if ($Platform -eq "vercel" -or $Platform -eq "both") {
        Log-Info "Vercel dashboard: https://vercel.com/dashboard"
    }

    if ($Platform -eq "netlify" -or $Platform -eq "both") {
        Log-Info "Netlify dashboard: https://app.netlify.com"
    }
}
catch {
    Log-Error "Deployment failed: $_"
    exit 1
}
