# 🚀 Keep健身后端 - 部署和使用完整指南

## 📋 目录
1. [环境要求](#环境要求)
2. [安装部署](#安装部署)
3. [功能测试](#功能测试)
4. [开发指南](#开发指南)
5. [生产部署](#生产部署)
6. [常见问题](#常见问题)

---

## 🖥️ 环境要求

### 必需环境
- **Python**: 3.8+
- **MySQL**: 8.0+
- **操作系统**: Windows/Linux/macOS

### 推荐环境
- **Python**: 3.10+
- **MySQL**: 8.0.30+
- **内存**: 4GB+
- **硬盘**: 20GB+

---

## 📦 安装部署

### 步骤1: 克隆项目
```bash
git clone <repository-url>
cd keep健身后端
```

### 步骤2: 创建虚拟环境
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 步骤3: 安装依赖
```bash
pip install -r requirements.txt
```

**依赖包清单**:
- Flask==2.3.3 - Web框架
- Flask-CORS==4.0.0 - 跨域支持
- SQLAlchemy==2.0.20 - ORM框架
- PyMySQL==1.1.0 - MySQL驱动
- PyJWT==2.8.0 - JWT认证
- requests==2.31.0 - HTTP客户端
- Werkzeug==2.3.7 - 密码加密
- python-dotenv==1.0.0 - 环境变量管理

### 步骤4: 配置数据库

**4.1 创建数据库**
```sql
CREATE DATABASE keep_fitness 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

**4.2 创建配置文件**
```bash
# 在项目根目录创建 .env 文件
touch .env  # Linux/Mac
New-Item .env  # Windows PowerShell
```

**4.3 编辑 .env 文件**
```env
# 数据库配置
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/keep_fitness?charset=utf8mb4

# 应用配置
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
FLASK_ENV=development
DEBUG=True

# 应用信息
APP_NAME=Keep Fitness API
APP_VERSION=1.0.0

# JWT配置
JWT_ACCESS_TOKEN_EXPIRES=86400
JWT_REFRESH_TOKEN_EXPIRES=2592000

# 第三方登录配置（可选）
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
APPLE_CLIENT_ID=your_apple_client_id
APPLE_TEAM_ID=your_apple_team_id
APPLE_KEY_ID=your_apple_key_id
```

### 步骤5: 初始化数据库
```bash
# 创建所有数据表
python utils/init_db.py create

# 如需重置数据库（慎用！）
python utils/init_db.py reset
```

**预期输出**:
```
=== Keep健身数据库管理工具 ===

正在创建数据库表...
✓ users 表已创建
✓ user_profiles 表已创建
✓ user_settings 表已创建
✓ user_roles 表已创建
✓ training_plans 表已创建
... (共21张表)

数据库表创建成功！
```

### 步骤6: 启动应用
```bash
python app.py
```

**预期输出**:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

### 步骤7: 验证安装
```bash
# 新开一个终端
curl http://localhost:5000/health

# 预期响应
{
  "status": "healthy",
  "app": "Keep Fitness API",
  "version": "1.0.0"
}
```

---

## 🧪 功能测试

### 1. 测试认证系统

**启动测试工具**:
```bash
python test_auth.py
```

**测试流程**:
```
1. 选择 "1. 运行完整测试"
2. 观察测试结果：
   ✅ 用户注册
   ✅ 用户登录
   ✅ 获取用户信息
   ✅ 刷新令牌
   ✅ 修改密码
   ✅ 登出
```

**手动测试示例**:
```bash
# 1. 注册用户
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456"
  }'

# 2. 登录
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "testuser",
    "password": "Test123456"
  }'

# 复制返回的 access_token
```

### 2. 测试训练计划系统

**启动测试工具**:
```bash
python test_training.py
```

**测试流程**:
```
1. 输入用户名和密码登录
2. 选择 "1. 运行完整测试"
3. 观察测试结果：
   ✅ 创建训练计划
   ✅ 获取计划列表
   ✅ 获取计划详情
   ✅ 更新计划
   ✅ 开始执行计划
   ✅ 获取计划进度
   ✅ 筛选功能
```

### 3. 使用Postman测试

**导入集合**:
1. 打开Postman
2. File → Import
3. 选择 `docs/TRAINING_API.md` 中的示例
4. 创建环境变量：
   - `base_url`: http://localhost:5000
   - `access_token`: (登录后获取)

**测试步骤**:
```
1. Auth → Login (获取token)
2. Plans → Create Plan
3. Plans → Get Plans
4. Plans → Get Plan Detail
5. Plans → Start Plan
6. Plans → Get Progress
```

---

## 💻 开发指南

### 项目结构
```
keep健身后端/
├── app.py                    # 应用入口
├── requirements.txt          # 依赖列表
├── .env                      # 环境配置（不提交到git）
│
├── config/                   # 配置模块
│   ├── __init__.py
│   ├── config.py            # 应用配置类
│   └── database.py          # 数据库配置
│
├── models/                   # 数据模型
│   ├── __init__.py
│   ├── base.py              # 基础模型
│   ├── user.py              # 用户模型
│   ├── auth.py              # 认证模型
│   ├── training.py          # 训练计划模型
│   ├── workout.py           # 运动记录模型
│   ├── course.py            # 课程模型
│   ├── social.py            # 社交模型
│   └── body_data.py         # 身体数据模型
│
├── services/                 # 服务层
│   ├── __init__.py
│   ├── auth_service.py      # 认证服务
│   ├── third_party_auth_service.py  # 第三方登录
│   └── training_service.py  # 训练计划服务
│
├── middleware/               # 中间件
│   ├── __init__.py
│   └── auth.py              # 认证中间件
│
├── api/                      # API路由
│   ├── __init__.py
│   ├── auth.py              # 认证API
│   └── training.py          # 训练计划API
│
├── utils/                    # 工具函数
│   ├── __init__.py
│   └── init_db.py           # 数据库初始化
│
├── docs/                     # 文档
│   ├── DATABASE_DESIGN.md
│   ├── AUTH_SYSTEM.md
│   ├── TRAINING_API.md
│   ├── TRAINING_QUICK_START.md
│   ├── API_CHEATSHEET.md
│   ├── PROJECT_OVERVIEW.md
│   └── TRAINING_IMPLEMENTATION_SUMMARY.md
│
└── tests/                    # 测试文件
    ├── test_auth.py
    └── test_training.py
```

### 开发流程

**1. 添加新功能**
```python
# Step 1: 创建或修改数据模型
# models/new_feature.py

# Step 2: 创建服务层
# services/new_feature_service.py
class NewFeatureService:
    @staticmethod
    def create(data):
        # 业务逻辑
        pass

# Step 3: 创建API路由
# api/new_feature.py
@new_feature_bp.route('/', methods=['POST'])
@token_required
def create():
    service = NewFeatureService.create(request.json)
    return jsonify(service), 201

# Step 4: 注册蓝图
# app.py
from api.new_feature import new_feature_bp
app.register_blueprint(new_feature_bp)
```

**2. 数据库迁移**
```bash
# 如果修改了模型，需要重新创建表
python utils/init_db.py reset  # 慎用！会清空数据
python utils/init_db.py create
```

**3. 运行测试**
```bash
# 单元测试（待实现）
pytest

# 集成测试
python test_auth.py
python test_training.py
```

### 代码规范

**命名规范**:
- 类名：大驼峰 `UserService`
- 函数名：小写下划线 `get_user_info`
- 变量名：小写下划线 `user_id`
- 常量：大写下划线 `MAX_PAGE_SIZE`

**注释规范**:
```python
def create_plan(user_id: int, plan_data: Dict) -> TrainingPlan:
    """
    创建训练计划
    
    Args:
        user_id: 用户ID
        plan_data: 计划数据字典
        
    Returns:
        创建的训练计划对象
        
    Raises:
        ValueError: 参数验证失败
        PermissionError: 权限不足
    """
    pass
```

---

## 🌐 生产部署

### 使用Gunicorn部署

**1. 安装Gunicorn**
```bash
pip install gunicorn
```

**2. 创建启动脚本**
```bash
# start.sh
#!/bin/bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**3. 启动应用**
```bash
chmod +x start.sh
./start.sh
```

### 使用Nginx反向代理

**nginx.conf**:
```nginx
server {
    listen 80;
    server_name api.keepfit.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 使用Docker部署

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@db:3306/keep_fitness
      - FLASK_ENV=production
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=keep_fitness
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

**启动**:
```bash
docker-compose up -d
```

---

## ❓ 常见问题

### Q1: 导入错误
```
ModuleNotFoundError: No module named 'flask'
```
**解决**: 确保虚拟环境已激活并安装了依赖
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Q2: 数据库连接失败
```
sqlalchemy.exc.OperationalError: Can't connect to MySQL server
```
**解决**: 
1. 检查MySQL是否运行
2. 确认 `.env` 中的数据库配置
3. 确认数据库用户权限

### Q3: JWT令牌错误
```
{"error": "令牌无效或已过期"}
```
**解决**: 
1. 检查令牌是否过期（24小时）
2. 使用refresh_token刷新
3. 重新登录获取新令牌

### Q4: 端口被占用
```
OSError: [WinError 10048] 通常每个套接字地址只允许使用一次
```
**解决**:
```bash
# Windows: 查找占用5000端口的进程
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Q5: 无法创建数据表
```
sqlalchemy.exc.ProgrammingError: Table 'users' already exists
```
**解决**:
```bash
# 重置数据库（会清空数据！）
python utils/init_db.py reset
python utils/init_db.py create
```

---

## 📞 技术支持

### 获取帮助
- 📧 邮件: support@keepfit.com
- 💬 问题: 在GitHub提Issue
- 📚 文档: 查看 `docs/` 目录

### 反馈Bug
1. 描述问题和预期行为
2. 提供错误信息和堆栈跟踪
3. 说明环境信息（OS、Python版本等）
4. 提供复现步骤

### 贡献代码
1. Fork项目
2. 创建特性分支
3. 提交代码并写清楚commit信息
4. 发起Pull Request

---

## 📚 延伸阅读

- [Flask官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy文档](https://www.sqlalchemy.org/)
- [JWT介绍](https://jwt.io/)
- [RESTful API设计](https://restfulapi.net/)

---

**文档版本**: v1.0  
**最后更新**: 2025-10-19  
**维护者**: Keep健身开发团队

---

**祝您使用愉快！如有问题，欢迎随时联系。💪**
