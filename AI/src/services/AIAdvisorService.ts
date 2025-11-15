import { ProjectRequirement, AnalysisResult, AIPrompt, TechStack, DevelopmentAdvice } from '../types';
import { AIProviderManager, AIMessage, AIConfig } from './AIProviderManager';

export class AIAdvisorService {
  // AI API 配置 (从环境变量加载)
  private static aiConfig: AIConfig | null = null;

  /**
   * 初始化 AI 配置
   */
  private static initAIConfig(): void {
    if (!this.aiConfig) {
      this.aiConfig = AIProviderManager.getConfigFromEnv();
      if (this.aiConfig) {
        console.log(`✅ AI Provider configured: ${this.aiConfig.provider} (${this.aiConfig.model})`);
      } else {
        console.log('ℹ️ No AI provider configured, using built-in intelligent algorithm');
      }
    }
  }

  // 分析项目复杂度
  private static analyzeComplexity(requirement: ProjectRequirement): {
    level: 'simple' | 'moderate' | 'complex' | 'enterprise';
    score: number;
    factors: string[];
  } {
    let score = 0;
    const factors: string[] = [];

    // 功能数量评分
    if (requirement.features.length > 10) {
      score += 3;
      factors.push('功能数量较多');
    } else if (requirement.features.length > 5) {
      score += 2;
      factors.push('功能数量适中');
    } else {
      score += 1;
      factors.push('功能数量较少');
    }

    // 平台数量评分
    if (requirement.targetPlatform.length >= 3) {
      score += 3;
      factors.push('需要多平台支持');
    } else if (requirement.targetPlatform.length === 2) {
      score += 2;
      factors.push('需要跨平台支持');
    }

    // 项目类型评分
    const category = requirement.category.toLowerCase();
    if (category.includes('企业') || category.includes('全栈')) {
      score += 3;
      factors.push('企业级应用复杂度高');
    } else if (category.includes('电商') || category.includes('社交')) {
      score += 2;
      factors.push('中等业务复杂度');
    }

    // 技术约束评分
    if (requirement.technicalConstraints && requirement.technicalConstraints.length > 50) {
      score += 2;
      factors.push('有特殊技术约束');
    }

    // 用户故事评分
    if (requirement.userStory && requirement.userStory.length > 100) {
      score += 1;
      factors.push('用户需求详细明确');
    }

    let level: 'simple' | 'moderate' | 'complex' | 'enterprise';
    if (score <= 3) level = 'simple';
    else if (score <= 6) level = 'moderate';
    else if (score <= 9) level = 'complex';
    else level = 'enterprise';

    return { level, score, factors };
  }

