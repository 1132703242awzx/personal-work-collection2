# 🚀 响应式设计快速开始

## 📋 5分钟快速上手

### 步骤 1: 导入组件

```tsx
import {
  ResponsiveContainer,
  ResponsiveNav,
  ResponsiveButton,
  ResponsiveInput,
  ResponsiveGrid
} from '@/components/responsive';
```

### 步骤 2: 创建基础布局

```tsx
function App() {
  return (
    <>
      {/* 导航栏 */}
      <ResponsiveNav
        logo={<Logo />}
        items={[
          { label: '首页', onClick: () => navigate('/') },
          { label: '关于', onClick: () => navigate('/about') }
        ]}
      />
      
      {/* 主内容 */}
      <ResponsiveContainer size="lg">
        <h1 className="text-2xl md:text-3xl lg:text-4xl">
          欢迎使用
        </h1>
      </ResponsiveContainer>
    </>
  );
}
```

### 步骤 3: 添加响应式表单

```tsx
<ResponsiveGrid cols={{ mobile: 1, tablet: 2, desktop: 3 }}>
  <ResponsiveInput label="姓名" placeholder="请输入姓名" />
  <ResponsiveInput label="邮箱" type="email" />
  <ResponsiveInput label="电话" type="tel" />
</ResponsiveGrid>

<ResponsiveButton variant="primary" fullWidth>
  提交
</ResponsiveButton>
```

### 步骤 4: 完成! 🎉

现在你的应用已经具备完整的响应式设计了!

---

## 📱 常用场景

### 场景 1: 响应式卡片网格

```tsx
<ResponsiveGrid 
  cols={{ mobile: 1, tablet: 2, desktop: 3, wide: 4 }}
  gap="large"
>
  {products.map(product => (
    <div key={product.id} className="
      p-4 md:p-6
      bg-white rounded-lg shadow-md
      hover:shadow-xl transition
    ">
      <ResponsiveImage
        src={product.image}
        aspectRatio="16/9"
        lazy
      />
      <h3 className="text-lg md:text-xl mt-4">
        {product.name}
      </h3>
      <p className="text-sm md:text-base text-gray-600">
        {product.description}
      </p>
      <ResponsiveButton variant="primary" fullWidth>
        购买
      </ResponsiveButton>
    </div>
  ))}
</ResponsiveGrid>
```

### 场景 2: 移动端友好的表格

```tsx
<ResponsiveTable
  columns={[
    { key: 'id', title: 'ID', width: '80px' },
    { key: 'name', title: '名称' },
    { key: 'status', title: '状态', align: 'center' },
    { key: 'date', title: '日期' }
  ]}
  data={tableData}
/>
```

### 场景 3: 自适应侧边栏布局

```tsx
<ResponsiveFlex direction="column-to-row" gap="large">
  {/* 侧边栏 */}
  <aside className="w-full lg:w-64 shrink-0">
    <ResponsiveNav
      items={sidebarItems}
      orientation="vertical"
    />
  </aside>
  
  {/* 主内容区 */}
  <main className="flex-1 min-w-0">
    <ResponsiveContainer>
      {children}
    </ResponsiveContainer>
  </main>
</ResponsiveFlex>
```

### 场景 4: 响应式英雄区

```tsx
<section className="
  py-12 md:py-16 lg:py-24
  px-4 md:px-6 lg:px-8
">
  <ResponsiveContainer>
    <ResponsiveFlex 
      direction="column-to-row" 
      align="center"
      gap="large"
    >
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
          text-gray-600 mb-6 md:mb-8
        ">
          响应式设计,完美适配所有设备
        </p>
        <ResponsiveFlex 
          justify="center lg:justify-start" 
          gap="normal"
        >
          <ResponsiveButton variant="primary" size="lg">
            开始使用
          </ResponsiveButton>
          <ResponsiveButton variant="outline" size="lg">
            了解更多
          </ResponsiveButton>
        </ResponsiveFlex>
      </div>
      
      {/* 图片 */}
      <div className="flex-1">
        <ResponsiveImage
          src="hero.jpg"
          aspectRatio="16/9"
          rounded="lg"
        />
      </div>
    </ResponsiveFlex>
  </ResponsiveContainer>
</section>
```

---

## 🎨 Tailwind 响应式工具类速查

### 基础语法

```tsx
// 移动优先: 默认 → md → lg → xl
<div className="text-sm md:text-base lg:text-lg xl:text-xl">
```

### 常用类

```tsx
// 宽度
w-full              // 100%
md:w-1/2           // 50% (平板+)
lg:w-1/3           // 33.33% (桌面+)

// 显示/隐藏
hidden md:block     // 移动隐藏,平板+显示
block md:hidden     // 移动显示,平板+隐藏

// 间距
p-4 md:p-6 lg:p-8   // padding: 16→24→32px
m-2 md:m-4 lg:m-6   // margin: 8→16→24px
gap-4 md:gap-6      // grid/flex gap: 16→24px

// 字体
text-sm md:text-base lg:text-lg  // 14→16→18px
text-center md:text-left         // 居中→左对齐

// 布局
flex-col md:flex-row            // 纵向→横向
grid-cols-1 md:grid-cols-2 lg:grid-cols-3  // 1→2→3列

// 高度
h-auto md:h-screen              // 自动→全屏高
min-h-screen md:min-h-0         // 最小全屏→无限制
```

---

## 🛠️ 实用代码片段

### 代码片段 1: 响应式导航 + 内容

