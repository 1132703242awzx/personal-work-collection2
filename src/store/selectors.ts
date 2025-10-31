import { createSelector } from '@reduxjs/toolkit';
import { RootState } from './index';

// ============= Requirements Selectors =============
export const selectRequirements = (state: RootState) => state.requirements.data;
export const selectRequirementsStep = (state: RootState) => state.requirements.currentStep;
export const selectRequirementsValid = (state: RootState) => state.requirements.isValid;

// ============= Recommendations Selectors =============
export const selectTechStack = (state: RootState) => state.recommendations.techStack;
export const selectPrompts = (state: RootState) => state.recommendations.prompts;
export const selectSuggestions = (state: RootState) => state.recommendations.suggestions;
export const selectRecommendationsLoading = (state: RootState) => state.recommendations.loading;
export const selectRecommendationsError = (state: RootState) => state.recommendations.error;

// 组合选择器: 获取完整推荐结果
export const selectFullRecommendations = createSelector(
  [selectTechStack, selectPrompts, selectSuggestions],
  (techStack, prompts, suggestions) => ({
    techStack,
    prompts,
    suggestions,
  })
);

// 组合选择器: 按分类分组的技术栈
export const selectTechStackByCategory = createSelector(
  [selectTechStack],
  (techStack) => {
    return techStack.reduce((acc, item) => {
      if (!acc[item.category]) {
        acc[item.category] = [];
      }
      acc[item.category].push(item);
      return acc;
    }, {} as Record<string, typeof techStack>);
  }
);

// 组合选择器: 必选技术栈
export const selectMustHaveTechStack = createSelector(
  [selectTechStack],
  (techStack) => techStack.filter(item => item.priority === 'must-have')
);

// ============= UI Selectors =============
export const selectLoading = (state: RootState) => state.ui.loading;
export const selectCurrentStep = (state: RootState) => state.ui.currentStep;
export const selectTheme = (state: RootState) => state.ui.theme;
export const selectSidebarOpen = (state: RootState) => state.ui.sidebarOpen;
export const selectNotifications = (state: RootState) => state.ui.notifications;

// 组合选择器: 未读通知数量
export const selectUnreadNotificationsCount = createSelector(
  [selectNotifications],
  (notifications) => notifications.length
);

// ============= History Selectors =============
export const selectHistory = (state: RootState) => state.history.items;
export const selectHistoryLoading = (state: RootState) => state.history.loading;
export const selectHistoryError = (state: RootState) => state.history.error;

// 组合选择器: 收藏的历史记录
export const selectFavoriteHistory = createSelector(
  [selectHistory],
  (history) => history.filter(item => item.favorite)
);

// 组合选择器: 最近的历史记录
export const selectRecentHistory = createSelector(
  [selectHistory],
  (history) => history.slice(0, 10)
);

// 组合选择器: 按日期分组的历史记录
export const selectHistoryByDate = createSelector(
  [selectHistory],
  (history) => {
    const grouped: Record<string, typeof history> = {};
    
    history.forEach(item => {
      const date = new Date(item.timestamp).toLocaleDateString('zh-CN');
      if (!grouped[date]) {
        grouped[date] = [];
      }
      grouped[date].push(item);
    });

    return grouped;
  }
);

// ============= 组合 Selectors =============

// 应用是否正在加载
export const selectIsAppLoading = createSelector(
  [selectLoading, selectRecommendationsLoading, selectHistoryLoading],
  (uiLoading, recsLoading, historyLoading) => {
    return uiLoading || recsLoading || historyLoading;
  }
);

// 是否有错误
export const selectHasError = createSelector(
  [selectRecommendationsError, selectHistoryError],
  (recsError, historyError) => {
    return !!(recsError || historyError);
  }
);

// 获取所有错误消息
export const selectAllErrors = createSelector(
  [selectRecommendationsError, selectHistoryError],
  (recsError, historyError) => {
    const errors: string[] = [];
    if (recsError) errors.push(recsError);
    if (historyError) errors.push(historyError);
    return errors;
  }
);
