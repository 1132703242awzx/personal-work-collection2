"""
快速验证所有模板文件
"""
import os

print("=" * 70)
print("Keep健身仪表盘 - 模板文件验证")
print("=" * 70 + "\n")

templates = [
    ("仪表盘", "templates/dashboard/index.html"),
    ("运动记录", "templates/workout/records.html"),
    ("添加记录", "templates/workout/add.html"),
    ("身体数据", "templates/workout/body_records.html"),
    ("数据分析", "templates/analytics/overview.html"),
    ("运动统计", "templates/analytics/workout_stats.html"),
    ("体重趋势", "templates/analytics/body_stats.html"),
    ("个人资料", "templates/auth/profile.html"),
    ("修改密码", "templates/auth/change_password.html"),
    ("登录页面", "templates/auth/login.html"),
    ("注册页面", "templates/auth/register.html"),
]

all_ok = True
for name, path in templates:
    full_path = os.path.join(r"D:\keep健身后端", path)
    exists = os.path.exists(full_path)
    
    if exists:
        size = os.path.getsize(full_path)
        if size > 0:
            print(f"✅ {name:12} - {path:45} ({size:,} bytes)")
        else:
            print(f"❌ {name:12} - {path:45} (空文件!)")
            all_ok = False
    else:
        print(f"❌ {name:12} - {path:45} (不存在!)")
        all_ok = False

print("\n" + "=" * 70)
if all_ok:
    print("✅ 所有模板文件验证通过!")
    print("\n访问 http://127.0.0.1:8080")
    print("测试账号: demo / 123456")
else:
    print("❌ 部分模板文件有问题,请检查!")
print("=" * 70)
