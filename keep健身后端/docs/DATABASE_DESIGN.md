# Keep健身后端 - 数据库设计文档

## 📊 数据库架构总览

本系统采用关系型数据库设计，共包含 **15张核心表**，覆盖6大业务模块。

---

## 🗂️ 数据表清单

### 1️⃣ 用户体系 (3张表)
| 表名 | 说明 | 主要字段 |
|-----|------|---------|
| `users` | 用户基础信息 | username, email, phone, password_hash, status |
| `user_profiles` | 用户详细资料 | nickname, avatar, gender, height, weight, fitness_goal |
| `user_settings` | 用户设置 | profile_visible, email_notification, language, theme |

### 2️⃣ 训练计划 (3张表)
| 表名 | 说明 | 主要字段 |
|-----|------|---------|
| `training_plans` | 训练计划 | name, difficulty, duration_weeks, goal, is_template |
| `plan_days` | 每日训练安排 | day_number, description, estimated_duration |
| `exercises` | 运动动作库 | name, muscle_group, sets, reps, weight, rest_time |

### 3️⃣ 运动记录 (3张表)
| 表名 | 说明 | 主要字段 |
|-----|------|---------|
| `workout_records` | 训练记录 | workout_date, duration, calories_burned, is_completed |
| `exercise_records` | 动作记录 | exercise_name, completed_sets, total_reps, max_weight |
| `set_records` | 组详细记录 | set_number, reps, weight, duration, heart_rate |

### 4️⃣ 课程体系 (3张表)
| 表名 | 说明 | 主要字段 |
|-----|------|---------|
| `courses` | 课程 | title, course_type, level, instructor, price, rating |
| `chapters` | 章节 | title, order_number, is_free, is_locked |
| `videos` | 视频 | title, video_url, duration, view_count |

### 5️⃣ 社交互动 (3张表)
| 表名 | 说明 | 主要字段 |
|-----|------|---------|
| `follows` | 关注关系 | follower_id, following_id, is_mutual |
| `likes` | 点赞 | user_id, target_type, target_id |
| `comments` | 评论 | user_id, target_type, target_id, content, parent_id |

### 6️⃣ 身体数据 (3张表)
| 表名 | 说明 | 主要字段 |
|-----|------|---------|
| `body_data` | 身体数据汇总 | weight, body_fat, bmi, muscle_mass, bmr |
| `weight_records` | 体重详细记录 | weight, weight_change, target_weight, progress_rate |
| `body_measurements` | 身体围度 | chest, waist, hip, arm, leg measurements |

---

## 🔗 关系映射图

### 用户体系关系
```
User (1) ──────── (1) UserProfile
  │
  ├─────────────── (1) UserSettings
  │
  ├─────────────── (*) TrainingPlan
  │
  ├─────────────── (*) WorkoutRecord
  │
  ├─────────────── (*) BodyData
  │
  ├─────────────── (*) Comment
  │
  ├─────────────── (*) Like
  │
  └─────────────── (*) Follow
```

### 训练计划关系
```
TrainingPlan (1) ──── (*) PlanDay (1) ──── (*) Exercise
      │
      └──────────────────── (*) WorkoutRecord
```

### 运动记录关系
```
WorkoutRecord (1) ──── (*) ExerciseRecord (1) ──── (*) SetRecord
```

### 课程体系关系
```
Course (1) ──── (*) Chapter (1) ──── (*) Video
```

### 社交互动关系
```
User ───┬──── Follow ────┬──── User
        │                 │
        ├──── Like ───────┼──── WorkoutRecord
        │                 │
        └──── Comment ────┴──── Course/Video
```

---

## 🎯 索引优化策略

### 高频查询索引
| 表名 | 索引字段 | 索引类型 | 用途 |
|-----|---------|----------|-----|
| users | username | UNIQUE | 用户登录 |
| users | email | UNIQUE | 邮箱登录 |
| users | phone | UNIQUE | 手机登录 |
| users | (status, is_deleted) | INDEX | 用户列表查询 |
| workout_records | (user_id, workout_date) | INDEX | 用户训练历史 |
| follows | (follower_id, following_id) | UNIQUE | 关注关系 |
| likes | (user_id, target_type, target_id) | INDEX | 点赞查询 |
| comments | (target_type, target_id, created_at) | INDEX | 评论列表 |
| body_data | (user_id, record_date) | INDEX | 身体数据趋势 |

### 复合索引设计
```sql
-- 关注关系查询优化
CREATE INDEX idx_follower_created ON follows(follower_id, created_at);
CREATE INDEX idx_following_created ON follows(following_id, created_at);

-- 社交互动查询优化
CREATE INDEX idx_user_target ON likes(user_id, target_type, target_id);
CREATE INDEX idx_target ON likes(target_type, target_id, created_at);

-- 评论查询优化
CREATE INDEX idx_target_comment ON comments(target_type, target_id, created_at);
CREATE INDEX idx_user_created ON comments(user_id, created_at);
```

---

## 🔐 数据完整性约束

### 外键约束
| 子表 | 外键字段 | 父表 | 级联规则 |
|-----|---------|------|---------|
| user_profiles | user_id | users | CASCADE |
| training_plans | user_id | users | CASCADE |
| workout_records | training_plan_id | training_plans | SET NULL |
| plan_days | training_plan_id | training_plans | CASCADE |
| exercise_records | workout_record_id | workout_records | CASCADE |

