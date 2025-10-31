# Redux Toolkit 状态管理完整指南

## 📋 目录

1. [架构概览](#架构概览)
2. [状态结构](#状态结构)
3. [Slices 详解](#slices-详解)
4. [使用指南](#使用指南)
5. [最佳实践](#最佳实践)
6. [API 参考](#api-参考)

---

## 🏗️ 架构概览

### 技术栈
- **Redux Toolkit**: 现代化的 Redux 开发工具
- **React Redux**: React 绑定库
- **TypeScript**: 完整类型支持
- **localStorage**: 状态持久化

### 文件结构
```
src/
├── store/
│   ├── index.ts                    # Store 配置
│   ├── selectors.ts                # Reselect 选择器
│   └── slices/
│       ├── requirementsSlice.ts    # 需求状态
│       ├── recommendationsSlice.ts # 推荐状态
│       ├── uiSlice.ts              # UI 状态
│       └── historySlice.ts         # 历史记录
├── components/
│   ├── ErrorBoundary.tsx           # 错误边界
│   ├── ReduxProvider.tsx           # Redux 提供者
│   └── NotificationSystem.tsx      # 通知系统
└── types/
    └── index.ts                    # 类型定义
```

---

## 📊 状态结构

### 完整状态树
```typescript
{
  requirements: {
    data: {
      projectType: string;
      targetPlatform: string[];
      complexity: number;
      budget: string;
      features: string[];
      description: string;
      timeline?: string;
      teamSize?: number;
    },
    currentStep: number;
    isValid: boolean;
  },
  
  recommendations: {
    techStack: TechStack[];
    prompts: AIPrompt | null;
    suggestions: DevelopmentAdvice[];
    loading: boolean;
    error: string | null;
  },
  
  ui: {
    loading: boolean;
    currentStep: number;
    theme: 'light' | 'dark';
    sidebarOpen: boolean;
    notifications: Notification[];
  },
  
  history: {
    items: SearchHistory[];
    loading: boolean;
    error: string | null;
  }
}
```

---

## 🔧 Slices 详解

### 1. Requirements Slice

**职责**: 管理项目需求表单数据

**Actions**:
```typescript
// 更新需求
updateRequirements(data: Partial<ProjectRequirements>)

// 重置需求
resetRequirements()

// 步骤控制
setCurrentStep(step: number)
nextStep()
previousStep()

// 验证
setValidationState(isValid: boolean)

// 草稿管理
loadFromDraft({ data, step })
```

**使用示例**:
```typescript
import { useAppDispatch } from '@/store';
import { updateRequirements, nextStep } from '@/store/slices/requirementsSlice';

const MyComponent = () => {
  const dispatch = useAppDispatch();

  const handleUpdate = () => {
    dispatch(updateRequirements({
      projectType: 'web',
      complexity: 3
    }));
    dispatch(nextStep());
  };
};
```

### 2. Recommendations Slice

**职责**: 管理 AI 推荐结果和异步请求

**Async Thunks**:
```typescript
// 获取推荐 (异步)
fetchRecommendations(requirements: ProjectRequirements)

// 重新生成提示词 (异步)
regeneratePrompts(requirements: ProjectRequirements)
```

**Actions**:
```typescript
// 清空推荐
clearRecommendations()

// 更新技术栈
updateTechStack(techStack: TechStack[])

// 清除错误
clearError()
```

**使用示例**:
```typescript
import { fetchRecommendations } from '@/store/slices/recommendationsSlice';

const handleSubmit = async () => {
  try {
    const result = await dispatch(fetchRecommendations(requirements)).unwrap();
    console.log('推荐结果:', result);
  } catch (error) {
    console.error('获取失败:', error);
  }
};
```

### 3. UI Slice

**职责**: 管理全局 UI 状态

**Actions**:
```typescript
// 加载状态
setLoading(loading: boolean)

// 步骤控制
setCurrentStep(step: number)

// 主题控制
toggleTheme()
setTheme('light' | 'dark')

// 侧边栏
toggleSidebar()
setSidebar(open: boolean)

// 通知系统
addNotification({ type, message })
removeNotification(id: string)
clearNotifications()
```

**通知类型**:
```typescript
type: 'success' | 'error' | 'warning' | 'info'
```

**使用示例**:
```typescript
import { addNotification } from '@/store/slices/uiSlice';

dispatch(addNotification({
  type: 'success',
  message: '操作成功！'
}));
```

### 4. History Slice

**职责**: 管理搜索历史记录 (含持久化)

**Async Thunks**:
```typescript
// 添加历史 (异步)
addHistoryItem({ requirements, result })

// 删除历史 (异步)
deleteHistoryItem(id: string)

// 清空历史 (异步)
clearHistory()
```

**Actions**:
```typescript
// 切换收藏
toggleFavorite(id: string)

// 批量删除
batchDelete(ids: string[])

// 导入历史
importHistory(items: SearchHistory[])
```

**持久化**: 自动保存到 localStorage，最多保留 50 条

---

## 📖 使用指南

### 1. 基础使用

#### 获取状态
```typescript
import { useAppSelector } from '@/store';
import { selectRequirements } from '@/store/selectors';

const MyComponent = () => {
  const requirements = useAppSelector(selectRequirements);
  const loading = useAppSelector(state => state.ui.loading);
  
  return <div>{requirements.projectType}</div>;
};
```

#### 更新状态
```typescript
import { useAppDispatch } from '@/store';
import { updateRequirements } from '@/store/slices/requirementsSlice';

const MyComponent = () => {
  const dispatch = useAppDispatch();

  const handleChange = (value: string) => {
    dispatch(updateRequirements({ projectType: value }));
  };
};
```

### 2. 异步操作

#### 标准异步流程
```typescript
import { fetchRecommendations } from '@/store/slices/recommendationsSlice';
import { addNotification } from '@/store/slices/uiSlice';

const handleAnalyze = async () => {
  try {
    // pending 状态会自动触发
    const result = await dispatch(fetchRecommendations(requirements)).unwrap();
    
    // 成功后的操作
    dispatch(addNotification({
      type: 'success',
      message: '分析完成！'
    }));
    
    // 保存到历史
    await dispatch(addHistoryItem({ requirements, result }));
    
  } catch (error) {
    // rejected 状态会自动触发
    dispatch(addNotification({
      type: 'error',
      message: `分析失败: ${error}`
    }));
  }
};
```

#### 监听加载状态
```typescript
const isLoading = useAppSelector(selectRecommendationsLoading);

return (
  <button disabled={isLoading}>
    {isLoading ? '加载中...' : '提交'}
  </button>
);
```

### 3. 使用 Selectors

#### 简单 Selector
```typescript
import { selectTechStack } from '@/store/selectors';

const techStack = useAppSelector(selectTechStack);
```

#### 组合 Selector (推荐)
```typescript
import { selectTechStackByCategory } from '@/store/selectors';

const techStackByCategory = useAppSelector(selectTechStackByCategory);
// 返回: { '前端框架': [...], '后端技术': [...] }
```

#### 自定义 Selector
```typescript
import { createSelector } from '@reduxjs/toolkit';

const selectMyData = createSelector(
  [selectTechStack, selectPrompts],
  (techStack, prompts) => ({
    totalItems: techStack.length,
    hasPrompts: !!prompts
  })
);
```

### 4. 表单集成示例

```typescript
import { useAppDispatch, useAppSelector } from '@/store';
import { updateRequirements, nextStep } from '@/store/slices/requirementsSlice';
import { selectRequirements, selectRequirementsStep } from '@/store/selectors';

const FormComponent = () => {
  const dispatch = useAppDispatch();
  const requirements = useAppSelector(selectRequirements);
  const currentStep = useAppSelector(selectRequirementsStep);

  const handleChange = (field: string, value: any) => {
    dispatch(updateRequirements({ [field]: value }));
  };

  const handleNext = () => {
    dispatch(nextStep());
  };

  return (
    <form>
      <input
        value={requirements.projectType || ''}
        onChange={(e) => handleChange('projectType', e.target.value)}
      />
      <button onClick={handleNext}>
        下一步 ({currentStep}/4)
      </button>
    </form>
  );
};
```

---

## 💡 最佳实践

### 1. 类型安全

✅ **推荐**: 使用类型化的 Hooks
```typescript
// 使用自定义 Hooks
import { useAppDispatch, useAppSelector } from '@/store';

// ❌ 不要使用原始 Hooks
import { useDispatch, useSelector } from 'react-redux';
```

### 2. Action 命名

✅ **推荐**: 使用语义化命名
```typescript
updateRequirements()  // ✅ 清晰
setData()            // ❌ 模糊
```

### 3. Selector 使用

✅ **推荐**: 使用 Selector 而不是直接访问状态
```typescript
// ✅ 推荐
const techStack = useAppSelector(selectTechStack);

// ❌ 不推荐
const techStack = useAppSelector(state => state.recommendations.techStack);
```

**原因**:
- 更好的代码复用
- 易于测试
- 性能优化 (memoization)

### 4. 异步错误处理

✅ **推荐**: 使用 try-catch + unwrap()
```typescript
try {
  const result = await dispatch(fetchRecommendations(data)).unwrap();
  // 处理成功
} catch (error) {
  // 处理错误
}
```

### 5. 状态标准化

✅ **推荐**: 使用扁平化结构
```typescript
// ✅ 推荐
{
  items: { '1': {...}, '2': {...} },
  ids: ['1', '2']
}

// ❌ 避免嵌套
{
  items: [
    { id: '1', nested: { ... } }
  ]
}
```

### 6. 避免状态冗余

✅ **推荐**: 只存储必要数据，派生数据用 Selector
```typescript
// ✅ Selector 计算
const selectTotalItems = createSelector(
  [selectItems],
  (items) => items.length
);

// ❌ 在状态中存储
{
  items: [...],
  totalItems: 10  // 冗余
}
```

---

## 🔌 API 参考

### Hooks

#### useAppDispatch
```typescript
const dispatch = useAppDispatch();
dispatch(action());
```

#### useAppSelector
```typescript
const data = useAppSelector(selector);
const data = useAppSelector(state => state.slice.field);
```

### Selectors

#### Requirements
```typescript
selectRequirements(state)         // 需求数据
selectRequirementsStep(state)     // 当前步骤
selectRequirementsValid(state)    // 验证状态
```

#### Recommendations
```typescript
selectTechStack(state)                  // 技术栈
selectPrompts(state)                    // 提示词
selectSuggestions(state)                // 建议
selectRecommendationsLoading(state)     // 加载状态
selectRecommendationsError(state)       // 错误信息
selectFullRecommendations(state)        // 完整推荐
selectTechStackByCategory(state)        // 分类技术栈
selectMustHaveTechStack(state)          // 必选技术栈
```

#### UI
```typescript
selectLoading(state)                    // 全局加载
selectCurrentStep(state)                // 当前步骤
selectTheme(state)                      // 主题
selectSidebarOpen(state)                // 侧边栏
selectNotifications(state)              // 通知列表
selectUnreadNotificationsCount(state)   // 未读通知数
```

#### History
```typescript
selectHistory(state)              // 历史列表
selectHistoryLoading(state)       // 加载状态
selectHistoryError(state)         // 错误信息
selectFavoriteHistory(state)      // 收藏历史
selectRecentHistory(state)        // 最近历史
selectHistoryByDate(state)        // 按日期分组
```

#### 组合 Selectors
```typescript
selectIsAppLoading(state)   // 应用是否加载中
selectHasError(state)       // 是否有错误
selectAllErrors(state)      // 所有错误消息
```

---

## 🧪 测试

### Slice 测试
```typescript
import reducer, { updateRequirements } from '@/store/slices/requirementsSlice';

describe('requirementsSlice', () => {
  it('should update requirements', () => {
    const initialState = { data: {}, currentStep: 1, isValid: false };
    const action = updateRequirements({ projectType: 'web' });
    const state = reducer(initialState, action);
    
    expect(state.data.projectType).toBe('web');
  });
});
```

### Selector 测试
```typescript
import { selectTechStack } from '@/store/selectors';

describe('selectors', () => {
  it('should select tech stack', () => {
    const state = {
      recommendations: {
        techStack: [{ name: 'React' }]
      }
    };
    
    expect(selectTechStack(state)).toHaveLength(1);
  });
});
```

---

## 🚀 性能优化

### 1. Reselect Memoization
```typescript
// 自动 memoization
const selectExpensiveData = createSelector(
  [selectTechStack],
  (techStack) => {
    // 复杂计算只在 techStack 变化时执行
    return techStack.filter(...).map(...);
  }
);
```

### 2. 批量 Dispatch
```typescript
import { batch } from 'react-redux';

batch(() => {
  dispatch(action1());
  dispatch(action2());
  dispatch(action3());
});
// 只触发一次重渲染
```

### 3. 选择性订阅
```typescript
// ✅ 只订阅需要的字段
const projectType = useAppSelector(state => state.requirements.data.projectType);

// ❌ 避免订阅整个对象
const requirements = useAppSelector(state => state.requirements);
```

---

## 🔄 数据流图

```
User Action
    ↓
Dispatch Action
    ↓
Middleware (Thunk)
    ↓
Reducer Updates State
    ↓
Store Notifies Subscribers
    ↓
Components Re-render
    ↓
LocalStorage Sync
```

---

## 📝 常见问题

### Q: 为什么使用 Redux Toolkit?
A: RTK 简化了 Redux 配置，内置了 Immer、Thunk、DevTools，减少样板代码。

### Q: 何时使用异步 Thunk?
A: 任何需要 API 调用、延迟操作或副作用的场景。

### Q: 如何调试状态?
A: 使用 Redux DevTools 浏览器扩展，可以查看每个 action 和状态变化。

### Q: 状态持久化如何工作?
A: Store 订阅状态变化，自动将指定的 slice 保存到 localStorage。

### Q: 如何清除持久化状态?
A: `localStorage.removeItem('redux_state')`

---

## 🔗 相关链接

- [Redux Toolkit 官方文档](https://redux-toolkit.js.org/)
- [React Redux Hooks](https://react-redux.js.org/api/hooks)
- [Reselect](https://github.com/reduxjs/reselect)
- [Redux DevTools](https://github.com/reduxjs/redux-devtools)

---

**💡 提示**: 查看 `src/components/examples/ReduxExampleComponent.tsx` 获取完整的实战示例！
