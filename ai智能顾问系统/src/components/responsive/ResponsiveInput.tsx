/**
 * 响应式输入组件
 * 触摸友好,适配不同屏幕尺寸
 */

import { InputHTMLAttributes, TextareaHTMLAttributes, forwardRef, ReactNode } from 'react';

interface ResponsiveInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
}

export const ResponsiveInput = forwardRef<HTMLInputElement, ResponsiveInputProps>(
  (
    {
      label,
      error,
      helperText,
      icon,
      iconPosition = 'left',
      fullWidth = true,
      className = '',
      ...props
    },
    ref
  ) => {
    return (
      <div className={`${fullWidth ? 'w-full' : ''} ${className}`}>
        {/* 标签 */}
        {label && (
          <label className="block text-sm md:text-base font-medium text-gray-300 mb-2">
            {label}
            {props.required && <span className="text-red-400 ml-1">*</span>}
          </label>
        )}

        {/* 输入框容器 */}
        <div className="relative">
          {/* 左侧图标 */}
          {icon && iconPosition === 'left' && (
            <div className="absolute left-3 md:left-4 top-1/2 -translate-y-1/2 text-gray-400">
              {icon}
            </div>
          )}

          {/* 输入框 */}
          <input
            ref={ref}
            className={`
              w-full
              min-h-[44px]
              px-3 md:px-4 py-2.5 md:py-3
              ${icon && iconPosition === 'left' ? 'pl-10 md:pl-11' : ''}
              ${icon && iconPosition === 'right' ? 'pr-10 md:pr-11' : ''}
              bg-slate-800
              border-2
              ${error ? 'border-red-500' : 'border-slate-700 focus:border-blue-500'}
              rounded-lg md:rounded-xl
              text-sm md:text-base
              text-white
              placeholder-gray-500
              transition-all duration-200
              focus:outline-none focus:ring-2 focus:ring-blue-500/20
              disabled:opacity-50 disabled:cursor-not-allowed
            `}
            {...props}
          />

          {/* 右侧图标 */}
          {icon && iconPosition === 'right' && (
            <div className="absolute right-3 md:right-4 top-1/2 -translate-y-1/2 text-gray-400">
              {icon}
            </div>
          )}
        </div>

        {/* 错误信息或帮助文本 */}
        {(error || helperText) && (
          <p className={`
            mt-1.5 text-xs md:text-sm
            ${error ? 'text-red-400' : 'text-gray-400'}
          `}>
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

ResponsiveInput.displayName = 'ResponsiveInput';

// 文本域组件
interface ResponsiveTextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
  fullWidth?: boolean;
}

export const ResponsiveTextarea = forwardRef<HTMLTextAreaElement, ResponsiveTextareaProps>(
  (
    {
      label,
      error,
      helperText,
      fullWidth = true,
      rows = 4,
      className = '',
      ...props
    },
    ref
  ) => {
    return (
      <div className={`${fullWidth ? 'w-full' : ''} ${className}`}>
        {/* 标签 */}
        {label && (
          <label className="block text-sm md:text-base font-medium text-gray-300 mb-2">
            {label}
            {props.required && <span className="text-red-400 ml-1">*</span>}
          </label>
        )}

        {/* 文本域 */}
        <textarea
          ref={ref}
          rows={rows}
          className={`
            w-full
            px-3 md:px-4 py-2.5 md:py-3
            bg-slate-800
            border-2
            ${error ? 'border-red-500' : 'border-slate-700 focus:border-blue-500'}
            rounded-lg md:rounded-xl
            text-sm md:text-base
            text-white
            placeholder-gray-500
            transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-blue-500/20
            disabled:opacity-50 disabled:cursor-not-allowed
            resize-none
          `}
          {...props}
        />

        {/* 错误信息或帮助文本 */}
        {(error || helperText) && (
          <p className={`
            mt-1.5 text-xs md:text-sm
            ${error ? 'text-red-400' : 'text-gray-400'}
          `}>
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

ResponsiveTextarea.displayName = 'ResponsiveTextarea';

// 选择框组件
export function ResponsiveSelect({
  label,
  error,
  helperText,
  options,
  fullWidth = true,
  className = '',
  ...props
}: {
  label?: string;
  error?: string;
  helperText?: string;
  options: Array<{ value: string; label: string }>;
  fullWidth?: boolean;
} & InputHTMLAttributes<HTMLSelectElement>) {
  return (
    <div className={`${fullWidth ? 'w-full' : ''} ${className}`}>
      {/* 标签 */}
      {label && (
        <label className="block text-sm md:text-base font-medium text-gray-300 mb-2">
          {label}
          {props.required && <span className="text-red-400 ml-1">*</span>}
        </label>
      )}

      {/* 选择框 */}
      <div className="relative">
        <select
          className={`
            w-full
            min-h-[44px]
            px-3 md:px-4 py-2.5 md:py-3
            pr-10 md:pr-11
            bg-slate-800
            border-2
            ${error ? 'border-red-500' : 'border-slate-700 focus:border-blue-500'}
            rounded-lg md:rounded-xl
            text-sm md:text-base
            text-white
            transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-blue-500/20
            disabled:opacity-50 disabled:cursor-not-allowed
            appearance-none
          `}
          {...props}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>

        {/* 下拉箭头 */}
        <div className="absolute right-3 md:right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      {/* 错误信息或帮助文本 */}
      {(error || helperText) && (
        <p className={`
          mt-1.5 text-xs md:text-sm
          ${error ? 'text-red-400' : 'text-gray-400'}
        `}>
          {error || helperText}
        </p>
      )}
    </div>
  );
}

// 复选框组件
export function ResponsiveCheckbox({
  label,
  error,
  className = '',
  ...props
}: {
  label: string;
  error?: string;
} & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div className={className}>
      <label className="flex items-center gap-3 cursor-pointer group">
        <input
          type="checkbox"
          className={`
            w-5 h-5 md:w-6 md:h-6
            rounded
            border-2
            ${error ? 'border-red-500' : 'border-slate-700'}
            bg-slate-800
            text-blue-600
            focus:ring-2 focus:ring-blue-500/20
            focus:ring-offset-2 focus:ring-offset-slate-900
            transition-all duration-200
            cursor-pointer
          `}
          {...props}
        />
        <span className="text-sm md:text-base text-gray-300 group-hover:text-white transition-colors">
          {label}
        </span>
      </label>
      {error && (
        <p className="mt-1.5 text-xs md:text-sm text-red-400">{error}</p>
      )}
    </div>
  );
}

// 单选按钮组
export function ResponsiveRadioGroup({
  label,
  error,
  options,
  name,
  value,
  onChange,
  orientation = 'vertical',
  className = ''
}: {
  label?: string;
  error?: string;
  options: Array<{ value: string; label: string }>;
  name: string;
  value: string;
  onChange: (value: string) => void;
  orientation?: 'horizontal' | 'vertical';
  className?: string;
}) {
  return (
    <div className={className}>
      {label && (
        <label className="block text-sm md:text-base font-medium text-gray-300 mb-3">
          {label}
        </label>
      )}
      
      <div className={`
        flex
        ${orientation === 'horizontal' ? 'flex-row flex-wrap gap-4 md:gap-6' : 'flex-col gap-3'}
      `}>
        {options.map((option) => (
          <label key={option.value} className="flex items-center gap-3 cursor-pointer group">
            <input
              type="radio"
              name={name}
              value={option.value}
              checked={value === option.value}
              onChange={() => onChange(option.value)}
              className={`
                w-5 h-5 md:w-6 md:h-6
                border-2
                ${error ? 'border-red-500' : 'border-slate-700'}
                bg-slate-800
                text-blue-600
                focus:ring-2 focus:ring-blue-500/20
                focus:ring-offset-2 focus:ring-offset-slate-900
                transition-all duration-200
                cursor-pointer
              `}
            />
            <span className="text-sm md:text-base text-gray-300 group-hover:text-white transition-colors">
              {option.label}
            </span>
          </label>
        ))}
      </div>

      {error && (
        <p className="mt-2 text-xs md:text-sm text-red-400">{error}</p>
      )}
    </div>
  );
}
