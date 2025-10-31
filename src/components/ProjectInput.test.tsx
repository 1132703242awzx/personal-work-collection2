/**
 * ProjectInput 组件测试
 */

import { describe, it, expect, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithAllProviders } from '@/test/utils';
import { ProjectInput } from '@/components/ProjectInput';

describe('ProjectInput', () => {
  it('应该正确渲染所有表单字段', () => {
    renderWithAllProviders(<ProjectInput />);

    expect(screen.getByLabelText(/项目名称/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/项目描述/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/技术栈/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /提交/i })).toBeInTheDocument();
  });

  it('应该验证必填字段', async () => {
    const user = userEvent.setup();
    renderWithAllProviders(<ProjectInput />);

    const submitButton = screen.getByRole('button', { name: /提交/i });
    
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/项目名称不能为空/i)).toBeInTheDocument();
    });
  });

  it('应该正确处理用户输入', async () => {
    const user = userEvent.setup();
    renderWithAllProviders(<ProjectInput />);

    const nameInput = screen.getByLabelText(/项目名称/i);
    const descInput = screen.getByLabelText(/项目描述/i);

    await user.type(nameInput, '测试项目');
    await user.type(descInput, '这是一个测试项目描述');

    expect(nameInput).toHaveValue('测试项目');
    expect(descInput).toHaveValue('这是一个测试项目描述');
  });

  it('应该在提交时调用 onSubmit 回调', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    
    renderWithAllProviders(<ProjectInput onSubmit={onSubmit} />);

    const nameInput = screen.getByLabelText(/项目名称/i);
    const submitButton = screen.getByRole('button', { name: /提交/i });

    await user.type(nameInput, '测试项目');
    await user.click(submitButton);

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          name: '测试项目',
        })
      );
    });
  });

  it('应该在提交过程中禁用提交按钮', async () => {
    const user = userEvent.setup();
    const slowSubmit = vi.fn(() => new Promise(resolve => setTimeout(resolve, 1000)));
    
    renderWithAllProviders(<ProjectInput onSubmit={slowSubmit} />);

    const nameInput = screen.getByLabelText(/项目名称/i);
    const submitButton = screen.getByRole('button', { name: /提交/i });

    await user.type(nameInput, '测试项目');
    await user.click(submitButton);

    expect(submitButton).toBeDisabled();

    await waitFor(() => {
      expect(submitButton).not.toBeDisabled();
    }, { timeout: 2000 });
  });

  it('应该正确显示错误消息', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn(() => Promise.reject(new Error('提交失败')));
    
    renderWithAllProviders(<ProjectInput onSubmit={onSubmit} />);

    const nameInput = screen.getByLabelText(/项目名称/i);
    const submitButton = screen.getByRole('button', { name: /提交/i });

    await user.type(nameInput, '测试项目');
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/提交失败/i)).toBeInTheDocument();
    });
  });

  it('应该支持清除表单', async () => {
    const user = userEvent.setup();
    renderWithAllProviders(<ProjectInput />);

    const nameInput = screen.getByLabelText(/项目名称/i);
    const clearButton = screen.getByRole('button', { name: /清除/i });

    await user.type(nameInput, '测试项目');
    expect(nameInput).toHaveValue('测试项目');

    await user.click(clearButton);
    expect(nameInput).toHaveValue('');
  });

  it('应该在移动设备上正确渲染', () => {
    // Mock 移动设备
    window.matchMedia = vi.fn().mockImplementation(query => ({
      matches: query === '(max-width: 768px)',
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    renderWithAllProviders(<ProjectInput />);

    // 验证移动端样式或布局
    const form = screen.getByRole('form');
    expect(form).toHaveClass('mobile-layout');
  });

  it('应该支持键盘导航', async () => {
    const user = userEvent.setup();
    renderWithAllProviders(<ProjectInput />);

    const nameInput = screen.getByLabelText(/项目名称/i);
    
    await user.tab();
    expect(nameInput).toHaveFocus();

    await user.tab();
    expect(screen.getByLabelText(/项目描述/i)).toHaveFocus();
  });

  it('应该在字段值变化时更新状态', async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();
    
    renderWithAllProviders(<ProjectInput onChange={onChange} />);

    const nameInput = screen.getByLabelText(/项目名称/i);
    
    await user.type(nameInput, 'A');

    await waitFor(() => {
      expect(onChange).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'A',
        })
      );
    });
  });
});
