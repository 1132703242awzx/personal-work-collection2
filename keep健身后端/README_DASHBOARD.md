# Keep健身仪表盘 v2.0

基于Flask服务器端渲染的健身数据统计仪表盘系统

## 🎯 项目特点

- **服务器端渲染**: 使用Jinja2模板引擎,非RESTful架构
- **轻量级数据库**: 开发环境使用SQLite,生产环境支持PostgreSQL
- **现代化UI**: Bootstrap 5 + Bootstrap Icons
- **数据可视化**: Chart.js图表库
- **用户认证**: Flask-Login会话管理
- **数据分析**: Pandas数据处理和统计

## 📋 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.9+ | 后端语言 |
| Flask | 2.3.3 | Web框架 |
| SQLAlchemy | 2.0.20 | ORM |
| Flask-Login | 0.6.2 | 用户认证 |
| Jinja2 | 3.1+ | 模板引擎 |
| Bootstrap | 5.3.0 | UI框架 |
| Chart.js | 4.4.0 | 数据可视化 |
| Pandas | 2.0.3 | 数据分析 |
| SQLite | 3.x | 数据库(开发) |

## 🚀 快速开始

### 方式1: 使用启动脚本(推荐)

双击运行 `start_dashboard.bat`,脚本会自动:
1. 创建虚拟环境
2. 安装依赖包
3. 初始化数据库
4. 启动服务器

### 方式2: 手动启动

```powershell
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements_dashboard.txt

# 4. 初始化数据库
python init_dashboard.py

# 5. 启动服务器
python app_dashboard.py
```

## 🌐 访问应用

启动后访问: **http://localhost:5000**

### 测试账号

- 用户名: `demo`
- 密码: `123456`

## 📁 项目结构

```
keep健身后端/
├── app_dashboard.py          # 主应用入口
├── dashboard_config.py       # 配置文件
├── dashboard_models.py       # 数据模型
├── dashboard_auth.py         # 认证蓝图
├── dashboard_main.py         # 主页蓝图
├── dashboard_workout.py      # 运动记录蓝图
├── dashboard_analytics.py    # 数据分析蓝图
├── init_dashboard.py         # 数据库初始化脚本
├── requirements_dashboard.txt # 依赖列表
├── start_dashboard.bat       # 快速启动脚本
├── keep_fitness.db           # SQLite数据库(自动生成)
├── static/                   # 静态文件
│   └── css/
│       └── style.css         # 自定义样式
└── templates/                # Jinja2模板
    ├── base.html             # 基础模板
    ├── auth/                 # 认证相关
    │   ├── login.html        # 登录页
    │   ├── register.html     # 注册页
    │   └── profile.html      # 个人资料
    ├── dashboard/            # 仪表盘
    │   └── index.html        # 仪表盘主页
    ├── workout/              # 运动记录
    │   ├── records.html      # 记录列表
    │   ├── add.html          # 添加记录
    │   └── body_records.html # 身体数据
    └── analytics/            # 数据分析
        ├── overview.html     # 数据概览
        ├── workout_stats.html# 运动统计
        └── body_stats.html   # 身体数据统计
```

## 🔥 核心功能

### 1. 用户管理
- ✅ 用户注册/登录/登出
- ✅ 个人资料管理
- ✅ 密码修改
- ✅ 会话管理(记住我)

### 2. 运动记录
- ✅ 添加运动记录
- ✅ 查看运动历史
- ✅ 编辑/删除记录
- ✅ 支持多种运动类型

### 3. 身体数据
- ✅ 体重记录
- ✅ 体脂率追踪
- ✅ BMI计算
- ✅ 历史数据查看

### 4. 数据可视化
- ✅ 运动趋势图表(Chart.js)
- ✅ 运动类型分布
- ✅ 体重趋势曲线
- ✅ 统计卡片展示

### 5. 数据分析
- ✅ 使用Pandas进行数据处理
- ✅ 运动统计汇总
- ✅ 趋势分析
- ✅ 个人运动报告

## 📊 数据模型

### User (用户)
- 用户名、邮箱、密码
- 个人信息(昵称、性别、生日、身高)
- 账号状态、最后登录时间

### WorkoutRecord (运动记录)
- 运动类型、名称
- 日期、时长、消耗卡路里
- 距离、难度、备注

### BodyRecord (身体数据)
- 记录日期
- 体重、体脂率、肌肉量
- 各部位围度

### TrainingPlan (训练计划)
- 计划名称、描述
- 目标、难度
- 周期、频率

## 🎨 界面特点

- **响应式设计**: 支持PC/平板/手机
- **现代化UI**: Bootstrap 5组件
- **数据可视化**: Chart.js图表
- **友好交互**: 实时反馈、提示信息
- **清晰导航**: 面包屑、菜单导航

## 🔧 配置说明

### 开发环境 (默认)
- 数据库: SQLite
- 调试模式: 开启
- 会话: HTTP Only

### 生产环境
修改 `dashboard_config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/keep_fitness'
DEBUG = False
SESSION_COOKIE_SECURE = True
```

## 📈 性能优化

- 数据库查询优化
- Pandas数据缓存
- 分页加载
- 静态资源CDN

## 🔒 安全特性

- 密码哈希(Werkzeug)
- CSRF保护
- XSS防护
- SQL注入防护
- 会话安全

## 📝 待开发功能

- [ ] 训练计划管理
- [ ] 数据导出(Excel/PDF)
- [ ] 社交功能(分享、点赞)
- [ ] 移动端App
- [ ] 更多图表类型

## 🤝 贡献

欢迎提交Issue和Pull Request!

## 📄 许可证

MIT License

## 📧 联系方式

如有问题,请联系开发团队

---

**Keep健身仪表盘 v2.0** - 让数据驱动你的健身之旅! 💪
