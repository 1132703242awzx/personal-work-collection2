# Keep健身后端 - 快速开始指南

## 📦 安装步骤

### 1. 克隆项目
```bash
cd keep健身后端
```

### 2. 创建虚拟环境
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. 安装依赖
```powershell
pip install -r requirements.txt
```

### 4. 配置数据库

#### 安装MySQL
确保已安装MySQL数据库服务器

#### 创建数据库
```sql
CREATE DATABASE keep_fitness CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 配置环境变量
复制 `.env.example` 为 `.env`：
```powershell
Copy-Item .env.example .env
```

编辑 `.env` 文件：
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/keep_fitness?charset=utf8mb4
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 5. 初始化数据库
```powershell
# 创建所有数据表
python utils/init_db.py create
```

### 6. 运行应用
```powershell
python app.py
```

访问: http://localhost:5000

---

## 🧪 测试端点

### 健康检查
```bash
curl http://localhost:5000/health
```

响应:
```json
{
  "status": "healthy",
  "app": "Keep Fitness",
  "version": "1.0.0"
}
```

### 首页
```bash
curl http://localhost:5000/
```

---

## 📚 数据库操作

### 创建表
```powershell
python utils/init_db.py create
```

### 删除表（慎用）
```powershell
python utils/init_db.py drop
```

### 重置数据库（慎用）
```powershell
python utils/init_db.py reset
```

---

## 🔧 常见问题

### 问题1: 导入错误
```
ImportError: No module named 'sqlalchemy'
```

**解决方案**:
```powershell
pip install -r requirements.txt
```

### 问题2: 数据库连接失败
```
sqlalchemy.exc.OperationalError: (2003, "Can't connect to MySQL server")
```

**解决方案**:
1. 确认MySQL服务正在运行
2. 检查 `.env` 中的数据库配置
3. 确认数据库已创建

### 问题3: 虚拟环境激活失败
```
无法加载文件，因为在此系统上禁止运行脚本
```

**解决方案**:
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy RemoteSigned
```

---

## 📖 下一步

1. **查看数据库设计**: `docs/DATABASE_DESIGN.md`
2. **开发API接口**: 在 `api/` 目录创建路由
3. **添加业务逻辑**: 在 `services/` 目录添加服务层
4. **编写单元测试**: 在 `tests/` 目录添加测试

---

## 🎯 推荐开发流程

### 第一步: 熟悉数据模型
```python
from models import User, TrainingPlan, WorkoutRecord

# 查看所有表
from config.database import Base
for table in Base.metadata.sorted_tables:
    print(table.name)
```

### 第二步: 创建测试数据
```python
from config.database import db_session
from models import User, UserProfile

# 创建用户
user = User(
    username="test_user",
    email="test@example.com",
    password_hash="hashed_password"
)
db_session.add(user)
db_session.commit()
```

### 第三步: 开发API
创建 `api/users.py`:
```python
from flask import Blueprint, jsonify, request
from models import User
from config.database import db_session

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.filter_by(is_deleted=False).all()
    return jsonify([user.to_dict() for user in users])
```

---

## 🛠️ 开发工具推荐

- **数据库管理**: MySQL Workbench, DBeaver
- **API测试**: Postman, Insomnia
- **Python IDE**: PyCharm, VS Code
- **版本控制**: Git

---

## 📞 获取帮助

- 查看文档: `docs/`
- 查看示例: `examples/`
- 提交Issue: GitHub Issues

---

**祝开发顺利！** 🚀
