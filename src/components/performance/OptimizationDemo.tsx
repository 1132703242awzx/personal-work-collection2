/**
 * 优化示例组件
 * 展示如何使用 React.memo, useCallback, useMemo 优化性能
 */

import { memo, useCallback, useMemo, useState } from 'react';
import { useRenderCount, useWhyDidYouUpdate } from '@/hooks/usePerformance';

/**
 * 未优化的组件示例
 */
export function UnoptimizedCard({ title, description, onClick }: {
  title: string;
  description: string;
  onClick: () => void;
}) {
  const renderCount = useRenderCount();
  
  return (
    <div className="border p-4 rounded-lg">
      <div className="text-xs text-gray-400 mb-2">渲染次数: {renderCount}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 mb-4">{description}</p>
      <button
        onClick={onClick}
        className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
      >
        点击
      </button>
    </div>
  );
}

/**
 * 优化后的组件示例 - 使用 React.memo
 */
export const OptimizedCard = memo(function OptimizedCard({ 
  title, 
  description, 
  onClick 
}: {
  title: string;
  description: string;
  onClick: () => void;
}) {
  const renderCount = useRenderCount();
  useWhyDidYouUpdate('OptimizedCard', { title, description, onClick });
  
  return (
    <div className="border p-4 rounded-lg">
      <div className="text-xs text-green-600 mb-2">渲染次数: {renderCount}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 mb-4">{description}</p>
      <button
        onClick={onClick}
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        点击
      </button>
    </div>
  );
});

/**
 * 优化对比演示
 */
export function OptimizationDemo() {
  const [count, setCount] = useState(0);
  const [items] = useState([
    { id: 1, title: '项目 1', description: '描述 1' },
    { id: 2, title: '项目 2', description: '描述 2' },
    { id: 3, title: '项目 3', description: '描述 3' },
  ]);

  // ❌ 未优化 - 每次渲染都创建新函数
  const unoptimizedHandler = () => {
    console.log('Unoptimized click');
  };

  // ✅ 优化 - 使用 useCallback 缓存函数
  const optimizedHandler = useCallback(() => {
    console.log('Optimized click');
  }, []);

  // ✅ 使用 useMemo 缓存计算结果
  const expensiveCalculation = useMemo(() => {
    console.log('执行昂贵的计算...');
    return items.reduce((sum, item) => sum + item.id, 0);
  }, [items]);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">性能优化对比</h1>

      {/* 计数器 */}
      <div className="mb-8 p-4 bg-blue-50 rounded-lg">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setCount(c => c + 1)}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            增加计数 ({count})
          </button>
          <span className="text-gray-600">
            点击此按钮会触发父组件重渲染
          </span>
        </div>
        <div className="mt-2 text-sm text-gray-600">
          计算结果 (useMemo): {expensiveCalculation}
        </div>
      </div>

      {/* 对比展示 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 未优化版本 */}
        <div>
          <h2 className="text-xl font-semibold mb-4 text-red-600">
            ❌ 未优化 (会重渲染)
          </h2>
          <div className="space-y-4">
            {items.map(item => (
              <UnoptimizedCard
                key={item.id}
                title={item.title}
                description={item.description}
                onClick={unoptimizedHandler}
              />
            ))}
          </div>
        </div>

        {/* 优化版本 */}
        <div>
          <h2 className="text-xl font-semibold mb-4 text-green-600">
            ✅ 已优化 (不会重渲染)
          </h2>
          <div className="space-y-4">
            {items.map(item => (
              <OptimizedCard
                key={item.id}
                title={item.title}
                description={item.description}
                onClick={optimizedHandler}
              />
            ))}
          </div>
        </div>
      </div>

      {/* 说明 */}
      <div className="mt-8 p-6 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-3">优化技巧:</h3>
        <ul className="space-y-2 text-gray-700">
          <li className="flex items-start">
            <span className="text-green-600 mr-2">✓</span>
            <span>
              <strong>React.memo:</strong> 避免不必要的重渲染,只在 props 变化时重新渲染
            </span>
          </li>
          <li className="flex items-start">
            <span className="text-green-600 mr-2">✓</span>
            <span>
              <strong>useCallback:</strong> 缓存函数引用,避免子组件因函数引用变化而重渲染
            </span>
          </li>
          <li className="flex items-start">
            <span className="text-green-600 mr-2">✓</span>
            <span>
              <strong>useMemo:</strong> 缓存计算结果,避免重复执行昂贵的计算
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}

/**
 * 列表项优化示例
 */
export const ListItem = memo(({ 
  id, 
  title, 
  content, 
  onDelete 
}: {
  id: number;
  title: string;
  content: string;
  onDelete: (id: number) => void;
}) => {
  const renderCount = useRenderCount();

  // ✅ 使用 useCallback 包装删除函数
  const handleDelete = useCallback(() => {
    onDelete(id);
  }, [id, onDelete]);

  return (
    <div className="flex items-center justify-between p-4 border rounded-lg">
      <div className="flex-1">
        <h4 className="font-semibold">{title}</h4>
        <p className="text-sm text-gray-600">{content}</p>
        <span className="text-xs text-gray-400">渲染: {renderCount}次</span>
      </div>
      <button
        onClick={handleDelete}
        className="px-3 py-1 text-sm text-red-600 border border-red-600 rounded hover:bg-red-50"
      >
        删除
      </button>
    </div>
  );
});

ListItem.displayName = 'ListItem';

/**
 * 大列表优化示例
 */
export function LargeListDemo() {
  const [items, setItems] = useState(() =>
    Array.from({ length: 100 }, (_, i) => ({
      id: i + 1,
      title: `项目 ${i + 1}`,
      content: `这是第 ${i + 1} 个项目的内容`,
    }))
  );

  // ✅ 使用 useCallback 缓存删除函数
  const handleDelete = useCallback((id: number) => {
    setItems(prev => prev.filter(item => item.id !== id));
  }, []);

  // ✅ 使用 useMemo 计算派生状态
  const itemCount = useMemo(() => items.length, [items.length]);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold">大列表优化演示</h2>
        <p className="text-gray-600">当前项数: {itemCount}</p>
      </div>

      <div className="space-y-3">
        {items.map(item => (
          <ListItem
            key={item.id}
            id={item.id}
            title={item.title}
            content={item.content}
            onDelete={handleDelete}
          />
        ))}
      </div>
    </div>
  );
}

export default OptimizationDemo;
