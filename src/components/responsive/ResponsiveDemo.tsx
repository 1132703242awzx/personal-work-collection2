/**
 * 响应式设计演示组件
 * 展示所有响应式组件和用法
 */

import { useState } from 'react';
import {
  ResponsiveContainer,
  ResponsiveGrid,
  ResponsiveFlex,
  ResponsiveCard,
  ResponsiveNav,
  NavSpacer,
  ResponsiveTable,
  ResponsiveButton,
  ResponsiveInput,
  ResponsiveTextarea,
  ResponsiveSelect,
} from './index';
import ResponsiveImage from './ResponsiveImage';

export default function ResponsiveDemo() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    category: 'web',
    message: '',
    newsletter: false
  });

  // 模拟数据
  const tableData = [
    { id: 1, name: '项目 A', status: '进行中', progress: 75 },
    { id: 2, name: '项目 B', status: '已完成', progress: 100 },
    { id: 3, name: '项目 C', status: '计划中', progress: 0 }
  ];

  const tableColumns = [
    { key: 'id', title: 'ID', width: '80px' },
    { key: 'name', title: '项目名称' },
    { key: 'status', title: '状态', align: 'center' as const },
    { 
      key: 'progress', 
      title: '进度', 
      align: 'right' as const,
      render: (value: number) => `${value}%`
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      
      {/* 响应式导航栏 */}
      <ResponsiveNav
        logo={
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 md:w-10 md:h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
              R
            </div>
            <span className="text-white font-bold text-lg md:text-xl hidden sm:inline">
              响应式演示
            </span>
          </div>
        }
        items={[
          { label: '首页', onClick: () => console.log('首页') },
          { label: '组件', onClick: () => console.log('组件') },
          { label: '文档', onClick: () => console.log('文档') },
          { label: '关于', onClick: () => console.log('关于') }
        ]}
        rightContent={
          <ResponsiveButton variant="primary" size="sm">
            登录
          </ResponsiveButton>
        }
      />

      <NavSpacer />

      {/* 主内容区域 */}
      <ResponsiveContainer size="xl" className="py-6 md:py-8 lg:py-12">
        
        {/* 标题部分 */}
        <div className="text-center mb-8 md:mb-12">
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-3 md:mb-4">
            响应式设计系统
          </h1>
          <p className="text-base md:text-lg lg:text-xl text-gray-400">
            移动优先 · 触摸友好 · 自适应布局
          </p>
        </div>

        {/* 1. 响应式栅格 */}
        <section className="mb-8 md:mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 md:mb-6">
            1. 响应式栅格
          </h2>
          <ResponsiveGrid 
            cols={{ mobile: 1, tablet: 2, desktop: 3, wide: 4 }}
            gap="normal"
          >
            {[1, 2, 3, 4, 5, 6].map((num) => (
              <ResponsiveCard key={num} padding="normal" hover>
                <div className="text-center py-6">
                  <div className="w-12 h-12 md:w-16 md:h-16 bg-blue-600 rounded-full mx-auto mb-3 md:mb-4 flex items-center justify-center text-white font-bold text-lg md:text-2xl">
                    {num}
                  </div>
                  <h3 className="text-base md:text-lg font-semibold text-white">
                    卡片 {num}
                  </h3>
                  <p className="text-xs md:text-sm text-gray-400 mt-2">
                    自动适配不同屏幕尺寸
                  </p>
                </div>
              </ResponsiveCard>
            ))}
          </ResponsiveGrid>
        </section>

        {/* 2. 响应式按钮 */}
        <section className="mb-8 md:mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 md:mb-6">
            2. 响应式按钮
          </h2>
          <ResponsiveCard padding="large">
            <ResponsiveFlex direction="column-to-row" gap="normal" wrap>
              <ResponsiveButton variant="primary" size="sm">
                小按钮
              </ResponsiveButton>
              <ResponsiveButton variant="secondary" size="md">
                中等按钮
              </ResponsiveButton>
              <ResponsiveButton variant="outline" size="lg">
                大按钮
              </ResponsiveButton>
              <ResponsiveButton 
                variant="primary" 
                fullWidth 
                className="md:w-auto"
                icon={
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                }
              >
                带图标按钮
              </ResponsiveButton>
            </ResponsiveFlex>

            <div className="mt-6 flex gap-3">
              <ResponsiveButton variant="ghost" size="sm">
                ❤️ 喜欢
              </ResponsiveButton>
              <ResponsiveButton variant="ghost" size="sm">
                🔗 分享
              </ResponsiveButton>
              <ResponsiveButton variant="ghost" size="sm">
                ⭐ 收藏
              </ResponsiveButton>
            </div>
          </ResponsiveCard>
        </section>

        {/* 3. 响应式表单 */}
        <section className="mb-8 md:mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 md:mb-6">
            3. 响应式表单
          </h2>
          <ResponsiveCard padding="large">
            <form className="space-y-4 md:space-y-6">
              <ResponsiveGrid cols={{ mobile: 1, tablet: 2 }} gap="normal">
                <ResponsiveInput
                  label="姓名"
                  placeholder="请输入姓名"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  icon={
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  }
                />

                <ResponsiveInput
                  label="邮箱"
                  type="email"
                  placeholder="请输入邮箱"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  icon={
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  }
                />
              </ResponsiveGrid>

              <ResponsiveSelect
                label="项目类别"
                options={[
                  { value: 'web', label: 'Web应用' },
                  { value: 'mobile', label: '移动应用' },
                  { value: 'desktop', label: '桌面应用' }
                ]}
                value={formData.category}
                onChange={(e: any) => setFormData({ ...formData, category: e.target.value })}
              />

              <ResponsiveTextarea
                label="项目描述"
                placeholder="请输入项目详细描述..."
                rows={4}
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
              />

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="newsletter"
                  checked={formData.newsletter}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, newsletter: e.target.checked })}
                  className="w-5 h-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <label htmlFor="newsletter" className="text-sm md:text-base text-gray-700">
                  订阅邮件通知
                </label>
              </div>

              <ResponsiveFlex direction="column-to-row" gap="normal" justify="end">
                <ResponsiveButton variant="ghost" fullWidth className="md:w-auto">
                  取消
                </ResponsiveButton>
                <ResponsiveButton variant="primary" fullWidth className="md:w-auto">
                  提交
                </ResponsiveButton>
              </ResponsiveFlex>
            </form>
          </ResponsiveCard>
        </section>

        {/* 4. 响应式表格 */}
        <section className="mb-8 md:mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 md:mb-6">
            4. 响应式表格
          </h2>
          <ResponsiveCard padding="normal">
            <ResponsiveTable
              columns={tableColumns}
              data={tableData}
            />
          </ResponsiveCard>
          <p className="text-xs md:text-sm text-gray-400 mt-3">
            💡 提示: 在移动端可以左右滑动查看完整表格
          </p>
        </section>

        {/* 5. 响应式图片和头像 */}
        <section className="mb-8 md:mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 md:mb-6">
            5. 响应式图片和头像
          </h2>
          <ResponsiveCard padding="large">
            <div className="space-y-6">
              <div>
                <h3 className="text-lg md:text-xl font-semibold text-white mb-4">头像</h3>
                <ResponsiveFlex direction="row" gap="normal" align="center">
                  <div className="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center text-white font-semibold">
                    A
                  </div>
                  <div className="w-14 h-14 rounded-full bg-red-500 flex items-center justify-center text-white font-semibold">
                    B
                  </div>
                  <div className="w-20 h-20 rounded-full bg-gray-500 flex items-center justify-center text-white font-semibold">
                    C
                  </div>
                </ResponsiveFlex>
              </div>

              <div>
                <h3 className="text-lg md:text-xl font-semibold text-white mb-4">响应式图片</h3>
                <ResponsiveImage
                  src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800"
                  alt="示例图片"
                  aspectRatio="16/9"
                  rounded="lg"
                />
              </div>
            </div>
          </ResponsiveCard>
        </section>

        {/* 6. 响应式提示 */}
        <section className="mb-8 md:mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 md:mb-6">
            6. 设备信息
          </h2>
          <ResponsiveCard padding="large">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <span className="text-sm md:text-base text-gray-400">当前设备:</span>
                <span className="text-sm md:text-base text-white font-medium">
                  <span className="md:hidden">移动端 (&lt; 768px)</span>
                  <span className="hidden md:inline lg:hidden">平板 (768px - 1024px)</span>
                  <span className="hidden lg:inline">桌面端 (&gt; 1024px)</span>
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm md:text-base text-gray-400">屏幕宽度:</span>
                <span className="text-sm md:text-base text-white font-medium">
                  {typeof window !== 'undefined' ? `${window.innerWidth}px` : '-'}
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm md:text-base text-gray-400">触摸设备:</span>
                <span className="text-sm md:text-base text-white font-medium">
                  {typeof window !== 'undefined' && 'ontouchstart' in window ? '是' : '否'}
                </span>
              </div>
            </div>
          </ResponsiveCard>
        </section>

      </ResponsiveContainer>
    </div>
  );
}
