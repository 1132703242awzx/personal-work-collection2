/**
 * MSW API 模拟 handlers
 */

import { http, HttpResponse } from 'msw';

// API 基础 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

export const handlers = [
  // 获取项目建议 - 成功响应
  http.post(`${API_BASE_URL}/advisor/suggestions`, async ({ request }) => {
    const body = await request.json();
    
    return HttpResponse.json({
      success: true,
      data: {
        suggestions: [
          {
            id: '1',
            title: '技术栈建议',
            description: '建议使用 React 19 + TypeScript + Vite',
            priority: 'high',
            category: 'technology',
          },
          {
            id: '2',
            title: '架构建议',
            description: '建议采用组件化架构，使用 Redux Toolkit 管理状态',
            priority: 'medium',
            category: 'architecture',
          },
          {
            id: '3',
            title: '性能优化建议',
            description: '建议实现虚拟滚动、懒加载等性能优化策略',
            priority: 'low',
            category: 'performance',
          },
        ],
        metadata: {
          processedAt: new Date().toISOString(),
          requestId: 'test-request-id',
        },
      },
    });
  }),

  // 获取项目建议 - 错误响应
  http.post(`${API_BASE_URL}/advisor/suggestions/error`, () => {
    return HttpResponse.json(
      {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '请求参数验证失败',
        },
      },
      { status: 400 }
    );
  }),

  // 获取项目建议 - 网络错误
  http.post(`${API_BASE_URL}/advisor/suggestions/network-error`, () => {
    return HttpResponse.error();
  }),

  // 获取项目详情
  http.get(`${API_BASE_URL}/projects/:id`, ({ params }) => {
    const { id } = params;
    
    return HttpResponse.json({
      success: true,
      data: {
        id,
        name: `测试项目 ${id}`,
        description: '这是一个测试项目',
        createdAt: new Date().toISOString(),
      },
    });
  }),

  // 创建项目
  http.post(`${API_BASE_URL}/projects`, async ({ request }) => {
    const body = await request.json();
    
    return HttpResponse.json(
      {
        success: true,
        data: {
          id: 'new-project-id',
          ...body,
          createdAt: new Date().toISOString(),
        },
      },
      { status: 201 }
    );
  }),

  // 更新项目
  http.put(`${API_BASE_URL}/projects/:id`, async ({ params, request }) => {
    const { id } = params;
    const body = await request.json();
    
    return HttpResponse.json({
      success: true,
      data: {
        id,
        ...body,
        updatedAt: new Date().toISOString(),
      },
    });
  }),

  // 删除项目
  http.delete(`${API_BASE_URL}/projects/:id`, ({ params }) => {
    const { id } = params;
    
    return HttpResponse.json({
      success: true,
      data: {
        id,
        deleted: true,
      },
    });
  }),

  // 获取用户信息
  http.get(`${API_BASE_URL}/user/profile`, () => {
    return HttpResponse.json({
      success: true,
      data: {
        id: 'test-user-id',
        name: '测试用户',
        email: 'test@example.com',
        avatar: 'https://via.placeholder.com/150',
      },
    });
  }),

  // 文件上传
  http.post(`${API_BASE_URL}/upload`, async ({ request }) => {
    const formData = await request.formData();
    const file = formData.get('file');
    
    return HttpResponse.json({
      success: true,
      data: {
        url: `https://example.com/uploads/${file?.toString()}`,
        filename: file?.toString(),
        size: 1024,
      },
    });
  }),
];