  // 生成智能 AI 提示词
  static generateAIPrompt(requirement: ProjectRequirement): AIPrompt {
    const platformStr = requirement.targetPlatform.join('、');
    const featuresStr = requirement.features.slice(0, 5).join('、');
    const complexity = this.analyzeComplexity(requirement);

    // 根据复杂度生成不同的提示词
    const complexityIntro = {
      simple: '这是一个相对简单的项目，适合快速开发和迭代。',
      moderate: '这是一个中等复杂度的项目，需要合理规划架构和技术选型。',
      complex: '这是一个复杂的项目，需要深思熟虑的架构设计和技术选型。',
      enterprise: '这是一个企业级项目，需要高可用、可扩展的架构设计。',
    }[complexity.level];

    const prompt = `# 项目开发需求分析

## 项目概述
**项目名称**: ${requirement.projectName}
**项目类型**: ${requirement.category}
**复杂度评估**: ${complexity.level.toUpperCase()} (评分: ${complexity.score}/12)

${complexityIntro}

## 详细描述
${requirement.description}

## 目标平台
${requirement.targetPlatform.map((p, i) => `${i + 1}. ${p}`).join('\n')}

## 核心功能需求
${requirement.features.map((f, i) => `${i + 1}. ${f}`).join('\n')}

${requirement.userStory ? `## 用户故事\n${requirement.userStory}\n` : ''}
${requirement.technicalConstraints ? `## 技术约束\n${requirement.technicalConstraints}\n` : ''}

## 复杂度分析因素
${complexity.factors.map(f => `- ${f}`).join('\n')}

## 请 AI 顾问提供以下内容

### 1. 系统架构设计
- 推荐的架构模式（单体/微服务/Serverless）
- 前后端分离方案
- 数据流设计
- 缓存策略

### 2. 技术栈选型理由
- 前端框架和生态选择
- 后端技术栈选择
- 数据库设计方案
- 第三方服务集成建议

### 3. 开发计划与最佳实践
- 分阶段开发计划
- 代码规范和团队协作
- 测试策略（单元/集成/E2E）
- 性能优化方案

### 4. 潜在风险与解决方案
- 技术风险识别
- 性能瓶颈预测
- 安全性考虑
- 可扩展性设计

### 5. 成本与时间估算
- 开发周期预估
- 团队规模建议
- 基础设施成本
- 维护成本预估`;

    const context = `这是一个${requirement.category}项目（复杂度: ${complexity.level}），目标平台为${platformStr}。核心功能包括${featuresStr}等。项目规模评分为 ${complexity.score}/12，${complexity.factors.join('，')}。`;

    // 根据复杂度生成智能建议
    const suggestions: string[] = [];
    
    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      suggestions.push(
        '🏗️ 建议采用微服务架构，便于团队协作和模块化开发',
        '🚀 实施完整的 CI/CD 流程，包括自动化测试和部署',
        '📊 建立完善的监控体系（APM、日志聚合、告警系统）',
        '🔒 重视安全性设计，实施 OAuth2.0/JWT 认证授权',
        '⚡ 考虑使用 CDN 和负载均衡提高性能'
      );
    } else if (complexity.level === 'moderate') {
      suggestions.push(
        '🏛️ 建议采用模块化的单体架构，预留微服务化可能',
        '🔄 实施基础的 CI/CD 流程确保代码质量',
        '📈 使用 Docker 容器化部署，简化运维',
        '🧪 编写核心功能的单元测试和集成测试',
        '💾 合理使用缓存（Redis）提升性能'
      );
    } else {
      suggestions.push(
        '⚡ 快速原型开发，使用成熟的脚手架和模板',
        '☁️ 考虑使用 Vercel/Netlify 等平台快速部署',
        '📦 选择轻量级的技术栈，降低学习成本',
        '🔧 使用 Git 进行版本控制，建立基础开发规范',
        '📱 优先考虑移动端适配和响应式设计'
      );
    }

    // 添加平台特定建议
    if (requirement.targetPlatform.some(p => p.includes('移动') || p.toLowerCase().includes('mobile'))) {
      suggestions.push('📱 考虑使用 React Native 或 Flutter 实现真正的跨平台开发');
    }
    if (requirement.targetPlatform.some(p => p.includes('Web') || p.includes('网页'))) {
      suggestions.push('🌐 实施 PWA 技术，提供类原生应用体验');
    }
    if (requirement.features.some(f => f.includes('实时') || f.includes('消息'))) {
      suggestions.push('💬 使用 WebSocket 或 Server-Sent Events 实现实时通信');
    }

    return { prompt, context, suggestions };
  }

  // 智能推荐技术栈
  static recommendTechStack(requirement: ProjectRequirement): TechStack[] {
    const stacks: TechStack[] = [];
    const category = requirement.category.toLowerCase();
    const platforms = requirement.targetPlatform.map(p => p.toLowerCase());
    const features = requirement.features.map(f => f.toLowerCase());
    const complexity = this.analyzeComplexity(requirement);

    // === 前端技术栈 ===
    if (platforms.some(p => p.includes('web') || p.includes('网页') || p.includes('h5'))) {
      // 前端框架
      if (complexity.level === 'enterprise' || complexity.level === 'complex') {
        stacks.push({
          category: '前端框架',
          name: 'React 18 + TypeScript + Vite',
          version: '^18.3.0',
          reason: '企业级项目推荐，强类型保证代码质量，Vite 提供极速开发体验',
          priority: 'must-have',
        });
      } else {
        stacks.push({
          category: '前端框架',
          name: 'React 18 + Vite',
          version: '^18.3.0',
          reason: '现代化前端开发框架，生态完善，开发效率高',
          priority: 'must-have',
        });
      }

      // 状态管理
      if (complexity.level === 'enterprise' || features.some(f => f.includes('实时') || f.includes('协作'))) {
        stacks.push({
          category: '状态管理',
          name: 'Redux Toolkit + RTK Query',
          version: '^2.0.0',
          reason: '复杂状态管理 + 数据获取和缓存一体化方案',
          priority: 'must-have',
        });
      } else if (complexity.level === 'complex') {
        stacks.push({
          category: '状态管理',
          name: 'Zustand',
          version: '^4.5.0',
          reason: '轻量级状态管理，API 简洁，性能优秀',
          priority: 'recommended',
        });
      } else {
        stacks.push({
          category: '状态管理',
          name: 'React Context + Hooks',
          reason: '简单项目使用内置方案即可，无需额外依赖',
          priority: 'recommended',
        });
      }

      // UI 框架
      if (category.includes('企业') || category.includes('管理') || category.includes('后台')) {
        stacks.push({
          category: 'UI 组件库',
          name: 'Ant Design',
          version: '^5.12.0',
          reason: '企业级 UI 组件库，开箱即用的中后台解决方案',
          priority: 'must-have',
        });
      } else if (category.includes('电商') || features.some(f => f.includes('商品') || f.includes('订单'))) {
        stacks.push({
          category: 'UI 组件库',
          name: 'Ant Design Mobile / Vant',
          reason: '移动端电商 UI 组件库，丰富的业务组件',
          priority: 'recommended',
        });
      } else {
        stacks.push({
          category: 'UI 组件库',
          name: 'Material-UI / Chakra UI',
          reason: '现代化设计系统，灵活的主题定制',
          priority: 'recommended',
        });
      }

      // 样式方案
      if (complexity.level === 'enterprise' || complexity.level === 'complex') {
        stacks.push({
          category: '样式方案',
          name: 'TailwindCSS + CSS Modules',
          reason: '原子化 CSS + 模块化样式，避免样式冲突',
          priority: 'recommended',
        });
      } else {
        stacks.push({
          category: '样式方案',
          name: 'Styled-components / Emotion',
          reason: 'CSS-in-JS 方案，组件化样式管理',
          priority: 'optional',
        });
      }

      // 路由
      stacks.push({
        category: '路由管理',
        name: 'React Router v6',
        version: '^6.20.0',
        reason: 'React 官方推荐路由库，支持嵌套路由和懒加载',
        priority: 'must-have',
      });

      // 数据可视化
      if (features.some(f => f.includes('图表') || f.includes('数据') || f.includes('统计') || f.includes('可视化'))) {
        stacks.push({
          category: '数据可视化',
          name: 'ECharts / Recharts',
          reason: '强大的数据可视化库，支持丰富的图表类型',
          priority: 'must-have',
        });
      }

      // 表单处理
      if (features.some(f => f.includes('表单') || f.includes('输入') || f.includes('注册'))) {
        stacks.push({
          category: '表单管理',
          name: 'React Hook Form + Zod',
          reason: '高性能表单库 + TypeScript 优先的校验库',
          priority: 'recommended',
        });
      }
    }

    // === 移动端技术栈 ===
    if (platforms.some(p => p.includes('mobile') || p.includes('移动') || p.includes('app'))) {
      if (platforms.length >= 2) {
        stacks.push({
          category: '跨平台开发',
          name: 'React Native + Expo',
          version: '^0.73.0',
          reason: '一套代码同时支持 iOS 和 Android，开发效率高',
          priority: 'must-have',
        });
      } else {
        stacks.push({
          category: '移动端开发',
          name: 'Flutter',
          reason: '高性能跨平台框架，原生体验',
          priority: 'recommended',
        });
      }

      stacks.push({
        category: '移动端 UI',
        name: 'React Native Paper / NativeBase',
        reason: 'Material Design 风格的移动端组件库',
        priority: 'recommended',
      });
    }

    // === 后端技术栈 ===
    if (category.includes('全栈') || category.includes('后端') || complexity.level === 'enterprise') {
      // 后端框架
      if (complexity.level === 'enterprise' || complexity.level === 'complex') {
        stacks.push({
          category: '后端框架',
          name: 'NestJS + TypeScript',
          version: '^10.0.0',
          reason: '企业级 Node.js 框架，架构清晰，支持微服务',
          priority: 'must-have',
        });
      } else {
        stacks.push({
          category: '后端框架',
          name: 'Express.js / Fastify',
          reason: '轻量级 Node.js 框架，灵活高效',
          priority: 'must-have',
        });
      }

      // 数据库选择
      if (features.some(f => f.includes('用户') || f.includes('订单') || f.includes('交易'))) {
        stacks.push({
          category: '主数据库',
          name: 'PostgreSQL',
          version: '^16.0',
          reason: '功能强大的关系型数据库，支持 JSONB 和全文搜索',
          priority: 'must-have',
        });
      } else {
        stacks.push({
          category: '主数据库',
          name: 'MongoDB',
          reason: '灵活的文档型数据库，适合快速迭代',
          priority: 'recommended',
        });
      }

      // 缓存层
      if (complexity.level !== 'simple') {
        stacks.push({
          category: '缓存',
          name: 'Redis',
          version: '^7.0',
          reason: '高性能缓存和消息队列，支持多种数据结构',
          priority: 'must-have',
        });
      }

      // ORM
      stacks.push({
        category: 'ORM',
        name: 'Prisma / TypeORM',
        reason: 'TypeScript 优先的 ORM，类型安全的数据库访问',
        priority: 'must-have',
      });

      // API 设计
      if (complexity.level === 'enterprise' || complexity.level === 'complex') {
        stacks.push({
          category: 'API 设计',
          name: 'GraphQL + Apollo Server',
          reason: '灵活的 API 查询语言，减少网络请求',
          priority: 'recommended',
        });
      } else {
        stacks.push({
          category: 'API 设计',
          name: 'RESTful API + Swagger',
          reason: '标准化 REST API + 自动文档生成',
          priority: 'must-have',
        });
      }

      // 身份认证
      stacks.push({
        category: '身份认证',
        name: 'JWT + Passport.js',
        reason: '无状态认证方案，支持多种认证策略',
        priority: 'must-have',
      });

      // 实时通信
      if (features.some(f => f.includes('实时') || f.includes('消息') || f.includes('聊天') || f.includes('推送'))) {
        stacks.push({
          category: '实时通信',
          name: 'Socket.io / WebSocket',
          reason: '双向实时通信，支持房间和广播',
          priority: 'must-have',
        });
      }

      // 任务队列
      if (features.some(f => f.includes('任务') || f.includes('定时') || f.includes('批处理'))) {
        stacks.push({
          category: '任务队列',
          name: 'Bull + Redis',
          reason: '强大的任务队列系统，支持延迟和重试',
          priority: 'recommended',
        });
      }

      // 文件存储
      if (features.some(f => f.includes('上传') || f.includes('文件') || f.includes('图片') || f.includes('视频'))) {
        stacks.push({
          category: '对象存储',
          name: 'AWS S3 / 阿里云 OSS',
          reason: '可靠的云存储服务，支持 CDN 加速',
          priority: 'recommended',
        });
      }
    }

    // === 通用开发工具 ===
    stacks.push(
      {
        category: '包管理',
        name: 'pnpm',
        version: '^8.0.0',
        reason: '快速、节省磁盘空间的包管理器',
        priority: 'recommended',
      },
      {
        category: '代码质量',
        name: 'ESLint + Prettier + Husky',
        reason: '代码检查 + 格式化 + Git Hooks，确保代码规范',
        priority: 'must-have',
      },
      {
        category: '类型检查',
        name: 'TypeScript',
        version: '^5.3.0',
        reason: '静态类型检查，提高代码可维护性',
        priority: complexity.level === 'simple' ? 'recommended' : 'must-have',
      },
      {
        category: '版本控制',
        name: 'Git + GitHub/GitLab',
        reason: '代码版本管理和团队协作平台',
        priority: 'must-have',
      }
    );

    // === 测试工具 ===
    if (complexity.level !== 'simple') {
      stacks.push(
        {
          category: '单元测试',
          name: 'Vitest + React Testing Library',
          reason: 'Vite 原生测试框架，速度快，配置简单',
          priority: 'must-have',
        },
        {
          category: 'E2E 测试',
          name: 'Playwright / Cypress',
          reason: '端到端测试框架，模拟真实用户操作',
          priority: 'recommended',
        }
      );
    }

    // === 部署和运维 ===
    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      stacks.push(
        {
          category: '容器化',
          name: 'Docker + Docker Compose',
          reason: '容器化部署，环境一致性保证',
          priority: 'must-have',
        },
        {
          category: 'CI/CD',
          name: 'GitHub Actions / GitLab CI',
          reason: '自动化构建、测试和部署',
          priority: 'must-have',
        },
        {
          category: '云服务',
          name: 'AWS / 阿里云 / 腾讯云',
          reason: '可靠的云计算基础设施',
          priority: 'must-have',
        },
        {
          category: '监控',
          name: 'Prometheus + Grafana',
          reason: '系统监控和可视化告警',
          priority: 'recommended',
        },
        {
          category: '日志',
          name: 'ELK Stack / Loki',
          reason: '集中式日志管理和分析',
          priority: 'recommended',
        }
      );
    } else {
      stacks.push(
        {
          category: '部署平台',
          name: 'Vercel / Netlify',
          reason: '前端应用一键部署，支持自动 CI/CD',
          priority: 'recommended',
        },
        {
          category: '后端部署',
          name: 'Railway / Render',
          reason: '简单易用的后端部署平台',
          priority: 'optional',
        }
      );
    }

    // === 性能优化 ===
    if (complexity.level !== 'simple') {
      stacks.push({
        category: '性能监控',
        name: 'Sentry + Google Analytics',
        reason: '错误追踪和用户行为分析',
        priority: 'recommended',
      });
    }

    return stacks;
  }

  // 生成智能开发建议
  static generateDevelopmentAdvice(requirement: ProjectRequirement): DevelopmentAdvice[] {
    const complexity = this.analyzeComplexity(requirement);
    const features = requirement.features;
    const advice: DevelopmentAdvice[] = [];

    // === 需求分析阶段 ===
    const requirementTasks = [
      '与利益相关者进行深入访谈，明确项目目标和成功标准',
      '绘制用户旅程地图和业务流程图',
      '进行竞品分析，了解行业最佳实践',
      '定义功能优先级（MoSCoW 方法）和 MVP 范围',
    ];

    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      requirementTasks.push(
        '进行技术可行性研究和 PoC（概念验证）',
        '评估技术风险和制定风险应对策略',
        '制定详细的项目章程和需求规格说明书'
      );
    }

    advice.push({
      phase: '📋 需求分析阶段',
      tasks: requirementTasks,
      estimatedTime: complexity.level === 'simple' ? '1周' : complexity.level === 'moderate' ? '1-2周' : '2-3周',
      resources: ['产品经理', '技术架构师', 'UI/UX 设计师', '业务分析师'],
    });

    // === 架构设计阶段 ===
    const architectureTasks = [
      '设计系统架构图（C4 模型：Context、Container、Component）',
      '制定技术选型方案，评估各技术栈优劣',
      '设计数据库 ER 图和数据模型',
      '定义 API 接口规范（RESTful/GraphQL）',
    ];

    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      architectureTasks.push(
        '设计微服务架构和服务边界',
        '制定缓存策略和数据一致性方案',
        '设计高可用架构（负载均衡、容错、降级）',
        '制定安全架构（认证授权、数据加密、XSS/CSRF 防护）',
        '性能优化方案（CDN、数据库索引、查询优化）'
      );
    } else {
      architectureTasks.push(
        '搭建开发环境和代码规范',
        '设计基础的安全策略（JWT 认证、输入验证）'
      );
    }

    advice.push({
      phase: '🏗️ 架构设计阶段',
      tasks: architectureTasks,
      estimatedTime: complexity.level === 'simple' ? '1周' : complexity.level === 'moderate' ? '1-2周' : '2-4周',
      resources: ['技术架构师', '高级后端工程师', 'DevOps 工程师', '安全专家'],
    });

    // === 开发实施阶段 ===
    const developmentTasks = [
      '搭建项目脚手架和基础框架',
      '配置 CI/CD 流程（代码检查、自动测试、自动部署）',
      '实施敏捷开发（2周一个 Sprint）',
      '按模块进行功能开发（前后端并行）',
      '编写单元测试（测试覆盖率 > 80%）',
      '进行代码审查（Code Review），确保代码质量',
    ];

    if (features.length > 8) {
      developmentTasks.push('采用特性分支开发模式（Git Flow）');
    }

    if (features.some(f => f.toLowerCase().includes('支付') || f.toLowerCase().includes('订单'))) {
      developmentTasks.push('集成第三方支付接口（支付宝、微信支付）');
    }

    if (features.some(f => f.toLowerCase().includes('实时') || f.toLowerCase().includes('消息'))) {
      developmentTasks.push('实现 WebSocket 实时通信功能');
    }

    developmentTasks.push(
      '编写 API 文档（Swagger/Postman）',
      '实施日志记录和错误追踪（Sentry）'
    );

    const devTime = complexity.level === 'simple' ? '4-6周' :
      complexity.level === 'moderate' ? '6-10周' :
        complexity.level === 'complex' ? '10-16周' : '16-24周';

    advice.push({
      phase: '💻 开发实施阶段',
      tasks: developmentTasks,
      estimatedTime: devTime,
      resources: [
        '前端工程师（2-3人）',
        '后端工程师（2-3人）',
        complexity.level !== 'simple' ? '全栈工程师（1人）' : null,
        'UI/UX 设计师（1人）',
      ].filter(Boolean) as string[],
    });

    // === 测试阶段 ===
    const testingTasks = [
      '单元测试（Jest/Vitest）- 覆盖核心业务逻辑',
      '集成测试 - 测试模块间交互',
      '端到端测试（E2E）- 模拟用户真实操作',
      '性能测试 - 负载测试和压力测试',
      '安全测试 - 渗透测试和漏洞扫描',
      'UI/UX 测试 - 兼容性和可用性测试',
      'Bug 修复和回归测试',
    ];

    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      testingTasks.push(
        '混沌工程测试 - 验证系统容错能力',
        'A/B 测试准备 - 灰度发布方案'
      );
    }

    advice.push({
      phase: '🧪 测试验证阶段',
      tasks: testingTasks,
      estimatedTime: complexity.level === 'simple' ? '1-2周' : complexity.level === 'moderate' ? '2-3周' : '3-4周',
      resources: ['QA 工程师（2人）', '自动化测试工程师（1人）', '安全工程师（1人）'],
    });

    // === 部署上线阶段 ===
    const deploymentTasks = [
      '准备生产环境配置和环境变量',
      '配置域名、SSL 证书和 CDN',
      '设置数据库备份和恢复策略',
      '配置监控和告警系统',
      '准备部署文档和运维手册',
    ];

    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      deploymentTasks.push(
        '容器化部署（Docker + Kubernetes）',
        '配置负载均衡和自动扩缩容',
        '实施蓝绿部署或金丝雀发布',
        '建立日志聚合和 APM 监控',
        '制定应急预案和回滚方案'
      );
    } else {
      deploymentTasks.push(
        '部署到云平台（Vercel/Netlify/Railway）',
        '配置基础监控（Uptime 监控）'
      );
    }

    advice.push({
      phase: '🚀 部署上线阶段',
      tasks: deploymentTasks,
      estimatedTime: complexity.level === 'simple' ? '3-5天' : complexity.level === 'moderate' ? '1-2周' : '2-3周',
      resources: [
        'DevOps 工程师（1-2人）',
        '运维工程师（1人）',
        complexity.level === 'enterprise' ? 'SRE 工程师（1人）' : null,
      ].filter(Boolean) as string[],
    });

    // === 运维迭代阶段 ===
    const maintenanceTasks = [
      '收集用户反馈和数据分析（Google Analytics）',
      '监控系统运行状态和性能指标',
      '及时修复线上 Bug 和安全漏洞',
      '进行性能优化和成本优化',
      '规划和开发新功能（持续迭代）',
    ];

    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      maintenanceTasks.push(
        '定期进行安全审计和合规性检查',
        '技术债务管理和代码重构',
        '容量规划和架构演进',
        '团队知识分享和技术文档维护'
      );
    }

    advice.push({
      phase: '🔄 运维迭代阶段',
      tasks: maintenanceTasks,
      estimatedTime: '持续进行（长期维护）',
      resources: ['全体技术团队', '产品经理', '数据分析师'],
    });

    return advice;
  }

  // 综合分析项目（主入口）
  static async analyzeProject(requirement: ProjectRequirement, useAI: boolean = true): Promise<AnalysisResult> {
    // 初始化 AI 配置
    this.initAIConfig();

    // 尝试使用真实 AI API（如果配置了且用户选择使用的话）
    if (this.aiConfig && useAI) {
      try {
        console.log('🤖 尝试使用 AI 增强分析...');
        console.log('📋 AI 配置:', {
          provider: this.aiConfig.provider,
          model: this.aiConfig.model,
          hasApiKey: !!this.aiConfig.apiKey,
          apiKeyPrefix: this.aiConfig.apiKey?.substring(0, 8) + '...',
        });
        return await this.analyzeWithAI(requirement);
      } catch (error: any) {
        console.error('❌ AI API 调用失败，降级到智能分析算法');
        console.error('错误详情:', {
          message: error.message,
          stack: error.stack,
          error: error,
        });
        // 降级到智能分析算法
      }
    } else if (!useAI) {
      console.log('ℹ️ 用户选择不使用 AI 增强,使用内置智能分析算法');
    } else if (!this.aiConfig) {
      console.log('⚠️ AI 未配置,使用内置智能分析算法');
    }

    // 使用智能分析算法
    console.log('💡 使用内置智能分析算法');
    return this.analyzeWithIntelligentAlgorithm(requirement);
  }

  // 使用真实 AI API 进行分析（可选功能）
  private static async analyzeWithAI(requirement: ProjectRequirement): Promise<AnalysisResult> {
    if (!this.aiConfig) {
      throw new Error('AI 配置未初始化');
    }

    const aiPrompt = this.generateAIPrompt(requirement);
    const complexity = this.analyzeComplexity(requirement);

    // 构建 AI 消息
    const messages: AIMessage[] = [
      {
        role: 'system',
        content: `你是一位资深的软件架构师和技术顾问，拥有 15 年以上的项目经验。你擅长：
1. 项目需求分析和复杂度评估
2. 技术栈选型和架构设计
3. 开发流程规划和最佳实践
4. 性能优化和安全性设计

请基于用户提供的项目需求，给出专业、详细、可落地的技术建议。`,
      },
      {
        role: 'user',
        content: `${aiPrompt.prompt}

请从以下几个方面给出详细建议（每个方面 2-3 段文字）：

1. **架构设计建议**：推荐的架构模式和理由
2. **技术栈选型**：核心技术选择和理由（前端、后端、数据库等）
3. **开发流程**：推荐的开发方法和实践
4. **关键挑战**：可能遇到的技术挑战和解决方案
5. **部署建议**：推荐的部署方案和运维策略

请用简洁专业的中文回答，每个方面用标题分隔。`,
      },
    ];

    // 调用 AI API
    const aiResponse = await AIProviderManager.callAI(this.aiConfig, messages);

    console.log(`✅ AI 分析完成 (${aiResponse.provider}):`, {
      model: aiResponse.model,
      tokens: aiResponse.usage?.totalTokens,
    });

    // 合并 AI 响应和智能算法结果
    const intelligentResult = this.analyzeWithIntelligentAlgorithm(requirement);

    return {
      aiPrompt: {
        ...intelligentResult.aiPrompt,
        suggestions: [
          ...intelligentResult.aiPrompt.suggestions,
          '',
          `🤖 **${aiResponse.provider?.toUpperCase()} AI 增强分析** (${aiResponse.model})`,
          '',
          aiResponse.content,
          '',
          `📊 **分析统计**: 使用了 ${aiResponse.usage?.totalTokens || 0} tokens`,
        ],
      },
      techStack: intelligentResult.techStack,
      developmentAdvice: intelligentResult.developmentAdvice,
      additionalNotes: [
        ...(intelligentResult.additionalNotes || []),
        '',
        `✨ 本次分析由 ${this.aiConfig.provider} (${aiResponse.model}) AI 增强`,
        `📈 项目复杂度: ${complexity.level.toUpperCase()} (${complexity.score}/12 分)`,
      ],
    };
  }

  // 使用智能分析算法
  private static analyzeWithIntelligentAlgorithm(requirement: ProjectRequirement): AnalysisResult {
    const aiPrompt = this.generateAIPrompt(requirement);
    const techStack = this.recommendTechStack(requirement);
    const developmentAdvice = this.generateDevelopmentAdvice(requirement);
    const additionalNotes = this.generateAdditionalNotes(requirement);

    return {
      aiPrompt,
      techStack,
      developmentAdvice,
      additionalNotes,
    };
  }

  // 生成额外建议
  private static generateAdditionalNotes(requirement: ProjectRequirement): string[] {
    const complexity = this.analyzeComplexity(requirement);
    const features = requirement.features.map(f => f.toLowerCase());
    const notes: string[] = [];

    // 通用建议
    notes.push(
      '✅ 建议采用敏捷开发方法（Scrum/Kanban），每 2 周一个迭代',
      '✅ 重视代码质量，实施代码审查（Code Review）制度',
      '✅ 建立完善的文档体系（技术文档、API 文档、用户手册）'
    );

    // 安全性建议
    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      notes.push(
        '🔒 安全性至关重要，实施 OWASP Top 10 防护措施',
        '🔒 使用 HTTPS、数据加密存储、定期安全审计',
        '🔒 实施 API 限流、防 DDoS 攻击、输入验证'
      );
    } else {
      notes.push('🔒 重视安全性，使用 HTTPS 和 JWT 认证');
    }

    // 性能优化建议
    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      notes.push(
        '⚡ 性能优化：使用 CDN、Redis 缓存、数据库索引优化',
        '⚡ 实施前端性能优化：代码分割、懒加载、图片优化',
        '⚡ 后端优化：连接池、异步处理、消息队列'
      );
    } else {
      notes.push('⚡ 关注性能，使用缓存和 CDN 加速');
    }

    // 监控和运维
    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      notes.push(
        '📊 建立完善的监控体系（日志、性能、错误追踪、业务指标）',
        '📊 使用 APM 工具（New Relic/Datadog）监控应用性能',
        '📊 设置告警规则，及时发现和处理问题'
      );
    } else {
      notes.push('📊 使用 Sentry 进行错误追踪和监控');
    }

    // 用户体验
    notes.push(
      '🎨 关注用户体验（UX），进行用户测试和 A/B 测试',
      '📱 确保移动端适配和响应式设计'
    );

    // 特定功能建议
    if (features.some(f => f.includes('支付') || f.includes('交易'))) {
      notes.push(
        '💳 支付功能需要特别注意安全性和幂等性设计',
        '💳 建议使用成熟的支付网关（Stripe/支付宝/微信支付）'
      );
    }

    if (features.some(f => f.includes('实时') || f.includes('消息'))) {
      notes.push('💬 实时功能建议使用 WebSocket 或 Server-Sent Events');
    }

    if (features.some(f => f.includes('搜索') || f.includes('检索'))) {
      notes.push(
        '🔍 搜索功能建议使用 Elasticsearch 或 Algolia',
        '🔍 实现搜索词联想、拼写纠正、相关性排序'
      );
    }

    if (features.some(f => f.includes('推荐') || f.includes('个性化'))) {
      notes.push(
        '🎯 推荐系统可以使用协同过滤或深度学习算法',
        '🎯 收集用户行为数据，建立用户画像'
      );
    }

    // 团队协作
    notes.push(
      '👥 建立良好的团队协作文化，定期进行技术分享',
      '👥 使用项目管理工具（Jira/Trello/Linear）跟踪进度'
    );

    // 成本优化
    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      notes.push(
        '💰 关注云服务成本，合理选择实例规格和存储方案',
        '💰 实施成本监控和预算告警'
      );
    }

    // 可扩展性
    if (complexity.level === 'enterprise' || complexity.level === 'complex') {
      notes.push(
        '🚀 设计要考虑未来扩展性，使用微服务和事件驱动架构',
        '🚀 水平扩展优于垂直扩展，设计无状态服务'
      );
    }

    // 合规性
    if (requirement.category.includes('企业') || requirement.category.includes('金融')) {
      notes.push(
        '📜 注意数据合规性（GDPR、个人信息保护法）',
        '📜 实施数据备份和灾难恢复计划'
      );
    }

    // 最后的建议
    notes.push(
      '✨ 持续学习新技术，但不要盲目追新，选择稳定成熟的技术栈',
      '✨ 从 MVP 开始，快速验证想法，然后逐步完善功能'
    );

    return notes;
  }
}
