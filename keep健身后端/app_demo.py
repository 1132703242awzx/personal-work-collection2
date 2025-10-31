"""
Keep健身后端 - 无数据库演示模式
用于测试API结构，不需要MySQL连接
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_demo_app():
    app = Flask(__name__)
    
    # 基础配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'demo-secret-key')
    app.config['DEBUG'] = True
    
    # 启用CORS
    CORS(app)
    
    # 首页路由
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Keep健身后端API - 演示模式',
            'version': '1.0.0',
            'status': 'running',
            'mode': 'demo (无数据库)',
            'note': '请启动MySQL服务器后使用完整功能',
            'mysql_config': {
                'required': True,
                'host': 'localhost',
                'port': 3306,
                'database': 'keep_fitness'
            },
            'available_endpoints': {
                'health': 'GET /',
                'api_list': 'GET /api',
                'auth': 'POST /api/auth/register, POST /api/auth/login',
                'plans': 'GET/POST /api/plans',
                'workouts': 'GET/POST /api/workouts',
                'social': 'GET /api/social/timeline',
                'analytics': 'GET /api/analytics/overview'
            },
            'total_apis': '69+个接口',
            'modules': {
                '认证系统': '2个API',
                '训练计划': '8个API',
                '运动记录': '18个API',
                '社交系统': '30个API',
                '数据分析': '11个API'
            }
        }), 200
    
    @app.route('/api')
    def api_list():
        return jsonify({
            'message': 'Keep健身API列表',
            'endpoints': [
                {'path': '/api/auth/register', 'method': 'POST', 'desc': '用户注册'},
                {'path': '/api/auth/login', 'method': 'POST', 'desc': '用户登录'},
                {'path': '/api/plans', 'method': 'GET', 'desc': '训练计划列表'},
                {'path': '/api/plans', 'method': 'POST', 'desc': '创建训练计划'},
                {'path': '/api/workouts', 'method': 'GET', 'desc': '训练记录列表'},
                {'path': '/api/workouts', 'method': 'POST', 'desc': '创建训练记录'},
                {'path': '/api/social/timeline', 'method': 'GET', 'desc': '动态时间线'},
                {'path': '/api/social/feeds', 'method': 'POST', 'desc': '发布动态'},
                {'path': '/api/analytics/overview', 'method': 'GET', 'desc': '数据概览'},
                {'path': '/api/analytics/dashboard', 'method': 'GET', 'desc': '综合仪表盘'}
            ]
        }), 200
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'ok',
            'mode': 'demo',
            'database': 'disconnected'
        }), 200
    
    # 演示API端点
    @app.route('/api/auth/register', methods=['POST'])
    def demo_register():
        return jsonify({
            'code': 503,
            'message': '演示模式：请启动MySQL服务器以使用完整功能',
            'note': '当前为无数据库演示模式'
        }), 503
    
    @app.route('/api/auth/login', methods=['POST'])
    def demo_login():
        return jsonify({
            'code': 503,
            'message': '演示模式：请启动MySQL服务器以使用完整功能'
        }), 503
    
    return app

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Keep健身后端 - 演示模式启动")
    print("=" * 60)
    print("\n⚠️  当前为无数据库演示模式")
    print("   - 可以查看API结构")
    print("   - 无法执行实际数据操作")
    print("   - 请启动MySQL服务器后使用: python app.py\n")
    print("MySQL配置:")
    print("   - 主机: localhost")
    print("   - 端口: 3306")
    print("   - 数据库: keep_fitness")
    print("   - 用户: root")
    print("\n" + "=" * 60)
    print("服务器启动中...")
    print("=" * 60)
    print("\n访问地址:")
    print("   - http://localhost:5000/")
    print("   - http://localhost:5000/api")
    print("   - http://localhost:5000/health")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")
    
    app = create_demo_app()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
