/**
 * 响应式容器组件
 * 提供一致的容器宽度和内边距
 */

import { ReactNode } from 'react';

interface ResponsiveContainerProps {
  children: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  padding?: boolean;
  className?: string;
}

export default function ResponsiveContainer({
  children,
  size = 'lg',
  padding = true,
  className = ''
}: ResponsiveContainerProps) {
  const sizeClasses = {
    sm: 'max-w-2xl',
    md: 'max-w-4xl',
    lg: 'max-w-6xl',
    xl: 'max-w-7xl',
    full: 'max-w-full'
  };

  const paddingClasses = padding ? 'px-4 md:px-6 lg:px-8' : '';

  return (
    <div className={`
      mx-auto w-full
      ${sizeClasses[size]}
      ${paddingClasses}
      ${className}
    `}>
      {children}
    </div>
  );
}

// 响应式栅格容器
export function ResponsiveGrid({
  children,
  cols = { mobile: 1, tablet: 2, desktop: 3 },
  gap = 'normal',
  className = ''
}: {
  children: ReactNode;
  cols?: { mobile?: number; tablet?: number; desktop?: number; wide?: number };
  gap?: 'small' | 'normal' | 'large';
  className?: string;
}) {
  const gapClasses = {
    small: 'gap-3 md:gap-4',
    normal: 'gap-4 md:gap-6',
    large: 'gap-6 md:gap-8'
  };

  const colClasses = [
    cols.mobile && `grid-cols-${cols.mobile}`,
    cols.tablet && `md:grid-cols-${cols.tablet}`,
    cols.desktop && `lg:grid-cols-${cols.desktop}`,
    cols.wide && `xl:grid-cols-${cols.wide}`
  ].filter(Boolean).join(' ');

  return (
    <div className={`
      grid
      ${colClasses}
      ${gapClasses[gap]}
      ${className}
    `}>
      {children}
    </div>
  );
}

// 响应式Flex容器
export function ResponsiveFlex({
  children,
  direction = 'column-to-row',
  align = 'start',
  justify = 'start',
  gap = 'normal',
  wrap = true,
  className = ''
}: {
  children: ReactNode;
  direction?: 'column-to-row' | 'row-to-column' | 'column' | 'row';
  align?: 'start' | 'center' | 'end' | 'stretch';
  justify?: 'start' | 'center' | 'end' | 'between' | 'around';
  gap?: 'small' | 'normal' | 'large';
  wrap?: boolean;
  className?: string;
}) {
  const directionClasses = {
    'column-to-row': 'flex-col md:flex-row',
    'row-to-column': 'flex-row md:flex-col',
    'column': 'flex-col',
    'row': 'flex-row'
  };

  const alignClasses = {
    start: 'items-start',
    center: 'items-center',
    end: 'items-end',
    stretch: 'items-stretch'
  };

  const justifyClasses = {
    start: 'justify-start',
    center: 'justify-center',
    end: 'justify-end',
    between: 'justify-between',
    around: 'justify-around'
  };

  const gapClasses = {
    small: 'gap-2 md:gap-3',
    normal: 'gap-3 md:gap-4',
    large: 'gap-4 md:gap-6'
  };

  return (
    <div className={`
      flex
      ${directionClasses[direction]}
      ${alignClasses[align]}
      ${justifyClasses[justify]}
      ${gapClasses[gap]}
      ${wrap ? 'flex-wrap' : 'flex-nowrap'}
      ${className}
    `}>
      {children}
    </div>
  );
}

// 响应式卡片
export function ResponsiveCard({
  children,
  padding = 'normal',
  hover = false,
  className = ''
}: {
  children: ReactNode;
  padding?: 'small' | 'normal' | 'large';
  hover?: boolean;
  className?: string;
}) {
  const paddingClasses = {
    small: 'p-3 md:p-4',
    normal: 'p-4 md:p-6',
    large: 'p-6 md:p-8'
  };

  return (
    <div className={`
      bg-slate-800 
      rounded-lg md:rounded-xl
      border border-slate-700
      ${paddingClasses[padding]}
      ${hover ? 'transition-all hover:border-blue-500 hover:shadow-lg' : ''}
      ${className}
    `}>
      {children}
    </div>
  );
}
