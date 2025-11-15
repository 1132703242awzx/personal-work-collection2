import { useEffect, useState } from 'react';

interface ProgressIndicatorProps {
  progress: number; // 0-100
  status?: 'loading' | 'success' | 'error';
  message?: string;
  showPercentage?: boolean;
}

const ProgressIndicator = ({
  progress,
  status = 'loading',
  message,
  showPercentage = true,
}: ProgressIndicatorProps) => {
  const [displayProgress, setDisplayProgress] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDisplayProgress(progress);
    }, 100);
    return () => clearTimeout(timer);
  }, [progress]);

  const statusConfig = {
    loading: {
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-500/20',
      icon: (
        <svg
          className="w-5 h-5 animate-spin"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      ),
    },
    success: {
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-500/20',
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
            clipRule="evenodd"
          />
        </svg>
      ),
    },
    error: {
      color: 'from-red-500 to-pink-500',
      bgColor: 'bg-red-500/20',
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clipRule="evenodd"
          />
        </svg>
      ),
    },
  };

  const config = statusConfig[status];

  return (
    <div className="space-y-4">
      {/* Progress Bar */}
      <div className="relative">
        <div className="h-3 bg-slate-800/50 backdrop-blur-sm rounded-full overflow-hidden border border-slate-700/50">
          <div
            className={`h-full bg-gradient-to-r ${config.color} transition-all duration-500 ease-out relative`}
            style={{ width: `${displayProgress}%` }}
          >
            {/* Shimmer Effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
          </div>
        </div>

        {/* Percentage Badge */}
        {showPercentage && (
          <div
            className="absolute -top-1 transition-all duration-500 ease-out"
            style={{ left: `calc(${displayProgress}% - 1.5rem)` }}
          >
            <div className={`px-2 py-1 ${config.bgColor} backdrop-blur-sm rounded-lg border border-slate-700/50`}>
              <span className={`text-xs font-bold bg-gradient-to-r ${config.color} bg-clip-text text-transparent`}>
                {Math.round(displayProgress)}%
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Status Message */}
      {message && (
        <div className="flex items-center space-x-3">
          <div className={`flex-shrink-0 text-white ${config.bgColor} p-2 rounded-lg`}>
            {config.icon}
          </div>
          <p className="text-sm text-slate-300 animate-fadeIn">{message}</p>
        </div>
      )}

      {/* Loading Dots */}
      {status === 'loading' && (
        <div className="flex items-center justify-center space-x-2">
          <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce animation-delay-200"></div>
          <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce animation-delay-400"></div>
        </div>
      )}
    </div>
  );
};

export default ProgressIndicator;
