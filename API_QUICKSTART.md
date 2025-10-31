# 🚀 API 服务快速开始

5 分钟快速掌握 API 服务层使用方法。

## 📦 安装

所有依赖已安装完成：
- ✅ axios - HTTP 客户端
- ✅ @reduxjs/toolkit - 状态管理
- ✅ react-redux - React 绑定

## 🎯 基础使用

### 1. 导入 API 服务

```typescript
import { API } from '@/services/api';
```

### 2. 调用 API

```typescript
// 分析需求
const result = await API.recommendation.analyzeRequirements(requirements);

// 获取技术栈
const techStacks = await API.techStack.getTechStacks();

// 保存历史
await API.history.saveToHistory(query, requirements, results);
```

### 3. 错误处理

```typescript
try {
  const result = await API.recommendation.analyzeRequirements(requirements);
  console.log('成功:', result);
} catch (error: any) {
  console.error('失败:', error.message);
}
```

## 📝 完整示例

### React 组件中使用

```typescript
import { useState } from 'react';
import { API } from '@/services/api';
import { useAppDispatch } from '@/store';
import { addNotification } from '@/store/slices/uiSlice';
import { ProjectRequirements } from '@/types';

function AnalyzeComponent() {
  const dispatch = useAppDispatch();
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);

    const requirements: ProjectRequirements = {
      projectType: 'Web 应用',
      complexity: 7,
      budget: '10-30万',
      features: ['用户认证', '数据分析'],
      description: '企业管理系统',
      targetPlatform: ['Web'],
    };

    try {
      // 调用 API
      const result = await API.recommendation.analyzeRequirements(requirements);
      
      console.log('分析结果:', result);
      
      // 显示成功通知
      dispatch(addNotification({
        type: 'success',
        message: '需求分析完成！'
      }));
      
      // 处理结果...
      
    } catch (error: any) {
      // 显示错误通知
      dispatch(addNotification({
        type: 'error',
        message: error.message || '分析失败'
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <button 
      onClick={handleAnalyze} 
      disabled={loading}
      className="px-4 py-2 bg-blue-600 text-white rounded"
    >
      {loading ? '分析中...' : '开始分析'}
    </button>
  );
}
```

## 🔌 集成 Redux Thunk

### 创建异步 Thunk

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
      return rejectWithValue(error.message);
    }
  }
);
```

### 在组件中使用

```typescript
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchRecommendations } from '@/store/slices/recommendationsSlice';

function Component() {
  const dispatch = useAppDispatch();
  const { loading, error } = useAppSelector(state => state.recommendations);

  const handleClick = () => {
    dispatch(fetchRecommendations(requirements))
      .unwrap()
      .then(result => {
        console.log('成功:', result);
      })
      .catch(error => {
        console.error('失败:', error);
      });
  };

  return (
    <div>
      {loading && <p>加载中...</p>}
      {error && <p>错误: {error}</p>}
      <button onClick={handleClick}>分析</button>
    </div>
  );
}
```

## 🎨 所有可用的 API

### 推荐服务 (`API.recommendation`)

```typescript
// 分析需求并生成推荐
const result = await API.recommendation.analyzeRequirements(requirements);

// 生成 AI 提示词
const prompts = await API.recommendation.generatePrompts(techStack, requirements);

// 优化提示词
const optimized = await API.recommendation.optimizePrompts(prompts);

// 重新生成提示词
const newPrompt = await API.recommendation.regeneratePrompts(prompt, feedback);
```

### 技术栈服务 (`API.techStack`)

```typescript
// 获取所有技术栈
const database = await API.techStack.getTechStacks();

// 获取热门技术栈
const trending = await API.techStack.getTrendingTechStacks();

// 搜索技术栈
const results = await API.techStack.searchTechStacks('React', '前端框架');

// 按分类获取
const frontend = await API.techStack.getTechStacksByCategory('前端框架');
```

### 历史记录服务 (`API.history`)

```typescript
// 获取历史记录
const history = await API.history.getHistory({ page: 1, pageSize: 10 });

