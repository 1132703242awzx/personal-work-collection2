"""
课程扩展模型
包含分类、标签、学习进度、视频任务等
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Boolean, JSON, DateTime, Float
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class VideoStatusEnum(enum.Enum):
    """视频处理状态"""
    UPLOADING = "uploading"  # 上传中
    UPLOADED = "uploaded"  # 已上传
    PROCESSING = "processing"  # 转码中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败


class CourseCategory(BaseModel):
    """课程分类表"""
    
    __tablename__ = 'course_categories'
    
    name = Column(String(50), nullable=False, unique=True, index=True, comment='分类名称')
    name_en = Column(String(50), comment='英文名称')
    description = Column(Text, comment='分类描述')
    icon = Column(String(255), comment='分类图标')
    cover_image = Column(String(255), comment='封面图片')
    
    # 层级关系
    parent_id = Column(Integer, ForeignKey('course_categories.id', ondelete='CASCADE'),
                      index=True, comment='父分类ID')
    level = Column(Integer, default=1, comment='层级')
    path = Column(String(255), comment='分类路径')
    
    # 显示排序
    order_number = Column(Integer, default=0, index=True, comment='排序号')
    
    # 状态
    is_active = Column(Boolean, default=True, index=True, comment='是否启用')
    is_featured = Column(Boolean, default=False, index=True, comment='是否推荐')
    
    # 统计
    course_count = Column(Integer, default=0, comment='课程数量')
    
    # 关系映射
    parent = relationship('CourseCategory', remote_side='CourseCategory.id',
                         backref='children')
    
    def __repr__(self):
        return f"<CourseCategory(id={self.id}, name={self.name})>"


class CourseTag(BaseModel):
    """课程标签表"""
    
    __tablename__ = 'course_tags'
    
    name = Column(String(50), nullable=False, unique=True, index=True, comment='标签名称')
    name_en = Column(String(50), comment='英文名称')
    description = Column(Text, comment='标签描述')
    color = Column(String(20), comment='标签颜色')
    
    # 标签类型
    tag_type = Column(String(20), default='general', index=True, 
                     comment='标签类型(general/level/body_part/goal)')
    
    # 显示排序
    order_number = Column(Integer, default=0, index=True, comment='排序号')
    
    # 状态
    is_active = Column(Boolean, default=True, index=True, comment='是否启用')
    
    # 统计
    course_count = Column(Integer, default=0, comment='使用次数')
    
    def __repr__(self):
        return f"<CourseTag(id={self.id}, name={self.name})>"


class CourseTagRelation(BaseModel):
    """课程标签关系表"""
    
    __tablename__ = 'course_tag_relations'
    
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'),
                      nullable=False, index=True, comment='课程ID')
    tag_id = Column(Integer, ForeignKey('course_tags.id', ondelete='CASCADE'),
                   nullable=False, index=True, comment='标签ID')
    
    def __repr__(self):
        return f"<CourseTagRelation(course_id={self.course_id}, tag_id={self.tag_id})>"


class VideoUploadTask(BaseModel):
    """视频上传任务表"""
    
    __tablename__ = 'video_upload_tasks'
    
    # 任务信息
    task_id = Column(String(100), unique=True, index=True, comment='Celery任务ID')
    user_id = Column(Integer, nullable=False, index=True, comment='用户ID')
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'),
                      index=True, comment='课程ID')
    chapter_id = Column(Integer, ForeignKey('chapters.id', ondelete='CASCADE'),
                       index=True, comment='章节ID')
    video_id = Column(Integer, ForeignKey('videos.id', ondelete='SET NULL'),
                     index=True, comment='视频ID')
    
    # 文件信息
    original_filename = Column(String(255), nullable=False, comment='原始文件名')
    file_path = Column(String(500), comment='文件路径')
    file_size = Column(Integer, comment='文件大小(字节)')
    file_md5 = Column(String(32), index=True, comment='文件MD5')
    
    # 上传信息
    chunk_size = Column(Integer, comment='分片大小')
    total_chunks = Column(Integer, comment='总分片数')
    uploaded_chunks = Column(Integer, default=0, comment='已上传分片数')
    
    # 处理状态
    status = Column(Enum(VideoStatusEnum), default=VideoStatusEnum.UPLOADING,
                   nullable=False, index=True, comment='状态')
    progress = Column(Integer, default=0, comment='进度百分比')
    error_message = Column(Text, comment='错误信息')
    
    # 转码信息
    transcode_started_at = Column(DateTime, comment='转码开始时间')
    transcode_completed_at = Column(DateTime, comment='转码完成时间')
    output_formats = Column(JSON, comment='输出格式')
    
    def __repr__(self):
        return f"<VideoUploadTask(id={self.id}, status={self.status}, progress={self.progress})>"


class VideoTranscodeJob(BaseModel):
    """视频转码任务表"""
    
    __tablename__ = 'video_transcode_jobs'
    
    # 任务信息
    task_id = Column(String(100), unique=True, index=True, comment='Celery任务ID')
    upload_task_id = Column(Integer, ForeignKey('video_upload_tasks.id', ondelete='CASCADE'),
                           index=True, comment='上传任务ID')
    video_id = Column(Integer, ForeignKey('videos.id', ondelete='CASCADE'),
                     index=True, comment='视频ID')
    
    # 输入信息
    input_file = Column(String(500), nullable=False, comment='输入文件路径')
    input_format = Column(String(20), comment='输入格式')
    input_duration = Column(Integer, comment='输入时长(秒)')
    input_resolution = Column(String(20), comment='输入分辨率')
    input_bitrate = Column(Integer, comment='输入码率')
    
    # 输出信息
    output_quality = Column(String(20), nullable=False, comment='输出清晰度(sd/hd/fhd/4k)')
    output_file = Column(String(500), comment='输出文件路径')
    output_format = Column(String(20), default='mp4', comment='输出格式')
    output_resolution = Column(String(20), comment='输出分辨率')
    output_bitrate = Column(Integer, comment='输出码率')
    output_size = Column(Integer, comment='输出大小(字节)')
    
    # 处理状态
    status = Column(Enum(VideoStatusEnum), default=VideoStatusEnum.PROCESSING,
                   nullable=False, index=True, comment='状态')
    progress = Column(Integer, default=0, comment='进度百分比')
    error_message = Column(Text, comment='错误信息')
    
    # 时间统计
    started_at = Column(DateTime, comment='开始时间')
    completed_at = Column(DateTime, comment='完成时间')
    processing_time = Column(Integer, comment='处理耗时(秒)')
    
    def __repr__(self):
        return f"<VideoTranscodeJob(id={self.id}, quality={self.output_quality}, status={self.status})>"


class LearningProgress(BaseModel):
    """学习进度表"""
    
    __tablename__ = 'learning_progress'
    
    user_id = Column(Integer, nullable=False, index=True, comment='用户ID')
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'),
                      nullable=False, index=True, comment='课程ID')
    
    # 进度信息
    total_videos = Column(Integer, default=0, comment='总视频数')
    watched_videos = Column(Integer, default=0, comment='已观看视频数')
    completed_videos = Column(Integer, default=0, comment='已完成视频数')
    completion_rate = Column(Float, default=0.0, comment='完成率')
    
    # 时间统计
    total_watch_time = Column(Integer, default=0, comment='总观看时长(秒)')
    last_watch_video_id = Column(Integer, comment='最后观看视频ID')
    last_watch_position = Column(Integer, default=0, comment='最后观看位置(秒)')
    last_watched_at = Column(DateTime, index=True, comment='最后观看时间')
    
    # 状态标记
    is_enrolled = Column(Boolean, default=True, index=True, comment='是否已报名')
    is_completed = Column(Boolean, default=False, index=True, comment='是否已完成')
    completed_at = Column(DateTime, comment='完成时间')
    
    # 评分
    rating = Column(Integer, comment='用户评分(1-5)')
    review = Column(Text, comment='用户评价')
    rated_at = Column(DateTime, comment='评分时间')
    
    def __repr__(self):
        return f"<LearningProgress(user_id={self.user_id}, course_id={self.course_id}, rate={self.completion_rate})>"


class VideoWatchRecord(BaseModel):
    """视频观看记录表"""
    
    __tablename__ = 'video_watch_records'
    
    user_id = Column(Integer, nullable=False, index=True, comment='用户ID')
    video_id = Column(Integer, ForeignKey('videos.id', ondelete='CASCADE'),
                     nullable=False, index=True, comment='视频ID')
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'),
                      nullable=False, index=True, comment='课程ID')
    
    # 观看信息
    watch_duration = Column(Integer, default=0, comment='观看时长(秒)')
    last_position = Column(Integer, default=0, comment='最后播放位置(秒)')
    watch_percentage = Column(Float, default=0.0, comment='观看百分比')
    
    # 状态标记
    is_completed = Column(Boolean, default=False, index=True, comment='是否完成')
    completed_at = Column(DateTime, comment='完成时间')
    
    # 设备信息
    device_type = Column(String(20), comment='设备类型')
    platform = Column(String(20), comment='平台')
    ip_address = Column(String(50), comment='IP地址')
    
    # 播放质量
    quality_played = Column(String(20), comment='播放清晰度')
    
    def __repr__(self):
        return f"<VideoWatchRecord(user_id={self.user_id}, video_id={self.video_id})>"


class CourseEnrollment(BaseModel):
    """课程报名表"""
    
    __tablename__ = 'course_enrollments'
    
    user_id = Column(Integer, nullable=False, index=True, comment='用户ID')
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'),
                      nullable=False, index=True, comment='课程ID')
    
    # 报名信息
    enrollment_type = Column(String(20), default='free', comment='报名类型(free/paid/trial)')
    price_paid = Column(Integer, default=0, comment='支付价格(分)')
    order_id = Column(String(100), index=True, comment='订单ID')
    
    # 有效期
    valid_from = Column(DateTime, comment='有效开始时间')
    valid_until = Column(DateTime, index=True, comment='有效结束时间')
    is_lifetime = Column(Boolean, default=False, comment='是否永久有效')
    
    # 状态
    is_active = Column(Boolean, default=True, index=True, comment='是否激活')
    canceled_at = Column(DateTime, comment='取消时间')
    cancel_reason = Column(Text, comment='取消原因')
    
    def __repr__(self):
        return f"<CourseEnrollment(user_id={self.user_id}, course_id={self.course_id})>"


class VideoPlayStatistics(BaseModel):
    """视频播放统计表"""
    
    __tablename__ = 'video_play_statistics'
    
    video_id = Column(Integer, ForeignKey('videos.id', ondelete='CASCADE'),
                     nullable=False, index=True, comment='视频ID')
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'),
                      nullable=False, index=True, comment='课程ID')
    
    # 日期统计
    stat_date = Column(DateTime, nullable=False, index=True, comment='统计日期')
    
    # 播放统计
    play_count = Column(Integer, default=0, comment='播放次数')
    unique_viewers = Column(Integer, default=0, comment='独立观众数')
    completion_count = Column(Integer, default=0, comment='完成次数')
    completion_rate = Column(Float, default=0.0, comment='完成率')
    
    # 时长统计
    total_watch_time = Column(Integer, default=0, comment='总观看时长(秒)')
    avg_watch_time = Column(Integer, default=0, comment='平均观看时长(秒)')
    avg_watch_percentage = Column(Float, default=0.0, comment='平均观看百分比')
    
    # 质量统计
    sd_plays = Column(Integer, default=0, comment='标清播放次数')
    hd_plays = Column(Integer, default=0, comment='高清播放次数')
    fhd_plays = Column(Integer, default=0, comment='超清播放次数')
    
    # 设备统计
    mobile_plays = Column(Integer, default=0, comment='移动端播放')
    desktop_plays = Column(Integer, default=0, comment='桌面端播放')
    tablet_plays = Column(Integer, default=0, comment='平板播放')
    
    def __repr__(self):
        return f"<VideoPlayStatistics(video_id={self.video_id}, date={self.stat_date})>"
