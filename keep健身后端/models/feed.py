"""
动态内容模型
包含用户动态、分享、话题标签
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, JSON, Index
from sqlalchemy.orm import relationship
from .base import BaseModel


class Feed(BaseModel):
    """动态内容表"""
    
    __tablename__ = 'feeds'
    __table_args__ = (
        Index('idx_user_created', 'user_id', 'created_at'),
        Index('idx_type_created', 'feed_type', 'created_at'),
        Index('idx_visibility', 'visibility', 'created_at'),
    )
    
    # 用户信息
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='用户ID')
    
    # 动态类型
    feed_type = Column(String(50), nullable=False, comment='动态类型')
    # workout: 训练记录分享
    # achievement: 成就分享
    # milestone: 里程碑
    # photo: 纯图片分享
    # text: 纯文字动态
    # video: 视频分享
    
    # 内容信息
    title = Column(String(200), comment='标题')
    content = Column(Text, comment='动态内容')
    
    # 媒体资源
    images = Column(JSON, comment='图片URL列表')  # ["url1", "url2"]
    video_url = Column(String(500), comment='视频URL')
    thumbnail_url = Column(String(500), comment='视频缩略图')
    
    # 关联内容
    workout_id = Column(Integer, ForeignKey('workout_records.id', ondelete='SET NULL'),
                       comment='关联训练记录ID')
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='SET NULL'),
                      comment='关联课程ID')
    
    # 训练数据摘要（用于展示）
    workout_summary = Column(JSON, comment='训练数据摘要')
    # {
    #     "workout_type": "力量训练",
    #     "duration": 60,
    #     "calories": 300,
    #     "exercises": ["深蹲", "卧推"]
    # }
    
    # 话题标签
    hashtags = Column(JSON, comment='话题标签列表')  # ["增肌", "减脂"]
    
    # 位置信息
    location = Column(String(200), comment='位置')
    location_lat = Column(String(20), comment='纬度')
    location_lng = Column(String(20), comment='经度')
    
    # 可见性设置
    visibility = Column(String(20), default='public', comment='可见性')
    # public: 公开
    # friends: 仅好友
    # private: 仅自己
    
    # 互动权限
    allow_comment = Column(Boolean, default=True, comment='允许评论')
    allow_share = Column(Boolean, default=True, comment='允许分享')
    
    # 统计信息
    likes_count = Column(Integer, default=0, comment='点赞数')
    comments_count = Column(Integer, default=0, comment='评论数')
    shares_count = Column(Integer, default=0, comment='分享数')
    views_count = Column(Integer, default=0, comment='浏览数')
    
    # 状态标记
    is_pinned = Column(Boolean, default=False, comment='是否置顶')
    is_featured = Column(Boolean, default=False, comment='是否精选')
    is_hot = Column(Boolean, default=False, comment='是否热门')
    
    # 审核状态
    status = Column(String(20), default='published', comment='状态')
    # draft: 草稿
    # published: 已发布
    # reviewing: 审核中
    # rejected: 已拒绝
    
    # 关系映射
    user = relationship('User', back_populates='feeds')
    workout_record = relationship('WorkoutRecord', back_populates='feeds')
    likes = relationship('Like', 
                        primaryjoin='and_(foreign(Like.target_id)==Feed.id, Like.target_type=="feed")',
                        viewonly=True)
    comments = relationship('Comment',
                           primaryjoin='and_(foreign(Comment.target_id)==Feed.id, Comment.target_type=="feed")',
                           viewonly=True)
    
    def __repr__(self):
        return f"<Feed(id={self.id}, user_id={self.user_id}, type={self.feed_type})>"


class FeedShare(BaseModel):
    """动态分享记录表"""
    
    __tablename__ = 'feed_shares'
    __table_args__ = (
        Index('idx_user_feed', 'user_id', 'feed_id'),
        Index('idx_feed_created', 'feed_id', 'created_at'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='分享用户ID')
    feed_id = Column(Integer, ForeignKey('feeds.id', ondelete='CASCADE'),
                    nullable=False, comment='原始动态ID')
    
    # 分享内容
    share_comment = Column(Text, comment='分享评论')
    
    # 分享目标
    share_to = Column(String(50), comment='分享目标')  # timeline/group/friend
    
    # 关系映射
    user = relationship('User')
    feed = relationship('Feed')
    
    def __repr__(self):
        return f"<FeedShare(user_id={self.user_id}, feed_id={self.feed_id})>"


class Hashtag(BaseModel):
    """话题标签表"""
    
    __tablename__ = 'hashtags'
    __table_args__ = (
        Index('idx_name', 'name'),
        Index('idx_category', 'category'),
    )
    
    # 标签信息
    name = Column(String(50), unique=True, nullable=False, comment='标签名称')
    description = Column(Text, comment='标签描述')
    
    # 分类
    category = Column(String(50), comment='标签分类')  # training/nutrition/lifestyle
    
    # 图标和封面
    icon = Column(String(500), comment='标签图标')
    cover_image = Column(String(500), comment='封面图片')
    
    # 统计信息
    feeds_count = Column(Integer, default=0, comment='动态数量')
    followers_count = Column(Integer, default=0, comment='关注人数')
    
    # 状态标记
    is_official = Column(Boolean, default=False, comment='是否官方标签')
    is_trending = Column(Boolean, default=False, comment='是否热门')
    
    def __repr__(self):
        return f"<Hashtag(name={self.name})>"


class HashtagFollow(BaseModel):
    """话题关注表"""
    
    __tablename__ = 'hashtag_follows'
    __table_args__ = (
        Index('idx_user_hashtag', 'user_id', 'hashtag_id'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='用户ID')
    hashtag_id = Column(Integer, ForeignKey('hashtags.id', ondelete='CASCADE'),
                       nullable=False, comment='标签ID')
    
    # 关系映射
    user = relationship('User')
    hashtag = relationship('Hashtag')
    
    def __repr__(self):
        return f"<HashtagFollow(user_id={self.user_id}, hashtag_id={self.hashtag_id})>"


class Achievement(BaseModel):
    """成就徽章表"""
    
    __tablename__ = 'achievements'
    
    # 成就信息
    name = Column(String(100), nullable=False, comment='成就名称')
    description = Column(Text, comment='成就描述')
    
    # 成就类型
    achievement_type = Column(String(50), nullable=False, comment='成就类型')
    # workout_count: 训练次数
    # total_duration: 累计时长
    # consistency: 连续打卡
    # weight_milestone: 重量里程碑
    # pr_count: PR次数
    
    # 成就图标
    icon = Column(String(500), comment='成就图标')
    badge_image = Column(String(500), comment='徽章图片')
    
    # 解锁条件
    unlock_condition = Column(JSON, comment='解锁条件')
    # {
    #     "type": "workout_count",
    #     "value": 100,
    #     "period": "all_time"
    # }
    
    # 稀有度
    rarity = Column(String(20), default='common', comment='稀有度')
    # common: 普通
    # rare: 稀有
    # epic: 史诗
    # legendary: 传说
    
    # 积分奖励
    points = Column(Integer, default=0, comment='积分奖励')
    
    # 排序和状态
    sort_order = Column(Integer, default=0, comment='排序')
    is_active = Column(Boolean, default=True, comment='是否启用')
    
    def __repr__(self):
        return f"<Achievement(name={self.name})>"


class UserAchievement(BaseModel):
    """用户成就记录表"""
    
    __tablename__ = 'user_achievements'
    __table_args__ = (
        Index('idx_user_achievement', 'user_id', 'achievement_id'),
        Index('idx_unlocked', 'unlocked_at'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='用户ID')
    achievement_id = Column(Integer, ForeignKey('achievements.id', ondelete='CASCADE'),
                           nullable=False, comment='成就ID')
    
    # 解锁信息
    unlocked_at = Column(Integer, comment='解锁时间戳')
    progress = Column(Integer, default=0, comment='完成进度')
    
    # 是否展示
    is_displayed = Column(Boolean, default=True, comment='是否展示在个人主页')
    
    # 关系映射
    user = relationship('User')
    achievement = relationship('Achievement')
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"
