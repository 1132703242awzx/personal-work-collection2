/**
 * 动画效果演示组件
 * 展示所有动画组件的使用示例
 */

import { useState } from 'react';
import FadeIn from './FadeIn';
import AnimatedList from './AnimatedList';
import CardStack from './CardStack';
import AnimatedButton, { FloatingActionButton, IconButton } from './AnimatedButton';
import AnimatedInput, { AnimatedTextarea, AnimatedSwitch } from './AnimatedInput';
import FloatingCard, { StatCard } from './FloatingCard';
import Modal, { ConfirmDialog } from './Modal';
import LoadingSpinner, { InlineLoading } from './LoadingSpinner';
import Skeleton, { SkeletonText, SkeletonCard } from './Skeleton';
import ProgressBar, { StepProgress, CircularProgress } from './ProgressBar';

export default function AnimationDemo() {
  const [modalOpen, setModalOpen] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(45);
  const [switchState, setSwitchState] = useState(false);

  const listItems = [
    'React 19 - 最新版本',
    'TypeScript 5.9 - 类型安全',
    'Tailwind CSS 3.4 - 样式框架',
    'Framer Motion - 动画库',
    'Redux Toolkit - 状态管理'
  ];

  const cards = [
    { title: '项目', count: 12, icon: '📁' },
    { title: '任务', count: 45, icon: '✅' },
    { title: '团队', count: 8, icon: '👥' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto space-y-12">
        
        {/* 标题 */}
        <FadeIn direction="up">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-white mb-4">
              动画效果演示
            </h1>
            <p className="text-xl text-gray-400">
              探索所有可用的动画组件和交互效果
            </p>
          </div>
        </FadeIn>

        {/* 基础动画 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">1. 基础动画</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FadeIn direction="none">
              <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold text-white mb-2">淡入</h3>
                <p className="text-gray-400">简单的淡入效果</p>
              </div>
            </FadeIn>

            <FadeIn direction="up" delay={0.1}>
              <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold text-white mb-2">上滑淡入</h3>
                <p className="text-gray-400">从下方滑入并淡入</p>
              </div>
            </FadeIn>

            <FadeIn direction="down" delay={0.2}>
              <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold text-white mb-2">下滑淡入</h3>
                <p className="text-gray-400">从上方滑入并淡入</p>
              </div>
            </FadeIn>
          </div>
        </section>

        {/* 列表动画 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">2. 列表动画</h2>
          
          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
            <h3 className="text-xl font-semibold text-white mb-4">技术栈</h3>
            <AnimatedList stagger="normal">
              {listItems.map((item, index) => (
                <div 
                  key={index}
                  className="py-3 px-4 bg-slate-700/50 rounded-lg mb-2 last:mb-0"
                >
                  <p className="text-gray-200">{item}</p>
                </div>
              ))}
            </AnimatedList>
          </div>
        </section>

        {/* 卡片堆叠 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">3. 卡片堆叠动画</h2>
          
          <CardStack stagger="fast">
            {cards.map((card, index) => (
              <FloatingCard key={index} gradient>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm mb-1">{card.title}</p>
                    <h3 className="text-3xl font-bold text-white">{card.count}</h3>
                  </div>
                  <span className="text-4xl">{card.icon}</span>
                </div>
              </FloatingCard>
            ))}
          </CardStack>
        </section>

        {/* 统计卡片 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">4. 统计卡片</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard
              title="总用户"
              value="12,345"
              icon="👤"
              trend="up"
              trendValue="↑ 12%"
            />
            <StatCard
              title="活跃项目"
              value="89"
              icon="🚀"
              trend="up"
              trendValue="↑ 5%"
            />
            <StatCard
              title="完成任务"
              value="234"
              icon="✅"
              trend="down"
              trendValue="↓ 3%"
            />
          </div>
        </section>

        {/* 按钮动画 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">5. 按钮动画</h2>
          
          <div className="flex flex-wrap gap-4">
            <AnimatedButton variant="primary" size="lg">
              主要按钮
            </AnimatedButton>
            <AnimatedButton variant="secondary" size="md">
              次要按钮
            </AnimatedButton>
            <AnimatedButton variant="outline" size="md">
              轮廓按钮
            </AnimatedButton>
            <AnimatedButton variant="ghost" size="md">
              幽灵按钮
            </AnimatedButton>
            <AnimatedButton variant="primary" size="md" loading>
              加载中...
            </AnimatedButton>
            <AnimatedButton variant="primary" size="md" disabled>
              禁用状态
            </AnimatedButton>
          </div>

          <div className="flex gap-4">
            <FloatingActionButton 
              onClick={() => alert('FAB clicked!')}
              icon={
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              }
            />

            <IconButton 
              icon={
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              }
              tooltip="设置"
            />
          </div>
        </section>

        {/* 表单输入 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">6. 表单输入动画</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <AnimatedInput 
              label="用户名" 
              placeholder="输入用户名"
              icon={
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              }
            />

            <AnimatedInput 
              label="邮箱" 
              type="email"
              placeholder="输入邮箱"
              error="邮箱格式不正确"
              icon={
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              }
            />
          </div>

          <AnimatedTextarea 
            label="项目描述" 
            placeholder="输入项目详细描述..."
            rows={4}
          />

          <AnimatedSwitch 
            checked={switchState}
            onChange={setSwitchState}
            label="启用通知"
          />
        </section>

        {/* 加载状态 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">7. 加载状态</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 flex flex-col items-center">
              <LoadingSpinner variant="spinner" size="lg" />
              <p className="text-gray-400 mt-4">旋转</p>
            </div>

            <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 flex flex-col items-center">
              <LoadingSpinner variant="dots" size="lg" />
              <p className="text-gray-400 mt-4">点</p>
            </div>

            <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 flex flex-col items-center">
              <LoadingSpinner variant="pulse" size="lg" />
              <p className="text-gray-400 mt-4">脉冲</p>
            </div>

            <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 flex flex-col items-center">
              <LoadingSpinner variant="bars" size="lg" />
              <p className="text-gray-400 mt-4">条形</p>
            </div>
          </div>

          <div className="flex gap-4">
            <AnimatedButton 
              variant="primary"
              onClick={() => {
                setLoading(true);
                setTimeout(() => setLoading(false), 2000);
              }}
            >
              {loading ? <InlineLoading text="处理中..." /> : '触发加载'}
            </AnimatedButton>
          </div>
        </section>

        {/* 骨架屏 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">8. 骨架屏</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <SkeletonCard />
            <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
              <Skeleton variant="circular" width="60px" height="60px" className="mb-4" />
              <SkeletonText lines={3} />
            </div>
          </div>
        </section>

        {/* 进度条 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">9. 进度指示器</h2>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-white">项目进度</span>
                <span className="text-gray-400">{progress}%</span>
              </div>
              <ProgressBar progress={progress} color="blue" />
              <div className="flex gap-2 mt-4">
                <AnimatedButton 
                  variant="outline" 
                  size="sm"
                  onClick={() => setProgress(Math.max(0, progress - 10))}
                >
                  -10%
                </AnimatedButton>
                <AnimatedButton 
                  variant="outline" 
                  size="sm"
                  onClick={() => setProgress(Math.min(100, progress + 10))}
                >
                  +10%
                </AnimatedButton>
              </div>
            </div>

            <StepProgress 
              steps={[
                { label: '需求分析', completed: true },
                { label: '设计方案', completed: true },
                { label: '开发实现', completed: false },
                { label: '测试部署', completed: false }
              ]}
            />

            <div className="flex gap-6">
              <CircularProgress progress={75} size={120} />
              <CircularProgress progress={45} size={120} />
              <CircularProgress progress={90} size={120} />
            </div>
          </div>
        </section>

        {/* 模态框 */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold text-white">10. 模态框动画</h2>
          
          <div className="flex gap-4">
            <AnimatedButton 
              variant="primary"
              onClick={() => setModalOpen(true)}
            >
              打开模态框
            </AnimatedButton>

            <AnimatedButton 
              variant="secondary"
              onClick={() => setConfirmOpen(true)}
            >
              打开确认对话框
            </AnimatedButton>
          </div>

          <Modal 
            isOpen={modalOpen}
            onClose={() => setModalOpen(false)}
            title="示例模态框"
            size="md"
          >
            <div className="space-y-4">
              <p className="text-gray-300">
                这是一个带动画效果的模态框。背景遮罩有淡入效果,内容有缩放+滑入效果。
              </p>
              <AnimatedInput 
                label="输入内容" 
                placeholder="在模态框中输入..."
              />
              <div className="flex justify-end gap-3">
                <AnimatedButton 
                  variant="outline"
                  onClick={() => setModalOpen(false)}
                >
                  取消
                </AnimatedButton>
                <AnimatedButton 
                  variant="primary"
                  onClick={() => setModalOpen(false)}
                >
                  确认
                </AnimatedButton>
              </div>
            </div>
          </Modal>

          <ConfirmDialog
            isOpen={confirmOpen}
            onClose={() => setConfirmOpen(false)}
            onConfirm={() => alert('已确认!')}
            title="确认操作"
            message="您确定要执行此操作吗?此操作不可撤销。"
            type="warning"
          />
        </section>

      </div>
    </div>
  );
}
