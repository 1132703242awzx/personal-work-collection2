/**
 * MSW Server 配置
 */

import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// 设置测试服务器
export const server = setupServer(...handlers);