// 获取单条记录
const item = await API.history.getHistoryItem(id);

// 保存到历史
const saved = await API.history.saveToHistory(query, requirements, results);

// 删除记录
await API.history.deleteHistory(id);

// 批量删除
await API.history.batchDeleteHistory([id1, id2, id3]);

// 切换收藏
const updated = await API.history.toggleFavorite(id);

// 清空历史
await API.history.clearHistory();

// 导出历史
const blob = await API.history.exportHistory('json');
```

## ⚙️ 配置

### 环境变量 (`.env`)

```bash
# API 基础 URL
VITE_API_BASE_URL=http://localhost:3000/api

# 启用 Mock 模式（开发环境）
VITE_ENABLE_MOCK=true
```

### Mock 模式

开发环境默认启用 Mock 模式，返回模拟数据：

```typescript
// config/api.config.ts
export const MOCK_CONFIG = {
  ENABLED: true,   // 是否启用 Mock
  DELAY: 1500,     // 模拟延迟（毫秒）
};
```

**Mock 特性:**
- 💾 使用 localStorage 持久化
- ⏱️ 模拟真实延迟
- 📝 完整的示例数据
- ✅ 与真实 API 结构一致

### 认证配置

API 会自动从 localStorage 读取 Token：

```typescript
// 保存 Token
localStorage.setItem('auth_token', 'your-token-here');

// API 会自动添加到请求头:
// Authorization: Bearer your-token-here
```

## 🛠️ 常用模式

### 1. 加载状态 + 错误处理

```typescript
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

const fetchData = async () => {
  setLoading(true);
  setError(null);

  try {
    const result = await API.techStack.getTechStacks();
    // 处理结果...
  } catch (err: any) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};
```

### 2. 通知集成

```typescript
import { useAppDispatch } from '@/store';
import { addNotification } from '@/store/slices/uiSlice';

const dispatch = useAppDispatch();

try {
  const result = await API.recommendation.analyzeRequirements(requirements);
  
  dispatch(addNotification({
    type: 'success',
    message: '分析完成！'
  }));
} catch (error: any) {
  dispatch(addNotification({
    type: 'error',
    message: error.message || '操作失败'
  }));
}
```

### 3. 文件下载

```typescript
const handleExport = async () => {
  try {
    const blob = await API.history.exportHistory('json');
    
    // 创建下载链接
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `history_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    dispatch(addNotification({
      type: 'success',
      message: '导出成功'
    }));
  } catch (error: any) {
    dispatch(addNotification({
      type: 'error',
      message: '导出失败'
    }));
  }
};
```

## 🐛 调试

### 查看请求日志

开发环境下，所有请求都会输出到控制台：

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

### 切换 Mock 模式

```typescript
// config/api.config.ts
export const MOCK_CONFIG = {
  ENABLED: false,  // 改为 false 使用真实 API
};
```

## 📚 更多资源

- 📖 [完整 API 文档](./API_INTEGRATION_GUIDE.md)
- 🎓 [Redux 使用指南](./REDUX_GUIDE.md)
- ⚡ [Redux 快速开始](./REDUX_QUICKSTART.md)
- 💡 [API 示例组件](./src/components/examples/ApiExampleComponent.tsx)

## ✅ 检查清单

在开始使用前，确保：

- ✅ 所有依赖已安装 (`npm install`)
- ✅ 环境变量已配置 (`.env` 文件)
- ✅ Redux store 已集成 (`src/index.tsx`)
- ✅ 了解基本的 async/await 语法
- ✅ 熟悉 TypeScript 类型定义

## 🎉 开始使用

现在您已经准备好使用 API 服务层了！

参考示例组件 `src/components/examples/ApiExampleComponent.tsx` 查看完整的使用示例。

有问题？查看完整文档：[API_INTEGRATION_GUIDE.md](./API_INTEGRATION_GUIDE.md)
