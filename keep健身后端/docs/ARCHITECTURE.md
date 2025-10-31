# Keep健身后端 - 项目架构总览

## 🏗️ 项目结构

```
keep健身后端/
│
├── 📄 app.py                      # Flask主应用文件
├── 📄 requirements.txt            # Python依赖包
├── 📄 README.md                   # 项目说明文档
├── 📄 .env.example               # 环境变量示例
│
├── 📁 config/                     # 配置模块
│   ├── __init__.py               # 配置包初始化
│   ├── config.py                 # 应用配置类
│   └── database.py               # 数据库配置和连接
│
├── 📁 models/                     # 数据模型层
│   ├── __init__.py               # 模型包初始化
│   ├── base.py                   # 基础模型类
│   ├── user.py                   # 用户体系模型
│   ├── training.py               # 训练计划模型
│   ├── workout.py                # 运动记录模型
│   ├── course.py                 # 课程体系模型
│   ├── social.py                 # 社交互动模型
│   └── body_data.py              # 身体数据模型
│
├── 📁 utils/                      # 工具模块
│   ├── __init__.py               # 工具包初始化
│   ├── init_db.py                # 数据库初始化脚本
│   ├── validators.py             # 数据验证工具
│   └── pagination.py             # 分页工具
│
├── 📁 docs/                       # 文档目录
│   ├── DATABASE_DESIGN.md        # 数据库设计文档
│   ├── QUICK_START.md            # 快速开始指南
│   └── database_design.py        # 设计说明代码
│
├── 📁 static/                     # 静态文件
│   └── uploads/                  # 上传文件目录
│
├── 📁 templates/                  # HTML模板
│
└── 📁 venv/                       # Python虚拟环境
```

---

## 📊 模块说明

### 1️⃣ Config模块 - 配置层

#### `config/config.py`
- **Config**: 基础配置类
- **DevelopmentConfig**: 开发环境配置
- **ProductionConfig**: 生产环境配置
- **TestingConfig**: 测试环境配置

#### `config/database.py`
- 数据库引擎配置
- 连接池管理
- 会话管理
- 数据库初始化函数

**特性**:
- ✅ 支持多环境配置
- ✅ 连接池自动管理
- ✅ 线程安全会话
- ✅ 配置热加载

---

### 2️⃣ Models模块 - 数据层

#### 核心模型类 (15个表)

**用户体系** (`user.py`)
- `User`: 用户基础信息
- `UserProfile`: 用户详细资料
- `UserSettings`: 用户个性化设置

**训练计划** (`training.py`)
- `TrainingPlan`: 训练计划
- `PlanDay`: 每日训练安排
- `Exercise`: 运动动作库

**运动记录** (`workout.py`)
- `WorkoutRecord`: 训练记录
- `ExerciseRecord`: 动作记录
- `SetRecord`: 组详细记录

**课程体系** (`course.py`)
- `Course`: 在线课程
- `Chapter`: 课程章节
- `Video`: 视频内容

**社交互动** (`social.py`)
- `Follow`: 关注关系
- `Like`: 点赞系统
- `Comment`: 评论系统

**身体数据** (`body_data.py`)
- `BodyData`: 身体数据汇总
- `WeightRecord`: 体重记录
- `BodyMeasurements`: 身体围度

**特性**:
- ✅ SQLAlchemy ORM
- ✅ 自动时间戳
- ✅ 软删除支持
- ✅ 关系映射完整
- ✅ 索引优化
- ✅ 数据验证

---

### 3️⃣ Utils模块 - 工具层

#### `utils/init_db.py`
数据库初始化管理工具
```bash
python utils/init_db.py create  # 创建表
python utils/init_db.py drop    # 删除表
python utils/init_db.py reset   # 重置数据库
```

#### `utils/validators.py`
数据验证工具类
- 邮箱格式验证
- 手机号验证
- 密码强度验证
- 年龄/体重/身高范围验证

#### `utils/pagination.py`
分页查询工具
- 自动分页
- 统计总数
- 上一页/下一页导航

**特性**:
- ✅ 命令行工具
- ✅ 完整数据验证
- ✅ 灵活分页
- ✅ 可复用性强

---

## 🎯 核心功能设计

### 1. 用户管理系统
```python
# 用户注册
user = User(username="john", email="john@example.com")
profile = UserProfile(user=user, nickname="John Doe")
settings = UserSettings(user=user)

# 自动关联
user.profile  # 访问资料
user.settings # 访问设置
```

### 2. 训练计划系统
```python
# 创建训练计划
plan = TrainingPlan(
    user=user,
    name="增肌计划",
    difficulty=DifficultyEnum.INTERMEDIATE
)

# 添加每日安排
day1 = PlanDay(training_plan=plan, day_number=1)
exercise1 = Exercise(
    plan_day=day1,
    name="卧推",
    muscle_group=MuscleGroupEnum.CHEST
)
```

### 3. 运动记录系统
```python
# 记录训练
workout = WorkoutRecord(
    user=user,
    training_plan=plan,
    workout_date=datetime.now()
)

# 记录动作
exercise_record = ExerciseRecord(
    workout_record=workout,
    exercise=exercise1
)

# 记录每组
set_record = SetRecord(
    exercise_record=exercise_record,
    set_number=1,
    reps=10,
    weight=50.0
)
```

