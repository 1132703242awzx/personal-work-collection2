/**
 * 推荐服务
 * 处理需求分析、AI 提示词生成等核心业务逻辑
 */

import apiClient from './axios.instance';
import { API_CONFIG, MOCK_CONFIG } from '../../config/api.config';
import {
  ProjectRequirements,
  AnalyzeRequirementsRequest,
  AnalyzeRequirementsResponse,
  GeneratePromptsRequest,
  GeneratePromptsResponse,
  TechStack,
  AIPrompt,
  DevelopmentAdvice,
  ApiResponse,
} from '../../types';

class RecommendationService {
  /**
   * 分析需求并生成推荐
   * POST /api/analyze-requirements
   */
  async analyzeRequirements(
    requirements: ProjectRequirements
  ): Promise<AnalyzeRequirementsResponse> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockAnalyzeRequirements(requirements);
    }

    try {
      const response = await apiClient.post<ApiResponse<AnalyzeRequirementsResponse>>(
        API_CONFIG.ENDPOINTS.ANALYZE_REQUIREMENTS,
        { requirements } as AnalyzeRequirementsRequest
      );

      return response.data.data;
    } catch (error) {
      console.error('[RecommendationService] analyzeRequirements failed:', error);
      throw error;
    }
  }

  /**
   * 生成 AI 提示词
   * POST /api/generate-prompts
   */
  async generatePrompts(
    techStack: TechStack[],
    requirements?: Partial<ProjectRequirements>
  ): Promise<GeneratePromptsResponse> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockGeneratePrompts(techStack, requirements);
    }

    try {
      const response = await apiClient.post<ApiResponse<GeneratePromptsResponse>>(
        API_CONFIG.ENDPOINTS.GENERATE_PROMPTS,
        { techStack, requirements } as GeneratePromptsRequest
      );

      return response.data.data;
    } catch (error) {
      console.error('[RecommendationService] generatePrompts failed:', error);
      throw error;
    }
  }

  /**
   * 优化现有提示词
   * POST /api/generate-prompts/optimize
   */
  async optimizePrompts(prompts: AIPrompt[]): Promise<AIPrompt[]> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      await this.sleep(MOCK_CONFIG.DELAY);
      return prompts.map(p => ({
        ...p,
        suggestions: [...p.suggestions, '已优化：增加更多细节'],
      }));
    }

    try {
      const response = await apiClient.post<ApiResponse<{ prompts: AIPrompt[] }>>(
        API_CONFIG.ENDPOINTS.OPTIMIZE_PROMPTS,
        { prompts }
      );

      return response.data.data.prompts;
    } catch (error) {
      console.error('[RecommendationService] optimizePrompts failed:', error);
      throw error;
    }
  }

  /**
   * 重新生成提示词（基于反馈）
   */
  async regeneratePrompts(
    originalPrompts: AIPrompt,
    feedback: string
  ): Promise<AIPrompt> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      await this.sleep(MOCK_CONFIG.DELAY);
      return {
        ...originalPrompts,
        prompt: `${originalPrompts.prompt}\n\n根据您的反馈"${feedback}"，我已调整建议。`,
        suggestions: [
          ...originalPrompts.suggestions,
          `基于反馈优化：${feedback}`,
        ],
      };
    }

    try {
      const response = await apiClient.post<ApiResponse<{ prompt: AIPrompt }>>(
        `${API_CONFIG.ENDPOINTS.GENERATE_PROMPTS}/regenerate`,
        { originalPrompts, feedback }
      );

      return response.data.data.prompt;
    } catch (error) {
      console.error('[RecommendationService] regeneratePrompts failed:', error);
      throw error;
    }
  }

  // ==================== Mock 数据方法 ====================

  private async mockAnalyzeRequirements(
    requirements: ProjectRequirements
  ): Promise<AnalyzeRequirementsResponse> {
    await this.sleep(MOCK_CONFIG.DELAY);

    const techStack: TechStack[] = [
      {
        category: '前端框架',
        name: 'React 18 + TypeScript',
        version: '^18.2.0',
        reason: '组件化开发，强类型支持，生态完善',
        priority: 'must-have',
      },
      {
        category: '状态管理',
        name: 'Redux Toolkit',
        version: '^2.0.0',
        reason: '强大的状态管理，适合复杂应用',
        priority: 'recommended',
      },
      {
        category: 'UI 框架',
        name: 'Tailwind CSS',
        version: '^3.4.0',
        reason: '实用优先的 CSS 框架，快速构建现代 UI',
        priority: 'recommended',
      },
      {
        category: '构建工具',
        name: 'Vite',
        version: '^5.0.0',
        reason: '极速开发体验，优化的生产构建',
        priority: 'must-have',
      },
    ];

    const prompts: AIPrompt = {
      prompt: `请帮我开发一个${requirements.projectType}类型的项目

项目描述：${requirements.description}

目标平台：${requirements.targetPlatform.join('、')}

核心功能：
${requirements.features.map((f, i) => `${i + 1}. ${f}`).join('\n')}

复杂度：${requirements.complexity}/10
预算：${requirements.budget}
${requirements.timeline ? `时间线：${requirements.timeline}` : ''}
${requirements.teamSize ? `团队规模：${requirements.teamSize}人` : ''}

请提供：
1. 详细的技术架构建议
2. 推荐的技术栈和工具
3. 开发步骤和最佳实践
4. 潜在的技术挑战和解决方案`,
      context: `这是一个${requirements.projectType}项目，复杂度为${requirements.complexity}/10，需要实现${requirements.features.join('、')}等功能。`,
      suggestions: [
        '考虑使用微服务架构提高系统可扩展性',
        '实施 CI/CD 流程确保代码质量',
        '采用容器化部署（Docker/Kubernetes）',
        '建立完善的监控和日志系统',
        '遵循 SOLID 原则和设计模式',
      ],
    };

    const suggestions: DevelopmentAdvice[] = [
      {
        phase: '需求分析',
        tasks: [
          '与利益相关者沟通，明确需求',
          '制作原型图和用户流程图',
          '评估技术可行性和风险',
          '制定详细的功能规格说明',
        ],
        estimatedTime: '1-2 周',
        resources: ['产品经理', 'UI/UX 设计师'],
      },
      {
        phase: '架构设计',
        tasks: [
          '设计系统架构和数据模型',
          '选择合适的技术栈',
          '规划 API 接口设计',
          '制定代码规范和开发流程',
        ],
        estimatedTime: '1 周',
        resources: ['架构师', '技术负责人'],
      },
      {
        phase: '开发实施',
        tasks: [
          '搭建开发环境和基础框架',
          '实现核心功能模块',
          '编写单元测试和集成测试',
          '进行代码审查和重构',
        ],
        estimatedTime: `${Math.ceil(requirements.complexity * 0.5)} 周`,
        resources: ['前端开发', '后端开发', 'QA 工程师'],
      },
      {
        phase: '测试部署',
        tasks: [
          '执行全面的功能测试',
          '性能优化和压力测试',
          '部署到生产环境',
          '监控系统运行状态',
        ],
        estimatedTime: '1-2 周',
        resources: ['DevOps 工程师', 'QA 团队'],
      },
    ];

    return {
      techStack,
      prompts,
      suggestions,
      estimatedCost: this.calculateEstimatedCost(requirements),
      estimatedDuration: this.calculateEstimatedDuration(requirements),
    };
  }

  private async mockGeneratePrompts(
    techStack: TechStack[],
    _requirements?: Partial<ProjectRequirements>
  ): Promise<GeneratePromptsResponse> {
    await this.sleep(MOCK_CONFIG.DELAY);

    const prompts: AIPrompt[] = techStack.slice(0, 3).map((tech) => ({
      prompt: `如何在项目中最佳实践使用 ${tech.name}？

技术栈：${tech.name} ${tech.version || ''}
优先级：${tech.priority}
选择理由：${tech.reason}

请提供：
1. 详细的配置步骤
2. 最佳实践建议
3. 常见问题和解决方案
4. 性能优化技巧`,
      context: `使用 ${tech.name} 作为${tech.category}解决方案`,
      suggestions: [
        '遵循官方推荐的项目结构',
        '实施代码分割和懒加载',
        '配置开发和生产环境',
        '集成 TypeScript 提高代码质量',
      ],
    }));

    const optimizationSuggestions = [
      '合理使用缓存策略提升性能',
      '实施自动化测试保证质量',
      '采用模块化设计提高可维护性',
      '建立监控和日志系统',
      '定期进行代码审查和重构',
    ];

    return { prompts, optimizationSuggestions };
  }

  private calculateEstimatedCost(requirements: ProjectRequirements): string {
    const baseCost = 50000;
    const complexityMultiplier = requirements.complexity * 0.2;
    const featureMultiplier = requirements.features.length * 5000;
    
    const total = baseCost * (1 + complexityMultiplier) + featureMultiplier;
    
    return `¥${(total / 10000).toFixed(1)}万 - ¥${(total * 1.5 / 10000).toFixed(1)}万`;
  }

  private calculateEstimatedDuration(requirements: ProjectRequirements): string {
    const baseWeeks = 4;
    const complexityWeeks = requirements.complexity * 0.5;
    const featureWeeks = requirements.features.length * 0.3;
    
    const totalWeeks = Math.ceil(baseWeeks + complexityWeeks + featureWeeks);
    
    if (totalWeeks <= 4) {
      return `${totalWeeks} 周`;
    } else if (totalWeeks <= 12) {
      return `${Math.ceil(totalWeeks / 4)} 个月`;
    } else {
      return `${(totalWeeks / 12).toFixed(1)} 年`;
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// 导出单例
export default new RecommendationService();
