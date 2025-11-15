import { useState } from 'react';

interface AIPromptDisplayProps {
  prompt: string;
  title?: string;
  language?: string;
}

const AIPromptDisplay = ({
  prompt,
  title = 'AI 提示词',
  language = 'markdown',
}: AIPromptDisplayProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(prompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">🤖</span>
          <h3 className="text-lg font-bold text-white">{title}</h3>
          <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs font-semibold rounded-md border border-blue-500/30">
            {language}
          </span>
        </div>

        {/* Copy Button */}
        <button
          onClick={handleCopy}
          className="group relative px-4 py-2 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-lg hover:bg-slate-700/50 hover:border-slate-600/50 transition-all duration-300"
        >
          <div className="flex items-center space-x-2">
            {copied ? (
              <>
                <svg
                  className="w-4 h-4 text-green-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="text-sm font-medium text-green-400">
                  已复制!
                </span>
              </>
            ) : (
              <>
                <svg
                  className="w-4 h-4 text-slate-400 group-hover:text-white transition-colors"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                  />
                </svg>
                <span className="text-sm font-medium text-slate-400 group-hover:text-white transition-colors">
                  复制
                </span>
              </>
            )}
          </div>
        </button>
      </div>

      {/* Prompt Content */}
      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        
        <div className="relative bg-slate-900/50 backdrop-blur-sm border border-slate-700/50 rounded-xl overflow-hidden">
          {/* Code Header Bar */}
          <div className="flex items-center space-x-2 px-4 py-2 bg-slate-800/50 border-b border-slate-700/50">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>

          {/* Code Content */}
          <pre className="p-6 overflow-x-auto">
            <code className="text-sm text-slate-300 leading-relaxed font-mono">
              {prompt}
            </code>
          </pre>

          {/* Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 pointer-events-none"></div>
        </div>
      </div>

      {/* Statistics */}
      <div className="flex items-center space-x-4 text-xs text-slate-500">
        <div className="flex items-center space-x-1">
          <span>📝</span>
          <span>{prompt.length} 字符</span>
        </div>
        <div className="flex items-center space-x-1">
          <span>📄</span>
          <span>{prompt.split('\n').length} 行</span>
        </div>
        <div className="flex items-center space-x-1">
          <span>🔤</span>
          <span>{prompt.split(/\s+/).length} 词</span>
        </div>
      </div>
    </div>
  );
};

export default AIPromptDisplay;
