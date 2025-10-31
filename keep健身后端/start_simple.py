"""
最简单的启动脚本 - 用于测试
"""
import sys
import os

# 确保在正确的目录
os.chdir(r'D:\keep健身后端')
sys.path.insert(0, r'D:\keep健身后端')

print("=" * 60)
print("开始启动Keep健身仪表盘...")
print("=" * 60)

try:
    from app_dashboard import create_app
    print("✓ 导入应用成功")
    
    app = create_app()
    print("✓ 创建应用成功")
    
    print("\n" + "=" * 60)
    print("Keep健身仪表盘已启动!")
    print("访问地址: http://127.0.0.1:5000")
    print("测试账号: demo / 123456")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")
    
    # 启动服务器
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    input("\n按任意键退出...")
