"""
身体数据模型
包含身体数据、体重记录、身体测量
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class BodyData(BaseModel):
    """身体数据汇总表"""
    
    __tablename__ = 'body_data'
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'record_date'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='用户ID')
    
    # 记录日期
    record_date = Column(Date, nullable=False, comment='记录日期')
    
    # 基础数据
    weight = Column(Float, comment='体重(kg)')
    body_fat = Column(Float, comment='体脂率(%)')
    bmi = Column(Float, comment='BMI指数')
    
    # 身体成分
    muscle_mass = Column(Float, comment='肌肉量(kg)')
    bone_mass = Column(Float, comment='骨量(kg)')
    water_percentage = Column(Float, comment='水分率(%)')
    visceral_fat = Column(Float, comment='内脏脂肪等级')
    
    # 代谢相关
    bmr = Column(Integer, comment='基础代谢率(kcal)')
    metabolic_age = Column(Integer, comment='代谢年龄')
    
    # 健康指标
    heart_rate_resting = Column(Integer, comment='静息心率(bpm)')
    blood_pressure_systolic = Column(Integer, comment='收缩压(mmHg)')
    blood_pressure_diastolic = Column(Integer, comment='舒张压(mmHg)')
    
    # 扩展数据（JSON格式存储其他测量数据）
    extra_data = Column(JSON, comment='扩展数据')
    
    # 数据来源
    data_source = Column(String(50), comment='数据来源')  # manual/smart_scale/app
    device_info = Column(String(100), comment='设备信息')
    
    # 备注
    notes = Column(String(500), comment='备注')
    
    # 关系映射
    user = relationship('User', back_populates='body_data')
    
    def __repr__(self):
        return f"<BodyData(id={self.id}, user_id={self.user_id}, date={self.record_date})>"


class WeightRecord(BaseModel):
    """体重记录表（详细记录）"""
    
    __tablename__ = 'weight_records'
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'record_date'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='用户ID')
    
    # 记录时间
    record_date = Column(Date, nullable=False, comment='记录日期')
    record_time = Column(String(10), comment='记录时间')  # HH:MM
    
    # 体重数据
    weight = Column(Float, nullable=False, comment='体重(kg)')
    
    # 体重变化
    weight_change = Column(Float, comment='体重变化(kg)')
    weight_change_rate = Column(Float, comment='变化率(%)')
    
    # 目标相关
    target_weight = Column(Float, comment='目标体重(kg)')
    remaining_weight = Column(Float, comment='剩余体重(kg)')
    progress_rate = Column(Float, comment='完成进度(%)')
    
    # 记录类型
    record_type = Column(String(20), comment='记录类型')  # morning/evening/after_workout
    
    # 环境因素
    is_fasting = Column(Integer, default=False, comment='是否空腹')
    is_after_meal = Column(Integer, default=False, comment='是否餐后')
    
    # 数据来源
    data_source = Column(String(50), comment='数据来源')
    device_info = Column(String(100), comment='设备信息')
    
    # 备注
    notes = Column(String(500), comment='备注')
    mood = Column(String(50), comment='心情')
    
    # 关联照片
    photo_urls = Column(JSON, comment='照片URL列表')
    
    def __repr__(self):
        return f"<WeightRecord(id={self.id}, user_id={self.user_id}, weight={self.weight})>"


class BodyMeasurements(BaseModel):
    """身体围度测量表"""
    
    __tablename__ = 'body_measurements'
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'measurement_date'),
    )
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False, comment='用户ID')
    
    # 测量日期
    measurement_date = Column(Date, nullable=False, comment='测量日期')
    
    # 胸部围度
    chest = Column(Float, comment='胸围(cm)')
    
    # 腰部围度
    waist = Column(Float, comment='腰围(cm)')
    lower_waist = Column(Float, comment='下腰围(cm)')
    
    # 臀部围度
    hip = Column(Float, comment='臀围(cm)')
    
    # 腿部围度
    left_thigh = Column(Float, comment='左大腿围(cm)')
    right_thigh = Column(Float, comment='右大腿围(cm)')
    left_calf = Column(Float, comment='左小腿围(cm)')
    right_calf = Column(Float, comment='右小腿围(cm)')
    
    # 手臂围度
    left_upper_arm = Column(Float, comment='左上臂围(cm)')
    right_upper_arm = Column(Float, comment='右上臂围(cm)')
    left_forearm = Column(Float, comment='左前臂围(cm)')
    right_forearm = Column(Float, comment='右前臂围(cm)')
    
    # 肩部
    shoulder_width = Column(Float, comment='肩宽(cm)')
    
    # 颈部
    neck = Column(Float, comment='颈围(cm)')
    
    # 腰臀比
    waist_hip_ratio = Column(Float, comment='腰臀比')
    
    # 测量方式
    measurement_method = Column(String(50), comment='测量方式')  # manual/body_scan
    
    # 对比照片
    front_photo = Column(String(255), comment='正面照')
    side_photo = Column(String(255), comment='侧面照')
    back_photo = Column(String(255), comment='背面照')
    
    # 备注
    notes = Column(String(500), comment='备注')
    
    # 扩展数据
    extra_measurements = Column(JSON, comment='其他测量数据')
    
    def __repr__(self):
        return f"<BodyMeasurements(id={self.id}, user_id={self.user_id}, date={self.measurement_date})>"
