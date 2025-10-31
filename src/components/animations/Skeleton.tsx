/**
 * 骨架屏组件
 * 用于加载状态显示
 */

import { motion } from 'framer-motion';
import { skeletonVariants } from '../../config/animations';

interface SkeletonProps {
  variant?: 'text' | 'rectangular' | 'circular';
  width?: string | number;
  height?: string | number;
  className?: string;
}

export default function Skeleton({ 
  variant = 'rectangular',
  width = '100%',
  height = '20px',
  className = '' 
}: SkeletonProps) {
  const getShape = () => {
    switch (variant) {
      case 'text':
        return 'rounded';
      case 'circular':
        return 'rounded-full';
      case 'rectangular':
      default:
        return 'rounded-lg';
    }
  };

  return (
    <motion.div
      variants={skeletonVariants}
      animate="animate"
      className={`bg-slate-700/50 ${getShape()} ${className}`}
      style={{ 
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height
      }}
    />
  );
}

// 预设骨架屏组件
export function SkeletonText({ lines = 3, className = '' }: { lines?: number; className?: string }) {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: lines }).map((_, index) => (
        <Skeleton 
          key={index}
          variant="text" 
          height={16}
          width={index === lines - 1 ? '70%' : '100%'}
        />
      ))}
    </div>
  );
}

export function SkeletonCard({ className = '' }: { className?: string }) {
  return (
    <div className={`p-6 bg-slate-800 rounded-lg ${className}`}>
      <Skeleton variant="rectangular" height={200} className="mb-4" />
      <Skeleton variant="text" height={24} className="mb-2" />
      <SkeletonText lines={2} />
    </div>
  );
}
