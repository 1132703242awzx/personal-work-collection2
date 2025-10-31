# Keep健身后端 - 认证系统文档

## 🔐 认证系统概述

完整的企业级用户认证和权限管理系统，支持：
- ✅ 手机号/邮箱注册登录
- ✅ JWT Token双令牌机制（Access + Refresh）
- ✅ 用户角色权限（普通用户/教练/管理员）
- ✅ 第三方登录（微信/Apple）
- ✅ 密码重置和安全验证
- ✅ 登录历史追踪
- ✅ 安全日志记录

---

## 📊 认证相关数据表

### 1. user_roles - 用户角色表
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| role | ENUM | 角色（user/coach/admin/super_admin） |
| coach_cert_number | VARCHAR | 教练证书编号 |
| coach_level | VARCHAR | 教练级别 |
| permissions | TEXT | 权限列表（JSON） |

### 2. third_party_accounts - 第三方账号表
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| provider | ENUM | 平台（wechat/apple/google） |
| provider_user_id | VARCHAR | 第三方用户ID |
| access_token | VARCHAR | 访问令牌 |
| is_bound | BOOLEAN | 是否绑定 |

### 3. refresh_tokens - 刷新令牌表
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| token | VARCHAR | 刷新令牌 |
| expires_at | DATETIME | 过期时间 |
| device_id | VARCHAR | 设备ID |
| is_revoked | BOOLEAN | 是否已撤销 |

### 4. password_reset_tokens - 密码重置令牌表
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| token | VARCHAR | 重置令牌 |
| verification_code | VARCHAR | 验证码 |
| expires_at | DATETIME | 过期时间 |
| is_used | BOOLEAN | 是否已使用 |

### 5. login_history - 登录历史表
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| login_type | VARCHAR | 登录方式 |
| is_success | BOOLEAN | 是否成功 |
| ip_address | VARCHAR | IP地址 |
| device_info | VARCHAR | 设备信息 |

### 6. security_logs - 安全日志表
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| event_type | VARCHAR | 事件类型 |
| is_success | BOOLEAN | 是否成功 |
| ip_address | VARCHAR | IP地址 |

---

## 🎯 API接口文档

### 基础URL
```
http://localhost:5000/api/auth
```

### 1. 用户注册
**POST** `/api/auth/register`

请求体：
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "13800138000",
  "password": "Password123",
  "nickname": "John"
}
```

响应（成功）：
```json
{
  "message": "注册成功",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "13800138000"
  }
}
```

### 2. 用户登录
**POST** `/api/auth/login`

请求体：
```json
{
  "identifier": "john_doe",
  "password": "Password123",
  "device_id": "device_123",
  "device_type": "iOS",
  "device_name": "iPhone 13"
}
```

响应（成功）：
```json
{
  "message": "登录成功",
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400
  }
}
```

### 3. 刷新令牌
**POST** `/api/auth/refresh`

请求体：
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

响应（成功）：
```json
{
  "message": "令牌刷新成功",
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400
  }
}
```

### 4. 用户登出
**POST** `/api/auth/logout`

请求头：
```
Authorization: Bearer <access_token>
```

请求体（可选）：
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 5. 请求密码重置
**POST** `/api/auth/password/reset/request`

请求体：
```json
{
  "identifier": "john@example.com"
}
```

响应：
```json
{
  "message": "如果该账号存在，重置链接已发送"
}
```

### 6. 重置密码
**POST** `/api/auth/password/reset`

请求体：
```json
{
  "token": "reset_token_here",
  "verification_code": "123456",
  "new_password": "NewPassword123"
}
```

### 7. 修改密码
**POST** `/api/auth/password/change`

请求头：
```
Authorization: Bearer <access_token>
```

请求体：
```json
{
  "old_password": "OldPassword123",
  "new_password": "NewPassword123"
}
```

### 8. 微信登录
**POST** `/api/auth/wechat/login`

请求体：
```json
{
  "code": "wechat_auth_code",
  "device_id": "device_123",
  "device_type": "iOS"
}
```

### 9. Apple登录
**POST** `/api/auth/apple/login`

请求体：
```json
{
  "id_token": "apple_id_token",
  "user_info": {
    "email": "john@example.com",
    "firstName": "John",
    "lastName": "Doe"
  },
  "device_id": "device_123"
}
```

### 10. 绑定第三方账号
**POST** `/api/auth/third-party/bind`

请求头：
```
Authorization: Bearer <access_token>
```

请求体：
```json
{
  "provider": "wechat",
  "code": "wechat_auth_code"
}
```

### 11. 解绑第三方账号
**POST** `/api/auth/third-party/unbind`

请求头：
```
Authorization: Bearer <access_token>
```

请求体：
```json
{
  "provider": "wechat"
}
```

### 12. 获取当前用户信息
**GET** `/api/auth/me`

请求头：
```
Authorization: Bearer <access_token>
```

响应：
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "13800138000",
    "status": "active",
    "is_verified": true,
    "is_premium": false,
    "roles": [
      {"role": "user"}
    ],
    "third_party_accounts": [
      {"provider": "wechat", "is_bound": true}
    ]
  }
}
```

