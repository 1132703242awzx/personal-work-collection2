"""
社交互动模型
包含关注、点赞、评论
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from .base import BaseModel


class Follow(BaseModel):
    """关注关系表"""
    
    __tablename__ = 'follows'
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='uk_follower_following'),
        Index('idx_follower_created', 'follower_id', 'created_at'),
        Index('idx_following_created', 'following_id', 'created_at'),
    )
    
    # 关注关系
    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False, comment='关注者ID')
    following_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                         nullable=False, comment='被关注者ID')
    
    # 关系状态
    is_mutual = Column(Boolean, default=False, comment='是否互关')
    is_blocked = Column(Boolean, default=False, comment='是否拉黑')
    is_muted = Column(Boolean, default=False, comment='是否静音')
    
    # 分组标签
    group_tag = Column(String(50), comment='分组标签')
    
    # 备注
    remark = Column(String(100), comment='备注名')
    
    # 关系映射
    follower = relationship('User', foreign_keys=[follower_id], back_populates='following')
    following = relationship('User', foreign_keys=[following_id], back_populates='followers')
    
    def __repr__(self):
        return f"<Follow(follower_id={self.follower_id}, following_id={self.following_id})>"


class Like(BaseModel):
    """点赞表"""
    
    __tablename__ = 'likes'
    __table_args__ = (
        Index('idx_user_target', 'user_id', 'target_type', 'target_id'),
        Index('idx_target', 'target_type', 'target_id', 'created_at'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    
    # 点赞目标（多态关联）
    target_type = Column(String(50), nullable=False, comment='目标类型')  # workout/comment/course
    target_id = Column(Integer, nullable=False, comment='目标ID')
    
    # 点赞状态
    is_active = Column(Boolean, default=True, comment='是否有效')
    
    # 关系映射
    user = relationship('User', back_populates='likes')
    workout_record = relationship('WorkoutRecord', back_populates='likes',
                                 foreign_keys='[Like.target_id]',
                                 primaryjoin='and_(Like.target_id==WorkoutRecord.id, Like.target_type=="workout")',
                                 viewonly=True)
    
    def __repr__(self):
        return f"<Like(user_id={self.user_id}, target_type={self.target_type}, target_id={self.target_id})>"


class Comment(BaseModel):
    """评论表"""
    
    __tablename__ = 'comments'
    __table_args__ = (
        Index('idx_target', 'target_type', 'target_id', 'created_at'),
        Index('idx_user_created', 'user_id', 'created_at'),
        Index('idx_parent', 'parent_id', 'created_at'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='用户ID')
    
    # 评论目标（多态关联）
    target_type = Column(String(50), nullable=False, comment='目标类型')  # workout/course/video
    target_id = Column(Integer, nullable=False, comment='目标ID')
    
    # 评论内容
    content = Column(Text, nullable=False, comment='评论内容')
    
    # 回复关系
    parent_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'),
                      comment='父评论ID')
    reply_to_user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'),
                             comment='回复目标用户ID')
    
    # 评论层级
    level = Column(Integer, default=0, comment='评论层级')  # 0:一级评论, 1:二级回复
    root_comment_id = Column(Integer, comment='根评论ID')
    
    # 富文本相关
    mentions = Column(String(500), comment='@提及的用户ID列表')  # 逗号分隔
    images = Column(Text, comment='图片URL列表')  # JSON格式
    
    # 状态标记
    is_pinned = Column(Boolean, default=False, comment='是否置顶')
    is_hot = Column(Boolean, default=False, comment='是否热门')
    is_author = Column(Boolean, default=False, comment='是否作者评论')
    
    # 审核状态
    is_approved = Column(Boolean, default=True, comment='是否审核通过')
    is_hidden = Column(Boolean, default=False, comment='是否隐藏')
    
    # 统计信息
    likes_count = Column(Integer, default=0, comment='点赞数')
    replies_count = Column(Integer, default=0, comment='回复数')
    
    # 关系映射
    user = relationship('User', foreign_keys=[user_id], back_populates='comments')
    reply_to_user = relationship('User', foreign_keys=[reply_to_user_id])
    parent_comment = relationship('Comment', remote_side='Comment.id',
                                 backref='replies')
    workout_record = relationship('WorkoutRecord', back_populates='comments',
                                 foreign_keys='[Comment.target_id]',
                                 primaryjoin='and_(Comment.target_id==WorkoutRecord.id, Comment.target_type=="workout")',
                                 viewonly=True)
    
    def __repr__(self):
        return f"<Comment(id={self.id}, user_id={self.user_id}, target_type={self.target_type})>"
