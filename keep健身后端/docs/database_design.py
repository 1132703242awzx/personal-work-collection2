"""
数据库关系图和设计文档

本文档描述了Keep健身应用的完整数据库设计
"""

# ============================================
# 数据库设计概览
# ============================================

"""
核心业务实体：

1. 用户体系 (User System)
   - users: 用户基础信息
   - user_profiles: 用户详细资料
   - user_settings: 用户设置

2. 训练计划 (Training Plan)
   - training_plans: 训练计划
   - plan_days: 计划每日安排
   - exercises: 运动动作

3. 运动记录 (Workout Record)
   - workout_records: 训练记录
   - exercise_records: 动作记录
   - set_records: 组记录

4. 课程体系 (Course System)
   - courses: 课程
   - chapters: 章节
   - videos: 视频

5. 社交互动 (Social)
   - follows: 关注关系
   - likes: 点赞
   - comments: 评论

6. 身体数据 (Body Data)
   - body_data: 身体数据汇总
   - weight_records: 体重记录
   - body_measurements: 身体围度测量
"""

# ============================================
# 关系映射详解
# ============================================

"""
一对一关系 (One-to-One):
├── User -> UserProfile
├── User -> UserSettings
└── 实现方式: ForeignKey + unique=True

一对多关系 (One-to-Many):
├── User -> TrainingPlan
├── User -> WorkoutRecord
├── User -> Comment
├── TrainingPlan -> PlanDay
├── PlanDay -> Exercise
├── WorkoutRecord -> ExerciseRecord
├── ExerciseRecord -> SetRecord
├── Course -> Chapter
└── Chapter -> Video
    实现方式: ForeignKey + relationship

多对多关系 (Many-to-Many):
└── User <-> User (通过Follow表)
    实现方式: 关联表 + 双向ForeignKey

多态关联 (Polymorphic):
├── Like (可关联: WorkoutRecord, Comment, Course等)
└── Comment (可关联: WorkoutRecord, Course, Video等)
    实现方式: target_type + target_id
"""

# ============================================
# 索引优化策略
# ============================================

"""
主键索引:
- 所有表的 id 字段（自动创建）

唯一索引:
├── users.username
├── users.email
├── users.phone
├── user_profiles.user_id
├── user_settings.user_id
└── follows.(follower_id, following_id) - 复合唯一索引

普通索引:
├── 时间字段: created_at, updated_at, workout_date
├── 状态字段: is_deleted, status, is_published, is_active
├── 外键字段: user_id, training_plan_id, course_id等
├── 分类字段: course_type, difficulty, muscle_group
└── 会员字段: is_premium

复合索引:
├── follows: (follower_id, created_at)
├── follows: (following_id, created_at)
├── likes: (user_id, target_type, target_id)
├── likes: (target_type, target_id, created_at)
├── comments: (target_type, target_id, created_at)
├── comments: (user_id, created_at)
├── body_data: (user_id, record_date)
└── weight_records: (user_id, record_date)
"""

# ============================================
# 数据完整性约束
# ============================================

"""
非空约束 (NOT NULL):
- 关键业务字段必须非空
- 例: username, email, password_hash, training_plan.name

唯一性约束 (UNIQUE):
- 防止数据重复
- 例: username, email, phone

外键约束 (FOREIGN KEY):
- 保证引用完整性
- 级联操作: CASCADE, SET NULL

检查约束 (CHECK):
- 通过枚举类型实现
- 例: GenderEnum, DifficultyEnum, UserStatusEnum

默认值 (DEFAULT):
- 状态字段: is_deleted=False, is_active=False
- 计数字段: followers_count=0, likes_count=0
- 时间字段: created_at=now(), updated_at=now()
"""

# ============================================
# 软删除设计
# ============================================

"""
所有表继承自 BaseModel，包含 is_deleted 字段
- 删除时设置 is_deleted=True
- 查询时过滤 is_deleted=False
- 保留历史数据用于审计和恢复
"""

# ============================================
# JSON字段应用
# ============================================

"""
灵活存储扩展数据:
├── user_settings.extra_settings - 用户额外设置
├── exercises.key_points - 动作要点
├── exercises.common_mistakes - 常见错误
├── workout_records.share_content - 分享内容
├── courses.tags - 课程标签
├── courses.learning_objectives - 学习目标
├── videos.video_quality - 多清晰度
├── videos.subtitles - 字幕
├── body_data.extra_data - 扩展身体数据
└── weight_records.photo_urls - 照片列表
"""

# ============================================
# 级联删除策略
# ============================================

"""
CASCADE (级联删除):
- User -> UserProfile, UserSettings, TrainingPlan, WorkoutRecord
- TrainingPlan -> PlanDay -> Exercise
- WorkoutRecord -> ExerciseRecord -> SetRecord
- Course -> Chapter -> Video
- 适用场景: 父记录删除，子记录也应删除

SET NULL (设置为空):
- WorkoutRecord.training_plan_id
- ExerciseRecord.exercise_id
- 适用场景: 保留记录但解除关联
"""

# ============================================
# 性能优化建议
# ============================================

"""
1. 查询优化:
   - 使用索引覆盖常见查询
   - 避免SELECT *，只查询需要的字段
   - 使用join代替多次查询

2. 连接池配置:
   - pool_size=10 (常规连接数)
   - max_overflow=20 (峰值额外连接)
   - pool_recycle=3600 (连接回收时间)

3. 分页查询:
   - 限制每页数量 (默认20，最大100)
   - 使用游标分页处理大数据集

4. 缓存策略:
   - 热点数据使用Redis缓存
   - 用户信息、课程列表等

5. 读写分离:
   - 主库写入，从库读取
   - 减轻主库压力
"""

# ============================================
# 数据统计字段设计
# ============================================

"""
实时统计字段（冗余设计，提升查询性能）:

用户相关:
├── user_profiles.followers_count - 粉丝数
├── user_profiles.following_count - 关注数
├── user_profiles.likes_count - 获赞数
└── user_profiles.workout_count - 训练次数

训练计划:
├── training_plans.usage_count - 使用次数
└── training_plans.completion_rate - 完成率

课程相关:
├── courses.view_count - 观看次数
├── courses.enrollment_count - 报名人数
├── courses.rating_average - 平均评分
└── videos.view_count - 视频观看次数

社交互动:
├── workout_records.likes_count - 点赞数
├── workout_records.comments_count - 评论数
└── comments.likes_count - 评论点赞数

更新策略:
- 使用触发器或应用层事务保证一致性
- 定期任务校验和修正统计数据
"""

# ============================================
# 数据安全设计
# ============================================

"""
1. 密码安全:
   - 使用bcrypt加密密码
   - 存储password_hash而非明文

2. 敏感信息:
   - 手机号、邮箱加密存储
   - 使用HTTPS传输

3. 数据备份:
   - 定期全量备份
   - 增量备份策略
   - 异地容灾

4. 访问控制:
   - 隐私设置 (UserSettings)
   - 数据可见性控制
"""
