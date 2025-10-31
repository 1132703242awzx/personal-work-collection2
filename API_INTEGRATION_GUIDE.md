# 🌐 API 集成指南

完整的 API 服务层实现，包含请求拦截器、错误处理、重试机制、响应转换和加载状态管理。

## 📚 目录

- [架构概览](#架构概览)
- [API 端点](#api-端点)
- [服务层实现](#服务层实现)
- [使用示例](#使用示例)
- [配置说明](#配置说明)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)

---

## 架构概览

### 文件结构

```
src/
├── config/
│   └── api.config.ts          # API 配置文件
├── services/
│   └── api/
│       ├── axios.instance.ts  # Axios 实例配置
│       ├── recommendation.service.ts  # 推荐服务
│       ├── techstack.service.ts       # 技术栈服务
│       ├── history.service.ts         # 历史记录服务
│       └── index.ts           # 统一导出
└── types/
    └── index.ts               # TypeScript 类型定义
```

### 核心功能

✅ **请求拦截器** - 自动添加 Token、请求 ID、时间戳
✅ **响应拦截器** - 统一处理响应格式和错误
✅ **错误处理** - 格式化错误信息，处理特定状态码
✅ **重试机制** - 自动重试失败的 GET 请求（最多 3 次）
✅ **加载状态** - 集成 Redux 状态管理
✅ **Mock 模式** - 开发环境支持 Mock 数据
✅ **TypeScript** - 完整的类型安全

---

## API 端点

### 1. 需求分析

#### POST `/api/analyze-requirements`
分析用户需求并生成技术栈推荐

**请求体:**
```typescript
{
  requirements: ProjectRequirements
}
```

**响应:**
```typescript
{
  success: true,
  data: {
    techStack: TechStack[],
    prompts: AIPrompt,
    suggestions: DevelopmentAdvice[],
    estimatedCost?: string,
    estimatedDuration?: string
  },
  timestamp: number
}
```

### 2. 技术栈服务

#### GET `/api/tech-stacks`
获取完整的技术栈数据库

**响应:**
```typescript
{
  success: true,
  data: {
    categories: {
      [key: string]: TechStack[]
    },
    trending: TechStack[],
    lastUpdated: string
  }
}
```

#### GET `/api/tech-stacks/trending`
获取热门/趋势技术栈

**响应:**
```typescript
{
  success: true,
  data: {
    stacks: TechStack[]
  }
}
```

#### GET `/api/tech-stacks/search?q=keyword&category=frontend`
搜索技术栈

**查询参数:**
- `q` - 搜索关键词
- `category` (可选) - 技术分类

### 3. AI 提示词生成

#### POST `/api/generate-prompts`
根据技术栈生成 AI 提示词

**请求体:**
```typescript
{
  techStack: TechStack[],
  requirements?: Partial<ProjectRequirements>
}
```

**响应:**
```typescript
{
  success: true,
  data: {
    prompts: AIPrompt[],
    optimizationSuggestions: string[]
  }
}
```

#### POST `/api/generate-prompts/optimize`
优化现有提示词

#### POST `/api/generate-prompts/regenerate`
基于反馈重新生成提示词

### 4. 历史记录

#### GET `/api/history?page=1&pageSize=10&sortBy=timestamp&order=desc`
获取用户历史记录

**查询参数:**
- `page` - 页码（默认: 1）
- `pageSize` - 每页数量（默认: 10）
- `sortBy` - 排序字段（timestamp | favorite）
- `order` - 排序方向（asc | desc）

#### POST `/api/history`
保存到历史记录

**请求体:**
```typescript
{
  query: string,
  requirements: ProjectRequirements,
  results: AnalysisResult
}
```

#### GET `/api/history/:id`
获取单条历史记录

#### DELETE `/api/history/:id`
删除历史记录

#### POST `/api/history/batch-delete`
批量删除历史记录

**请求体:**
```typescript
{
  ids: string[]
}
```

#### PATCH `/api/history/:id/favorite`
切换收藏状态

#### DELETE `/api/history`
清空所有历史记录

#### GET `/api/history/export?format=json`
导出历史记录

**查询参数:**
- `format` - 导出格式（json | csv）

---

## 服务层实现

### 1. API 配置 (`api.config.ts`)

```typescript
import { API_CONFIG } from '@/config/api.config';

// 基础 URL
API_CONFIG.BASE_URL  // 'http://localhost:3000/api'

// 超时设置
API_CONFIG.TIMEOUT  // 30000 (30秒)

// 重试配置
API_CONFIG.RETRY.MAX_RETRIES  // 3
API_CONFIG.RETRY.RETRY_DELAY  // 1000 (1秒)
API_CONFIG.RETRY.RETRY_STATUS_CODES  // [408, 429, 500, 502, 503, 504]

// Mock 模式
MOCK_CONFIG.ENABLED  // 开发环境默认启用
MOCK_CONFIG.DELAY  // 1500ms 模拟延迟
```

**环境变量配置 (`.env`):**

```bash
# API 基础 URL
VITE_API_BASE_URL=http://localhost:3000/api

# 启用 Mock 模式
VITE_ENABLE_MOCK=true
```

### 2. Axios 实例 (`axios.instance.ts`)

#### 请求拦截器功能

- ✅ 生成唯一请求 ID (`X-Request-ID`)
- ✅ 自动添加认证 Token (`Authorization: Bearer <token>`)
- ✅ GET 请求添加时间戳防止缓存
- ✅ 开发环境日志输出

#### 响应拦截器功能

- ✅ 统一处理响应格式
- ✅ 格式化错误信息
- ✅ 处理特定 HTTP 状态码：
  - `401` - 清除 Token，跳转登录
  - `403` - 禁止访问
  - `404` - 资源不存在
  - `429` - 请求过于频繁
  - `5xx` - 服务器错误

#### 重试机制

```typescript
// 自动重试配置
- 最多重试 3 次
- 重试延迟：1秒 × 重试次数
- 仅重试 GET 请求
- 重试状态码：408, 429, 500, 502, 503, 504
```

### 3. 推荐服务 (`recommendation.service.ts`)

```typescript
import { API } from '@/services/api';

// 分析需求
const result = await API.recommendation.analyzeRequirements(requirements);

// 生成 AI 提示词
const prompts = await API.recommendation.generatePrompts(techStack, requirements);

// 优化提示词
const optimized = await API.recommendation.optimizePrompts(prompts);

// 重新生成（基于反馈）
const newPrompt = await API.recommendation.regeneratePrompts(originalPrompt, feedback);
```

### 4. 技术栈服务 (`techstack.service.ts`)

```typescript
import { API } from '@/services/api';

// 获取所有技术栈
const database = await API.techStack.getTechStacks();

// 获取热门技术栈
const trending = await API.techStack.getTrendingTechStacks();

// 搜索技术栈
const results = await API.techStack.searchTechStacks('React', '前端框架');

// 按分类获取
const frontend = await API.techStack.getTechStacksByCategory('前端框架');
```

### 5. 历史记录服务 (`history.service.ts`)

```typescript
import { API } from '@/services/api';

// 获取历史记录（分页）
const history = await API.history.getHistory({
  page: 1,
  pageSize: 10,
  sortBy: 'timestamp',
  order: 'desc'
});

// 保存到历史
const item = await API.history.saveToHistory(query, requirements, results);

// 删除单条
await API.history.deleteHistory(id);

// 批量删除
await API.history.batchDeleteHistory([id1, id2, id3]);

// 切换收藏
const updated = await API.history.toggleFavorite(id);

// 清空所有
await API.history.clearHistory();

// 导出数据
const blob = await API.history.exportHistory('json');
```

---

## 使用示例

### 基础用法

```typescript
import { API } from '@/services/api';
import { useAppDispatch } from '@/store';
import { addNotification } from '@/store/slices/uiSlice';

function MyComponent() {
  const dispatch = useAppDispatch();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);

    try {
      const result = await API.recommendation.analyzeRequirements(requirements);
      
      console.log('分析结果:', result);
      
      dispatch(addNotification({
        type: 'success',
        message: '分析完成！'
      }));
      
      // 处理结果...
    } catch (error: any) {
      console.error('分析失败:', error);
      
      dispatch(addNotification({
        type: 'error',
        message: error.message || '分析失败'
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleSubmit} disabled={loading}>
      {loading ? '分析中...' : '开始分析'}
    </button>
  );
}
```

### 集成 Redux Thunk

```typescript
// store/slices/recommendationsSlice.ts
import { createAsyncThunk } from '@reduxjs/toolkit';
import { API } from '@/services/api';

export const fetchRecommendations = createAsyncThunk(
  'recommendations/fetch',
  async (requirements: ProjectRequirements, { rejectWithValue }) => {
    try {
      const response = await API.recommendation.analyzeRequirements(requirements);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch recommendations');
    }
  }
);

// 组件中使用
import { useAppDispatch } from '@/store';
import { fetchRecommendations } from '@/store/slices/recommendationsSlice';

function MyComponent() {
  const dispatch = useAppDispatch();

  const handleAnalyze = () => {
    dispatch(fetchRecommendations(requirements))
      .unwrap()
      .then((result) => {
        console.log('成功:', result);
      })
      .catch((error) => {
        console.error('失败:', error);
      });
  };
}
```

### 完整示例组件

参考文件: `src/components/examples/ApiExampleComponent.tsx`

该组件展示了所有 API 服务的使用方法，包括：
- 错误处理
- 加载状态管理
- Redux 通知集成
- 文件下载处理

---

## 配置说明

### Mock 模式配置

Mock 模式默认在开发环境启用，可通过环境变量控制：

```bash
# .env.development
VITE_ENABLE_MOCK=true  # 启用 Mock

# .env.production
VITE_ENABLE_MOCK=false  # 禁用 Mock
```

**Mock 数据特性:**
- ⏱️ 模拟 1.5 秒延迟
- 💾 使用 localStorage 持久化
- 📝 提供完整的示例数据
- ✅ 与真实 API 结构一致

### 认证配置

Token 存储在 `localStorage` 中：

```typescript
// 保存 Token
localStorage.setItem('auth_token', 'your-token-here');

// Axios 会自动添加到请求头：
// Authorization: Bearer your-token-here
```

### 超时配置

```typescript
// 全局超时（30秒）
API_CONFIG.TIMEOUT = 30000;

// 单次请求自定义超时
import { apiClient } from '@/services/api';

const response = await apiClient.get('/api/some-endpoint', {
  timeout: 60000  // 60秒
});
```

---

## 错误处理

### 错误格式

所有错误都被格式化为统一格式：

```typescript
{
  code: string,      // 错误代码 (HTTP_401, TIMEOUT, NETWORK_ERROR)
  message: string,   // 错误信息
  details?: any,     // 详细信息
  status?: number    // HTTP 状态码
}
```

### 错误类型

| 错误代码 | 描述 | 处理方式 |
|---------|------|---------|
| `HTTP_401` | 未授权 | 清除 Token，跳转登录 |
| `HTTP_403` | 禁止访问 | 显示权限不足提示 |
| `HTTP_404` | 资源不存在 | 显示错误信息 |
| `HTTP_429` | 请求过于频繁 | 自动重试 |
| `HTTP_5xx` | 服务器错误 | 自动重试（GET 请求） |
| `TIMEOUT` | 请求超时 | 提示用户重试 |
| `NETWORK_ERROR` | 网络错误 | 检查网络连接 |

### 错误处理示例

```typescript
try {
  const result = await API.techStack.getTechStacks();
} catch (error: any) {
  // error 已被格式化
  console.error('错误代码:', error.code);
  console.error('错误信息:', error.message);
  console.error('详细信息:', error.details);
  
  // 根据错误类型处理
  switch (error.code) {
    case 'HTTP_401':
      // 跳转登录
      break;
    case 'NETWORK_ERROR':
      // 显示网络错误提示
      break;
    case 'TIMEOUT':
      // 显示超时提示
      break;
    default:
      // 显示通用错误
      dispatch(addNotification({
        type: 'error',
        message: error.message
      }));
  }
}
```

---

## 最佳实践

### 1. 使用 TypeScript 类型

```typescript
import { ProjectRequirements, AnalyzeRequirementsResponse } from '@/types';

const requirements: ProjectRequirements = {
  projectType: 'Web 应用',
  complexity: 7,
  // ... 其他字段
};

const result: AnalyzeRequirementsResponse = 
  await API.recommendation.analyzeRequirements(requirements);
```

### 2. 统一错误处理

```typescript
// 创建通用错误处理函数
function handleApiError(error: any, dispatch: any) {
  console.error('API Error:', error);
  
  dispatch(addNotification({
    type: 'error',
    message: error.message || '操作失败，请重试'
  }));
}

// 使用
try {
  await API.recommendation.analyzeRequirements(requirements);
} catch (error) {
  handleApiError(error, dispatch);
}
```

### 3. 加载状态管理

```typescript
// 使用 Redux 管理全局加载状态
import { setLoading } from '@/store/slices/uiSlice';

dispatch(setLoading(true));
try {
  const result = await API.recommendation.analyzeRequirements(requirements);
} finally {
  dispatch(setLoading(false));
}

// 或使用局部状态
const [loading, setLoading] = useState(false);
```

### 4. 取消请求

```typescript
import { apiClient } from '@/services/api';

const controller = new AbortController();

const fetchData = async () => {
  try {
    const response = await apiClient.get('/api/data', {
      signal: controller.signal
    });
  } catch (error: any) {
    if (error.code === 'ERR_CANCELED') {
      console.log('请求已取消');
    }
  }
};

// 取消请求
controller.abort();
```

### 5. 请求去重

```typescript
// 防止重复请求
let pendingRequest: Promise<any> | null = null;

async function fetchData() {
  if (pendingRequest) {
    return pendingRequest;
  }

  pendingRequest = API.techStack.getTechStacks();
  
  try {
    return await pendingRequest;
  } finally {
    pendingRequest = null;
  }
}
```

### 6. 数据缓存

```typescript
// 简单的内存缓存
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000; // 5分钟

async function getCachedData(key: string, fetcher: () => Promise<any>) {
  const cached = cache.get(key);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }

  const data = await fetcher();
  cache.set(key, { data, timestamp: Date.now() });
  
  return data;
}

// 使用
const techStacks = await getCachedData('tech-stacks', () => 
  API.techStack.getTechStacks()
);
```

---

## 调试技巧

### 1. 开发环境日志

开发环境下，所有请求和响应都会输出到控制台：

```
[API Request req_1234567890_abc] {
  method: 'POST',
  url: '/api/analyze-requirements',
  data: { ... }
}

[API Response req_1234567890_abc] {
  status: 200,
  data: { ... }
}
```

### 2. 查看请求 ID

每个请求都有唯一 ID，方便追踪：

```typescript
// 请求头中包含
X-Request-ID: req_1234567890_abc
```

### 3. Mock 数据开关

快速切换 Mock 模式：

```typescript
// api.config.ts
export const MOCK_CONFIG = {
  ENABLED: true,  // 改为 false 使用真实 API
  DELAY: 1500,
};
```

### 4. 网络监控

使用浏览器开发者工具的 Network 面板：
- 查看请求详情
- 检查响应时间
- 分析失败原因

---

## 常见问题

### Q: 如何修改 API 基础 URL？

A: 在 `.env` 文件中设置：
```bash
VITE_API_BASE_URL=https://api.example.com
```

### Q: 如何添加自定义请求头？

A: 修改 `api.config.ts` 或在单次请求中添加：
```typescript
const response = await apiClient.get('/api/data', {
  headers: {
    'Custom-Header': 'value'
  }
});
```

### Q: 如何处理文件上传？

A: 使用 `FormData`：
```typescript
const formData = new FormData();
formData.append('file', file);

const response = await apiClient.post('/api/upload', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});
```

### Q: 如何禁用重试机制？

A: 在单次请求中禁用：
```typescript
const response = await apiClient.get('/api/data', {
  // @ts-ignore
  __skipRetry: true
});
```

---

## 总结

✅ **完整的 API 服务层** - 包含 3 个核心服务
✅ **强大的错误处理** - 统一格式化，特定状态码处理
✅ **自动重试机制** - 提高请求成功率
✅ **TypeScript 支持** - 完整的类型定义
✅ **Mock 模式** - 便于开发和测试
✅ **Redux 集成** - 状态管理和通知系统
✅ **详细的文档** - 使用示例和最佳实践

现在您可以在项目中使用这套完整的 API 服务层了！🎉
