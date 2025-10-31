# 🤖 AI 大模型集成指南

## 概述

本项目已完整集成多个主流 AI 大模型，可以大幅提升项目需求分析的深度和准确性。

### ✨ 支持的 AI 提供商

| 提供商 | 模型 | 优势 | 价格 | 国内可用 |
|--------|------|------|------|---------|
| **DeepSeek** | deepseek-chat, deepseek-coder | 性价比极高，中文支持好 | ⭐ 最便宜 | ✅ 是 |
| **OpenAI** | gpt-4, gpt-4-turbo | 最强大，应用最广泛 | 💰 较贵 | ❌ 需代理 |
| **Claude** | claude-3-5-sonnet | 长文本能力强，推理能力好 | 💰 中等 | ❌ 需代理 |
| **Azure OpenAI** | gpt-4 | 企业级，稳定性高 | 💰 较贵 | ✅ 是 |
| **Google Gemini** | gemini-pro | Google 产品，多模态 | 💰 中等 | ❌ 需代理 |

---

## 🚀 快速开始

### 方式 1: 使用 DeepSeek (推荐，最简单)

#### 步骤 1: 获取 API Key

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册账号（支持国内手机号）
3. 进入 [API Keys 页面](https://platform.deepseek.com/api_keys)
4. 创建新的 API Key 并复制

#### 步骤 2: 配置环境变量

在项目根目录创建 `.env.local` 文件:

```bash
# DeepSeek 配置
VITE_AI_PROVIDER=deepseek
VITE_AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VITE_AI_MODEL=deepseek-chat
```

#### 步骤 3: 重启开发服务器

```bash
npm run dev
```

#### 步骤 4: 测试

访问 http://localhost:3002/ai-config 测试连接

---

### 方式 2: 使用 OpenAI GPT-4

#### 步骤 1: 获取 API Key

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录/注册账号（需要国际手机号和信用卡）
3. 进入 [API Keys](https://platform.openai.com/api-keys)
4. 创建新的 API Key

#### 步骤 2: 配置环境变量

```bash
# OpenAI 配置
VITE_AI_PROVIDER=openai
VITE_AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VITE_AI_MODEL=gpt-4
```

#### 步骤 3: 重启并测试

```bash
npm run dev
```

---

### 方式 3: 使用 Claude

#### 步骤 1: 获取 API Key

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册账号
3. 创建 API Key

#### 步骤 2: 配置环境变量

```bash
# Claude 配置
VITE_AI_PROVIDER=claude
VITE_AI_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxx
VITE_AI_MODEL=claude-3-5-sonnet-20241022
```

---

## 📖 完整配置参数

### 必需参数

- `VITE_AI_PROVIDER`: AI 提供商 ID
  - 可选值: `openai`, `deepseek`, `deepseek-coder`, `claude`, `azure-openai`, `gemini`
  
- `VITE_AI_API_KEY`: API 密钥

### 可选参数

- `VITE_AI_MODEL`: 模型名称（留空使用默认模型）
  - OpenAI: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
  - DeepSeek: `deepseek-chat`, `deepseek-coder`
  - Claude: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`

- `VITE_AI_API_ENDPOINT`: 自定义 API 端点（通常不需要）

---

## 🧪 测试 AI 连接

### 方式 1: 使用 Web 界面测试

1. 启动项目: `npm run dev`
2. 访问: http://localhost:3002/ai-config
3. 选择 AI 提供商
4. 输入 API Key
5. 点击"测试连接"

### 方式 2: 使用控制台日志

配置完成后,访问 AI 顾问页面,按 F12 打开控制台:

```javascript
// 成功配置
✅ AI Provider configured: deepseek (deepseek-chat)
🤖 Calling AI: deepseek (deepseek-chat)
✅ AI 分析完成 (deepseek): {model: 'deepseek-chat', tokens: 2345}

// 未配置
ℹ️ No AI provider configured, using built-in intelligent algorithm
💡 使用内置智能分析算法
```

---

## 💡 使用效果对比

### 不使用 AI (内置算法)

**分析时间**: 1-2 秒
**结果内容**:
- ✅ 项目复杂度评估
- ✅ 技术栈推荐 (20-30 项)
- ✅ 开发阶段规划
- ✅ 通用最佳实践建议

### 使用 AI 增强

**分析时间**: 3-6 秒
**结果内容**:
- ✅ 所有内置算法的内容
- ✅ **AI 深度分析**:
  - 架构设计建议 (2-3 段)
  - 技术选型理由 (详细分析)
  - 开发流程建议 (具体方案)
  - 关键挑战和解决方案
  - 部署和运维策略
- ✅ 针对项目特点的个性化建议
- ✅ 更详细的风险评估

---

## 📊 成本估算

### DeepSeek (推荐)

- **输入**: ¥0.001 / 1K tokens
- **输出**: ¥0.002 / 1K tokens
- **单次分析**: 约 3000-5000 tokens
- **成本**: ¥0.01-0.02 / 次
- **100 次分析**: 约 ¥1-2

### OpenAI GPT-4

- **输入**: $0.03 / 1K tokens
- **输出**: $0.06 / 1K tokens
- **单次分析**: 约 3000-5000 tokens
- **成本**: $0.15-0.30 / 次 (约 ¥1-2 / 次)
- **100 次分析**: 约 ¥100-200

### Claude 3.5 Sonnet

- **输入**: $0.003 / 1K tokens
- **输出**: $0.015 / 1K tokens
- **单次分析**: 约 3000-5000 tokens
- **成本**: $0.05-0.10 / 次 (约 ¥0.3-0.7 / 次)
- **100 次分析**: 约 ¥30-70

### 结论

DeepSeek 性价比最高，适合高频使用!

---

## 🔒 安全注意事项

### ⚠️ 重要警告

1. **不要提交 API Key 到 Git**
   ```bash
   # .gitignore 已包含
   .env.local
   .env.*.local
   ```

2. **不要在前端代码中硬编码 API Key**
   - ❌ 错误: `const apiKey = 'sk-xxx...'`
   - ✅ 正确: 使用环境变量 `import.meta.env.VITE_AI_API_KEY`

3. **生产环境建议使用后端代理**
   - 前端直接调用会暴露 API Key
   - 推荐架构: 前端 → 后端 API → AI 服务

4. **设置使用限制**
   - 在 AI 提供商后台设置月度预算
   - 限制单次请求的 token 数量
   - 实施请求频率限制

---

## 🛠️ 高级配置

### 自定义 API 端点

如果使用代理或自建服务:

```bash
VITE_AI_PROVIDER=openai
VITE_AI_API_KEY=sk-xxx
VITE_AI_MODEL=gpt-4
VITE_AI_API_ENDPOINT=https://your-proxy.com/v1/chat/completions
```

### 调整 AI 参数

修改 `src/services/AIProviderManager.ts`:

```typescript
const requestBody = {
  model: config.model,
  messages,
  temperature: 0.7,      // 创造性 (0-2)
  max_tokens: 4000,      // 最大输出
  top_p: 0.9,           // 多样性
  frequency_penalty: 0,  // 重复惩罚
  presence_penalty: 0,   // 主题惩罚
};
```

---

## 🐛 故障排查

### 问题 1: 连接测试失败

**可能原因**:
- API Key 错误
- 网络问题（需要代理）
- API 端点配置错误
- 账户余额不足

**解决方案**:
1. 检查 API Key 是否正确复制
2. 测试网络连接
3. 查看浏览器控制台详细错误
4. 检查 AI 提供商后台余额

### 问题 2: 分析时没有使用 AI

**现象**: 控制台显示 "使用内置智能分析算法"

**原因**: 环境变量未生效

**解决方案**:
1. 确认 `.env.local` 文件在项目根目录
2. 确认文件名正确（不是 `.env.local.txt`）
3. 重启开发服务器: `Ctrl+C` 然后 `npm run dev`
4. 清除浏览器缓存 `Ctrl+Shift+R`

### 问题 3: API 请求超时

**原因**: 网络问题或 AI 服务过载

**解决方案**:
1. 检查网络连接
2. 尝试使用其他 AI 提供商
3. 增加请求超时时间

### 问题 4: 返回结果为空

**原因**: Token 限制或模型问题

**解决方案**:
1. 增加 `max_tokens` 限制
2. 更换模型（如 gpt-4-turbo）
3. 简化输入内容

---

## 📈 性能优化

### 1. 缓存策略

对于相同的输入,可以缓存结果:

```typescript
// 未来版本将实现
const cacheKey = generateHash(requirement);
if (cache.has(cacheKey)) {
  return cache.get(cacheKey);
}
```

### 2. 请求节流

限制用户请求频率:

```typescript
// 实施 Rate Limiting
let lastRequestTime = 0;
const MIN_INTERVAL = 3000; // 3秒

if (Date.now() - lastRequestTime < MIN_INTERVAL) {
  throw new Error('请求过于频繁,请稍后再试');
}
```

### 3. 降级策略

AI 失败时自动降级到内置算法（已实现）:

```typescript
try {
  return await analyzeWithAI(requirement);
} catch (error) {
  console.warn('AI 失败,使用内置算法');
  return analyzeWithIntelligentAlgorithm(requirement);
}
```

---

## 🎯 最佳实践

### 开发环境

- ✅ 使用 DeepSeek (便宜)
- ✅ 设置较小的 max_tokens (节省成本)
- ✅ 使用 `.env.local` 配置

### 生产环境

- ✅ 使用后端代理 AI API
- ✅ 实施请求频率限制
- ✅ 记录 AI 使用情况
- ✅ 监控成本和性能
- ✅ 设置月度预算告警

### 团队协作

- ✅ 每个开发者使用自己的 API Key
- ✅ 测试环境使用独立账户
- ✅ 生产环境使用企业账户
- ✅ 定期审查 API 使用情况

---

## 📚 相关资源

### 官方文档

- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [OpenAI API 文档](https://platform.openai.com/docs/)
- [Claude API 文档](https://docs.anthropic.com/)
- [Azure OpenAI 文档](https://learn.microsoft.com/azure/ai-services/openai/)

### 获取 API Key

- [DeepSeek API Keys](https://platform.deepseek.com/api_keys) ⭐ 推荐
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Claude API Keys](https://console.anthropic.com/)
- [Google AI Studio](https://makersuite.google.com/app/apikey)

### 价格对比

- [DeepSeek 价格](https://platform.deepseek.com/api-docs/pricing/)
- [OpenAI 价格](https://openai.com/pricing)
- [Claude 价格](https://www.anthropic.com/pricing)

---

## 💬 常见问题

### Q1: 必须配置 AI 吗？

**A**: 不是必须的。不配置 AI 时,系统使用内置的智能分析算法(完全免费),也能提供高质量的分析结果。配置 AI 后可以获得更深入、更个性化的分析。

### Q2: 哪个 AI 提供商最好？

**A**: 
- **个人/小团队**: DeepSeek (性价比最高)
- **企业级**: Azure OpenAI (稳定可靠)
- **追求最强**: OpenAI GPT-4 (能力最强)
- **长文本**: Claude (上下文窗口大)

### Q3: 成本可控吗？

**A**: 可控。每次分析约 ¥0.01-2 元,可以在 AI 提供商后台设置月度预算上限。

### Q4: 支持流式输出吗？

**A**: 当前版本暂不支持,未来版本会实现流式输出以提升用户体验。

### Q5: 可以同时配置多个 AI 吗？

**A**: 当前版本只支持一个 AI 提供商,未来版本会支持多 AI 负载均衡。

---

**最后更新**: 2025-10-24  
**版本**: 2.0.0  
**作者**: AI 智能开发顾问团队
