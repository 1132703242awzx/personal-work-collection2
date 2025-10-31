"""
服务层包初始化
"""
from .auth_service import AuthService
from .third_party_auth_service import ThirdPartyAuthService
from .training_service import TrainingService

__all__ = [
    'AuthService',
    'ThirdPartyAuthService',
    'TrainingService'
]
