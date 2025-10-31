"""
通知系统模型
包含系统通知、消息提醒
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, JSON, Index
from sqlalchemy.orm import relationship
from .base import BaseModel


class Notification(BaseModel):
    """通知表"""
    
    __tablename__ = 'notifications'
    __table_args__ = (
        Index('idx_user_created', 'user_id', 'created_at'),
        Index('idx_user_read', 'user_id', 'is_read', 'created_at'),
        Index('idx_type', 'notification_type', 'created_at'),
    )
    
    # 接收者
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='接收用户ID')
    
    # 发送者
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'),
                      comment='发送者ID')
    
    # 通知类型
    notification_type = Column(String(50), nullable=False, comment='通知类型')
    # follow: 新关注
    # like: 点赞
    # comment: 评论
    # reply: 回复
    # mention: @提及
    # share: 分享
    # achievement: 成就解锁
    # system: 系统通知
    # workout_reminder: 训练提醒
    # milestone: 里程碑
    
    # 通知内容
    title = Column(String(200), nullable=False, comment='通知标题')
    content = Column(Text, comment='通知内容')
    
    # 关联对象
    target_type = Column(String(50), comment='目标类型')  # feed/comment/workout
    target_id = Column(Integer, comment='目标ID')
    
    # 额外数据
    extra_data = Column(JSON, comment='额外数据')
    # {
    #     "workout_type": "力量训练",
    #     "exercise_name": "深蹲",
    #     "feed_image": "url"
    # }
    
    # 跳转链接
    action_url = Column(String(500), comment='操作链接')
    
    # 状态
    is_read = Column(Boolean, default=False, comment='是否已读')
    read_at = Column(Integer, comment='阅读时间戳')
    
    # 推送状态
    is_pushed = Column(Boolean, default=False, comment='是否已推送')
    push_status = Column(String(20), comment='推送状态')  # pending/sent/failed
    
    # 关系映射
    user = relationship('User', foreign_keys=[user_id], back_populates='notifications')
    sender = relationship('User', foreign_keys=[sender_id])
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type})>"


class NotificationSetting(BaseModel):
    """通知设置表"""
    
    __tablename__ = 'notification_settings'
    __table_args__ = (
        Index('idx_user', 'user_id'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    unique=True, nullable=False, comment='用户ID')
    
    # 关注通知
    follow_enabled = Column(Boolean, default=True, comment='关注通知')
    
    # 互动通知
    like_enabled = Column(Boolean, default=True, comment='点赞通知')
    comment_enabled = Column(Boolean, default=True, comment='评论通知')
    reply_enabled = Column(Boolean, default=True, comment='回复通知')
    mention_enabled = Column(Boolean, default=True, comment='@提及通知')
    
    # 训练通知
    workout_reminder_enabled = Column(Boolean, default=True, comment='训练提醒')
    milestone_enabled = Column(Boolean, default=True, comment='里程碑通知')
    achievement_enabled = Column(Boolean, default=True, comment='成就通知')
    
    # 系统通知
    system_enabled = Column(Boolean, default=True, comment='系统通知')
    
    # 推送设置
    push_enabled = Column(Boolean, default=True, comment='推送通知总开关')
    quiet_start_time = Column(String(5), comment='免打扰开始时间')  # "22:00"
    quiet_end_time = Column(String(5), comment='免打扰结束时间')  # "08:00"
    
    # 关系映射
    user = relationship('User', back_populates='notification_setting')
    
    def __repr__(self):
        return f"<NotificationSetting(user_id={self.user_id})>"


class Message(BaseModel):
    """私信表"""
    
    __tablename__ = 'messages'
    __table_args__ = (
        Index('idx_sender_receiver', 'sender_id', 'receiver_id', 'created_at'),
        Index('idx_receiver_read', 'receiver_id', 'is_read', 'created_at'),
        Index('idx_conversation', 'conversation_id', 'created_at'),
    )
    
    # 会话ID（用于快速查询对话）
    conversation_id = Column(String(100), nullable=False, comment='会话ID')
    # 格式: "user_id1_user_id2" (小ID在前)
    
    # 发送者和接收者
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                      nullable=False, comment='发送者ID')
    receiver_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False, comment='接收者ID')
    
    # 消息类型
    message_type = Column(String(20), default='text', comment='消息类型')
    # text: 文本
    # image: 图片
    # workout: 训练记录分享
    # feed: 动态分享
    
    # 消息内容
    content = Column(Text, comment='消息内容')
    
    # 媒体资源
    image_url = Column(String(500), comment='图片URL')
    
    # 关联内容
    workout_id = Column(Integer, ForeignKey('workout_records.id', ondelete='SET NULL'),
                       comment='关联训练记录')
    feed_id = Column(Integer, ForeignKey('feeds.id', ondelete='SET NULL'),
                    comment='关联动态')
    
    # 状态
    is_read = Column(Boolean, default=False, comment='是否已读')
    read_at = Column(Integer, comment='阅读时间戳')
    
    is_recalled = Column(Boolean, default=False, comment='是否已撤回')
    recalled_at = Column(Integer, comment='撤回时间戳')
    
    # 关系映射
    sender = relationship('User', foreign_keys=[sender_id])
    receiver = relationship('User', foreign_keys=[receiver_id])
    workout_record = relationship('WorkoutRecord')
    feed = relationship('Feed')
    
    def __repr__(self):
        return f"<Message(id={self.id}, sender_id={self.sender_id}, receiver_id={self.receiver_id})>"


class Conversation(BaseModel):
    """会话表"""
    
    __tablename__ = 'conversations'
    __table_args__ = (
        Index('idx_user1_user2', 'user1_id', 'user2_id'),
    )
    
    # 参与者
    user1_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False, comment='用户1 ID')
    user2_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False, comment='用户2 ID')
    
    # 会话ID
    conversation_id = Column(String(100), unique=True, nullable=False, comment='会话ID')
    
    # 最后消息
    last_message_id = Column(Integer, ForeignKey('messages.id', ondelete='SET NULL'),
                            comment='最后一条消息ID')
    last_message_content = Column(String(200), comment='最后消息内容')
    last_message_at = Column(Integer, comment='最后消息时间戳')
    
    # 未读数
    user1_unread_count = Column(Integer, default=0, comment='用户1未读数')
    user2_unread_count = Column(Integer, default=0, comment='用户2未读数')
    
    # 是否删除（对于某一方）
    user1_deleted = Column(Boolean, default=False, comment='用户1是否删除')
    user2_deleted = Column(Boolean, default=False, comment='用户2是否删除')
    
    # 关系映射
    user1 = relationship('User', foreign_keys=[user1_id])
    user2 = relationship('User', foreign_keys=[user2_id])
    last_message = relationship('Message', foreign_keys=[last_message_id])
    
    def __repr__(self):
        return f"<Conversation(id={self.conversation_id})>"