### 4. 社交互动系统
```python
# 关注用户
follow = Follow(follower=user1, following=user2)

# 点赞训练
like = Like(
    user=user,
    target_type="workout",
    target_id=workout.id
)

# 评论
comment = Comment(
    user=user,
    target_type="workout",
    target_id=workout.id,
    content="训练很棒！"
)
```

---

## 🔐 安全特性

### 1. 密码安全
```python
from werkzeug.security import generate_password_hash, check_password_hash

# 密码加密
password_hash = generate_password_hash("Password123")
user.password_hash = password_hash

# 密码验证
if check_password_hash(user.password_hash, "Password123"):
    # 登录成功
    pass
```

### 2. 软删除
```python
# 软删除（推荐）
user.soft_delete()  # is_deleted = True

# 查询时自动过滤
active_users = User.query.filter_by(is_deleted=False).all()
```

### 3. 隐私控制
```python
# 用户设置隐私
settings.profile_visible = False  # 资料不可见
settings.workout_visible = False  # 训练记录不可见
settings.allow_follow = False     # 不允许关注
```

---

## 📈 性能优化

### 1. 连接池配置
```python
# config/database.py
pool_size = 10           # 基础连接数
max_overflow = 20        # 峰值额外连接
pool_recycle = 3600     # 连接回收时间
pool_timeout = 30       # 连接超时
```

### 2. 查询优化
```python
# 使用索引
User.query.filter_by(username="john").first()

# 预加载关联
from sqlalchemy.orm import joinedload
user = User.query.options(
    joinedload(User.profile),
    joinedload(User.settings)
).first()

# 分页查询
from utils.pagination import paginate
result = paginate(User.query, page=1, page_size=20)
```

### 3. 缓存策略
```python
# TODO: Redis缓存
from flask_caching import Cache
cache = Cache(app)

@cache.cached(timeout=300)
def get_popular_courses():
    return Course.query.filter_by(is_featured=True).all()
```

---

## 🧪 测试示例

### 单元测试
```python
# tests/test_models.py
def test_create_user():
    user = User(
        username="test",
        email="test@example.com",
        password_hash="hashed"
    )
    db.session.add(user)
    db.session.commit()
    
    assert user.id is not None
    assert user.username == "test"
```

### 集成测试
```python
# tests/test_api.py
def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
```

---

## 📊 数据统计示例

### 用户统计
```python
from sqlalchemy import func

# 统计用户训练次数
stats = db.session.query(
    func.count(WorkoutRecord.id).label('total'),
    func.sum(WorkoutRecord.calories_burned).label('calories')
).filter(
    WorkoutRecord.user_id == user_id,
    WorkoutRecord.is_deleted == False
).first()
```

### 排行榜
```python
# 训练次数排行
top_users = User.query.join(UserProfile).order_by(
    UserProfile.workout_count.desc()
).limit(10).all()
```

---

## 🚀 部署建议

### 1. 生产环境配置
```python
# 使用生产配置
app = create_app('production')

# 环境变量
FLASK_ENV=production
DEBUG=False
SQLALCHEMY_ECHO=False
```

### 2. 数据库迁移
```bash
# 使用Alembic管理数据库版本
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 3. 部署方式
- **Docker**: 容器化部署
- **Gunicorn**: WSGI服务器
- **Nginx**: 反向代理
- **Supervisor**: 进程管理

---

## 📚 扩展开发方向

### 1. API层开发
- RESTful API设计
- JWT身份认证
- API文档 (Swagger)
- 接口限流

### 2. 业务逻辑层
- 用户服务
- 训练服务
- 社交服务
- 支付服务

### 3. 数据分析
- 训练效果分析
- 身体数据趋势
- 个性化推荐
- 数据可视化

### 4. 功能增强
- 实时消息推送
- 视频直播
- AI训练助手
- 社区论坛

---

## 🎓 技术栈

### 后端框架
- **Flask 2.3.3**: Web框架
- **SQLAlchemy 2.0**: ORM框架
- **PyMySQL**: MySQL驱动

### 数据库
- **MySQL 8.0+**: 关系型数据库
- **Redis**: 缓存数据库

### 开发工具
- **Python 3.8+**
- **Git**: 版本控制
- **VS Code**: 开发IDE

---

## ✅ 项目检查清单

### 基础功能
- [x] 数据库模型设计
- [x] 用户体系
- [x] 训练计划系统
- [x] 运动记录系统
- [x] 课程体系
- [x] 社交互动
- [x] 身体数据管理

### 技术特性
- [x] ORM映射
- [x] 关系设计
- [x] 索引优化
- [x] 数据验证
- [x] 软删除
- [x] 连接池

### 文档完善
- [x] README
- [x] 数据库设计文档
- [x] 快速开始指南
- [x] 架构说明

### 待开发功能
- [ ] API路由层
- [ ] JWT认证
- [ ] 业务逻辑层
- [ ] 单元测试
- [ ] API文档
- [ ] 部署配置

---

## 📞 联系方式

**项目**: Keep健身后端  
**版本**: v1.0.0  
**日期**: 2025-10-19  
**作者**: Keep健身后端团队  

---

**🎉 恭喜！您已完成企业级健身后端核心数据模型设计！**
