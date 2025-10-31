# 训练计划API快速使用指南

## 📝 使用流程

### 步骤1: 用户注册和登录

```bash
# 1. 注册新用户
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fitness_user",
    "email": "user@example.com",
    "password": "Test123456"
  }'

# 2. 登录获取令牌
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "fitness_user",
    "password": "Test123456"
  }'

# 响应中获取 access_token
# 后续请求需要在 Header 中带上: Authorization: Bearer <access_token>
```

---

### 步骤2: 创建训练计划

```bash
curl -X POST http://localhost:5000/api/plans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "name": "4周减脂计划",
    "description": "适合初学者的有氧+力量结合训练",
    "difficulty": "beginner",
    "duration_weeks": 4,
    "days_per_week": 3,
    "goal": "减脂",
    "target_muscle_group": "full_body",
    "plan_days": [
      {
        "day_number": 1,
        "day_name": "全身有氧+核心",
        "description": "开合跳+卷腹组合",
        "estimated_duration": 30,
        "target_calories": 250,
        "exercises": [
          {
            "name": "开合跳",
            "exercise_type": "有氧",
            "muscle_group": "cardio",
            "order_number": 1,
            "sets": 3,
            "reps": 30,
            "rest_time": 30,
            "difficulty": "beginner",
            "calories_per_set": 40
          },
          {
            "name": "卷腹",
            "exercise_type": "力量",
            "muscle_group": "core",
            "order_number": 2,
            "sets": 3,
            "reps": 20,
            "rest_time": 30,
            "difficulty": "beginner",
            "calories_per_set": 30
          }
        ]
      }
    ]
  }'
```

---

### 步骤3: 查看我的计划

```bash
# 获取我的所有计划
curl -X GET "http://localhost:5000/api/plans?my_plans=true" \
  -H "Authorization: Bearer <your_access_token>"

# 按难度筛选
curl -X GET "http://localhost:5000/api/plans?difficulty=beginner&my_plans=true" \
  -H "Authorization: Bearer <your_access_token>"

# 搜索计划
curl -X GET "http://localhost:5000/api/plans?keyword=减脂" \
  -H "Authorization: Bearer <your_access_token>"
```

---

### 步骤4: 查看计划详情

```bash
curl -X GET http://localhost:5000/api/plans/1 \
  -H "Authorization: Bearer <your_access_token>"
```

---

### 步骤5: 开始执行计划

```bash
curl -X POST http://localhost:5000/api/plans/1/start \
  -H "Authorization: Bearer <your_access_token>"

# 这会将计划标记为"激活"状态
# 同时自动取消其他已激活的计划
```

---

### 步骤6: 查看训练进度

```bash
curl -X GET http://localhost:5000/api/plans/1/progress \
  -H "Authorization: Bearer <your_access_token>"

# 返回完成率、已完成天数等信息
```

---

### 步骤7: 更新计划

```bash
curl -X PUT http://localhost:5000/api/plans/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "name": "4周减脂计划 (加强版)",
    "difficulty": "intermediate",
    "description": "增加了训练强度"
  }'
```

---

## 🎯 常见使用场景

### 场景1: 教练创建模板计划

```json
POST /api/plans
{
  "name": "专业增肌模板",
  "is_template": true,
  "is_public": true,
  "difficulty": "advanced",
  "duration_weeks": 12,
  "days_per_week": 6,
  "plan_days": [...]
}
```

### 场景2: 用户浏览并复制模板

```bash
# 1. 浏览公开模板
GET /api/plans?templates=true

# 2. 查看模板详情
GET /api/plans/5

# 3. 复制模板到自己账户
POST /api/plans/5/copy

# 4. 开始执行复制后的计划
POST /api/plans/10/start
```

### 场景3: 用户定制个人计划

```bash
# 1. 创建基础计划
POST /api/plans
{
  "name": "我的个性化计划",
  "difficulty": "intermediate",
  "duration_weeks": 8,
  "days_per_week": 4,
  "plan_days": [
    {
      "day_number": 1,
      "day_name": "周一: 胸+三头",
      "exercises": [...]
    },
    {
      "day_number": 2,
      "day_name": "周三: 背+二头",
      "exercises": [...]
    }
  ]
}

# 2. 根据实际情况调整
PUT /api/plans/1
{
  "plan_days": [...] // 修改训练内容
}

# 3. 激活并开始训练
POST /api/plans/1/start
```

