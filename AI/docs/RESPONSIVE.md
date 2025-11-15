# 📱 响应式设计系统文档

## 🎯 概述

本响应式设计系统采用**移动优先**策略,提供了一套完整的响应式组件和工具,确保应用在所有设备上都有出色的用户体验。

## 📐 断点设计

### 标准断点

```typescript
移动端 (Mobile):    < 768px   - sm以下
平板 (Tablet):     768px - 1024px - md
桌面端 (Desktop):   > 1024px  - lg
超宽屏 (Wide):      > 1280px  - xl (可选)
```

### Tailwind CSS 断点前缀

```css
/* 默认样式 - 移动端 */
.class

/* 平板及以上 */
@media (min-width: 768px) {
  md:.class
}

/* 桌面及以上 */
@media (min-width: 1024px) {
  lg:.class
}

/* 超宽屏 */
@media (min-width: 1280px) {
  xl:.class
}
```

## 🎨 核心原则

### 1. 移动优先
- 先设计移动端界面
- 使用 `md:` `lg:` 逐步增强
- 确保核心功能在小屏幕可用

### 2. 触摸友好
- 最小触摸目标: **44×44px**
- 按钮间距: 至少 **8px**
- 表单输入高度: 至少 **44px**

### 3. 可读性
- 移动端字体: 14-16px
- 桌面端字体: 16-18px
- 行高: 1.5-1.8
- 段落最大宽度: 65-75字符

### 4. 性能优化
- 响应式图片
- 懒加载
- 移动端减少动画
- 按需加载组件

## 📦 组件系统

### 1. 容器组件

#### ResponsiveContainer
提供一致的容器宽度和内边距。

```tsx
import { ResponsiveContainer } from '@/components/responsive';

<ResponsiveContainer size="lg" padding>
  {/* 内容 */}
</ResponsiveContainer>
```

**Props:**
- `size`: 'sm' | 'md' | 'lg' | 'xl' | 'full'
- `padding`: boolean (默认: true)
- `className`: string

**尺寸对照:**
- sm: max-w-2xl (672px)
- md: max-w-4xl (896px)
- lg: max-w-6xl (1152px)
- xl: max-w-7xl (1280px)
- full: max-w-full

---

#### ResponsiveGrid
响应式栅格布局。

```tsx
import { ResponsiveGrid } from '@/components/responsive';

<ResponsiveGrid 
  cols={{ mobile: 1, tablet: 2, desktop: 3, wide: 4 }}
  gap="normal"
>
  {items.map(item => <Card key={item.id} {...item} />)}
</ResponsiveGrid>
```

**Props:**
- `cols`: { mobile?, tablet?, desktop?, wide? }
- `gap`: 'small' | 'normal' | 'large'
- `className`: string

---

#### ResponsiveFlex
响应式弹性布局。

```tsx
import { ResponsiveFlex } from '@/components/responsive';

<ResponsiveFlex 
  direction="column-to-row"
  align="center"
  justify="between"
  gap="normal"
>
  {children}
</ResponsiveFlex>
```

**Props:**
- `direction`: 'column-to-row' | 'row-to-column' | 'column' | 'row'
- `align`: 'start' | 'center' | 'end' | 'stretch'
- `justify`: 'start' | 'center' | 'end' | 'between' | 'around'
- `gap`: 'small' | 'normal' | 'large'
- `wrap`: boolean

---

### 2. 导航组件

#### ResponsiveNav
响应式导航栏,移动端显示汉堡菜单。

```tsx
import { ResponsiveNav, NavSpacer } from '@/components/responsive';

<ResponsiveNav
  logo={<Logo />}
  items={[
    { label: '首页', onClick: () => {} },
    { label: '关于', onClick: () => {} }
  ]}
  rightContent={<Button>登录</Button>}
/>

<NavSpacer /> {/* 避免内容被导航遮挡 */}
```

**Props:**
- `logo`: ReactNode
- `items`: Array<{ label, href?, onClick?, icon? }>
- `rightContent`: ReactNode

**特性:**
- 移动端: 侧边滑入菜单
- 桌面端: 顶部水平菜单
- 滚动时添加背景
- 菜单打开时禁止背景滚动

---

### 3. 表格组件

#### ResponsiveTable
移动端水平滚动的响应式表格。

```tsx
import { ResponsiveTable } from '@/components/responsive';

const columns = [
  { key: 'id', title: 'ID', width: '80px' },
  { key: 'name', title: '名称' },
  { 
    key: 'status', 
    title: '状态',
    align: 'center',
    render: (value, row) => <Badge>{value}</Badge>
  }
];

<ResponsiveTable
  columns={columns}
  data={data}
  loading={false}
  emptyText="暂无数据"
/>
```

**Props:**
- `columns`: Array<Column>
- `data`: Array<any>
- `loading`: boolean
- `emptyText`: string

**Column 类型:**
```typescript
interface Column {
  key: string;
  title: string;
  width?: string;
  align?: 'left' | 'center' | 'right';
  render?: (value, row, index) => ReactNode;
}
```

---

#### ResponsiveCardTable
移动端卡片式表格(替代方案)。

