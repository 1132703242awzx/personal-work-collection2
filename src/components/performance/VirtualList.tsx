/**
 * 虚拟列表组件
 * 用于优化长列表渲染性能
 */

import React, { useState, useRef, useCallback } from 'react';
import { virtualListConfig } from '@/config/performance';
import { useThrottle } from '@/hooks/useDebounceThrottle';

export interface VirtualListProps<T> {
  /** 列表数据 */
  items: T[];
  /** 项渲染函数 */
  renderItem: (item: T, index: number) => React.ReactNode;
  /** 项高度 (px) */
  itemHeight?: number;
  /** 容器高度 (px) */
  height: number;
  /** 缓冲区项数 (上下各多渲染几项) */
  overscan?: number;
  /** 唯一键提取函数 */
  getKey?: (item: T, index: number) => string | number;
  /** 容器类名 */
  className?: string;
  /** 加载更多回调 */
  onLoadMore?: () => void;
  /** 是否正在加载 */
  loading?: boolean;
  /** 加载更多阈值 (距离底部多少像素触发) */
  loadMoreThreshold?: number;
}

/**
 * VirtualList 组件
 * 使用虚拟滚动优化长列表性能
 * 
 * @example
 * <VirtualList
 *   items={data}
 *   itemHeight={80}
 *   height={600}
 *   renderItem={(item) => <ItemCard {...item} />}
 *   getKey={(item) => item.id}
 *   onLoadMore={loadMore}
 * />
 */
export default function VirtualList<T>({
  items,
  renderItem,
  itemHeight = virtualListConfig.defaultItemHeight,
  height,
  overscan = virtualListConfig.overscan,
  getKey = (_, index) => index,
  className = '',
  onLoadMore,
  loading = false,
  loadMoreThreshold = 200,
}: VirtualListProps<T>) {
  const [scrollTop, setScrollTop] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  // 计算可见范围
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
  const endIndex = Math.min(
    items.length - 1,
    Math.ceil((scrollTop + height) / itemHeight) + overscan
  );

  // 可见项
  const visibleItems = items.slice(startIndex, endIndex + 1);

  // 总高度
  const totalHeight = items.length * itemHeight;

  // 偏移量
  const offsetY = startIndex * itemHeight;

  // 节流滚动处理
  const handleScroll = useThrottle((e: React.UIEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    setScrollTop(target.scrollTop);

    // 检查是否需要加载更多
    if (onLoadMore && !loading) {
      const { scrollTop, scrollHeight, clientHeight } = target;
      const distanceToBottom = scrollHeight - scrollTop - clientHeight;

      if (distanceToBottom < loadMoreThreshold) {
        onLoadMore();
      }
    }
  }, virtualListConfig.scrollThrottle);

  return (
    <div
      ref={containerRef}
      className={`overflow-auto ${className}`}
      style={{ height }}
      onScroll={handleScroll}
    >
      {/* 占位容器 */}
      <div style={{ height: totalHeight, position: 'relative' }}>
        {/* 可见项容器 */}
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, i) => {
            const actualIndex = startIndex + i;
            const key = getKey(item, actualIndex);

            return (
              <div
                key={key}
                style={{ height: itemHeight }}
                className="virtual-list-item"
              >
                {renderItem(item, actualIndex)}
              </div>
            );
          })}
        </div>
      </div>

      {/* 加载指示器 */}
      {loading && (
        <div className="flex justify-center items-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span className="ml-3 text-gray-600">加载中...</span>
        </div>
      )}
    </div>
  );
}

/**
 * 动态高度虚拟列表
 * 支持不同高度的列表项
 */
export interface DynamicVirtualListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  estimatedItemHeight?: number;
  height: number;
  overscan?: number;
  getKey?: (item: T, index: number) => string | number;
  className?: string;
  onLoadMore?: () => void;
  loading?: boolean;
}

export function DynamicVirtualList<T>({
  items,
  renderItem,
  estimatedItemHeight = 80,
  height,
  overscan = 3,
  getKey = (_, index) => index,
  className = '',
  onLoadMore,
  loading = false,
}: DynamicVirtualListProps<T>) {
  const [scrollTop, setScrollTop] = useState(0);
  const [itemHeights, setItemHeights] = useState<Map<number, number>>(new Map());
  const containerRef = useRef<HTMLDivElement>(null);
  const itemRefs = useRef<Map<number, HTMLDivElement>>(new Map());

  // 测量项高度
  const measureItem = useCallback((index: number, element: HTMLDivElement | null) => {
    if (!element) {
      itemRefs.current.delete(index);
      return;
    }

    itemRefs.current.set(index, element);
    const height = element.getBoundingClientRect().height;

    setItemHeights(prev => {
      if (prev.get(index) !== height) {
        const newMap = new Map(prev);
        newMap.set(index, height);
        return newMap;
      }
      return prev;
    });
  }, []);

  // 计算项位置
  const getItemOffset = useCallback((index: number) => {
    let offset = 0;
    for (let i = 0; i < index; i++) {
      offset += itemHeights.get(i) || estimatedItemHeight;
    }
    return offset;
  }, [itemHeights, estimatedItemHeight]);

  // 计算总高度
  const totalHeight = items.reduce((sum, _, index) => {
    return sum + (itemHeights.get(index) || estimatedItemHeight);
  }, 0);

  // 查找可见范围
  const findVisibleRange = useCallback(() => {
    let startIndex = 0;
    let endIndex = items.length - 1;
    let currentOffset = 0;

    // 查找起始索引
    for (let i = 0; i < items.length; i++) {
      const itemHeight = itemHeights.get(i) || estimatedItemHeight;
      if (currentOffset + itemHeight > scrollTop) {
        startIndex = Math.max(0, i - overscan);
        break;
      }
      currentOffset += itemHeight;
    }

    // 查找结束索引
    currentOffset = getItemOffset(startIndex);
    for (let i = startIndex; i < items.length; i++) {
      const itemHeight = itemHeights.get(i) || estimatedItemHeight;
      if (currentOffset > scrollTop + height) {
        endIndex = Math.min(items.length - 1, i + overscan);
        break;
      }
      currentOffset += itemHeight;
    }

    return { startIndex, endIndex };
  }, [items.length, itemHeights, estimatedItemHeight, scrollTop, height, overscan, getItemOffset]);

  const { startIndex, endIndex } = findVisibleRange();
  const visibleItems = items.slice(startIndex, endIndex + 1);

  const handleScroll = useThrottle((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);

    if (onLoadMore && !loading) {
      const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
      if (scrollHeight - scrollTop - clientHeight < 200) {
        onLoadMore();
      }
    }
  }, 16);

  return (
    <div
      ref={containerRef}
      className={`overflow-auto ${className}`}
      style={{ height }}
      onScroll={handleScroll}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        {visibleItems.map((item, i) => {
          const actualIndex = startIndex + i;
          const key = getKey(item, actualIndex);
          const offset = getItemOffset(actualIndex);

          return (
            <div
              key={key}
              ref={el => measureItem(actualIndex, el)}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                transform: `translateY(${offset}px)`,
              }}
            >
              {renderItem(item, actualIndex)}
            </div>
          );
        })}
      </div>

      {loading && (
        <div className="flex justify-center items-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      )}
    </div>
  );
}
