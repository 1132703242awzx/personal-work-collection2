"""
简单的仪表盘启动脚本
避免调试模式重启问题
"""
from app_dashboard import create_app

if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("Keep健身仪表盘启动成功!")
    print("访问地址: http://127.0.0.1:5000")
    print("测试账号: demo / 123456")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
