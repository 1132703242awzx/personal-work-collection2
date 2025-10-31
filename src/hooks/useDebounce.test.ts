/**
 * useDebounce Hook 单元测试
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from '@/hooks/useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('应该返回初始值', () => {
    const { result } = renderHook(() => useDebounce('initial', 500));
    
    expect(result.current).toBe('initial');
  });

  it('应该在延迟后更新值', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 500 },
      }
    );

    expect(result.current).toBe('initial');

    // 更新值
    rerender({ value: 'updated', delay: 500 });

    // 值应该还是旧值
    expect(result.current).toBe('initial');

    // 快进时间
    act(() => {
      vi.advanceTimersByTime(500);
    });

    // 值应该更新了
    expect(result.current).toBe('updated');
  });

  it('应该在延迟时间内多次更新时只保留最后一个值', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 500 },
      }
    );

    // 快速多次更新
    rerender({ value: 'update1', delay: 500 });
    rerender({ value: 'update2', delay: 500 });
    rerender({ value: 'update3', delay: 500 });

    // 快进时间
    act(() => {
      vi.advanceTimersByTime(500);
    });

    // 应该只有最后一个值
    expect(result.current).toBe('update3');
  });

  it('应该支持不同的延迟时间', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 1000 },
      }
    );

    rerender({ value: 'updated', delay: 1000 });

    // 500ms 后值应该还是旧值
    act(() => {
      vi.advanceTimersByTime(500);
    });
    expect(result.current).toBe('initial');

    // 再过 500ms (总共 1000ms) 后值应该更新
    act(() => {
      vi.advanceTimersByTime(500);
    });
    expect(result.current).toBe('updated');
  });

  it('应该在组件卸载时清理定时器', () => {
    const { unmount } = renderHook(() => useDebounce('test', 500));
    
    const clearTimeoutSpy = vi.spyOn(global, 'clearTimeout');
    
    unmount();

    expect(clearTimeoutSpy).toHaveBeenCalled();
  });

  it('应该处理复杂对象', () => {
    const initialObj = { id: 1, name: 'Initial' };
    const updatedObj = { id: 2, name: 'Updated' };

    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: initialObj, delay: 500 },
      }
    );

    expect(result.current).toBe(initialObj);

    rerender({ value: updatedObj, delay: 500 });

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(result.current).toBe(updatedObj);
  });

  it('应该处理 0 延迟', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 0 },
      }
    );

    rerender({ value: 'updated', delay: 0 });

    act(() => {
      vi.advanceTimersByTime(0);
    });

    expect(result.current).toBe('updated');
  });

  it('应该处理 undefined 值', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: undefined, delay: 500 },
      }
    );

    expect(result.current).toBeUndefined();

    rerender({ value: 'defined', delay: 500 });

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(result.current).toBe('defined');
  });
});
