# Keep健身后端

企业级健身应用后端系统，基于Flask + SQLAlchemy构建。

## 项目结构

```
keep健身后端/
├── app.py                 # 主应用文件
├── requirements.txt       # 项目依赖
├── README.md             # 项目文档
├── .env                  # 环境变量配置
│
├── config/               # 配置模块
│   ├── __init__.py
│   ├── config.py        # 应用配置
│   └── database.py      # 数据库配置
│
├── models/              # 数据模型
│   ├── __init__.py
│   ├── base.py         # 基础模型
│   ├── user.py         # 用户模型
│   ├── training.py     # 训练计划模型
│   ├── workout.py      # 运动记录模型
│   ├── course.py       # 课程模型
│   ├── social.py       # 社交模型
│   └── body_data.py    # 身体数据模型
│
├── utils/              # 工具模块
│   ├── __init__.py
│   ├── init_db.py     # 数据库初始化
│   ├── validators.py  # 数据验证
│   └── pagination.py  # 分页工具
│
├── static/            # 静态文件
└── templates/         # 模板文件
```

## 核心数据模型

### 1. 用户体系 (User System)
- **User**: 用户基础信息
- **UserProfile**: 用户详细资料
- **UserSettings**: 用户设置
- **UserRole**: 用户角色（普通用户/教练/管理员）

### 2. 训练计划 (Training Plan)
- **TrainingPlan**: 训练计划
- **PlanDay**: 计划每日安排
- **Exercise**: 运动动作

### 3. 运动记录 (Workout Record)
- **WorkoutRecord**: 训练记录
- **ExerciseRecord**: 动作记录
- **SetRecord**: 组记录

### 4. 课程体系 (Course System)
- **Course**: 课程
- **Chapter**: 章节
- **Video**: 视频

### 5. 社交互动 (Social) ✨EXPANDED
**关系管理**
- **Follow**: 关注关系（互关检测、分组标签、屏蔽）

**动态内容**
- **Feed**: 动态（训练/成就/图文/视频，可见性控制）
- **FeedShare**: 分享记录
- **Hashtag**: 话题标签（热门推荐）
- **HashtagFollow**: 标签关注

**互动系统**
- **Like**: 点赞（动态/评论/训练记录）
- **Comment**: 评论（嵌套回复、@提到）

**通知系统**
- **Notification**: 通知（9种类型，已读状态）
- **NotificationSetting**: 通知偏好设置

**消息系统**
- **Message**: 私信（文字/图片/训练/动态分享）
- **Conversation**: 会话（未读计数）

**成就系统**
- **Achievement**: 成就徽章（稀有度、解锁条件）
- **UserAchievement**: 用户成就记录

### 6. 身体数据 (Body Data)
- **BodyData**: 身体数据汇总
- **WeightRecord**: 体重记录
- **BodyMeasurements**: 身体围度

### 7. 认证系统 (Authentication)
- **RefreshToken**: 刷新令牌
- **ThirdPartyAccount**: 第三方账号
- **PasswordResetToken**: 密码重置令牌
- **LoginHistory**: 登录历史
- **SecurityLog**: 安全日志测量

## 技术特性

### ORM特性
- ✅ SQLAlchemy ORM模型
- ✅ 关系映射（一对多、多对多）
- ✅ 级联删除和更新
- ✅ 软删除支持
- ✅ 自动时间戳

### 数据验证
- ✅ 字段类型约束
- ✅ 非空约束
- ✅ 唯一性约束
- ✅ 外键约束
- ✅ 枚举类型

### 索引优化
- ✅ 主键索引
- ✅ 唯一索引
- ✅ 普通索引
- ✅ 复合索引
- ✅ 外键索引

### 企业级特性
- ✅ 连接池管理
- ✅ 事务处理
- ✅ 错误处理
- ✅ 分页支持
- ✅ 数据验证
- ✅ JSON字段支持

## API接口

### 认证系统API (2个)
- **POST** `/api/auth/register` - 用户注册
- **POST** `/api/auth/login` - 用户登录

