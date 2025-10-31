import { useState } from 'react';
import { AIPrompt } from '../../types';

interface AIPromptSectionProps {
  prompt: AIPrompt;
}

const AIPromptSection = ({ prompt }: AIPromptSectionProps) => {
  const [copiedField, setCopiedField] = useState<string | null>(null);
  const [expandedSection, setExpandedSection] = useState<string | null>('architecture');

  const promptSections = [
    {
      id: 'architecture',
      title: '架构设计提示词',
      icon: '🏗️',
      content: prompt.prompt,
      color: 'from-blue-500 to-cyan-500',
    },
    {
      id: 'context',
      title: '开发指导提示词',
      icon: '💡',
      content: prompt.context,
      color: 'from-purple-500 to-pink-500',
    },
    {
      id: 'suggestions',
      title: '测试策略提示词',
      icon: '🧪',
      content: prompt.suggestions.join('\n\n'),
      color: 'from-green-500 to-emerald-500',
    },
  ];

  const handleCopy = async (content: string, field: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedField(field);
      setTimeout(() => setCopiedField(null), 2000);
    } catch (error) {
      console.error('复制失败:', error);
    }
  };

  const handleCopyAll = async () => {
    const allContent = `
# 架构设计提示词
${prompt.prompt}

# 开发指导提示词
${prompt.context}

# 测试策略提示词
${prompt.suggestions.join('\n\n')}
    `.trim();

    await handleCopy(allContent, 'all');
  };

  return (
    <div className="space-y-6">
      {/* 标题和全局操作 */}
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold text-white flex items-center space-x-2">
          <span>🤖</span>
          <span>AI 提示词</span>
        </h3>
        <button
          onClick={handleCopyAll}
          className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 flex items-center space-x-2 shadow-lg shadow-blue-500/30"
        >
          {copiedField === 'all' ? (
            <>
              <span>✓</span>
              <span>已复制全部</span>
            </>
          ) : (
            <>
              <span>📋</span>
              <span>复制全部</span>
            </>
          )}
        </button>
      </div>

      {/* 提示词卡片 */}
      <div className="space-y-4">
        {promptSections.map((section) => (
          <div
            key={section.id}
            className="bg-slate-800/30 border border-slate-700/50 rounded-xl overflow-hidden hover:border-slate-600/50 transition-all duration-300"
          >
            {/* 标题栏 */}
            <button
              onClick={() => setExpandedSection(expandedSection === section.id ? null : section.id)}
              className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-800/30 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${section.color} flex items-center justify-center text-xl`}>
                  {section.icon}
                </div>
                <h4 className="text-lg font-bold text-white">{section.title}</h4>
              </div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleCopy(section.content, section.id);
                  }}
                  className="px-3 py-1.5 bg-slate-700/50 text-slate-300 rounded-lg text-sm hover:bg-slate-600/50 transition-colors flex items-center space-x-1"
                >
                  {copiedField === section.id ? (
                    <>
                      <span>✓</span>
                      <span>已复制</span>
                    </>
                  ) : (
                    <>
                      <span>📋</span>
                      <span>复制</span>
                    </>
                  )}
                </button>
                <svg
                  className={`w-5 h-5 text-slate-400 transition-transform duration-300 ${
                    expandedSection === section.id ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </button>

            {/* 展开的内容 */}
            {expandedSection === section.id && (
              <div className="px-6 pb-6 animate-fadeIn">
                <div className="relative">
                  {/* 代码块样式的内容展示 */}
                  <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
                    <pre className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap font-mono overflow-x-auto">
                      {section.content}
                    </pre>
                  </div>

                  {/* 字符统计 */}
                  <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
                    <span>字符数: {section.content.length}</span>
                    <span>行数: {section.content.split('\n').length}</span>
                  </div>
                </div>

                {/* 使用提示 */}
                <div className="mt-4 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                  <div className="flex items-start space-x-2 text-sm text-blue-400">
                    <span className="text-lg">💡</span>
                    <div>
                      <p className="font-semibold mb-1">使用建议:</p>
                      <p className="text-blue-300/80">
                        {section.id === 'architecture' && '将此提示词输入到 AI 助手中，获取详细的架构设计方案'}
                        {section.id === 'context' && '使用此提示词指导开发流程，确保代码质量和最佳实践'}
                        {section.id === 'suggestions' && '参考这些建议制定完整的测试策略，提高代码可靠性'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* 快速操作提示 */}
      <div className="p-4 bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-xl">
        <div className="flex items-start space-x-3">
          <span className="text-2xl">✨</span>
          <div className="flex-1">
            <h5 className="text-white font-semibold mb-2">如何使用这些提示词</h5>
            <ul className="space-y-1 text-sm text-slate-400">
              <li className="flex items-center space-x-2">
                <span className="text-purple-400">•</span>
                <span>点击"复制"按钮将提示词复制到剪贴板</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="text-purple-400">•</span>
                <span>粘贴到 ChatGPT、Claude 等 AI 助手中</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="text-purple-400">•</span>
                <span>根据 AI 的回复进行项目开发和优化</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIPromptSection;
