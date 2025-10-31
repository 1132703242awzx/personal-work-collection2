"""
Keep健身后端主应用
企业级Flask应用架构
"""
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os

from config import config, shutdown_session
from models import *


def create_app(config_name='development'):
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称 (development/production/testing)
    
    Returns:
        Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 启用CORS
    CORS(app)
    
    # 注册数据库关闭钩子
    @app.teardown_appcontext
    def teardown_db(exception=None):
        shutdown_session(exception)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 健康检查端点
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'app': app.config['APP_NAME'],
            'version': app.config['APP_VERSION']
        })
    
    # 首页 - 显示友好的管理界面
    @app.route('/')
    def index():
        # 如果是浏览器访问,返回HTML页面
        return render_template('index.html')
    
    # API信息端点
    @app.route('/api')
    def api_info():
        return jsonify({
            'message': 'Welcome to Keep Fitness API',
            'version': app.config['APP_VERSION'],
            'endpoints': {
                'health': '/health',
                'api_docs': '/api/docs'
            }
        })
    
    return app


def register_blueprints(app):
    """注册蓝图"""
    from api.auth import auth_bp
    from api.training import training_bp
    from api.workout import workout_bp
    from api.social import social_bp
    from api.analytics import analytics_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(social_bp)
    app.register_blueprint(analytics_bp)


def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred'
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request was invalid or cannot be served'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication is required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403


if __name__ == '__main__':
    # 创建应用实例
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    
    # 运行应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
