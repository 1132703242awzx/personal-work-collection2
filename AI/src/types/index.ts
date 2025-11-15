// 项目需求接口
export interface ProjectRequirement {
  projectName: string;
  description: string;
  category: string;
  targetPlatform: string[];
  features: string[];
  userStory?: string;
  technicalConstraints?: string;
}

// 智能需求输入接口
export interface ProjectRequirements {
  projectType: string;
  complexity: number;
  budget: string;
  features: string[];
  description: string;
  targetPlatform: string[];
  timeline?: string;
  teamSize?: number;
}

// 表单草稿
export interface FormDraft {
  step: number;
  currentStep: number; // 添加当前步骤字段
  data: Partial<ProjectRequirements>;
  timestamp: number;
}

// AI 提示词响应
export interface AIPrompt {
  prompt: string;
  context: string;
  suggestions: string[];
}

// 技术栈推荐
export interface TechStack {
  category: string;
  name: string;
  version?: string;
  reason: string;
  priority: 'must-have' | 'recommended' | 'optional';
}

// 开发建议
export interface DevelopmentAdvice {
  phase: string;
  tasks: string[];
  estimatedTime?: string;
  resources?: string[];
}

// 完整分析结果
export interface AnalysisResult {
  aiPrompt: AIPrompt;
  techStack: TechStack[];
  developmentAdvice: DevelopmentAdvice[];
  additionalNotes?: string[];
}

// 搜索历史
export interface SearchHistory {
  id: string;
  requirements: ProjectRequirements;
  result: AnalysisResult;
  timestamp: number;
  favorite?: boolean;
}

// Redux 状态类型
export interface AppState {
  requirements: RequirementsState;
  recommendations: RecommendationsState;
  ui: UIState;
  history: HistoryState;
}

export interface RequirementsState {
  data: Partial<ProjectRequirements>;
  currentStep: number;
  isValid: boolean;
}

export interface RecommendationsState {
  techStack: TechStack[];
  prompts: AIPrompt | null;
  suggestions: DevelopmentAdvice[];
  loading: boolean;
  error: string | null;
}

export interface UIState {
  loading: boolean;
  currentStep: number;
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  notifications: Notification[];
}

export interface HistoryState {
  items: SearchHistory[];
  loading: boolean;
  error: string | null;
}

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  timestamp: number;
}

// API 响应类型
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  timestamp: number;
}

export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
  timestamp: number;
}

// API 请求类型
export interface AnalyzeRequirementsRequest {
  requirements: ProjectRequirements;
}

export interface AnalyzeRequirementsResponse {
  techStack: TechStack[];
  prompts: AIPrompt;
  suggestions: DevelopmentAdvice[];
  estimatedCost?: string;
  estimatedDuration?: string;
}

export interface GeneratePromptsRequest {
  techStack: TechStack[];
  requirements?: Partial<ProjectRequirements>;
}

export interface GeneratePromptsResponse {
  prompts: AIPrompt[];
  optimizationSuggestions: string[];
}

export interface SaveHistoryRequest {
  query: string;
  requirements: ProjectRequirements;
  results: AnalysisResult;
}

export interface TechStackDatabaseResponse {
  categories: {
    [key: string]: TechStack[];
  };
  trending: TechStack[];
  lastUpdated: string;
}
