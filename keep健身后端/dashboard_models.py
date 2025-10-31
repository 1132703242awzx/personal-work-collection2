"""
Keep健身仪表盘 - 数据模型
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 个人信息
    nickname = db.Column(db.String(80))
    gender = db.Column(db.String(10))  # male, female, other
    birth_date = db.Column(db.Date)
    height = db.Column(db.Float)  # cm
    avatar = db.Column(db.String(255))
    
    # 系统字段
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 关系
    workout_records = db.relationship('WorkoutRecord', backref='user', lazy='dynamic', 
                                     cascade='all, delete-orphan')
    body_records = db.relationship('BodyRecord', backref='user', lazy='dynamic',
                                  cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def get_age(self):
        """计算年龄"""
        if self.birth_date:
            today = datetime.today()
            return today.year - self.birth_date.year - \
                   ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def get_latest_weight(self):
        """获取最新体重"""
        latest = self.body_records.order_by(BodyRecord.record_date.desc()).first()
        return latest.weight if latest else None
    
    def get_bmi(self):
        """计算BMI"""
        weight = self.get_latest_weight()
        if weight and self.height:
            height_m = self.height / 100
            return round(weight / (height_m ** 2), 1)
        return None
    
    def __repr__(self):
        return f'<User {self.username}>'


class WorkoutRecord(db.Model):
    """运动记录模型"""
    __tablename__ = 'workout_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 运动信息
    workout_type = db.Column(db.String(50), nullable=False)  # running, cycling, strength, etc.
    workout_name = db.Column(db.String(100))
    duration = db.Column(db.Integer)  # 分钟
    calories = db.Column(db.Integer)  # 卡路里
    distance = db.Column(db.Float)  # 公里
    
    # 详细数据
    sets = db.Column(db.Integer)  # 组数
    reps = db.Column(db.Integer)  # 次数
    weight = db.Column(db.Float)  # 重量(kg)
    heart_rate_avg = db.Column(db.Integer)  # 平均心率
    heart_rate_max = db.Column(db.Integer)  # 最大心率
    
    # 感受和备注
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    notes = db.Column(db.Text)
    
    # 时间
    workout_date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WorkoutRecord {self.workout_type} on {self.workout_date}>'


class BodyRecord(db.Model):
    """身体数据记录模型"""
    __tablename__ = 'body_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 身体数据
    weight = db.Column(db.Float, nullable=False)  # kg
    body_fat = db.Column(db.Float)  # 体脂率 %
    muscle_mass = db.Column(db.Float)  # 肌肉量 kg
    
    # 围度数据
    chest = db.Column(db.Float)  # 胸围 cm
    waist = db.Column(db.Float)  # 腰围 cm
    hips = db.Column(db.Float)  # 臀围 cm
    arm = db.Column(db.Float)  # 臂围 cm
    thigh = db.Column(db.Float)  # 腿围 cm
    
    # 备注
    notes = db.Column(db.Text)
    
    # 时间
    record_date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BodyRecord {self.weight}kg on {self.record_date}>'


class TrainingPlan(db.Model):
    """训练计划模型"""
    __tablename__ = 'training_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 计划信息
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    goal = db.Column(db.String(50))  # lose_weight, gain_muscle, endurance, etc.
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    
    # 计划周期
    duration_weeks = db.Column(db.Integer)
    days_per_week = db.Column(db.Integer)
    
    # 状态
    is_active = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='training_plans')
    
    def __repr__(self):
        return f'<TrainingPlan {self.name}>'
