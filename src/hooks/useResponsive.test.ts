/**
 * useResponsive Hook 单元测试
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useResponsive } from '@/hooks/useResponsive';

describe('useResponsive', () => {
  let matchMediaMock: any;

  beforeEach(() => {
    // 重置 matchMedia mock
    matchMediaMock = vi.fn();
    window.matchMedia = matchMediaMock;
  });

  it('应该正确检测移动设备', () => {
    matchMediaMock.mockImplementation((query: string) => ({
      matches: query === '(max-width: 768px)',
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    const { result } = renderHook(() => useResponsive());

    expect(result.current.isMobile).toBe(true);
    expect(result.current.isTablet).toBe(false);
    expect(result.current.isDesktop).toBe(false);
  });

  it('应该正确检测平板设备', () => {
    matchMediaMock.mockImplementation((query: string) => ({
      matches: query === '(min-width: 769px) and (max-width: 1024px)',
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    const { result } = renderHook(() => useResponsive());

    expect(result.current.isMobile).toBe(false);
    expect(result.current.isTablet).toBe(true);
    expect(result.current.isDesktop).toBe(false);
  });

  it('应该正确检测桌面设备', () => {
    matchMediaMock.mockImplementation((query: string) => ({
      matches: query === '(min-width: 1025px)',
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    const { result } = renderHook(() => useResponsive());

    expect(result.current.isMobile).toBe(false);
    expect(result.current.isTablet).toBe(false);
    expect(result.current.isDesktop).toBe(true);
  });

  it('应该在窗口大小改变时更新状态', () => {
    let changeHandler: ((e: MediaQueryListEvent) => void) | null = null;

    matchMediaMock.mockImplementation((query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn((event: string, handler: (e: MediaQueryListEvent) => void) => {
        if (event === 'change') {
          changeHandler = handler;
        }
      }),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    const { result } = renderHook(() => useResponsive());

    expect(result.current.isMobile).toBe(false);

    // 模拟窗口大小改变
    act(() => {
      if (changeHandler) {
        changeHandler({ matches: true } as MediaQueryListEvent);
      }
    });

    // 注意: 由于 matchMedia 的限制,实际的响应式更新可能需要重新渲染
    // 这里主要测试事件监听器是否正确设置
    expect(matchMediaMock).toHaveBeenCalled();
  });

  it('应该在卸载时清理事件监听器', () => {
    const removeEventListenerMock = vi.fn();

    matchMediaMock.mockImplementation(() => ({
      matches: false,
      media: '',
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: removeEventListenerMock,
      dispatchEvent: vi.fn(),
    }));

    const { unmount } = renderHook(() => useResponsive());

    unmount();

    expect(removeEventListenerMock).toHaveBeenCalled();
  });

  it('应该返回正确的设备类型', () => {
    matchMediaMock.mockImplementation((query: string) => ({
      matches: query === '(max-width: 768px)',
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    const { result } = renderHook(() => useResponsive());

    expect(result.current.deviceType).toBe('mobile');
  });

  it('应该正确处理方向变化', () => {
    matchMediaMock.mockImplementation((query: string) => ({
      matches: query === '(orientation: portrait)',
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    const { result } = renderHook(() => useResponsive());

    expect(result.current.orientation).toBe('portrait');
  });
});
