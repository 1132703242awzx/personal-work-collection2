/**
 * 交互式按钮组件
 * 带悬停和点击动画效果
 */

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { buttonHoverVariants } from '../../config/animations';

interface AnimatedButtonProps {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  type?: 'button' | 'submit' | 'reset';
  loading?: boolean;
}

export default function AnimatedButton({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
  size = 'md',
  className = '',
  type = 'button',
  loading = false
}: AnimatedButtonProps) {
  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-purple-600 hover:bg-purple-700 text-white',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-600/10',
    ghost: 'bg-transparent hover:bg-white/10 text-white'
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      variants={buttonHoverVariants}
      initial="rest"
      whileHover="hover"
      whileTap="tap"
      className={`
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        rounded-lg font-medium
        transition-colors duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        flex items-center justify-center space-x-2
        ${className}
      `}
    >
      {loading && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
        />
      )}
      <span>{children}</span>
    </motion.button>
  );
}

// 浮动动作按钮
export function FloatingActionButton({
  icon,
  onClick,
  className = ''
}: {
  icon: ReactNode;
  onClick?: () => void;
  className?: string;
}) {
  return (
    <motion.button
      onClick={onClick}
      whileHover={{ scale: 1.1, rotate: 90 }}
      whileTap={{ scale: 0.9 }}
      className={`
        fixed bottom-6 right-6
        w-14 h-14 rounded-full
        bg-blue-600 hover:bg-blue-700
        text-white shadow-lg
        flex items-center justify-center
        z-50
        ${className}
      `}
    >
      {icon}
    </motion.button>
  );
}

// 图标按钮
export function IconButton({
  icon,
  onClick,
  tooltip,
  className = ''
}: {
  icon: ReactNode;
  onClick?: () => void;
  tooltip?: string;
  className?: string;
}) {
  return (
    <motion.button
      onClick={onClick}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      className={`
        p-2 rounded-lg
        bg-slate-800 hover:bg-slate-700
        text-gray-300 hover:text-white
        transition-colors duration-200
        ${className}
      `}
      title={tooltip}
    >
      {icon}
    </motion.button>
  );
}
