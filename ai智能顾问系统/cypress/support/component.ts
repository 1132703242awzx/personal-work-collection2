// Cypress 组件测试支持文件
/// <reference types="cypress" />

import { mount } from 'cypress/react18';

// 添加自定义命令
Cypress.Commands.add('mount', mount);

// TypeScript 声明
declare global {
  namespace Cypress {
    interface Chainable {
      mount: typeof mount;
    }
  }
}

export {};
