#!/bin/bash

# ==========================================
# 部署脚本 - 构建和部署到 Vercel/Netlify
# ==========================================

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 显示帮助信息
show_help() {
    echo "Usage: ./deploy.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -e, --env ENV        Environment (production|preview|development)"
    echo "  -p, --platform PLAT  Platform (vercel|netlify|both)"
    echo "  -t, --test           Run tests before deploy"
    echo "  -s, --skip-build     Skip build step"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh -e production -p vercel -t"
    echo "  ./deploy.sh --env preview --platform netlify"
}

# 默认参数
ENV="production"
PLATFORM="vercel"
RUN_TESTS=false
SKIP_BUILD=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENV="$2"
            shift 2
            ;;
        -p|--platform)
            PLATFORM="$2"
            shift 2
            ;;
        -t|--test)
            RUN_TESTS=true
            shift
            ;;
        -s|--skip-build)
            SKIP_BUILD=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# 开始部署
log_info "Starting deployment process..."
log_info "Environment: $ENV"
log_info "Platform: $PLATFORM"

# 检查 Node.js 版本
log_info "Checking Node.js version..."
NODE_VERSION=$(node -v)
log_success "Node.js version: $NODE_VERSION"

# 检查 npm 版本
log_info "Checking npm version..."
NPM_VERSION=$(npm -v)
log_success "npm version: $NPM_VERSION"

# 清理旧的构建文件
log_info "Cleaning old build files..."
rm -rf dist
rm -rf .vercel
rm -rf .netlify
log_success "Cleaned successfully"

# 安装依赖
log_info "Installing dependencies..."
npm ci --prefer-offline --no-audit
log_success "Dependencies installed"

# 运行 lint
log_info "Running lint..."
npm run lint
log_success "Lint passed"

# 运行类型检查
log_info "Running type check..."
npx tsc --noEmit
log_success "Type check passed"

# 运行测试(如果启用)
if [ "$RUN_TESTS" = true ]; then
    log_info "Running tests..."
    npm run test:coverage
    log_success "Tests passed"
fi

# 构建应用
if [ "$SKIP_BUILD" = false ]; then
    log_info "Building application for $ENV..."
    
    # 根据环境设置环境变量
    if [ "$ENV" = "production" ]; then
        export NODE_ENV=production
        npm run build
    elif [ "$ENV" = "preview" ]; then
        export NODE_ENV=production
        npm run build
    else
        export NODE_ENV=development
        npm run build
    fi
    
    log_success "Build completed"
    
    # 显示构建大小
    log_info "Build size:"
    du -sh dist
    du -sh dist/assets
else
    log_warning "Skipping build step"
fi

# 部署到指定平台
deploy_to_vercel() {
    log_info "Deploying to Vercel..."
    
    if ! command -v vercel &> /dev/null; then
        log_error "Vercel CLI not found. Install with: npm install -g vercel"
        exit 1
    fi
    
    if [ "$ENV" = "production" ]; then
        vercel --prod --yes
    else
        vercel --yes
    fi
    
    log_success "Deployed to Vercel successfully"
}

deploy_to_netlify() {
    log_info "Deploying to Netlify..."
    
    if ! command -v netlify &> /dev/null; then
        log_error "Netlify CLI not found. Install with: npm install -g netlify-cli"
        exit 1
    fi
    
    if [ "$ENV" = "production" ]; then
        netlify deploy --prod --dir=dist
    else
        netlify deploy --dir=dist
    fi
    
    log_success "Deployed to Netlify successfully"
}

# 根据平台部署
case $PLATFORM in
    vercel)
        deploy_to_vercel
        ;;
    netlify)
        deploy_to_netlify
        ;;
    both)
        deploy_to_vercel
        deploy_to_netlify
        ;;
    *)
        log_error "Unknown platform: $PLATFORM"
        exit 1
        ;;
esac

# 完成
log_success "🎉 Deployment completed successfully!"
log_info "Environment: $ENV"
log_info "Platform: $PLATFORM"

# 显示部署信息
if [ "$PLATFORM" = "vercel" ] || [ "$PLATFORM" = "both" ]; then
    log_info "Vercel dashboard: https://vercel.com/dashboard"
fi

if [ "$PLATFORM" = "netlify" ] || [ "$PLATFORM" = "both" ]; then
    log_info "Netlify dashboard: https://app.netlify.com"
fi
