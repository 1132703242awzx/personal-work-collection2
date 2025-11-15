/**
 * 加载指示器组件
 * 多种样式的加载动画
 */

import { motion } from 'framer-motion';
import { spinnerVariants, pulseVariants } from '../../config/animations';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'spinner' | 'dots' | 'pulse' | 'bars';
  color?: string;
  text?: string;
  fullScreen?: boolean;
}

export default function LoadingSpinner({ 
  size = 'md',
  variant = 'spinner',
  color = 'text-blue-500',
  text,
  fullScreen = false
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const container = fullScreen ? (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      {renderContent()}
    </div>
  ) : renderContent();

  function renderContent() {
    return (
      <div className="flex flex-col items-center space-y-3">
        {variant === 'spinner' && (
          <motion.div
            variants={spinnerVariants}
            animate="animate"
            className={`${sizeClasses[size]} ${color} border-4 border-t-transparent rounded-full`}
          />
        )}

        {variant === 'dots' && (
          <div className="flex space-x-2">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className={`w-3 h-3 ${color.replace('text-', 'bg-')} rounded-full`}
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [1, 0.5, 1]
                }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: i * 0.2
                }}
              />
            ))}
          </div>
        )}

        {variant === 'pulse' && (
          <motion.div
            variants={pulseVariants}
            animate="animate"
            className={`${sizeClasses[size]} ${color.replace('text-', 'bg-')} rounded-full`}
          />
        )}

        {variant === 'bars' && (
          <div className="flex space-x-1">
            {[0, 1, 2, 3].map((i) => (
              <motion.div
                key={i}
                className={`w-1 ${color.replace('text-', 'bg-')} rounded-full`}
                animate={{
                  height: [12, 24, 12]
                }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: i * 0.1
                }}
              />
            ))}
          </div>
        )}

        {text && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-sm text-gray-300 font-medium"
          >
            {text}
          </motion.p>
        )}
      </div>
    );
  }

  return container;
}

// 预设加载组件
export function PageLoading() {
  return (
    <LoadingSpinner 
      size="lg" 
      variant="spinner" 
      text="加载中..." 
      fullScreen 
    />
  );
}

export function InlineLoading({ text }: { text?: string }) {
  return (
    <div className="flex items-center justify-center py-8">
      <LoadingSpinner size="md" variant="dots" text={text} />
    </div>
  );
}
