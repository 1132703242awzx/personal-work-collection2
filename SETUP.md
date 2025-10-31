# React + TypeScript + Vite 项目

这是一个使用 Vite、React、TypeScript、Tailwind CSS、React Router 和 Axios 构建的现代化前端项目。

## 🚀 技术栈

- **构建工具**: Vite 5
- **框架**: React 19
- **语言**: TypeScript 5
- **样式**: Tailwind CSS 3
- **路由**: React Router 6
- **HTTP 客户端**: Axios
- **代码规范**: ESLint + Prettier

## 📦 项目结构

```
react-app/
├── public/              # 静态资源
├── src/
│   ├── components/      # React 组件
│   ├── router/          # 路由配置
│   ├── services/        # API 服务
│   ├── types/           # TypeScript 类型定义
│   ├── utils/           # 工具函数 (包含 axios 配置)
│   ├── App.tsx          # 主应用组件
│   ├── index.tsx        # 应用入口
│   └── index.css        # 全局样式
├── .env                 # 环境变量
├── .eslintrc.cjs        # ESLint 配置
├── .prettierrc.json     # Prettier 配置
├── tailwind.config.js   # Tailwind CSS 配置
├── tsconfig.json        # TypeScript 配置
├── vite.config.ts       # Vite 配置
└── package.json         # 项目依赖

```

## 🛠️ 安装和运行

### 1. 安装依赖

```bash
npm install
# 或
yarn install
# 或
pnpm install
```

### 2. 开发模式

```bash
npm run dev
```

项目将在 `http://localhost:3000` 启动

### 3. 构建生产版本

```bash
npm run build
```

### 4. 预览生产构建

```bash
npm run preview
```

## 📝 可用脚本

- `npm run dev` - 启动开发服务器
- `npm run build` - 构建生产版本
- `npm run preview` - 预览生产构建
- `npm run lint` - 运行 ESLint 检查
- `npm run lint:fix` - 自动修复 ESLint 问题
- `npm run format` - 格式化代码
- `npm run format:check` - 检查代码格式

## 🔧 配置说明

### Vite 配置

- 支持路径别名: `@` 指向 `src` 目录
- 开发服务器端口: 3000
- 自动打开浏览器

### Tailwind CSS

已集成并配置好，可以直接使用 Tailwind 的 utility classes。

### Axios

HTTP 请求已配置在 `src/utils/axios.ts`，包含:

- 请求/响应拦截器
- 统一错误处理
- Token 自动添加
- 封装的 CRUD 方法

### React Router

路由配置在 `src/router/index.tsx`，已设置:

- 首页 (`/`)
- AI 顾问页 (`/advisor`)
- 关于页 (`/about`)
- 404 页面

### 环境变量

在 `.env` 文件中配置环境变量 (以 `VITE_` 开头):

```env
VITE_API_BASE_URL=http://localhost:8080/api
```

## 🎨 代码规范

项目已配置 ESLint 和 Prettier:

- ESLint: 代码质量检查
- Prettier: 代码格式化
- 保存时自动格式化 (需要 VS Code 配置)

## 📚 使用示例

### 使用 Axios 发送请求

```typescript
import { http } from '@/utils/axios';

// GET 请求
const data = await http.get('/users');

// POST 请求
const result = await http.post('/users', { name: 'John' });
```

### 使用 Tailwind CSS

```tsx
<div className="flex items-center justify-center p-4 bg-blue-500 text-white rounded-lg">
  Hello Tailwind!
</div>
```

### 使用 React Router

```tsx
import { Link, useNavigate } from 'react-router-dom';

// 链接导航
<Link to="/about">关于</Link>;

// 编程式导航
const navigate = useNavigate();
navigate('/about');
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 许可

MIT License
