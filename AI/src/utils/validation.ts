import { ProjectRequirements } from '../types';

export interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

export const validateStep = (
  step: number,
  data: Partial<ProjectRequirements>
): ValidationResult => {
  const errors: Record<string, string> = {};

  switch (step) {
    case 1: // 项目类型
      if (!data.projectType) {
        errors.projectType = '请选择项目类型';
      }
      if (!data.targetPlatform || data.targetPlatform.length === 0) {
        errors.targetPlatform = '请至少选择一个目标平台';
      }
      break;

    case 2: // 复杂度和预算
      if (data.complexity === undefined || data.complexity < 1 || data.complexity > 5) {
        errors.complexity = '请选择项目复杂度';
      }
      if (!data.budget) {
        errors.budget = '请选择预算范围';
      }
      if (data.teamSize !== undefined && (data.teamSize < 1 || data.teamSize > 100)) {
        errors.teamSize = '团队规模应在 1-100 人之间';
      }
      break;

    case 3: // 功能需求
      if (!data.features || data.features.length === 0) {
        errors.features = '请至少添加一个功能需求';
      }
      if (!data.description || data.description.trim().length < 20) {
        errors.description = '项目描述至少需要 20 个字符';
      }
      break;

    case 4: // 确认信息
      // 所有字段的最终验证
      if (!data.projectType) errors.projectType = '缺少项目类型';
      if (!data.targetPlatform?.length) errors.targetPlatform = '缺少目标平台';
      if (!data.complexity) errors.complexity = '缺少复杂度评估';
      if (!data.budget) errors.budget = '缺少预算信息';
      if (!data.features?.length) errors.features = '缺少功能需求';
      if (!data.description) errors.description = '缺少项目描述';
      break;
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

export const getComplexityLabel = (complexity: number): string => {
  const labels: Record<number, string> = {
    1: '非常简单',
    2: '简单',
    3: '中等',
    4: '复杂',
    5: '非常复杂',
  };
  return labels[complexity] || '未知';
};

export const getComplexityDescription = (complexity: number): string => {
  const descriptions: Record<number, string> = {
    1: '基础功能，快速开发，适合 MVP 或原型',
    2: '标准功能，常规开发周期',
    3: '多个模块，需要协调开发',
    4: '复杂业务逻辑，需要专业团队',
    5: '大型系统，需要架构设计和长期维护',
  };
  return descriptions[complexity] || '';
};

export const getBudgetLabel = (budget: string): string => {
  const labels: Record<string, string> = {
    low: '< 10万',
    medium: '10-50万',
    high: '50-200万',
    enterprise: '> 200万',
  };
  return labels[budget] || budget;
};
