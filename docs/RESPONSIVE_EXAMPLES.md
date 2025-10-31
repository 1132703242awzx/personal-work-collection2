# 📚 响应式设计使用示例

## 🎯 完整应用示例

### 示例 1: 完整的响应式页面布局

```tsx
import {
  ResponsiveContainer,
  ResponsiveNav,
  NavSpacer,
  ResponsiveGrid,
  ResponsiveCard,
  ResponsiveButton,
  ResponsiveImage,
  ShowDesktopUp,
  HideMobile,
} from '@/components/responsive';
import { useResponsive } from '@/hooks/useResponsive';

function HomePage() {
  const { isMobile, isDesktop } = useResponsive();

  return (
    <>
      {/* 导航栏 */}
      <ResponsiveNav
        logo={
          <div className="flex items-center gap-2">
            <img src="/logo.svg" alt="Logo" className="h-8" />
            <span className="text-xl font-bold">我的应用</span>
          </div>
        }
        items={[
          { label: '首页', href: '/' },
          { label: '产品', href: '/products' },
          { label: '关于', href: '/about' },
          { label: '联系', href: '/contact' },
        ]}
        rightContent={
          <ResponsiveButton variant="primary" size={isMobile ? 'sm' : 'md'}>
            登录
          </ResponsiveButton>
        }
      />
      
      <NavSpacer />

      {/* 英雄区 */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <ResponsiveContainer size="lg">
          <div className="
            py-12 md:py-16 lg:py-24
            flex flex-col lg:flex-row
            items-center gap-8 lg:gap-12
          ">
            {/* 文字内容 */}
            <div className="flex-1 text-center lg:text-left">
              <h1 className="
                text-3xl md:text-4xl lg:text-5xl xl:text-6xl
                font-bold mb-4 md:mb-6
              ">
                打造现代化应用
              </h1>
              <p className="
                text-base md:text-lg lg:text-xl
                opacity-90 mb-6 md:mb-8
                max-w-2xl mx-auto lg:mx-0
              ">
                使用最新的响应式设计技术,为您的用户提供完美的体验
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <ResponsiveButton variant="primary" size="lg">
                  开始使用
                </ResponsiveButton>
                <ResponsiveButton variant="outline" size="lg">
                  了解更多
                </ResponsiveButton>
              </div>
            </div>

            {/* 图片 */}
            <div className="flex-1 w-full">
              <ResponsiveImage
                src="/hero.jpg"
                alt="英雄图"
                aspectRatio="16/9"
                rounded="lg"
                objectFit="cover"
              />
            </div>
          </div>
        </ResponsiveContainer>
      </section>

      {/* 特性展示 */}
      <section className="py-12 md:py-16 lg:py-24">
        <ResponsiveContainer>
          <h2 className="
            text-2xl md:text-3xl lg:text-4xl
            font-bold text-center mb-8 md:mb-12
          ">
            核心特性
          </h2>

          <ResponsiveGrid 
            cols={{ mobile: 1, tablet: 2, desktop: 3 }}
            gap="large"
          >
            {features.map((feature) => (
              <ResponsiveCard key={feature.id} hover>
                <div className="text-center">
                  <div className="
                    w-16 h-16 md:w-20 md:h-20
                    mx-auto mb-4 md:mb-6
                    bg-primary-100 rounded-full
                    flex items-center justify-center
                  ">
                    <feature.Icon className="w-8 h-8 md:w-10 md:h-10 text-primary-600" />
                  </div>
                  <h3 className="text-lg md:text-xl font-semibold mb-2 md:mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-sm md:text-base text-gray-600">
                    {feature.description}
                  </p>
                </div>
              </ResponsiveCard>
            ))}
          </ResponsiveGrid>
        </ResponsiveContainer>
      </section>

      {/* 桌面端才显示的复杂功能 */}
      <ShowDesktopUp>
        <section className="py-24 bg-gray-50">
          <ResponsiveContainer>
            <h2 className="text-4xl font-bold text-center mb-12">
              高级功能
            </h2>
            {/* 复杂的桌面端功能 */}
          </ResponsiveContainer>
        </section>
      </ShowDesktopUp>

      {/* 页脚 */}
      <footer className="bg-gray-900 text-white py-8 md:py-12">
        <ResponsiveContainer>
          <ResponsiveGrid 
            cols={{ mobile: 1, tablet: 2, desktop: 4 }}
            gap="large"
          >
            <div>
              <h4 className="text-lg font-semibold mb-4">关于我们</h4>
              <p className="text-sm text-gray-400">
                我们致力于打造最好的产品体验
              </p>
            </div>
            {/* 更多页脚内容 */}
          </ResponsiveGrid>
        </ResponsiveContainer>
      </footer>
    </>
  );
}
```

