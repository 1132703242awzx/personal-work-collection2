"""
Keep健身仪表盘 - 主应用
基于Flask服务器端渲染架构
"""
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, current_user
from datetime import datetime
import os

from dashboard_config import Config
from dashboard_models import db, User
from dashboard_auth import auth_bp
from dashboard_main import main_bp
from dashboard_workout import workout_bp
from dashboard_analytics import analytics_bp


def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(analytics_bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 全局上下文处理器
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    # 错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
