"""
课程体系模型
包含课程、章节、视频
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class CourseTypeEnum(enum.Enum):
    """课程类型枚举"""
    VIDEO = "video"  # 视频课程
    LIVE = "live"  # 直播课程
    ARTICLE = "article"  # 图文课程


class CourseLevelEnum(enum.Enum):
    """课程级别枚举"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(BaseModel):
    """课程表"""
    
    __tablename__ = 'courses'
    
    # 课程基础信息
    title = Column(String(200), nullable=False, index=True, comment='课程标题')
    subtitle = Column(String(200), comment='副标题')
    description = Column(Text, comment='课程描述')
    cover_image = Column(String(255), comment='封面图片')
    promo_video = Column(String(255), comment='宣传视频')
    
    # 课程分类
    course_type = Column(Enum(CourseTypeEnum), nullable=False, 
                        index=True, comment='课程类型')
    category = Column(String(50), nullable=False, index=True, comment='课程分类')
    tags = Column(JSON, comment='标签')
    
    # 难度和目标
    level = Column(Enum(CourseLevelEnum), nullable=False, comment='课程级别')
    target_audience = Column(String(100), comment='目标人群')
    learning_objectives = Column(JSON, comment='学习目标')
    
    # 讲师信息
    instructor_id = Column(Integer, comment='讲师ID')
    instructor_name = Column(String(50), comment='讲师名称')
    instructor_bio = Column(Text, comment='讲师简介')
    instructor_avatar = Column(String(255), comment='讲师头像')
    
    # 课程内容
    chapter_count = Column(Integer, default=0, comment='章节数')
    video_count = Column(Integer, default=0, comment='视频数')
    total_duration = Column(Integer, default=0, comment='总时长(分钟)')
    
    # 价格和访问
    price = Column(Integer, default=0, comment='价格(分)')
    original_price = Column(Integer, comment='原价(分)')
    is_free = Column(Boolean, default=False, index=True, comment='是否免费')
    is_premium_only = Column(Boolean, default=False, index=True, comment='仅限会员')
    
    # 状态标记
    is_published = Column(Boolean, default=False, index=True, comment='是否发布')
    is_featured = Column(Boolean, default=False, index=True, comment='是否推荐')
    
    # 统计信息
    view_count = Column(Integer, default=0, comment='观看次数')
    enrollment_count = Column(Integer, default=0, comment='报名人数')
    completion_count = Column(Integer, default=0, comment='完成人数')
    rating_average = Column(Integer, default=0, comment='平均评分')
    rating_count = Column(Integer, default=0, comment='评分人数')
    
    # 推荐权重
    popularity_score = Column(Integer, default=0, index=True, comment='热度分数')
    quality_score = Column(Integer, default=0, comment='质量分数')
    
    # 关系映射
    chapters = relationship('Chapter', back_populates='course',
                          cascade='all, delete-orphan', order_by='Chapter.order_number')
    
    def __repr__(self):
        return f"<Course(id={self.id}, title={self.title}, type={self.course_type})>"


class Chapter(BaseModel):
    """章节表"""
    
    __tablename__ = 'chapters'
    
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'),
                      nullable=False, index=True, comment='课程ID')
    
    # 章节信息
    title = Column(String(200), nullable=False, comment='章节标题')
    description = Column(Text, comment='章节描述')
    order_number = Column(Integer, nullable=False, comment='排序号')
    
    # 章节内容
    video_count = Column(Integer, default=0, comment='视频数')
    total_duration = Column(Integer, default=0, comment='总时长(分钟)')
    
    # 访问控制
    is_free = Column(Boolean, default=False, comment='是否免费')
    is_locked = Column(Boolean, default=False, comment='是否锁定')
    unlock_condition = Column(JSON, comment='解锁条件')
    
    # 状态
    is_published = Column(Boolean, default=False, comment='是否发布')
    
    # 关系映射
    course = relationship('Course', back_populates='chapters')
    videos = relationship('Video', back_populates='chapter',
                         cascade='all, delete-orphan', order_by='Video.order_number')
    
    def __repr__(self):
        return f"<Chapter(id={self.id}, title={self.title}, course_id={self.course_id})>"


class Video(BaseModel):
    """视频表"""
    
    __tablename__ = 'videos'
    
    chapter_id = Column(Integer, ForeignKey('chapters.id', ondelete='CASCADE'),
                       nullable=False, index=True, comment='章节ID')
    
    # 视频信息
    title = Column(String(200), nullable=False, comment='视频标题')
    description = Column(Text, comment='视频描述')
    cover_image = Column(String(255), comment='封面图片')
    order_number = Column(Integer, nullable=False, comment='排序号')
    
    # 视频资源
    video_url = Column(String(255), nullable=False, comment='视频URL')
    video_quality = Column(JSON, comment='视频清晰度')  # {sd, hd, fhd}
    duration = Column(Integer, nullable=False, comment='时长(秒)')
    file_size = Column(Integer, comment='文件大小(字节)')
    
    # 字幕和资源
    subtitles = Column(JSON, comment='字幕')
    attachments = Column(JSON, comment='附件')
    
    # 访问控制
    is_free = Column(Boolean, default=False, comment='是否免费')
    is_trial = Column(Boolean, default=False, comment='是否试看')
    trial_duration = Column(Integer, comment='试看时长(秒)')
    
    # 状态
    is_published = Column(Boolean, default=False, comment='是否发布')
    
    # 统计信息
    view_count = Column(Integer, default=0, comment='观看次数')
    completion_count = Column(Integer, default=0, comment='完成次数')
    avg_watch_duration = Column(Integer, default=0, comment='平均观看时长(秒)')
    
    # 互动数据
    likes_count = Column(Integer, default=0, comment='点赞数')
    comments_count = Column(Integer, default=0, comment='评论数')
    
    # 关系映射
    chapter = relationship('Chapter', back_populates='videos')
    
    def __repr__(self):
        return f"<Video(id={self.id}, title={self.title}, duration={self.duration})>"
