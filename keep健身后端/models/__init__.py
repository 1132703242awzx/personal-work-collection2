"""
数据模型包初始化
导出所有数据模型以便统一管理
"""
from .base import BaseModel
from .user import User, UserProfile, UserSettings
from .training import TrainingPlan, PlanDay, Exercise
from .workout import WorkoutRecord, ExerciseRecord, SetRecord
from .course import Course, Chapter, Video
from .social import Follow, Like, Comment
from .body_data import BodyData, WeightRecord, BodyMeasurements
from .auth import (
    UserRole, ThirdPartyAccount, RefreshToken, 
    PasswordResetToken, LoginHistory, SecurityLog,
    UserRoleEnum, ThirdPartyProviderEnum, TokenTypeEnum
)
from .feed import (
    Feed, FeedShare, Hashtag, HashtagFollow,
    Achievement, UserAchievement
)
from .notification import (
    Notification, NotificationSetting,
    Message, Conversation
)

__all__ = [
    'BaseModel',
    'User', 'UserProfile', 'UserSettings',
    'TrainingPlan', 'PlanDay', 'Exercise',
    'WorkoutRecord', 'ExerciseRecord', 'SetRecord',
    'Course', 'Chapter', 'Video',
    'Follow', 'Like', 'Comment',
    'BodyData', 'WeightRecord', 'BodyMeasurements',
    'UserRole', 'ThirdPartyAccount', 'RefreshToken',
    'PasswordResetToken', 'LoginHistory', 'SecurityLog',
    'UserRoleEnum', 'ThirdPartyProviderEnum', 'TokenTypeEnum',
    'Feed', 'FeedShare', 'Hashtag', 'HashtagFollow',
    'Achievement', 'UserAchievement',
    'Notification', 'NotificationSetting',
    'Message', 'Conversation'
]
