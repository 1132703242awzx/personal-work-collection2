/**
 * 动画组件统一导出
 */

// 页面过渡
export { default as PageTransition } from './PageTransition';

// 基础动画
export { default as FadeIn } from './FadeIn';
export { default as AnimatedList } from './AnimatedList';
export { default as CardStack } from './CardStack';

// 交互组件
export { default as AnimatedButton, FloatingActionButton, IconButton } from './AnimatedButton';
export { default as AnimatedInput, AnimatedTextarea, AnimatedSwitch } from './AnimatedInput';
export { default as FloatingCard, StatCard } from './FloatingCard';
export { default as Modal, ConfirmDialog } from './Modal';

// 加载状态
export { default as LoadingSpinner, PageLoading, InlineLoading } from './LoadingSpinner';
export { default as Skeleton, SkeletonText, SkeletonCard } from './Skeleton';

// 进度指示
export { default as ProgressBar, StepProgress, CircularProgress } from './ProgressBar';

// 动画配置
export * from '../../config/animations';
