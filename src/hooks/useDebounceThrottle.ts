/**
 * 防抖和节流 Hooks
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { debounceThrottleConfig } from '@/config/performance';

/**
 * useDebounce Hook
 * 防抖函数,延迟执行
 * 
 * @param callback - 要防抖的函数
 * @param delay - 延迟时间 (毫秒)
 * @returns 防抖后的函数
 * 
 * @example
 * const handleSearch = useDebounce((value: string) => {
 *   // 执行搜索
 * }, 300);
 */
export function useDebounce<T extends (...args: any[]) => any>(
  callback: T,
  delay: number = debounceThrottleConfig.searchDebounce
): (...args: Parameters<T>) => void {
  const timeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return useCallback(
    (...args: Parameters<T>) => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      timeoutRef.current = setTimeout(() => {
        callback(...args);
      }, delay);
    },
    [callback, delay]
  );
}

/**
 * useThrottle Hook
 * 节流函数,限制执行频率
 * 
 * @param callback - 要节流的函数
 * @param delay - 节流时间间隔 (毫秒)
 * @returns 节流后的函数
 * 
 * @example
 * const handleScroll = useThrottle(() => {
 *   // 处理滚动
 * }, 100);
 */
export function useThrottle<T extends (...args: any[]) => any>(
  callback: T,
  delay: number = debounceThrottleConfig.scrollThrottle
): (...args: Parameters<T>) => void {
  const lastRunRef = useRef<number>(0);
  const timeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return useCallback(
    (...args: Parameters<T>) => {
      const now = Date.now();
      const timeSinceLastRun = now - lastRunRef.current;

      if (timeSinceLastRun >= delay) {
        callback(...args);
        lastRunRef.current = now;
      } else {
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
        }

        timeoutRef.current = setTimeout(() => {
          callback(...args);
          lastRunRef.current = Date.now();
        }, delay - timeSinceLastRun);
      }
    },
    [callback, delay]
  );
}

/**
 * useDebouncedValue Hook
 * 防抖值,延迟更新
 * 
 * @param value - 原始值
 * @param delay - 延迟时间 (毫秒)
 * @returns 防抖后的值
 * 
 * @example
 * const [searchTerm, setSearchTerm] = useState('');
 * const debouncedSearchTerm = useDebouncedValue(searchTerm, 300);
 * 
 * useEffect(() => {
 *   // 使用 debouncedSearchTerm 执行搜索
 * }, [debouncedSearchTerm]);
 */
export function useDebouncedValue<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timeout);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * useThrottledValue Hook
 * 节流值,限制更新频率
 * 
 * @param value - 原始值
 * @param delay - 节流时间间隔 (毫秒)
 * @returns 节流后的值
 */
export function useThrottledValue<T>(value: T, delay: number = 100): T {
  const [throttledValue, setThrottledValue] = useState<T>(value);
  const lastUpdatedRef = useRef<number>(0);
  const timeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);

  useEffect(() => {
    const now = Date.now();
    const timeSinceLastUpdate = now - lastUpdatedRef.current;

    if (timeSinceLastUpdate >= delay) {
      setThrottledValue(value);
      lastUpdatedRef.current = now;
    } else {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      timeoutRef.current = setTimeout(() => {
        setThrottledValue(value);
        lastUpdatedRef.current = Date.now();
      }, delay - timeSinceLastUpdate);
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, delay]);

  return throttledValue;
}
