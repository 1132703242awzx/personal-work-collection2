# 动画系统文档

## 📚 概述

本项目使用 **Framer Motion**、**CSS Transitions** 和 **Lottie** 构建了一个完整的动画系统,提供了丰富的动画组件和配置,用于创建流畅、专业的用户界面。

## 🎯 核心特性

- ✅ **页面过渡动画** - 路由切换时的淡入淡出效果
- ✅ **微交互动画** - 按钮悬停、表单反馈、列表项逐项显示
- ✅ **加载状态** - AI处理进度、骨架屏、多种加载器样式
- ✅ **性能优化** - 使用 transform 和 opacity 实现GPU加速
- ✅ **TypeScript 支持** - 完整的类型定义

## 📦 安装依赖

```bash
npm install framer-motion lottie-react
```

## 🏗️ 架构

```
src/
├── config/
│   └── animations.ts          # 动画配置和variants
├── components/
│   └── animations/
│       ├── PageTransition.tsx # 页面过渡
│       ├── FadeIn.tsx         # 淡入动画
│       ├── AnimatedList.tsx   # 列表动画
│       ├── CardStack.tsx      # 卡片堆叠
│       ├── AnimatedButton.tsx # 交互按钮
│       ├── AnimatedInput.tsx  # 表单输入
│       ├── FloatingCard.tsx   # 悬浮卡片
│       ├── Modal.tsx          # 模态框
│       ├── LoadingSpinner.tsx # 加载器
│       ├── Skeleton.tsx       # 骨架屏
│       ├── ProgressBar.tsx    # 进度指示器
│       ├── AnimationDemo.tsx  # 演示组件
│       └── index.ts           # 统一导出
└── tailwind.config.js         # CSS动画扩展
```

## 🎨 组件使用指南

### 1. 页面过渡 (PageTransition)

用于路由切换时的页面过渡效果。

```tsx
import { PageTransition } from '@/components/animations';

function MyPage() {
  return (
    <PageTransition>
      <div>页面内容</div>
    </PageTransition>
  );
}
```

**特性:**
- 淡入淡出 + 轻微滑动
- 自动处理进入/退出动画
- 性能优化的过渡效果

---

### 2. 淡入动画 (FadeIn)

通用的淡入动画包装器。

```tsx
import { FadeIn } from '@/components/animations';

// 简单淡入
<FadeIn>
  <div>内容</div>
</FadeIn>

// 从下方滑入
<FadeIn direction="up" delay={0.2}>
  <div>内容</div>
</FadeIn>

// 从上方滑入
<FadeIn direction="down" duration={0.6}>
  <div>内容</div>
</FadeIn>
```

**Props:**
- `direction`: `'none'` | `'up'` | `'down'` (默认: `'none'`)
- `delay`: 延迟时间(秒) (默认: `0`)
- `duration`: 动画时长(秒) (默认: `0.4`)
- `className`: 额外的CSS类名

---

### 3. 列表动画 (AnimatedList)

列表项逐项显示的交错动画。

```tsx
import { AnimatedList } from '@/components/animations';

const items = ['项目 1', '项目 2', '项目 3'];

<AnimatedList stagger="normal">
  {items.map(item => (
    <div key={item}>{item}</div>
  ))}
</AnimatedList>
```

**Props:**
- `stagger`: `'fast'` (0.05s) | `'normal'` (0.1s) | `'slow'` (0.2s)
- `children`: 子元素数组

**最佳实践:**
- 每个子元素需要唯一的 `key` prop
- 适合 5-20 个列表项
- 超过 20 项建议使用虚拟滚动

---

### 4. 卡片堆叠 (CardStack)

卡片依次出现的堆叠效果。

```tsx
import { CardStack } from '@/components/animations';

<CardStack stagger="fast">
  <div className="card">卡片 1</div>
  <div className="card">卡片 2</div>
  <div className="card">卡片 3</div>
</CardStack>
```

**Props:**
- `stagger`: 交错速度
- `children`: 卡片元素数组

**动画效果:**
- 缩放 0.8 → 1.0
- 透明度 0 → 1
- Y轴位移 20px → 0

---

### 5. 交互按钮 (AnimatedButton)

