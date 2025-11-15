/**
 * AI 提供商配置和管理服务
 * 支持 OpenAI、DeepSeek、Claude 等多个 AI 提供商
 */

export interface AIProvider {
  id: string;
  name: string;
  apiEndpoint: string;
  model: string;
  enabled: boolean;
  supportsStreaming?: boolean;
}

export interface AIConfig {
  provider: string;
  apiKey: string;
  model?: string;
  temperature?: number;
  maxTokens?: number;
}

export interface AIMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface AIResponse {
  content: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  model?: string;
  provider?: string;
}

/**
 * AI 提供商管理类
 */
export class AIProviderManager {
  // 预定义的 AI 提供商配置
  private static readonly PROVIDERS: Record<string, AIProvider> = {
    openai: {
      id: 'openai',
      name: 'OpenAI GPT',
      apiEndpoint: 'https://api.openai.com/v1/chat/completions',
      model: 'gpt-4',
      enabled: true,
      supportsStreaming: true,
    },
    deepseek: {
      id: 'deepseek',
      name: 'DeepSeek',
      apiEndpoint: 'https://api.deepseek.com/v1/chat/completions',
      model: 'deepseek-chat',
      enabled: true,
      supportsStreaming: true,
    },
    'deepseek-coder': {
      id: 'deepseek-coder',
      name: 'DeepSeek Coder',
      apiEndpoint: 'https://api.deepseek.com/v1/chat/completions',
      model: 'deepseek-coder',
      enabled: true,
      supportsStreaming: true,
    },
    claude: {
      id: 'claude',
      name: 'Anthropic Claude',
      apiEndpoint: 'https://api.anthropic.com/v1/messages',
      model: 'claude-3-5-sonnet-20241022',
      enabled: true,
      supportsStreaming: true,
    },
    'azure-openai': {
      id: 'azure-openai',
      name: 'Azure OpenAI',
      apiEndpoint: '', // 需要用户配置
      model: 'gpt-4',
      enabled: true,
      supportsStreaming: true,
    },
    gemini: {
      id: 'gemini',
      name: 'Google Gemini',
      apiEndpoint: 'https://generativelanguage.googleapis.com/v1/models',
      model: 'gemini-pro',
      enabled: true,
      supportsStreaming: false,
    },
  };

  /**
   * 获取所有可用的 AI 提供商
   */
  static getAllProviders(): AIProvider[] {
    return Object.values(this.PROVIDERS);
  }

  /**
   * 获取指定的 AI 提供商
   */
  static getProvider(providerId: string): AIProvider | null {
    return this.PROVIDERS[providerId] || null;
  }

  /**
   * 从环境变量获取配置
   */
  static getConfigFromEnv(): AIConfig | null {
    const provider = import.meta.env.VITE_AI_PROVIDER;
    const apiKey = import.meta.env.VITE_AI_API_KEY;
    const model = import.meta.env.VITE_AI_MODEL;

    console.log('🔍 读取环境变量:', {
      provider: provider || '未设置',
      hasApiKey: !!apiKey,
      apiKeyPrefix: apiKey ? apiKey.substring(0, 8) + '...' : '未设置',
      model: model || '使用默认',
    });

    if (!provider || !apiKey) {
      console.warn('⚠️ AI 配置不完整: provider 或 apiKey 未设置');
      return null;
    }

    const providerConfig = this.PROVIDERS[provider];
    if (!providerConfig) {
      console.warn(`Unknown AI provider: ${provider}`);
      return null;
    }

    return {
      provider,
      apiKey,
      model: model || providerConfig.model,
      temperature: 0.7,
      maxTokens: 4000,
    };
  }

