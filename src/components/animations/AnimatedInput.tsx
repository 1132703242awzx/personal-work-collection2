/**
 * 表单输入动画组件
 * 带动画反馈的输入框
 */

import { motion, AnimatePresence } from 'framer-motion';
import { useState, InputHTMLAttributes } from 'react';

interface AnimatedInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'className'> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
  className?: string;
}

export default function AnimatedInput({
  label,
  error,
  icon,
  className = '',
  ...props
}: AnimatedInputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [hasValue, setHasValue] = useState(false);

  return (
    <div className={`relative ${className}`}>
      {/* 标签 */}
      {label && (
        <motion.label
          initial={false}
          animate={{
            y: isFocused || hasValue ? 0 : 10,
            scale: isFocused || hasValue ? 0.85 : 1,
            color: error ? '#ef4444' : isFocused ? '#3b82f6' : '#9ca3af'
          }}
          className="absolute left-3 top-0 pointer-events-none font-medium origin-left transition-colors"
        >
          {label}
        </motion.label>
      )}

      {/* 输入框容器 */}
      <div className="relative">
        {icon && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
            {icon}
          </div>
        )}

        <input
          {...props}
          onFocus={(e) => {
            setIsFocused(true);
            props.onFocus?.(e);
          }}
          onBlur={(e) => {
            setIsFocused(false);
            setHasValue(e.target.value !== '');
            props.onBlur?.(e);
          }}
          style={{
            borderColor: error ? '#ef4444' : isFocused ? '#3b82f6' : '#475569'
          }}
          className={`
            w-full px-4 py-3 ${icon ? 'pl-10' : ''}
            bg-slate-800 border-2
            rounded-lg
            text-white
            transition-all duration-300
            focus:outline-none
            ${label ? 'pt-6' : ''}
          `}
        />
      </div>

      {/* 错误信息 */}
      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-1 text-sm text-red-400"
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>

      {/* 聚焦指示器 */}
      <motion.div
        initial={false}
        animate={{
          scaleX: isFocused ? 1 : 0,
          backgroundColor: error ? '#ef4444' : '#3b82f6'
        }}
        className="absolute bottom-0 left-0 right-0 h-0.5 origin-center"
      />
    </div>
  );
}

// Textarea 组件
export function AnimatedTextarea({
  label,
  error,
  className = '',
  ...props
}: {
  label?: string;
  error?: string;
  className?: string;
} & React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  const [isFocused, setIsFocused] = useState(false);
  const [hasValue, setHasValue] = useState(false);

  return (
    <div className={`relative ${className}`}>
      {label && (
        <motion.label
          initial={false}
          animate={{
            y: isFocused || hasValue ? 0 : 10,
            scale: isFocused || hasValue ? 0.85 : 1,
            color: error ? '#ef4444' : isFocused ? '#3b82f6' : '#9ca3af'
          }}
          className="absolute left-3 top-2 pointer-events-none font-medium origin-left z-10"
        >
          {label}
        </motion.label>
      )}

      <textarea
        {...props}
        onFocus={(e) => {
          setIsFocused(true);
          props.onFocus?.(e);
        }}
        onBlur={(e) => {
          setIsFocused(false);
          setHasValue(e.target.value !== '');
          props.onBlur?.(e);
        }}
        style={{
          borderColor: error ? '#ef4444' : isFocused ? '#3b82f6' : '#475569'
        }}
        className={`
          w-full px-4 py-3
          bg-slate-800 border-2
          rounded-lg
          text-white
          transition-all duration-300
          focus:outline-none
          resize-none
          ${label ? 'pt-8' : ''}
        `}
      />

      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="mt-1 text-sm text-red-400"
        >
          {error}
        </motion.p>
      )}
    </div>
  );
}

// 开关组件
export function AnimatedSwitch({
  checked,
  onChange,
  label,
  className = ''
}: {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  className?: string;
}) {
  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <motion.button
        onClick={() => onChange(!checked)}
        className={`
          relative w-14 h-7 rounded-full
          transition-colors duration-300
          ${checked ? 'bg-blue-600' : 'bg-slate-700'}
        `}
      >
        <motion.div
          animate={{
            x: checked ? 28 : 2
          }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
          className="absolute top-1 w-5 h-5 bg-white rounded-full shadow-lg"
        />
      </motion.button>
      {label && <span className="text-gray-300">{label}</span>}
    </div>
  );
}
