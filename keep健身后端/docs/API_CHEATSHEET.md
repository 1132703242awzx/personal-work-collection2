# Keep健身后端 - API速查表

## 🔐 认证系统 `/api/auth`

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/register` | 用户注册 | ❌ |
| POST | `/login` | 用户登录 | ❌ |
| POST | `/refresh` | 刷新令牌 | ❌ |
| POST | `/logout` | 用户登出 | ✅ |
| GET | `/me` | 获取当前用户 | ✅ |
| POST | `/password/change` | 修改密码 | ✅ |
| POST | `/password/reset/request` | 请求重置密码 | ❌ |
| POST | `/password/reset` | 重置密码 | ❌ |
| POST | `/wechat/login` | 微信登录 | ❌ |
| POST | `/apple/login` | Apple登录 | ❌ |
| POST | `/third-party/bind` | 绑定第三方 | ✅ |
| DELETE | `/third-party/unbind` | 解绑第三方 | ✅ |

---

## 🏋️ 训练计划 `/api/plans`

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/` | 创建训练计划 | ✅ |
| GET | `/` | 获取计划列表 | ✅ |
| GET | `/{id}` | 获取计划详情 | ✅ |
| PUT | `/{id}` | 更新计划 | ✅ |
| DELETE | `/{id}` | 删除计划 | ✅ |
| POST | `/{id}/start` | 开始执行计划 | ✅ |
| POST | `/{id}/copy` | 复制模板 | ✅ |
| GET | `/{id}/progress` | 获取进度 | ✅ |

---

## 📝 枚举值参考

### 难度等级 (difficulty)
```
beginner      - 初级
intermediate  - 中级
advanced      - 高级
```

### 目标肌群 (muscle_group / target_muscle_group)
```
chest      - 胸部
back       - 背部
shoulders  - 肩部
arms       - 手臂
legs       - 腿部
core       - 核心
cardio     - 有氧
full_body  - 全身
```

### 训练目标 (goal)
```
减脂
增肌
塑形
体能
```

### 动作类型 (exercise_type)
```
力量
有氧
拉伸
```

### 用户角色 (role)
```
user         - 普通用户
coach        - 教练
admin        - 管理员
super_admin  - 超级管理员
```

### 第三方登录 (provider)
```
wechat  - 微信
apple   - Apple
google  - Google
```

---

## 🔑 请求头格式

### 认证请求
```http
GET /api/plans
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

---

## 📊 响应格式

### 成功响应
```json
{
  "message": "操作成功",
  "data": {...}
}
```

### 分页响应
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

### 错误响应
```json
{
  "error": "错误描述信息"
}
```

---

## ⚡ 常用查询参数

### 分页参数
```
?page=1           - 页码（默认1）
?per_page=20      - 每页数量（默认20，最大100）
```

### 筛选参数（训练计划）
```
?my_plans=true              - 只看我的计划
?templates=true             - 只看模板
?difficulty=intermediate    - 按难度筛选
?target_muscle_group=chest  - 按目标肌群筛选
?goal=增肌                  - 按训练目标筛选
?is_active=true             - 只看激活的计划
?keyword=增肌               - 搜索关键词
?order_by=usage_count       - 排序方式
```

### 排序方式
```
created_at      - 创建时间（默认）
usage_count     - 使用次数
completion_rate - 完成率
```

---

## 🎯 快速示例

### 1. 完整流程：注册→登录→创建计划→开始训练

```bash
# 1. 注册
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user1@test.com","password":"Test123456"}'

# 2. 登录
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"user1","password":"Test123456"}'
# 获取 access_token

# 3. 创建计划
curl -X POST http://localhost:5000/api/plans \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"我的计划","difficulty":"beginner","duration_weeks":4,"days_per_week":3,...}'

# 4. 开始训练
curl -X POST http://localhost:5000/api/plans/1/start \
  -H "Authorization: Bearer <token>"
