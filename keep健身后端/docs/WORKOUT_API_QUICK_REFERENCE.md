# 运动记录API速查表 🏋️

## 📋 接口清单

### 基础操作
| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/workouts` | 创建训练记录 |
| GET | `/api/workouts` | 获取训练列表 |
| GET | `/api/workouts/{id}` | 获取训练详情 |
| PUT | `/api/workouts/{id}` | 更新训练记录 |
| DELETE | `/api/workouts/{id}` | 删除训练记录 |
| POST | `/api/workouts/{id}/finish` | 完成训练 |

### 训练组操作
| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/workouts/{id}/sets` | 添加训练组 |
| PUT | `/api/sets/{id}` | 更新训练组 |
| DELETE | `/api/sets/{id}` | 删除训练组 |

### 查询功能
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/workouts/calendar` | 获取训练日历 |
| GET | `/api/workouts/records` | 获取个人最佳记录 |

### 统计功能
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/stats/overview` | 统计总览 |
| GET | `/api/stats/weekly` | 周统计 |
| GET | `/api/stats/monthly` | 月统计 |
| GET | `/api/stats/muscle-distribution` | 肌群分布 |
| GET | `/api/stats/workout-types` | 训练类型分布 |
| GET | `/api/stats/progress` | 进步趋势 |
| GET | `/api/stats/consistency` | 坚持度评分 |

---

## 🔥 快速使用

### 1. 创建训练记录

```bash
POST /api/workouts
Authorization: Bearer {token}

{
  "workout_date": "2024-01-20",
  "workout_type": "力量训练",
  "plan_id": 1,
  "exercises": [
    {
      "exercise_name": "深蹲",
      "muscle_group": "腿部",
      "sets": [
        {
          "set_number": 1,
          "set_type": "normal",
          "reps": 10,
          "weight": 80.0
        }
      ]
    }
  ]
}
```

### 2. 获取训练列表（带筛选）

```bash
GET /api/workouts?start_date=2024-01-01&end_date=2024-01-31&workout_type=力量训练
Authorization: Bearer {token}
```

### 3. 完成训练

```bash
POST /api/workouts/1/finish
Authorization: Bearer {token}

{
  "notes": "今天状态很好!"
}
```

### 4. 添加训练组

```bash
POST /api/workouts/1/sets
Authorization: Bearer {token}

{
  "exercise_id": 1,
  "set_number": 2,
  "set_type": "normal",
  "reps": 12,
  "weight": 85.0
}
```

### 5. 获取个人最佳记录

```bash
GET /api/workouts/records?exercise_name=深蹲
Authorization: Bearer {token}
```

### 6. 获取训练日历

```bash
GET /api/workouts/calendar?year=2024&month=1
Authorization: Bearer {token}
```

### 7. 获取统计总览

```bash
GET /api/stats/overview?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer {token}
```

### 8. 获取坚持度评分

```bash
GET /api/stats/consistency
Authorization: Bearer {token}
```

---

## 📊 数据模型

### 训练组类型（SetType）
- `normal`: 正常组
- `warmup`: 热身组
- `drop`: 递减组
- `super`: 超级组

### 训练类型（WorkoutType）
- `力量训练`: 力量/抗阻训练
- `有氧训练`: 跑步、游泳等
- `混合训练`: 组合训练

### 肌群类型（MuscleGroup）
胸部、背部、腿部、肩部、手臂、核心、全身

---

## ⚡ 高级功能

### 批量创建（性能优化）
系统自动使用批量插入优化,单次可创建包含多个动作和多个训练组的完整训练记录。

### 自动统计
完成训练时自动计算:
- 总组数
- 总次数
- 总重量
- 卡路里消耗

### 个人记录追踪
系统自动检测并标记个人最佳记录（PR）:
- 最大重量
- 最多次数
- 最高总量

### 进度跟踪
完成训练后自动更新关联训练计划的进度。

---

## 🎯 查询参数

### 训练列表查询
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)
- `workout_type`: 训练类型
- `plan_id`: 训练计划ID
- `is_completed`: 是否完成 (true/false)
- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 20)

### 日历查询
- `year`: 年份 (默认: 当前年)
- `month`: 月份 (默认: 当前月)

### 统计查询
- `start_date`: 开始日期
- `end_date`: 结束日期

### 进步趋势
- `exercise_name`: 动作名称 (可选)
- `period`: 统计周期 (week/month/year)

---

## 💡 最佳实践

1. **训练中实时记录**: 每完成一组立即调用添加训练组API
2. **训练结束时完成**: 调用完成训练API触发自动统计
3. **定期查看统计**: 使用统计API了解训练进展
4. **关注个人记录**: 追踪PR激励持续进步
5. **利用日历视图**: 可视化训练频率

---

## 🔒 认证说明

所有接口都需要JWT认证，请在请求头中添加:
```
Authorization: Bearer {your_jwt_token}
```

---

## 📝 响应格式

### 成功响应
```json
{
  "code": 0,
  "message": "操作成功",
  "data": { /* 返回数据 */ }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "数据验证失败",
  "errors": [ /* 错误详情 */ ]
}
```

---

**提示**: 更多详细文档请参考 `WORKOUT_API.md`
