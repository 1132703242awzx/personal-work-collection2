import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../store';
import {
  updateRequirements,
  resetRequirements,
  nextStep,
  previousStep,
} from '../../store/slices/requirementsSlice';
import {
  fetchRecommendations,
  clearRecommendations,
} from '../../store/slices/recommendationsSlice';
import { addNotification } from '../../store/slices/uiSlice';
import { addHistoryItem } from '../../store/slices/historySlice';
import {
  selectRequirements,
  selectRequirementsStep,
  selectFullRecommendations,
  selectRecommendationsLoading,
  selectTechStackByCategory,
} from '../../store/selectors';
import { ProjectRequirements } from '../../types';

/**
 * Redux 集成示例组件
 * 展示如何在组件中使用 Redux Toolkit
 */
const ReduxExampleComponent = () => {
  const dispatch = useAppDispatch();

  // ========== 使用 Selectors 获取状态 ==========
  const requirements = useAppSelector(selectRequirements);
  const currentStep = useAppSelector(selectRequirementsStep);
  const recommendations = useAppSelector(selectFullRecommendations);
  const isLoading = useAppSelector(selectRecommendationsLoading);
  const techStackByCategory = useAppSelector(selectTechStackByCategory);

  // ========== 事件处理函数 ==========

  // 更新需求
  const handleUpdateRequirements = (data: Partial<ProjectRequirements>) => {
    dispatch(updateRequirements(data));
  };

  // 提交分析
  const handleSubmitAnalysis = async () => {
    if (!requirements.projectType || !requirements.description) {
      dispatch(addNotification({
        type: 'error',
        message: '请填写完整的项目信息',
      }));
      return;
    }

    try {
      // 发起异步请求
      const result = await dispatch(fetchRecommendations(requirements as ProjectRequirements)).unwrap();

      // 成功后添加到历史记录
      await dispatch(addHistoryItem({
        requirements: requirements as ProjectRequirements,
        result,
      })).unwrap();

      // 显示成功通知
      dispatch(addNotification({
        type: 'success',
        message: '分析完成！',
      }));
    } catch (error) {
      // 错误处理
      dispatch(addNotification({
        type: 'error',
        message: `分析失败: ${error}`,
      }));
    }
  };

  // 重置表单
  const handleReset = () => {
    dispatch(resetRequirements());
    dispatch(clearRecommendations());
    dispatch(addNotification({
      type: 'info',
      message: '已重置表单',
    }));
  };

  // 下一步
  const handleNext = () => {
    dispatch(nextStep());
  };

  // 上一步
  const handlePrevious = () => {
    dispatch(previousStep());
  };

  // ========== 副作用 ==========
  useEffect(() => {
    // 组件挂载时的初始化逻辑
    console.log('Redux Example Component Mounted');

    return () => {
      // 清理逻辑
      console.log('Redux Example Component Unmounted');
    };
  }, []);

  // 监听需求变化
  useEffect(() => {
    console.log('需求已更新:', requirements);
  }, [requirements]);

  // ========== 渲染 ==========
  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-bold text-white">Redux 集成示例</h1>

      {/* 当前状态 */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <h2 className="text-xl font-bold text-white mb-4">当前状态</h2>
        <div className="space-y-2 text-slate-300">
          <p>当前步骤: {currentStep}/4</p>
          <p>项目类型: {requirements.projectType || '未选择'}</p>
          <p>复杂度: {requirements.complexity || 3}</p>
          <p>预算: {requirements.budget || 'medium'}</p>
          <p>功能数量: {requirements.features?.length || 0}</p>
        </div>
      </div>

      {/* 操作按钮 */}
      <div className="flex flex-wrap gap-4">
        <button
          onClick={() => handleUpdateRequirements({ projectType: 'web' })}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          设置项目类型为 Web
        </button>
        <button
          onClick={handlePrevious}
          disabled={currentStep === 1}
          className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 disabled:opacity-50"
        >
          上一步
        </button>
        <button
          onClick={handleNext}
          disabled={currentStep === 4}
          className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 disabled:opacity-50"
        >
          下一步
        </button>
        <button
          onClick={handleSubmitAnalysis}
          disabled={isLoading}
          className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50"
        >
          {isLoading ? '分析中...' : '提交分析'}
        </button>
        <button
          onClick={handleReset}
          className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
        >
          重置
        </button>
      </div>

      {/* 推荐结果 */}
      {recommendations.techStack.length > 0 && (
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4">推荐结果</h2>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-slate-300 mb-2">技术栈分类</h3>
              {Object.entries(techStackByCategory).map(([category, stacks]) => (
                <div key={category} className="mb-2">
                  <span className="text-blue-400">{category}:</span>{' '}
                  <span className="text-slate-400">{stacks.length} 项</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReduxExampleComponent;
