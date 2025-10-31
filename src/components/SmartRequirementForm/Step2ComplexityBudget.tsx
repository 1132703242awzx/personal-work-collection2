import { useState } from 'react';
import { ProjectRequirements } from '../../types';
import { getComplexityLabel, getComplexityDescription, getBudgetLabel } from '../../utils/validation';

interface Step2Props {
  data: Partial<ProjectRequirements>;
  errors: Record<string, string>;
  onChange: (data: Partial<ProjectRequirements>) => void;
}

const Step2ComplexityBudget = ({ data, errors, onChange }: Step2Props) => {
  const [isDragging, setIsDragging] = useState(false);

  const budgetOptions = [
    { id: 'low', label: '< 10万', description: '小型项目', icon: '💰', color: 'from-green-500 to-emerald-500' },
    { id: 'medium', label: '10-50万', description: '中型项目', icon: '💵', color: 'from-blue-500 to-cyan-500' },
    { id: 'high', label: '50-200万', description: '大型项目', icon: '💎', color: 'from-purple-500 to-pink-500' },
    { id: 'enterprise', label: '> 200万', description: '企业级项目', icon: '👑', color: 'from-orange-500 to-red-500' },
  ];

  const timelineOptions = [
    { id: '1month', label: '1 个月内', icon: '⚡' },
    { id: '3months', label: '1-3 个月', icon: '📅' },
    { id: '6months', label: '3-6 个月', icon: '📆' },
    { id: '1year', label: '6-12 个月', icon: '🗓️' },
    { id: 'long', label: '超过 1 年', icon: '⏳' },
  ];

  const handleComplexityChange = (value: number) => {
    onChange({ ...data, complexity: value });
  };

  const handleBudgetChange = (budget: string) => {
    onChange({ ...data, budget });
  };

  const handleTimelineChange = (timeline: string) => {
    onChange({ ...data, timeline });
  };

  const handleTeamSizeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value) || 0;
    onChange({ ...data, teamSize: value });
  };

  const complexity = data.complexity || 3;

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* 复杂度评估滑块 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">项目复杂度评估</h3>
        <p className="text-slate-400 mb-6">评估项目的技术复杂程度</p>

        <div className="p-8 bg-slate-800/30 border border-slate-700/50 rounded-xl">
          {/* 复杂度显示 */}
          <div className="text-center mb-8">
            <div className="inline-block p-6 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl mb-4">
              <span className="text-6xl">
                {['🌱', '🌿', '🌳', '🏔️', '🚀'][complexity - 1]}
              </span>
            </div>
            <h4 className="text-3xl font-bold text-white mb-2">
              {getComplexityLabel(complexity)}
            </h4>
            <p className="text-slate-400">
              {getComplexityDescription(complexity)}
            </p>
          </div>

          {/* 滑块 */}
          <div className="relative">
            <input
              type="range"
              min="1"
              max="5"
              step="1"
              value={complexity}
              onChange={(e) => handleComplexityChange(parseInt(e.target.value))}
              onMouseDown={() => setIsDragging(true)}
              onMouseUp={() => setIsDragging(false)}
              onTouchStart={() => setIsDragging(true)}
              onTouchEnd={() => setIsDragging(false)}
              className="w-full h-3 bg-slate-700 rounded-full appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, 
                  rgb(59, 130, 246) 0%, 
                  rgb(147, 51, 234) ${((complexity - 1) / 4) * 100}%, 
                  rgb(51, 65, 85) ${((complexity - 1) / 4) * 100}%)`,
              }}
            />
            
            {/* 刻度标签 */}
            <div className="flex justify-between mt-4 px-1">
              {[1, 2, 3, 4, 5].map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => handleComplexityChange(level)}
                  className={`text-xs font-medium transition-colors ${
                    complexity >= level ? 'text-blue-400' : 'text-slate-600'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>
        </div>

        {errors.complexity && (
          <p className="mt-2 text-sm text-red-400 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{errors.complexity}</span>
          </p>
        )}
      </div>

      {/* 预算范围 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">预算范围</h3>
        <p className="text-slate-400 mb-6">选择项目的大致预算区间</p>

        <div className="grid md:grid-cols-2 gap-4">
          {budgetOptions.map(option => (
            <button
              key={option.id}
              type="button"
              onClick={() => handleBudgetChange(option.id)}
              className={`p-6 rounded-xl text-left transition-all duration-300 ${
                data.budget === option.id
                  ? 'bg-gradient-to-br from-blue-500/20 to-purple-500/20 border-2 border-blue-500 shadow-lg shadow-blue-500/20 scale-105'
                  : 'bg-slate-800/30 border-2 border-slate-700/50 hover:bg-slate-800/50 hover:border-slate-600/50'
              }`}
            >
              <div className="flex items-start space-x-4">
                <div className={`w-16 h-16 bg-gradient-to-br ${option.color} rounded-xl flex items-center justify-center text-3xl`}>
                  {option.icon}
                </div>
                <div className="flex-1">
                  <h4 className="text-xl font-bold text-white mb-1">
                    {option.label}
                  </h4>
                  <p className="text-sm text-slate-400">{option.description}</p>
                </div>
                {data.budget === option.id && (
                  <div className="text-blue-400">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>

        {errors.budget && (
          <p className="mt-2 text-sm text-red-400 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{errors.budget}</span>
          </p>
        )}
      </div>

      {/* 开发周期 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">预期开发周期</h3>
        <p className="text-slate-400 mb-6">项目预计需要多长时间完成</p>

        <div className="flex flex-wrap gap-3">
          {timelineOptions.map(option => (
            <button
              key={option.id}
              type="button"
              onClick={() => handleTimelineChange(option.id)}
              className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
                data.timeline === option.id
                  ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                  : 'bg-slate-800/50 text-slate-400 border border-slate-700/50 hover:border-slate-600/50'
              }`}
            >
              <span className="mr-2">{option.icon}</span>
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* 团队规模 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">团队规模（可选）</h3>
        <p className="text-slate-400 mb-6">预计参与项目的开发人员数量</p>

        <div className="max-w-md">
          <input
            type="number"
            min="1"
            max="100"
            value={data.teamSize || ''}
            onChange={handleTeamSizeChange}
            placeholder="例如：5"
            className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 transition-all duration-300"
          />
          {data.teamSize && (
            <p className="mt-2 text-sm text-slate-400">
              👥 {data.teamSize} 人团队
            </p>
          )}
        </div>

        {errors.teamSize && (
          <p className="mt-2 text-sm text-red-400 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{errors.teamSize}</span>
          </p>
        )}
      </div>

      {/* 评估总结 */}
      {data.complexity && data.budget && (
        <div className="p-6 bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl animate-fadeIn">
          <h4 className="text-lg font-bold text-blue-400 mb-3 flex items-center space-x-2">
            <span>📊</span>
            <span>项目评估概览</span>
          </h4>
          <div className="grid md:grid-cols-2 gap-4 text-slate-300">
            <div>
              <span className="text-slate-500">复杂度：</span>
              <span className="font-semibold">{getComplexityLabel(data.complexity)}</span>
            </div>
            <div>
              <span className="text-slate-500">预算范围：</span>
              <span className="font-semibold">{getBudgetLabel(data.budget)}</span>
            </div>
            {data.timeline && (
              <div>
                <span className="text-slate-500">开发周期：</span>
                <span className="font-semibold">
                  {timelineOptions.find(t => t.id === data.timeline)?.label}
                </span>
              </div>
            )}
            {data.teamSize && (
              <div>
                <span className="text-slate-500">团队规模：</span>
                <span className="font-semibold">{data.teamSize} 人</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Step2ComplexityBudget;