### 训练计划API (8个)
- **POST** `/api/plans` - 创建训练计划
- **GET** `/api/plans` - 获取计划列表
- **GET** `/api/plans/{id}` - 获取计划详情
- **PUT** `/api/plans/{id}` - 更新计划
- **DELETE** `/api/plans/{id}` - 删除计划
- **POST** `/api/plans/{id}/copy` - 复制模板计划
- **POST** `/api/plans/{id}/activate` - 激活计划
- **POST** `/api/plans/{id}/deactivate` - 停用计划

### 运动记录API (18个) ✨NEW
**基础操作 (6个)**
- **POST** `/api/workouts` - 创建训练记录
- **GET** `/api/workouts` - 获取训练列表
- **GET** `/api/workouts/{id}` - 获取训练详情
- **PUT** `/api/workouts/{id}` - 更新训练记录
- **DELETE** `/api/workouts/{id}` - 删除训练记录
- **POST** `/api/workouts/{id}/finish` - 完成训练

**训练组操作 (3个)**
- **POST** `/api/workouts/{id}/sets` - 添加训练组
- **PUT** `/api/sets/{id}` - 更新训练组
- **DELETE** `/api/sets/{id}` - 删除训练组

**查询功能 (2个)**
- **GET** `/api/workouts/calendar` - 获取训练日历
- **GET** `/api/workouts/records` - 获取个人最佳记录

**统计功能 (7个)**
- **GET** `/api/stats/overview` - 统计总览
- **GET** `/api/stats/weekly` - 周统计
- **GET** `/api/stats/monthly` - 月统计
- **GET** `/api/stats/muscle-distribution` - 肌群分布
- **GET** `/api/stats/workout-types` - 训练类型分布
- **GET** `/api/stats/progress` - 进步趋势
- **GET** `/api/stats/achievements` - 成就统计

### 社交系统API (30个) ✨NEW
**关注关系 (6个)**
- **POST** `/api/social/follow` - 关注用户
- **POST** `/api/social/unfollow/{id}` - 取消关注
- **PUT** `/api/social/follow/{id}` - 更新关注信息
- **GET** `/api/social/following` - 我的关注列表
- **GET** `/api/social/followers` - 我的粉丝列表
- **GET** `/api/social/follow-status/{id}` - 检查关注状态

**动态Feed (7个)**
- **POST** `/api/social/feeds` - 发布动态
- **GET** `/api/social/feeds/{id}` - 获取动态详情
- **GET** `/api/social/timeline` - 关注用户动态流
- **GET** `/api/social/explore` - 探索热门动态
- **GET** `/api/social/users/{id}/feeds` - 用户动态列表
- **PUT** `/api/social/feeds/{id}` - 更新动态
- **DELETE** `/api/social/feeds/{id}` - 删除动态

**互动系统 (4个)**
- **POST** `/api/social/like` - 点赞/取消点赞
- **POST** `/api/social/comments` - 发表评论
- **GET** `/api/social/comments` - 获取评论列表
- **DELETE** `/api/social/comments/{id}` - 删除评论

**通知系统 (4个)**
- **GET** `/api/social/notifications` - 获取通知列表
- **POST** `/api/social/notifications/read` - 标记已读
- **GET** `/api/social/notifications/unread-count` - 未读数量
- **GET/PUT** `/api/social/notification-settings` - 通知设置

**消息系统 (3个)**
- **POST** `/api/social/messages` - 发送私信
- **GET** `/api/social/conversations` - 会话列表
- **GET** `/api/social/conversations/{id}/messages` - 会话消息

**成就系统 (2个)**
- **GET** `/api/social/users/{id}/achievements` - 用户成就
- **GET** `/api/social/achievements` - 所有成就

**标签系统 (3个)**
- **GET** `/api/social/hashtags/trending` - 热门标签
- **POST** `/api/social/hashtags/{id}/follow` - 关注标签
- **DELETE** `/api/social/hashtags/{id}/follow` - 取消关注标签
- **GET** `/api/stats/consistency` - 坚持度评分

