"""
认证和权限相关模型
包含用户角色、第三方账号、密码重置等
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel
import enum


class UserRoleEnum(enum.Enum):
    """用户角色枚举"""
    USER = "user"  # 普通用户
    COACH = "coach"  # 教练
    ADMIN = "admin"  # 管理员
    SUPER_ADMIN = "super_admin"  # 超级管理员


class ThirdPartyProviderEnum(enum.Enum):
    """第三方登录平台枚举"""
    WECHAT = "wechat"  # 微信
    APPLE = "apple"  # Apple
    GOOGLE = "google"  # Google
    FACEBOOK = "facebook"  # Facebook


class TokenTypeEnum(enum.Enum):
    """Token类型枚举"""
    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFY = "email_verify"


class UserRole(BaseModel):
    """用户角色表"""
    
    __tablename__ = 'user_roles'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    role = Column(Enum(UserRoleEnum), nullable=False, 
                 default=UserRoleEnum.USER, index=True, comment='角色')
    
    # 教练相关信息（仅当role=COACH时有效）
    coach_cert_number = Column(String(100), comment='教练证书编号')
    coach_level = Column(String(50), comment='教练级别')
    coach_specialties = Column(String(255), comment='专长领域')
    verified_at = Column(DateTime, comment='认证时间')
    
    # 管理员相关
    permissions = Column(Text, comment='权限列表（JSON）')
    
    # 关系映射
    user = relationship('User', back_populates='roles')
    
    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role={self.role})>"


class ThirdPartyAccount(BaseModel):
    """第三方账号绑定表"""
    
    __tablename__ = 'third_party_accounts'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    
    # 第三方平台信息
    provider = Column(Enum(ThirdPartyProviderEnum), nullable=False,
                     index=True, comment='第三方平台')
    provider_user_id = Column(String(255), nullable=False, 
                             index=True, comment='第三方用户ID')
    provider_username = Column(String(100), comment='第三方用户名')
    
    # 授权信息
    access_token = Column(String(500), comment='访问令牌')
    refresh_token = Column(String(500), comment='刷新令牌')
    expires_at = Column(DateTime, comment='令牌过期时间')
    
    # 用户信息（来自第三方）
    nickname = Column(String(100), comment='昵称')
    avatar_url = Column(String(255), comment='头像')
    email = Column(String(100), comment='邮箱')
    phone = Column(String(20), comment='手机号')
    
    # 额外信息
    extra_data = Column(Text, comment='额外数据（JSON）')
    
    # 状态
    is_bound = Column(Boolean, default=True, nullable=False, comment='是否绑定')
    last_login_at = Column(DateTime, comment='最后登录时间')
    
    # 关系映射
    user = relationship('User', back_populates='third_party_accounts')
    
    def __repr__(self):
        return f"<ThirdPartyAccount(user_id={self.user_id}, provider={self.provider})>"


class RefreshToken(BaseModel):
    """刷新令牌表"""
    
    __tablename__ = 'refresh_tokens'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    
    # Token信息
    token = Column(String(500), nullable=False, unique=True, 
                  index=True, comment='刷新令牌')
    token_type = Column(Enum(TokenTypeEnum), default=TokenTypeEnum.REFRESH,
                       nullable=False, comment='令牌类型')
    
    # 过期信息
    expires_at = Column(DateTime, nullable=False, 
                       index=True, comment='过期时间')
    
    # 设备信息
    device_id = Column(String(255), comment='设备ID')
    device_type = Column(String(50), comment='设备类型')  # iOS/Android/Web
    device_name = Column(String(100), comment='设备名称')
    ip_address = Column(String(50), comment='IP地址')
    user_agent = Column(String(500), comment='User Agent')
    
    # 状态
    is_revoked = Column(Boolean, default=False, nullable=False,
                       index=True, comment='是否已撤销')
    revoked_at = Column(DateTime, comment='撤销时间')
    
    # 使用记录
    last_used_at = Column(DateTime, comment='最后使用时间')
    use_count = Column(Integer, default=0, comment='使用次数')
    
    # 关系映射
    user = relationship('User', back_populates='refresh_tokens')
    
    def __repr__(self):
        return f"<RefreshToken(user_id={self.user_id}, token={self.token[:20]}...)>"


class PasswordResetToken(BaseModel):
    """密码重置令牌表"""
    
    __tablename__ = 'password_reset_tokens'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    
    # Token信息
    token = Column(String(500), nullable=False, unique=True,
                  index=True, comment='重置令牌')
    
    # 验证码（短信/邮箱）
    verification_code = Column(String(10), comment='验证码')
    verification_type = Column(String(20), comment='验证方式')  # sms/email
    
    # 过期信息
    expires_at = Column(DateTime, nullable=False,
                       index=True, comment='过期时间')
    
    # 使用状态
    is_used = Column(Boolean, default=False, nullable=False,
                    index=True, comment='是否已使用')
    used_at = Column(DateTime, comment='使用时间')
    
    # 请求信息
    ip_address = Column(String(50), comment='请求IP')
    user_agent = Column(String(500), comment='User Agent')
    
    # 关系映射
    user = relationship('User', back_populates='password_reset_tokens')
    
    def __repr__(self):
        return f"<PasswordResetToken(user_id={self.user_id}, is_used={self.is_used})>"


class LoginHistory(BaseModel):
    """登录历史记录表"""
    
    __tablename__ = 'login_history'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    
    # 登录方式
    login_type = Column(String(50), nullable=False, comment='登录方式')  # password/wechat/apple
    
    # 登录结果
    is_success = Column(Boolean, nullable=False, index=True, comment='是否成功')
    fail_reason = Column(String(255), comment='失败原因')
    
    # 设备信息
    device_id = Column(String(255), comment='设备ID')
    device_type = Column(String(50), comment='设备类型')
    device_name = Column(String(100), comment='设备名称')
    os_version = Column(String(50), comment='操作系统版本')
    app_version = Column(String(50), comment='应用版本')
    
    # 网络信息
    ip_address = Column(String(50), index=True, comment='IP地址')
    location = Column(String(200), comment='地理位置')
    user_agent = Column(String(500), comment='User Agent')
    
    # 时间戳
    login_at = Column(DateTime, default=datetime.utcnow, 
                     nullable=False, index=True, comment='登录时间')
    logout_at = Column(DateTime, comment='登出时间')
    
    # 关系映射
    user = relationship('User', back_populates='login_history')
    
    def __repr__(self):
        return f"<LoginHistory(user_id={self.user_id}, login_at={self.login_at})>"


class SecurityLog(BaseModel):
    """安全日志表"""
    
    __tablename__ = 'security_logs'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    index=True, comment='用户ID')
    
    # 事件信息
    event_type = Column(String(50), nullable=False, 
                       index=True, comment='事件类型')  # password_change/email_change/phone_change
    event_description = Column(Text, comment='事件描述')
    
    # 操作信息
    ip_address = Column(String(50), comment='IP地址')
    user_agent = Column(String(500), comment='User Agent')
    
    # 结果
    is_success = Column(Boolean, nullable=False, comment='是否成功')
    error_message = Column(String(500), comment='错误信息')
    
    # 额外数据
    extra_data = Column(Text, comment='额外数据（JSON）')
    
    # 关系映射
    user = relationship('User', back_populates='security_logs')
    
    def __repr__(self):
        return f"<SecurityLog(user_id={self.user_id}, event_type={self.event_type})>"
