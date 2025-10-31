"""
运动记录模型
包含训练记录、动作记录、组记录
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class WorkoutRecord(BaseModel):
    """训练记录表"""
    
    __tablename__ = 'workout_records'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    training_plan_id = Column(Integer, ForeignKey('training_plans.id', ondelete='SET NULL'),
                             index=True, comment='训练计划ID')
    
    # 训练基础信息
    workout_date = Column(DateTime, default=datetime.utcnow, nullable=False,
                         index=True, comment='训练日期')
    workout_name = Column(String(100), nullable=False, comment='训练名称')
    workout_type = Column(String(50), comment='训练类型')  # 力量/有氧/混合
    
    # 训练时间
    start_time = Column(DateTime, comment='开始时间')
    end_time = Column(DateTime, comment='结束时间')
    duration = Column(Integer, comment='训练时长(分钟)')
    
    # 训练数据
    total_sets = Column(Integer, default=0, comment='总组数')
    total_reps = Column(Integer, default=0, comment='总次数')
    total_weight = Column(Float, default=0.0, comment='总重量(kg)')
    total_distance = Column(Float, default=0.0, comment='总距离(km)')
    calories_burned = Column(Integer, default=0, comment='消耗卡路里')
    
    # 训练感受
    difficulty_rating = Column(Integer, comment='难度评分(1-10)')
    fatigue_level = Column(Integer, comment='疲劳程度(1-10)')
    mood_rating = Column(Integer, comment='心情评分(1-10)')
    notes = Column(Text, comment='训练笔记')
    
    # 状态标记
    is_completed = Column(Integer, default=False, comment='是否完成')
    completion_rate = Column(Integer, default=0, comment='完成率(%)')
    
    # 位置信息
    location = Column(String(100), comment='训练地点')
    weather = Column(String(50), comment='天气')
    
    # 分享设置
    is_shared = Column(Integer, default=False, index=True, comment='是否分享')
    share_content = Column(JSON, comment='分享内容')
    
    # 统计信息
    likes_count = Column(Integer, default=0, comment='点赞数')
    comments_count = Column(Integer, default=0, comment='评论数')
    
    # 关系映射
    user = relationship('User', back_populates='workout_records')
    training_plan = relationship('TrainingPlan', back_populates='workout_records')
    exercise_records = relationship('ExerciseRecord', back_populates='workout_record',
                                   cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='workout_record',
                        cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='workout_record',
                           cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<WorkoutRecord(id={self.id}, user_id={self.user_id}, date={self.workout_date})>"


class ExerciseRecord(BaseModel):
    """动作记录表"""
    
    __tablename__ = 'exercise_records'
    
    workout_record_id = Column(Integer, ForeignKey('workout_records.id', ondelete='CASCADE'),
                              nullable=False, index=True, comment='训练记录ID')
    exercise_id = Column(Integer, ForeignKey('exercises.id', ondelete='SET NULL'),
                        index=True, comment='动作ID')
    
    # 动作信息（冗余存储，防止删除动作后丢失记录）
    exercise_name = Column(String(100), nullable=False, comment='动作名称')
    muscle_group = Column(String(50), comment='目标肌群')
    exercise_type = Column(String(50), comment='动作类型')
    
    # 完成情况
    order_number = Column(Integer, comment='顺序')
    planned_sets = Column(Integer, comment='计划组数')
    completed_sets = Column(Integer, default=0, comment='完成组数')
    
    # 统计数据
    total_reps = Column(Integer, default=0, comment='总次数')
    total_weight = Column(Float, default=0.0, comment='总重量(kg)')
    total_duration = Column(Integer, default=0, comment='总时长(秒)')
    calories_burned = Column(Integer, default=0, comment='消耗卡路里')
    
    # 个人记录
    max_weight = Column(Float, comment='最大重量(kg)')
    max_reps = Column(Integer, comment='最多次数')
    is_personal_record = Column(Integer, default=False, comment='是否个人记录')
    
    # 备注
    notes = Column(Text, comment='备注')
    
    # 关系映射
    workout_record = relationship('WorkoutRecord', back_populates='exercise_records')
    exercise = relationship('Exercise', back_populates='exercise_records')
    set_records = relationship('SetRecord', back_populates='exercise_record',
                              cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<ExerciseRecord(id={self.id}, exercise_name={self.exercise_name})>"


class SetRecord(BaseModel):
    """组记录表"""
    
    __tablename__ = 'set_records'
    
    exercise_record_id = Column(Integer, ForeignKey('exercise_records.id', ondelete='CASCADE'),
                               nullable=False, index=True, comment='动作记录ID')
    
    # 组信息
    set_number = Column(Integer, nullable=False, comment='组号')
    set_type = Column(String(20), comment='组类型')  # 正常组/热身组/递减组/超级组
    
    # 完成数据
    reps = Column(Integer, comment='次数')
    weight = Column(Float, comment='重量(kg)')
    duration = Column(Integer, comment='持续时间(秒)')
    distance = Column(Float, comment='距离(km)')
    rest_time = Column(Integer, comment='休息时间(秒)')
    
    # 心率数据
    avg_heart_rate = Column(Integer, comment='平均心率')
    max_heart_rate = Column(Integer, comment='最大心率')
    
    # 完成状态
    is_completed = Column(Integer, default=True, comment='是否完成')
    is_failed = Column(Integer, default=False, comment='是否失败')
    
    # 感受评分
    difficulty_rating = Column(Integer, comment='难度评分(1-10)')
    
    # 时间戳
    completed_at = Column(DateTime, default=datetime.utcnow, comment='完成时间')
    
    # 备注
    notes = Column(Text, comment='备注')
    
    # 关系映射
    exercise_record = relationship('ExerciseRecord', back_populates='set_records')
    
    def __repr__(self):
        return f"<SetRecord(id={self.id}, set_number={self.set_number}, reps={self.reps})>"