### 数据分析API (11个) ✨NEW
**核心统计 (8个)**
- **GET** `/api/analytics/overview` - 数据概览
- **GET** `/api/analytics/frequency` - 训练频率统计
- **GET** `/api/analytics/duration` - 训练时长统计
- **GET** `/api/analytics/strength-progress` - 力量进步分析
- **GET** `/api/analytics/body-trends` - 身体数据趋势
- **GET** `/api/analytics/calories` - 卡路里统计
- **GET** `/api/analytics/volume` - 训练容量统计
- **GET** `/api/analytics/achievements` - 成就汇总

**综合分析 (3个)**
- **GET** `/api/analytics/dashboard` - 综合仪表盘
- **GET** `/api/analytics/leaderboard` - 排行榜
- **POST** `/api/analytics/comparison` - 用户对比

**总计: 69+个API接口**

详细文档：
- [训练计划API文档](docs/TRAINING_API.md)
- [运动记录API速查表](docs/WORKOUT_API_QUICK_REFERENCE.md)
- [社交系统API文档](SOCIAL_API.md)
- [数据分析API文档](ANALYTICS_API.md) ✨NEW

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt

# 重要: 安装pydantic (运动记录系统必需)
pip install pydantic==2.5.0
```

### 2. 配置数据库

创建 `.env` 文件：

```env
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/keep_fitness?charset=utf8mb4
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
FLASK_ENV=development
```

### 3. 初始化数据库

```bash
# 创建数据表
python utils/init_db.py create

# 重置数据库（慎用）
python utils/init_db.py reset
```

### 4. 运行应用

```bash
python app.py
```

访问 http://localhost:5000

### 5. 测试API

```bash
# 测试认证系统
python test_auth.py

# 测试训练计划API
python test_training.py

# 测试运动记录API
python test_workout.py

# 测试社交系统API ✨NEW
python test_social.py

