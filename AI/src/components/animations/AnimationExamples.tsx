/**
 * 动画集成示例
 * 展示如何在实际应用中使用动画系统
 */

import { useState, useEffect } from 'react';
import PageTransition from './PageTransition';
import FadeIn from './FadeIn';
import AnimatedList from './AnimatedList';
import AnimatedButton from './AnimatedButton';
import AnimatedInput from './AnimatedInput';
import LoadingSpinner from './LoadingSpinner';
import Skeleton from './Skeleton';
import ProgressBar from './ProgressBar';
import Modal from './Modal';

// 示例1: 带动画的登录页面
export function AnimatedLoginPage() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000));
    setLoading(false);
  };

  return (
    <PageTransition>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
        <FadeIn direction="up" delay={0.2}>
          <div className="bg-slate-800 p-8 rounded-lg border border-slate-700 w-full max-w-md">
            <h1 className="text-3xl font-bold text-white mb-6 text-center">
              欢迎回来
            </h1>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <AnimatedInput
                label="邮箱"
                type="email"
                placeholder="输入您的邮箱"
                icon={
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                }
              />

              <AnimatedInput
                label="密码"
                type="password"
                placeholder="输入您的密码"
                icon={
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                }
              />

              <AnimatedButton
                variant="primary"
                size="lg"
                type="submit"
                loading={loading}
                className="w-full mt-6"
              >
                {loading ? '登录中...' : '登录'}
              </AnimatedButton>
            </form>
          </div>
        </FadeIn>
      </div>
    </PageTransition>
  );
}

// 示例2: 带动画的数据列表
export function AnimatedDataList() {
  const [items, setItems] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 模拟数据加载
    setTimeout(() => {
      setItems([
        '项目管理系统 v2.0',
        '用户认证服务',
        '实时通知模块',
        '数据分析平台',
        'API网关服务'
      ]);
      setLoading(false);
    }, 1500);
  }, []);

  return (
    <PageTransition>
      <div className="container mx-auto p-8">
        <FadeIn direction="down">
          <h1 className="text-4xl font-bold text-white mb-8">
            项目列表
          </h1>
        </FadeIn>

        {loading ? (
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <Skeleton key={i} variant="rectangular" height="80px" />
            ))}
          </div>
        ) : (
          <AnimatedList stagger="normal">
            {items.map((item, index) => (
              <div
                key={index}
                className="bg-slate-800 p-6 rounded-lg border border-slate-700 mb-4 hover:border-blue-500 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-white">{item}</h3>
                  <AnimatedButton variant="outline" size="sm">
                    查看详情
                  </AnimatedButton>
                </div>
              </div>
            ))}
          </AnimatedList>
        )}
      </div>
    </PageTransition>
  );
}

