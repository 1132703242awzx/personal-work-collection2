import { AnalysisResult } from '../types';
import Layout from '../components/Layout';
import TechStackCard from '../components/TechStackCard';
import AIPromptDisplay from '../components/AIPromptDisplay';

interface ResultPageProps {
  result: AnalysisResult;
  onReset: () => void;
}

const ResultPage = ({ result, onReset }: ResultPageProps) => {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12 animate-fadeIn">
          <div className="inline-block p-4 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl mb-4">
            <span className="text-6xl">✨</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
            分析完成!
          </h1>
          <p className="text-slate-400 text-lg">
            为您生成了专业的开发建议和技术方案
          </p>
        </div>

        {/* Project Overview */}
        <div className="mb-8 p-8 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl animate-fadeIn animation-delay-100">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-white mb-2">
                {result.projectName}
              </h2>
              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-lg text-sm font-semibold border border-blue-500/30">
                  {result.category}
                </span>
                <span className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-lg text-sm font-semibold border border-purple-500/30">
                  复杂度: {result.complexity}
                </span>
                <span className="px-3 py-1 bg-orange-500/20 text-orange-400 rounded-lg text-sm font-semibold border border-orange-500/30">
                  预估周期: {result.estimatedTime}
                </span>
              </div>
            </div>
            
            <button
              onClick={onReset}
              className="px-6 py-3 bg-slate-700/50 backdrop-blur-sm border border-slate-600/50 rounded-xl text-slate-300 hover:bg-slate-600/50 hover:text-white transition-all duration-300 flex items-center space-x-2"
            >
              <span>←</span>
              <span>重新分析</span>
            </button>
          </div>

          <p className="text-slate-300 leading-relaxed">
            {result.description}
          </p>
        </div>

        {/* AI Prompt */}
        <div className="mb-8 animate-fadeIn animation-delay-200">
          <AIPromptDisplay
            prompt={result.aiPrompt}
            title="AI 开发提示词"
          />
        </div>

        {/* Tech Stack */}
        <div className="mb-8 animate-fadeIn animation-delay-300">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-white mb-2">
                推荐技术栈
              </h2>
              <p className="text-slate-400">
                根据项目需求精心挑选的技术方案
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {result.techStack.map((tech, index) => (
              <TechStackCard
                key={index}
                name={tech.name}
                version={tech.version}
                description={tech.reason}
                category={tech.category}
                icon={getCategoryIcon(tech.category)}
                recommended={index < 3}
                difficulty={getDifficulty(tech.name)}
              />
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="mb-8 animate-fadeIn animation-delay-400">
          <h2 className="text-3xl font-bold text-white mb-6">
            开发建议
          </h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            {result.recommendations.map((rec, index) => (
              <div
                key={index}
                className="p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl hover:bg-slate-800/50 hover:border-slate-600/50 transition-all duration-300"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-xl">
                    {index + 1}
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white mb-2">
                      {rec.title || `建议 ${index + 1}`}
                    </h3>
                    <p className="text-slate-400 leading-relaxed">
                      {rec}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-fadeIn animation-delay-500">
          <button
            onClick={() => window.print()}
            className="px-8 py-4 bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 rounded-xl text-blue-400 hover:bg-blue-500/30 hover:border-blue-500/50 transition-all duration-300 flex items-center space-x-2 font-semibold"
          >
            <span>🖨️</span>
            <span>打印报告</span>
          </button>
          
          <button
            onClick={() => {
              // 保存到历史记录的逻辑
              alert('已保存到历史记录!');
            }}
            className="px-8 py-4 bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 rounded-xl text-purple-400 hover:bg-purple-500/30 hover:border-purple-500/50 transition-all duration-300 flex items-center space-x-2 font-semibold"
          >
            <span>💾</span>
            <span>保存到历史</span>
          </button>
        </div>
      </div>
    </Layout>
  );
};

// Helper functions
const getCategoryIcon = (category: string): string => {
  const icons: Record<string, string> = {
    '前端框架': '⚛️',
    '后端框架': '🔧',
    '数据库': '🗄️',
    '工具': '🛠️',
    '部署': '🚀',
    '测试': '🧪',
  };
  return icons[category] || '📦';
};

const getDifficulty = (techName: string): 'easy' | 'medium' | 'hard' => {
  const easy = ['HTML', 'CSS', 'JavaScript', 'Express.js'];
  const hard = ['Kubernetes', 'Docker', 'GraphQL', 'TypeScript'];
  
  if (easy.some(t => techName.includes(t))) return 'easy';
  if (hard.some(t => techName.includes(t))) return 'hard';
  return 'medium';
};

export default ResultPage;
