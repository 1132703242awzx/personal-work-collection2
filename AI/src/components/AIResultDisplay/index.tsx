import { useState } from 'react';
import { AnalysisResult, TechStack } from '../../types';
import TechStackSection from './TechStackSection';
import AIPromptSection from './AIPromptSection';
import DevelopmentAdviceSection from './DevelopmentAdviceSection';

interface AIResultDisplayProps {
  result: AnalysisResult;
  onReset?: () => void;
}

const AIResultDisplay = ({ result, onReset }: AIResultDisplayProps) => {
  const [activeTab, setActiveTab] = useState<'techstack' | 'prompt' | 'advice'>('techstack');
  const [rating, setRating] = useState<number>(0);
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackText, setFeedbackText] = useState('');
  const [compareMode, setCompareMode] = useState(false);
  const [compareStacks, setCompareStacks] = useState<TechStack[]>([]);

  const tabs = [
    { id: 'techstack' as const, label: '技术栈推荐', icon: '🚀', count: result.techStack.length },
    { id: 'prompt' as const, label: 'AI 提示词', icon: '🤖', count: 3 },
    { id: 'advice' as const, label: '开发建议', icon: '📚', count: result.developmentAdvice.length },
  ];

  const handleExportJSON = () => {
    const dataStr = JSON.stringify(result, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ai-analysis-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleExportPDF = () => {
    // 这里实际应用中可以使用 jsPDF 或类似库
    alert('PDF 导出功能开发中...\n建议先导出 JSON 格式');
  };

  const handleRatingClick = (value: number) => {
    setRating(value);
    setShowFeedback(true);
  };

  const handleSubmitFeedback = () => {
    console.log('反馈评分:', rating);
    console.log('反馈内容:', feedbackText);
    alert('感谢您的反馈！🎉');
    setShowFeedback(false);
    setFeedbackText('');
  };

  const handleCompare = (stacks: TechStack[]) => {
    setCompareStacks(stacks);
    setCompareMode(true);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* 顶部操作栏 */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 animate-fadeIn">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-2">
              AI 分析结果
            </h2>
            <p className="text-slate-400">
              基于您的需求，我们为您生成了以下专业建议
            </p>
          </div>
          
          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleExportJSON}
              className="px-4 py-2 bg-slate-700 text-white rounded-lg font-semibold hover:bg-slate-600 transition-all duration-300 flex items-center space-x-2"
            >
              <span>📄</span>
              <span>导出 JSON</span>
            </button>
            <button
              onClick={handleExportPDF}
              className="px-4 py-2 bg-slate-700 text-white rounded-lg font-semibold hover:bg-slate-600 transition-all duration-300 flex items-center space-x-2"
            >
              <span>📑</span>
              <span>导出 PDF</span>
            </button>
            {onReset && (
              <button
                onClick={onReset}
                className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 flex items-center space-x-2 shadow-lg shadow-blue-500/30"
              >
                <span>🔄</span>
                <span>新建分析</span>
              </button>
            )}
          </div>
        </div>

        {/* Tab 导航 */}
        <div className="bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl p-2 animate-fadeIn animation-delay-200">
          <div className="flex space-x-2">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all duration-300 flex items-center justify-center space-x-2 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg shadow-blue-500/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
                }`}
              >
                <span className="text-xl">{tab.icon}</span>
                <span>{tab.label}</span>
                <span className={`px-2 py-0.5 rounded-full text-xs ${
                  activeTab === tab.id
                    ? 'bg-white/20'
                    : 'bg-slate-700/50'
                }`}>
                  {tab.count}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* 主要内容区域 */}
        <div className="bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 shadow-2xl animate-fadeIn animation-delay-400">
          {activeTab === 'techstack' && (
            <TechStackSection 
              techStacks={result.techStack}
              onCompare={handleCompare}
            />
          )}
          {activeTab === 'prompt' && (
            <AIPromptSection prompt={result.aiPrompt} />
          )}
          {activeTab === 'advice' && (
            <DevelopmentAdviceSection advice={result.developmentAdvice} />
          )}
        </div>

        {/* 技术栈对比弹窗 */}
        {compareMode && compareStacks.length > 0 && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
            <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bold text-white">技术栈对比</h3>
                <button
                  onClick={() => setCompareMode(false)}
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="grid md:grid-cols-2 gap-6">
                {compareStacks.map((stack, index) => (
                  <div
                    key={index}
                    className="p-6 bg-slate-900/50 border border-slate-700 rounded-xl"
                  >
                    <h4 className="text-xl font-bold text-white mb-2">{stack.name}</h4>
                    {stack.version && (
                      <p className="text-slate-400 text-sm mb-3">版本: {stack.version}</p>
                    )}
                    <p className="text-slate-300 mb-4">{stack.reason}</p>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-400">分类: {stack.category}</span>
                      <span className={`px-3 py-1 rounded-full text-white text-xs font-semibold ${
                        stack.priority === 'must-have' ? 'bg-red-500' :
                        stack.priority === 'recommended' ? 'bg-blue-500' :
                        'bg-slate-600'
                      }`}>
                        {stack.priority === 'must-have' ? '必选' :
                         stack.priority === 'recommended' ? '推荐' : '可选'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* 附加说明 */}
        {result.additionalNotes && result.additionalNotes.length > 0 && (
          <div className="bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 rounded-xl p-6 animate-fadeIn animation-delay-600">
            <h3 className="text-xl font-bold text-orange-400 mb-4 flex items-center space-x-2">
              <span>⚠️</span>
              <span>重要提示</span>
            </h3>
            <ul className="space-y-2">
              {result.additionalNotes.map((note, index) => (
                <li key={index} className="flex items-start space-x-3 text-slate-300">
                  <span className="text-orange-400 mt-1">•</span>
                  <span>{note}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 反馈评分系统 */}
        <div className="bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 animate-fadeIn animation-delay-800">
          <h3 className="text-xl font-bold text-white mb-4 text-center">
            这个分析结果对您有帮助吗？
          </h3>
          
          {!showFeedback ? (
            <div className="flex justify-center space-x-3">
              {[1, 2, 3, 4, 5].map(value => (
                <button
                  key={value}
                  onClick={() => handleRatingClick(value)}
                  className={`w-12 h-12 rounded-lg transition-all duration-300 ${
                    rating >= value
                      ? 'bg-gradient-to-br from-yellow-400 to-orange-500 text-white scale-110'
                      : 'bg-slate-700 text-slate-400 hover:bg-slate-600 hover:scale-105'
                  }`}
                >
                  ⭐
                </button>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              <div className="text-center">
                <div className="flex justify-center space-x-1 mb-4">
                  {[1, 2, 3, 4, 5].map(value => (
                    <span
                      key={value}
                      className={`text-2xl ${rating >= value ? 'text-yellow-400' : 'text-slate-600'}`}
                    >
                      ⭐
                    </span>
                  ))}
                </div>
                <p className="text-slate-400 mb-4">感谢您的评分！请告诉我们更多想法</p>
              </div>
              
              <textarea
                value={feedbackText}
                onChange={(e) => setFeedbackText(e.target.value)}
                placeholder="您的宝贵意见将帮助我们改进..."
                className="w-full px-4 py-3 bg-slate-900/50 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"
                rows={4}
              />
              
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowFeedback(false)}
                  className="px-6 py-2 text-slate-400 hover:text-white transition-colors"
                >
                  取消
                </button>
                <button
                  onClick={handleSubmitFeedback}
                  className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 shadow-lg shadow-blue-500/30"
                >
                  提交反馈
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIResultDisplay;
