# 认证系统测试指南

## 🧪 快速测试

### 1. 启动应用
```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装新依赖
pip install PyJWT==2.8.0 requests==2.31.0

# 运行应用
python app.py
```

### 2. 使用Postman测试

#### 测试序列

**第一步：注册用户**
```http
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "username": "testuser001",
  "email": "test001@example.com",
  "phone": "13800138001",
  "password": "Test123456",
  "nickname": "测试用户001"
}
```

**预期响应**：
```json
{
  "message": "注册成功",
  "user": {
    "id": 1,
    "username": "testuser001",
    "email": "test001@example.com",
    "phone": "13800138001"
  }
}
```

---

**第二步：登录获取令牌**
```http
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "identifier": "testuser001",
  "password": "Test123456",
  "device_id": "test_device_001",
  "device_type": "Web",
  "device_name": "Chrome Browser"
}
```

**预期响应**：
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

**💡 提示**：复制access_token，后续请求需要使用

---

**第三步：获取当前用户信息**
```http
GET http://localhost:5000/api/auth/me
Authorization: Bearer <your_access_token>
```

**预期响应**：
```json
{
  "user": {
    "id": 1,
    "username": "testuser001",
    "email": "test001@example.com",
    "phone": "13800138001",
    "status": "active",
    "is_verified": false,
    "is_premium": false,
    "created_at": "2025-10-19T10:00:00",
    "roles": [
      {"role": "user"}
    ],
    "third_party_accounts": []
  }
}
```

---

**第四步：修改密码**
```http
POST http://localhost:5000/api/auth/password/change
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "old_password": "Test123456",
  "new_password": "NewTest123456"
}
```

---

**第五步：刷新令牌**
```http
POST http://localhost:5000/api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "<your_refresh_token>"
}
```

**预期响应**：
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

---

**第六步：请求密码重置**
```http
POST http://localhost:5000/api/auth/password/reset/request
Content-Type: application/json

{
  "identifier": "test001@example.com"
}
```

**预期响应**：
```json
{
  "message": "如果该账号存在，重置链接已发送",
  "reset_token": "xxx"  // 开发环境返回，生产环境不返回
}
```

---

**第七步：重置密码**
```http
POST http://localhost:5000/api/auth/password/reset
Content-Type: application/json

{
  "token": "<reset_token>",
  "verification_code": "123456",
  "new_password": "ResetPassword123"
}
```

---

**第八步：登出**
```http
POST http://localhost:5000/api/auth/logout
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "refresh_token": "<your_refresh_token>"
}
```

---

## 🔧 Python测试脚本

创建 `test_auth.py`：

```python
import requests
import json

BASE_URL = "http://localhost:5000/api/auth"

def test_register():
    """测试注册"""
    print("=== 测试注册 ===")
    url = f"{BASE_URL}/register"
    data = {
        "username": "testuser002",
        "email": "test002@example.com",
        "phone": "13800138002",
        "password": "Test123456"
    }
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_login():
    """测试登录"""
    print("=== 测试登录 ===")
    url = f"{BASE_URL}/login"
    data = {
        "identifier": "testuser002",
        "password": "Test123456",
        "device_id": "test_device",
        "device_type": "Python"
    }
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        access_token = result['tokens']['access_token']
        print(f"\nAccess Token: {access_token[:50]}...")
        return access_token
    print()
    return None

def test_get_user_info(access_token):
    """测试获取用户信息"""
    print("=== 测试获取用户信息 ===")
    url = f"{BASE_URL}/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

if __name__ == "__main__":
    # 1. 注册
    test_register()
    
    # 2. 登录
    access_token = test_login()
    
    # 3. 获取用户信息
    if access_token:
        test_get_user_info(access_token)
```

运行测试：
```powershell
python test_auth.py
```

---

## 🎯 功能验证清单

### 基础认证
- [ ] 用户注册（用户名+邮箱）
- [ ] 用户注册（用户名+手机号）
- [ ] 密码强度验证
- [ ] 用户名重复检查
- [ ] 邮箱重复检查
- [ ] 手机号重复检查

### 登录功能
- [ ] 用户名登录
- [ ] 邮箱登录
- [ ] 手机号登录
- [ ] 错误密码处理
- [ ] 获取JWT令牌
- [ ] 记录登录历史

### Token管理
- [ ] Access Token生成
- [ ] Refresh Token生成
- [ ] Token过期验证
- [ ] Token刷新
- [ ] Token撤销（登出）
- [ ] 多设备Token管理

