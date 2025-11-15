# 🎬 动画系统使用快速指南

## 🚀 立即开始

### 1. 导入动画组件

```tsx
// 从统一入口导入
import {
  // 页面过渡
  PageTransition,
  
  // 基础动画
  FadeIn,
  AnimatedList,
  CardStack,
  
  // 交互组件
  AnimatedButton,
  FloatingActionButton,
  IconButton,
  AnimatedInput,
  AnimatedTextarea,
  AnimatedSwitch,
  FloatingCard,
  StatCard,
  Modal,
  ConfirmDialog,
  
  // 加载状态
  LoadingSpinner,
  PageLoading,
  InlineLoading,
  Skeleton,
  SkeletonText,
  SkeletonCard,
  
  // 进度指示
  ProgressBar,
  StepProgress,
  CircularProgress
} from '@/components/animations';
```

### 2. 基础用法示例

```tsx
import { PageTransition, FadeIn, AnimatedButton } from '@/components/animations';

function MyPage() {
  return (
    <PageTransition>
      <div className="container">
        {/* 标题淡入上滑 */}
        <FadeIn direction="up">
          <h1>欢迎使用</h1>
        </FadeIn>

        {/* 动画按钮 */}
        <AnimatedButton variant="primary" onClick={() => alert('clicked!')}>
          开始使用
        </AnimatedButton>
      </div>
    </PageTransition>
  );
}
```

### 3. 列表动画

```tsx
import { AnimatedList } from '@/components/animations';

const items = ['项目 1', '项目 2', '项目 3'];

<AnimatedList stagger="normal">
  {items.map((item, i) => (
    <div key={i} className="item">{item}</div>
  ))}
</AnimatedList>
```

### 4. 表单动画

```tsx
import { AnimatedInput, AnimatedButton } from '@/components/animations';

<form onSubmit={handleSubmit}>
  <AnimatedInput
    label="用户名"
    placeholder="输入用户名"
    error={errors.username}
  />
  
  <AnimatedButton 
    variant="primary" 
    type="submit"
    loading={isSubmitting}
  >
    提交
  </AnimatedButton>
</form>
```

### 5. 加载状态

```tsx
import { LoadingSpinner, Skeleton } from '@/components/animations';

// 加载器
{loading && <LoadingSpinner variant="spinner" size="lg" />}

// 骨架屏
{loading ? (
  <Skeleton variant="rectangular" height="200px" />
) : (
  <Content />
)}
```

### 6. 模态框

```tsx
import { Modal, AnimatedButton } from '@/components/animations';

const [open, setOpen] = useState(false);

<AnimatedButton onClick={() => setOpen(true)}>
  打开
</AnimatedButton>

<Modal isOpen={open} onClose={() => setOpen(false)} title="标题">
  <p>模态框内容</p>
</Modal>
```

### 7. 进度指示

```tsx
import { ProgressBar, StepProgress } from '@/components/animations';

// 线性进度
<ProgressBar progress={75} showLabel />

// 步骤进度
<StepProgress 
  steps={[
    { label: '步骤1', completed: true },
    { label: '步骤2', completed: true },
    { label: '步骤3', completed: false }
  ]}
/>
```

## 🎨 常用组合

### 登录页面
```tsx
<PageTransition>
  <FadeIn direction="up" delay={0.2}>
    <div className="login-card">
      <h1>登录</h1>
      <AnimatedInput label="邮箱" type="email" />
      <AnimatedInput label="密码" type="password" />
      <AnimatedButton variant="primary" type="submit">
        登录
      </AnimatedButton>
    </div>
  </FadeIn>
</PageTransition>
```

### 数据列表
```tsx
{loading ? (
  <SkeletonCard />
) : (
  <AnimatedList stagger="fast">
    {data.map(item => (
      <FloatingCard key={item.id}>
        <h3>{item.title}</h3>
        <p>{item.description}</p>
      </FloatingCard>
    ))}
  </AnimatedList>
)}
```

### 仪表板卡片
```tsx
<div className="grid grid-cols-3 gap-6">
  <FadeIn direction="up" delay={0.1}>
    <StatCard
      title="总用户"
      value="12,345"
      trend="up"
      trendValue="↑ 12%"
    />
  </FadeIn>
  
  <FadeIn direction="up" delay={0.2}>
    <StatCard
      title="活跃项目"
      value="89"
      trend="up"
      trendValue="↑ 5%"
    />
  </FadeIn>
  
  <FadeIn direction="up" delay={0.3}>
    <StatCard
      title="完成任务"
      value="234"
      trend="down"
      trendValue="↓ 3%"
    />
  </FadeIn>
</div>
```

## 📋 Props 速查表

### AnimatedButton
- `variant`: 'primary' | 'secondary' | 'outline' | 'ghost'
- `size`: 'sm' | 'md' | 'lg'
- `loading`: boolean
- `disabled`: boolean

### FadeIn
- `direction`: 'none' | 'up' | 'down'
- `delay`: number (秒)
- `duration`: number (秒)

### AnimatedList
- `stagger`: 'fast' | 'normal' | 'slow'

### LoadingSpinner
- `variant`: 'spinner' | 'dots' | 'pulse' | 'bars'
- `size`: 'sm' | 'md' | 'lg'
- `text`: string

### Modal
- `isOpen`: boolean
- `onClose`: () => void
- `title`: string
- `size`: 'sm' | 'md' | 'lg' | 'xl'

### ProgressBar
- `progress`: number (0-100)
- `showLabel`: boolean
- `color`: string (Tailwind class)

## 🎯 最佳实践

1. **页面入口使用 PageTransition**
   ```tsx
   <PageTransition>
     {/* 页面内容 */}
   </PageTransition>
   ```

2. **重要内容用 FadeIn**
   ```tsx
   <FadeIn direction="up">
     <MainContent />
   </FadeIn>
   ```

3. **列表用 AnimatedList**
   ```tsx
   <AnimatedList stagger="normal">
     {items.map(item => <Item key={item.id} {...item} />)}
   </AnimatedList>
   ```

4. **加载用骨架屏**
   ```tsx
   {loading ? <Skeleton /> : <Content />}
   ```

5. **按钮统一用 AnimatedButton**
   ```tsx
   <AnimatedButton variant="primary">
     提交
   </AnimatedButton>
   ```

## 📖 完整文档

查看 `docs/ANIMATIONS.md` 获取完整的API文档和高级用法。

## 🎉 演示页面

运行以下组件查看所有动画效果:

```tsx
import AnimationDemo from '@/components/animations/AnimationDemo';

<AnimationDemo />
```

或查看实际应用示例:

```tsx
import { 
  AnimatedLoginPage,
  AnimatedDataList,
  AnimatedMultiStepForm,
  AnimatedDashboard 
} from '@/components/animations/AnimationExamples';
```

---

**提示**: 所有组件都支持 `className` prop,可以添加自定义样式!