  /**
   * 调用 OpenAI 兼容的 API
   */
  static async callOpenAICompatibleAPI(
    config: AIConfig,
    messages: AIMessage[],
    signal?: AbortSignal
  ): Promise<AIResponse> {
    const provider = this.getProvider(config.provider);
    if (!provider) {
      throw new Error(`Provider not found: ${config.provider}`);
    }

    const endpoint = import.meta.env.VITE_AI_API_ENDPOINT || provider.apiEndpoint;

    const requestBody: any = {
      model: config.model || provider.model,
      messages,
      temperature: config.temperature || 0.7,
      max_tokens: config.maxTokens || 4000,
    };

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // 根据不同提供商设置不同的认证头
    if (config.provider === 'openai' || config.provider === 'deepseek' || config.provider === 'deepseek-coder') {
      headers['Authorization'] = `Bearer ${config.apiKey}`;
    } else if (config.provider === 'azure-openai') {
      headers['api-key'] = config.apiKey;
    }

    console.log('🌐 准备发送 AI 请求:', {
      endpoint,
      model: requestBody.model,
      messagesCount: messages.length,
      hasAuth: !!headers['Authorization'],
    });

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody),
        signal,
      });

      console.log('📨 收到 AI 响应:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('❌ AI API 错误响应:', errorData);
        throw new Error(
          `AI API request failed: ${response.status} ${response.statusText}\n${JSON.stringify(errorData, null, 2)}`
        );
      }

      const data = await response.json();
      console.log('✅ AI 响应解析成功:', {
        model: data.model,
        totalTokens: data.usage?.total_tokens,
        contentLength: data.choices?.[0]?.message?.content?.length,
      });

      return {
        content: data.choices[0].message.content,
        usage: {
          promptTokens: data.usage?.prompt_tokens || 0,
          completionTokens: data.usage?.completion_tokens || 0,
          totalTokens: data.usage?.total_tokens || 0,
        },
        model: data.model,
        provider: config.provider,
      };
    } catch (error: any) {
      if (error.name === 'AbortError') {
        throw new Error('AI request was cancelled');
      }
      throw error;
    }
  }

  /**
   * 调用 Claude API
   */
  static async callClaudeAPI(
    config: AIConfig,
    messages: AIMessage[],
    signal?: AbortSignal
  ): Promise<AIResponse> {
    const provider = this.getProvider('claude');
    if (!provider) {
      throw new Error('Claude provider not found');
    }

    const endpoint = import.meta.env.VITE_AI_API_ENDPOINT || provider.apiEndpoint;

    // Claude API 格式转换
    const systemMessage = messages.find(m => m.role === 'system')?.content || '';
    const userMessages = messages.filter(m => m.role !== 'system');

    const requestBody = {
      model: config.model || provider.model,
      max_tokens: config.maxTokens || 4000,
      temperature: config.temperature || 0.7,
      system: systemMessage,
      messages: userMessages.map(m => ({
        role: m.role,
        content: m.content,
      })),
    };

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': config.apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify(requestBody),
        signal,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          `Claude API request failed: ${response.status} ${response.statusText}\n${JSON.stringify(errorData, null, 2)}`
        );
      }

      const data = await response.json();

      return {
        content: data.content[0].text,
        usage: {
          promptTokens: data.usage?.input_tokens || 0,
          completionTokens: data.usage?.output_tokens || 0,
          totalTokens: (data.usage?.input_tokens || 0) + (data.usage?.output_tokens || 0),
        },
        model: data.model,
        provider: 'claude',
      };
    } catch (error: any) {
      if (error.name === 'AbortError') {
        throw new Error('AI request was cancelled');
      }
      throw error;
    }
  }

  /**
   * 统一的 AI 调用接口
   */
  static async callAI(
    config: AIConfig,
    messages: AIMessage[],
    signal?: AbortSignal
  ): Promise<AIResponse> {
    console.log(`🤖 Calling AI: ${config.provider} (${config.model})`);
    
    if (config.provider === 'claude') {
      return this.callClaudeAPI(config, messages, signal);
    } else {
      // OpenAI 兼容的 API (OpenAI, DeepSeek, Azure OpenAI 等)
      return this.callOpenAICompatibleAPI(config, messages, signal);
    }
  }

  /**
   * 测试 AI 连接
   */
  static async testConnection(config: AIConfig): Promise<{ success: boolean; message: string }> {
    try {
      const messages: AIMessage[] = [
        {
          role: 'system',
          content: 'You are a helpful assistant.',
        },
        {
          role: 'user',
          content: 'Say "Hello" in one word.',
        },
      ];

      const response = await this.callAI(config, messages);
      
      return {
        success: true,
        message: `连接成功! 模型: ${response.model || config.model}, 响应: ${response.content.substring(0, 50)}`,
      };
    } catch (error: any) {
      return {
        success: false,
        message: `连接失败: ${error.message}`,
      };
    }
  }
}
