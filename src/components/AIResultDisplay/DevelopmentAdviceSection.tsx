import { useState } from 'react';
import { DevelopmentAdvice } from '../../types';

interface DevelopmentAdviceSectionProps {
  advice: DevelopmentAdvice[];
}

const DevelopmentAdviceSection = ({ advice }: DevelopmentAdviceSectionProps) => {
  const [expandedPhase, setExpandedPhase] = useState<string | null>(advice[0]?.phase || null);
  const [selectedPhases, setSelectedPhases] = useState<string[]>([]);

  const phaseIcons: Record<string, string> = {
    '需求分析': '📋',
    '系统设计': '🎨',
    '开发阶段': '💻',
    '测试阶段': '🧪',
    '部署上线': '🚀',
    '维护优化': '🔧',
  };

  const phaseColors: Record<string, string> = {
    '需求分析': 'from-blue-500 to-cyan-500',
    '系统设计': 'from-purple-500 to-pink-500',
    '开发阶段': 'from-green-500 to-emerald-500',
    '测试阶段': 'from-yellow-500 to-orange-500',
    '部署上线': 'from-red-500 to-pink-500',
    '维护优化': 'from-indigo-500 to-purple-500',
  };

  const handlePhaseToggle = (phase: string) => {
    setSelectedPhases(prev =>
      prev.includes(phase)
        ? prev.filter(p => p !== phase)
        : [...prev, phase]
    );
  };

  const handleExportSelected = () => {
    const selectedAdvice = advice.filter(a => selectedPhases.includes(a.phase));
    const content = selectedAdvice.map(a => `
# ${a.phase}
${a.estimatedTime ? `预计时间: ${a.estimatedTime}` : ''}

## 任务清单
${a.tasks.map((task, i) => `${i + 1}. ${task}`).join('\n')}

${a.resources?.length ? `## 所需资源\n${a.resources.map(r => `- ${r}`).join('\n')}` : ''}
    `).join('\n\n---\n\n');

    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'development-plan.md';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* 标题和操作栏 */}
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold text-white flex items-center space-x-2">
          <span>📚</span>
          <span>开发建议</span>
        </h3>
        {selectedPhases.length > 0 && (
          <button
            onClick={handleExportSelected}
            className="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg font-semibold hover:from-green-600 hover:to-emerald-600 transition-all duration-300 flex items-center space-x-2 shadow-lg shadow-green-500/30"
          >
            <span>📥</span>
            <span>导出选中 ({selectedPhases.length})</span>
          </button>
        )}
      </div>

      {/* 时间线概览 */}
      <div className="relative">
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-500 via-purple-500 to-pink-500"></div>
        
        <div className="space-y-6">
          {advice.map((phase, index) => (
            <div
              key={index}
              className="relative pl-16 animate-fadeIn"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* 时间线节点 */}
              <div className={`absolute left-0 w-12 h-12 rounded-full bg-gradient-to-br ${phaseColors[phase.phase] || 'from-slate-500 to-slate-600'} flex items-center justify-center text-2xl shadow-lg`}>
                {phaseIcons[phase.phase] || '📌'}
              </div>

              {/* 阶段卡片 */}
              <div className="bg-slate-800/30 border border-slate-700/50 rounded-xl overflow-hidden hover:bg-slate-800/50 hover:border-slate-600/50 transition-all duration-300">
                {/* 标题栏 */}
                <button
                  onClick={() => setExpandedPhase(expandedPhase === phase.phase ? null : phase.phase)}
                  className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-800/30 transition-colors"
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="text-lg font-bold text-white">{phase.phase}</h4>
                      {phase.estimatedTime && (
                        <span className="px-3 py-1 bg-blue-500/20 text-blue-400 text-sm rounded-full flex items-center space-x-1">
                          <span>⏱️</span>
                          <span>{phase.estimatedTime}</span>
                        </span>
                      )}
                    </div>
                    <div className="flex items-center space-x-4 text-sm text-slate-400">
                      <span>{phase.tasks.length} 个任务</span>
                      {phase.resources && <span>{phase.resources.length} 项资源</span>}
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      checked={selectedPhases.includes(phase.phase)}
                      onChange={() => handlePhaseToggle(phase.phase)}
                      onClick={(e) => e.stopPropagation()}
                      className="w-5 h-5 rounded border-slate-600 text-blue-500 focus:ring-blue-500 focus:ring-offset-slate-900 cursor-pointer"
                    />
                    <svg
                      className={`w-5 h-5 text-slate-400 transition-transform duration-300 ${
                        expandedPhase === phase.phase ? 'rotate-180' : ''
                      }`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>

                {/* 展开内容 */}
                {expandedPhase === phase.phase && (
                  <div className="px-6 pb-6 space-y-4 animate-fadeIn">
                    {/* 任务清单 */}
                    <div>
                      <h5 className="text-sm font-semibold text-slate-400 mb-3 uppercase tracking-wider">
                        任务清单
                      </h5>
                      <div className="space-y-2">
                        {phase.tasks.map((task, taskIndex) => (
                          <div
                            key={taskIndex}
                            className="flex items-start space-x-3 p-3 bg-slate-900/50 rounded-lg hover:bg-slate-900/70 transition-colors"
                          >
                            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                              {taskIndex + 1}
                            </div>
                            <p className="flex-1 text-slate-300 text-sm leading-relaxed">{task}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* 所需资源 */}
                    {phase.resources && phase.resources.length > 0 && (
                      <div>
                        <h5 className="text-sm font-semibold text-slate-400 mb-3 uppercase tracking-wider">
                          所需资源
                        </h5>
                        <div className="flex flex-wrap gap-2">
                          {phase.resources.map((resource, resourceIndex) => (
                            <span
                              key={resourceIndex}
                              className="px-3 py-1.5 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-400 text-sm flex items-center space-x-2"
                            >
                              <span>📦</span>
                              <span>{resource}</span>
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 最佳实践提示 */}
                    <div className="p-4 bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-lg">
                      <div className="flex items-start space-x-2">
                        <span className="text-lg">💡</span>
                        <div className="flex-1">
                          <p className="text-sm text-blue-400 font-semibold mb-1">最佳实践</p>
                          <p className="text-sm text-blue-300/80">
                            {phase.phase === '需求分析' && '充分理解业务需求，与stakeholder保持密切沟通'}
                            {phase.phase === '系统设计' && '注重模块化设计，考虑可扩展性和可维护性'}
                            {phase.phase === '开发阶段' && '遵循代码规范，进行持续集成和代码审查'}
                            {phase.phase === '测试阶段' && '建立完整的测试体系，包括单元测试、集成测试和E2E测试'}
                            {phase.phase === '部署上线' && '制定详细的上线计划，准备回滚方案'}
                            {phase.phase === '维护优化' && '持续监控系统性能，及时响应用户反馈'}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 统计信息 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-xl text-center">
          <div className="text-2xl font-bold text-blue-400 mb-1">{advice.length}</div>
          <div className="text-sm text-slate-400">开发阶段</div>
        </div>
        <div className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-xl text-center">
          <div className="text-2xl font-bold text-purple-400 mb-1">
            {advice.reduce((sum, a) => sum + a.tasks.length, 0)}
          </div>
          <div className="text-sm text-slate-400">总任务数</div>
        </div>
        <div className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-xl text-center">
          <div className="text-2xl font-bold text-green-400 mb-1">
            {advice.filter(a => a.estimatedTime).length}
          </div>
          <div className="text-sm text-slate-400">有时间估算</div>
        </div>
        <div className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-xl text-center">
          <div className="text-2xl font-bold text-orange-400 mb-1">
            {advice.reduce((sum, a) => sum + (a.resources?.length || 0), 0)}
          </div>
          <div className="text-sm text-slate-400">所需资源</div>
        </div>
      </div>
    </div>
  );
};

export default DevelopmentAdviceSection;