### 唯一性约束
- `users`: username, email, phone
- `user_profiles`: user_id
- `user_settings`: user_id
- `follows`: (follower_id, following_id)

### 枚举约束
```python
GenderEnum = ["male", "female", "other"]
UserStatusEnum = ["active", "inactive", "suspended", "deleted"]
DifficultyEnum = ["beginner", "intermediate", "advanced"]
MuscleGroupEnum = ["chest", "back", "shoulders", "arms", "legs", "core"]
CourseTypeEnum = ["video", "live", "article"]
```

---

## 📈 统计字段设计

### 用户统计
- `followers_count`: 粉丝数
- `following_count`: 关注数
- `likes_count`: 获赞总数
- `workout_count`: 训练总次数

### 训练统计
- `total_sets`: 总组数
- `total_reps`: 总次数
- `calories_burned`: 消耗卡路里
- `completion_rate`: 完成率

### 课程统计
- `view_count`: 观看次数
- `enrollment_count`: 报名人数
- `rating_average`: 平均评分
- `completion_count`: 完成人数

---

## 🛡️ 安全设计

### 密码安全
- 使用 bcrypt 加密
- 存储 password_hash
- 最小长度8位，包含大小写字母和数字

### 软删除
- 所有表包含 `is_deleted` 字段
- 删除时标记而非物理删除
- 保留数据用于审计

### 隐私保护
- `profile_visible`: 资料可见性
- `workout_visible`: 训练记录可见性
- `allow_follow`: 是否允许关注

---

## 🚀 性能优化建议

### 1. 连接池配置
```python
pool_size = 10              # 常规连接数
max_overflow = 20           # 峰值额外连接
pool_recycle = 3600        # 连接回收时间(秒)
pool_timeout = 30          # 连接超时时间(秒)
```

### 2. 查询优化
- ✅ 使用索引覆盖查询
- ✅ 避免 SELECT *
- ✅ 使用 JOIN 代替多次查询
- ✅ 分页查询限制数量

### 3. 缓存策略
- 用户信息缓存 (Redis)
- 课程列表缓存
- 热门动作缓存
- 排行榜缓存

### 4. 读写分离
- 主库：写操作
- 从库：读操作
- 减轻主库压力

---

## 📊 数据字典

### 字段命名规范
- **主键**: `id`
- **外键**: `{table}_id` (如: user_id, course_id)
- **时间戳**: `created_at`, `updated_at`
- **状态**: `is_{status}` (如: is_deleted, is_active)
- **计数**: `{item}_count` (如: likes_count, followers_count)
- **枚举**: 使用复数形式 (如: GenderEnum, StatusEnum)

### 时间字段
- `created_at`: 创建时间 (自动)
- `updated_at`: 更新时间 (自动)
- `workout_date`: 训练日期
- `record_date`: 记录日期
- `last_login_at`: 最后登录时间

---

## 🔄 级联操作

### CASCADE (级联删除)
```
User 删除 → 自动删除
  ├─ UserProfile
  ├─ UserSettings
  ├─ TrainingPlan
  ├─ WorkoutRecord
  ├─ Follow
  ├─ Like
  └─ Comment
```

### SET NULL (设置为空)
```
TrainingPlan 删除 → WorkoutRecord.training_plan_id = NULL
Exercise 删除 → ExerciseRecord.exercise_id = NULL
```

---

## 📝 使用示例

### 创建用户
```python
user = User(
    username="john_doe",
    email="john@example.com",
    password_hash=hash_password("Password123")
)
db.session.add(user)
db.session.commit()
```

### 查询用户训练记录
```python
records = WorkoutRecord.query\
    .filter_by(user_id=user_id, is_deleted=False)\
    .order_by(WorkoutRecord.workout_date.desc())\
    .limit(10)\
    .all()
```

### 统计数据查询
```python
from sqlalchemy import func

stats = db.session.query(
    func.count(WorkoutRecord.id).label('total_workouts'),
    func.sum(WorkoutRecord.calories_burned).label('total_calories'),
    func.avg(WorkoutRecord.duration).label('avg_duration')
).filter(
    WorkoutRecord.user_id == user_id,
    WorkoutRecord.is_deleted == False
).first()
```

---

## 🎨 ER图说明

### 实体关系
- **一对一**: User ↔ UserProfile (一个用户对应一个资料)
- **一对多**: User → WorkoutRecord (一个用户有多个训练记录)
- **多对多**: User ↔ User (通过Follow表实现关注关系)
- **多态**: Like/Comment (可以关联多种目标类型)

---

## ✅ 设计特点

### ✨ 核心优势
1. **模块化设计**: 6大业务模块清晰分离
2. **关系完整**: 覆盖一对一、一对多、多对多关系
3. **索引优化**: 针对高频查询建立索引
4. **软删除**: 数据安全可恢复
5. **扩展性**: JSON字段支持灵活扩展
6. **统计冗余**: 提升查询性能

### 🎯 企业级特性
- ✅ 连接池管理
- ✅ 事务支持
- ✅ 级联操作
- ✅ 数据验证
- ✅ 安全加密
- ✅ 审计日志

---

**文档版本**: v1.0  
**更新日期**: 2025-10-19  
**维护者**: Keep健身后端团队
