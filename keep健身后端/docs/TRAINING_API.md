# 训练计划管理API文档

## 📋 概述

训练计划管理API提供了完整的CRUD操作，支持计划模板、自定义计划、训练进度跟踪等功能。

**基础路径**: `/api/plans`

**认证方式**: Bearer Token (JWT)

---

## 🔑 核心概念

### 1. 训练计划类型

- **自定义计划**: 用户创建的个人训练计划
- **模板计划**: 公开的、可复用的训练计划模板
- **激活计划**: 当前正在执行的训练计划（每个用户同时只能有一个激活计划）

### 2. 难度等级

- `beginner`: 初级
- `intermediate`: 中级
- `advanced`: 高级

### 3. 目标肌群

- `chest`: 胸部
- `back`: 背部
- `shoulders`: 肩部
- `arms`: 手臂
- `legs`: 腿部
- `core`: 核心
- `cardio`: 有氧
- `full_body`: 全身

### 4. 训练目标

- 减脂 (fat_loss)
- 增肌 (muscle_gain)
- 塑形 (body_shaping)
- 体能 (endurance)

---

## 📡 API端点

### 1. 创建训练计划

**端点**: `POST /api/plans`

**权限**: 需要登录

**请求体**:
```json
{
  "name": "8周增肌训练计划",
  "description": "适合中级健身者的全面增肌计划",
  "cover_image": "https://example.com/cover.jpg",
  "difficulty": "intermediate",
  "duration_weeks": 8,
  "days_per_week": 5,
  "goal": "增肌",
  "target_muscle_group": "full_body",
  "is_active": false,
  "is_public": false,
  "plan_days": [
    {
      "day_number": 1,
      "day_name": "胸部+三头肌",
      "description": "胸部和三头肌强化训练",
      "warm_up": "动态拉伸5分钟",
      "cool_down": "静态拉伸10分钟",
      "estimated_duration": 60,
      "target_calories": 400,
      "rest_time": 90,
      "exercises": [
        {
          "name": "杠铃卧推",
          "description": "经典的胸部力量训练动作",
          "video_url": "https://example.com/videos/bench-press.mp4",
          "image_url": "https://example.com/images/bench-press.jpg",
          "exercise_type": "力量",
          "muscle_group": "chest",
          "equipment": "杠铃",
          "order_number": 1,
          "sets": 4,
          "reps": 10,
          "weight": 60,
          "rest_time": 90,
          "difficulty": "intermediate",
          "calories_per_set": 50,
          "key_points": [
            "保持肩胛骨收紧",
            "下放时控制速度",
            "推起时胸部发力"
          ],
          "common_mistakes": [
            "臀部离开卧推凳",
            "手肘过度外展",
            "不完全伸展手臂"
          ]
        },
        {
          "name": "哑铃飞鸟",
          "description": "胸部孤立训练动作",
          "exercise_type": "力量",
          "muscle_group": "chest",
          "equipment": "哑铃",
          "order_number": 2,
          "sets": 3,
          "reps": 12,
          "weight": 15,
          "rest_time": 60,
          "difficulty": "intermediate",
          "calories_per_set": 40
        },
        {
          "name": "绳索下压",
          "description": "三头肌孤立训练",
          "exercise_type": "力量",
          "muscle_group": "arms",
          "equipment": "绳索",
          "order_number": 3,
          "sets": 3,
          "reps": 15,
          "rest_time": 60,
          "difficulty": "beginner",
          "calories_per_set": 30
        }
      ]
    },
    {
      "day_number": 2,
      "day_name": "背部+二头肌",
      "description": "背部和二头肌强化训练",
      "estimated_duration": 65,
      "target_calories": 420,
      "exercises": [
        {
          "name": "引体向上",
          "exercise_type": "力量",
          "muscle_group": "back",
          "equipment": "单杠",
          "order_number": 1,
          "sets": 4,
          "reps": 8,
          "rest_time": 90,
          "difficulty": "advanced",
          "calories_per_set": 60
        }
      ]
    }
  ]
}
```

