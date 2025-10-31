import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('错误边界捕获到错误:', error, errorInfo);
    
    this.setState({
      error,
      errorInfo,
    });

    // 这里可以将错误发送到错误追踪服务
    // logErrorToService(error, errorInfo);
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      // 自定义错误 UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // 默认错误 UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4">
          <div className="max-w-2xl w-full">
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-8 shadow-2xl">
              {/* 错误图标 */}
              <div className="text-center mb-6">
                <div className="inline-block p-6 bg-red-500/10 rounded-full mb-4">
                  <span className="text-6xl">⚠️</span>
                </div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  哎呀，出错了！
                </h1>
                <p className="text-slate-400 text-lg">
                  应用遇到了一个意外错误
                </p>
              </div>

              {/* 错误详情 */}
              {process.env.NODE_ENV === 'development' && (
                <div className="mb-6">
                  <details className="bg-slate-900/50 rounded-lg p-4 border border-slate-700">
                    <summary className="cursor-pointer text-slate-300 font-semibold mb-2">
                      错误详情 (开发模式)
                    </summary>
                    <div className="mt-4 space-y-4">
                      {this.state.error && (
                        <div>
                          <p className="text-red-400 font-mono text-sm mb-2">
                            {this.state.error.toString()}
                          </p>
                          {this.state.error.stack && (
                            <pre className="text-slate-400 text-xs overflow-x-auto bg-slate-950 p-3 rounded">
                              {this.state.error.stack}
                            </pre>
                          )}
                        </div>
                      )}
                      {this.state.errorInfo && (
                        <div>
                          <p className="text-slate-400 text-sm font-semibold mb-2">
                            组件堆栈:
                          </p>
                          <pre className="text-slate-400 text-xs overflow-x-auto bg-slate-950 p-3 rounded">
                            {this.state.errorInfo.componentStack}
                          </pre>
                        </div>
                      )}
                    </div>
                  </details>
                </div>
              )}

              {/* 操作按钮 */}
              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={this.handleReset}
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 shadow-lg shadow-blue-500/30"
                >
                  重试
                </button>
                <button
                  onClick={() => window.location.href = '/'}
                  className="flex-1 px-6 py-3 bg-slate-700 text-white rounded-xl font-semibold hover:bg-slate-600 transition-all duration-300"
                >
                  返回首页
                </button>
                <button
                  onClick={() => window.location.reload()}
                  className="flex-1 px-6 py-3 bg-slate-700 text-white rounded-xl font-semibold hover:bg-slate-600 transition-all duration-300"
                >
                  刷新页面
                </button>
              </div>

              {/* 帮助信息 */}
              <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                <p className="text-blue-400 text-sm">
                  💡 <strong>建议:</strong> 如果问题持续存在，请尝试清除浏览器缓存或联系技术支持。
                </p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
