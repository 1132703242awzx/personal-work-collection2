/**
 * 测试工具函数
 */

import { render, RenderOptions } from '@testing-library/react';
import { ReactElement } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { configureStore } from '@reduxjs/toolkit';
import type { RootState } from '@/store';
import requirementsReducer from '@/store/slices/requirementsSlice';
import recommendationsReducer from '@/store/slices/recommendationsSlice';
import uiReducer from '@/store/slices/uiSlice';
import historyReducer from '@/store/slices/historySlice';

/**
 * 创建测试用的 Redux Store
 */
export function createTestStore(preloadedState?: Partial<RootState>) {
  return configureStore({
    reducer: {
      requirements: requirementsReducer,
      recommendations: recommendationsReducer,
      ui: uiReducer,
      history: historyReducer,
    },
    preloadedState: preloadedState as any,
  });
}

/**
 * 自定义渲染函数 - 包含 Redux Provider
 */
interface ExtendedRenderOptions extends Omit<RenderOptions, 'queries'> {
  preloadedState?: Partial<RootState>;
  store?: ReturnType<typeof createTestStore>;
}

export function renderWithProviders(
  ui: ReactElement,
  {
    preloadedState = {},
    store = createTestStore(preloadedState),
    ...renderOptions
  }: ExtendedRenderOptions = {}
) {
  function Wrapper({ children }: { children: React.ReactNode }) {
    return <Provider store={store}>{children}</Provider>;
  }

  return {
    store,
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
  };
}

/**
 * 自定义渲染函数 - 包含 Router
 */
export function renderWithRouter(
  ui: ReactElement,
  { route = '/' }: { route?: string } = {}
) {
  window.history.pushState({}, 'Test page', route);

  return render(ui, { wrapper: BrowserRouter });
}

/**
 * 自定义渲染函数 - 包含所有 Providers
 */
export function renderWithAllProviders(
  ui: ReactElement,
  {
    preloadedState = {},
    store = createTestStore(preloadedState),
    route = '/',
    ...renderOptions
  }: ExtendedRenderOptions & { route?: string } = {}
) {
  window.history.pushState({}, 'Test page', route);

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <Provider store={store}>
        <BrowserRouter>{children}</BrowserRouter>
      </Provider>
    );
  }

  return {
    store,
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
  };
}

/**
 * 等待指定时间
 */
export const wait = (ms: number) =>
  new Promise(resolve => setTimeout(resolve, ms));

/**
 * 模拟延迟
 */
export const delay = (ms: number) =>
  new Promise(resolve => setTimeout(resolve, ms));

/**
 * 创建模拟的 Redux Store
 */
export function createMockStore(initialState: Partial<RootState> = {}) {
  return createTestStore(initialState);
}

/**
 * 生成测试 ID
 */
export function generateTestId(prefix: string): string {
  return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * 模拟文件上传
 */
export function createMockFile(
  name: string,
  size: number,
  type: string
): File {
  const file = new File(['a'.repeat(size)], name, { type });
  return file;
}

/**
 * 模拟触摸事件
 */
export function createTouchEvent(type: string, touches: Touch[] = []) {
  return new TouchEvent(type, {
    touches,
    targetTouches: touches,
    changedTouches: touches,
    bubbles: true,
    cancelable: true,
  });
}

/**
 * 等待元素出现
 */
export async function waitForElement(
  callback: () => HTMLElement | null,
  options: { timeout?: number; interval?: number } = {}
): Promise<HTMLElement> {
  const { timeout = 3000, interval = 50 } = options;
  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    const element = callback();
    if (element) return element;
    await wait(interval);
  }

  throw new Error('Element not found within timeout');
}

// 重新导出常用的测试工具
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';
