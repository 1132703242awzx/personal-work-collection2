# 数据分析API快速参考

## API端点速查表

| 端点 | 方法 | 功能 | 响应时间 | 缓存策略 |
|------|------|------|----------|----------|
| `/api/analytics/frequency` | GET | 训练频率统计 | ~100ms | 10分钟 |
| `/api/analytics/duration` | GET | 训练时长统计 | ~100ms | 10分钟 |
| `/api/analytics/strength-progress` | GET | 力量进步曲线 | ~200ms | 10分钟 |
| `/api/analytics/body-trends` | GET | 身体数据趋势 | ~150ms | 10分钟 |
| `/api/analytics/calories` | GET | 卡路里统计 | ~100ms | 10分钟 |
| `/api/analytics/volume` | GET | 训练容量统计 | ~100ms | 10分钟 |
| `/api/analytics/achievements` | GET | 成就汇总 | ~50ms | 5分钟 |
| `/api/analytics/dashboard` | GET | 综合仪表盘 | ~300ms | 1分钟 |
| `/api/analytics/leaderboard` | GET | 排行榜 | ~200ms | 5分钟 |
| `/api/analytics/comparison` | POST | 用户对比 | ~150ms | 无 |
| `/api/analytics/overview` | GET | 数据概览 | ~50ms | 1分钟 |

---

## 通用查询参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `time_range` | string | week/month/quarter/year/all | `time_range=month` |
| `start_date` | date | YYYY-MM-DD格式 | `start_date=2024-01-01` |
| `end_date` | date | YYYY-MM-DD格式 | `end_date=2024-01-31` |
| `include_chart` | boolean | 是否包含图表 | `include_chart=true` |

---

## 常用代码示例

### Python (requests)

```python
import requests

# 1. 获取训练频率
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:5000/api/analytics/frequency",
    params={"time_range": "month", "include_chart": True},
    headers=headers
)
data = response.json()

# 2. 获取仪表盘
response = requests.get(
    "http://localhost:5000/api/analytics/dashboard",
    params={"time_range": "week"},
    headers=headers
)
dashboard = response.json()

# 3. 用户对比
response = requests.post(
    "http://localhost:5000/api/analytics/comparison",
    json={
        "user_ids": [1, 2, 3],
        "metrics": ["workouts", "duration", "calories"],
        "time_range": "month"
    },
    headers=headers
)
comparison = response.json()
```

### JavaScript (axios)

```javascript
// 1. 获取力量进步
const response = await axios.get('/api/analytics/strength-progress', {
    params: {
        exercise_id: 1,
        time_range: 'all',
        include_chart: true
    },
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

// 2. 获取排行榜
const leaderboard = await axios.get('/api/analytics/leaderboard', {
    params: {
        metric: 'workouts',
        time_range: 'month',
        limit: 20,
        scope: 'global'
    },
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

// 3. 获取身体数据趋势
const trends = await axios.get('/api/analytics/body-trends', {
    params: {
        metrics: 'weight,body_fat',
        time_range: 'month'
    },
    headers: {
        'Authorization': `Bearer ${token}`
    }
});
```

### cURL

```bash
# 1. 训练频率统计
curl -X GET "http://localhost:5000/api/analytics/frequency?time_range=month" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 2. 排行榜
curl -X GET "http://localhost:5000/api/analytics/leaderboard?metric=workouts&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. 用户对比
curl -X POST "http://localhost:5000/api/analytics/comparison" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_ids": [1, 2, 3],
    "metrics": ["workouts", "duration"],
    "time_range": "month"
  }'
```

---

## 响应数据结构

### 成功响应
```json
{
    "code": 200,
    "data": {
        // 具体数据
    }
}
```

### 错误响应
```json
{
    "code": 400,
    "error": "错误描述",
    "message": "详细信息"
}
```

### 图表数据结构
```json
{
    "chart_type": "line",
    "title": "标题",
    "data": [
        {
            "date": "2024-01-01",
            "value": 100,
            "label": "标签"
        }
    ],
    "x_axis_label": "X轴标签",
    "y_axis_label": "Y轴标签",
    "unit": "单位"
}
```

---

## 排行榜指标

