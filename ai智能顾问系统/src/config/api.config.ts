/**
 * API 配置文件
 * 统一管理 API 端点、超时设置、重试策略等配置
 */

export const API_CONFIG = {
  // 基础 URL（根据环境变量切换）
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
  
  // 超时设置
  TIMEOUT: 30000, // 30秒
  
  // 重试配置
  RETRY: {
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000, // 1秒
    RETRY_STATUS_CODES: [408, 429, 500, 502, 503, 504],
  },
  
  // API 端点
  ENDPOINTS: {
    // 需求分析
    ANALYZE_REQUIREMENTS: '/analyze-requirements',
    
    // 技术栈
    TECH_STACKS: '/tech-stacks',
    TECH_STACKS_TRENDING: '/tech-stacks/trending',
    TECH_STACKS_SEARCH: '/tech-stacks/search',
    
    // AI 提示词
    GENERATE_PROMPTS: '/generate-prompts',
    OPTIMIZE_PROMPTS: '/generate-prompts/optimize',
    
    // 历史记录
    HISTORY: '/history',
    HISTORY_ITEM: (id: string) => `/history/${id}`,
    HISTORY_FAVORITE: (id: string) => `/history/${id}/favorite`,
    HISTORY_EXPORT: '/history/export',
    
    // 用户相关
    USER_PROFILE: '/user/profile',
    USER_PREFERENCES: '/user/preferences',
  },
  
  // 请求头
  HEADERS: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
} as const;

// 环境检测
export const isDevelopment = import.meta.env.MODE === 'development';
export const isProduction = import.meta.env.MODE === 'production';

// Mock 模式配置（开发环境可启用）
export const MOCK_CONFIG = {
  ENABLED: import.meta.env.VITE_ENABLE_MOCK === 'true' || isDevelopment,
  DELAY: 1500, // Mock 响应延迟（毫秒）
};
