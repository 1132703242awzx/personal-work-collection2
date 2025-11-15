import { useState } from 'react';
import { ProjectRequirements } from '../../types';
import SmartInput from '../SmartInput';

interface Step3Props {
  data: Partial<ProjectRequirements>;
  errors: Record<string, string>;
  onChange: (data: Partial<ProjectRequirements>) => void;
}

const Step3Features = ({ data, errors, onChange }: Step3Props) => {
  const [newFeature, setNewFeature] = useState('');

  const commonFeatures = [
    { id: 'auth', name: '用户认证', icon: '🔐', category: '基础' },
    { id: 'dashboard', name: '数据面板', icon: '📊', category: '展示' },
    { id: 'crud', name: 'CRUD 操作', icon: '✏️', category: '基础' },
    { id: 'search', name: '搜索功能', icon: '🔍', category: '功能' },
    { id: 'notification', name: '通知系统', icon: '🔔', category: '功能' },
    { id: 'payment', name: '支付集成', icon: '💳', category: '集成' },
    { id: 'chat', name: '实时聊天', icon: '💬', category: '功能' },
    { id: 'file-upload', name: '文件上传', icon: '📁', category: '功能' },
    { id: 'analytics', name: '数据分析', icon: '📈', category: '分析' },
    { id: 'export', name: '数据导出', icon: '📤', category: '功能' },
    { id: 'multi-language', name: '多语言', icon: '🌍', category: '国际化' },
    { id: 'responsive', name: '响应式设计', icon: '📱', category: '界面' },
  ];

  const handleFeatureToggle = (feature: string) => {
    const currentFeatures = data.features || [];
    const newFeatures = currentFeatures.includes(feature)
      ? currentFeatures.filter(f => f !== feature)
      : [...currentFeatures, feature];
    
    onChange({ ...data, features: newFeatures });
  };

  const handleAddCustomFeature = () => {
    if (newFeature.trim()) {
      const currentFeatures = data.features || [];
      onChange({ ...data, features: [...currentFeatures, newFeature.trim()] });
      setNewFeature('');
    }
  };

  const handleRemoveFeature = (feature: string) => {
    const currentFeatures = data.features || [];
    onChange({ ...data, features: currentFeatures.filter(f => f !== feature) });
  };

  const handleDescriptionChange = (value: string) => {
    onChange({ ...data, description: value });
  };

  const selectedFeatures = data.features || [];
  const customFeatures = selectedFeatures.filter(
    f => !commonFeatures.find(cf => cf.id === f)
  );

  // 按分类分组
  const categorizedFeatures = commonFeatures.reduce((acc, feature) => {
    if (!acc[feature.category]) {
      acc[feature.category] = [];
    }
    acc[feature.category].push(feature);
    return acc;
  }, {} as Record<string, typeof commonFeatures>);

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* 常用功能快速选择 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">选择功能需求</h3>
        <p className="text-slate-400 mb-6">快速选择项目需要的常用功能（可多选）</p>

        <div className="space-y-6">
          {Object.entries(categorizedFeatures).map(([category, features]) => (
            <div key={category}>
              <h4 className="text-sm font-semibold text-slate-500 mb-3 uppercase tracking-wider">
                {category}
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                {features.map(feature => {
                  const isSelected = selectedFeatures.includes(feature.id);
                  return (
                    <button
                      key={feature.id}
                      type="button"
                      onClick={() => handleFeatureToggle(feature.id)}
                      className={`p-4 rounded-xl text-left transition-all duration-300 ${
                        isSelected
                          ? 'bg-gradient-to-br from-blue-500/20 to-purple-500/20 border-2 border-blue-500 shadow-lg shadow-blue-500/20'
                          : 'bg-slate-800/30 border-2 border-slate-700/50 hover:bg-slate-800/50 hover:border-slate-600/50'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{feature.icon}</span>
                        <span className={`text-sm font-medium ${
                          isSelected ? 'text-blue-400' : 'text-slate-300'
                        }`}>
                          {feature.name}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {errors.features && (
          <p className="mt-2 text-sm text-red-400 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{errors.features}</span>
          </p>
        )}
      </div>

      {/* 自定义功能添加 */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">添加自定义功能</h3>
        <p className="text-slate-400 mb-6">如果上面没有您需要的功能，请在这里添加</p>

        <div className="flex gap-3">
          <input
            type="text"
            value={newFeature}
            onChange={(e) => setNewFeature(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAddCustomFeature()}
            placeholder="输入自定义功能，按回车添加..."
            className="flex-1 px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 transition-all duration-300"
          />
          <button
            type="button"
            onClick={handleAddCustomFeature}
            disabled={!newFeature.trim()}
            className="px-6 py-3 bg-blue-500 text-white rounded-xl font-semibold hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
          >
            添加
          </button>
        </div>

        {/* 自定义功能列表 */}
        {customFeatures.length > 0 && (
          <div className="mt-4 space-y-2">
            <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">
              自定义功能
            </h4>
            <div className="flex flex-wrap gap-2">
              {customFeatures.map((feature, index) => (
                <div
                  key={index}
                  className="px-4 py-2 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-400 flex items-center space-x-2"
                >
                  <span className="text-sm font-medium">{feature}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveFeature(feature)}
                    className="text-purple-400 hover:text-purple-300 transition-colors"
                  >
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 项目描述 */}
      <div>
        <SmartInput
          value={data.description || ''}
          onChange={handleDescriptionChange}
          label="项目详细描述"
          placeholder="请详细描述您的项目需求、目标用户、核心功能、预期效果等..."
          maxLength={2000}
          rows={8}
        />
        {errors.description && (
          <p className="mt-2 text-sm text-red-400 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{errors.description}</span>
          </p>
        )}
      </div>

      {/* 已选功能摘要 */}
      {selectedFeatures.length > 0 && (
        <div className="p-6 bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl animate-fadeIn">
          <h4 className="text-lg font-bold text-blue-400 mb-3 flex items-center space-x-2">
            <span>✨</span>
            <span>已选择 {selectedFeatures.length} 个功能</span>
          </h4>
          <div className="flex flex-wrap gap-2">
            {selectedFeatures.slice(0, 10).map((featureId, index) => {
              const feature = commonFeatures.find(f => f.id === featureId);
              return (
                <div
                  key={index}
                  className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 text-sm"
                >
                  {feature ? `${feature.icon} ${feature.name}` : featureId}
                </div>
              );
            })}
            {selectedFeatures.length > 10 && (
              <div className="px-3 py-1 bg-slate-700/50 rounded-lg text-slate-400 text-sm">
                +{selectedFeatures.length - 10} 更多...
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Step3Features;