```tsx
import {
  ResponsiveNav,
  NavSpacer,
  ResponsiveContainer
} from '@/components/responsive';

function Layout({ children }) {
  return (
    <>
      <ResponsiveNav
        logo={<Logo />}
        items={[
          { label: '首页', href: '/' },
          { label: '产品', href: '/products' },
          { label: '关于', href: '/about' }
        ]}
        rightContent={
          <ResponsiveButton variant="primary">
            登录
          </ResponsiveButton>
        }
      />
      <NavSpacer />
      <ResponsiveContainer>
        {children}
      </ResponsiveContainer>
    </>
  );
}
```

### 代码片段 2: 响应式表单

```tsx
import {
  ResponsiveGrid,
  ResponsiveInput,
  ResponsiveTextarea,
  ResponsiveSelect,
  ResponsiveButton
} from '@/components/responsive';

function ContactForm() {
  return (
    <form className="space-y-6">
      <ResponsiveGrid cols={{ mobile: 1, tablet: 2 }} gap="normal">
        <ResponsiveInput
          label="姓名"
          placeholder="张三"
          required
        />
        <ResponsiveInput
          label="邮箱"
          type="email"
          placeholder="zhangsan@example.com"
          required
        />
      </ResponsiveGrid>
      
      <ResponsiveInput
        label="主题"
        placeholder="请输入主题"
        required
      />
      
      <ResponsiveTextarea
        label="消息"
        placeholder="请输入您的消息..."
        rows={5}
        required
      />
      
      <ResponsiveButton
        variant="primary"
        size="lg"
        fullWidth
        type="submit"
      >
        提交
      </ResponsiveButton>
    </form>
  );
}
```

### 代码片段 3: 响应式卡片列表

```tsx
import {
  ResponsiveGrid,
  ResponsiveCard,
  ResponsiveImage,
  ResponsiveButton
} from '@/components/responsive';

function ProductList({ products }) {
  return (
    <ResponsiveGrid 
      cols={{ mobile: 1, tablet: 2, desktop: 3, wide: 4 }}
      gap="large"
    >
      {products.map(product => (
        <ResponsiveCard key={product.id} hover>
          <ResponsiveImage
            src={product.image}
            alt={product.name}
            aspectRatio="4/3"
            lazy
            rounded="t-lg"
          />
          <div className="p-4 md:p-6">
            <h3 className="text-lg md:text-xl font-semibold mb-2">
              {product.name}
            </h3>
            <p className="text-sm md:text-base text-gray-600 mb-4">
              {product.description}
            </p>
            <div className="flex items-center justify-between">
              <span className="text-xl md:text-2xl font-bold text-primary-600">
                ¥{product.price}
              </span>
              <ResponsiveButton variant="primary">
                购买
              </ResponsiveButton>
            </div>
          </div>
        </ResponsiveCard>
      ))}
    </ResponsiveGrid>
  );
}
```

### 代码片段 4: 响应式数据表格

```tsx
import { ResponsiveTable } from '@/components/responsive';

function UserTable() {
  const columns = [
    { 
      key: 'avatar', 
      title: '头像',
      width: '60px',
      render: (value) => (
        <ResponsiveAvatar src={value} size="sm" />
      )
    },
    { key: 'name', title: '姓名' },
    { key: 'email', title: '邮箱' },
    { 
      key: 'status', 
      title: '状态',
      align: 'center',
      render: (value) => (
        <span className={`
          px-2 py-1 rounded-full text-xs md:text-sm
          ${value === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}
        `}>
          {value === 'active' ? '活跃' : '停用'}
        </span>
      )
    },
    {
      key: 'actions',
      title: '操作',
      align: 'center',
      render: (_, row) => (
        <ResponsiveFlex gap="small" justify="center">
          <ResponsiveIconButton
            icon={<EditIcon />}
            label="编辑"
            size="sm"
          />
          <ResponsiveIconButton
            icon={<DeleteIcon />}
            label="删除"
            variant="danger"
            size="sm"
          />
        </ResponsiveFlex>
      )
    }
  ];

  return <ResponsiveTable columns={columns} data={users} />;
}
```

---

## 💡 常见问题

### Q1: 如何隐藏/显示某个元素?

```tsx
// 移动端隐藏
<div className="hidden md:block">
  桌面端内容
</div>

// 桌面端隐藏
<div className="block md:hidden">
  移动端内容
</div>
```

### Q2: 如何改变布局方向?

```tsx
// 移动纵向 → 桌面横向
<div className="flex flex-col md:flex-row">
  <div>左侧</div>
  <div>右侧</div>
</div>
```

### Q3: 如何调整元素顺序?

```tsx
<div className="flex flex-col md:flex-row">
  <div className="order-2 md:order-1">第一个(桌面)</div>
  <div className="order-1 md:order-2">第二个(桌面)</div>
</div>
```

### Q4: 如何实现响应式字体?

```tsx
<h1 className="text-2xl md:text-3xl lg:text-4xl xl:text-5xl">
  标题
</h1>
```

### Q5: 移动端如何处理长表格?

```tsx
// 方案1: 水平滚动
<ResponsiveTable columns={columns} data={data} />

// 方案2: 卡片视图
<ResponsiveCardTable columns={columns} data={data} />
```

---

## 🎯 下一步

1. 查看 [完整文档](./RESPONSIVE.md)
2. 浏览 [组件演示](../src/components/responsive/ResponsiveDemo.tsx)
3. 阅读 [最佳实践](./RESPONSIVE.md#最佳实践)
4. 开始构建你的响应式应用! 🚀

---

## 📞 需要帮助?

- 查看源代码: `src/components/responsive/`
- 配置文件: `src/config/responsive.ts`
- 演示页面: `ResponsiveDemo.tsx`
