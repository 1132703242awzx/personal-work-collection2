import { useState } from 'react';
import { ProjectRequirement } from '../types';
import SmartInput from './SmartInput';
import ProgressIndicator from './ProgressIndicator';

interface ProjectInputProps {
  onAnalyze: (requirement: ProjectRequirement, useAI: boolean) => void;
  isLoading: boolean;
}

const ProjectInput: React.FC<ProjectInputProps> = ({ onAnalyze, isLoading }) => {
  const [formData, setFormData] = useState<ProjectRequirement>({
    projectName: '',
    description: '',
    category: 'Web应用',
    targetPlatform: ['Web'],
    features: [],
    userStory: '',
    technicalConstraints: '',
  });

  const [currentFeature, setCurrentFeature] = useState('');
  const [useAI, setUseAI] = useState(true); // AI 增强分析开关
  const [progress, setProgress] = useState(0);

  // 检查 AI 配置状态
  const aiConfigured = !!(
    import.meta.env.VITE_AI_PROVIDER && 
    import.meta.env.VITE_AI_API_KEY
  );

  const categories = ['Web应用', '移动应用', '全栈应用', '数据分析', '人工智能', '企业系统', '游戏开发', '其他'];
  const platforms = ['Web', '移动端', '桌面端', '云平台', '物联网'];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePlatformChange = (platform: string) => {
    setFormData(prev => ({
      ...prev,
      targetPlatform: prev.targetPlatform.includes(platform)
        ? prev.targetPlatform.filter(p => p !== platform)
        : [...prev.targetPlatform, platform],
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // 验证必填字段
    if (!formData.projectName || !formData.description) {
      alert('请填写项目名称和项目描述');
      return;
    }
    
    // 过滤空的 features
    const validFeatures = formData.features.filter(f => f.trim() !== '');
    
    // 提交数据,传递 useAI 参数
    console.log('提交分析请求:', { ...formData, features: validFeatures, useAI });
    setProgress(0);
    onAnalyze({ ...formData, features: validFeatures }, useAI);
    
    // 模拟进度
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 150);
  };

  if (isLoading) {
    return (
      <div className="max-w-2xl mx-auto p-8">
        <div className="text-center mb-8">
          <div className="inline-block p-4 bg-blue-500/10 rounded-2xl mb-4">
            <span className="text-6xl">🤖</span>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">AI 正在分析中...</h2>
          <p className="text-slate-400">请稍候，我们正在为您生成专业的开发建议</p>
        </div>

        <ProgressIndicator
          progress={progress}
          status="loading"
          message="分析项目需求和技术要求..."
        />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-12 animate-fadeIn">
        <div className="inline-block p-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-4">
          <span className="text-6xl">📝</span>
        </div>
        <h2 className="text-4xl font-bold text-white mb-3">项目需求输入</h2>
        <p className="text-slate-400 text-lg">请详细描述您的项目需求，我们将为您生成专业的开发建议</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Project Name */}
        <div className="space-y-2 animate-fadeIn">
          <label className="block text-sm font-semibold text-slate-300">
            项目名称 <span className="text-red-400">*</span>
          </label>
          <input
            type="text"
            name="projectName"
            value={formData.projectName}
            onChange={handleInputChange}
            placeholder="例如：智能客服系统"
            required
            className="w-full px-4 py-3 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 transition-all duration-300"
          />
        </div>

        {/* Category */}
        <div className="space-y-2 animate-fadeIn animation-delay-100">
          <label className="block text-sm font-semibold text-slate-300">
            项目类型 <span className="text-red-400">*</span>
          </label>
          <select
            name="category"
            value={formData.category}
            onChange={handleInputChange}
            className="w-full px-4 py-3 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl text-slate-200 focus:outline-none focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 transition-all duration-300"
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        {/* Target Platform */}
        <div className="space-y-3 animate-fadeIn animation-delay-200">
          <label className="block text-sm font-semibold text-slate-300">
            目标平台 <span className="text-red-400">*</span>
          </label>
          <div className="flex flex-wrap gap-3">
            {platforms.map(platform => (
              <button
                key={platform}
                type="button"
                onClick={() => handlePlatformChange(platform)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                  formData.targetPlatform.includes(platform)
                    ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                    : 'bg-slate-800/50 text-slate-400 border border-slate-700/50 hover:border-slate-600/50'
                }`}
              >
                {platform}
              </button>
            ))}
          </div>
        </div>

        {/* Description */}
        <div className="animate-fadeIn animation-delay-300">
          <SmartInput
            value={formData.description}
            onChange={(value) => setFormData(prev => ({ ...prev, description: value }))}
            label="项目描述"
            placeholder="详细描述您的项目功能、目标用户、核心价值..."
            maxLength={2000}
            rows={6}
          />
        </div>

        {/* Core Features */}
        <div className="space-y-3 animate-fadeIn animation-delay-350">
          <label className="block text-sm font-semibold text-slate-300">
            核心功能 <span className="text-slate-500">(可选，建议至少填写3-5个)</span>
          </label>
          <div className="space-y-2">
            <div className="flex gap-2">
              <input
                type="text"
                value={currentFeature}
                onChange={(e) => setCurrentFeature(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    if (currentFeature.trim()) {
                      setFormData(prev => ({
                        ...prev,
                        features: [...prev.features, currentFeature.trim()]
                      }));
                      setCurrentFeature('');
                    }
                  }
                }}
                placeholder="输入功能后按回车添加，例如：用户登录注册"
                className="flex-1 px-4 py-3 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 transition-all duration-300"
              />
              <button
                type="button"
                onClick={() => {
                  if (currentFeature.trim()) {
                    setFormData(prev => ({
                      ...prev,
                      features: [...prev.features, currentFeature.trim()]
                    }));
                    setCurrentFeature('');
                  }
                }}
                className="px-6 py-3 bg-blue-500/20 text-blue-400 rounded-xl font-medium hover:bg-blue-500/30 transition-all duration-300"
              >
                添加
              </button>
            </div>
            {formData.features.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3">
                {formData.features.map((feature, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-2 px-3 py-2 bg-blue-500/20 border border-blue-500/30 rounded-lg text-slate-300"
                  >
                    <span>{feature}</span>
                    <button
                      type="button"
                      onClick={() => {
                        setFormData(prev => ({
                          ...prev,
                          features: prev.features.filter((_, i) => i !== index)
                        }));
                      }}
                      className="text-slate-400 hover:text-red-400 transition-colors"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* User Story */}
        <div className="animate-fadeIn animation-delay-400">
          <SmartInput
            value={formData.userStory || ''}
            onChange={(value) => setFormData(prev => ({ ...prev, userStory: value }))}
            label="用户故事（可选）"
            placeholder="作为...我想要...以便于..."
            maxLength={1000}
            rows={4}
          />
        </div>

        {/* Technical Constraints */}
        <div className="animate-fadeIn animation-delay-500">
          <SmartInput
            value={formData.technicalConstraints || ''}
            onChange={(value) => setFormData(prev => ({ ...prev, technicalConstraints: value }))}
            label="技术约束（可选）"
            placeholder="例如：必须使用 React、需要支持 IE11、预算有限..."
            maxLength={1000}
            rows={4}
          />
        </div>

        {/* AI Enhancement Toggle */}
        <div className="animate-fadeIn animation-delay-550">
          <div className="p-6 bg-gradient-to-r from-purple-500/10 to-blue-500/10 backdrop-blur-sm border border-purple-500/20 rounded-2xl">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <span className="text-2xl">🤖</span>
                  <h3 className="text-lg font-bold text-white">AI 增强分析</h3>
                  {aiConfigured ? (
                    <span className="px-3 py-1 bg-green-500/20 text-green-400 text-xs rounded-full border border-green-500/30">
                      ✓ 已配置
                    </span>
                  ) : (
                    <span className="px-3 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full border border-yellow-500/30">
                      未配置
                    </span>
                  )}
                </div>
                <p className="text-sm text-slate-400">
                  {aiConfigured 
                    ? '使用 DeepSeek AI 提供更深入的分析和建议 (约 ¥0.01-0.02/次)'
                    : '启用后可获得更智能的分析，需先配置 AI (前往 /ai-config 页面配置)'}
                </p>
              </div>
              
              <div className="ml-6">
                <button
                  type="button"
                  onClick={() => setUseAI(!useAI)}
                  disabled={!aiConfigured}
                  className={`relative inline-flex h-8 w-16 items-center rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-900 ${
                    useAI && aiConfigured
                      ? 'bg-gradient-to-r from-purple-500 to-blue-500'
                      : 'bg-slate-700'
                  } ${!aiConfigured ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                >
                  <span
                    className={`inline-block h-6 w-6 transform rounded-full bg-white shadow-lg transition-transform duration-300 ${
                      useAI && aiConfigured ? 'translate-x-9' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
            
            {!aiConfigured && (
              <div className="mt-4 pt-4 border-t border-slate-700">
                <a
                  href="/ai-config"
                  className="inline-flex items-center space-x-2 text-sm text-blue-400 hover:text-blue-300 transition-colors"
                >
                  <span>⚙️</span>
                  <span>前往配置 AI</span>
                  <span>→</span>
                </a>
              </div>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-center pt-6 animate-fadeIn animation-delay-600">
          <button
            type="submit"
            disabled={!formData.projectName || !formData.description}
            className="group px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transform hover:-translate-y-1 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center space-x-2"
          >
            <span>🚀</span>
            <span>{useAI && aiConfigured ? 'AI 增强分析' : '开始分析'}</span>
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </button>
        </div>
      </form>

      {/* Tips */}
      <div className="mt-12 p-6 bg-blue-500/10 backdrop-blur-sm border border-blue-500/20 rounded-2xl animate-fadeIn animation-delay-700">
        <h3 className="text-lg font-bold text-blue-400 mb-3 flex items-center space-x-2">
          <span>💡</span>
          <span>填写建议</span>
        </h3>
        <ul className="space-y-2 text-sm text-slate-400">
          <li>• 项目描述越详细，AI 生成的建议越准确</li>
          <li>• 可以使用 Markdown 格式来组织内容</li>
          <li>• 建议包含：功能需求、性能要求、用户规模等信息</li>
          <li>• 技术约束可以帮助我们推荐更合适的技术栈</li>
        </ul>
      </div>
    </div>
  );
};

export default ProjectInput;
