import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SmartRequirementForm from '../components/SmartRequirementForm';
import { ProjectRequirements } from '../types';

const SmartFormPage = () => {
  const navigate = useNavigate();
  const [isGenerating, setIsGenerating] = useState(false);

  const handleSubmit = async (data: ProjectRequirements) => {
    console.log('📋 提交的需求数据:', data);
    setIsGenerating(true);

    try {
      // 这里可以调用 AI 服务生成方案
      // const result = await AIAdvisorService.analyzeRequirements(data);
      
      // 模拟 AI 生成过程
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 生成成功后跳转到结果页面或显示结果
      alert('✅ 需求提交成功!AI 正在生成技术方案...');
      
      // 可以传递数据到结果页面
      // navigate('/result', { state: { requirements: data } });
    } catch (error) {
      console.error('提交失败:', error);
      alert('❌ 提交失败,请重试');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="text-center mb-12 animate-fadeIn">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            智能需求分析
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            通过多步骤引导,帮助您清晰地描述项目需求,AI 将基于您的输入生成专业的技术方案
          </p>
        </div>

        {/* 智能表单 */}
        {!isGenerating ? (
          <SmartRequirementForm onSubmit={handleSubmit} onCancel={handleCancel} />
        ) : (
          // 生成中的加载状态
          <div className="max-w-3xl mx-auto bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-12 text-center animate-fadeIn">
            <div className="flex justify-center mb-6">
              <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
            </div>
            <h3 className="text-2xl font-bold text-white mb-3">AI 正在分析您的需求...</h3>
            <p className="text-slate-400 mb-8">
              正在生成技术方案、架构建议和开发计划,请稍候
            </p>
            <div className="space-y-3 text-left max-w-md mx-auto">
              {[
                '分析项目复杂度和技术要求',
                '推荐最佳技术栈组合',
                '设计系统架构方案',
                '制定开发阶段计划',
                '评估资源和时间预算',
              ].map((step, index) => (
                <div
                  key={index}
                  className="flex items-center space-x-3 text-slate-400 animate-fadeIn"
                  style={{ animationDelay: `${index * 0.2}s` }}
                >
                  <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                  <span>{step}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SmartFormPage;