```

### 2. 浏览并复制模板

```bash
# 1. 浏览模板列表
curl http://localhost:5000/api/plans?templates=true \
  -H "Authorization: Bearer <token>"

# 2. 查看模板详情
curl http://localhost:5000/api/plans/5 \
  -H "Authorization: Bearer <token>"

# 3. 复制模板
curl -X POST http://localhost:5000/api/plans/5/copy \
  -H "Authorization: Bearer <token>"

# 4. 开始执行复制的计划
curl -X POST http://localhost:5000/api/plans/10/start \
  -H "Authorization: Bearer <token>"
```

### 3. 查看训练进度

```bash
# 获取我的激活计划
curl "http://localhost:5000/api/plans?is_active=true&my_plans=true" \
  -H "Authorization: Bearer <token>"

# 查看计划进度
curl http://localhost:5000/api/plans/1/progress \
  -H "Authorization: Bearer <token>"
```

---

## 🔧 HTTP状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 创建成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未授权（需要登录） |
| 403 | Forbidden | 禁止访问（无权限） |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

---

## 💡 最佳实践

### 1. 令牌管理
- ✅ 将access_token存储在内存或SessionStorage
- ✅ 将refresh_token存储在HttpOnly Cookie
- ✅ 令牌过期时使用refresh_token刷新
- ❌ 不要在URL参数中传递令牌

### 2. 错误处理
```javascript
try {
  const response = await fetch('/api/plans', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (response.status === 401) {
    // 令牌过期，跳转登录
    redirectToLogin();
  } else if (!response.ok) {
    const error = await response.json();
    console.error(error.error);
  }
} catch (err) {
  console.error('网络错误:', err);
}
```

### 3. 分页请求
```javascript
// 获取第一页
const page1 = await fetch('/api/plans?page=1&per_page=20');

// 检查是否有更多页
const result = await page1.json();
const hasMore = result.pagination.page < result.pagination.pages;
```

---

## 🐛 常见错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `令牌无效或已过期` | JWT令牌失效 | 使用refresh_token刷新或重新登录 |
| `无权访问该资源` | 权限不足 | 检查用户角色或资源所有权 |
| `缺少必填字段: name` | 请求参数不完整 | 补充缺少的字段 |
| `无效的难度等级` | 枚举值错误 | 使用正确的枚举值 |
| `计划不存在` | ID无效或已删除 | 检查计划ID |

---

## 📱 移动端集成示例

### iOS (Swift)
```swift
struct AuthRequest: Codable {
    let identifier: String
    let password: String
}

func login(username: String, password: String) {
    let url = URL(string: "http://api.keepfit.com/api/auth/login")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = AuthRequest(identifier: username, password: password)
    request.httpBody = try? JSONEncoder().encode(body)
    
    URLSession.shared.dataTask(with: request) { data, response, error in
        // 处理响应
    }.resume()
}
```

### Android (Kotlin)
```kotlin
data class AuthRequest(
    val identifier: String,
    val password: String
)

fun login(username: String, password: String) {
    val retrofit = Retrofit.Builder()
        .baseUrl("http://api.keepfit.com")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val api = retrofit.create(ApiService::class.java)
    val request = AuthRequest(username, password)
    
    api.login(request).enqueue(object : Callback<LoginResponse> {
        override fun onResponse(call: Call<LoginResponse>, response: Response<LoginResponse>) {
            // 处理响应
        }
        override fun onFailure(call: Call<LoginResponse>, t: Throwable) {
            // 处理错误
        }
    })
}
```

---

## 📚 相关文档

- [完整API文档 - 认证系统](AUTH_SYSTEM.md)
- [完整API文档 - 训练计划](TRAINING_API.md)
- [快速开始指南](TRAINING_QUICK_START.md)
- [项目总览](PROJECT_OVERVIEW.md)

---

**版本**: v1.0  
**更新**: 2025-10-19  
**打印友好**: ✅
