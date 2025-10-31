"""
临时启动脚本 - 不加载需要pydantic的模块
等待pydantic安装成功后,使用 python app.py 启动完整功能
"""
import os
from flask import Flask
from flask_cors import CORS

def create_app_minimal():
    """创建最小化Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    
    # 启用CORS
    CORS(app)
    
    # 只注册不需要pydantic的蓝图
    try:
        from api.auth import auth_bp
        app.register_blueprint(auth_bp)
        print("✓ 认证系统已加载")
    except Exception as e:
        print(f"✗ 认证系统加载失败: {e}")
    
    try:
        from api.training import training_bp
        app.register_blueprint(training_bp)
        print("✓ 训练计划系统已加载")
    except Exception as e:
        print(f"✗ 训练计划系统加载失败: {e}")
    
    # 跳过需要pydantic的模块
    print("\n⚠️  以下模块需要pydantic,暂时跳过:")
    print("  - 运动记录系统 (api.workout)")
    print("  - 社交系统 (api.social)")
    print("  - 数据分析系统 (api.analytics)")
    
    @app.route('/')
    def index():
        return {
            'message': 'Keep健身后端API',
            'version': '1.0.0',
            'status': 'running (minimal mode)',
            'available_modules': [
                '认证系统 (/api/auth)',
                '训练计划系统 (/api/plans)'
            ],
            'disabled_modules': [
                '运动记录系统 (需要安装pydantic)',
                '社交系统 (需要安装pydantic)',
                '数据分析系统 (需要安装pydantic)'
            ],
            'note': '请安装pydantic后使用完整功能: pip install pydantic==2.5.0'
        }
    
    @app.route('/health')
    def health():
        return {'status': 'ok', 'mode': 'minimal'}
    
    return app


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Keep健身后端 - 最小化模式启动")
    print("="*60)
    print("\n正在加载模块...\n")
    
    app = create_app_minimal()
    
    print("\n" + "="*60)
    print("服务器启动中...")
    print("="*60)
    print("\n访问地址:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/health")
    print("  - http://localhost:5000/api/auth/register")
    print("  - http://localhost:5000/api/plans")
    print("\n按 Ctrl+C 停止服务器")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