---

## 🔒 中间件装饰器

### @token_required
验证JWT访问令牌

```python
from middleware.auth import token_required

@app.route('/api/protected')
@token_required
def protected_route():
    user_id = g.user_id
    user = g.current_user
    return jsonify({'message': 'Protected data'})
```

### @role_required
验证用户角色

```python
from middleware.auth import role_required
from models import UserRoleEnum

@app.route('/api/coach/dashboard')
@role_required([UserRoleEnum.COACH, UserRoleEnum.ADMIN])
def coach_dashboard():
    return jsonify({'message': 'Coach dashboard'})
```

### @admin_required
验证管理员权限

```python
from middleware.auth import admin_required

@app.route('/api/admin/users')
@admin_required
def admin_users():
    return jsonify({'message': 'Admin only'})
```

### @coach_required
验证教练权限

```python
from middleware.auth import coach_required

@app.route('/api/coach/courses')
@coach_required
def coach_courses():
    return jsonify({'message': 'Coach courses'})
```

### @optional_token
可选令牌验证

```python
from middleware.auth import optional_token

@app.route('/api/public')
@optional_token
def public_route():
    user = get_current_user()
    if user:
        # 已登录用户
        pass
    else:
        # 未登录用户
        pass
    return jsonify({'message': 'Public data'})
```

---

## 🎓 使用示例

### 1. 用户注册和登录流程

```python
# 1. 注册
POST /api/auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "Password123"
}

# 2. 登录获取令牌
POST /api/auth/login
{
  "identifier": "john_doe",
  "password": "Password123"
}

# 响应
{
  "tokens": {
    "access_token": "...",  # 24小时有效
    "refresh_token": "...", # 30天有效
    "expires_in": 86400
  }
}

# 3. 使用access_token访问受保护接口
GET /api/auth/me
Headers: Authorization: Bearer <access_token>

# 4. access_token过期后，使用refresh_token刷新
POST /api/auth/refresh
{
  "refresh_token": "..."
}
```

### 2. 第三方登录流程

```python
# 微信登录
# 1. 前端获取微信授权码
# 2. 发送到后端
POST /api/auth/wechat/login
{
  "code": "wechat_code"
}

# 3. 后端处理
# - 用code换取access_token
# - 获取微信用户信息
# - 查找或创建用户
# - 返回JWT令牌
```

### 3. 密码重置流程

```python
# 1. 请求重置
POST /api/auth/password/reset/request
{
  "identifier": "john@example.com"
}

# 2. 用户收到邮件/短信验证码
# 3. 提交重置请求
POST /api/auth/password/reset
{
  "token": "reset_token",
  "verification_code": "123456",
  "new_password": "NewPassword123"
}
```

### 4. 权限验证示例

