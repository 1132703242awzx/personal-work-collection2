# Keep健身仪表盘 - 图表和API完整指南

## 🎨 所有图表页面

### 1. 仪表盘 (`/dashboard`)
**图表类型**:
- 📈 运动趋势折线图 - 近30天卡路里和时长
- 🍩 运动类型饼图 - 各类运动占比

**数据展示**:
- 4个统计卡片:本周运动、本月消耗、本月时长、BMI
- 最近运动记录表格(最多10条)
- 最新身体数据卡片

**API端点**:
- `GET /analytics/api/workout-trend?days=30`
- `GET /analytics/api/workout-type-distribution`

---

### 2. 数据分析 (`/analytics/overview`)
**图表类型**:
- 📊 月度运动统计柱状图 - 最近6个月运动次数
- 🍩 运动类型分布饼图 - 各类运动占比

**数据展示**:
- 4个统计卡片:总运动次数、总消耗、总时长、平均时长

**API端点**:
- `GET /analytics/api/monthly-stats`
- `GET /analytics/api/workout-type-distribution`

---

### 3. 运动统计 (`/analytics/workout-stats`)
**图表类型**:
- 📈 运动趋势折线图 - 近30天数据
- 📊 运动时长分布柱状图
- 🥧 难度分布饼图

**API端点**:
- `GET /analytics/api/workout-trend?days=30`

---

### 4. 体重趋势 (`/analytics/body-stats`) ✨ 重点修复
**图表类型**:
- 📈 体重变化趋势折线图 - 90天数据
- 📉 体脂率变化折线图
- 📊 BMI变化折线图

**数据展示**:
- 所有图表都依赖身体数据记录
- 自动计算BMI(需要用户设置身高)

**API端点**:
- `GET /analytics/api/body-data-trend?days=90` ✅ 已修复

---

### 5. 身体数据 (`/workout/body-records`)
**图表类型**:
- 📈 体重变化趋势折线图 - 90天数据

**数据展示**:
- 身体数据记录表格
- 最新数据卡片

**API端点**:
- `GET /analytics/api/body-data-trend?days=90`

---

## 🔌 API端点列表

### 运动数据API

#### 1. 运动趋势
```
GET /analytics/api/workout-trend?days=30
```
**返回**:
```json
{
  "labels": ["10-01", "10-02", ...],
  "calories": [250, 300, ...],
  "duration": [30, 45, ...],
  "distance": [5.0, 6.2, ...]
}
```

#### 2. 运动类型分布
```
GET /analytics/api/workout-type-distribution
```
**返回**:
```json
{
  "labels": ["running", "cycling", "swimming"],
  "data": [10, 8, 5]
}
```

#### 3. 月度统计 ✅ 新增
```
GET /analytics/api/monthly-stats
```
**返回**:
```json
{
  "labels": ["2025-05", "2025-06", "2025-07", ...],
  "count": [12, 15, 18, ...]
}
```

### 身体数据API

#### 4. 身体数据趋势 ✅ 已修复
```
GET /analytics/api/body-data-trend?days=90
```
**返回**:
```json
{
  "labels": ["10-01", "10-02", ...],
  "weight": [65.5, 65.3, 65.0, ...],
  "body_fat": [16.5, 16.3, 16.0, ...],
  "bmi": [21.4, 21.3, 21.2, ...]
}
```

#### 5. 汇总统计
```
GET /analytics/api/summary-stats
```
**返回**:
```json
{
  "total_workouts": 30,
  "total_calories": 8500,
  "total_duration": 900,
  "week_workouts": 5,
  "month_calories": 2500,
  "avg_duration": 30
}
```

---

## 🔧 本次修复内容

### 问题1: 体重趋势页面没有图表数据
**原因**: API端点名称不匹配
- 模板调用: `/analytics/api/body-data-trend`
- 实际端点: `/analytics/api/body-weight-trend`

**解决方案**:
✅ 添加了 `/analytics/api/body-data-trend` 端点
✅ 实现完整的数据返回:
  - 体重数据 (weight)
  - 体脂率数据 (body_fat)
  - BMI数据 (自动计算)

