import { useState } from 'react';
import { AIProviderManager, AIProvider, AIConfig } from '../services/AIProviderManager';

const AIConfigTest: React.FC = () => {
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [apiKey, setApiKey] = useState<string>('');
  const [model, setModel] = useState<string>('');
  const [endpoint, setEndpoint] = useState<string>('');
  const [testing, setTesting] = useState<boolean>(false);
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);
  const [debugLogs, setDebugLogs] = useState<string[]>([]);

  const providers = AIProviderManager.getAllProviders();
  const currentConfig = AIProviderManager.getConfigFromEnv();

  const addDebugLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setDebugLogs(prev => [...prev, `[${timestamp}] ${message}`]);
    console.log(message);
  };

  const handleProviderChange = (providerId: string) => {
    setSelectedProvider(providerId);
    const provider = AIProviderManager.getProvider(providerId);
    if (provider) {
      setModel(provider.model);
      setEndpoint(provider.apiEndpoint);
    }
    setResult(null);
  };

  const handleTest = async () => {
    if (!selectedProvider || !apiKey) {
      setResult({
        success: false,
        message: '请选择 AI 提供商并输入 API Key',
      });
      return;
    }

    setTesting(true);
    setResult(null);
    setDebugLogs([]);
    addDebugLog('🚀 开始测试 AI 连接...');
    addDebugLog(`📋 提供商: ${selectedProvider}`);
    addDebugLog(`🔑 API Key: ${apiKey.substring(0, 8)}...`);
    addDebugLog(`🎯 模型: ${model || '默认'}`);

    const testConfig: AIConfig = {
      provider: selectedProvider,
      apiKey,
      model: model || undefined,
      temperature: 0.7,
      maxTokens: 100,
    };

    try {
      addDebugLog('📤 发送测试请求...');
      const testResult = await AIProviderManager.testConnection(testConfig);
      addDebugLog(testResult.success ? '✅ 测试成功!' : '❌ 测试失败');
      addDebugLog(`📨 响应: ${testResult.message}`);
      setResult(testResult);
    } catch (error: any) {
      addDebugLog('❌ 发生错误: ' + error.message);
      setResult({
        success: false,
        message: `测试失败: ${error.message}`,
      });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8">
        <div className="flex items-center gap-3 mb-6">
          <span className="text-4xl">🤖</span>
          <div>
            <h2 className="text-2xl font-bold text-white">AI 配置测试</h2>
            <p className="text-slate-400 text-sm">测试您的 AI API 连接</p>
          </div>
        </div>

        {/* 当前配置状态 */}
        {currentConfig && (
          <div className="mb-6 p-4 bg-green-500/10 border border-green-500/30 rounded-xl">
            <div className="flex items-center gap-2 text-green-400 font-semibold mb-2">
              <span>✅</span>
              <span>当前已配置 AI 提供商</span>
            </div>
            <div className="text-slate-300 text-sm space-y-1">
              <p>• 提供商: {currentConfig.provider}</p>
              <p>• 模型: {currentConfig.model}</p>
              <p>• 状态: 已启用 AI 增强分析</p>
            </div>
          </div>
        )}

        {!currentConfig && (
          <div className="mb-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl">
            <div className="flex items-center gap-2 text-blue-400 font-semibold mb-2">
              <span>ℹ️</span>
              <span>未配置 AI 提供商</span>
            </div>
            <p className="text-slate-400 text-sm">
              当前使用内置智能分析算法。配置 AI 提供商可以获得更详细的分析结果。
            </p>
          </div>
        )}

        {/* 提供商选择 */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              选择 AI 提供商
            </label>
            <select
              value={selectedProvider}
              onChange={(e) => handleProviderChange(e.target.value)}
              className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-slate-200 focus:outline-none focus:border-blue-500 transition-all"
            >
              <option value="">-- 请选择 --</option>
              {providers.map((provider: AIProvider) => (
                <option key={provider.id} value={provider.id}>
                  {provider.name} ({provider.model})
                </option>
              ))}
            </select>
          </div>

          {selectedProvider && (
            <>
              {/* API Key */}
              <div>
                <label className="block text-sm font-semibold text-slate-300 mb-2">
                  API Key <span className="text-red-400">*</span>
                </label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="输入您的 API Key"
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-all"
                />
                <p className="text-slate-500 text-xs mt-1">
                  您的 API Key 仅用于测试，不会被保存
                </p>
              </div>

              {/* Model */}
              <div>
                <label className="block text-sm font-semibold text-slate-300 mb-2">
                  模型名称 (可选)
                </label>
                <input
                  type="text"
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  placeholder="留空使用默认模型"
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-all"
                />
              </div>

              {/* Endpoint */}
              <div>
                <label className="block text-sm font-semibold text-slate-300 mb-2">
                  API 端点 (可选)
                </label>
                <input
                  type="text"
                  value={endpoint}
                  onChange={(e) => setEndpoint(e.target.value)}
                  placeholder="留空使用默认端点"
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-all"
                />
              </div>

              {/* 测试按钮 */}
              <button
                onClick={handleTest}
                disabled={testing || !apiKey}
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold text-white shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {testing ? '测试中...' : '测试连接'}
              </button>
            </>
          )}
        </div>

        {/* 测试结果 */}
        {result && (
          <div
            className={`mt-6 p-4 rounded-xl border ${
              result.success
                ? 'bg-green-500/10 border-green-500/30'
                : 'bg-red-500/10 border-red-500/30'
            }`}
          >
            <div
              className={`flex items-center gap-2 font-semibold mb-2 ${
                result.success ? 'text-green-400' : 'text-red-400'
              }`}
            >
              <span>{result.success ? '✅' : '❌'}</span>
              <span>{result.success ? '连接成功' : '连接失败'}</span>
            </div>
            <p className="text-slate-300 text-sm whitespace-pre-wrap">{result.message}</p>
          </div>
        )}

        {/* 调试日志 */}
        {debugLogs.length > 0 && (
          <div className="mt-6 p-4 bg-slate-800/50 rounded-xl border border-slate-600">
            <h3 className="text-lg font-bold text-slate-300 mb-3 flex items-center gap-2">
              <span>🔍</span>
              <span>调试日志</span>
            </h3>
            <div className="space-y-1 max-h-64 overflow-y-auto">
              {debugLogs.map((log, index) => (
                <div key={index} className="text-xs font-mono text-slate-400 py-1">
                  {log}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 配置说明 */}
        <div className="mt-8 p-4 bg-slate-700/30 rounded-xl">
          <h3 className="text-lg font-bold text-slate-300 mb-3">⚙️ 配置方法</h3>
          <div className="space-y-2 text-sm text-slate-400">
            <p>1. 在项目根目录创建 <code className="text-blue-400">.env.local</code> 文件</p>
            <p>2. 添加以下配置 (以 DeepSeek 为例):</p>
            <pre className="mt-2 p-3 bg-slate-800/50 rounded-lg text-xs overflow-x-auto">
{`VITE_AI_PROVIDER=deepseek
VITE_AI_API_KEY=your-api-key-here
VITE_AI_MODEL=deepseek-chat`}
            </pre>
            <p>3. 重启开发服务器: <code className="text-blue-400">npm run dev</code></p>
            <p>4. 系统将自动使用配置的 AI 进行分析</p>
          </div>
        </div>

        {/* AI 提供商推荐 */}
        <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl">
          <h3 className="text-lg font-bold text-blue-400 mb-3">💡 推荐选择</h3>
          <div className="space-y-3 text-sm text-slate-300">
            <div>
              <p className="font-semibold">• DeepSeek (推荐)</p>
              <p className="text-slate-400 ml-4">性价比最高，中文支持好，国内可用，价格便宜</p>
            </div>
            <div>
              <p className="font-semibold">• OpenAI GPT-4</p>
              <p className="text-slate-400 ml-4">最强大，但价格较贵，需要国际支付</p>
            </div>
            <div>
              <p className="font-semibold">• Claude 3.5 Sonnet</p>
              <p className="text-slate-400 ml-4">长文本处理能力强，适合复杂分析</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIConfigTest;
