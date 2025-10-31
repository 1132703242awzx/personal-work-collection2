# 数据统计分析系统使用指南

## 📊 系统概述

数据统计分析系统是Keep健身后端的核心功能模块,提供全面的用户数据分析、趋势追踪、排行榜和数据可视化功能。

### 核心特性

✅ **多维度统计分析**
- 训练频率和时长统计
- 力量进步曲线追踪
- 身体数据变化趋势
- 卡路里和训练容量统计
- 成就系统汇总

✅ **数据可视化**
- 5种图表类型(折线图、柱状图、饼图、面积图、散点图)
- 图表数据自动生成
- 前端灵活渲染

✅ **社交竞争功能**
- 多维度排行榜系统
- 好友/关注用户排名
- 多用户对比分析

✅ **性能优化**
- 高效的数据聚合查询
- 灵活的时间范围支持
- 可配置缓存策略

---

## 🚀 快速开始

### 1. 安装依赖

系统已集成到现有后端,无需额外安装。

### 2. 测试API

```bash
# 交互式测试
python test_analytics.py

# 运行所有测试
python test_analytics.py --all YOUR_TOKEN
```

### 3. 查看文档

- **完整API文档**: [ANALYTICS_API.md](./ANALYTICS_API.md)
- **快速参考**: [ANALYTICS_QUICK_REFERENCE.md](./ANALYTICS_QUICK_REFERENCE.md)

---

## 📝 API端点总览

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/analytics/overview` | GET | 数据概览 |
| `/api/analytics/frequency` | GET | 训练频率统计 |
| `/api/analytics/duration` | GET | 训练时长统计 |
| `/api/analytics/strength-progress` | GET | 力量进步分析 |
| `/api/analytics/body-trends` | GET | 身体数据趋势 |
| `/api/analytics/calories` | GET | 卡路里统计 |
| `/api/analytics/volume` | GET | 训练容量统计 |
| `/api/analytics/achievements` | GET | 成就汇总 |
| `/api/analytics/dashboard` | GET | 综合仪表盘 |
| `/api/analytics/leaderboard` | GET | 排行榜 |
| `/api/analytics/comparison` | POST | 用户对比 |

---

## 💡 使用示例

### 示例1: 获取本周训练概览

```python
import requests

headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:5000/api/analytics/overview",
    headers=headers
)

data = response.json()['data']
print(f"本周训练: {data['this_week']['workouts']}次")
print(f"连续天数: {data['this_week']['streak']}天")
```

### 示例2: 获取力量进步曲线

```python
response = requests.get(
    "http://localhost:5000/api/analytics/strength-progress",
    params={
        "exercise_id": 1,  # 深蹲
        "time_range": "all",
        "include_chart": True
    },
    headers=headers
)

progress = response.json()['data'][0]
print(f"{progress['exercise_name']}")
print(f"起始重量: {progress['start_weight']}kg")
print(f"当前重量: {progress['current_weight']}kg")
print(f"进步幅度: {progress['progress']}%")

# 渲染图表
chart = progress['chart']
render_line_chart(chart['data'])
```

### 示例3: 查看排行榜

```python
response = requests.get(
    "http://localhost:5000/api/analytics/leaderboard",
    params={
        "metric": "workouts",
        "time_range": "month",
        "limit": 10,
        "scope": "global"
    },
    headers=headers
)

leaderboard = response.json()['data']
for entry in leaderboard['rankings']:
    print(f"#{entry['rank']} {entry['badge']} {entry['nickname']}: {entry['formatted_value']}")
```

### 示例4: 对比用户数据

```python
response = requests.post(
    "http://localhost:5000/api/analytics/comparison",
    json={
        "user_ids": [1, 2, 3],
        "metrics": ["workouts", "duration", "calories"],
        "time_range": "month"
    },
    headers=headers
)

comparison = response.json()['data']
for user in comparison['users']:
    print(f"{user['nickname']}:")
    for metric, value in user['metrics'].items():
        print(f"  {metric}: {value}")
```

---

## 🎨 前端集成指南

### 步骤1: 首页概览

```javascript
// 获取概览数据
const overview = await axios.get('/api/analytics/overview', {
    headers: { 'Authorization': `Bearer ${token}` }
});