---

### 示例 2: 响应式表单页面

```tsx
import {
  ResponsiveContainer,
  ResponsiveGrid,
  ResponsiveInput,
  ResponsiveTextarea,
  ResponsiveSelect,
  ResponsiveButton,
} from '@/components/responsive';
import { useResponsive } from '@/hooks/useResponsive';
import { useState } from 'react';

function ContactForm() {
  const { isMobile } = useResponsive();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });

  return (
    <ResponsiveContainer size="md">
      <div className="py-8 md:py-12 lg:py-16">
        <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-6 md:mb-8">
          联系我们
        </h1>

        <form className="space-y-4 md:space-y-6">
          {/* 姓名和邮箱 */}
          <ResponsiveGrid cols={{ mobile: 1, tablet: 2 }} gap="normal">
            <ResponsiveInput
              label="姓名"
              placeholder="请输入您的姓名"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
            <ResponsiveInput
              label="邮箱"
              type="email"
              placeholder="your@email.com"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </ResponsiveGrid>

          {/* 主题 */}
          <ResponsiveSelect
            label="主题"
            value={formData.subject}
            onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
            required
          >
            <option value="">请选择主题</option>
            <option value="general">一般咨询</option>
            <option value="support">技术支持</option>
            <option value="sales">商务合作</option>
          </ResponsiveSelect>

          {/* 消息 */}
          <ResponsiveTextarea
            label="消息"
            placeholder="请输入您的消息..."
            rows={isMobile ? 4 : 6}
            value={formData.message}
            onChange={(e) => setFormData({ ...formData, message: e.target.value })}
            required
          />

          {/* 提交按钮 */}
          <ResponsiveButton
            variant="primary"
            size="lg"
            fullWidth
            type="submit"
          >
            发送消息
          </ResponsiveButton>
        </form>
      </div>
    </ResponsiveContainer>
  );
}
```

---

### 示例 3: 响应式数据展示

```tsx
import {
  ResponsiveContainer,
  ResponsiveTable,
  ResponsiveButton,
  ShowMobile,
  HideMobile,
} from '@/components/responsive';

function UsersPage() {
  const columns = [
    {
      key: 'avatar',
      title: '头像',
      width: '60px',
      render: (value: string) => (
        <img
          src={value}
          alt="Avatar"
          className="w-10 h-10 rounded-full"
        />
      ),
    },
    { key: 'name', title: '姓名' },
    { key: 'email', title: '邮箱' },
    {
      key: 'role',
      title: '角色',
      align: 'center' as const,
      render: (value: string) => (
        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
          {value}
        </span>
      ),
    },
    {
      key: 'actions',
      title: '操作',
      align: 'center' as const,
      render: () => (
        <div className="flex gap-2 justify-center">
          <ResponsiveButton variant="ghost" size="sm">
            编辑
          </ResponsiveButton>
          <ResponsiveButton variant="ghost" size="sm">
            删除
          </ResponsiveButton>
        </div>
      ),
    },
  ];

  return (
    <ResponsiveContainer>
      <div className="py-8">
        {/* 标题和操作 */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <h1 className="text-2xl md:text-3xl font-bold">
            用户管理
          </h1>
          <ResponsiveButton variant="primary">
            添加用户
          </ResponsiveButton>
        </div>

        {/* 桌面端提示 */}
        <HideMobile>
          <div className="mb-4 p-4 bg-blue-50 text-blue-700 rounded">
            提示: 您可以点击表格行进行编辑
          </div>
        </HideMobile>

        {/* 移动端提示 */}
        <ShowMobile>
          <div className="mb-4 p-4 bg-amber-50 text-amber-700 rounded text-sm">
            提示: 表格可以左右滑动查看更多内容
          </div>
        </ShowMobile>

        {/* 数据表格 */}
        <ResponsiveTable
          columns={columns}
          data={users}
          loading={loading}
        />
      </div>
    </ResponsiveContainer>
  );
}
```

