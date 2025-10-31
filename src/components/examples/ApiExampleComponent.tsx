/**
 * API 使用示例组件
 * 展示如何使用 API 服务层
 */

import { useState } from 'react';
import { useAppDispatch } from '../../store';
import { addNotification } from '../../store/slices/uiSlice';
import { API } from '../../services/api';
import { ProjectRequirements, TechStack } from '../../types';

export default function ApiExampleComponent() {
  const dispatch = useAppDispatch();
  const [loading, setLoading] = useState(false);
  const [techStacks, setTechStacks] = useState<TechStack[]>([]);

  // ==================== 需求分析示例 ====================
  const handleAnalyzeRequirements = async () => {
    setLoading(true);

    try {
      const requirements: ProjectRequirements = {
        projectType: 'Web 应用',
        complexity: 7,
        budget: '10-30万',
        features: ['用户认证', '数据可视化', '实时通信'],
        description: '企业级项目管理系统',
        targetPlatform: ['Web', 'Mobile'],
        timeline: '3个月',
        teamSize: 5,
      };

      const result = await API.recommendation.analyzeRequirements(requirements);

      console.log('分析结果:', result);

      dispatch(
        addNotification({
          type: 'success',
          message: '需求分析完成！',
        })
      );

      setTechStacks(result.techStack);
    } catch (error: any) {
      console.error('分析失败:', error);

      dispatch(
        addNotification({
          type: 'error',
          message: error.message || '需求分析失败',
        })
      );
    } finally {
      setLoading(false);
    }
  };

  // ==================== 生成 AI 提示词示例 ====================
  const handleGeneratePrompts = async () => {
    if (techStacks.length === 0) {
      dispatch(
        addNotification({
          type: 'warning',
          message: '请先分析需求获取技术栈',
        })
      );
      return;
    }

    setLoading(true);

    try {
      const result = await API.recommendation.generatePrompts(techStacks);

      console.log('生成的提示词:', result);

      dispatch(
        addNotification({
          type: 'success',
          message: `成功生成 ${result.prompts.length} 个 AI 提示词`,
        })
      );
    } catch (error: any) {
      console.error('生成提示词失败:', error);

      dispatch(
        addNotification({
          type: 'error',
          message: error.message || '生成提示词失败',
        })
      );
    } finally {
      setLoading(false);
    }
  };

  // ==================== 获取技术栈数据库示例 ====================
  const handleGetTechStacks = async () => {
    setLoading(true);
    try {
      const result = await API.techStack.getTechStacks();
      console.log('技术栈数据库:', result);
      dispatch(addNotification({ type: 'success', message: '技术栈数据加载成功' }));
    } catch (error: any) {
      console.error('获取技术栈失败:', error);
      dispatch(addNotification({ type: 'error', message: error.message || '获取技术栈失败' }));
    } finally {
      setLoading(false);
    }
  };

  // ==================== 获取趋势技术栈示例 ====================
  const handleGetTrending = async () => {
    setLoading(true);
    try {
      const result = await API.techStack.getTrendingTechStacks();
      console.log('趋势技术栈:', result);
      dispatch(addNotification({ type: 'success', message: `发现 ${result.length} 个热门技术栈` }));
    } catch (error: any) {
      console.error('获取趋势技术栈失败:', error);
      dispatch(addNotification({ type: 'error', message: error.message || '获取趋势技术栈失败' }));
    } finally {
      setLoading(false);
    }
  };

  // ==================== 搜索技术栈示例 ====================
  const handleSearchTechStacks = async () => {
    setLoading(true);
    try {
      const result = await API.techStack.searchTechStacks('React', '前端框架');
      console.log('搜索结果:', result);
      dispatch(addNotification({ type: 'success', message: `找到 ${result.length} 个匹配的技术栈` }));
    } catch (error: any) {
      console.error('搜索技术栈失败:', error);
      dispatch(addNotification({ type: 'error', message: error.message || '搜索技术栈失败' }));
    } finally {
      setLoading(false);
    }
  };

  // ==================== 保存历史记录示例 ====================
  const handleSaveHistory = async () => {
    setLoading(true);
    try {
      await API.history.saveToHistory(
        'AI 项目开发',
        {
          projectType: 'Web 应用',
          complexity: 7,
          budget: '10-30万',
          features: ['AI 集成', '数据分析'],
          description: 'AI 驱动的数据分析平台',
          targetPlatform: ['Web'],
        },
        {
          aiPrompt: {
            prompt: '示例提示词',
            context: '示例上下文',
            suggestions: ['建议1', '建议2'],
          },
          techStack: techStacks,
          developmentAdvice: [],
        }
      );
      dispatch(addNotification({ type: 'success', message: '已保存到历史记录' }));
    } catch (error: any) {
      console.error('保存历史记录失败:', error);
      dispatch(addNotification({ type: 'error', message: error.message || '保存历史记录失败' }));
    } finally {
      setLoading(false);
    }
  };

  // ==================== 获取历史记录示例 ====================
  const handleGetHistory = async () => {
    setLoading(true);
    try {
      const result = await API.history.getHistory({
        page: 1,
        pageSize: 10,
        sortBy: 'timestamp',
        order: 'desc',
      });
      console.log('历史记录:', result);
      dispatch(addNotification({ type: 'success', message: `加载了 ${result.items.length} 条历史记录` }));
    } catch (error: any) {
      console.error('获取历史记录失败:', error);
      dispatch(addNotification({ type: 'error', message: error.message || '获取历史记录失败' }));
    } finally {
      setLoading(false);
    }
  };

  // ==================== 导出历史记录示例 ====================
  const handleExportHistory = async () => {
    setLoading(true);
    try {
      const blob = await API.history.exportHistory('json');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `history_${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      dispatch(addNotification({ type: 'success', message: '历史记录已导出' }));
    } catch (error: any) {
      console.error('导出历史记录失败:', error);
      dispatch(addNotification({ type: 'error', message: error.message || '导出历史记录失败' }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 space-y-6 bg-slate-900 min-h-screen">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">API 服务使用示例</h1>

        {/* 推荐服务 */}
        <section className="bg-slate-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold text-white mb-4">📊 推荐服务</h2>
          <div className="space-y-3">
            <button
              onClick={handleAnalyzeRequirements}
              disabled={loading}
              className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              分析需求并生成推荐
            </button>
            <button
              onClick={handleGeneratePrompts}
              disabled={loading || techStacks.length === 0}
              className="w-full py-3 px-4 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              生成 AI 提示词
            </button>
          </div>
        </section>

        {/* 技术栈服务 */}
        <section className="bg-slate-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold text-white mb-4">🛠️ 技术栈服务</h2>
          <div className="space-y-3">
            <button
              onClick={handleGetTechStacks}
              disabled={loading}
              className="w-full py-3 px-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              获取技术栈数据库
            </button>
            <button
              onClick={handleGetTrending}
              disabled={loading}
              className="w-full py-3 px-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              获取趋势技术栈
            </button>
            <button
              onClick={handleSearchTechStacks}
              disabled={loading}
              className="w-full py-3 px-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              搜索技术栈（React）
            </button>
          </div>
        </section>

        {/* 历史记录服务 */}
        <section className="bg-slate-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-4">📚 历史记录服务</h2>
          <div className="space-y-3">
            <button
              onClick={handleSaveHistory}
              disabled={loading}
              className="w-full py-3 px-4 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              保存到历史记录
            </button>
            <button
              onClick={handleGetHistory}
              disabled={loading}
              className="w-full py-3 px-4 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              获取历史记录
            </button>
            <button
              onClick={handleExportHistory}
              disabled={loading}
              className="w-full py-3 px-4 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              导出历史记录
            </button>
          </div>
        </section>

        {/* 加载状态 */}
        {loading && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span className="text-gray-800 font-medium">请求处理中...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
