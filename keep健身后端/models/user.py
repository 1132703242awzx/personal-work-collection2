"""
用户体系模型
包含用户、用户资料、用户设置
"""
from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class GenderEnum(enum.Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserStatusEnum(enum.Enum):
    """用户状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class User(BaseModel):
    """用户基础信息表"""
    
    __tablename__ = 'users'
    
    # 基础信息
    username = Column(String(50), unique=True, nullable=False, index=True, comment='用户名')
    email = Column(String(100), unique=True, nullable=False, index=True, comment='邮箱')
    phone = Column(String(20), unique=True, index=True, comment='手机号')
    password_hash = Column(String(255), nullable=False, comment='密码哈希')
    
    # 状态信息
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.ACTIVE, 
                   nullable=False, index=True, comment='用户状态')
    is_verified = Column(Boolean, default=False, nullable=False, comment='是否验证')
    is_premium = Column(Boolean, default=False, nullable=False, 
                       index=True, comment='是否高级会员')
    
    # 安全相关
    last_login_at = Column(Date, comment='最后登录时间')
    login_count = Column(Integer, default=0, comment='登录次数')
    
    # 关系映射
    profile = relationship('UserProfile', back_populates='user', uselist=False, 
                          cascade='all, delete-orphan')
    settings = relationship('UserSettings', back_populates='user', uselist=False,
                           cascade='all, delete-orphan')
    training_plans = relationship('TrainingPlan', back_populates='user',
                                 cascade='all, delete-orphan')
    workout_records = relationship('WorkoutRecord', back_populates='user',
                                  cascade='all, delete-orphan')
    body_data = relationship('BodyData', back_populates='user',
                            cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='user',
                           cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='user',
                        cascade='all, delete-orphan')
    
    # 关注关系（作为关注者）
    following = relationship('Follow', foreign_keys='Follow.follower_id',
                           back_populates='follower', cascade='all, delete-orphan')
    # 粉丝关系（作为被关注者）
    followers = relationship('Follow', foreign_keys='Follow.following_id',
                            back_populates='following', cascade='all, delete-orphan')
    
    # 认证相关
    roles = relationship('UserRole', back_populates='user',
                        cascade='all, delete-orphan')
    third_party_accounts = relationship('ThirdPartyAccount', back_populates='user',
                                       cascade='all, delete-orphan')
    refresh_tokens = relationship('RefreshToken', back_populates='user',
                                 cascade='all, delete-orphan')
    password_reset_tokens = relationship('PasswordResetToken', back_populates='user',
                                        cascade='all, delete-orphan')
    login_history = relationship('LoginHistory', back_populates='user',
                                cascade='all, delete-orphan')
    security_logs = relationship('SecurityLog', back_populates='user',
                                cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class UserProfile(BaseModel):
    """用户详细资料表"""
    
    __tablename__ = 'user_profiles'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    unique=True, nullable=False, index=True, comment='用户ID')
    
    # 个人信息
    nickname = Column(String(50), comment='昵称')
    avatar_url = Column(String(255), comment='头像URL')
    gender = Column(Enum(GenderEnum), comment='性别')
    birthday = Column(Date, comment='生日')
    bio = Column(Text, comment='个人简介')
    
    # 身体基础数据
    height = Column(Integer, comment='身高(cm)')
    current_weight = Column(Integer, comment='当前体重(kg)')
    target_weight = Column(Integer, comment='目标体重(kg)')
    
    # 健身目标
    fitness_goal = Column(String(50), comment='健身目标')  # 减脂/增肌/保持/塑形
    fitness_level = Column(String(20), comment='健身水平')  # 新手/中级/高级
    
    # 社交统计
    followers_count = Column(Integer, default=0, comment='粉丝数')
    following_count = Column(Integer, default=0, comment='关注数')
    likes_count = Column(Integer, default=0, comment='获赞数')
    workout_count = Column(Integer, default=0, comment='训练次数')
    
    # 关系映射
    user = relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, nickname={self.nickname})>"


class UserSettings(BaseModel):
    """用户设置表"""
    
    __tablename__ = 'user_settings'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    unique=True, nullable=False, index=True, comment='用户ID')
    
    # 隐私设置
    profile_visible = Column(Boolean, default=True, comment='资料可见性')
    workout_visible = Column(Boolean, default=True, comment='训练记录可见性')
    allow_follow = Column(Boolean, default=True, comment='允许关注')
    allow_message = Column(Boolean, default=True, comment='允许私信')
    
    # 通知设置
    email_notification = Column(Boolean, default=True, comment='邮件通知')
    push_notification = Column(Boolean, default=True, comment='推送通知')
    workout_reminder = Column(Boolean, default=True, comment='训练提醒')
    
    # 偏好设置
    language = Column(String(10), default='zh-CN', comment='语言偏好')
    theme = Column(String(20), default='light', comment='主题')
    weight_unit = Column(String(10), default='kg', comment='体重单位')
    distance_unit = Column(String(10), default='km', comment='距离单位')
    
    # 扩展设置（JSON格式存储其他设置）
    extra_settings = Column(JSON, comment='扩展设置')
    
    # 关系映射
    user = relationship('User', back_populates='settings')
    
    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id})>"
