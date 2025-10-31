"""
使用Waitress WSGI服务器启动
Waitress在Windows上更稳定,不会被安全软件拦截
"""
import sys
import os

os.chdir(r'D:\keep健身后端')
sys.path.insert(0, r'D:\keep健身后端')

print("=" * 70)
print(" Keep健身仪表盘 - Waitress服务器")
print("=" * 70)

try:
    from waitress import serve
    from app_dashboard import create_app
    
    app = create_app()
    print("\n✓ 应用创建成功")
    print("\n" + "=" * 70)
    print(" 服务器启动成功!")
    print(" ")
    print(" 访问地址: http://127.0.0.1:8080")
    print(" 测试账号: demo / 123456")
    print(" ")
    print(" 按 Ctrl+C 停止服务器")
    print("=" * 70 + "\n")
    
    # 使用waitress启动,绑定到本地8080端口
    serve(app, host='127.0.0.1', port=8080, threads=4)
    
except KeyboardInterrupt:
    print("\n服务器已停止")
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    input("\n按Enter键退出...")
