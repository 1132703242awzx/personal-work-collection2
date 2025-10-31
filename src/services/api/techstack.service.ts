/**
 * 技术栈服务
 * 处理技术栈数据库查询、搜索、趋势等功能
 */

import apiClient from './axios.instance';
import { API_CONFIG, MOCK_CONFIG } from '../../config/api.config';
import { TechStack, ApiResponse, TechStackDatabaseResponse } from '../../types';

class TechStackService {
  /**
   * 获取技术栈数据库
   * GET /api/tech-stacks
   */
  async getTechStacks(): Promise<TechStackDatabaseResponse> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockGetTechStacks();
    }

    try {
      const response = await apiClient.get<ApiResponse<TechStackDatabaseResponse>>(
        API_CONFIG.ENDPOINTS.TECH_STACKS
      );

      return response.data.data;
    } catch (error) {
      console.error('[TechStackService] getTechStacks failed:', error);
      throw error;
    }
  }

  /**
   * 获取趋势技术栈
   * GET /api/tech-stacks/trending
   */
  async getTrendingTechStacks(): Promise<TechStack[]> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockGetTrendingTechStacks();
    }

    try {
      const response = await apiClient.get<ApiResponse<{ stacks: TechStack[] }>>(
        API_CONFIG.ENDPOINTS.TECH_STACKS_TRENDING
      );

      return response.data.data.stacks;
    } catch (error) {
      console.error('[TechStackService] getTrendingTechStacks failed:', error);
      throw error;
    }
  }

  /**
   * 搜索技术栈
   * GET /api/tech-stacks/search?q=keyword
   */
  async searchTechStacks(query: string, category?: string): Promise<TechStack[]> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockSearchTechStacks(query, category);
    }

    try {
      const response = await apiClient.get<ApiResponse<{ stacks: TechStack[] }>>(
        API_CONFIG.ENDPOINTS.TECH_STACKS_SEARCH,
        {
          params: { q: query, category },
        }
      );

      return response.data.data.stacks;
    } catch (error) {
      console.error('[TechStackService] searchTechStacks failed:', error);
      throw error;
    }
  }

  /**
   * 获取特定分类的技术栈
   */
  async getTechStacksByCategory(category: string): Promise<TechStack[]> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      const allStacks = await this.mockGetTechStacks();
      return allStacks.categories[category] || [];
    }

    try {
      const response = await apiClient.get<ApiResponse<{ stacks: TechStack[] }>>(
        API_CONFIG.ENDPOINTS.TECH_STACKS,
        {
          params: { category },
        }
      );

      return response.data.data.stacks;
    } catch (error) {
      console.error('[TechStackService] getTechStacksByCategory failed:', error);
      throw error;
    }
  }

  // ==================== Mock 数据方法 ====================

  private async mockGetTechStacks(): Promise<TechStackDatabaseResponse> {
    await this.sleep(MOCK_CONFIG.DELAY);

    return {
      categories: {
        '前端框架': [
          {
            category: '前端框架',
            name: 'React',
            version: '^18.2.0',
            reason: '组件化开发，生态完善，社区活跃',
            priority: 'must-have',
          },
          {
            category: '前端框架',
            name: 'Vue 3',
            version: '^3.4.0',
            reason: '渐进式框架，学习曲线平缓，性能优秀',
            priority: 'must-have',
          },
          {
            category: '前端框架',
            name: 'Next.js',
            version: '^14.0.0',
            reason: 'React 全栈框架，支持 SSR/SSG',
            priority: 'recommended',
          },
        ],
        '状态管理': [
          {
            category: '状态管理',
            name: 'Redux Toolkit',
            version: '^2.0.0',
            reason: '强大的状态管理，适合复杂应用',
            priority: 'recommended',
          },
          {
            category: '状态管理',
            name: 'Zustand',
            version: '^4.5.0',
            reason: '轻量级状态管理，API 简洁',
            priority: 'recommended',
          },
          {
            category: '状态管理',
            name: 'Jotai',
            version: '^2.6.0',
            reason: '原子化状态管理，TypeScript 友好',
            priority: 'optional',
          },
        ],
        'UI 框架': [
          {
            category: 'UI 框架',
            name: 'Tailwind CSS',
            version: '^3.4.0',
            reason: '实用优先的 CSS 框架，开发效率高',
            priority: 'recommended',
          },
          {
            category: 'UI 框架',
            name: 'Ant Design',
            version: '^5.12.0',
            reason: '企业级 UI 组件库，组件丰富',
            priority: 'recommended',
          },
          {
            category: 'UI 框架',
            name: 'Material-UI',
            version: '^5.15.0',
            reason: 'Material Design 实现，定制性强',
            priority: 'optional',
          },
        ],
        '构建工具': [
          {
            category: '构建工具',
            name: 'Vite',
            version: '^5.0.0',
            reason: '极速开发体验，优化的生产构建',
            priority: 'must-have',
          },
          {
            category: '构建工具',
            name: 'Webpack',
            version: '^5.89.0',
            reason: '成熟的打包工具，插件生态丰富',
            priority: 'recommended',
          },
        ],
        '后端框架': [
          {
            category: '后端框架',
            name: 'NestJS',
            version: '^10.3.0',
            reason: 'TypeScript 企业级后端框架',
            priority: 'must-have',
          },
          {
            category: '后端框架',
            name: 'Express',
            version: '^4.18.0',
            reason: '轻量级 Node.js 框架，灵活度高',
            priority: 'recommended',
          },
        ],
        '数据库': [
          {
            category: '数据库',
            name: 'PostgreSQL',
            version: '^16.0',
            reason: '功能强大的关系型数据库',
            priority: 'must-have',
          },
          {
            category: '数据库',
            name: 'MongoDB',
            version: '^7.0',
            reason: '灵活的文档型数据库',
            priority: 'recommended',
          },
          {
            category: '数据库',
            name: 'Redis',
            version: '^7.2',
            reason: '高性能缓存和消息队列',
            priority: 'recommended',
          },
        ],
      },
      trending: [
        {
          category: '前端框架',
          name: 'Next.js 14',
          version: '^14.0.0',
          reason: 'App Router 架构，性能大幅提升',
          priority: 'must-have',
        },
        {
          category: 'AI 工具',
          name: 'LangChain',
          version: '^0.1.0',
          reason: 'LLM 应用开发框架，快速构建 AI 应用',
          priority: 'recommended',
        },
        {
          category: '状态管理',
          name: 'Zustand',
          version: '^4.5.0',
          reason: '极简状态管理，正在快速流行',
          priority: 'recommended',
        },
      ],
      lastUpdated: new Date().toISOString(),
    };
  }

  private async mockGetTrendingTechStacks(): Promise<TechStack[]> {
    await this.sleep(MOCK_CONFIG.DELAY);

    return [
      {
        category: '前端框架',
        name: 'Next.js 14',
        version: '^14.0.0',
        reason: 'App Router 架构，Server Components 支持',
        priority: 'must-have',
      },
      {
        category: 'AI 框架',
        name: 'LangChain.js',
        version: '^0.1.0',
        reason: '构建 LLM 驱动的应用，集成主流 AI 模型',
        priority: 'recommended',
      },
      {
        category: '状态管理',
        name: 'Zustand',
        version: '^4.5.0',
        reason: '轻量级、高性能，正在替代 Redux',
        priority: 'recommended',
      },
      {
        category: '全栈框架',
        name: 'Remix',
        version: '^2.4.0',
        reason: 'Web 标准优先，性能卓越',
        priority: 'optional',
      },
      {
        category: 'UI 库',
        name: 'Shadcn/ui',
        version: 'latest',
        reason: '基于 Radix UI，可定制性强',
        priority: 'recommended',
      },
    ];
  }

  private async mockSearchTechStacks(query: string, category?: string): Promise<TechStack[]> {
    await this.sleep(MOCK_CONFIG.DELAY / 2);

    const allStacks = await this.mockGetTechStacks();
    let results: TechStack[] = [];

    // 收集所有技术栈
    Object.values(allStacks.categories).forEach((stacks) => {
      results = results.concat(stacks);
    });

    // 按分类过滤
    if (category) {
      results = results.filter((stack) => stack.category === category);
    }

    // 按查询关键词过滤
    if (query) {
      const lowerQuery = query.toLowerCase();
      results = results.filter(
        (stack) =>
          stack.name.toLowerCase().includes(lowerQuery) ||
          stack.reason.toLowerCase().includes(lowerQuery)
      );
    }

    return results;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// 导出单例
export default new TechStackService();