```tsx
import { ResponsiveCardTable } from '@/components/responsive';

<ResponsiveCardTable
  columns={columns}
  data={data}
  keyExtractor={(item) => item.id}
/>
```

---

### 4. 按钮组件

#### ResponsiveButton
触摸友好的响应式按钮。

```tsx
import { ResponsiveButton } from '@/components/responsive';

<ResponsiveButton
  variant="primary"
  size="md"
  fullWidth={false}
  loading={false}
  icon={<Icon />}
  iconPosition="left"
>
  提交
</ResponsiveButton>
```

**Variants:**
- `primary`: 主要按钮 (蓝色)
- `secondary`: 次要按钮 (灰色)
- `outline`: 轮廓按钮
- `ghost`: 幽灵按钮
- `danger`: 危险按钮 (红色)

**Sizes:**
- `sm`: min-h-[44px] - 移动端友好
- `md`: min-h-[48px] (默认)
- `lg`: min-h-[52px]

---

#### ResponsiveIconButton
图标按钮。

```tsx
import { ResponsiveIconButton } from '@/components/responsive';

<ResponsiveIconButton
  icon={<HeartIcon />}
  label="喜欢"
  variant="ghost"
  size="md"
/>
```

**Sizes:**
- `sm`: 44×44px
- `md`: 48×48px
- `lg`: 56×56px

---

### 5. 表单组件

#### ResponsiveInput
响应式输入框。

```tsx
import { ResponsiveInput } from '@/components/responsive';

<ResponsiveInput
  label="邮箱"
  placeholder="请输入邮箱"
  error="邮箱格式不正确"
  helperText="我们不会分享您的邮箱"
  icon={<EmailIcon />}
  iconPosition="left"
  fullWidth
  required
/>
```

---

#### ResponsiveTextarea
文本域组件。

```tsx
import { ResponsiveTextarea } from '@/components/responsive';

<ResponsiveTextarea
  label="描述"
  placeholder="请输入描述..."
  rows={4}
  required
/>
```

---

#### ResponsiveSelect
选择框组件。

```tsx
import { ResponsiveSelect } from '@/components/responsive';

<ResponsiveSelect
  label="类别"
  options={[
    { value: 'web', label: 'Web应用' },
    { value: 'mobile', label: '移动应用' }
  ]}
/>
```

---

#### ResponsiveCheckbox
复选框组件。

```tsx
import { ResponsiveCheckbox } from '@/components/responsive';

<ResponsiveCheckbox
  label="我同意服务条款"
  checked={agreed}
  onChange={(e) => setAgreed(e.target.checked)}
/>
```

---

#### ResponsiveRadioGroup
单选按钮组。

```tsx
import { ResponsiveRadioGroup } from '@/components/responsive';

<ResponsiveRadioGroup
  label="选择类型"
  options={[
    { value: 'a', label: '选项 A' },
    { value: 'b', label: '选项 B' }
  ]}
  name="type"
  value={selectedType}
  onChange={setSelectedType}
  orientation="horizontal"
/>
```

---

### 6. 图片组件

#### ResponsiveImage
响应式图片,支持懒加载和占位符。

```tsx
import ResponsiveImage from '@/components/responsive/ResponsiveImage';

<ResponsiveImage
  src="image.jpg"
  alt="描述"
  srcSet="image-small.jpg 480w, image-large.jpg 800w"
  sizes="(max-width: 768px) 100vw, 50vw"
  aspectRatio="16/9"
  objectFit="cover"
  lazy
  rounded="md"
/>
```

**Props:**
- `aspectRatio`: '1/1' | '4/3' | '16/9' | '21/9'
- `objectFit`: 'cover' | 'contain' | 'fill'
- `lazy`: boolean
- `rounded`: 'none' | 'sm' | 'md' | 'lg' | 'full'

---

#### ResponsiveAvatar
头像组件。

```tsx
import { ResponsiveAvatar } from '@/components/responsive/ResponsiveImage';

<ResponsiveAvatar
  src="avatar.jpg"
  alt="用户名"
  size="md"
  status="online"
  fallback="U"
/>
```

**Sizes:**
- `sm`: 8/10 (32/40px)
- `md`: 12/14 (48/56px)
- `lg`: 16/20 (64/80px)
- `xl`: 24/32 (96/128px)

**Status:**
- `online`: 绿色
- `offline`: 灰色
- `busy`: 红色

---

## 🛠️ 工具函数

### useResponsive Hook

```tsx
import { useResponsive } from '@/config/responsive';

function MyComponent() {
  const { isMobile, isTablet, isDesktop, deviceType } = useResponsive();

  return (
    <div>
      {isMobile && <MobileView />}
      {isDesktop && <DesktopView />}
    </div>
  );
}
```

---

### getDeviceType

```tsx
import { getDeviceType } from '@/config/responsive';

const device = getDeviceType(); // 'mobile' | 'tablet' | 'desktop'
```

---

### isTouchDevice

```tsx
import { isTouchDevice } from '@/config/responsive';

if (isTouchDevice()) {
  // 触摸设备特殊处理
}
```

---

## 📏 尺寸规范