### 密码管理
- [ ] 修改密码
- [ ] 请求密码重置
- [ ] 验证码生成
- [ ] 密码重置
- [ ] 旧密码验证

### 权限验证
- [ ] @token_required验证
- [ ] @role_required验证
- [ ] @admin_required验证
- [ ] @coach_required验证
- [ ] 权限不足处理

### 第三方登录（需配置）
- [ ] 微信登录
- [ ] Apple登录
- [ ] 账号绑定
- [ ] 账号解绑

---

## 🐛 常见问题

### 1. 导入错误
```
ModuleNotFoundError: No module named 'jwt'
```

**解决方案**：
```powershell
pip install PyJWT==2.8.0
```

### 2. 数据库表不存在
```
sqlalchemy.exc.OperationalError: Table 'user_roles' doesn't exist
```

**解决方案**：
```powershell
python utils/init_db.py create
```

### 3. JWT密钥错误
```
jwt.exceptions.DecodeError: Invalid crypto padding
```

**解决方案**：检查`.env`文件中的`JWT_SECRET_KEY`配置

### 4. Token过期
```
{
  "error": "令牌已过期"
}
```

**解决方案**：使用refresh_token刷新access_token

---

## 📊 性能测试

使用Apache Bench测试并发登录：

```bash
# 安装ab工具（Windows可使用Apache自带的ab.exe）

# 测试100个并发请求
ab -n 1000 -c 100 -T "application/json" -p login.json http://localhost:5000/api/auth/login
```

`login.json` 内容：
```json
{
  "identifier": "testuser001",
  "password": "Test123456"
}
```

---

## 🔍 调试技巧

### 1. 查看Token内容
使用 [jwt.io](https://jwt.io) 解码Token：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyMDAxIiwiZXhwIjoxNzI5NDIzMjAwLCJpYXQiOjE3MjkzMzY4MDAsInR5cGUiOiJhY2Nlc3MifQ.xxxxx
```

解码后：
```json
{
  "user_id": 1,
  "username": "testuser001",
  "exp": 1729423200,
  "iat": 1729336800,
  "type": "access"
}
```

### 2. 启用SQL日志
在 `config/database.py` 中：
```python
SQLALCHEMY_ECHO = True  # 打印所有SQL语句
```

### 3. 查看登录历史
```sql
SELECT * FROM login_history ORDER BY login_at DESC LIMIT 10;
```

### 4. 查看活跃Token
```sql
SELECT * FROM refresh_tokens 
WHERE is_revoked = FALSE 
AND expires_at > NOW()
ORDER BY created_at DESC;
```

---

## 🎓 进阶测试

### 1. 测试角色权限

```python
# 创建教练角色
from models import UserRole, UserRoleEnum
from config.database import db_session

user_role = UserRole(
    user_id=1,
    role=UserRoleEnum.COACH,
    coach_cert_number="CERT123456",
    coach_level="高级"
)
db_session.add(user_role)
db_session.commit()
```

### 2. 测试第三方绑定

```python
# 模拟微信账号绑定
from models import ThirdPartyAccount, ThirdPartyProviderEnum

third_party = ThirdPartyAccount(
    user_id=1,
    provider=ThirdPartyProviderEnum.WECHAT,
    provider_user_id="wx_openid_123",
    nickname="微信用户"
)
db_session.add(third_party)
db_session.commit()
```

### 3. 测试并发登录

```python
import threading
import requests

def concurrent_login(thread_id):
    url = "http://localhost:5000/api/auth/login"
    data = {
        "identifier": "testuser001",
        "password": "Test123456"
    }
    response = requests.post(url, json=data)
    print(f"Thread {thread_id}: {response.status_code}")

# 创建10个并发请求
threads = []
for i in range(10):
    t = threading.Thread(target=concurrent_login, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

---

## ✅ 测试检查表

### 安全性测试
- [ ] SQL注入防护
- [ ] XSS防护
- [ ] CSRF防护
- [ ] 暴力破解防护
- [ ] Token劫持防护

### 功能测试
- [ ] 正常注册流程
- [ ] 重复注册拒绝
- [ ] 正常登录流程
- [ ] 错误密码拒绝
- [ ] Token刷新机制
- [ ] 登出功能

### 压力测试
- [ ] 100并发登录
- [ ] 1000并发请求
- [ ] 长时间运行稳定性

---

**测试文档版本**: v1.0  
**更新日期**: 2025-10-19
