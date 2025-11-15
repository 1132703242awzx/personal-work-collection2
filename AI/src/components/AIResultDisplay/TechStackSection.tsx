import { useState } from 'react';
import { TechStack } from '../../types';

interface TechStackSectionProps {
  techStacks: TechStack[];
  onCompare?: (stacks: TechStack[]) => void;
}

const TechStackSection = ({ techStacks, onCompare }: TechStackSectionProps) => {
  const [selectedStacks, setSelectedStacks] = useState<string[]>([]);
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);

  // 按分类分组
  const groupedStacks = techStacks.reduce((acc, stack) => {
    if (!acc[stack.category]) {
      acc[stack.category] = [];
    }
    acc[stack.category].push(stack);
    return acc;
  }, {} as Record<string, TechStack[]>);

  const categoryIcons: Record<string, string> = {
    '前端框架': '⚛️',
    '后端技术': '🔧',
    '数据库': '🗄️',
    '部署方案': '☁️',
    'UI框架': '🎨',
    '状态管理': '📦',
    'API': '🔌',
    '测试': '🧪',
    '构建工具': '⚙️',
  };

  const priorityColors = {
    'must-have': 'from-red-500 to-orange-500',
    'recommended': 'from-blue-500 to-cyan-500',
    'optional': 'from-slate-500 to-slate-600',
  };

  const priorityLabels = {
    'must-have': '必选',
    'recommended': '推荐',
    'optional': '可选',
  };

  const handleSelectStack = (stackName: string) => {
    setSelectedStacks(prev => 
      prev.includes(stackName)
        ? prev.filter(s => s !== stackName)
        : [...prev, stackName]
    );
  };

  const handleCompare = () => {
    const stacksToCompare = techStacks.filter(s => selectedStacks.includes(s.name));
    onCompare?.(stacksToCompare);
  };

  return (
    <div className="space-y-6">
      {/* 标题和操作栏 */}
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold text-white flex items-center space-x-2">
          <span>🚀</span>
          <span>技术栈推荐</span>
        </h3>
        {selectedStacks.length > 1 && (
          <button
            onClick={handleCompare}
            className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-semibold hover:from-purple-600 hover:to-pink-600 transition-all duration-300 flex items-center space-x-2 shadow-lg shadow-purple-500/30"
          >
            <span>📊</span>
            <span>对比选中项 ({selectedStacks.length})</span>
          </button>
        )}
      </div>

      {/* 技术栈分类展示 */}
      <div className="space-y-4">
        {Object.entries(groupedStacks).map(([category, stacks]) => (
          <div
            key={category}
            className="bg-slate-800/30 border border-slate-700/50 rounded-xl overflow-hidden hover:bg-slate-800/50 transition-all duration-300"
          >
            {/* 分类标题 */}
            <button
              onClick={() => setExpandedCategory(expandedCategory === category ? null : category)}
              className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-800/30 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{categoryIcons[category] || '📌'}</span>
                <h4 className="text-lg font-bold text-white">{category}</h4>
                <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded-full">
                  {stacks.length} 项
                </span>
              </div>
              <svg
                className={`w-5 h-5 text-slate-400 transition-transform duration-300 ${
                  expandedCategory === category ? 'rotate-180' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {/* 展开的技术栈列表 */}
            {expandedCategory === category && (
              <div className="px-6 pb-6 space-y-3 animate-fadeIn">
                {stacks.map((stack, index) => (
                  <div
                    key={index}
                    className="relative p-4 bg-slate-900/50 rounded-lg border border-slate-700/30 hover:border-blue-500/30 transition-all duration-300 group"
                  >
                    {/* 选择框 */}
                    <div className="absolute top-4 right-4">
                      <input
                        type="checkbox"
                        checked={selectedStacks.includes(stack.name)}
                        onChange={() => handleSelectStack(stack.name)}
                        className="w-5 h-5 rounded border-slate-600 text-blue-500 focus:ring-blue-500 focus:ring-offset-slate-900 cursor-pointer"
                      />
                    </div>

                    {/* 技术栈信息 */}
                    <div className="pr-12">
                      <div className="flex items-center space-x-3 mb-2">
                        <h5 className="text-lg font-bold text-white">{stack.name}</h5>
                        {stack.version && (
                          <span className="px-2 py-1 bg-slate-700/50 text-slate-400 text-xs rounded">
                            v{stack.version}
                          </span>
                        )}
                        <span
                          className={`px-2 py-1 bg-gradient-to-r ${priorityColors[stack.priority]} text-white text-xs rounded-full font-semibold`}
                        >
                          {priorityLabels[stack.priority]}
                        </span>
                      </div>
                      
                      <p className="text-slate-400 text-sm leading-relaxed">{stack.reason}</p>

                      {/* 悬停显示更多信息 */}
                      <div className="mt-3 pt-3 border-t border-slate-700/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <div className="flex items-center space-x-4 text-xs text-slate-500">
                          <span className="flex items-center space-x-1">
                            <span>⭐</span>
                            <span>推荐指数: {stack.priority === 'must-have' ? '★★★★★' : stack.priority === 'recommended' ? '★★★★☆' : '★★★☆☆'}</span>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* 统计信息 */}
      <div className="grid grid-cols-3 gap-4">
        {(['must-have', 'recommended', 'optional'] as const).map(priority => {
          const count = techStacks.filter(s => s.priority === priority).length;
          return (
            <div
              key={priority}
              className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-xl text-center"
            >
              <div className={`text-2xl font-bold bg-gradient-to-r ${priorityColors[priority]} bg-clip-text text-transparent mb-1`}>
                {count}
              </div>
              <div className="text-sm text-slate-400">{priorityLabels[priority]}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TechStackSection;
