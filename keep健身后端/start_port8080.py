"""
使用8080端口启动 - 避免5000端口冲突
"""
import sys
import os

os.chdir(r'D:\keep健身后端')
sys.path.insert(0, r'D:\keep健身后端')

print("=" * 60)
print("Keep健身仪表盘 - 使用8080端口")
print("=" * 60)

try:
    from app_dashboard import create_app
    
    app = create_app()
    
    print("\n✓ 应用创建成功")
    print("\n" + "=" * 60)
    print("访问地址: http://127.0.0.1:8080")
    print("测试账号: demo / 123456")
    print("=" * 60 + "\n")
    
    app.run(
        host='127.0.0.1',  # 只监听本地
        port=8080,
        debug=False,
        use_reloader=False
    )
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    input("\n按任意键退出...")
