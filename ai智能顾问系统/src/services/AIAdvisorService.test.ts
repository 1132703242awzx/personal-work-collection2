/**
 * AI Advisor Service 集成测试
 */

import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { server } from '@/test/mocks/server';
import { http, HttpResponse } from 'msw';
import { AIAdvisorService } from '@/services/AIAdvisorService';

// API 基础 URL
const API_BASE_URL = 'http://localhost:3000/api';

describe('AIAdvisorService 集成测试', () => {
  beforeAll(() => {
    server.listen();
  });

  afterEach(() => {
    server.resetHandlers();
  });

  afterAll(() => {
    server.close();
  });

  describe('getSuggestions', () => {
    it('应该成功获取项目建议', async () => {
      const request = {
        name: '测试项目',
        description: '测试描述',
        techStack: ['React', 'TypeScript'],
      };

      const response = await AIAdvisorService.getSuggestions(request);

      expect(response.success).toBe(true);
      expect(response.data.suggestions).toHaveLength(3);
      expect(response.data.suggestions[0]).toMatchObject({
        id: expect.any(String),
        title: expect.any(String),
        description: expect.any(String),
        priority: expect.any(String),
        category: expect.any(String),
      });
    });

    it('应该处理验证错误', async () => {
      // 覆盖默认 handler 返回错误
      server.use(
        http.post(`${API_BASE_URL}/advisor/suggestions`, () => {
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
        })
      );

      const request = {
        name: '',
        description: '',
        techStack: [],
      };

      await expect(AIAdvisorService.getSuggestions(request)).rejects.toThrow();
    });

    it('应该处理网络错误', async () => {
      server.use(
        http.post(`${API_BASE_URL}/advisor/suggestions`, () => {
          return HttpResponse.error();
        })
      );

      const request = {
        name: '测试项目',
        description: '测试描述',
        techStack: ['React'],
      };

      await expect(AIAdvisorService.getSuggestions(request)).rejects.toThrow();
    });

    it('应该处理超时', async () => {
      server.use(
        http.post(`${API_BASE_URL}/advisor/suggestions`, async () => {
          await new Promise(resolve => setTimeout(resolve, 10000));
          return HttpResponse.json({ success: true, data: {} });
        })
      );

      const request = {
        name: '测试项目',
        description: '测试描述',
        techStack: ['React'],
      };

      // 假设设置了 5 秒超时
      await expect(
        Promise.race([
          AIAdvisorService.getSuggestions(request),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Timeout')), 5000)
          ),
        ])
      ).rejects.toThrow('Timeout');
    });

    it('应该正确发送请求数据', async () => {
      let receivedData: any = null;

      server.use(
        http.post(`${API_BASE_URL}/advisor/suggestions`, async ({ request }) => {
          receivedData = await request.json();
          return HttpResponse.json({
            success: true,
            data: { suggestions: [] },
          });
        })
      );

      const requestData = {
        name: '测试项目',
        description: '测试描述',
        techStack: ['React', 'TypeScript', 'Vite'],
      };

      await AIAdvisorService.getSuggestions(requestData);

      expect(receivedData).toEqual(requestData);
    });

    it('应该处理服务器错误响应', async () => {
      server.use(
        http.post(`${API_BASE_URL}/advisor/suggestions`, () => {
          return HttpResponse.json(
            {
              success: false,
              error: {
                code: 'INTERNAL_ERROR',
                message: '服务器内部错误',
              },
            },
            { status: 500 }
          );
        })
      );

      const request = {
        name: '测试项目',
        description: '测试描述',
        techStack: ['React'],
      };

      await expect(AIAdvisorService.getSuggestions(request)).rejects.toThrow();
    });

    it('应该处理空响应', async () => {
      server.use(
        http.post(`${API_BASE_URL}/advisor/suggestions`, () => {
          return HttpResponse.json({
            success: true,
            data: { suggestions: [] },
          });
        })
      );

      const request = {
        name: '测试项目',
        description: '测试描述',
        techStack: ['React'],
      };

      const response = await AIAdvisorService.getSuggestions(request);

      expect(response.data.suggestions).toEqual([]);
    });

    it('应该包含正确的请求头', async () => {
      let requestHeaders: Headers | null = null;

      server.use(
        http.post(`${API_BASE_URL}/advisor/suggestions`, ({ request }) => {
          requestHeaders = request.headers;
          return HttpResponse.json({
            success: true,
            data: { suggestions: [] },
          });
        })
      );

      const request = {
        name: '测试项目',
        description: '测试描述',
        techStack: ['React'],
      };

      await AIAdvisorService.getSuggestions(request);

      expect(requestHeaders?.get('Content-Type')).toBe('application/json');
    });
  });

  describe('getProjectDetails', () => {
    it('应该成功获取项目详情', async () => {
      const projectId = 'test-project-id';
      const response = await AIAdvisorService.getProjectDetails(projectId);

      expect(response.success).toBe(true);
      expect(response.data).toMatchObject({
        id: projectId,
        name: expect.any(String),
        description: expect.any(String),
      });
    });

    it('应该处理不存在的项目', async () => {
      server.use(
        http.get(`${API_BASE_URL}/projects/:id`, () => {
          return HttpResponse.json(
            {
              success: false,
              error: {
                code: 'NOT_FOUND',
                message: '项目不存在',
              },
            },
            { status: 404 }
          );
        })
      );

      await expect(
        AIAdvisorService.getProjectDetails('non-existent-id')
      ).rejects.toThrow();
    });
  });

  describe('createProject', () => {
    it('应该成功创建项目', async () => {
      const projectData = {
        name: '新项目',
        description: '新项目描述',
      };

      const response = await AIAdvisorService.createProject(projectData);

      expect(response.success).toBe(true);
      expect(response.data).toMatchObject({
        id: expect.any(String),
        name: projectData.name,
        description: projectData.description,
      });
    });

    it('应该验证必填字段', async () => {
      server.use(
        http.post(`${API_BASE_URL}/projects`, () => {
          return HttpResponse.json(
            {
              success: false,
              error: {
                code: 'VALIDATION_ERROR',
                message: '项目名称不能为空',
              },
            },
            { status: 400 }
          );
        })
      );

      const invalidData = {
        name: '',
        description: '描述',
      };

      await expect(
        AIAdvisorService.createProject(invalidData)
      ).rejects.toThrow();
    });
  });
});
