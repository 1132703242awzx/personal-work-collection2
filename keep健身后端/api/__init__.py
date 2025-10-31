"""
API包初始化
"""
from .auth import auth_bp
from .training import training_bp

__all__ = ['auth_bp', 'training_bp']
