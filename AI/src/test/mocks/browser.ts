/**
 * MSW Browser 配置 (用于开发环境)
 */

import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

// 设置浏览器 worker
export const worker = setupWorker(...handlers);
