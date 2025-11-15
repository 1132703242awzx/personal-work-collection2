# Redux Toolkit 快速入门

## 🚀 5分钟上手

### 1. 在组件中读取状态

```typescript
import { useAppSelector } from '@/store';
import { selectRequirements } from '@/store/selectors';

function MyComponent() {
  // 方式 1: 使用 selector
  const requirements = useAppSelector(selectRequirements);
  
  // 方式 2: 直接访问
  const loading = useAppSelector(state => state.ui.loading);
  
  return <div>{requirements.projectType}</div>;
}
```

### 2. 更新状态

```typescript
import { useAppDispatch } from '@/store';
import { updateRequirements } from '@/store/slices/requirementsSlice';

function MyComponent() {
  const dispatch = useAppDispatch();
  
  const handleUpdate = () => {
    dispatch(updateRequirements({
      projectType: 'web',
      complexity: 3
    }));
  };
  
  return <button onClick={handleUpdate}>更新</button>;
}
```

### 3. 异步操作

```typescript
import { fetchRecommendations } from '@/store/slices/recommendationsSlice';
import { addNotification } from '@/store/slices/uiSlice';

function MyComponent() {
  const dispatch = useAppDispatch();
  
  const handleSubmit = async () => {
    try {
      const result = await dispatch(fetchRecommendations(data)).unwrap();
      dispatch(addNotification({
        type: 'success',
        message: '成功！'
      }));
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        message: '失败'
      }));
    }
  };
}
```

### 4. 显示通知

```typescript
import { addNotification } from '@/store/slices/uiSlice';

// 成功通知
dispatch(addNotification({
  type: 'success',
  message: '操作成功！'
}));

// 错误通知
dispatch(addNotification({
  type: 'error',
  message: '操作失败'
}));

// 警告通知
dispatch(addNotification({
  type: 'warning',
  message: '请注意'
}));

// 信息通知
dispatch(addNotification({
  type: 'info',
  message: '提示信息'
}));
```

### 5. 历史记录

```typescript
import { addHistoryItem, deleteHistoryItem } from '@/store/slices/historySlice';
import { selectHistory } from '@/store/selectors';

function HistoryComponent() {
  const dispatch = useAppDispatch();
  const history = useAppSelector(selectHistory);
  
  // 添加历史
  const handleAdd = async () => {
    await dispatch(addHistoryItem({ requirements, result }));
  };
  
  // 删除历史
  const handleDelete = (id: string) => {
    dispatch(deleteHistoryItem(id));
  };
  
  return (
    <div>
      {history.map(item => (
        <div key={item.id}>
          {item.requirements.projectType}
          <button onClick={() => handleDelete(item.id)}>删除</button>
        </div>
      ))}
    </div>
  );
}
```

## 📦 常用 Selectors

```typescript
import {
  // Requirements
  selectRequirements,
  selectRequirementsStep,
  
  // Recommendations
  selectTechStack,
  selectPrompts,
  selectTechStackByCategory,
  selectMustHaveTechStack,
  
  // UI
  selectLoading,
  selectTheme,
  selectNotifications,
  
  // History
  selectHistory,
  selectFavoriteHistory,
  selectRecentHistory,
  
  // 组合
  selectIsAppLoading,
  selectHasError,
} from '@/store/selectors';
```

## 🎯 常用 Actions

### Requirements
```typescript
import {
  updateRequirements,
  resetRequirements,
  nextStep,
  previousStep,
  setCurrentStep,
} from '@/store/slices/requirementsSlice';
```

### Recommendations
```typescript
import {
  fetchRecommendations,    // 异步
  regeneratePrompts,       // 异步
  clearRecommendations,
  clearError,
} from '@/store/slices/recommendationsSlice';
```

### UI
```typescript
import {
  setLoading,
  toggleTheme,
  addNotification,
  removeNotification,
} from '@/store/slices/uiSlice';
```

### History
```typescript
import {
  addHistoryItem,      // 异步
  deleteHistoryItem,   // 异步
  clearHistory,        // 异步
  toggleFavorite,
  batchDelete,
} from '@/store/slices/historySlice';
```

## 💡 实战示例

### 完整的表单提交流程

```typescript
import { useAppDispatch, useAppSelector } from '@/store';
import { updateRequirements, resetRequirements } from '@/store/slices/requirementsSlice';
import { fetchRecommendations } from '@/store/slices/recommendationsSlice';
import { addNotification } from '@/store/slices/uiSlice';
import { addHistoryItem } from '@/store/slices/historySlice';
import { selectRequirements, selectRecommendationsLoading } from '@/store/selectors';

function SmartForm() {
  const dispatch = useAppDispatch();
  const requirements = useAppSelector(selectRequirements);
  const loading = useAppSelector(selectRecommendationsLoading);

  const handleChange = (field: string, value: any) => {
    dispatch(updateRequirements({ [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      // 1. 获取推荐
      const result = await dispatch(
        fetchRecommendations(requirements as ProjectRequirements)
      ).unwrap();
      
      // 2. 保存到历史
      await dispatch(addHistoryItem({
        requirements: requirements as ProjectRequirements,
        result
      }));
      
      // 3. 显示成功通知
      dispatch(addNotification({
        type: 'success',
        message: '分析完成！'
      }));
      
    } catch (error) {
      // 4. 错误处理
      dispatch(addNotification({
        type: 'error',
        message: `分析失败: ${error}`
      }));
    }
  };

  const handleReset = () => {
    dispatch(resetRequirements());
    dispatch(addNotification({
      type: 'info',
      message: '已重置表单'
    }));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={requirements.projectType || ''}
        onChange={(e) => handleChange('projectType', e.target.value)}
      />
      
      <button type="submit" disabled={loading}>
        {loading ? '分析中...' : '提交'}
      </button>
      
      <button type="button" onClick={handleReset}>
        重置
      </button>
    </form>
  );
}
```

## 🔍 调试技巧

### 1. 使用 Redux DevTools
- 安装浏览器扩展
- 查看每个 action
- 时间旅行调试
- 导出/导入状态

### 2. 控制台日志
```typescript
// 监听状态变化
store.subscribe(() => {
  console.log('State:', store.getState());
});
```

### 3. React DevTools
- 查看组件树
- 检查 Props
- 分析性能

## ⚠️ 常见陷阱

### 1. ❌ 直接修改状态
```typescript
// ❌ 错误
state.data.projectType = 'web';

// ✅ 正确 (RTK 内置 Immer)
state.data = { ...state.data, projectType: 'web' };
```

### 2. ❌ 忘记 unwrap()
```typescript
// ❌ 错误 - 无法捕获 rejected
const result = await dispatch(fetchData(params));

// ✅ 正确
try {
  const result = await dispatch(fetchData(params)).unwrap();
} catch (error) {
  // 处理错误
}
```

### 3. ❌ 过度使用全局状态
```typescript
// ❌ 不需要存储在 Redux 中
const [localState, setLocalState] = useState();

// ✅ 只存储需要共享的状态
```

## 📚 下一步

- 阅读完整文档: `REDUX_GUIDE.md`
- 查看示例组件: `src/components/examples/ReduxExampleComponent.tsx`
- 学习 TypeScript 类型: `src/types/index.ts`
- 研究 Selectors: `src/store/selectors.ts`

---

**🎉 现在你已经掌握了 Redux Toolkit 的基础使用！**