### 问题2: 缺少月度统计API
**原因**: 数据分析页面需要月度统计数据

**解决方案**:
✅ 添加了 `/analytics/api/monthly-stats` 端点
✅ 使用Pandas处理数据
✅ 返回最近6个月的运动次数

---

## 📊 图表配置详情

### Chart.js 配置

#### 折线图 (Line Chart)
```javascript
{
  type: 'line',
  data: {
    labels: ['10-01', '10-02', ...],
    datasets: [{
      label: '体重(kg)',
      data: [65.5, 65.3, ...],
      borderColor: '#4F46E5',
      backgroundColor: 'rgba(79, 70, 229, 0.1)',
      tension: 0.4,
      fill: true
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: true
  }
}
```

#### 饼图 (Doughnut Chart)
```javascript
{
  type: 'doughnut',
  data: {
    labels: ['跑步', '骑行', '游泳'],
    datasets: [{
      data: [10, 8, 5],
      backgroundColor: ['#4F46E5', '#10B981', '#F59E0B']
    }]
  }
}
```

#### 柱状图 (Bar Chart)
```javascript
{
  type: 'bar',
  data: {
    labels: ['2025-05', '2025-06'],
    datasets: [{
      label: '运动次数',
      data: [12, 15],
      backgroundColor: '#4F46E5',
      borderRadius: 4
    }]
  }
}
```

---

## 🧪 测试步骤

### 测试体重趋势页面
1. 访问 http://127.0.0.1:8080
2. 登录: demo / 123456
3. 点击左侧菜单"体重趋势"
4. **预期结果**:
   - ✅ 顶部显示体重变化趋势折线图(90天)
   - ✅ 左下显示体脂率变化折线图
   - ✅ 右下显示BMI变化折线图
   - 📊 图表应该显示12条测试数据的曲线

### 测试数据分析页面
1. 点击左侧菜单"数据分析"
2. **预期结果**:
   - ✅ 4个统计卡片显示数据
   - ✅ 月度运动统计柱状图
   - ✅ 运动类型分布饼图

### 测试仪表盘
1. 点击左侧菜单"仪表盘"
2. **预期结果**:
   - ✅ 运动趋势折线图(双线:卡路里+时长)
   - ✅ 运动类型饼图
   - ✅ 所有统计卡片有数据

---

## 🎨 图表颜色方案

### 主色调
- 主蓝色: `#4F46E5` (Indigo)
- 成功绿: `#10B981` (Emerald)
- 警告橙: `#F59E0B` (Amber)
- 信息青: `#06B6D4` (Cyan)
- 紫色: `#8B5CF6` (Violet)
- 粉色: `#EC4899` (Pink)

### 半透明背景
- 使用 `rgba(R, G, B, 0.1)` 作为填充色
- 边框使用完全不透明色

---

## 🚨 故障排除

### 如果图表不显示:
1. **检查浏览器控制台**
   - F12 打开开发者工具
   - 查看Console标签是否有JavaScript错误
   - 查看Network标签API请求是否成功

2. **检查API返回数据**
   - 直接访问API端点:
     - http://127.0.0.1:8080/analytics/api/body-data-trend?days=90
   - 确认返回JSON格式正确

3. **检查Chart.js加载**
   - 确认CDN链接可访问
   - 查看Network标签中Chart.js是否加载成功

### 如果数据为空:
1. **检查测试数据**
   - 确认数据库中有身体数据记录
   - 运行: `python init_dashboard.py` 重新初始化测试数据

2. **检查用户身高**
   - BMI计算需要用户设置身高
   - 在"个人资料"页面设置身高

---

## ✅ 修复完成清单

- ✅ 添加 `/analytics/api/body-data-trend` API端点
- ✅ 添加 `/analytics/api/monthly-stats` API端点
- ✅ 体重趋势页面可显示3个图表
- ✅ 数据分析页面可显示2个图表
- ✅ BMI自动计算功能
- ✅ 服务器正常运行

---

**修复时间**: 2025年10月25日  
**服务器状态**: ✅ 运行中 (http://127.0.0.1:8080)  
**测试账号**: demo / 123456