**响应** (201 Created):
```json
{
  "message": "计划创建成功",
  "plan": {
    "id": 1,
    "name": "8周增肌训练计划",
    "description": "适合中级健身者的全面增肌计划",
    "difficulty": "intermediate",
    "duration_weeks": 8,
    "days_per_week": 5,
    "goal": "增肌",
    "target_muscle_group": "full_body",
    "is_active": false,
    "is_template": false,
    "is_public": false,
    "usage_count": 0,
    "completion_rate": 0,
    "created_at": "2025-10-19T10:00:00",
    "plan_days": [...]
  }
}
```

---

### 2. 获取训练计划列表

**端点**: `GET /api/plans`

**权限**: 需要登录

**查询参数**:
- `page` (int): 页码，默认1
- `per_page` (int): 每页数量，默认20，最大100
- `my_plans` (bool): 只显示我的计划
- `templates` (bool): 只显示模板
- `difficulty` (string): 难度筛选 (beginner/intermediate/advanced)
- `target_muscle_group` (string): 目标肌群筛选
- `goal` (string): 训练目标筛选
- `is_active` (bool): 是否激活
- `keyword` (string): 搜索关键词
- `order_by` (string): 排序方式 (created_at/usage_count/completion_rate)

**请求示例**:
```http
GET /api/plans?page=1&per_page=10&difficulty=intermediate&my_plans=true
Authorization: Bearer <token>
```

**响应** (200 OK):
```json
{
  "plans": [
    {
      "id": 1,
      "name": "8周增肌训练计划",
      "description": "适合中级健身者的全面增肌计划",
      "cover_image": "https://example.com/cover.jpg",
      "difficulty": "intermediate",
      "duration_weeks": 8,
      "days_per_week": 5,
      "goal": "增肌",
      "target_muscle_group": "full_body",
      "is_active": true,
      "is_template": false,
      "is_public": false,
      "usage_count": 5,
      "completion_rate": 60,
      "created_at": "2025-10-19T10:00:00",
      "updated_at": "2025-10-20T15:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3
  }
}
```

---

### 3. 获取计划详情

**端点**: `GET /api/plans/{id}`

**权限**: 需要登录（只能查看自己的计划或公开模板）

**请求示例**:
```http
GET /api/plans/1
Authorization: Bearer <token>
```

**响应** (200 OK):
```json
{
  "plan": {
    "id": 1,
    "name": "8周增肌训练计划",
    "description": "适合中级健身者的全面增肌计划",
    "difficulty": "intermediate",
    "duration_weeks": 8,
    "days_per_week": 5,
    "is_active": true,
    "plan_days": [
      {
        "id": 1,
        "day_number": 1,
        "day_name": "胸部+三头肌",
        "description": "胸部和三头肌强化训练",
        "warm_up": "动态拉伸5分钟",
        "cool_down": "静态拉伸10分钟",
        "estimated_duration": 60,
        "target_calories": 400,
        "rest_time": 90,
        "exercises": [
          {
            "id": 1,
            "name": "杠铃卧推",
            "description": "经典的胸部力量训练动作",
            "video_url": "https://example.com/videos/bench-press.mp4",
            "exercise_type": "力量",
            "muscle_group": "chest",
            "equipment": "杠铃",
            "order_number": 1,
            "sets": 4,
            "reps": 10,
            "weight": 60,
            "rest_time": 90,
            "difficulty": "intermediate",
            "calories_per_set": 50,
            "key_points": [...],
            "common_mistakes": [...]
          }
        ]
      }
    ],
    "creator": {
      "id": 1,
      "username": "fitness_coach",
      "nickname": "健身教练小王"
    }
  }
}
```

---

### 4. 更新训练计划

**端点**: `PUT /api/plans/{id}`

**权限**: 需要登录（只能修改自己的计划）

**请求体** (所有字段可选):
```json
{
  "name": "新的计划名称",
  "description": "更新的描述",
  "difficulty": "advanced",
  "is_active": true,
  "is_public": false,
  "plan_days": [...]
}
```

**响应** (200 OK):
```json
{
  "message": "更新成功",
  "plan": {
    "id": 1,
    "name": "新的计划名称",
    ...
  }
}
```

