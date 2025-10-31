"""
训练计划模型
包含训练计划、计划天数、运动动作
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class DifficultyEnum(enum.Enum):
    """难度等级枚举"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MuscleGroupEnum(enum.Enum):
    """目标肌群枚举"""
    CHEST = "chest"  # 胸部
    BACK = "back"  # 背部
    SHOULDERS = "shoulders"  # 肩部
    ARMS = "arms"  # 手臂
    LEGS = "legs"  # 腿部
    CORE = "core"  # 核心
    CARDIO = "cardio"  # 有氧
    FULL_BODY = "full_body"  # 全身


class TrainingPlan(BaseModel):
    """训练计划表"""
    
    __tablename__ = 'training_plans'
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, index=True, comment='用户ID')
    
    # 计划基础信息
    name = Column(String(100), nullable=False, comment='计划名称')
    description = Column(Text, comment='计划描述')
    cover_image = Column(String(255), comment='封面图片')
    
    # 计划属性
    difficulty = Column(Enum(DifficultyEnum), nullable=False, comment='难度等级')
    duration_weeks = Column(Integer, nullable=False, comment='计划周期(周)')
    days_per_week = Column(Integer, nullable=False, comment='每周训练天数')
    
    # 目标设置
    goal = Column(String(50), comment='训练目标')  # 减脂/增肌/塑形/体能
    target_muscle_group = Column(Enum(MuscleGroupEnum), comment='主要目标肌群')
    
    # 状态标记
    is_active = Column(Boolean, default=False, comment='是否激活')
    is_template = Column(Boolean, default=False, index=True, comment='是否为模板')
    is_public = Column(Boolean, default=False, index=True, comment='是否公开')
    
    # 统计信息
    usage_count = Column(Integer, default=0, comment='使用次数')
    completion_rate = Column(Integer, default=0, comment='完成率')
    
    # 关系映射
    user = relationship('User', back_populates='training_plans')
    plan_days = relationship('PlanDay', back_populates='training_plan',
                            cascade='all, delete-orphan', order_by='PlanDay.day_number')
    workout_records = relationship('WorkoutRecord', back_populates='training_plan')
    
    def __repr__(self):
        return f"<TrainingPlan(id={self.id}, name={self.name}, user_id={self.user_id})>"


class PlanDay(BaseModel):
    """训练计划每日安排表"""
    
    __tablename__ = 'plan_days'
    
    training_plan_id = Column(Integer, ForeignKey('training_plans.id', ondelete='CASCADE'),
                             nullable=False, index=True, comment='训练计划ID')
    
    # 日期信息
    day_number = Column(Integer, nullable=False, comment='第几天')
    day_name = Column(String(50), comment='当天名称')  # 如：胸部训练日
    
    # 训练内容
    description = Column(Text, comment='训练描述')
    warm_up = Column(Text, comment='热身内容')
    cool_down = Column(Text, comment='放松内容')
    
    # 训练参数
    estimated_duration = Column(Integer, comment='预计时长(分钟)')
    target_calories = Column(Integer, comment='目标消耗卡路里')
    rest_time = Column(Integer, comment='组间休息时间(秒)')
    
    # 关系映射
    training_plan = relationship('TrainingPlan', back_populates='plan_days')
    exercises = relationship('Exercise', back_populates='plan_day',
                           cascade='all, delete-orphan', order_by='Exercise.order_number')
    
    def __repr__(self):
        return f"<PlanDay(id={self.id}, day_number={self.day_number}, plan_id={self.training_plan_id})>"


class Exercise(BaseModel):
    """运动动作表"""
    
    __tablename__ = 'exercises'
    
    plan_day_id = Column(Integer, ForeignKey('plan_days.id', ondelete='CASCADE'),
                        nullable=False, index=True, comment='计划日ID')
    
    # 动作信息
    name = Column(String(100), nullable=False, index=True, comment='动作名称')
    description = Column(Text, comment='动作描述')
    video_url = Column(String(255), comment='演示视频URL')
    image_url = Column(String(255), comment='演示图片URL')
    
    # 动作分类
    exercise_type = Column(String(50), nullable=False, index=True, comment='动作类型')  # 力量/有氧/拉伸
    muscle_group = Column(Enum(MuscleGroupEnum), nullable=False, 
                         index=True, comment='目标肌群')
    equipment = Column(String(50), comment='所需器械')
    
    # 训练参数
    order_number = Column(Integer, nullable=False, comment='顺序')
    sets = Column(Integer, comment='组数')
    reps = Column(Integer, comment='每组次数')
    duration = Column(Integer, comment='持续时间(秒)')
    weight = Column(Integer, comment='建议重量(kg)')
    rest_time = Column(Integer, comment='休息时间(秒)')
    
    # 难度和消耗
    difficulty = Column(Enum(DifficultyEnum), comment='难度等级')
    calories_per_set = Column(Integer, comment='每组消耗卡路里')
    
    # 动作要点（JSON格式）
    key_points = Column(JSON, comment='动作要点')
    common_mistakes = Column(JSON, comment='常见错误')
    
    # 关系映射
    plan_day = relationship('PlanDay', back_populates='exercises')
    exercise_records = relationship('ExerciseRecord', back_populates='exercise')
    
    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name}, muscle_group={self.muscle_group})>"
