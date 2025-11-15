# 🚀 部署指南

本文档提供完整的项目部署指南,包括 Vercel、Netlify、GitHub Actions CI/CD 和性能监控配置。

## 📋 目录

- [快速开始](#快速开始)
- [环境变量配置](#环境变量配置)
- [部署到 Vercel](#部署到-vercel)
- [部署到 Netlify](#部署到-netlify)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [性能监控](#性能监控)
- [构建优化](#构建优化)
- [PWA 配置](#pwa-配置)
- [故障排除](#故障排除)

---

## 🚀 快速开始

### 前置要求

- Node.js 18+ 
- npm 9+
- Git
- Vercel/Netlify 账号

### 本地构建

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

---

## 🔐 环境变量配置

### 1. 创建环境变量文件

复制 `.env.example` 并根据环境创建对应的文件:

```bash
# 开发环境
cp .env.example .env.development

# 生产环境
cp .env.example .env.production

# 本地覆盖(不提交到 Git)
cp .env.example .env.local
```

### 2. 必需的环境变量

```bash
# 应用配置
VITE_APP_TITLE=React AI Advisor
VITE_APP_DESCRIPTION=智能项目顾问助手

# API 配置
VITE_API_BASE_URL=https://api.yourdomain.com/api
VITE_API_TIMEOUT=30000
VITE_API_KEY=your_api_key_here

# 功能开关
VITE_ENABLE_PERFORMANCE_MONITORING=true
VITE_ENABLE_ERROR_TRACKING=true
VITE_ENABLE_ANALYTICS=true

# 第三方服务
VITE_SENTRY_DSN=your_sentry_dsn
VITE_GA_ID=your_google_analytics_id
```

### 3. 环境变量优先级

```
.env.local > .env.[mode].local > .env.[mode] > .env
```

---

## 🎯 部署到 Vercel

### 方法 1: 通过 Vercel CLI

#### 安装 Vercel CLI

```bash
npm install -g vercel
```

#### 登录

```bash
vercel login
```

#### 部署

```bash
# 部署到预览环境
vercel

# 部署到生产环境
vercel --prod
```

#### 使用脚本部署

```bash
# Linux/Mac
chmod +x scripts/deploy.sh
./scripts/deploy.sh -e production -p vercel -t

# Windows
.\scripts\deploy.ps1 -Env production -Platform vercel -Test
```

### 方法 2: 通过 Vercel Dashboard

1. **连接 Git 仓库**
   - 访问 [vercel.com](https://vercel.com)
   - 点击 "New Project"
   - 导入 GitHub 仓库

2. **配置项目**
   ```
   Framework Preset: Vite
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

3. **设置环境变量**
   - 进入 "Settings" → "Environment Variables"
   - 添加所有必需的环境变量
   - 为不同环境设置不同的值

4. **部署**
   - 点击 "Deploy"
   - 等待构建完成

### Vercel 配置文件

`vercel.json` 已配置:
- ✅ 自动 HTTPS
- ✅ 静态资源缓存
- ✅ 安全头设置
- ✅ SPA 路由重写
- ✅ GitHub 集成

---

## 🌐 部署到 Netlify

### 方法 1: 通过 Netlify CLI

#### 安装 Netlify CLI

```bash
npm install -g netlify-cli
```

#### 登录

```bash
netlify login
```

#### 初始化

```bash
netlify init
```

#### 部署

```bash
# 部署到预览环境
netlify deploy

# 部署到生产环境
netlify deploy --prod
```

#### 使用脚本部署

```bash
# Linux/Mac
./scripts/deploy.sh -e production -p netlify -t

# Windows
.\scripts\deploy.ps1 -Env production -Platform netlify -Test
```

### 方法 2: 通过 Netlify Dashboard

1. **连接 Git 仓库**
   - 访问 [app.netlify.com](https://app.netlify.com)
   - 点击 "New site from Git"
   - 选择仓库

2. **配置构建设置**
   ```
   Build command: npm run build
   Publish directory: dist
   ```

3. **设置环境变量**
   - 进入 "Site settings" → "Environment variables"
   - 添加所有必需的环境变量

4. **部署**
   - 点击 "Deploy site"
   - 等待构建完成

### Netlify 配置文件

`netlify.toml` 已配置:
- ✅ 构建优化
- ✅ 资源压缩
- ✅ 缓存策略
- ✅ 重定向规则
- ✅ Lighthouse 插件
- ✅ 表单处理

---

## ⚙️ GitHub Actions CI/CD

### 配置步骤

#### 1. 设置 GitHub Secrets

进入仓库 Settings → Secrets and variables → Actions，添加以下 secrets:

**Vercel 部署:**
```
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id
```

**Netlify 部署:**
```
NETLIFY_AUTH_TOKEN=your_netlify_token
NETLIFY_SITE_ID=your_site_id
```

**其他服务:**
```
CODECOV_TOKEN=your_codecov_token
SNYK_TOKEN=your_snyk_token
SLACK_WEBHOOK=your_slack_webhook
```

**应用环境变量:**
```
VITE_APP_TITLE=your_app_title
VITE_API_BASE_URL=your_api_url
VITE_SENTRY_DSN=your_sentry_dsn
VITE_GA_ID=your_ga_id
```

#### 2. 获取 Token

**Vercel Token:**
1. 访问 [vercel.com/account/tokens](https://vercel.com/account/tokens)
2. 创建新 Token
3. 获取 Org ID 和 Project ID:
   ```bash
   vercel link
   cat .vercel/project.json
   ```

**Netlify Token:**
1. 访问 [app.netlify.com/user/applications](https://app.netlify.com/user/applications)
2. 创建 Personal Access Token
3. 获取 Site ID 从网站设置

#### 3. CI/CD 流程

`.github/workflows/ci-cd.yml` 包含:

✅ **Lint & Test** - 代码检查和测试
✅ **TypeScript Check** - 类型检查
✅ **Build** - 构建应用(production & preview)
✅ **E2E Test** - Cypress 端到端测试
✅ **Lighthouse** - 性能测试
✅ **Security Scan** - 安全扫描
✅ **Deploy** - 自动部署到 Vercel/Netlify
✅ **Notifications** - Slack 通知

#### 4. 触发条件

- **Push to main/develop** - 完整 CI/CD 流程
- **Pull Request** - 测试和预览部署
- **Manual trigger** - 手动触发

#### 5. 查看结果

访问 GitHub Actions 标签页查看:
- 构建日志
- 测试结果
- 部署状态
- 性能报告

---

## 📊 性能监控

### Web Vitals 监控

项目集成了 Web Vitals 监控,自动追踪:

- **LCP** (Largest Contentful Paint) - 最大内容绘制
- **FID** (First Input Delay) - 首次输入延迟
- **CLS** (Cumulative Layout Shift) - 累积布局偏移
- **FCP** (First Contentful Paint) - 首次内容绘制
- **TTFB** (Time to First Byte) - 首字节时间
- **INP** (Interaction to Next Paint) - 交互响应

### 配置性能监控

在 `src/utils/performance.ts` 中配置:

```typescript
export const performanceConfig = {
  enabled: true,
  sampleRate: 1.0,
  endpoint: '/api/performance',
  thresholds: {
    LCP: { good: 2500, needsImprovement: 4000 },
    FID: { good: 100, needsImprovement: 300 },
    CLS: { good: 0.1, needsImprovement: 0.25 },
  },
};
```

### 启用监控

在 `src/main.tsx` 中:

```typescript
import { initPerformanceMonitoring } from '@/utils/performance';

// 初始化性能监控
initPerformanceMonitoring();
```

### 查看性能数据

**开发环境:**
- 打开浏览器控制台查看性能日志

**生产环境:**
- Vercel Analytics: [vercel.com/analytics](https://vercel.com/analytics)
- Netlify Analytics: [app.netlify.com/analytics](https://app.netlify.com/analytics)
- Google Analytics: 查看 Web Vitals 事件
- 自定义端点: 查看 `/api/performance` 数据

---

## ⚡ 构建优化

### 代码分割

`vite.config.ts` 已配置智能代码分割:

```typescript
manualChunks: {
  'react-vendor': ['react', 'react-dom', 'react-router-dom'],
  'redux-vendor': ['@reduxjs/toolkit', 'react-redux'],
  'animation-vendor': ['framer-motion'],
  'utils-vendor': ['axios', 'date-fns'],
}
```

### 压缩优化

- ✅ Gzip 压缩
- ✅ Brotli 压缩
- ✅ Terser 代码压缩
- ✅ CSS 代码分割

### 静态资源优化

```typescript
assetFileNames: (assetInfo) => {
  const ext = assetInfo.name?.split('.').pop();
  
  if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(ext)) {
    return 'assets/images/[name]-[hash][extname]';
  }
  if (/woff2?|eot|ttf|otf/i.test(ext)) {
    return 'assets/fonts/[name]-[hash][extname]';
  }
  return 'assets/[ext]/[name]-[hash][extname]';
}
```

### 打包分析

```bash
# 生成打包分析报告
ANALYZE=true npm run build

# 报告将在 dist/stats.html
```

### 性能优化建议

1. **懒加载路由**
   ```typescript
   const Home = lazy(() => import('@/pages/Home'));
   ```

2. **图片优化**
   - 使用 WebP 格式
   - 实现懒加载
   - 使用响应式图片

3. **预加载关键资源**
   ```html
   <link rel="preload" href="/fonts/main.woff2" as="font" />
   ```

4. **缓存策略**
   - 静态资源: 1 年强缓存
   - HTML: 无缓存,每次验证

---

## 📱 PWA 配置

### Service Worker

项目支持 PWA,配置文件:
- `public/manifest.json` - Web App Manifest
- `public/sw.js` - Service Worker(需创建)

### 启用 PWA

1. **安装 PWA 插件**
   ```bash
   npm install vite-plugin-pwa -D
   ```

2. **配置 vite.config.ts**
   ```typescript
   import { VitePWA } from 'vite-plugin-pwa';
   
   plugins: [
     VitePWA({
       registerType: 'autoUpdate',
       manifest: {
         name: 'React AI Advisor',
         short_name: 'AI Advisor',
         theme_color: '#6366f1',
       },
     }),
   ],
   ```

3. **测试 PWA**
   ```bash
   npm run build
   npm run preview
   ```
   
   使用 Lighthouse 测试 PWA 分数

---

## 🐛 故障排除

### 构建失败

**问题: 内存不足**
```bash
# 增加 Node.js 内存限制
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

**问题: 依赖冲突**
```bash
# 清除缓存重新安装
rm -rf node_modules package-lock.json
npm install
```

### 部署失败

**Vercel 部署失败:**
1. 检查环境变量是否正确设置
2. 查看构建日志
3. 确认 `vercel.json` 配置正确

**Netlify 部署失败:**
1. 检查 `netlify.toml` 配置
2. 确认构建命令正确
3. 查看部署日志

### 环境变量不生效

1. 确保变量名以 `VITE_` 开头
2. 重启开发服务器
3. 清除构建缓存
4. 检查部署平台的环境变量设置

### 性能问题

1. 运行打包分析: `ANALYZE=true npm run build`
2. 检查大文件: `du -sh dist/assets/*`
3. 使用 Lighthouse 测试
4. 查看 Web Vitals 指标

---

## 📚 相关资源

- [Vite 文档](https://vitejs.dev/)
- [Vercel 文档](https://vercel.com/docs)
- [Netlify 文档](https://docs.netlify.com/)
- [GitHub Actions 文档](https://docs.github.com/actions)
- [Web Vitals](https://web.dev/vitals/)
- [PWA 指南](https://web.dev/progressive-web-apps/)

---

## 🆘 获取帮助

遇到问题?

1. 查看 [GitHub Issues](https://github.com/yourusername/react-app/issues)
2. 阅读 [故障排除](#故障排除) 部分
3. 提交新 Issue

---

## ✅ 部署检查清单

部署前确保:

- [ ] 所有测试通过
- [ ] 代码已 lint
- [ ] 类型检查通过
- [ ] 环境变量已配置
- [ ] 构建成功
- [ ] PWA 配置正确(如果启用)
- [ ] 性能指标达标
- [ ] 安全头已设置
- [ ] 缓存策略已配置
- [ ] 监控已启用
- [ ] CI/CD 配置正确
- [ ] 文档已更新

祝部署顺利! 🎉