// 渲染卡片
renderCard('本周训练', overview.data.this_week.workouts + '次');
renderCard('连续天数', overview.data.this_week.streak + '天');
renderCard('本月频率', overview.data.this_month.frequency_rate + '%');
```

### 步骤2: 统计页面

```javascript
// 获取仪表盘
const dashboard = await axios.get('/api/analytics/dashboard', {
    params: { time_range: 'month', include_charts: true }
});

// 渲染各项统计
renderFrequencyChart(dashboard.data.frequency);
renderDurationChart(dashboard.data.duration);
renderCaloriesChart(dashboard.data.calories);
```

### 步骤3: 进步追踪

```javascript
// 获取力量进步
const progress = await axios.get('/api/analytics/strength-progress', {
    params: { time_range: 'all', include_chart: true }
});

// 为每个运动渲染进步曲线
progress.data.forEach(exercise => {
    renderProgressCard({
        name: exercise.exercise_name,
        progress: exercise.progress,
        chart: exercise.chart
    });
});
```

### 步骤4: 排行榜

```javascript
// 获取排行榜
const leaderboard = await axios.get('/api/analytics/leaderboard', {
    params: {
        metric: 'workouts',
        time_range: 'month',
        limit: 20,
        scope: 'global'
    }
});

// 渲染排行榜
renderLeaderboard(leaderboard.data.rankings);
renderMyRank(leaderboard.data.current_user_rank);
```

---

## 🔧 技术实现

### 数据模型

系统基于以下数据模型:
- `User` - 用户信息
- `WorkoutRecord` - 训练记录
- `ExerciseRecord` - 运动记录
- `SetRecord` - 组数记录
- `WeightRecord` - 体重记录
- `Achievement` - 成就系统
- `Follow` - 关注关系

### 核心服务

**AnalyticsService** (`services/analytics_service.py`)
- 8个核心统计方法
- SQLAlchemy聚合查询
- 图表数据生成

**LeaderboardService** (`services/leaderboard_service.py`)
- 5种排名指标
- 3种排名范围
- 排名算法优化

**ComparisonService** (`services/leaderboard_service.py`)
- 多用户对比
- 多指标分析
- 对比图表生成

### 数据聚合示例

```python
# 训练次数统计
workout_count = db.session.query(
    func.count(WorkoutRecord.id)
).filter(
    WorkoutRecord.user_id == user_id,
    WorkoutRecord.status == 'completed',
    WorkoutRecord.start_time >= start_date
).scalar()

# 训练容量计算
total_volume = db.session.query(
    func.sum(SetRecord.weight * SetRecord.reps)
).join(ExerciseRecord).join(WorkoutRecord).filter(
    WorkoutRecord.user_id == user_id,
    WorkoutRecord.start_time >= start_date
).scalar()
```

---

## ⚡ 性能优化

### 1. 查询优化

```python
# 使用索引
WorkoutRecord.__table__.create_index('idx_user_start_time', 
    ['user_id', 'start_time'])

# 预加载关联数据
workout = db.session.query(WorkoutRecord).options(
    joinedload(WorkoutRecord.exercise_records)
).filter_by(id=workout_id).first()
```

### 2. 缓存策略

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@cache.cached(timeout=300, key_prefix='leaderboard')
def get_leaderboard_data():
    # ... 排行榜查询
    pass
```

### 3. 分页查询

```python
# 排行榜分页
rankings = db.session.query(
    User.id, func.count(WorkoutRecord.id).label('count')
).join(WorkoutRecord).group_by(User.id).order_by(
    desc('count')
).limit(limit).all()
```

---

## 📊 数据可视化

### 支持的图表类型

1. **折线图 (line)** - 趋势分析
   - 力量进步曲线
   - 体重变化趋势
   - 时间序列数据

2. **柱状图 (bar)** - 对比分析
   - 训练频率对比
   - 用户数据对比
   - 周/月统计

3. **饼图 (pie)** - 占比分析
   - 训练容量分布
   - 肌群训练占比
   - 成就分类统计

4. **面积图 (area)** - 累积趋势
   - 训练时长累积
   - 卡路里消耗累积

5. **散点图 (scatter)** - 分布分析
   - 数据分布可视化