# 测试数据分析API ✨NEW
python test_analytics.py
```

更多信息：
- [运动记录快速启动指南](WORKOUT_QUICKSTART.md)
- [社交系统API文档](SOCIAL_API.md)
- [社交系统快速参考](SOCIAL_QUICK_REFERENCE.md)
- [数据分析系统使用指南](ANALYTICS_README.md) ✨NEW
- [数据分析API文档](ANALYTICS_API.md) ✨NEW
- [数据分析快速参考](ANALYTICS_QUICK_REFERENCE.md) ✨NEW
- [项目状态报告](PROJECT_STATUS_REPORT.md)

## 数据库设计亮点

### 1. 用户体系设计
- 用户信息分离（基础信息、资料、设置）
- 支持多种登录方式
- 完善的隐私设置
- 会员等级体系

### 2. 训练计划设计
- 模板化训练计划
- 灵活的每日安排
- 详细的动作库
- 支持自定义和公开分享

### 3. 运动记录设计
- 三层记录结构（训练-动作-组）
- 完整的训练数据追踪
- 个人记录标记
- 训练感受评分

### 4. 课程体系设计
- 多种课程类型支持
- 章节-视频层级结构
- 灵活的访问控制
- 多清晰度视频支持

### 5. 社交互动设计 ✨EXPANDED
**关系管理**
- 关注/粉丝体系（互相关注检测）
- 分组标签和备注支持
- 动态屏蔽功能

**动态内容系统**
- 多种动态类型（训练/成就/图文/视频）
- 三级可见性控制（公开/好友/私密）
- 话题标签系统（热门推荐）
- 自动提取训练摘要

**互动系统**
- 多态点赞系统（动态/评论/训练）
- 嵌套评论支持（两级结构）
- @提到用户功能
- 互动统计实时更新

**通知系统**
- 9种通知类型（关注/点赞/评论/回复/提到/分享/成就/系统/提醒/里程碑）
- 用户偏好设置（分类开关、免打扰时段）
- 未读计数和批量已读

**消息和成就**
- 私信系统（文字/图片/分享）
- 会话管理（未读计数）
- 成就徽章系统（稀有度、解锁条件）
- 用户成就进度追踪

### 6. 身体数据设计
- 全面的身体指标追踪
- 体重变化趋势
- 身体围度测量
- 数据来源追溯

### 7. 数据分析设计 ✨NEW
**多维度统计**
- 训练频率和连续天数追踪
- 训练时长分布分析
- 力量进步曲线生成
- 身体数据变化趋势
- 卡路里和训练容量统计

**排行榜系统**
- 5种排名指标（训练次数/时长/卡路里/容量/成就）
- 3种排名范围（全局/好友/关注）
- 实时排名更新

**数据可视化**
- 5种图表类型支持（折线/柱状/饼图/面积/散点）
- 图表数据自动生成
- 灵活时间范围（周/月/季度/年/全部）

**对比分析**
- 多用户数据对比（2-5人）
- 多指标同时对比
- 对比图表生成

## 索引策略

### 查询优化索引
- 用户登录：username, email, phone
- 时间查询：created_at, workout_date
- 状态过滤：is_deleted, status, is_published
- 关联查询：外键字段

### 复合索引
- 用户关注：(follower_id, following_id)
- 社交互动：(target_type, target_id, created_at)
- 身体数据：(user_id, record_date)

## 最佳实践

### 1. 数据完整性
- 使用外键约束保证引用完整性
- 使用唯一约束防止数据重复
- 使用枚举类型限制字段值

### 2. 性能优化
- 合理使用索引提升查询性能
- 使用连接池管理数据库连接
- 避免N+1查询问题

### 3. 数据安全
- 密码加密存储
- 软删除保留数据
- 敏感信息加密

### 4. 可扩展性
- JSON字段存储扩展数据
- 模块化设计便于维护
- 清晰的关系映射

## 已完成功能

### ✅ 数据模型层 (31张表) ✨EXPANDED
- 用户体系（User, UserProfile, UserSettings, UserRole）
- 训练计划（TrainingPlan, PlanDay, Exercise）
- 运动记录（WorkoutRecord, ExerciseRecord, SetRecord）
- 课程体系（Course, Chapter, Video）
- 社交互动（Follow, Like, Comment, Feed, FeedShare, Hashtag, HashtagFollow）
- 通知系统（Notification, NotificationSetting）
- 消息系统（Message, Conversation）
- 成就系统（Achievement, UserAchievement）
- 身体数据（BodyData, WeightRecord, BodyMeasurements）
- 认证系统（RefreshToken, ThirdPartyAccount, PasswordResetToken, LoginHistory, SecurityLog）

### ✅ 认证系统
- JWT令牌认证
- 用户注册和登录
- 密码加密存储
- 认证中间件

### ✅ 训练计划管理
- 计划CRUD操作
- 计划模板系统
- 训练日和动作管理
- 计划筛选和搜索
- 进度跟踪
- 难度级别适配
- 完整文档和测试

### ✅ 运动记录跟踪 ✨NEW
- **数据验证**: Pydantic运行时验证
- **训练记录**: 完整的CRUD操作
- **训练组管理**: 实时添加/更新训练组
- **个人记录**: 自动检测和追踪PR
- **训练日历**: 月度视图和聚合
- **统计分析**: 多维度数据分析
- **文档**: 完整API文档和快速指南
- **测试工具**: 交互式测试工具

### ✅ 社交系统 ✨NEW
- **关系管理**: 关注/取消关注、互关检测、分组标签
- **动态Feed**: 多类型动态、可见性控制、时间线生成
- **互动系统**: 点赞/取消、嵌套评论、@提到
- **通知系统**: 9种通知类型、偏好设置、未读计数
- **消息系统**: 私信、会话管理、消息类型
- **成就系统**: 徽章解锁、进度追踪、稀有度
- **标签系统**: 话题标签、热门推荐、标签关注
- **探索页**: 热度算法、公开动态推荐
- **文档**: 完整API文档(30个接口)和快速参考
- **测试工具**: 全功能交互式测试工具

### ✅ 数据分析系统 ✨NEW
- **多维度统计**: 训练频率、时长、力量进步、身体数据、卡路里、训练容量
- **连续天数追踪**: 当前连续、最长连续、训练频率计算
- **力量进步分析**: 按运动统计重量进步、进步曲线、训练容量
- **身体数据趋势**: 体重/体脂变化、趋势检测（上升/下降/稳定）
- **排行榜系统**: 5种指标、3种范围、实时排名更新
- **用户对比**: 多用户多指标对比、对比图表生成
- **图表生成**: 5种图表类型、自动数据格式化
- **综合仪表盘**: 整合所有统计数据、一站式数据展示
- **文档**: 完整API文档(11个接口)、快速参考、使用指南
- **测试工具**: 交互式测试工具、批量测试

## 待开发功能

### ⏳ 数据分析增强
- Redis缓存实现（排行榜、仪表盘数据缓存）
- 定时统计任务（APScheduler后台任务）
- 周报/月报自动生成
- 数据导出功能（PDF/Excel）
- AI健身建议（基于数据分析）

### ⏳ 社交系统增强
- WebSocket实时通知
- 消息已读回执
- 社交数据分析
- 推荐算法优化
- 动态置顶功能
- 用户黑名单

### ✅ 服务层
- 认证服务（AuthService）
- 训练计划服务（TrainingService）
- 运动记录服务（WorkoutService）
- 统计分析服务（StatsService）
- 社交关系服务（SocialService）
- 动态Feed服务（FeedService）
- 互动服务（InteractionService）
- 通知服务（NotificationService）
- 数据分析服务（AnalyticsService） ✨NEW
- 排行榜服务（LeaderboardService） ✨NEW
- 用户对比服务（ComparisonService） ✨NEW

### ✅ 验证层
- Pydantic数据验证schemas
- 请求数据验证
- 响应数据序列化
- 训练记录验证schemas
- 社交系统验证schemas
- 数据分析验证schemas ✨NEW

### ✅ 文档
- 数据库设计文档
- 训练计划API完整文档
- 运动记录API速查表
- 运动记录快速启动指南
- 社交系统API完整文档
- 社交系统快速参考
- 数据分析系统使用指南 ✨NEW
- 数据分析API完整文档 ✨NEW
- 数据分析快速参考 ✨NEW
- 项目状态报告
- 测试指南

**项目进度: 80% → 核心功能全部完成,数据分析上线!**

## 下一步开发

### 🔜 短期任务
1. ✅ 运动记录系统 - 已完成!
2. ✅ 社交系统 - 已完成!
3. ✅ 数据分析系统 - 已完成!
4. 系统完整测试和部署准备

### 🔜 中期功能
1. **课程管理API** - 视频课程的CRUD
2. **身体数据API** - 体重和围度记录完善
3. **搜索功能** - 全文搜索训练计划和课程
4. **数据分析增强** - Redis缓存、定时任务、报告生成

### 🔜 长期规划
1. **WebSocket实时通知** - 社交系统实时推送
2. **AI推荐系统** - 基于数据的智能推荐
3. **管理后台** - 用户管理、内容审核
4. **移动端优化** - API性能优化、离线支持

### 🔧 性能优化
- Redis缓存集成
- 数据库查询优化
- CDN静态资源加速
- 接口限流保护

### 🧪 测试覆盖
- 单元测试
- 集成测试
- 性能测试
- 压力测试

## 项目亮点

### 🏗️ 架构设计
- **分层架构**: Models → Services → API，职责清晰
- **蓝图组织**: 按业务模块组织路由
- **工厂模式**: 应用工厂函数支持多环境配置
- **依赖注入**: 服务层解耦，易于测试

### 🔒 安全特性
- **JWT认证**: 无状态令牌认证
- **角色权限**: 细粒度权限控制
- **密码加密**: Bcrypt加密存储
- **软删除**: 数据安全保护
- **审计日志**: 完整的操作记录

### 📊 数据设计
- **标准化设计**: 避免数据冗余
- **关系完整性**: 外键约束保证一致性
- **索引优化**: 提升查询性能
- **扩展性**: JSON字段支持灵活扩展

### 🎯 业务特色
- **计划模板**: 复用优质训练计划
- **进度跟踪**: 完整的训练历史
- **难度适配**: 多级难度选择
- **社交互动**: 激励用户坚持

## License

MIT
