# 🤖 AI 智能开发顾问系统

[![React](https://img.shields.io/badge/React-18.3.1-61dafb?logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-3178c6?logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4.21-646cff?logo=vite)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🎯 基于 AI 的智能项目需求分析和技术栈推荐系统

## ✨ 核心功能

### 🧠 智能需求分析
- **自动复杂度评估**: 基于多维度因素智能评估项目复杂度 (简单/中等/复杂/企业级)
- **智能提示词生成**: 生成结构化的 AI 分析提示词,可直接用于 ChatGPT/Claude 等工具
- **上下文理解**: 深度分析项目描述、功能需求、平台特征等信息

### 🛠️ 技术栈推荐
- **精准匹配**: 根据项目类型、复杂度、平台自动推荐最合适的技术栈
- **分层推荐**: 前端、后端、数据库、部署、测试等全栈技术推荐
- **优先级标识**: 必需(must-have)、推荐(recommended)、可选(optional)
- **实时更新**: 推荐最新、最稳定的技术版本

### 📋 开发计划生成
- **6 个开发阶段**: 需求分析 → 架构设计 → 开发实施 → 测试验证 → 部署上线 → 运维迭代
- **详细任务清单**: 每个阶段包含具体的任务列表和最佳实践
- **时间估算**: 根据复杂度智能估算各阶段所需时间
- **团队配置**: 建议所需的团队规模和角色分工

### 💡 专业建议
- **安全性**: OWASP 安全实践、数据加密、认证授权
- **性能优化**: CDN、缓存策略、数据库优化、代码分割
- **监控运维**: 日志聚合、性能监控、错误追踪、告警系统
- **成本控制**: 云服务选型、资源优化建议

### 🔌 AI 增强 (可选)
- 支持集成 **OpenAI GPT-4**、**DeepSeek**、**Claude**、**Azure OpenAI**、**Gemini** 等真实 AI
- 智能降级: API 失败时自动使用内置算法
- 无缝体验: 用户无感知切换
- **一键配置**: 5 分钟快速接入
- **成本可控**: DeepSeek 每次分析仅 ¥0.01-0.02

---

## 🚀 快速开始

### 前置要求

- Node.js >= 18.0.0
- npm >= 9.0.0 或 pnpm >= 8.0.0

### 安装依赖

```bash
# 使用 npm
npm install

# 或使用 pnpm (推荐)
pnpm install
```

### 启动开发服务器

```bash
npm run dev
```

打开浏览器访问 [http://localhost:3000](http://localhost:3000)

### 🤖 (可选) 配置 AI 增强功能

#### 5 分钟快速配置 DeepSeek

1. **获取 API Key**
   - 访问 [DeepSeek Platform](https://platform.deepseek.com/)
   - 注册并创建 API Key

2. **创建配置文件**
   在项目根目录创建 `.env.local`:
   ```bash
   VITE_AI_PROVIDER=deepseek
   VITE_AI_API_KEY=sk-your-api-key-here
   VITE_AI_MODEL=deepseek-chat
   ```

3. **重启服务器**
   ```bash
   npm run dev
   ```

4. **测试连接**
   - 访问: http://localhost:3000/ai-config
   - 验证 AI 配置状态

📖 **详细指南**: 
- [5分钟快速开始](./docs/AI_QUICK_START.md)
- [完整 AI 集成指南](./docs/AI_INTEGRATION_GUIDE.md)

### 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist` 目录。

---

## 📖 使用指南

### 1. 填写项目需求

在首页表单中填写:
- **项目名称**: 简短清晰的项目名称
- **项目描述**: 详细描述项目背景、目标和用户
- **项目类型**: 选择最匹配的类型（Web应用、移动应用、企业应用等）
- **目标平台**: 选择一个或多个目标平台
- **核心功能**: 列出 5-10 个核心功能点
- **用户故事** (可选): 描述典型用户使用场景
- **技术约束** (可选): 说明技术限制或特殊要求

### 2. 开始分析

点击 **"开始分析"** 按钮,系统将:
1. 分析项目复杂度
2. 推荐技术栈
3. 生成开发计划
4. 提供专业建议

分析过程约需 1-2 秒。

### 3. 查看结果

分析完成后,您将看到:

#### 📝 AI 提示词
- 结构化的项目分析提示词
- 可直接复制到 ChatGPT/Claude 使用
- 包含项目概述、功能需求、复杂度分析等完整信息

#### 🛠️ 技术栈推荐
- 按类别组织的技术栈（前端、后端、数据库、工具等）
- 每个技术包含版本号、推荐理由、优先级
- 根据项目特征智能匹配

#### 📅 开发计划
- 6 个开发阶段的详细规划
- 每个阶段的任务清单
- 时间估算和团队配置建议

#### 💡 额外建议
- 安全性、性能、监控等方面的专业建议
- 根据项目特征提供针对性建议

### 4. 导出结果

- **复制 AI 提示词**: 一键复制到剪贴板
- **重新分析**: 修改需求后重新生成结果

---

## 🎯 示例场景

### 场景 1: 企业知识管理系统

**输入**:
```
项目名称: 企业知识管理系统
项目描述: 为企业提供知识库管理、文档协作和智能搜索功能
项目类型: 企业应用
目标平台: Web、移动端
核心功能:
  - 用户权限管理
  - 文档在线编辑
  - 全文搜索
  - 版本控制
  - 评论和协作
  - 知识图谱
  - 智能推荐
  - 数据统计分析
```

**输出**:
- 复杂度: `complex` (评分: 8/12)
- 推荐技术栈: React 18 + TypeScript, NestJS, PostgreSQL, Redis, Elasticsearch
- 开发周期: 10-16 周
- 团队规模: 7-8 人

### 场景 2: 简单个人博客

**输入**:
```
项目名称: 个人技术博客
项目描述: 个人技术博客,支持文章发布、评论和 RSS 订阅
项目类型: 博客
目标平台: Web
核心功能:
  - 文章发布和编辑
  - Markdown 支持
  - 评论系统
  - 标签分类
  - RSS 订阅
```

**输出**:
- 复杂度: `simple` (评分: 2/12)
- 推荐技术栈: React 18 + Vite, Express.js, MongoDB
- 开发周期: 4-6 周
- 团队规模: 2-3 人

---

## 🔧 配置

### 环境变量

复制 `.env.example` 到 `.env.local`:

```bash
cp .env.example .env.local
```

### 集成真实 AI API (可选)

如果您想使用真实的 AI API 增强分析能力,可以配置:

#### OpenAI GPT-4
```bash
VITE_AI_API_ENDPOINT=https://api.openai.com/v1/chat/completions
VITE_AI_API_KEY=sk-your-openai-api-key-here
```

#### Claude
```bash
VITE_AI_API_ENDPOINT=https://api.anthropic.com/v1/messages
VITE_AI_API_KEY=sk-ant-your-claude-api-key-here
```

详细配置指南请参考 [AI 分析功能指南](./docs/AI_ANALYSIS_GUIDE.md)

---

## 📁 项目结构

```
react-app/
├── src/
│   ├── components/          # React 组件
│   │   ├── ProjectInput.tsx    # 项目需求输入表单
│   │   └── ResultDisplay.tsx   # 分析结果展示
│   ├── services/            # 业务逻辑
│   │   └── AIAdvisorService.ts # AI 分析服务
│   ├── types/               # TypeScript 类型定义
│   │   └── index.ts
│   ├── utils/               # 工具函数
│   ├── App.tsx              # 主应用组件
│   └── index.tsx            # 应用入口
├── docs/                    # 文档
│   ├── AI_ANALYSIS_GUIDE.md    # AI 分析功能详细指南
│   ├── DEPLOYMENT.md           # 部署指南
│   ├── QUICK_DEPLOY.md         # 快速部署
│   ├── PERFORMANCE.md          # 性能优化文档
│   └── TESTING.md              # 测试文档
├── public/                  # 静态资源
├── .github/                 # GitHub 配置
│   └── workflows/
│       └── ci-cd.yml           # CI/CD 流程
├── scripts/                 # 部署脚本
│   ├── deploy.sh
│   └── deploy.ps1
├── vite.config.ts          # Vite 配置
├── tsconfig.json           # TypeScript 配置
├── package.json            # 项目依赖
└── README.md               # 项目说明
```

---

## 🛠️ 技术栈

### 核心技术
- **React 18.3.1** - 前端框架
- **TypeScript 5.3.3** - 类型安全
- **Vite 5.4.21** - 构建工具

### 开发工具
- **ESLint** - 代码检查
- **Prettier** - 代码格式化
- **Vitest** - 单元测试
- **Cypress** - E2E 测试

### 部署
- **Vercel** - 主要部署平台
- **Netlify** - 备选部署平台
- **GitHub Actions** - CI/CD 流程

---

## 📚 文档

- [AI 分析功能详细指南](./docs/AI_ANALYSIS_GUIDE.md) - 核心功能说明
- [部署指南](./docs/DEPLOYMENT.md) - 完整部署文档
- [快速部署](./docs/QUICK_DEPLOY.md) - 一键部署指南
- [性能优化文档](./docs/PERFORMANCE.md) - 性能优化最佳实践
- [测试文档](./docs/TESTING.md) - 测试策略和用例

---

## 🚢 部署

### Vercel 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/react-app)

### Netlify 一键部署

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/react-app)

### 手动部署

详见 [部署指南](./docs/DEPLOYMENT.md)

---

## 🧪 测试

```bash
# 运行单元测试
npm run test

# 运行 E2E 测试
npm run test:e2e

# 生成测试覆盖率报告
npm run test:coverage
```

---

## 📈 性能

- ⚡ Lighthouse 性能评分: **95+**
- 📦 初始加载时间: **< 1s**
- 🎨 首次内容绘制 (FCP): **< 0.8s**
- 🖼️ 最大内容绘制 (LCP): **< 1.5s**
- ⚙️ 代码分割: 自动按路由和组件分割

详见 [性能优化文档](./docs/PERFORMANCE.md)

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议!

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👥 作者

- 开发者: Your Name
- 邮箱: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 致谢

- [React](https://reactjs.org/) - 优秀的前端框架
- [TypeScript](https://www.typescriptlang.org/) - JavaScript 类型超集
- [Vite](https://vitejs.dev/) - 极速的构建工具
- [Ant Design](https://ant.design/) - 企业级 UI 设计语言

---

## 📞 支持

如有问题或建议,请:
- 提交 [Issue](https://github.com/yourusername/react-app/issues)
- 发送邮件至 your.email@example.com
- 加入讨论群: [链接]

---

**⭐ 如果这个项目对您有帮助,请给个 Star!**


### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
