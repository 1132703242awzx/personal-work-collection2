"""
快速测试所有API端点
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8080"

print("=" * 70)
print("Keep健身仪表盘 - API端点测试")
print("=" * 70 + "\n")

# 测试需要登录的API端点
apis = [
    ("运动趋势API", "/analytics/api/workout-trend?days=30"),
    ("运动类型分布", "/analytics/api/workout-type-distribution"),
    ("身体数据趋势", "/analytics/api/body-data-trend?days=90"),
    ("月度统计API", "/analytics/api/monthly-stats"),
    ("汇总统计API", "/analytics/api/summary-stats"),
]

print("⚠️  注意: 需要先在浏览器登录 (demo/123456) 才能测试API")
print("\n以下是API端点列表:\n")

for name, endpoint in apis:
    full_url = BASE_URL + endpoint
    print(f"✅ {name:16} -> {endpoint}")

print("\n" + "=" * 70)
print("测试方法:")
print("1. 在浏览器打开 http://127.0.0.1:8080")
print("2. 使用 demo/123456 登录")
print("3. 打开开发者工具(F12)")
print("4. 切换到Network标签")
print("5. 访问各个图表页面")
print("6. 查看API请求是否成功返回数据")
print("=" * 70)
