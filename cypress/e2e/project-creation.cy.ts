/**
 * E2E 测试 - 项目创建流程
 */

describe('项目创建流程', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('应该成功创建一个新项目', () => {
    // 填写项目表单
    cy.fillProjectForm({
      name: '测试项目',
      description: '这是一个 E2E 测试项目',
      techStack: ['React', 'TypeScript', 'Vite'],
    });

    // 提交表单
    cy.get('button[type="submit"]').click();

    // 验证成功提示
    cy.contains('项目创建成功').should('be.visible');

    // 验证跳转到结果页面
    cy.url().should('include', '/results');

    // 验证结果显示
    cy.contains('测试项目').should('be.visible');
    cy.contains('AI 建议').should('be.visible');
  });

  it('应该显示验证错误', () => {
    // 不填写任何内容直接提交
    cy.get('button[type="submit"]').click();

    // 验证错误提示
    cy.contains('项目名称不能为空').should('be.visible');
  });

  it('应该支持清除表单', () => {
    // 填写表单
    cy.get('input[name="name"]').type('测试项目');
    cy.get('textarea[name="description"]').type('测试描述');

    // 点击清除按钮
    cy.get('button').contains('清除').click();

    // 验证表单已清空
    cy.get('input[name="name"]').should('have.value', '');
    cy.get('textarea[name="description"]').should('have.value', '');
  });

  it('应该在移动设备上正常工作', () => {
    // 切换到移动设备视口
    cy.viewport('iphone-x');

    // 填写并提交表单
    cy.fillProjectForm({
      name: '移动端测试项目',
      description: '移动端测试描述',
      techStack: ['React'],
    });

    cy.get('button[type="submit"]').click();

    // 验证成功
    cy.contains('项目创建成功').should('be.visible');
  });

  it('应该处理 API 错误', () => {
    // 模拟 API 错误
    cy.intercept('POST', '/api/advisor/suggestions', {
      statusCode: 500,
      body: {
        success: false,
        error: {
          message: '服务器错误',
        },
      },
    }).as('createProject');

    // 填写并提交表单
    cy.fillProjectForm({
      name: '测试项目',
      description: '测试描述',
      techStack: ['React'],
    });

    cy.get('button[type="submit"]').click();

    // 等待 API 调用
    cy.wait('@createProject');

    // 验证错误提示
    cy.contains('服务器错误').should('be.visible');
  });

  it('应该支持键盘导航', () => {
    // 使用 Tab 键导航
    cy.get('body').tab();
    cy.focused().should('have.attr', 'name', 'name');

    cy.focused().tab();
    cy.focused().should('have.attr', 'name', 'description');

    cy.focused().tab();
    cy.focused().should('have.attr', 'name', 'techStack');
  });

  it('应该显示加载状态', () => {
    // 模拟慢速 API
    cy.intercept('POST', '/api/advisor/suggestions', (req) => {
      req.reply({
        delay: 2000,
        body: {
          success: true,
          data: { suggestions: [] },
        },
      });
    }).as('slowRequest');

    // 填写并提交表单
    cy.fillProjectForm({
      name: '测试项目',
      description: '测试描述',
      techStack: ['React'],
    });

    cy.get('button[type="submit"]').click();

    // 验证加载状态
    cy.get('button[type="submit"]').should('be.disabled');
    cy.contains('加载中').should('be.visible');

    // 等待请求完成
    cy.wait('@slowRequest');

    // 验证加载状态消失
    cy.get('button[type="submit"]').should('not.be.disabled');
  });
});