---

### 示例 4: 使用 Hooks 进行条件渲染

```tsx
import { useResponsive, useMediaQuery } from '@/hooks/useResponsive';
import { useState, useEffect } from 'react';

function DashboardPage() {
  const { 
    isMobile, 
    isTablet, 
    isDesktop,
    deviceType,
    windowWidth 
  } = useResponsive();

  // 自定义媒体查询
  const isLandscape = useMediaQuery('(orientation: landscape)');
  const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)');

  // 根据设备类型调整布局
  const getLayoutColumns = () => {
    if (isMobile) return 1;
    if (isTablet) return 2;
    return 3;
  };

  // 根据屏幕宽度动态调整
  const getFontSize = () => {
    if (windowWidth < 768) return '14px';
    if (windowWidth < 1024) return '16px';
    return '18px';
  };

  return (
    <div style={{ fontSize: getFontSize() }}>
      <h1>仪表板</h1>
      
      <div className="mb-4 p-4 bg-gray-100 rounded">
        <p>当前设备: {deviceType}</p>
        <p>屏幕宽度: {windowWidth}px</p>
        <p>横屏模式: {isLandscape ? '是' : '否'}</p>
        <p>减少动画: {prefersReducedMotion ? '是' : '否'}</p>
      </div>

      {/* 根据设备类型渲染不同内容 */}
      {isMobile && (
        <MobileDashboard columns={1} />
      )}
      
      {isTablet && (
        <TabletDashboard columns={2} />
      )}
      
      {isDesktop && (
        <DesktopDashboard 
          columns={3} 
          enableAnimations={!prefersReducedMotion}
        />
      )}
    </div>
  );
}
```

---

### 示例 5: 响应式侧边栏布局

```tsx
import {
  ResponsiveContainer,
  ResponsiveFlex,
  ResponsiveButton,
  Show,
  Hide,
} from '@/components/responsive';
import { useResponsive } from '@/hooks/useResponsive';
import { useState } from 'react';

function AppLayout({ children }: { children: React.ReactNode }) {
  const { isMobile } = useResponsive();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen">
      {/* 移动端: 汉堡菜单按钮 */}
      <Show mobile>
        <div className="fixed top-4 left-4 z-50">
          <ResponsiveButton
            variant="ghost"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰ 菜单
          </ResponsiveButton>
        </div>
      </Show>

      <ResponsiveFlex direction="row" gap="none">
        {/* 侧边栏 */}
        <aside className={`
          ${isMobile ? 'fixed inset-y-0 left-0 z-40' : 'relative'}
          ${isMobile && !sidebarOpen ? '-translate-x-full' : 'translate-x-0'}
          w-64 bg-gray-900 text-white
          transition-transform duration-300
        `}>
          <div className="p-6">
            <h2 className="text-xl font-bold mb-6">导航</h2>
            <nav className="space-y-2">
              <a href="/" className="block py-2 px-4 rounded hover:bg-gray-800">
                首页
              </a>
              <a href="/dashboard" className="block py-2 px-4 rounded hover:bg-gray-800">
                仪表板
              </a>
              <a href="/settings" className="block py-2 px-4 rounded hover:bg-gray-800">
                设置
              </a>
            </nav>
          </div>
        </aside>

        {/* 移动端: 遮罩层 */}
        <Show mobile>
          {sidebarOpen && (
            <div
              className="fixed inset-0 bg-black bg-opacity-50 z-30"
              onClick={() => setSidebarOpen(false)}
            />
          )}
        </Show>

        {/* 主内容区 */}
        <main className="flex-1 min-w-0">
          <ResponsiveContainer>
            {children}
          </ResponsiveContainer>
        </main>
      </ResponsiveFlex>
    </div>
  );
}
```