| 指标 | metric值 | 说明 |
|------|----------|------|
| 训练次数 | `workouts` | 训练记录总数 |
| 训练时长 | `duration` | 总时长(秒) |
| 卡路里 | `calories` | 总消耗卡路里 |
| 训练容量 | `volume` | 重量×次数 |
| 成就数 | `achievements` | 已解锁成就数 |

---

## 排行榜范围

| 范围 | scope值 | 说明 |
|------|---------|------|
| 全局 | `global` | 所有用户 |
| 好友 | `friends` | 互相关注的用户 |
| 关注 | `following` | 我关注的用户 |

---

## 图表类型

| 类型 | chart_type值 | 适用场景 |
|------|--------------|----------|
| 折线图 | `line` | 趋势分析(力量进步、体重变化) |
| 柱状图 | `bar` | 对比分析(训练频率、用户对比) |
| 饼图 | `pie` | 占比分析(训练容量分布) |
| 面积图 | `area` | 累积趋势(时长、卡路里) |
| 散点图 | `scatter` | 分布分析(未使用) |

---

## 时间范围对应天数

| time_range | 天数 | 说明 |
|------------|------|------|
| `week` | 7天 | 最近一周 |
| `month` | 30天 | 最近一月 |
| `quarter` | 90天 | 最近一季度 |
| `year` | 365天 | 最近一年 |
| `all` | 全部 | 所有历史数据 |

---

## 常见使用场景

### 场景1: 用户首页概览
```python
# 获取概览数据
overview = requests.get(
    f"{base_url}/api/analytics/overview",
    headers=headers
).json()

# 显示:
# - 本周训练次数: overview['data']['this_week']['workouts']
# - 连续天数: overview['data']['this_week']['streak']
# - 本月频率: overview['data']['this_month']['frequency_rate']
```

### 场景2: 训练统计页面
```python
# 获取完整仪表盘
dashboard = requests.get(
    f"{base_url}/api/analytics/dashboard",
    params={"time_range": "month", "include_charts": True},
    headers=headers
).json()

# 渲染各项统计图表
for chart in dashboard['data']['charts']:
    render_chart(chart['chart_type'], chart['data'])
```

### 场景3: 排行榜页面
```python
# 获取不同指标排行
metrics = ['workouts', 'duration', 'calories', 'volume', 'achievements']

for metric in metrics:
    leaderboard = requests.get(
        f"{base_url}/api/analytics/leaderboard",
        params={
            "metric": metric,
            "time_range": "month",
            "limit": 20,
            "scope": "global"
        },
        headers=headers
    ).json()
    
    display_leaderboard(metric, leaderboard['data']['rankings'])
```

### 场景4: 力量进步追踪
```python
# 获取所有运动的进步数据
progress = requests.get(
    f"{base_url}/api/analytics/strength-progress",
    params={"time_range": "all", "include_chart": True},
    headers=headers
).json()

# 为每个运动绘制进步曲线
for exercise in progress['data']:
    print(f"{exercise['exercise_name']}: {exercise['progress']}% 进步")
    render_progress_chart(exercise['chart'])
```

### 场景5: 好友对比
```python
# 对比当前用户和好友
comparison = requests.post(
    f"{base_url}/api/analytics/comparison",
    json={
        "user_ids": [current_user_id, friend_id],
        "metrics": ["workouts", "duration", "calories", "volume"],
        "time_range": "month"
    },
    headers=headers
).json()

# 渲染对比图表
for chart in comparison['data']['charts']:
    render_comparison_chart(chart)
```

---

## 性能优化建议

1. **首屏加载**: 先调用 `/overview` 获取概览,再按需加载详细数据
2. **图表渲染**: 使用 `include_chart=false` 减少数据量,前端自行绘制
3. **分页加载**: 排行榜使用合理的 `limit` 值(10-20)
4. **缓存策略**: 客户端缓存概览数据1分钟,统计数据5-10分钟
5. **懒加载**: 仪表盘图表按需展开加载

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权(token无效) |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

---

## 联系方式

- **API文档**: [ANALYTICS_API.md](./ANALYTICS_API.md)
- **测试工具**: [test_analytics.py](./tests/test_analytics.py)
- **更新日志**: 查看Git提交记录

**最后更新**: 2024-01-01
