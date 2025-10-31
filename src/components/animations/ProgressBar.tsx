/**
 * 进度条组件
 * 显示任务进度，带动画效果
 */

import { motion } from 'framer-motion';
// import { progressBarVariants } from '../../config/animations';

interface ProgressBarProps {
  progress: number; // 0-100
  showLabel?: boolean;
  color?: string;
  height?: string;
  className?: string;
}

export default function ProgressBar({ 
  progress,
  showLabel = true,
  color = 'bg-blue-600',
  height = 'h-2',
  className = ''
}: ProgressBarProps) {
  const clampedProgress = Math.min(100, Math.max(0, progress));

  return (
    <div className={`w-full ${className}`}>
      {showLabel && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-400">进度</span>
          <span className="text-sm font-medium text-white">
            {clampedProgress.toFixed(0)}%
          </span>
        </div>
      )}
      
      <div className={`w-full bg-slate-700 rounded-full overflow-hidden ${height}`}>
        <motion.div
          className={`${height} ${color} rounded-full`}
          initial={{ width: '0%' }}
          animate={{ width: `${clampedProgress}%` }}
          transition={{
            duration: 0.5,
            ease: [0.4, 0, 0.2, 1]
          }}
        />
      </div>
    </div>
  );
}

// 步骤进度条
interface StepProgressProps {
  steps: Array<{ label: string; completed: boolean }>;
  className?: string;
}

export function StepProgress({ steps, className = '' }: StepProgressProps) {
  return (
    <div className={`w-full ${className}`}>
      <div className="flex items-center justify-between mb-4">
        {steps.map((step, index) => (
          <div key={index} className="flex items-center flex-1">
            <div className="flex flex-col items-center flex-1">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ 
                  scale: 1, 
                  opacity: 1,
                  backgroundColor: step.completed ? '#3b82f6' : '#475569'
                }}
                transition={{ delay: index * 0.1, duration: 0.3 }}
                className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  text-white font-semibold text-sm
                  ${step.completed ? 'bg-blue-600' : 'bg-slate-600'}
                `}
              >
                {step.completed ? '✓' : index + 1}
              </motion.div>
              <span className="text-xs mt-2 text-gray-400 text-center">
                {step.label}
              </span>
            </div>
            
            {index < steps.length - 1 && (
              <div className="flex-1 h-1 mx-2 bg-slate-700 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: '0%' }}
                  animate={{ 
                    width: step.completed && steps[index + 1]?.completed ? '100%' : '0%'
                  }}
                  transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
                  className="h-full bg-blue-600"
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// 环形进度条
export function CircularProgress({ 
  progress, 
  size = 120,
  strokeWidth = 8,
  className = '' 
}: { 
  progress: number; 
  size?: number;
  strokeWidth?: number;
  className?: string;
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className={`relative ${className}`} style={{ width: size, height: size }}>
      <svg className="transform -rotate-90" width={size} height={size}>
        {/* 背景圆 */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="text-slate-700"
        />
        {/* 进度圆 */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: [0.4, 0, 0.2, 1] }}
          className="text-blue-600"
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-2xl font-bold text-white">
          {progress.toFixed(0)}%
        </span>
      </div>
    </div>
  );
}
