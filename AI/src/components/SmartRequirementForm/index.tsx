import { useState, useEffect, useCallback } from 'react';
import { ProjectRequirements } from '../../types';
import { validateStep } from '../../utils/validation';
import { DraftManager } from '../../utils/draftManager';
import StepIndicator from '../StepIndicator';
import Step1ProjectType from './Step1ProjectType';
import Step2ComplexityBudget from './Step2ComplexityBudget';
import Step3Features from './Step3Features';
import Step4Confirmation from './Step4Confirmation';

interface SmartRequirementFormProps {
  onSubmit: (data: ProjectRequirements) => void;
  onCancel?: () => void;
}

const STEPS = [
  { number: 1, title: '项目类型', description: '选择项目类型和平台' },
  { number: 2, title: '复杂度与预算', description: '评估项目规模' },
  { number: 3, title: '功能需求', description: '定义具体功能' },
  { number: 4, title: '确认提交', description: '核对信息' },
];

const SmartRequirementForm = ({ onSubmit, onCancel }: SmartRequirementFormProps) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<Partial<ProjectRequirements>>({
    projectType: '',
    targetPlatform: [],
    complexity: 3,
    budget: 'medium',
    features: [],
    description: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const draftManager = new DraftManager();

  // 加载草稿
  useEffect(() => {
    const draft = draftManager.loadDraft();
    if (draft) {
      setFormData(draft.data);
      setCurrentStep(draft.step);
    }
  }, []);

  // 自动保存草稿（防抖 2 秒）
  useEffect(() => {
    const timer = setTimeout(() => {
      draftManager.autoSaveDraft(currentStep, formData);
    }, 2000);

    return () => clearTimeout(timer);
  }, [formData, currentStep]);

  // 更新表单数据
  const handleDataChange = useCallback((newData: Partial<ProjectRequirements>) => {
    setFormData(newData);
    // 清除当前步骤的错误
    setErrors({});
  }, []);

  // 验证当前步骤
  const validateCurrentStep = () => {
    const result = validateStep(currentStep, formData);
    setErrors(result.errors);
    return result.isValid;
  };

  // 下一步
  const handleNext = () => {
    if (validateCurrentStep()) {
      setCurrentStep(prev => Math.min(prev + 1, STEPS.length));
    }
  };

  // 上一步
  const handlePrevious = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
    setErrors({});
  };

  // 跳转到指定步骤
  const handleStepClick = (step: number) => {
    // 只允许跳转到已完成的步骤或下一步
    if (step < currentStep) {
      setCurrentStep(step);
      setErrors({});
    } else if (step === currentStep + 1) {
      handleNext();
    }
  };

  // 从确认页编辑指定步骤
  const handleEdit = (step: number) => {
    setCurrentStep(step);
    setErrors({});
  };

  // 提交表单
  const handleSubmit = async () => {
    if (!validateCurrentStep()) {
      return;
    }

    setIsSubmitting(true);
    try {
      // 确保所有必填字段都有值
      const completeData: ProjectRequirements = {
        projectType: formData.projectType || '',
        targetPlatform: formData.targetPlatform || [],
        complexity: formData.complexity || 3,
        budget: formData.budget || 'medium',
        features: formData.features || [],
        description: formData.description || '',
        timeline: formData.timeline,
        teamSize: formData.teamSize,
      };

      await onSubmit(completeData);
      
      // 提交成功后清除草稿
      draftManager.clearDraft();
    } catch (error) {
      console.error('提交失败:', error);
      // 这里可以显示错误提示
    } finally {
      setIsSubmitting(false);
    }
  };

  // 取消并清除草稿
  const handleCancel = () => {
    if (window.confirm('确定要取消吗?未保存的数据将丢失。')) {
      draftManager.clearDraft();
      onCancel?.();
    }
  };

  // 检查是否有草稿
  const hasDraft = draftManager.hasDraft();
  const draftTime = draftManager.getDraftTimestamp();

  return (
    <div className="max-w-5xl mx-auto">
      {/* 草稿提示 */}
      {hasDraft && draftTime && (
        <div className="mb-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl animate-fadeIn">
          <div className="flex items-center space-x-2 text-blue-400">
            <span>💾</span>
            <span className="text-sm">
              已自动恢复上次编辑的内容（
              {new Date(draftTime).toLocaleString('zh-CN')}）
            </span>
          </div>
        </div>
      )}

      {/* 步骤指示器 */}
      <div className="mb-8">
        <StepIndicator
          steps={STEPS}
          currentStep={currentStep}
          onStepClick={handleStepClick}
        />
      </div>

      {/* 表单内容 */}
      <div className="bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
        {currentStep === 1 && (
          <Step1ProjectType
            data={formData}
            errors={errors}
            onChange={handleDataChange}
          />
        )}
        {currentStep === 2 && (
          <Step2ComplexityBudget
            data={formData}
            errors={errors}
            onChange={handleDataChange}
          />
        )}
        {currentStep === 3 && (
          <Step3Features
            data={formData}
            errors={errors}
            onChange={handleDataChange}
          />
        )}
        {currentStep === 4 && (
          <Step4Confirmation
            data={formData}
            onEdit={handleEdit}
          />
        )}

        {/* 导航按钮 */}
        <div className="flex items-center justify-between mt-8 pt-6 border-t border-slate-700/50">
          <div>
            {currentStep > 1 ? (
              <button
                type="button"
                onClick={handlePrevious}
                className="px-6 py-3 bg-slate-700 text-white rounded-xl font-semibold hover:bg-slate-600 transition-all duration-300 flex items-center space-x-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>上一步</span>
              </button>
            ) : (
              <button
                type="button"
                onClick={handleCancel}
                className="px-6 py-3 text-slate-400 hover:text-white transition-colors"
              >
                取消
              </button>
            )}
          </div>

          <div className="flex items-center space-x-4">
            {/* 步骤进度提示 */}
            <span className="text-slate-500 text-sm">
              第 {currentStep} / {STEPS.length} 步
            </span>

            {currentStep < STEPS.length ? (
              <button
                type="button"
                onClick={handleNext}
                className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 flex items-center space-x-2 shadow-lg shadow-blue-500/30"
              >
                <span>下一步</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-xl font-semibold hover:from-green-600 hover:to-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center space-x-2 shadow-lg shadow-green-500/30"
              >
                {isSubmitting ? (
                  <>
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    <span>提交中...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span>提交需求</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* 底部提示 */}
      <div className="mt-6 text-center">
        <p className="text-slate-500 text-sm">
          ✨ 您的输入会自动保存，可以随时返回继续编辑
        </p>
      </div>
    </div>
  );
};

export default SmartRequirementForm;
