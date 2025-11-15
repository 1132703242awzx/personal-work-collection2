/**
 * 响应式按钮组件
 * 触摸友好,支持多种尺寸和变体
 */

import { ButtonHTMLAttributes, ReactNode } from 'react';

interface ResponsiveButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  loading?: boolean;
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
}

export default function ResponsiveButton({
  children,
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  loading = false,
  icon,
  iconPosition = 'left',
  disabled,
  className = '',
  ...props
}: ResponsiveButtonProps) {
  // 变体样式
  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white border-transparent',
    secondary: 'bg-slate-700 hover:bg-slate-600 text-white border-transparent',
    outline: 'bg-transparent hover:bg-slate-800 text-blue-400 border-blue-400',
    ghost: 'bg-transparent hover:bg-slate-800 text-gray-300 border-transparent',
    danger: 'bg-red-600 hover:bg-red-700 text-white border-transparent'
  };

  // 尺寸样式 (触摸友好的最小尺寸)
  const sizeClasses = {
    sm: 'min-h-[44px] px-3 md:px-4 py-2 text-xs md:text-sm',
    md: 'min-h-[48px] px-4 md:px-6 py-2.5 md:py-3 text-sm md:text-base',
    lg: 'min-h-[52px] px-6 md:px-8 py-3 md:py-4 text-base md:text-lg'
  };

  const iconSizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  return (
    <button
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center gap-2
        ${fullWidth ? 'w-full' : ''}
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        border
        rounded-lg md:rounded-xl
        font-medium
        transition-all duration-200
        hover:scale-105 active:scale-95
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-900
        disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
        ${className}
      `}
      {...props}
    >
      {loading && (
        <svg className={`animate-spin ${iconSizeClasses[size]}`} fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      )}
      
      {!loading && icon && iconPosition === 'left' && (
        <span className={iconSizeClasses[size]}>{icon}</span>
      )}
      
      <span>{children}</span>
      
      {!loading && icon && iconPosition === 'right' && (
        <span className={iconSizeClasses[size]}>{icon}</span>
      )}
    </button>
  );
}

// 图标按钮
export function ResponsiveIconButton({
  icon,
  label,
  size = 'md',
  variant = 'ghost',
  className = '',
  ...props
}: {
  icon: ReactNode;
  label: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
} & ButtonHTMLAttributes<HTMLButtonElement>) {
  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-slate-700 hover:bg-slate-600 text-white',
    outline: 'bg-transparent hover:bg-slate-800 text-blue-400 border border-blue-400',
    ghost: 'bg-transparent hover:bg-slate-800 text-gray-300',
    danger: 'bg-red-600 hover:bg-red-700 text-white'
  };

  const sizeClasses = {
    sm: 'w-11 h-11', // 44px
    md: 'w-12 h-12', // 48px
    lg: 'w-14 h-14'  // 56px
  };

  const iconSizeClasses = {
    sm: 'w-5 h-5',
    md: 'w-6 h-6',
    lg: 'w-7 h-7'
  };

  return (
    <button
      aria-label={label}
      title={label}
      className={`
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        flex items-center justify-center
        rounded-lg md:rounded-xl
        transition-all duration-200
        hover:scale-105 active:scale-95
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-900
        disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
        ${className}
      `}
      {...props}
    >
      <span className={iconSizeClasses[size]}>{icon}</span>
    </button>
  );
}

// 按钮组
export function ResponsiveButtonGroup({
  children,
  orientation = 'horizontal',
  fullWidth = false,
  className = ''
}: {
  children: ReactNode;
  orientation?: 'horizontal' | 'vertical';
  fullWidth?: boolean;
  className?: string;
}) {
  return (
    <div className={`
      flex
      ${orientation === 'horizontal' ? 'flex-row' : 'flex-col'}
      ${fullWidth ? 'w-full' : ''}
      gap-2 md:gap-3
      ${className}
    `}>
      {children}
    </div>
  );
}
