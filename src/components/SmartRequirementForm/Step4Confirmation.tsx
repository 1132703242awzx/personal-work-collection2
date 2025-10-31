import { ProjectRequirements } from '../../types';
import {
  getComplexityLabel,
  getBudgetLabel,
} from '../../utils/validation';

interface Step4Props {
  data: Partial<ProjectRequirements>;
  onEdit: (step: number) => void;
}

const Step4Confirmation = ({ data, onEdit }: Step4Props) => {
  const platformIcons: Record<string, string> = {
    web: '🌐',
    ios: '🍎',
    android: '🤖',
    windows: '🪟',
    mac: '💻',
    linux: '🐧',
    cloud: '☁️',
  };

  const projectTypeNames: Record<string, string> = {
    web: 'Web 应用',
    mobile: '移动应用',
    desktop: '桌面应用',
    fullstack: '全栈应用',
    api: 'API 服务',
    data: '数据处理',
  };

  const timelineLabels: Record<string, string> = {
    urgent: '紧急（1-2周）',
    short: '短期（1个月）',
    medium: '中期（3个月）',
    long: '长期（6个月）',
    flexible: '灵活安排',
  };

  const commonFeatures = [
    { id: 'auth', name: '用户认证', icon: '🔐' },
    { id: 'dashboard', name: '数据面板', icon: '📊' },
    { id: 'crud', name: 'CRUD 操作', icon: '✏️' },
    { id: 'search', name: '搜索功能', icon: '🔍' },
    { id: 'notification', name: '通知系统', icon: '🔔' },
    { id: 'payment', name: '支付集成', icon: '💳' },
    { id: 'chat', name: '实时聊天', icon: '💬' },
    { id: 'file-upload', name: '文件上传', icon: '📁' },
    { id: 'analytics', name: '数据分析', icon: '📈' },
    { id: 'export', name: '数据导出', icon: '📤' },
    { id: 'multi-language', name: '多语言', icon: '🌍' },
    { id: 'responsive', name: '响应式设计', icon: '📱' },
  ];

  const getFeatureName = (featureId: string) => {
    const feature = commonFeatures.find(f => f.id === featureId);
    return feature ? `${feature.icon} ${feature.name}` : featureId;
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* 标题 */}
      <div className="text-center">
        <h3 className="text-3xl font-bold text-white mb-2">确认需求信息</h3>
        <p className="text-slate-400">请仔细核对以下信息，确认无误后提交</p>
      </div>

      {/* 项目类型与平台 */}
      <div className="p-6 bg-slate-800/30 border border-slate-700/50 rounded-xl hover:bg-slate-800/50 transition-all duration-300">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-bold text-blue-400 flex items-center space-x-2">
            <span>📋</span>
            <span>项目类型与平台</span>
          </h4>
          <button
            type="button"
            onClick={() => onEdit(1)}
            className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
          >
            编辑
          </button>
        </div>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <span className="text-slate-500 w-24">项目类型:</span>
            <span className="text-white font-medium">
              {projectTypeNames[data.projectType || ''] || data.projectType}
            </span>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-slate-500 w-24">目标平台:</span>
            <div className="flex flex-wrap gap-2">
              {(data.targetPlatform || []).map((platform) => (
                <span
                  key={platform}
                  className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 text-sm flex items-center space-x-1"
                >
                  <span>{platformIcons[platform]}</span>
                  <span className="capitalize">{platform}</span>
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 项目复杂度与预算 */}
      <div className="p-6 bg-slate-800/30 border border-slate-700/50 rounded-xl hover:bg-slate-800/50 transition-all duration-300">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-bold text-purple-400 flex items-center space-x-2">
            <span>⚙️</span>
            <span>项目复杂度与预算</span>
          </h4>
          <button
            type="button"
            onClick={() => onEdit(2)}
            className="text-sm text-purple-400 hover:text-purple-300 transition-colors"
          >
            编辑
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <span className="text-slate-500 text-sm">项目复杂度</span>
            <div className="text-white font-medium text-lg">
              {getComplexityLabel(data.complexity || 1)}
            </div>
          </div>
          <div className="space-y-2">
            <span className="text-slate-500 text-sm">预算范围</span>
            <div className="text-white font-medium text-lg">
              {getBudgetLabel(data.budget || 'medium')}
            </div>
          </div>
          {data.timeline && (
            <div className="space-y-2">
              <span className="text-slate-500 text-sm">预期时间</span>
              <div className="text-white font-medium">
                {timelineLabels[data.timeline]}
              </div>
            </div>
          )}
          {data.teamSize && (
            <div className="space-y-2">
              <span className="text-slate-500 text-sm">团队规模</span>
              <div className="text-white font-medium">
                {data.teamSize} 人
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 功能需求 */}
      <div className="p-6 bg-slate-800/30 border border-slate-700/50 rounded-xl hover:bg-slate-800/50 transition-all duration-300">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-bold text-green-400 flex items-center space-x-2">
            <span>✨</span>
            <span>功能需求</span>
          </h4>
          <button
            type="button"
            onClick={() => onEdit(3)}
            className="text-sm text-green-400 hover:text-green-300 transition-colors"
          >
            编辑
          </button>
        </div>
        {data.features && data.features.length > 0 ? (
          <div className="flex flex-wrap gap-2 mb-4">
            {data.features.map((feature, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-green-500/20 border border-green-500/30 rounded-lg text-green-400 text-sm"
              >
                {getFeatureName(feature)}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-slate-500 text-sm mb-4">未选择功能</p>
        )}
        
        {data.description && (
          <div className="space-y-2">
            <span className="text-slate-500 text-sm">项目描述</span>
            <div className="p-4 bg-slate-900/50 rounded-lg text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
              {data.description}
            </div>
          </div>
        )}
      </div>

      {/* 提交提示 */}
      <div className="p-6 bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl">
        <div className="flex items-start space-x-3">
          <span className="text-2xl">💡</span>
          <div className="flex-1">
            <h5 className="text-white font-semibold mb-2">提交前的提示</h5>
            <ul className="text-slate-400 text-sm space-y-1 list-disc list-inside">
              <li>请确保所有信息准确无误</li>
              <li>AI 将基于您提供的信息生成技术方案</li>
              <li>您可以随时返回修改任何步骤的信息</li>
              <li>生成的方案可以保存到历史记录</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Step4Confirmation;