---

### 示例 6: 响应式卡片网格(高级)

```tsx
import {
  ResponsiveGrid,
  ResponsiveCard,
  ResponsiveImage,
  ResponsiveButton,
  Show,
} from '@/components/responsive';
import { useResponsive } from '@/hooks/useResponsive';

function ProductGrid({ products }: { products: Product[] }) {
  const { isMobile, isTablet, isDesktop } = useResponsive();

  // 根据设备类型动态调整显示数量
  const getVisibleCount = () => {
    if (isMobile) return 4;
    if (isTablet) return 6;
    return 12;
  };

  const [visibleCount, setVisibleCount] = useState(getVisibleCount());

  return (
    <div>
      <ResponsiveGrid
        cols={{
          mobile: 1,
          tablet: 2,
          desktop: 3,
          wide: 4,
        }}
        gap="large"
      >
        {products.slice(0, visibleCount).map((product) => (
          <ResponsiveCard key={product.id} hover>
            {/* 产品图片 */}
            <ResponsiveImage
              src={product.image}
              alt={product.name}
              aspectRatio="4/3"
              objectFit="cover"
              rounded="t-lg"
              lazy
            />

            {/* 产品信息 */}
            <div className="p-4 md:p-6">
              {/* 标题 */}
              <h3 className="
                text-base md:text-lg lg:text-xl
                font-semibold mb-2
                line-clamp-2
              ">
                {product.name}
              </h3>

              {/* 描述 - 桌面端显示 */}
              <Hide mobile tablet>
                <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                  {product.description}
                </p>
              </Hide>

              {/* 价格和评分 */}
              <div className="flex items-center justify-between mb-4">
                <span className="text-xl md:text-2xl font-bold text-primary-600">
                  ¥{product.price}
                </span>
                <div className="flex items-center gap-1">
                  <span className="text-yellow-400">★</span>
                  <span className="text-sm md:text-base">
                    {product.rating}
                  </span>
                </div>
              </div>

              {/* 操作按钮 */}
              <ResponsiveButton
                variant="primary"
                fullWidth
                size={isMobile ? 'sm' : 'md'}
              >
                {isMobile ? '购买' : '添加到购物车'}
              </ResponsiveButton>
            </div>
          </ResponsiveCard>
        ))}
      </ResponsiveGrid>

      {/* 加载更多按钮 */}
      {visibleCount < products.length && (
        <div className="text-center mt-8">
          <ResponsiveButton
            variant="outline"
            size="lg"
            onClick={() => setVisibleCount(visibleCount + getVisibleCount())}
          >
            加载更多
          </ResponsiveButton>
        </div>
      )}
    </div>
  );
}
```

---

## 🎨 CSS 技巧

### 技巧 1: 响应式排版

```tsx
// 使用 Tailwind 的响应式字体类
<h1 className="
  text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl
  leading-tight sm:leading-tight md:leading-tight
  tracking-tight
">
  响应式标题
</h1>

// 或使用 clamp() 函数(在 CSS 中)
<h1 style={{
  fontSize: 'clamp(1.5rem, 5vw, 4rem)'
}}>
  流式标题
</h1>
```

### 技巧 2: 容器查询 (实验性)

```css
/* 在 CSS Module 或全局 CSS 中 */
.container {
  container-type: inline-size;
}

.card {
  padding: 1rem;
}

@container (min-width: 400px) {
  .card {
    padding: 2rem;
  }
}
```

### 技巧 3: 响应式间距

```tsx
// 使用响应式 padding/margin
<div className="
  p-4 md:p-6 lg:p-8 xl:p-12
  m-2 md:m-4 lg:m-6
  space-y-4 md:space-y-6 lg:space-y-8
">
  {/* 内容 */}
</div>
```

---

## 🚀 总结

这些示例展示了如何:
- ✅ 构建完整的响应式页面
- ✅ 使用响应式组件库
- ✅ 利用 hooks 进行条件渲染
- ✅ 实现复杂的响应式布局
- ✅ 优化移动端体验

根据这些示例,您可以快速构建出专业的响应式应用! 🎉
