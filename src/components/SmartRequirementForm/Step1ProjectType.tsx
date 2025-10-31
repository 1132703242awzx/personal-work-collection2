import { ProjectRequirements } from '../../types';

interface Step1Props {
  data: Partial<ProjectRequirements>;
  errors: Record<string, string>;
  onChange: (data: Partial<ProjectRequirements>) => void;
}

const Step1ProjectType = ({ data, errors, onChange }: Step1Props) => {
  const projectTypes = [
    { id: 'web', name: 'Web 应用', icon: '🌐', description: '网站、Web 应用程序' },
    { id: 'mobile', name: '移动应用', icon: '📱', description: 'iOS、Android 应用' },
    { id: 'desktop', name: '桌面应用', icon: '💻', description: 'Windows、Mac、Linux' },
    { id: 'fullstack', name: '全栈应用', icon: '🔄', description: '前后端完整系统' },
    { id: 'api', name: 'API 服务', icon: '🔌', description: 'RESTful、GraphQL' },
    { id: 'data', name: '数据分析', icon: '📊', description: '数据处理、可视化' },
  ];

  const platforms = [
    { id: 'web', name: 'Web 浏览器', icon: '🌐' },
    { id: 'ios', name: 'iOS', icon: '🍎' },
    { id: 'android', name: 'Android', icon: '🤖' },
    { id: 'windows', name: 'Windows', icon: '🪟' },
    { id: 'mac', name: 'macOS', icon: '🖥️' },
    { id: 'linux', name: 'Linux', icon: '🐧' },
    { id: 'cloud', name: '云平台', icon: '☁️' },
  ];

  const handleProjectTypeChange = (type: string) => {
    onChange({ ...data, projectType: type });
  };

  const handlePlatformToggle = (platform: string) => {
    const currentPlatforms = data.targetPlatform || [];
    const newPlatforms = currentPlatforms.includes(platform)
      ? currentPlatforms.filter(p => p !== platform)
      : [...currentPlatforms, platform];
    
    onChange({ ...data, targetPlatform: newPlatforms });
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* 项目类型选择 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">选择项目类型</h3>
        <p className="text-slate-400 mb-6">选择最符合您项目的类型</p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projectTypes.map(type => (
            <button
              key={type.id}
              type="button"
              onClick={() => handleProjectTypeChange(type.id)}
              className={`p-6 rounded-xl text-left transition-all duration-300 ${
                data.projectType === type.id
                  ? 'bg-gradient-to-br from-blue-500/20 to-purple-500/20 border-2 border-blue-500 shadow-lg shadow-blue-500/20'
                  : 'bg-slate-800/30 border-2 border-slate-700/50 hover:bg-slate-800/50 hover:border-slate-600/50'
              }`}
            >
              <div className="flex items-start space-x-4">
                <div className="text-4xl">{type.icon}</div>
                <div className="flex-1">
                  <h4 className="text-lg font-bold text-white mb-1">
                    {type.name}
                  </h4>
                  <p className="text-sm text-slate-400">{type.description}</p>
                </div>
                {data.projectType === type.id && (
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

        {errors.projectType && (
          <p className="mt-2 text-sm text-red-400 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{errors.projectType}</span>
          </p>
        )}
      </div>

      {/* 目标平台选择 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">目标平台</h3>
        <p className="text-slate-400 mb-6">选择应用需要支持的平台（可多选）</p>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
          {platforms.map(platform => {
            const isSelected = data.targetPlatform?.includes(platform.id);
            return (
              <button
                key={platform.id}
                type="button"
                onClick={() => handlePlatformToggle(platform.id)}
                className={`p-4 rounded-xl text-center transition-all duration-300 ${
                  isSelected
                    ? 'bg-gradient-to-br from-blue-500/20 to-purple-500/20 border-2 border-blue-500 shadow-lg shadow-blue-500/20 scale-105'
                    : 'bg-slate-800/30 border-2 border-slate-700/50 hover:bg-slate-800/50 hover:border-slate-600/50'
                }`}
              >
                <div className="text-3xl mb-2">{platform.icon}</div>
                <div className={`text-sm font-medium ${
                  isSelected ? 'text-blue-400' : 'text-slate-400'
                }`}>
                  {platform.name}
                </div>
              </button>
            );
          })}
        </div>

        {errors.targetPlatform && (
          <p className="mt-2 text-sm text-red-400 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{errors.targetPlatform}</span>
          </p>
        )}
      </div>

      {/* 选择摘要 */}
      {data.projectType && data.targetPlatform && data.targetPlatform.length > 0 && (
        <div className="p-6 bg-blue-500/10 border border-blue-500/20 rounded-xl animate-fadeIn">
          <h4 className="text-lg font-bold text-blue-400 mb-3 flex items-center space-x-2">
            <span>✨</span>
            <span>您的选择</span>
          </h4>
          <div className="space-y-2 text-slate-300">
            <p>
              <span className="text-slate-500">项目类型：</span>
              <span className="font-semibold">
                {projectTypes.find(t => t.id === data.projectType)?.name}
              </span>
            </p>
            <p>
              <span className="text-slate-500">目标平台：</span>
              <span className="font-semibold">
                {data.targetPlatform
                  .map(p => platforms.find(pl => pl.id === p)?.name)
                  .join('、')}
              </span>
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Step1ProjectType;
