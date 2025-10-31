import { useState, useRef, useEffect } from 'react';

interface SmartInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  maxLength?: number;
  rows?: number;
}

const SmartInput = ({
  value,
  onChange,
  placeholder = '请输入内容...',
  label,
  maxLength = 1000,
  rows = 5,
}: SmartInputProps) => {
  const [isFocused, setIsFocused] = useState(false);
  const [charCount, setCharCount] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setCharCount(value.length);
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (newValue.length <= maxLength) {
      onChange(newValue);
      setCharCount(newValue.length);
    }
  };

  const isNearLimit = charCount > maxLength * 0.9;

  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm font-semibold text-slate-300 mb-2">
          {label}
        </label>
      )}
      
      <div
        className={`relative bg-slate-800/50 backdrop-blur-sm border rounded-xl transition-all duration-300 ${
          isFocused
            ? 'border-blue-500 shadow-lg shadow-blue-500/20'
            : 'border-slate-700/50 hover:border-slate-600/50'
        }`}
      >
        <textarea
          ref={textareaRef}
          value={value}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          rows={rows}
          className="w-full px-4 py-3 bg-transparent text-slate-200 placeholder-slate-500 focus:outline-none resize-none"
          style={{ minHeight: `${rows * 1.5}rem` }}
        />

        {/* Character Counter */}
        <div className="absolute bottom-3 right-3 flex items-center space-x-2">
          <span
            className={`text-xs font-medium transition-colors ${
              isNearLimit ? 'text-orange-400' : 'text-slate-500'
            }`}
          >
            {charCount}/{maxLength}
          </span>
          
          {/* Progress Ring */}
          <svg className="w-6 h-6 transform -rotate-90">
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
              className="text-slate-700"
            />
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
              strokeDasharray={`${2 * Math.PI * 10}`}
              strokeDashoffset={`${
                2 * Math.PI * 10 * (1 - charCount / maxLength)
              }`}
              className={`transition-all duration-300 ${
                isNearLimit ? 'text-orange-400' : 'text-blue-400'
              }`}
              strokeLinecap="round"
            />
          </svg>
        </div>

        {/* Focus Glow Effect */}
        {isFocused && (
          <div className="absolute inset-0 rounded-xl bg-blue-500/5 pointer-events-none animate-pulse"></div>
        )}
      </div>

      {/* Markdown Support Hint */}
      <div className="flex items-center space-x-2 text-xs text-slate-500">
        <span>💡</span>
        <span>支持 Markdown 格式</span>
      </div>
    </div>
  );
};

export default SmartInput;