### 字体大小

| 用途 | 移动端 | 平板 | 桌面端 |
|------|--------|------|--------|
| H1标题 | 30px | 36px | 48px |
| H2标题 | 24px | 30px | 36px |
| H3标题 | 20px | 24px | 30px |
| 正文 | 14px | 16px | 18px |
| 小字 | 12px | 14px | 16px |

### 间距

| 类型 | 移动端 | 平板 | 桌面端 |
|------|--------|------|--------|
| 容器padding | 16px | 24px | 32px |
| 卡片padding | 16px | 24px | 32px |
| 栅格gap | 12px | 16px | 24px |
| 元素margin | 12px | 16px | 24px |

### 触摸目标

| 元素 | 最小尺寸 |
|------|----------|
| 按钮 | 44×44px |
| 图标按钮 | 44×44px |
| 输入框高度 | 44px |
| 复选框/单选 | 20×20px |
| 链接间距 | 8px |

---

## 🎨 最佳实践

### 1. 移动优先CSS

```tsx
// ✅ 好 - 移动优先
<div className="
  text-sm md:text-base lg:text-lg
  p-4 md:p-6 lg:p-8
  grid-cols-1 md:grid-cols-2 lg:grid-cols-3
">

// ❌ 差 - 桌面优先
<div className="
  lg:text-lg md:text-base text-sm
">
```

### 2. 合理使用断点

```tsx
// ✅ 好 - 渐进增强
<div className="w-full md:w-1/2 lg:w-1/3">

// ❌ 差 - 过度细化
<div className="w-full sm:w-11/12 md:w-10/12 lg:w-9/12 xl:w-8/12">
```

### 3. 触摸友好

```tsx
// ✅ 好 - 足够的触摸区域
<button className="min-h-[44px] min-w-[44px] px-4">

// ❌ 差 - 太小
<button className="h-6 w-6 p-1">
```

### 4. 图片优化

```tsx
// ✅ 好 - 响应式图片
<ResponsiveImage
  src="image.jpg"
  srcSet="small.jpg 480w, large.jpg 800w"
  sizes="(max-width: 768px) 100vw, 50vw"
  lazy
/>

// ❌ 差 - 固定尺寸
<img src="large-image.jpg" width="1920" />
```

### 5. 导航设计

```tsx
// ✅ 好 - 移动端折叠
<ResponsiveNav
  items={navItems}
  mobileCollapsed
/>

// ❌ 差 - 移动端显示所有项
<nav className="flex gap-2">
  {/* 10+ 导航项 */}
</nav>
```

---

## 🚀 快速开始

### 1. 查看演示

```tsx
import ResponsiveDemo from '@/components/responsive/ResponsiveDemo';

<ResponsiveDemo />
```

### 2. 基础布局

```tsx
import {
  ResponsiveContainer,
  ResponsiveNav,
  NavSpacer
} from '@/components/responsive';

function App() {
  return (
    <>
      <ResponsiveNav
        logo={<Logo />}
        items={navItems}
      />
      <NavSpacer />
      <ResponsiveContainer>
        {/* 内容 */}
      </ResponsiveContainer>
    </>
  );
}
```

### 3. 响应式表单

```tsx
import {
  ResponsiveGrid,
  ResponsiveInput,
  ResponsiveButton
} from '@/components/responsive';

<form>
  <ResponsiveGrid cols={{ mobile: 1, tablet: 2 }}>
    <ResponsiveInput label="姓名" />
    <ResponsiveInput label="邮箱" type="email" />
  </ResponsiveGrid>
  
  <ResponsiveButton variant="primary" fullWidth>
    提交
  </ResponsiveButton>
</form>
```

---

## 📱 测试清单

### 移动端 (< 768px)
- [ ] 导航折叠成汉堡菜单
- [ ] 表格可以水平滚动
- [ ] 按钮足够大(44×44px)
- [ ] 文字清晰可读
- [ ] 触摸交互流畅
- [ ] 图片正确加载

### 平板 (768px - 1024px)
- [ ] 布局适配中等屏幕
- [ ] 导航显示部分项
- [ ] 卡片2列显示
- [ ] 字体大小适中

### 桌面端 (> 1024px)
- [ ] 充分利用屏幕空间
- [ ] 导航完整显示
- [ ] 卡片3-4列显示
- [ ] 悬停效果正常

---

## 📊 性能建议

1. **图片优化**
   - 使用 WebP 格式
   - 实现懒加载
   - 提供多种尺寸

2. **CSS优化**
   - 避免深层嵌套
   - 使用 Tailwind purge
   - 减少动画复杂度

3. **JavaScript优化**
   - 使用 React.memo
   - 防抖/节流窗口事件
   - 按需加载组件

4. **移动端特殊处理**
   - 减少动画效果
   - 简化复杂交互
   - 优先显示核心功能

---

## 🎉 总结

这套响应式系统提供了:
- ✅ 完整的组件库
- ✅ 移动优先设计
- ✅ 触摸友好交互
- ✅ 自适应布局
- ✅ 性能优化
- ✅ 易于使用

可以立即在项目中使用! 🚀