带悬停和点击动画的按钮。

```tsx
import { AnimatedButton, FloatingActionButton, IconButton } from '@/components/animations';

// 主要按钮
<AnimatedButton 
  variant="primary" 
  size="lg"
  onClick={handleClick}
>
  提交
</AnimatedButton>

// 加载状态
<AnimatedButton 
  variant="primary"
  loading={isLoading}
>
  处理中...
</AnimatedButton>

// 浮动操作按钮
<FloatingActionButton 
  icon={<PlusIcon />}
  onClick={handleAdd}
/>

// 图标按钮
<IconButton 
  icon={<SettingsIcon />}
  tooltip="设置"
  onClick={handleSettings}
/>
```

**Variants:**
- `primary`: 主要蓝色按钮
- `secondary`: 次要灰色按钮
- `outline`: 轮廓按钮
- `ghost`: 幽灵按钮(透明背景)

**Sizes:**
- `sm`: 小按钮 (px-3 py-1.5, text-sm)
- `md`: 中等按钮 (px-4 py-2, text-base)
- `lg`: 大按钮 (px-6 py-3, text-lg)

**动画效果:**
- Hover: scale 1.05
- Tap: scale 0.95
- 流畅的过渡效果

---

### 6. 表单输入 (AnimatedInput)

带动画反馈的表单组件。

```tsx
import { AnimatedInput, AnimatedTextarea, AnimatedSwitch } from '@/components/animations';

// 输入框
<AnimatedInput 
  label="用户名"
  placeholder="输入用户名"
  icon={<UserIcon />}
  error={errors.username}
/>

// 文本域
<AnimatedTextarea 
  label="项目描述"
  placeholder="输入描述..."
  rows={4}
/>

// 开关
<AnimatedSwitch 
  checked={enabled}
  onChange={setEnabled}
  label="启用通知"
/>
```

**动画特性:**
- 聚焦时标签上移并缩小
- 边框颜色平滑过渡
- 错误消息淡入动画
- 底部指示器动画

---

### 7. 悬浮卡片 (FloatingCard)

悬停时上浮的卡片组件。

```tsx
import { FloatingCard, StatCard } from '@/components/animations';

// 基础卡片
<FloatingCard gradient onClick={handleClick}>
  <h3>标题</h3>
  <p>内容</p>
</FloatingCard>

// 统计卡片
<StatCard
  title="总用户"
  value="12,345"
  icon={<UserIcon />}
  trend="up"
  trendValue="↑ 12%"
/>
```

**动画效果:**
- 悬停时 Y轴 -10px
- 边框高亮效果
- 阴影增强

---

### 8. 模态框 (Modal)

带动画的模态框组件。

```tsx
import { Modal, ConfirmDialog } from '@/components/animations';

// 基础模态框
<Modal 
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  title="标题"
  size="md"
>
  <div>模态框内容</div>
</Modal>

// 确认对话框
<ConfirmDialog
  isOpen={confirmOpen}
  onClose={() => setConfirmOpen(false)}
  onConfirm={handleConfirm}
  title="确认操作"
  message="您确定要执行此操作吗?"
  type="warning"
  confirmText="确认"
  cancelText="取消"
/>
```

**Sizes:**
- `sm`: max-w-sm
- `md`: max-w-md (默认)
- `lg`: max-w-2xl
- `xl`: max-w-4xl

**Dialog Types:**
- `info`: 信息提示 (蓝色)
- `warning`: 警告 (黄色)
- `danger`: 危险操作 (红色)

**动画效果:**
- 背景遮罩淡入
- 内容缩放 0.8 → 1.0 + 滑入
- 弹性动画效果

---

### 9. 加载状态 (LoadingSpinner)

多种样式的加载器。

```tsx
import { LoadingSpinner, PageLoading, InlineLoading } from '@/components/animations';

// 基础加载器
<LoadingSpinner 
  variant="spinner"
  size="lg"
  color="text-blue-500"
  text="加载中..."
/>

// 全屏加载
<PageLoading />

// 内联加载
<InlineLoading text="处理中..." />
```

