# 🚀 快速部署参考

## 一分钟部署

### Vercel (推荐)

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录
vercel login

# 3. 部署
vercel --prod
```

### Netlify

```bash
# 1. 安装 Netlify CLI
npm install -g netlify-cli

# 2. 登录
netlify login

# 3. 部署
netlify deploy --prod
```

---

## 常用命令

```bash
# 🏗️ 构建
npm run build              # 生产构建
npm run build:analyze      # 带分析的构建
npm run preview            # 预览构建结果

# 🧪 测试
npm run test               # 运行测试
npm run test:coverage      # 测试覆盖率
npm run test:e2e           # E2E 测试

# 🔍 检查
npm run lint               # 代码检查
npm run typecheck          # 类型检查
npm run format:check       # 格式检查

# 🚀 部署
npm run deploy:vercel      # Vercel 生产部署
npm run deploy:netlify     # Netlify 生产部署
npm run deploy:preview     # 预览部署

# 🧹 清理
npm run clean              # 清理构建文件
```

---

## 环境变量快速配置

```bash
# 1. 复制示例文件
cp .env.example .env.local

# 2. 编辑文件
nano .env.local  # 或使用你喜欢的编辑器

# 3. 必填项
VITE_API_BASE_URL=https://your-api.com/api
VITE_APP_TITLE=Your App Name
```

---

## GitHub Actions 快速设置

### 1. 添加 Secrets

访问: `Settings` → `Secrets and variables` → `Actions`

**Vercel:**
```
VERCEL_TOKEN=xxx
VERCEL_ORG_ID=xxx
VERCEL_PROJECT_ID=xxx
```

**Netlify:**
```
NETLIFY_AUTH_TOKEN=xxx
NETLIFY_SITE_ID=xxx
```

### 2. 推送代码

```bash
git add .
git commit -m "feat: setup deployment"
git push origin main
```

✅ 自动部署开始!

---

## 获取部署 Token

### Vercel Token

1. 访问: https://vercel.com/account/tokens
2. 点击 "Create Token"
3. 复制 token

**获取项目 ID:**
```bash
vercel link
cat .vercel/project.json
```

### Netlify Token

1. 访问: https://app.netlify.com/user/applications
2. 创建 "Personal Access Token"
3. 复制 token

**获取 Site ID:**
- 在 Netlify Dashboard → Site Settings → Site ID

---

## 性能检查清单

```bash
# ✅ 运行前检查
npm run lint           # 无错误
npm run typecheck      # 通过
npm run test:coverage  # 覆盖率 > 70%

# ✅ 构建检查
npm run build          # 构建成功
npm run build:analyze  # 查看打包大小

# ✅ 预览检查
npm run preview        # 本地预览
# 打开 Lighthouse 测试性能
```

---

## 故障排除

### 构建失败?

```bash
# 清理并重新安装
npm run clean
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 部署失败?

1. 检查环境变量是否设置
2. 查看构建日志
3. 确认 token 是否正确
4. 验证 vercel.json/netlify.toml 配置

### 环境变量不生效?

1. 变量名必须以 `VITE_` 开头
2. 重启开发服务器
3. 检查部署平台的环境变量设置

---

## 性能优化快速提示

```typescript
// 1. 懒加载路由
const Home = lazy(() => import('@/pages/Home'));

// 2. 使用 React.memo
export default memo(MyComponent);

// 3. 代码分割
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// 4. 图片优化
<img src="image.webp" loading="lazy" />
```

---

## 监控设置

### 开发环境
- 打开浏览器控制台查看性能日志

### 生产环境
- Vercel Analytics: https://vercel.com/analytics
- Netlify Analytics: https://app.netlify.com/analytics
- Google Analytics: 配置 `VITE_GA_ID`

---

## 部署检查清单

- [ ] 代码已提交到 Git
- [ ] 测试全部通过
- [ ] 环境变量已配置
- [ ] GitHub Secrets 已设置
- [ ] 构建成功
- [ ] 本地预览正常
- [ ] Lighthouse 分数 > 90

✅ 准备就绪,开始部署!

---

## 🆘 需要帮助?

- 📖 完整文档: [DEPLOYMENT.md](./DEPLOYMENT.md)
- 🧪 测试文档: [TESTING.md](./TESTING.md)
- 📦 设置总结: [DEPLOYMENT_SETUP_SUMMARY.md](./DEPLOYMENT_SETUP_SUMMARY.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/react-app/issues)

---

## 🎉 快速开始示例

```bash
# 完整流程(5分钟)
git clone <repo-url>
cd react-app
npm install
cp .env.example .env.local
# 编辑 .env.local
npm run dev              # 开发
npm run build            # 构建
vercel --prod            # 部署
```

完成! 🚀
