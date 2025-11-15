/**
 * Axios 实例配置
 * 包含请求/响应拦截器、错误处理、重试机制
 */

import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';
import { API_CONFIG, isDevelopment } from '../../config/api.config';
import { ApiError, ApiResponse } from '../../types';

// 创建 Axios 实例
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: API_CONFIG.HEADERS,
});

// 请求计数器（用于生成请求 ID）
let requestId = 0;

/**
 * 请求拦截器
 */
apiClient.interceptors.request.use(
  (config) => {
    // 生成唯一请求 ID
    const reqId = `req_${Date.now()}_${++requestId}`;
    config.headers['X-Request-ID'] = reqId;

    // 添加认证 Token（如果存在）
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now(),
      };
    }

    // 开发环境日志
    if (isDevelopment) {
      console.log(`[API Request ${reqId}]`, {
        method: config.method?.toUpperCase(),
        url: config.url,
        params: config.params,
        data: config.data,
      });
    }

    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

/**
 * 响应拦截器
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const reqId = response.config.headers['X-Request-ID'];

    // 开发环境日志
    if (isDevelopment) {
      console.log(`[API Response ${reqId}]`, {
        status: response.status,
        data: response.data,
      });
    }

    // 统一处理响应数据
    if (response.data.success === false) {
      const error = new Error(response.data.message || 'API request failed');
      return Promise.reject(error);
    }

    return response;
  },
  async (error: AxiosError<ApiError>) => {
    const reqId = error.config?.headers?.['X-Request-ID'];

    // 开发环境日志
    if (isDevelopment) {
      console.error(`[API Error ${reqId}]`, {
        status: error.response?.status,
        message: error.message,
        data: error.response?.data,
      });
    }

    // 处理特定错误状态码
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          // 未授权 - 清除 Token 并跳转登录
          localStorage.removeItem('auth_token');
          if (isDevelopment) {
            console.warn('[API] 401 Unauthorized - Token cleared');
          }
          // 可以在这里触发跳转到登录页
          break;

        case 403:
          // 禁止访问
          console.error('[API] 403 Forbidden - Access denied');
          break;

        case 404:
          // 资源不存在
          console.error('[API] 404 Not Found');
          break;

        case 429:
          // 请求过于频繁
          console.warn('[API] 429 Too Many Requests - Rate limited');
          break;

        case 500:
        case 502:
        case 503:
        case 504:
          // 服务器错误
          console.error('[API] Server Error', status);
          break;
      }

      // 重试机制
      const config = error.config as AxiosRequestConfig & { _retryCount?: number };
      if (config && shouldRetry(status, config)) {
        config._retryCount = (config._retryCount || 0) + 1;
        
        const delay = API_CONFIG.RETRY.RETRY_DELAY * config._retryCount;
        
        if (isDevelopment) {
          console.log(`[API] Retrying request (${config._retryCount}/${API_CONFIG.RETRY.MAX_RETRIES}) after ${delay}ms`);
        }

        await sleep(delay);
        return apiClient(config);
      }

      // 返回格式化的错误
      return Promise.reject({
        code: data?.error?.code || `HTTP_${status}`,
        message: data?.error?.message || error.message || 'Network error',
        details: data?.error?.details,
        status,
      });
    }

    // 网络错误或请求超时
    if (error.code === 'ECONNABORTED') {
      return Promise.reject({
        code: 'TIMEOUT',
        message: 'Request timeout',
        details: error.message,
      });
    }

    if (!error.response) {
      return Promise.reject({
        code: 'NETWORK_ERROR',
        message: 'Network error, please check your connection',
        details: error.message,
      });
    }

    return Promise.reject(error);
  }
);

/**
 * 判断是否应该重试请求
 */
function shouldRetry(status: number, config: AxiosRequestConfig & { _retryCount?: number }): boolean {
  const retryCount = config._retryCount || 0;
  const maxRetries = API_CONFIG.RETRY.MAX_RETRIES;
  const retryStatuses = API_CONFIG.RETRY.RETRY_STATUS_CODES;

  return (
    retryCount < maxRetries &&
    (retryStatuses as readonly number[]).includes(status) &&
    config.method?.toLowerCase() === 'get' // 只重试 GET 请求
  );
}

/**
 * 延迟函数
 */
function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export default apiClient;