---

## 💡 实用技巧

### 1. 分页获取大量计划

```bash
# 第1页，每页20条
GET /api/plans?page=1&per_page=20

# 第2页
GET /api/plans?page=2&per_page=20
```

### 2. 多条件组合筛选

```bash
# 中级难度 + 全身训练 + 我的计划
GET /api/plans?difficulty=intermediate&target_muscle_group=full_body&my_plans=true

# 高级难度 + 增肌目标 + 按使用次数排序
GET /api/plans?difficulty=advanced&goal=增肌&order_by=usage_count
```

### 3. 管理激活状态

```bash
# 查看当前激活的计划
GET /api/plans?is_active=true&my_plans=true

# 激活新计划会自动取消旧计划
POST /api/plans/2/start
```

### 4. 计划进度追踪

```bash
# 定期检查进度
GET /api/plans/1/progress

# 响应示例
{
  "plan_id": 1,
  "total_days": 12,
  "completed_days": 7,
  "completion_rate": 58,  // 58%
  "duration_weeks": 4,
  "days_per_week": 3
}
```

---

## 📊 数据格式说明

### 训练计划完整结构

```json
{
  "name": "计划名称",
  "description": "计划描述",
  "cover_image": "封面图URL",
  "difficulty": "beginner|intermediate|advanced",
  "duration_weeks": 8,
  "days_per_week": 5,
  "goal": "减脂|增肌|塑形|体能",
  "target_muscle_group": "chest|back|shoulders|arms|legs|core|cardio|full_body",
  "is_active": false,
  "is_template": false,
  "is_public": false,
  "plan_days": [
    {
      "day_number": 1,
      "day_name": "训练日名称",
      "description": "当日训练描述",
      "warm_up": "热身内容",
      "cool_down": "放松内容",
      "estimated_duration": 60,
      "target_calories": 400,
      "rest_time": 90,
      "exercises": [
        {
          "name": "动作名称",
          "description": "动作描述",
          "video_url": "演示视频URL",
          "image_url": "演示图片URL",
          "exercise_type": "力量|有氧|拉伸",
          "muscle_group": "目标肌群",
          "equipment": "所需器械",
          "order_number": 1,
          "sets": 4,
          "reps": 10,
          "duration": 30,
          "weight": 50,
          "rest_time": 90,
          "difficulty": "难度等级",
          "calories_per_set": 50,
          "key_points": ["要点1", "要点2"],
          "common_mistakes": ["错误1", "错误2"]
        }
      ]
    }
  ]
}
```

---

## ⚠️ 注意事项

### 1. 认证令牌
- 所有API请求都需要携带JWT令牌
- 令牌有效期24小时
- 过期后需要使用refresh_token刷新

### 2. 权限控制
- 只能修改/删除自己创建的计划
- 公开模板可以被所有人查看和复制
- 激活状态每个用户同时只能有一个

### 3. 数据验证
- 必填字段: name, difficulty, duration_weeks, days_per_week
- 动作必填字段: name, exercise_type, muscle_group, order_number
- 枚举字段必须使用规定的值

### 4. 性能建议
- 使用分页避免一次获取过多数据
- 利用筛选条件减少不必要的查询
- 缓存常用的模板计划详情

---

## 🐛 常见问题

### Q1: 创建计划返回400错误
**原因**: 缺少必填字段或字段值不合法  
**解决**: 检查difficulty、target_muscle_group等枚举字段是否使用了正确的值

### Q2: 获取计划详情返回403
**原因**: 尝试访问其他用户的私有计划  
**解决**: 只能访问自己的计划或公开的模板

### Q3: 开始执行计划后找不到原计划
**原因**: 如果是模板计划，start会创建一个副本  
**解决**: 查看响应中返回的新plan_id

### Q4: 删除计划后还能查到
**原因**: 使用的是软删除  
**解决**: 软删除的数据在API中不会返回，但数据库中仍存在

---

## 📚 相关文档

- [完整API文档](TRAINING_API.md)
- [认证系统文档](AUTH_SYSTEM.md)
- [数据库设计文档](DATABASE_DESIGN.md)

---

**文档版本**: v1.0  
**更新日期**: 2025-10-19