**Variants:**
- `spinner`: 旋转边框 (默认)
- `dots`: 跳动的点
- `pulse`: 脉冲圆形
- `bars`: 高度动画条形

**Sizes:**
- `sm`: 小尺寸
- `md`: 中等尺寸 (默认)
- `lg`: 大尺寸

---

### 10. 骨架屏 (Skeleton)

加载占位符组件。

```tsx
import { Skeleton, SkeletonText, SkeletonCard } from '@/components/animations';

// 基础骨架
<Skeleton variant="rectangular" width="100%" height="200px" />

// 圆形骨架
<Skeleton variant="circular" width="60px" height="60px" />

// 文本骨架
<SkeletonText lines={3} />

// 卡片骨架
<SkeletonCard />
```

**Variants:**
- `text`: 文本行 (默认)
- `rectangular`: 矩形
- `circular`: 圆形

**动画效果:**
- 透明度脉冲 0.4 → 1.0
- 平滑的循环动画

---

### 11. 进度指示器 (ProgressBar)

多种进度显示组件。

```tsx
import { ProgressBar, StepProgress, CircularProgress } from '@/components/animations';

// 线性进度条
<ProgressBar 
  progress={75}
  showLabel={true}
  color="bg-blue-500"
  height="h-2"
/>

// 步骤进度
<StepProgress 
  steps={[
    { label: '需求分析', completed: true },
    { label: '设计方案', completed: true },
    { label: '开发实现', completed: false },
    { label: '测试部署', completed: false }
  ]}
/>

// 环形进度
<CircularProgress 
  progress={75}
  size={120}
  strokeWidth={8}
/>
```

**动画特性:**
- 宽度/角度平滑过渡
- 自定义缓动函数
- 步骤间交错动画

---

## 🎬 动画配置 (animations.ts)

### Variants 列表

```typescript
// 基础动画
fadeInVariants
fadeInUpVariants
fadeInDownVariants
slideInRightVariants
slideInLeftVariants
scaleInVariants
bounceInVariants

// 列表动画
listContainerVariants
listItemVariants

// 卡片动画
cardStackVariants
cardItemVariants

// 页面动画
pageTransitionVariants

// 模态框动画
modalBackdropVariants
modalContentVariants

// UI交互
buttonHoverVariants
floatingCardVariants
notificationVariants

// 加载动画
spinnerVariants
pulseVariants
skeletonVariants
progressBarVariants
```

### 配置对象

```typescript
// 交错速度
staggerConfig = {
  fast: 0.05,
  normal: 0.1,
  slow: 0.2
}

// 动画时长
duration = {
  fast: 0.2,
  normal: 0.4,
  slow: 0.6
}

// 缓动函数
easing = {
  easeOut: [0.4, 0, 0.2, 1],      // 标准缓出
  easeInOut: [0.4, 0, 0.6, 1],    // 进出缓动
  bounce: [0.68, -0.55, 0.265, 1.55]  // 弹性
}
```

---

## 🎨 Tailwind CSS 动画

配置文件已扩展以下动画:

```javascript
// tailwind.config.js

animation: {
  'fade-in': 'fadeIn 0.4s ease-out',
  'fade-in-up': 'fadeInUp 0.5s ease-out',
  'fade-in-down': 'fadeInDown 0.5s ease-out',
  'slide-in-right': 'slideInRight 0.5s ease-out',
  'slide-in-left': 'slideInLeft 0.5s ease-out',
  'scale-in': 'scaleIn 0.3s ease-out',
  'bounce-in': 'bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  'spin-slow': 'spin 3s linear infinite',
  'shimmer': 'shimmer 2s linear infinite',
  'blob': 'blob 7s infinite',
  'float': 'float 3s ease-in-out infinite',
  'gradient': 'gradient 3s ease infinite'
}
```

**使用示例:**

```tsx
<div className="animate-fade-in-up">
  淡入上滑内容
</div>

<div className="animate-pulse-slow">
  缓慢脉冲
</div>

<div className="animate-shimmer">
  闪烁效果
</div>
```

---

## ⚡ 性能优化

### 1. 使用 GPU 加速属性

优先使用 `transform` 和 `opacity`,避免触发重排:

