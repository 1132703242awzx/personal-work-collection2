# Keep健身 - 数据统计分析API文档

## 目录
- [概述](#概述)
- [核心功能](#核心功能)
- [训练频率统计](#训练频率统计)
- [训练时长统计](#训练时长统计)
- [力量进步分析](#力量进步分析)
- [身体数据趋势](#身体数据趋势)
- [卡路里统计](#卡路里统计)
- [训练容量统计](#训练容量统计)
- [成就系统](#成就系统)
- [综合仪表盘](#综合仪表盘)
- [排行榜](#排行榜)
- [用户对比](#用户对比)
- [数据概览](#数据概览)

## 概述

数据统计分析系统提供全面的用户数据分析功能,支持:
- 多维度数据统计
- 趋势分析和图表生成
- 排行榜系统
- 用户对比分析
- 综合仪表盘

**基础URL**: `http://localhost:5000/api/analytics`

**认证方式**: Bearer Token

---

## 核心功能

### 数据分析维度

1. **训练频率和时长**
   - 训练次数统计
   - 时长分布分析
   - 连续训练天数
   - 训练频率趋势

2. **力量进步曲线**
   - 按运动统计最大重量
   - 进步率计算
   - 训练容量分析
   - 历史数据趋势

3. **身体数据变化**
   - 体重变化趋势
   - 体脂率变化
   - 身体围度变化
   - 对比分析

4. **卡路里和容量**
   - 卡路里消耗统计
   - 训练容量计算
   - 肌群分布分析
   - 目标完成度

5. **成就系统**
   - 成就解锁统计
   - 成就点数计算
   - 分类和稀有度分析
   - 最近解锁记录

### 时间范围

所有统计接口支持以下时间范围:
- `week` - 最近7天
- `month` - 最近30天
- `quarter` - 最近90天
- `year` - 最近365天
- `all` - 全部时间

也可以通过 `start_date` 和 `end_date` 自定义日期范围。

### 图表类型

支持多种图表类型:
- `line` - 折线图 (趋势分析)
- `bar` - 柱状图 (对比分析)
- `pie` - 饼图 (占比分析)
- `area` - 面积图 (累积趋势)
- `scatter` - 散点图 (分布分析)

---

## 训练频率统计

### 获取训练频率统计
**GET** `/api/analytics/frequency`

获取用户训练频率统计数据。

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| time_range | string | 否 | 时间范围(默认: month) |
| start_date | date | 否 | 开始日期(YYYY-MM-DD) |
| end_date | date | 否 | 结束日期(YYYY-MM-DD) |
| include_chart | boolean | 否 | 是否包含图表(默认: true) |

**示例请求**:
```http
GET /api/analytics/frequency?time_range=month&include_chart=true
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "total_workouts": 24,
        "total_days": 30,
        "average_per_week": 5.6,
        "max_streak": 7,
        "current_streak": 3,
        "workout_days": 24,
        "rest_days": 6,
        "frequency_rate": 80.0,
        "chart": {
            "chart_type": "bar",
            "title": "训练频率趋势",
            "data": [
                {
                    "date": "2024-W01",
                    "value": 5,
                    "label": "第1周"
                },
                {
                    "date": "2024-W02",
                    "value": 6,
                    "label": "第2周"
                }
            ],
            "x_axis_label": "周",
            "y_axis_label": "训练次数",
            "unit": "次"
        }
    }
}
```

**字段说明**:
- `total_workouts`: 总训练次数
- `average_per_week`: 周平均训练次数
- `max_streak`: 最长连续训练天数
- `current_streak`: 当前连续训练天数
- `workout_days`: 训练天数
- `rest_days`: 休息天数
- `frequency_rate`: 训练频率百分比

---

## 训练时长统计

### 获取训练时长统计
**GET** `/api/analytics/duration`

获取用户训练时长统计和分布。

**查询参数**: 同训练频率

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "total_duration": 86400,
        "total_duration_formatted": "24小时0分钟",
        "average_duration": 3600,
        "average_duration_formatted": "60分钟",
        "longest_workout": 5400,
        "shortest_workout": 1800,
        "duration_distribution": {
            "0-30分钟": 5,
            "30-60分钟": 15,
            "60-90分钟": 8,
            "90分钟以上": 2
        },
        "chart": {
            "chart_type": "area",
            "title": "训练时长趋势",
            "data": [
                {
                    "date": "2024-01-01",
                    "value": 60,
                    "label": "2024-01-01"
                }
            ],
            "x_axis_label": "日期",
            "y_axis_label": "时长",
            "unit": "分钟"
        }
    }
}
```

**字段说明**:
- `total_duration`: 总时长(秒)
- `average_duration`: 平均时长(秒)
- `longest_workout`: 最长单次训练(秒)
- `shortest_workout`: 最短单次训练(秒)
- `duration_distribution`: 时长分布统计

---

## 力量进步分析

### 获取力量进步曲线
**GET** `/api/analytics/strength-progress`

分析力量训练进步情况。

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| exercise_id | integer | 否 | 运动ID(不传则返回所有) |
| time_range | string | 否 | 时间范围(默认: all) |
| start_date | date | 否 | 开始日期 |
| end_date | date | 否 | 结束日期 |
| include_chart | boolean | 否 | 是否包含图表 |

**示例请求**:
```http
GET /api/analytics/strength-progress?exercise_id=1&time_range=all
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
    "code": 200,
    "data": [
        {
            "exercise_id": 1,
            "exercise_name": "深蹲",
            "start_weight": 60.0,
            "current_weight": 85.0,
            "max_weight": 90.0,
            "progress": 50.0,
            "total_volume": 45000.0,
            "records_count": 120,
            "chart": {
                "chart_type": "line",
                "title": "深蹲 - 力量进步",
                "data": [
                    {
                        "date": "2024-01-01",
                        "value": 60.0,
                        "label": "60kg"
                    },
                    {
                        "date": "2024-01-15",
                        "value": 70.0,
                        "label": "70kg"
                    },
                    {
                        "date": "2024-02-01",
                        "value": 80.0,
                        "label": "80kg"
                    }
                ],
                "x_axis_label": "日期",
                "y_axis_label": "重量",
                "unit": "kg"
            }
        }
    ]
}
```

**字段说明**:
- `start_weight`: 起始重量
- `current_weight`: 当前平均重量
- `max_weight`: 最大重量
- `progress`: 进步幅度(百分比)
- `total_volume`: 总训练容量(重量×次数)
- `records_count`: 记录总数

---

## 身体数据趋势

### 获取身体数据变化趋势
**GET** `/api/analytics/body-trends`

分析体重、体脂等身体数据变化。

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| metrics | string | 否 | 指标列表,逗号分隔(默认: weight) |
| time_range | string | 否 | 时间范围 |
| start_date | date | 否 | 开始日期 |
| end_date | date | 否 | 结束日期 |
| include_chart | boolean | 否 | 是否包含图表 |

**示例请求**:
```http
GET /api/analytics/body-trends?metrics=weight,body_fat&time_range=month
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
    "code": 200,
    "data": [
        {
            "metric": "体重",
            "start_value": 75.5,
            "current_value": 73.2,
            "change": -2.3,
            "change_rate": -3.05,
            "trend": "down",
            "records_count": 30,
            "chart": {
                "chart_type": "line",
                "title": "体重变化趋势",
                "data": [
                    {
                        "date": "2024-01-01",
                        "value": 75.5,
                        "label": "75.5kg"
                    },
                    {
                        "date": "2024-01-15",
                        "value": 74.3,
                        "label": "74.3kg"
                    },
                    {
                        "date": "2024-01-30",
                        "value": 73.2,
                        "label": "73.2kg"
                    }
                ],
                "x_axis_label": "日期",
                "y_axis_label": "体重",
                "unit": "kg"
            }
        }
    ]
}
```

**字段说明**:
- `metric`: 指标名称
- `start_value`: 起始值
- `current_value`: 当前值
- `change`: 变化量
- `change_rate`: 变化率(百分比)
- `trend`: 趋势 (up/down/stable)

---

## 卡路里统计

### 获取卡路里统计
**GET** `/api/analytics/calories`

统计卡路里消耗情况。

**查询参数**: 同训练频率

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "total_calories": 15000.0,
        "average_per_workout": 625.0,
        "max_calories": 850.0,
        "calories_goal": null,
        "goal_completion": null,
        "chart": {
            "chart_type": "area",
            "title": "卡路里消耗趋势",
            "data": [
                {
                    "date": "2024-01-01",
                    "value": 600.0,
                    "label": "600卡"
                }
            ],
            "x_axis_label": "日期",
            "y_axis_label": "卡路里",
            "unit": "千卡"
        }
    }
}
```

---

## 训练容量统计

### 获取训练容量统计
**GET** `/api/analytics/volume`

统计训练容量(重量×次数)。

**查询参数**: 同训练频率

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "total_volume": 125000.0,
        "average_per_workout": 5208.3,
        "by_muscle_group": {
            "胸部": 35000.0,
            "腿部": 50000.0,
            "背部": 30000.0,
            "肩部": 10000.0
        },
        "chart": {
            "chart_type": "pie",
            "title": "训练容量分布",
            "data": [
                {
                    "date": "胸部",
                    "value": 35000.0,
                    "label": "35000kg"
                },
                {
                    "date": "腿部",
                    "value": 50000.0,
                    "label": "50000kg"
                }
            ],
            "unit": "kg"
        }
    }
}
```

---

## 成就系统

### 获取成就汇总
**GET** `/api/analytics/achievements`

获取用户成就统计。

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "total_achievements": 50,
        "unlocked_count": 23,
        "unlock_rate": 46.0,
        "total_points": 5000,
        "earned_points": 2300,
        "by_category": {
            "running": 8,
            "strength": 10,
            "yoga": 5
        },
        "by_rarity": {
            "common": 15,
            "rare": 6,
            "epic": 2
        },
        "recent_unlocked": [
            {
                "id": 1,
                "name": "跑步新手",
                "description": "完成首次跑步",
                "icon": "running.png",
                "category": "running",
                "rarity": "common",
                "points": 10,
                "is_unlocked": true,
                "unlocked_at": "2024-01-01T10:00:00",
                "progress": 100.0
            }
        ]
    }
}
```

---

## 综合仪表盘

### 获取仪表盘数据
**GET** `/api/analytics/dashboard`

获取综合统计仪表盘。

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| time_range | string | 否 | 时间范围(默认: week) |
| include_charts | boolean | 否 | 是否包含图表(默认: true) |

**示例请求**:
```http
GET /api/analytics/dashboard?time_range=week&include_charts=true
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "overview": {
            "time_range": "week",
            "workout_count": 5,
            "last_updated": "2024-01-01T12:00:00"
        },
        "frequency": {
            "total_workouts": 5,
            "average_per_week": 5.0,
            "current_streak": 3,
            "frequency_rate": 71.4
        },
        "duration": {
            "total_duration": 18000,
            "total_duration_formatted": "5小时0分钟",
            "average_duration": 3600
        },
        "calories": {
            "total_calories": 3000.0,
            "average_per_workout": 600.0
        },
        "strength_summary": {
            "exercises_tracked": 8,
            "total_volume": 25000.0,
            "average_progress": 15.5
        },
        "body_data_summary": {
            "metrics_tracked": 1,
            "trends": [
                {
                    "metric": "体重",
                    "change": -0.5,
                    "trend": "down"
                }
            ]
        },
        "achievements": {
            "total_achievements": 50,
            "unlocked_count": 23,
            "points": 2300
        },
        "charts": [...]
    }
}
```

**用途**: 首页仪表盘、周报/月报生成

---

## 排行榜

### 获取排行榜
**GET** `/api/analytics/leaderboard`

获取各项指标排行榜。

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| metric | string | 否 | 排名指标(默认: workouts) |
| time_range | string | 否 | 时间范围(默认: month) |
| limit | integer | 否 | 返回数量(默认: 10, 最大: 100) |
| scope | string | 否 | 范围(global/friends/following) |

**支持的排名指标**:
- `workouts` - 训练次数
- `duration` - 训练时长
- `calories` - 卡路里消耗
- `volume` - 训练容量
- `achievements` - 成就数量

**示例请求**:
```http
GET /api/analytics/leaderboard?metric=workouts&time_range=month&limit=10&scope=global
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "metric": "workouts",
        "time_range": "month",
        "total_participants": 1000,
        "rankings": [
            {
                "rank": 1,
                "user_id": 123,
                "username": "fitness_king",
                "nickname": "健身王",
                "avatar": "avatar.jpg",
                "value": 30.0,
                "formatted_value": "30次",
                "badge": "🥇",
                "is_current_user": false
            },
            {
                "rank": 2,
                "user_id": 456,
                "username": "strong_man",
                "nickname": "力量猛男",
                "avatar": "avatar2.jpg",
                "value": 28.0,
                "formatted_value": "28次",
                "badge": "🥈",
                "is_current_user": false
            }
        ],
        "current_user_rank": {
            "rank": 15,
            "user_id": 789,
            "username": "current_user",
            "nickname": "我",
            "value": 20.0,
            "formatted_value": "20次",
            "is_current_user": true
        },
        "last_updated": "2024-01-01T12:00:00"
    }
}
```

---

## 用户对比

### 用户对比分析
**POST** `/api/analytics/comparison`

对比多个用户的数据。

**请求体**:
```json
{
    "user_ids": [1, 2, 3],
    "metrics": ["workouts", "duration", "calories"],
    "time_range": "month"
}
```

**参数说明**:
- `user_ids`: 对比用户IDs (2-5个)
- `metrics`: 对比指标列表
- `time_range`: 时间范围

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "time_range": "month",
        "metrics": ["workouts", "duration", "calories"],
        "users": [
            {
                "user_id": 1,
                "username": "user1",
                "nickname": "用户1",
                "metrics": {
                    "workouts": 24.0,
                    "duration": 1440.0,
                    "calories": 14400.0
                }
            },
            {
                "user_id": 2,
                "username": "user2",
                "nickname": "用户2",
                "metrics": {
                    "workouts": 20.0,
                    "duration": 1200.0,
                    "calories": 12000.0
                }
            }
        ],
        "charts": [
            {
                "chart_type": "bar",
                "title": "训练次数对比",
                "data": [
                    {
                        "date": "user1",
                        "value": 24.0,
                        "label": "用户1"
                    },
                    {
                        "date": "user2",
                        "value": 20.0,
                        "label": "用户2"
                    }
                ],
                "x_axis_label": "用户",
                "y_axis_label": "训练次数",
                "unit": ""
            }
        ]
    }
}
```

---

## 数据概览

### 获取数据概览
**GET** `/api/analytics/overview`

快速获取关键指标汇总。

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "this_week": {
            "workouts": 5,
            "duration": 18000,
            "calories": 3000.0,
            "streak": 3
        },
        "this_month": {
            "workouts": 24,
            "duration": 86400,
            "calories": 15000.0,
            "frequency_rate": 80.0
        },
        "achievements": {
            "total": 50,
            "unlocked": 23,
            "points": 2300
        }
    }
}
```

**用途**: APP首页概览、快速查看

---

## 技术实现

### 数据聚合查询

使用SQLAlchemy聚合函数:
```python
# 训练次数统计
workout_count = db.query(func.count(WorkoutRecord.id)).filter(
    WorkoutRecord.user_id == user_id,
    WorkoutRecord.status == 'completed'
).scalar()

# 训练容量计算
total_volume = db.query(
    func.sum(SetRecord.weight * SetRecord.reps)
).join(...).filter(...).scalar()
```

### 图表数据生成

返回标准化图表数据结构:
```json
{
    "chart_type": "line",
    "title": "标题",
    "data": [
        {"date": "2024-01-01", "value": 100, "label": "标签"}
    ],
    "x_axis_label": "X轴",
    "y_axis_label": "Y轴",
    "unit": "单位"
}
```

### 缓存优化策略

1. **Redis缓存**:
   - 排行榜数据缓存(5分钟)
   - 仪表盘数据缓存(1分钟)
   - 统计数据缓存(10分钟)

2. **数据库优化**:
   - 使用索引加速查询
   - 批量预加载关联数据
   - 分页查询大数据集

3. **计算优化**:
   - 增量计算(只计算新数据)
   - 异步后台任务
   - 定时预计算

### 定时统计任务

使用APScheduler定时任务:
```python
# 每天凌晨更新排行榜
scheduler.add_job(
    update_leaderboard,
    'cron',
    hour=0,
    minute=0
)

# 每小时更新成就
scheduler.add_job(
    check_achievements,
    'interval',
    hours=1
)
```

---

## 使用场景

### 1. 用户首页
- 调用 `/overview` 获取概览
- 显示本周/本月关键指标
- 连续训练天数提醒

### 2. 统计页面
- 调用 `/dashboard` 获取完整仪表盘
- 展示各项统计图表
- 趋势分析可视化

### 3. 排行榜页面
- 调用 `/leaderboard` 获取排名
- 切换不同指标排行
- 查看好友排名

### 4. 个人进步页
- 调用 `/strength-progress` 查看力量进步
- 调用 `/body-trends` 查看身体变化
- 生成进步报告

### 5. 好友对比
- 调用 `/comparison` 对比数据
- 生成对比图表
- 激励竞争

---

## 最佳实践

### 1. 性能优化
- 首次加载不包含图表数据
- 按需加载详细图表
- 使用分页查询

### 2. 用户体验
- 提供多种时间范围选择
- 支持自定义日期区间
- 图表交互式展示

### 3. 数据可靠性
- 定时备份统计数据
- 异常数据过滤
- 数据一致性校验

---

**更新时间**: 2024-01-01  
**版本**: v1.0  
**API数量**: 12个核心接口