### 图表数据格式

```json
{
    "chart_type": "line",
    "title": "深蹲力量进步",
    "data": [
        {
            "date": "2024-01-01",
            "value": 60.0,
            "label": "60kg"
        }
    ],
    "x_axis_label": "日期",
    "y_axis_label": "重量",
    "unit": "kg"
}
```

### 前端渲染示例 (Chart.js)

```javascript
function renderChart(chartData) {
    new Chart(ctx, {
        type: chartData.chart_type,
        data: {
            labels: chartData.data.map(d => d.date),
            datasets: [{
                label: chartData.title,
                data: chartData.data.map(d => d.value),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: chartData.x_axis_label } },
                y: { title: { display: true, text: chartData.y_axis_label } }
            }
        }
    });
}
```

---

## 🔒 安全性

### 认证和授权

所有分析API都需要JWT认证:

```python
from utils.auth import token_required

@analytics_bp.route('/frequency', methods=['GET'])
@token_required
def get_frequency_statistics(current_user):
    # 只能访问自己的数据
    user_id = current_user.id
    # ...
```

### 数据隔离

- 用户只能查看自己的详细数据
- 排行榜只显示公开信息(昵称、头像)
- 对比功能需要关注/好友关系验证

---

## 🧪 测试指南

### 使用测试工具

```bash
# 启动交互式测试
python test_analytics.py

# 按提示输入:
# 1. API地址 (默认: http://localhost:5000)
# 2. 认证Token
# 3. 选择测试项目 (1-12)
```

### 测试场景

1. **基础统计** - 测试频率、时长、卡路里统计
2. **进步追踪** - 测试力量和身体数据分析
3. **仪表盘** - 测试综合数据展示
4. **排行榜** - 测试不同指标和范围
5. **用户对比** - 测试多用户多指标对比

### 测试数据准备

```sql
-- 插入测试训练记录
INSERT INTO workout_records (user_id, plan_id, start_time, end_time, status, calories)
VALUES (1, 1, '2024-01-01 10:00:00', '2024-01-01 11:00:00', 'completed', 500);

-- 插入测试体重记录
INSERT INTO weight_records (user_id, weight, body_fat, recorded_at)
VALUES (1, 75.5, 20.0, '2024-01-01 08:00:00');
```

---

## 📈 未来扩展

### 计划中的功能

- [ ] 实时数据推送(WebSocket)
- [ ] 周报/月报自动生成
- [ ] AI健身建议(基于数据分析)
- [ ] 社区挑战和活动排名
- [ ] 数据导出(PDF/Excel)
- [ ] 更多图表类型(雷达图、热力图)

### 性能优化计划

- [ ] Redis缓存完整实现
- [ ] 定时任务预计算统计数据
- [ ] 数据库分区优化
- [ ] CDN加速图表资源

---

## 📞 技术支持

### 文档资源

- [完整API文档](./ANALYTICS_API.md) - 所有接口详细说明
- [快速参考](./ANALYTICS_QUICK_REFERENCE.md) - 常用代码示例
- [测试工具](./test_analytics.py) - 交互式测试

### 常见问题

**Q: 如何修改时间范围?**
A: 使用 `time_range` 参数,支持 week/month/quarter/year/all

**Q: 图表数据太大怎么办?**
A: 设置 `include_chart=false`,前端自行绘制

**Q: 排行榜刷新频率?**
A: 建议实现5分钟缓存,定时刷新

**Q: 如何优化查询性能?**
A: 添加数据库索引,使用Redis缓存,限制返回数量

---

## 🎯 总结

数据统计分析系统提供了完整的用户数据分析能力:

✅ **11个REST API** - 覆盖所有统计场景
✅ **8种核心分析** - 频率、时长、力量、身体、卡路里、容量、成就、仪表盘
✅ **5种图表类型** - 支持多种可视化方式
✅ **排行榜系统** - 5种指标,3种范围
✅ **用户对比** - 多用户多指标分析
✅ **完整文档** - API文档、快速参考、测试工具

系统已经可以投入使用,支持Web和移动端集成!

---

**版本**: v1.0  
**最后更新**: 2024-01-01  
**API数量**: 11个核心接口  
**文档**: 3个完整文档 + 交互式测试工具