```tsx
// ✅ 好 - GPU加速
animate={{ opacity: 1, transform: 'translateY(0)' }}

// ❌ 差 - 触发重排
animate={{ top: '0px', height: '100px' }}
```

### 2. will-change 提示

对频繁动画的元素使用 `will-change`:

```css
.frequently-animated {
  will-change: transform, opacity;
}
```

### 3. 减少动画范围

```tsx
// ✅ 好 - 只动画需要的元素
<motion.div animate={{ opacity: 1 }}>
  <StaticContent />
</motion.div>

// ❌ 差 - 整个树都参与动画
<motion.div animate={{ opacity: 1 }}>
  <motion.div animate={{ scale: 1 }}>
    <motion.div animate={{ rotate: 0 }}>
      ...
    </motion.div>
  </motion.div>
</motion.div>
```

### 4. 使用 AnimatePresence 控制退出

```tsx
import { AnimatePresence } from 'framer-motion';

<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      内容
    </motion.div>
  )}
</AnimatePresence>
```

### 5. 延迟非关键动画

```tsx
// 关键内容立即显示
<FadeIn delay={0}>
  <CriticalContent />
</FadeIn>

// 装饰性内容延迟显示
<FadeIn delay={0.2}>
  <DecorativeContent />
</FadeIn>
```

---

## 🎯 最佳实践

### 1. 动画时长建议

| 类型 | 推荐时长 | 说明 |
|------|----------|------|
| 微交互 | 150-200ms | 按钮点击、输入反馈 |
| 页面过渡 | 300-400ms | 路由切换、模态框 |
| 复杂动画 | 500-600ms | 列表展开、卡片翻转 |
| 无限动画 | 2-3s | 脉冲、闪烁效果 |

### 2. 缓动函数选择

| 缓动 | 用途 | 示例 |
|------|------|------|
| easeOut | 进入动画 | 元素出现、淡入 |
| easeIn | 退出动画 | 元素消失、淡出 |
| easeInOut | 来回动画 | 悬停效果、开关 |
| linear | 持续动画 | 旋转、进度条 |
| bounce | 吸引注意 | 按钮点击、通知 |

### 3. 可访问性考虑

支持用户的动画偏好设置:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

在组件中检测:

```tsx
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

<motion.div
  animate={{ opacity: 1 }}
  transition={{ duration: prefersReducedMotion ? 0 : 0.4 }}
>
  内容
</motion.div>
```

### 4. 移动端优化

```tsx
// 减少移动端动画复杂度
const isMobile = window.innerWidth < 768;

<AnimatedList stagger={isMobile ? 'fast' : 'normal'}>
  {items}
</AnimatedList>
```

---

## 🚀 快速开始

### 1. 查看演示

```tsx
import AnimationDemo from '@/components/animations/AnimationDemo';

<AnimationDemo />
```

### 2. 在项目中使用

```tsx
import { 
  PageTransition,
  FadeIn,
  AnimatedButton,
  LoadingSpinner
} from '@/components/animations';

function MyApp() {
  const [loading, setLoading] = useState(false);

  return (
    <PageTransition>
      <div className="container">
        <FadeIn direction="up">
          <h1>欢迎</h1>
        </FadeIn>

        <AnimatedButton 
          variant="primary"
          loading={loading}
          onClick={() => setLoading(true)}
        >
          开始
        </AnimatedButton>

        {loading && <LoadingSpinner />}
      </div>
    </PageTransition>
  );
}
```

---

## 📝 注意事项

1. **不要过度动画**: 过多的动画会让用户分心,降低性能
2. **保持一致性**: 在整个应用中使用相同的动画时长和缓动
3. **测试性能**: 在低端设备上测试动画性能
4. **提供反馈**: 动画应该有明确的目的(加载、状态变化等)
5. **可取消**: 长时间动画应该可以被用户中断

---

## 🔗 相关资源

- [Framer Motion 文档](https://www.framer.com/motion/)
- [Lottie 动画](https://lottiefiles.com/)
- [Material Design 动画指南](https://material.io/design/motion)
- [CSS Easing 函数](https://easings.net/)

---

## 📄 许可证

MIT License

---

**作者:** Your Team  
**更新时间:** 2024
