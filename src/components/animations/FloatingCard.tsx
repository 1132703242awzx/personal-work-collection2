/**
 * 悬浮卡片组件
 * 带悬停动画效果的卡片
 */

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { floatingCardVariants } from '../../config/animations';

interface FloatingCardProps {
  children: ReactNode;
  onClick?: () => void;
  className?: string;
  gradient?: boolean;
}

export default function FloatingCard({ 
  children, 
  onClick,
  className = '',
  gradient = false 
}: FloatingCardProps) {
  return (
    <motion.div
      variants={floatingCardVariants}
      initial="rest"
      whileHover="hover"
      onClick={onClick}
      className={`
        p-6 rounded-lg
        ${gradient 
          ? 'bg-gradient-to-br from-slate-800 to-slate-900' 
          : 'bg-slate-800'
        }
        border border-slate-700
        cursor-pointer
        transition-all duration-300
        hover:border-blue-500/50
        hover:shadow-xl hover:shadow-blue-500/20
        ${className}
      `}
    >
      {children}
    </motion.div>
  );
}

// 统计卡片
export function StatCard({
  title,
  value,
  icon,
  trend,
  trendValue,
  className = ''
}: {
  title: string;
  value: string | number;
  icon?: ReactNode;
  trend?: 'up' | 'down';
  trendValue?: string;
  className?: string;
}) {
  return (
    <FloatingCard className={className} gradient>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-400 mb-1">{title}</p>
          <h3 className="text-3xl font-bold text-white mb-2">{value}</h3>
          {trend && trendValue && (
            <div className={`flex items-center text-sm ${
              trend === 'up' ? 'text-green-400' : 'text-red-400'
            }`}>
              <span className="mr-1">{trend === 'up' ? '↑' : '↓'}</span>
              <span>{trendValue}</span>
            </div>
          )}
        </div>
        {icon && (
          <div className="text-blue-400 text-2xl">
            {icon}
          </div>
        )}
      </div>
    </FloatingCard>
  );
}
