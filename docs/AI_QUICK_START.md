# 🚀 AI 集成快速开始 (5 分钟)

## 最简单的方式 - 使用 DeepSeek

### 第 1 步: 获取 API Key (2 分钟)

1. 打开 [DeepSeek 官网](https://www.deepseek.com/)
2. 点击右上角"注册/登录"
3. 使用手机号注册(支持国内手机号)
4. 进入 [API Keys 页面](https://platform.deepseek.com/api_keys)
5. 点击"Create API Key"
6. 复制生成的 API Key (以 `sk-` 开头)

💡 **提示**: DeepSeek 新用户送免费额度,可以免费测试!

---

### 第 2 步: 配置项目 (1 分钟)

在项目根目录(与 `package.json` 同级)创建文件 `.env.local`:

**Windows 用户**:
```powershell
# 在项目根目录执行
New-Item -Path .env.local -ItemType File
```

**Mac/Linux 用户**:
```bash
touch .env.local
```

然后编辑 `.env.local`,添加以下内容:

```bash
VITE_AI_PROVIDER=deepseek
VITE_AI_API_KEY=sk-你的API密钥
VITE_AI_MODEL=deepseek-chat
```

⚠️ **重要**: 将 `sk-你的API密钥` 替换为第 1 步复制的实际 API Key!

---

### 第 3 步: 重启项目 (1 分钟)

1. **停止当前运行的服务器** (在终端按 `Ctrl+C`)

2. **重新启动**:
   ```bash
   npm run dev
   ```

3. **查看启动日志**,应该显示:
   ```
   ✅ AI Provider configured: deepseek (deepseek-chat)
   ```

---

### 第 4 步: 测试 AI (1 分钟)

#### 方式 A: 测试连接

1. 浏览器打开: http://localhost:3002/ai-config
2. 看到绿色的 "✅ 当前已配置 AI 提供商"
3. 如果未显示,按 `Ctrl+Shift+R` 强制刷新

#### 方式 B: 直接使用

1. 打开: http://localhost:3002/advisor
2. 填写项目信息:
   ```
   项目名称: AI 测试项目
   项目描述: 测试 AI 集成功能
   ```
3. 点击"开始分析"
4. 按 F12 打开控制台,查看日志:
   ```
   🤖 尝试使用 AI 增强分析...
   🤖 Calling AI: deepseek (deepseek-chat)
   ✅ AI 分析完成 (deepseek): {model: 'deepseek-chat', tokens: 2345}
   ```

---

## ✅ 完成!

现在您的项目已经集成了 DeepSeek AI!

### 效果对比

**不使用 AI**:
- 分析时间: 1-2 秒
- 结果长度: 约 2000 字
- 内容: 通用建议和推荐

**使用 AI 增强**:
- 分析时间: 3-6 秒 
- 结果长度: 约 5000+ 字
- 内容: 
  - ✅ 所有内置算法的结果
  - ✅ AI 深度架构分析
  - ✅ 详细的技术选型理由
  - ✅ 具体的开发流程建议
  - ✅ 潜在挑战和解决方案
  - ✅ 部署运维策略

---

## 🎯 下一步

### 查看详细文档
- [完整 AI 集成指南](./AI_INTEGRATION_GUIDE.md)
- [支持的 AI 提供商列表](./AI_INTEGRATION_GUIDE.md#支持的-ai-提供商)
- [成本估算](./AI_INTEGRATION_GUIDE.md#成本估算)

### 尝试其他 AI
- [OpenAI GPT-4](./AI_INTEGRATION_GUIDE.md#方式-2-使用-openai-gpt-4)
- [Claude 3.5](./AI_INTEGRATION_GUIDE.md#方式-3-使用-claude)
- [Azure OpenAI](./AI_INTEGRATION_GUIDE.md#azure-openai)

### 高级功能
- 自定义 AI 参数
- 实施成本控制
- 生产环境部署

---

## 🐛 遇到问题?

### 问题 1: 控制台显示 "使用内置智能分析算法"

**原因**: 环境变量未生效

**解决**:
1. 确认 `.env.local` 在项目根目录
2. 确认文件内容正确
3. 重启服务器: `Ctrl+C` → `npm run dev`
4. 刷新浏览器: `Ctrl+Shift+R`

### 问题 2: API 调用失败

**可能原因**:
- API Key 错误
- 账户余额不足
- 网络问题

**解决**:
1. 访问 http://localhost:3002/ai-config
2. 使用测试工具验证 API Key
3. 查看详细错误信息

### 问题 3: .env.local 文件不存在

**解决**:
```bash
# 在项目根目录执行
cd c:\Users\11327\react-app
echo VITE_AI_PROVIDER=deepseek > .env.local
echo VITE_AI_API_KEY=sk-your-key >> .env.local
echo VITE_AI_MODEL=deepseek-chat >> .env.local
```

然后用记事本编辑 `.env.local`,替换 API Key。

---

## 💰 成本说明

DeepSeek 定价:
- 输入: ¥0.001 / 1K tokens
- 输出: ¥0.002 / 1K tokens
- 单次分析: 约 ¥0.01-0.02
- 免费额度: 新用户赠送

**100 次分析约需 ¥1-2 元** 🎉

---

## 📱 联系支持

如果遇到问题,请:
1. 查看 [完整文档](./AI_INTEGRATION_GUIDE.md)
2. 查看浏览器控制台错误信息
3. 提交 Issue 到项目仓库

---

**最后更新**: 2025-10-24  
**预计用时**: 5 分钟  
**难度**: ⭐ 非常简单
