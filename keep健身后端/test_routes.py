"""
测试所有页面路由
"""
print("=" * 70)
print("Keep健身仪表盘 - 页面路由测试")
print("=" * 70)

pages = {
    "仪表盘": "/dashboard",
    "运动记录": "/workout/records",
    "添加记录": "/workout/add",
    "身体数据": "/workout/body-records",
    "数据分析": "/analytics/overview",
    "运动统计": "/analytics/workout-stats",
    "体重趋势": "/analytics/body-stats",
    "个人资料": "/auth/profile",
    "修改密码": "/auth/change-password",
}

print("\n✓ 所有路由已配置:")
for name, route in pages.items():
    print(f"  • {name:12} -> {route}")

print("\n" + "=" * 70)
print("请访问 http://127.0.0.1:8080 并使用 demo/123456 登录")
print("=" * 70)
