# 测试文档

本项目采用全面的测试策略,包含单元测试、组件测试、集成测试和端到端测试。

## 测试工具

- **Vitest**: 现代化的测试运行器 (与 Vite 深度集成)
- **React Testing Library**: React 组件测试库
- **MSW (Mock Service Worker)**: API 模拟工具
- **Cypress**: 端到端测试框架

## 快速开始

### 安装依赖

```bash
npm install
```

### 运行测试

```bash
# 运行所有单元测试和组件测试
npm test

# 运行测试并生成覆盖率报告
npm run test:coverage

# 运行测试 UI 界面
npm run test:ui

# 监听模式运行测试
npm run test:watch

# 运行 E2E 测试 (交互式)
npm run test:e2e

# 运行 E2E 测试 (无头模式)
npm run test:e2e:headless

# 运行所有测试 (单元测试 + E2E)
npm run test:all
```

## 测试结构

```
src/
├── test/
│   ├── setup.ts              # 测试环境全局设置
│   ├── utils.tsx             # 测试工具函数
│   └── mocks/
│       ├── handlers.ts       # MSW API handlers
│       ├── server.ts         # MSW server (Node.js 环境)
│       └── browser.ts        # MSW worker (浏览器环境)
├── hooks/
│   ├── useResponsive.ts
│   ├── useResponsive.test.ts # Hook 单元测试
│   ├── useDebounce.ts
│   └── useDebounce.test.ts
├── components/
│   ├── ProjectInput.tsx
│   ├── ProjectInput.test.tsx  # 组件测试
│   └── ...
└── services/
    ├── AIAdvisorService.ts
    └── AIAdvisorService.test.ts  # 集成测试

cypress/
├── e2e/
│   └── project-creation.cy.ts  # E2E 测试
└── support/
    ├── e2e.ts                   # E2E 支持文件
    └── component.ts             # 组件测试支持文件
```

## 测试类型

### 1. 单元测试

测试独立的函数、工具和 Hooks。

**示例: `useDebounce.test.ts`**

```typescript
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from '@/hooks/useDebounce';

it('应该在延迟后更新值', () => {
  const { result, rerender } = renderHook(
    ({ value, delay }) => useDebounce(value, delay),
    { initialProps: { value: 'initial', delay: 500 } }
  );

  rerender({ value: 'updated', delay: 500 });
  
  act(() => {
    vi.advanceTimersByTime(500);
  });

  expect(result.current).toBe('updated');
});
```

### 2. 组件测试

测试 React 组件的渲染和用户交互。

**示例: `ProjectInput.test.tsx`**

```typescript
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithAllProviders } from '@/test/utils';
import ProjectInput from '@/components/ProjectInput';

it('应该正确处理用户输入', async () => {
  const user = userEvent.setup();
  renderWithAllProviders(<ProjectInput />);

  const nameInput = screen.getByLabelText(/项目名称/i);
  await user.type(nameInput, '测试项目');

  expect(nameInput).toHaveValue('测试项目');
});
```

### 3. 集成测试

测试多个模块之间的集成,特别是 API 调用。

**示例: `AIAdvisorService.test.ts`**

```typescript
import { server } from '@/test/mocks/server';
import { AIAdvisorService } from '@/services/AIAdvisorService';

it('应该成功获取项目建议', async () => {
  const request = {
    name: '测试项目',
    description: '测试描述',
    techStack: ['React', 'TypeScript'],
  };

  const response = await AIAdvisorService.getSuggestions(request);

  expect(response.success).toBe(true);
  expect(response.data.suggestions).toHaveLength(3);
});
```

### 4. E2E 测试

测试完整的用户流程。

**示例: `project-creation.cy.ts`**

```typescript
it('应该成功创建一个新项目', () => {
  cy.visit('/');
  
  cy.fillProjectForm({
    name: '测试项目',
    description: '这是一个 E2E 测试项目',
    techStack: ['React', 'TypeScript', 'Vite'],
  });

  cy.get('button[type="submit"]').click();
  cy.contains('项目创建成功').should('be.visible');
});
```

## 测试工具函数

### renderWithProviders

包含 Redux Provider 的自定义渲染函数。

```typescript
import { renderWithProviders } from '@/test/utils';

const { store } = renderWithProviders(<MyComponent />, {
  preloadedState: {
    user: { isLoggedIn: true },
  },
});
```

### renderWithRouter

包含 Router 的自定义渲染函数。

