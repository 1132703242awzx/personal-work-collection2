# 🚀 React 应用性能优化文档

## 📋 目录

1. [性能优化概述](#性能优化概述)
2. [代码分割](#代码分割)
3. [渲染优化](#渲染优化)
4. [资源优化](#资源优化)
5. [性能监控](#性能监控)
6. [最佳实践](#最佳实践)

---

## 性能优化概述

本项目实施了全面的性能优化策略,包括:

- ✅ **代码分割** - 路由懒加载、组件动态导入
- ✅ **渲染优化** - React.memo、useCallback、useMemo、虚拟列表
- ✅ **资源优化** - 图片懒加载、字体优化、代码压缩
- ✅ **性能监控** - Web Vitals、渲染监控、内存监控

---

## 代码分割

### 1. 路由级懒加载

使用 `lazy` 和 `Suspense` 实现路由级代码分割:

```tsx
import { lazy } from 'react';
import { LazyLoad } from '@/components/performance';

// 懒加载页面组件
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Routes>
      <Route path="/dashboard" element={
        <LazyLoad fallback={<PageSkeleton />}>
          <Dashboard />
        </LazyLoad>
      } />
      <Route path="/profile" element={
        <LazyLoad>
          <Profile />
        </LazyLoad>
      } />
    </Routes>
  );
}
```

### 2. 组件动态导入

使用 `lazyWithRetry` 实现带重试功能的懒加载:

```tsx
import { lazyWithRetry } from '@/components/performance';

// 懒加载组件 (自动重试 3 次)
const HeavyChart = lazyWithRetry(
  () => import('./components/HeavyChart')
);

// 使用
<LazyLoad fallback={<Skeleton height={400} />}>
  <HeavyChart data={chartData} />
</LazyLoad>
```

### 3. 预加载关键组件

```tsx
import { preloadComponent } from '@/components/performance';

const LazyModal = lazy(() => import('./Modal'));

// 鼠标悬停时预加载
<button
  onClick={() => setShowModal(true)}
  onMouseEnter={() => preloadComponent(LazyModal)}
>
  打开弹窗
</button>
```

---

## 渲染优化

### 1. React.memo 避免不必要渲染

```tsx
import { memo } from 'react';

// ❌ 未优化 - 父组件更新时总是重渲染
function UserCard({ user }) {
  return <div>{user.name}</div>;
}

// ✅ 优化 - 只在 user 变化时重渲染
const UserCard = memo(function UserCard({ user }) {
  return <div>{user.name}</div>;
});

// ✅ 自定义比较函数
const UserCard = memo(
  function UserCard({ user }) {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => {
    // 返回 true 表示不重渲染
    return prevProps.user.id === nextProps.user.id;
  }
);
```

### 2. useCallback 优化函数

```tsx
import { useCallback, useState } from 'react';

function ParentComponent() {
  const [count, setCount] = useState(0);

  // ❌ 未优化 - 每次渲染都创建新函数
  const handleClick = () => {
    console.log('Clicked');
  };

  // ✅ 优化 - 函数引用保持不变
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []); // 依赖数组为空,函数永不变

  // ✅ 带依赖的 useCallback
  const handleUpdate = useCallback((id) => {
    console.log('Update', id, count);
  }, [count]); // count 变化时才创建新函数

  return <ChildComponent onClick={handleClick} />;
}
```

### 3. useMemo 优化计算

```tsx
import { useMemo, useState } from 'react';

function DataTable({ data }) {
  const [filter, setFilter] = useState('');

  // ❌ 未优化 - 每次渲染都重新过滤
  const filteredData = data.filter(item => 
    item.name.includes(filter)
  );

  // ✅ 优化 - 只在 data 或 filter 变化时重新计算
  const filteredData = useMemo(() => {
    console.log('过滤数据...');
    return data.filter(item => item.name.includes(filter));
  }, [data, filter]);

  // ✅ 复杂计算优化
  const statistics = useMemo(() => {
    console.log('计算统计数据...');
    return {
      total: data.length,
      average: data.reduce((sum, item) => sum + item.value, 0) / data.length,
      max: Math.max(...data.map(item => item.value)),
    };
  }, [data]);

  return (
    <div>
      <div>总数: {statistics.total}</div>
      <div>平均: {statistics.average}</div>
      {filteredData.map(item => <div key={item.id}>{item.name}</div>)}
    </div>
  );
}
```

### 4. 虚拟列表优化长列表

```tsx
import { VirtualList } from '@/components/performance';

function LongList({ items }) {
  return (
    <VirtualList
      items={items}
      itemHeight={80}
      height={600}
      renderItem={(item) => (
        <div className="p-4 border-b">
          <h3>{item.title}</h3>
          <p>{item.description}</p>
        </div>
      )}
      getKey={(item) => item.id}
      onLoadMore={loadMore}
    />
  );
}

// 动态高度虚拟列表
import { DynamicVirtualList } from '@/components/performance';

<DynamicVirtualList
  items={items}
  estimatedItemHeight={100}
  height={600}
  renderItem={(item) => <ComplexCard {...item} />}
/>
```

---

## 资源优化

### 1. 图片懒加载

响应式图片组件已内置懒加载:

```tsx
import { ResponsiveImage } from '@/components/responsive';

<ResponsiveImage
  src="large-image.jpg"
  srcSet="small.jpg 480w, large.jpg 800w"
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="描述"
  lazy  // 启用懒加载
  aspectRatio="16/9"
/>
```

### 2. 防抖和节流

```tsx
import { useDebounce, useThrottle, useDebouncedValue } from '@/hooks';

function SearchInput() {
  const [query, setQuery] = useState('');

  // ✅ 防抖搜索 - 延迟 300ms 执行
  const handleSearch = useDebounce((value: string) => {
    console.log('搜索:', value);
    // 执行搜索 API 调用
  }, 300);

  return (
    <input
      value={query}
      onChange={(e) => {
        setQuery(e.target.value);
        handleSearch(e.target.value);
      }}
    />
  );
}

function ScrollTracker() {
  // ✅ 节流滚动事件 - 最多 100ms 执行一次
  const handleScroll = useThrottle(() => {
    console.log('Scroll position:', window.scrollY);
  }, 100);

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);
}

// ✅ 防抖值
function LiveSearch() {
  const [input, setInput] = useState('');
  const debouncedInput = useDebouncedValue(input, 300);

  useEffect(() => {
    // debouncedInput 变化时执行搜索
    if (debouncedInput) {
      performSearch(debouncedInput);
    }
  }, [debouncedInput]);

  return <input value={input} onChange={(e) => setInput(e.target.value)} />;
}
```

### 3. 骨架屏加载状态

```tsx
import { Skeleton, CardSkeleton, ListSkeleton, TableSkeleton } from '@/components/performance';

// 基础骨架屏
<Skeleton height={20} width="80%" />
<Skeleton height={100} width="100%" count={3} />
<Skeleton circle width={48} height={48} />

// 卡片骨架屏
<CardSkeleton count={6} />

// 列表骨架屏
<ListSkeleton count={10} />

// 表格骨架屏
<TableSkeleton rows={5} columns={4} />
```

---

## 性能监控

### 1. 组件渲染监控

```tsx
import { useRenderCount, useWhyDidYouUpdate, usePerformance } from '@/hooks';

function MyComponent(props) {
  // 统计渲染次数
  const renderCount = useRenderCount();
  console.log(`渲染了 ${renderCount} 次`);

  // 调试 props 变化
  useWhyDidYouUpdate('MyComponent', props);

  // 测量组件性能
  const { mountTime, renderCount: count } = usePerformance('MyComponent');

  return <div>组件内容</div>;
}
```

### 2. Web Vitals 监控

```tsx
import { useWebVitals } from '@/hooks';

function App() {
  const vitals = useWebVitals();

  useEffect(() => {
    console.log('Web Vitals:', vitals);
    // {
    //   lcp: 1500,  // Largest Contentful Paint
    //   fid: 50,    // First Input Delay
    //   cls: 0.05,  // Cumulative Layout Shift
    //   fcp: 1000,  // First Contentful Paint
    //   ttfb: 200   // Time to First Byte
    // }
  }, [vitals]);

  return <div>App</div>;
}
```

### 3. 内存监控

```tsx
import { useMemoryMonitor } from '@/hooks';

function MemoryMonitor() {
  const memory = useMemoryMonitor();

  return (
    <div>
      <p>已使用: {(memory.usedJSHeapSize / 1024 / 1024).toFixed(2)} MB</p>
      <p>总计: {(memory.totalJSHeapSize / 1024 / 1024).toFixed(2)} MB</p>
      <p>限制: {(memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2)} MB</p>
      <p>使用率: {memory.usedPercentage?.toFixed(2)}%</p>
    </div>
  );
}
```

### 4. 长任务监控

```tsx
import { useLongTask } from '@/hooks';

function PerformanceMonitor() {
  const longTasks = useLongTask();

  return (
    <div>
      <h3>检测到 {longTasks.length} 个长任务</h3>
      {longTasks.map((task, i) => (
        <div key={i}>
          任务 {i + 1}: {task.duration.toFixed(2)}ms
        </div>
      ))}
    </div>
  );
}
```

---

## 最佳实践

### 1. 代码分割原则

```tsx
// ✅ 好 - 按路由分割
const Dashboard = lazy(() => import('./pages/Dashboard'));

// ✅ 好 - 按功能分割
const Chart = lazy(() => import('./components/Chart'));

// ❌ 差 - 过度分割
const Button = lazy(() => import('./components/Button'));
```

### 2. memo 使用原则

```tsx
// ✅ 好 - 纯展示组件
const UserAvatar = memo(({ user }) => <img src={user.avatar} />);

// ✅ 好 - 渲染成本高的组件
const ComplexChart = memo(({ data }) => <ExpensiveChart data={data} />);

// ❌ 差 - 简单组件不需要 memo
const Text = memo(({ children }) => <span>{children}</span>);
```

### 3. useCallback/useMemo 使用原则

```tsx
// ✅ 好 - 传给 memo 组件的函数
const handleClick = useCallback(() => {
  doSomething();
}, []);

<MemoizedChild onClick={handleClick} />

// ✅ 好 - 昂贵的计算
const result = useMemo(() => {
  return expensiveCalculation(data);
}, [data]);

// ❌ 差 - 简单计算不需要 useMemo
const sum = useMemo(() => a + b, [a, b]); // 过度优化
```

### 4. 列表渲染优化

```tsx
// ✅ 好 - 使用稳定的 key
{items.map(item => (
  <Item key={item.id} {...item} />
))}

// ❌ 差 - 使用索引作为 key
{items.map((item, index) => (
  <Item key={index} {...item} />
))}

// ✅ 好 - 长列表使用虚拟滚动
<VirtualList items={longList} ... />

// ❌ 差 - 直接渲染 10000 项
{longList.map(item => <Item key={item.id} {...item} />)}
```

### 5. 状态管理优化

```tsx
// ✅ 好 - 状态尽量靠近使用的地方
function UserProfile() {
  const [expanded, setExpanded] = useState(false);
  return <div>{/* 使用 expanded */}</div>;
}

// ❌ 差 - 不必要的全局状态
// 在 Redux 中存储 UI 状态 (如 expanded)

// ✅ 好 - 拆分状态避免不必要的渲染
const [name, setName] = useState('');
const [email, setEmail] = useState('');

// ❌ 差 - 对象状态可能导致更多渲染
const [form, setForm] = useState({ name: '', email: '' });
```

---

## 性能检查清单

### 开发阶段
- [ ] 使用 React DevTools Profiler 分析渲染
- [ ] 检查不必要的重渲染
- [ ] 使用 `useWhyDidYouUpdate` 调试
- [ ] 测量组件挂载时间

### 构建阶段
- [ ] 启用代码压缩
- [ ] 配置 Tree Shaking
- [ ] 分析 Bundle 大小
- [ ] 检查重复依赖

### 部署前
- [ ] 运行 Lighthouse 审计
- [ ] 检查 Web Vitals 指标
- [ ] 测试慢速网络下的加载
- [ ] 验证图片优化

### 生产环境
- [ ] 监控 LCP (< 2.5s)
- [ ] 监控 FID (< 100ms)
- [ ] 监控 CLS (< 0.1)
- [ ] 监控内存泄漏

---

## 性能配置

所有性能配置在 `src/config/performance.ts`:

```typescript
import { getPerformanceConfig } from '@/config/performance';

const config = getPerformanceConfig();

// 懒加载配置
config.lazyLoad.timeout       // 10000ms
config.lazyLoad.retryCount    // 3次

// 虚拟列表配置
config.virtualList.itemHeight    // 80px
config.virtualList.overscan      // 3项

// 防抖节流配置
config.debounceThrottle.searchDebounce  // 300ms
config.debounceThrottle.scrollThrottle  // 100ms

// 性能监控配置
config.performanceMonitor.enabled  // true
config.performanceMonitor.thresholds.lcp  // 2500ms
```

---

## 性能工具

### Vite 配置优化

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    // 代码分割
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['framer-motion'],
        },
      },
    },
    // 压缩
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
      },
    },
  },
});
```

---

## 总结

本项目实现了全面的性能优化:

- ✅ **18+ 性能优化组件**
- ✅ **8+ 性能监控 Hooks**
- ✅ **完整的性能配置系统**
- ✅ **代码分割和懒加载**
- ✅ **渲染优化 (memo, callback, memoization)**
- ✅ **虚拟列表优化长列表**
- ✅ **防抖节流优化事件**
- ✅ **Web Vitals 监控**
- ✅ **内存和长任务监控**

可以立即应用到项目中提升性能! 🚀