```python
from flask import Blueprint, jsonify
from middleware.auth import token_required, admin_required, coach_required
from models import UserRoleEnum

api_bp = Blueprint('api', __name__)

# 普通用户接口
@api_bp.route('/profile')
@token_required
def get_profile():
    user = g.current_user
    return jsonify({'user': user.to_dict()})

# 教练接口
@api_bp.route('/coach/students')
@coach_required
def get_students():
    return jsonify({'students': []})

# 管理员接口
@api_bp.route('/admin/users')
@admin_required
def manage_users():
    return jsonify({'users': []})
```

---

## 🔐 安全特性

### 1. 密码安全
- 使用bcrypt加密存储
- 密码强度验证（至少8位，包含大小写字母和数字）
- 支持密码重置和修改

### 2. JWT双令牌机制
- **Access Token**: 短期有效（24小时），用于API访问
- **Refresh Token**: 长期有效（30天），用于刷新Access Token
- 撤销机制：登出时撤销Refresh Token

### 3. 设备管理
- 记录设备信息（设备ID、类型、名称）
- 支持多设备登录
- 可以查看和管理登录设备

### 4. 登录保护
- 记录登录历史（成功/失败）
- IP地址追踪
- 异常登录检测

### 5. 第三方登录安全
- OAuth 2.0标准流程
- Token验证
- 账号绑定解绑控制

---

## 📊 数据库设计亮点

### 1. 多角色支持
```python
# 一个用户可以有多个角色
user.roles = [
    UserRole(role=UserRoleEnum.USER),
    UserRole(role=UserRoleEnum.COACH)
]
```

### 2. 刷新令牌管理
```python
# 每个设备独立的刷新令牌
RefreshToken(
    user_id=1,
    token="...",
    device_id="device_123",
    expires_at=datetime(2025, 11, 18)
)
```

### 3. 登录历史追踪
```python
# 记录每次登录尝试
LoginHistory(
    user_id=1,
    login_type="password",  # password/wechat/apple
    is_success=True,
    ip_address="192.168.1.1",
    device_type="iOS"
)
```

---

## 🛠️ 配置说明

### JWT配置（config/config.py）
```python
class Config:
    # JWT密钥（生产环境必须更改）
    JWT_SECRET_KEY = "your-secret-key"
    
    # 令牌有效期
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

### 第三方平台配置
```python
# 微信
WECHAT_APP_ID = "your_wechat_app_id"
WECHAT_APP_SECRET = "your_wechat_app_secret"

# Apple
APPLE_CLIENT_ID = "your_apple_client_id"
APPLE_TEAM_ID = "your_apple_team_id"
APPLE_KEY_ID = "your_apple_key_id"
```

---

## 🧪 测试用例

### Postman测试集合

1. **注册**
```
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "Test123456"
}
```

2. **登录**
```
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "identifier": "testuser",
  "password": "Test123456"
}
```

3. **获取用户信息**
```
GET http://localhost:5000/api/auth/me
Authorization: Bearer <your_access_token>
```

---

## ⚠️ 注意事项

### 生产环境部署
1. **更改密钥**：修改JWT_SECRET_KEY为强随机字符串
2. **HTTPS**：强制使用HTTPS传输
3. **Token存储**：前端安全存储令牌（不要存localStorage）
4. **签名验证**：第三方登录需要验证签名
5. **邮件/短信**：实现真实的邮件和短信发送

### 安全建议
1. 定期轮换JWT密钥
2. 实现登录限流（防止暴力破解）
3. 添加验证码（注册/登录）
4. 实现设备指纹识别
5. 监控异常登录行为

---

## 📚 相关文档

- [数据库设计文档](./DATABASE_DESIGN.md)
- [快速开始指南](./QUICK_START.md)
- [项目架构说明](./ARCHITECTURE.md)

---

**文档版本**: v1.0  
**更新日期**: 2025-10-19  
**维护者**: Keep健身后端团队