---

### 5. 删除训练计划

**端点**: `DELETE /api/plans/{id}`

**权限**: 需要登录（只能删除自己的计划）

**响应** (200 OK):
```json
{
  "message": "删除成功"
}
```

---

### 6. 开始执行计划

**端点**: `POST /api/plans/{id}/start`

**权限**: 需要登录

**功能说明**:
- 如果是模板计划，会自动复制一份
- 如果已有其他激活的计划，会自动取消激活
- 增加计划使用次数

**响应** (200 OK):
```json
{
  "message": "计划已激活",
  "plan": {
    "id": 2,
    "name": "8周增肌训练计划 (副本)",
    "is_active": true,
    ...
  }
}
```

---

### 7. 复制模板计划

**端点**: `POST /api/plans/{id}/copy`

**权限**: 需要登录

**功能说明**:
- 将公开的模板计划复制到自己账户
- 复制后的计划为非模板、非公开状态
- 可以自由编辑复制后的计划

**响应** (201 Created):
```json
{
  "message": "复制成功",
  "plan": {
    "id": 3,
    "name": "8周增肌训练计划 (副本)",
    "is_template": false,
    "is_active": false,
    ...
  }
}
```

---

### 8. 获取计划进度

**端点**: `GET /api/plans/{id}/progress`

**权限**: 需要登录（只能查看自己的计划进度）

**响应** (200 OK):
```json
{
  "plan_id": 1,
  "total_days": 40,
  "completed_days": 24,
  "completion_rate": 60,
  "duration_weeks": 8,
  "days_per_week": 5
}
```

---

## 🎯 使用场景

### 场景1: 创建自定义训练计划

```bash
# 1. 用户登录获取token
POST /api/auth/login

# 2. 创建计划
POST /api/plans
{
  "name": "我的减脂计划",
  "difficulty": "beginner",
  "duration_weeks": 4,
  "days_per_week": 3,
  "goal": "减脂",
  "plan_days": [...]
}

# 3. 激活计划
POST /api/plans/1/start
```

### 场景2: 使用模板计划

```bash
# 1. 浏览模板列表
GET /api/plans?templates=true

# 2. 查看模板详情
GET /api/plans/5

# 3. 复制模板
POST /api/plans/5/copy

# 4. 开始执行
POST /api/plans/10/start
```

### 场景3: 查看训练进度

```bash
# 1. 获取我的激活计划
GET /api/plans?is_active=true&my_plans=true

# 2. 查看计划进度
GET /api/plans/1/progress

# 3. 查看计划详情
GET /api/plans/1
```

---

## 🔧 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（需要登录） |
| 403 | 禁止访问（无权限） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

**错误响应格式**:
```json
{
  "error": "错误信息"
}
```

---

## 💡 最佳实践

### 1. 计划命名规范
- 使用清晰、描述性的名称
- 包含目标、难度、周期等关键信息
- 例如："8周中级增肌计划"、"4周初级减脂计划"

### 2. 训练日设置
- 合理安排训练日顺序
- 同一肌群至少间隔48小时
- 包含充分的热身和放松

### 3. 动作编排
- 大肌群动作优先
- 复合动作在前，孤立动作在后
- 合理设置组数、次数和休息时间

### 4. 进度跟踪
- 定期记录训练完成情况
- 根据进度调整训练强度
- 每4-8周评估并调整计划

---

## 📊 数据模型关系

```
TrainingPlan (训练计划)
  ├── PlanDay (训练日) [1对多]
  │     └── Exercise (动作) [1对多]
  ├── User (创建者) [多对1]
  └── WorkoutRecord (训练记录) [1对多]
```

---

## 🚀 下一步开发

- [ ] 训练记录API（记录训练完成情况）
- [ ] 训练统计API（分析训练数据）
- [ ] 计划分享功能
- [ ] 计划评论和点赞
- [ ] AI推荐训练计划
- [ ] 训练提醒功能

---

**文档版本**: v1.0  
**更新日期**: 2025-10-19  
**维护者**: Keep团队
