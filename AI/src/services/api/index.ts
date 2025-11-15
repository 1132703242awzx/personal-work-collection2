/**
 * API 服务统一导出
 * 提供所有 API 服务的访问入口
 */

export { default as apiClient } from './axios.instance';
import recommendationService from './recommendation.service';
import techStackService from './techstack.service';
import historyService from './history.service';

export { default as RecommendationService } from './recommendation.service';
export { default as TechStackService } from './techstack.service';
export { default as HistoryService } from './history.service';

// 统一的 API 服务对象
export const API = {
  recommendation: recommendationService,
  techStack: techStackService,
  history: historyService,
};

export default API;
