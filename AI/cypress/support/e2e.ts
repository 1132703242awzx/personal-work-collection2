// Cypress E2E 测试支持文件
/// <reference types="cypress" />

// 自定义命令
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('fillProjectForm', (projectData: {
  name: string;
  description: string;
  techStack: string[];
}) => {
  cy.get('input[name="name"]').type(projectData.name);
  cy.get('textarea[name="description"]').type(projectData.description);
  
  projectData.techStack.forEach(tech => {
    cy.get('input[name="techStack"]').type(`${tech}{enter}`);
  });
});

// TypeScript 声明
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      fillProjectForm(projectData: {
        name: string;
        description: string;
        techStack: string[];
      }): Chainable<void>;
    }
  }
}

export {};