```typescript
import { renderWithRouter } from '@/test/utils';

renderWithRouter(<MyComponent />, { route: '/dashboard' });
```

### renderWithAllProviders

包含所有 Providers (Redux + Router) 的自定义渲染函数。

```typescript
import { renderWithAllProviders } from '@/test/utils';

const { store } = renderWithAllProviders(<MyComponent />, {
  preloadedState: { /* ... */ },
  route: '/dashboard',
});
```

## API 模拟 (MSW)

MSW 用于模拟 API 请求,无需真实的后端服务器。

### 添加新的 API Handler

在 `src/test/mocks/handlers.ts` 中添加:

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id,
      name: '测试用户',
    });
  }),
];
```

### 在测试中覆盖 Handler

```typescript
import { server } from '@/test/mocks/server';
import { http, HttpResponse } from 'msw';

it('应该处理错误响应', async () => {
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json(
        { error: '用户不存在' },
        { status: 404 }
      );
    })
  );

  // 测试代码...
});
```

## 代码覆盖率

运行测试覆盖率:

```bash
npm run test:coverage
```

覆盖率报告会生成在 `coverage/` 目录:

- `coverage/index.html`: HTML 格式的详细报告
- `coverage/lcov.info`: LCOV 格式 (用于 CI/CD)

### 覆盖率目标

- **Lines**: 70%
- **Functions**: 70%
- **Branches**: 70%
- **Statements**: 70%

## 最佳实践

### 1. 测试文件命名

- 单元测试: `*.test.ts` 或 `*.spec.ts`
- 组件测试: `*.test.tsx` 或 `*.spec.tsx`
- E2E 测试: `*.cy.ts`

### 2. 测试描述

使用清晰的描述,遵循 "应该..." 模式:

```typescript
it('应该在用户点击提交按钮时调用 onSubmit', () => {
  // ...
});
```

### 3. 使用用户事件模拟

优先使用 `@testing-library/user-event` 而不是 `fireEvent`:

```typescript
// ✅ 推荐
import userEvent from '@testing-library/user-event';
const user = userEvent.setup();
await user.click(button);

// ❌ 避免
import { fireEvent } from '@testing-library/react';
fireEvent.click(button);
```

### 4. 避免实现细节

测试用户可见的行为,而不是实现细节:

```typescript
// ✅ 推荐 - 测试用户可见的内容
expect(screen.getByText('成功')).toBeInTheDocument();

// ❌ 避免 - 测试实现细节
expect(component.state.success).toBe(true);
```

### 5. 清理副作用

使用 `afterEach` 清理:

```typescript
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});
```

### 6. 使用假定时器

测试涉及时间的代码:

```typescript
beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.restoreAllMocks();
});

it('应该在延迟后执行', () => {
  // ...
  vi.advanceTimersByTime(1000);
  // ...
});
```

## 调试测试

### 查看 DOM

```typescript
import { screen } from '@testing-library/react';

screen.debug(); // 打印当前 DOM 树
```

### 使用测试 UI

```bash
npm run test:ui
```

打开浏览器界面,可以:
- 查看测试结果
- 重新运行特定测试
- 查看代码覆盖率
- 调试测试

### Cypress 调试

```bash
npm run test:e2e  # 打开 Cypress UI
```

在 Cypress UI 中:
- 实时查看测试执行
- 时间旅行调试
- 查看网络请求
- 截图和视频记录

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
      
      - name: Run E2E tests
        run: npm run test:e2e:headless
```

## 故障排除

### 1. 测试超时

增加超时时间:

```typescript
it('长时间运行的测试', async () => {
  // ...
}, { timeout: 10000 }); // 10 秒
```

### 2. 异步更新警告

使用 `waitFor` 等待异步更新:

```typescript
import { waitFor } from '@testing-library/react';

await waitFor(() => {
  expect(screen.getByText('加载完成')).toBeInTheDocument();
});
```

### 3. Mock 未生效

确保在 `beforeEach` 中重置 mock:

```typescript
beforeEach(() => {
  vi.clearAllMocks();
});
```

### 4. Cypress 端口冲突

检查 `cypress.config.ts` 中的 `baseUrl` 是否正确:

```typescript
export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173', // 确保与开发服务器端口一致
  },
});
```

## 参考资料

- [Vitest 文档](https://vitest.dev/)
- [React Testing Library 文档](https://testing-library.com/react)
- [MSW 文档](https://mswjs.io/)
- [Cypress 文档](https://docs.cypress.io/)
- [Testing Library 最佳实践](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
