/**
 * 测试配置验证
 */

import { describe, it, expect } from 'vitest';

describe('测试环境配置', () => {
  it('应该正确加载 Vitest', () => {
    expect(true).toBe(true);
  });

  it('应该支持基本断言', () => {
    const value = 'test';
    expect(value).toBe('test');
    expect(value).toBeTruthy();
    expect(value).toHaveLength(4);
  });

  it('应该支持异步测试', async () => {
    const promise = Promise.resolve('success');
    await expect(promise).resolves.toBe('success');
  });

  it('应该支持 DOM 匹配器', () => {
    const element = document.createElement('div');
    element.textContent = 'Hello World';
    
    expect(element).toBeInTheDocument;
    expect(element.textContent).toBe('Hello World');
  });
});