// 示例3: 带进度的表单
export function AnimatedMultiStepForm() {
  const [step, setStep] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const totalSteps = 4;
  const progress = (step / totalSteps) * 100;

  const nextStep = () => {
    if (step < totalSteps) {
      setStep(step + 1);
    } else {
      setModalOpen(true);
    }
  };

  const prevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <PageTransition>
      <div className="container mx-auto p-8 max-w-2xl">
        <FadeIn direction="up">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            智能项目创建
          </h1>
        </FadeIn>

        {/* 进度条 */}
        <FadeIn direction="down" delay={0.1}>
          <div className="mb-8">
            <div className="flex justify-between mb-2">
              <span className="text-white text-sm">进度</span>
              <span className="text-gray-400 text-sm">步骤 {step} / {totalSteps}</span>
            </div>
            <ProgressBar progress={progress} color="bg-blue-500" />
          </div>
        </FadeIn>

        {/* 表单内容 */}
        <div className="bg-slate-800 p-8 rounded-lg border border-slate-700">
          <FadeIn key={step} direction="up">
            <div className="min-h-[300px]">
              {step === 1 && (
                <div className="space-y-4">
                  <h2 className="text-2xl font-semibold text-white mb-4">
                    基本信息
                  </h2>
                  <AnimatedInput label="项目名称" placeholder="输入项目名称" />
                  <AnimatedInput label="项目描述" placeholder="简要描述项目" />
                </div>
              )}

              {step === 2 && (
                <div className="space-y-4">
                  <h2 className="text-2xl font-semibold text-white mb-4">
                    技术选择
                  </h2>
                  <AnimatedList stagger="fast">
                    {['React', 'Vue', 'Angular'].map(tech => (
                      <div
                        key={tech}
                        className="p-4 bg-slate-700 rounded-lg mb-2 cursor-pointer hover:bg-slate-600 transition-colors"
                      >
                        <span className="text-white">{tech}</span>
                      </div>
                    ))}
                  </AnimatedList>
                </div>
              )}

              {step === 3 && (
                <div className="space-y-4">
                  <h2 className="text-2xl font-semibold text-white mb-4">
                    项目配置
                  </h2>
                  <AnimatedInput label="Git仓库地址" placeholder="https://github.com/..." />
                  <AnimatedInput label="部署环境" placeholder="生产环境 URL" />
                </div>
              )}

              {step === 4 && (
                <div className="space-y-4">
                  <h2 className="text-2xl font-semibold text-white mb-4">
                    确认信息
                  </h2>
                  <div className="bg-slate-700 p-4 rounded-lg space-y-2">
                    <p className="text-gray-300">✓ 基本信息已填写</p>
                    <p className="text-gray-300">✓ 技术栈已选择</p>
                    <p className="text-gray-300">✓ 配置已完成</p>
                  </div>
                </div>
              )}
            </div>
          </FadeIn>

          {/* 按钮组 */}
          <div className="flex justify-between mt-8">
            <AnimatedButton
              variant="outline"
              onClick={prevStep}
              disabled={step === 1}
            >
              上一步
            </AnimatedButton>

            <AnimatedButton
              variant="primary"
              onClick={nextStep}
            >
              {step === totalSteps ? '完成' : '下一步'}
            </AnimatedButton>
          </div>
        </div>

        {/* 完成模态框 */}
        <Modal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          title="创建成功"
          size="md"
        >
          <div className="text-center py-6">
            <div className="text-6xl mb-4">🎉</div>
            <h3 className="text-2xl font-bold text-white mb-2">
              项目创建成功!
            </h3>
            <p className="text-gray-400 mb-6">
              您的项目已成功创建,可以开始使用了。
            </p>
            <AnimatedButton
              variant="primary"
              onClick={() => setModalOpen(false)}
            >
              开始使用
            </AnimatedButton>
          </div>
        </Modal>
      </div>
    </PageTransition>
  );
}

// 示例4: 带动画的仪表板
export function AnimatedDashboard() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 2000);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <LoadingSpinner variant="spinner" size="lg" text="加载数据中..." />
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
        <div className="container mx-auto">
          <FadeIn direction="down">
            <h1 className="text-4xl font-bold text-white mb-8">
              数据仪表板
            </h1>
          </FadeIn>

          {/* 统计卡片 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <FadeIn direction="up" delay={0.1}>
              <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
                <h3 className="text-gray-400 text-sm mb-2">总用户</h3>
                <p className="text-4xl font-bold text-white">12,345</p>
                <span className="text-green-400 text-sm">↑ 12%</span>
              </div>
            </FadeIn>

            <FadeIn direction="up" delay={0.2}>
              <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
                <h3 className="text-gray-400 text-sm mb-2">活跃项目</h3>
                <p className="text-4xl font-bold text-white">89</p>
                <span className="text-green-400 text-sm">↑ 5%</span>
              </div>
            </FadeIn>

            <FadeIn direction="up" delay={0.3}>
              <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
                <h3 className="text-gray-400 text-sm mb-2">完成任务</h3>
                <p className="text-4xl font-bold text-white">234</p>
                <span className="text-red-400 text-sm">↓ 3%</span>
              </div>
            </FadeIn>
          </div>

          {/* 图表区域 */}
          <FadeIn direction="up" delay={0.4}>
            <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
              <h2 className="text-2xl font-semibold text-white mb-4">
                项目进度
              </h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-300">前端开发</span>
                    <span className="text-gray-400">85%</span>
                  </div>
                  <ProgressBar progress={85} color="bg-blue-500" />
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-300">后端开发</span>
                    <span className="text-gray-400">65%</span>
                  </div>
                  <ProgressBar progress={65} color="bg-green-500" />
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-300">测试</span>
                    <span className="text-gray-400">40%</span>
                  </div>
                  <ProgressBar progress={40} color="bg-yellow-500" />
                </div>
              </div>
            </div>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
}
