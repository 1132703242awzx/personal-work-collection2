import { useState } from 'react';

interface LogEntry {
  timestamp: string;
  message: string;
  type: 'info' | 'success' | 'error';
}

const AIDebugTest: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addLog = (message: string, type: 'info' | 'success' | 'error' = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { timestamp, message, type }]);
  };

  const clearLogs = () => {
    setLogs([]);
  };

  const testEnvVariables = () => {
    addLog('🔍 检查环境变量配置...', 'info');
    
    const provider = import.meta.env.VITE_AI_PROVIDER;
    const apiKey = import.meta.env.VITE_AI_API_KEY;
    const model = import.meta.env.VITE_AI_MODEL;

    const checks = {
      'VITE_AI_PROVIDER': provider || '未设置',
      'VITE_AI_API_KEY': apiKey ? apiKey.substring(0, 8) + '...' : '未设置',
      'VITE_AI_MODEL': model || '未设置',
    };

    addLog('环境变量状态:\n' + JSON.stringify(checks, null, 2), 'info');

    if (!provider || !apiKey) {
      addLog('❌ 环境变量未正确配置! 请检查 .env.local 文件', 'error');
      addLog('提示: 确保已重启开发服务器', 'error');
    } else {
      addLog('✅ 环境变量配置正确', 'success');
    }
  };

  const testSimpleCall = async () => {
    setIsLoading(true);
    addLog('🚀 开始测试简单 API 调用...', 'info');
    
    const API_KEY = import.meta.env.VITE_AI_API_KEY;
    const API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';

    if (!API_KEY) {
      addLog('❌ API Key 未配置', 'error');
      setIsLoading(false);
      return;
    }

    const requestBody = {
      model: 'deepseek-chat',
      messages: [
        {
          role: 'user',
          content: '你好,请回复"测试成功"'
        }
      ],
      max_tokens: 20,
      temperature: 0.7
    };

    addLog('📤 发送请求:\n' + JSON.stringify(requestBody, null, 2), 'info');

    try {
      const startTime = Date.now();
      
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        },
        body: JSON.stringify(requestBody)
      });

      const duration = Date.now() - startTime;
      addLog(`📨 收到响应 (耗时: ${duration}ms)`, 'info');
      addLog(`状态: ${response.status} ${response.statusText}`, 'info');

      if (!response.ok) {
        const errorData = await response.json();
        addLog('❌ API 调用失败:\n' + JSON.stringify(errorData, null, 2), 'error');
        setIsLoading(false);
        return;
      }

      const data = await response.json();
      addLog('✅ API 调用成功!', 'success');
      addLog('响应内容:\n' + JSON.stringify(data, null, 2), 'success');
      addLog(`💬 AI 回复: ${data.choices[0].message.content}`, 'success');
      addLog(`📊 Token 使用: ${data.usage.total_tokens} tokens (输入: ${data.usage.prompt_tokens}, 输出: ${data.usage.completion_tokens})`, 'success');
      addLog(`💰 预估成本: ¥${(data.usage.total_tokens * 0.001 * 0.001).toFixed(6)}`, 'success');

    } catch (error: any) {
      addLog('❌ 请求失败: ' + error.message, 'error');
      addLog('错误详情:\n' + error.stack, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const testFullAnalysis = async () => {
    setIsLoading(true);
    addLog('🔬 开始测试完整项目分析...', 'info');
    
    const API_KEY = import.meta.env.VITE_AI_API_KEY;
    const API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';

    if (!API_KEY) {
      addLog('❌ API Key 未配置', 'error');
      setIsLoading(false);
      return;
    }

    const requestBody = {
      model: 'deepseek-chat',
      messages: [
        {
          role: 'system',
          content: '你是一位资深的软件架构师和技术顾问，拥有 15 年以上的项目经验。'
        },
        {
          role: 'user',
          content: `我需要开发一个"在线教育平台"项目。

项目描述: 提供在线课程、直播教学、作业提交等功能

请简要给出技术建议(100字内)。`
        }
      ],
      max_tokens: 500,
      temperature: 0.7
    };

    addLog('📤 发送完整分析请求...', 'info');

    try {
      const startTime = Date.now();
      
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        },
        body: JSON.stringify(requestBody)
      });

      const duration = Date.now() - startTime;
      addLog(`📨 收到响应 (耗时: ${duration}ms)`, 'info');

      if (!response.ok) {
        const errorData = await response.json();
        addLog('❌ API 调用失败:\n' + JSON.stringify(errorData, null, 2), 'error');
        setIsLoading(false);
        return;
      }

      const data = await response.json();
      addLog('✅ 完整分析成功!', 'success');
      addLog(`💬 AI 分析结果:\n${data.choices[0].message.content}`, 'success');
      addLog(`📊 Token 使用: ${data.usage.total_tokens} tokens`, 'success');
      addLog(`💰 预估成本: ¥${(data.usage.total_tokens * 0.001 * 0.001).toFixed(6)}`, 'success');

    } catch (error: any) {
      addLog('❌ 请求失败: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700">
        <h1 className="text-3xl font-bold text-white mb-2 flex items-center space-x-3">
          <span>🤖</span>
          <span>AI 调用测试工具</span>
        </h1>
        <p className="text-slate-400 mb-6">此工具用于测试 DeepSeek API 是否正常工作</p>

        <div className="flex flex-wrap gap-3 mb-6">
          <button
            onClick={testEnvVariables}
            disabled={isLoading}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            1. 检查环境变量
          </button>
          <button
            onClick={testSimpleCall}
            disabled={isLoading}
            className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            2. 测试简单调用
          </button>
          <button
            onClick={testFullAnalysis}
            disabled={isLoading}
            className="px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            3. 测试完整分析
          </button>
          <button
            onClick={clearLogs}
            disabled={isLoading}
            className="px-4 py-2 bg-slate-600 hover:bg-slate-700 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            清空结果
          </button>
        </div>

        {isLoading && (
          <div className="mb-4 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-center space-x-3">
            <div className="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
            <span className="text-blue-400">处理中...</span>
          </div>
        )}

        <div className="space-y-2 max-h-[600px] overflow-y-auto">
          {logs.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <p>点击上方按钮开始测试</p>
            </div>
          ) : (
            logs.map((log, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-l-4 ${
                  log.type === 'error'
                    ? 'bg-red-500/10 border-red-500'
                    : log.type === 'success'
                    ? 'bg-green-500/10 border-green-500'
                    : 'bg-blue-500/10 border-blue-500'
                }`}
              >
                <div className="flex items-start space-x-3">
                  <span className="text-xs text-slate-500 mt-1">[{log.timestamp}]</span>
                  <pre className="flex-1 text-sm font-mono whitespace-pre-wrap break-words text-slate-300">
                    {log.message}
                  </pre>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="mt-6 p-6 bg-yellow-500/10 border border-yellow-500/30 rounded-xl">
        <h3 className="text-lg font-bold text-yellow-400 mb-3 flex items-center space-x-2">
          <span>💡</span>
          <span>使用提示</span>
        </h3>
        <ul className="space-y-2 text-sm text-slate-400">
          <li>• <strong>步骤 1</strong>: 先点击"检查环境变量",确认配置已加载</li>
          <li>• <strong>步骤 2</strong>: 点击"测试简单调用",验证 API 连接是否正常</li>
          <li>• <strong>步骤 3</strong>: 点击"测试完整分析",模拟真实项目分析场景</li>
          <li>• <strong>注意</strong>: 如果环境变量显示"未设置",请确保已重启开发服务器</li>
        </ul>
      </div>
    </div>
  );
};

export default AIDebugTest;
