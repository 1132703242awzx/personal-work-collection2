"""
Keep健身后端 - 使用Waitress启动
更稳定的WSGI服务器
"""
print("正在启动Keep健身后端...")
print("=" * 60)

try:
    from app_demo import create_demo_app
    from waitress import serve
    
    app = create_demo_app()
    
    print("\n✓ 应用创建成功")
    print("✓ 使用Waitress WSGI服务器")
    print("\n" + "=" * 60)
    print("Keep健身后端 - 演示模式")
    print("=" * 60)
    print("\n访问地址:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/api")
    print("  - http://localhost:5000/health")
    print("\n⚠️  当前为无数据库演示模式")
    print("   请启动MySQL服务器后使用完整功能")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")
    
    # 使用Waitress启动
    serve(app, host='0.0.0.0', port=5000, threads=4)
    
except KeyboardInterrupt:
    print("\n\n服务器已停止")
except Exception as e:
    print(f"\n启动失败: {e}")
    import traceback
    traceback.print_exc()
