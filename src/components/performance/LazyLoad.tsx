/**
 * 懒加载组件包装器
 * 提供加载状态、错误处理和重试功能
 */

import React, { Suspense, ComponentType, lazy, ReactNode } from 'react';
import { lazyLoadConfig, lazyLoadWithRetry } from '@/config/performance';

export interface LazyLoadProps {
  /** 加载中显示的组件 */
  fallback?: ReactNode;
  /** 错误时显示的组件 */
  errorFallback?: (error: Error, retry: () => void) => ReactNode;
  /** 是否启用预加载 */
  preload?: boolean;
  /** 子组件 */
  children: ReactNode;
}

/**
 * LazyLoad 组件
 * Suspense 包装器,提供加载和错误状态
 * 
 * @example
 * <LazyLoad fallback={<Skeleton />}>
 *   <LazyComponent />
 * </LazyLoad>
 */
export function LazyLoad({
  fallback = <DefaultFallback />,
  errorFallback = DefaultErrorFallback,
  children,
}: LazyLoadProps) {
  return (
    <ErrorBoundary fallback={errorFallback}>
      <Suspense fallback={fallback}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}

/**
 * 默认加载中组件
 */
function DefaultFallback() {
  return (
    <div className="flex justify-center items-center min-h-[200px]">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p className="text-gray-600">加载中...</p>
      </div>
    </div>
  );
}

/**
 * 默认错误组件
 */
function DefaultErrorFallback(error: Error, retry: () => void) {
  return (
    <div className="flex justify-center items-center min-h-[200px]">
      <div className="text-center max-w-md p-6">
        <div className="text-red-500 text-5xl mb-4">⚠️</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          加载失败
        </h3>
        <p className="text-gray-600 mb-4">
          {error.message || '组件加载时出现错误'}
        </p>
        <button
          onClick={retry}
          className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
        >
          重试
        </button>
      </div>
    </div>
  );
}

/**
 * ErrorBoundary 类组件
 */
interface ErrorBoundaryProps {
  children: ReactNode;
  fallback: (error: Error, retry: () => void) => ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('LazyLoad Error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      return this.props.fallback(this.state.error, this.handleRetry);
    }

    return this.props.children;
  }
}

/**
 * 创建懒加载组件 (带重试)
 * 
 * @param importFn - 动态导入函数
 * @param retries - 重试次数
 * @returns 懒加载组件
 * 
 * @example
 * const LazyDashboard = lazyWithRetry(() => import('./pages/Dashboard'));
 */
export function lazyWithRetry<T extends ComponentType<any>>(
  importFn: () => Promise<{ default: T }>,
  retries = lazyLoadConfig.retryCount
): React.LazyExoticComponent<T> {
  return lazy(() => lazyLoadWithRetry(importFn, retries));
}

/**
 * 预加载组件
 * 
 * @param Component - 懒加载组件
 * @example
 * const LazyPage = lazy(() => import('./Page'));
 * preloadComponent(LazyPage);
 */
export function preloadComponent<T extends ComponentType<any>>(
  Component: React.LazyExoticComponent<T>
): void {
  // @ts-ignore - 访问 lazy 组件的 _payload
  if (Component && Component._payload && Component._payload._result === undefined) {
    // @ts-ignore
    Component._payload._result = Component._payload._init(Component._payload);
  }
}

/**
 * Skeleton 加载占位符组件
 */
export interface SkeletonProps {
  /** 高度 */
  height?: string | number;
  /** 宽度 */
  width?: string | number;
  /** 是否为圆形 */
  circle?: boolean;
  /** 数量 (显示多少个骨架屏) */
  count?: number;
  /** 类名 */
  className?: string;
}

export function Skeleton({
  height = '20px',
  width = '100%',
  circle = false,
  count = 1,
  className = '',
}: SkeletonProps) {
  const skeletons = Array.from({ length: count }, (_, i) => (
    <div
      key={i}
      className={`animate-pulse bg-gray-200 ${circle ? 'rounded-full' : 'rounded'} ${className}`}
      style={{
        height: typeof height === 'number' ? `${height}px` : height,
        width: typeof width === 'number' ? `${width}px` : width,
      }}
    />
  ));

  return count > 1 ? (
    <div className="space-y-3">
      {skeletons}
    </div>
  ) : (
    <>{skeletons}</>
  );
}

/**
 * 卡片骨架屏
 */
export function CardSkeleton({ count = 1 }: { count?: number }) {
  const cards = Array.from({ length: count }, (_, i) => (
    <div key={i} className="border border-gray-200 rounded-lg p-6">
      <Skeleton height="120px" width="100%" className="mb-4" />
      <Skeleton height="20px" width="60%" className="mb-2" />
      <Skeleton height="16px" width="100%" count={2} />
    </div>
  ));

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {cards}
    </div>
  );
}

/**
 * 列表骨架屏
 */
export function ListSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className="flex items-center space-x-4">
          <Skeleton circle width={48} height={48} />
          <div className="flex-1">
            <Skeleton height="18px" width="40%" className="mb-2" />
            <Skeleton height="14px" width="80%" />
          </div>
        </div>
      ))}
    </div>
  );
}

/**
 * 表格骨架屏
 */
export function TableSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            {Array.from({ length: columns }, (_, i) => (
              <th key={i} className="px-6 py-3">
                <Skeleton height="16px" width="80px" />
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {Array.from({ length: rows }, (_, i) => (
            <tr key={i}>
              {Array.from({ length: columns }, (_, j) => (
                <td key={j} className="px-6 py-4">
                  <Skeleton height="14px" width="100px" />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default LazyLoad;
