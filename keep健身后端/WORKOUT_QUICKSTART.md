# 运动记录系统快速启动指南 🚀

## 📦 安装依赖

由于网络问题,尝试以下方法安装Pydantic:

### 方法1: 清除代理
```powershell
pip install pydantic==2.5.0 --proxy=""
```

### 方法2: 使用国内镜像
```powershell
pip install pydantic==2.5.0 -i https://mirrors.aliyun.com/pypi/simple/
```

### 方法3: 手动下载安装
```powershell
# 1. 下载wheel文件
# 访问: https://pypi.org/project/pydantic/2.5.0/#files
# 下载对应Python版本的wheel文件

# 2. 安装
pip install pydantic-2.5.0-py3-none-any.whl
```

---

## 🎯 快速测试

### 1. 启动应用
```powershell
cd "d:\keep健身后端"
python app.py
```

### 2. 获取Token
使用已有的认证接口获取JWT token

### 3. 运行测试工具
```powershell
python test_workout.py
```

### 4. 测试单个接口

#### 创建训练记录
```powershell
curl -X POST http://localhost:5000/api/workouts `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -d '{
    "workout_date": "2024-01-20",
    "workout_type": "力量训练",
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
  }'
```

#### 获取统计数据
```powershell
curl http://localhost:5000/api/stats/overview `
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 查看训练日历
```powershell
curl "http://localhost:5000/api/workouts/calendar?year=2024&month=1" `
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 系统架构

```
运动记录系统
│
├── 数据层 (models/)
│   └── workout.py - 已存在的数据模型
│
├── 验证层 (schemas/) - ✅ 新增
│   ├── workout_schemas.py - Pydantic验证模型
│   └── __init__.py - 导出
│
├── 服务层 (services/) - ✅ 新增
│   ├── workout_service.py - 训练业务逻辑
│   └── stats_service.py - 统计分析
│
├── API层 (api/) - ✅ 新增
│   └── workout.py - REST接口
│
├── 测试 (tests/) - ✅ 新增
│   └── test_workout.py - 交互式测试工具
│
└── 文档 (docs/) - ✅ 新增
    └── WORKOUT_API_QUICK_REFERENCE.md
```

---

## 🔥 核心功能演示

### 场景1: 记录今天的训练

```python
import requests

# 1. 创建训练记录
workout = {
    "workout_date": "2024-01-20",
    "workout_type": "力量训练",
    "exercises": [
        {
            "exercise_name": "深蹲",
            "muscle_group": "腿部",
            "sets": [
                {"set_number": 1, "set_type": "warmup", "reps": 10, "weight": 60},
                {"set_number": 2, "set_type": "normal", "reps": 8, "weight": 80},
                {"set_number": 3, "set_type": "normal", "reps": 8, "weight": 85}
            ]
        }
    ]
}

response = requests.post(
    'http://localhost:5000/api/workouts',
    json=workout,
    headers={'Authorization': f'Bearer {token}'}
)

workout_id = response.json()['data']['id']

# 2. 完成训练
requests.post(
    f'http://localhost:5000/api/workouts/{workout_id}/finish',
    json={'notes': '今天状态很好!'},
    headers={'Authorization': f'Bearer {token}'}
)
```

### 场景2: 查看本周训练数据

```python
# 获取周统计
response = requests.get(
    'http://localhost:5000/api/stats/weekly',
    headers={'Authorization': f'Bearer {token}'}
)

week_stats = response.json()['data']
print(f"本周训练: {week_stats['week_total']['total_workouts']}次")
print(f"总时长: {week_stats['week_total']['total_duration']}分钟")
print(f"总卡路里: {week_stats['week_total']['total_calories']}千卡")
```

### 场景3: 追踪个人记录

```python
# 获取深蹲的个人最佳记录
response = requests.get(
    'http://localhost:5000/api/workouts/records',
    params={'exercise_name': '深蹲'},
    headers={'Authorization': f'Bearer {token}'}
)

records = response.json()['data']
for record in records:
    print(f"最大重量: {record['best_weight']}kg")
    print(f"最多次数: {record['best_reps']}次")
    print(f"最高总量: {record['best_volume']}kg")
```

### 场景4: 查看坚持度评分

```python
# 获取坚持度评分
response = requests.get(
    'http://localhost:5000/api/stats/consistency',
    headers={'Authorization': f'Bearer {token}'}
)

score = response.json()['data']
print(f"30天训练: {score['training_days']}天")
print(f"坚持率: {score['consistency_rate']}%")
print(f"评分等级: {score['grade']} - {score['grade_text']}")
print(f"连续训练: {score['current_streak']}天")
```

---

## 🎯 功能亮点

### 1. 数据验证 ✨
- Pydantic自动验证所有输入
- 友好的错误提示
- 类型安全保证

### 2. 性能优化 ⚡
- 批量插入优化
- 关联预加载
- 数据库事务处理

### 3. 智能统计 📊
- 自动计算统计数据
- 个人记录检测
- 多维度分析

### 4. 用户体验 💯
- RESTful API设计
- 统一响应格式
- 完善的错误处理

---

## 📚 相关文档

- **API速查表**: `docs/WORKOUT_API_QUICK_REFERENCE.md`
- **实现总结**: `WORKOUT_IMPLEMENTATION_SUMMARY.md`
- **测试工具**: `test_workout.py`

---

## ⚠️ 注意事项

1. **依赖安装**: 必须先安装pydantic才能运行
2. **数据库**: 确保MySQL服务正在运行
3. **认证**: 所有接口都需要有效的JWT token
4. **时区**: 默认使用UTC时间

---

## 🆘 常见问题

### Q1: 安装pydantic失败
A: 尝试使用国内镜像或手动下载安装

### Q2: 运行test_workout.py报错
A: 确保Flask应用已启动,且有有效的token

### Q3: 数据库连接失败
A: 检查config/config.py中的数据库配置

### Q4: API返回401错误
A: token可能已过期,需要重新登录获取

---

## 📞 技术支持

如有问题,请查看:
1. 代码注释
2. API文档
3. 测试用例
4. 实现总结

---

**祝训练愉快! 💪**
