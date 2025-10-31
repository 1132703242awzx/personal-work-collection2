"""
数据验证模式 (使用Pydantic)
用于验证请求数据的格式和内容
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SetTypeEnum(str, Enum):
    """组类型枚举"""
    NORMAL = "normal"  # 正常组
    WARMUP = "warmup"  # 热身组
    DROP = "drop"  # 递减组
    SUPER = "super"  # 超级组


class WorkoutTypeEnum(str, Enum):
    """训练类型枚举"""
    STRENGTH = "力量"
    CARDIO = "有氧"
    MIXED = "混合"
    FLEXIBILITY = "柔韧"


# ============= 组记录验证 =============

class SetRecordCreate(BaseModel):
    """创建组记录验证"""
    set_number: int = Field(..., ge=1, le=50, description="组号(1-50)")
    set_type: SetTypeEnum = Field(SetTypeEnum.NORMAL, description="组类型")
    reps: Optional[int] = Field(None, ge=0, le=1000, description="次数")
    weight: Optional[float] = Field(None, ge=0, le=1000, description="重量(kg)")
    duration: Optional[int] = Field(None, ge=0, le=7200, description="持续时间(秒)")
    distance: Optional[float] = Field(None, ge=0, le=1000, description="距离(km)")
    rest_time: Optional[int] = Field(None, ge=0, le=3600, description="休息时间(秒)")
    avg_heart_rate: Optional[int] = Field(None, ge=40, le=220, description="平均心率")
    max_heart_rate: Optional[int] = Field(None, ge=40, le=220, description="最大心率")
    is_completed: bool = Field(True, description="是否完成")
    is_failed: bool = Field(False, description="是否失败")
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10, description="难度评分")
    notes: Optional[str] = Field(None, max_length=500, description="备注")

    @validator('weight', 'reps', 'duration')
    def at_least_one_metric(cls, v, values):
        """至少要有一个数据指标"""
        if not any([values.get('weight'), values.get('reps'), values.get('duration'), v]):
            raise ValueError('至少需要填写重量、次数或持续时间中的一项')
        return v

    class Config:
        use_enum_values = True


class SetRecordUpdate(BaseModel):
    """更新组记录验证"""
    reps: Optional[int] = Field(None, ge=0, le=1000)
    weight: Optional[float] = Field(None, ge=0, le=1000)
    duration: Optional[int] = Field(None, ge=0, le=7200)
    distance: Optional[float] = Field(None, ge=0, le=1000)
    rest_time: Optional[int] = Field(None, ge=0, le=3600)
    avg_heart_rate: Optional[int] = Field(None, ge=40, le=220)
    max_heart_rate: Optional[int] = Field(None, ge=40, le=220)
    is_completed: Optional[bool] = None
    is_failed: Optional[bool] = None
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = Field(None, max_length=500)

    class Config:
        use_enum_values = True


# ============= 动作记录验证 =============

class ExerciseRecordCreate(BaseModel):
    """创建动作记录验证"""
    exercise_id: Optional[int] = Field(None, description="动作ID（可选）")
    exercise_name: str = Field(..., min_length=1, max_length=100, description="动作名称")
    muscle_group: Optional[str] = Field(None, max_length=50, description="目标肌群")
    exercise_type: Optional[str] = Field(None, max_length=50, description="动作类型")
    order_number: int = Field(..., ge=1, le=100, description="顺序")
    planned_sets: int = Field(..., ge=1, le=50, description="计划组数")
    notes: Optional[str] = Field(None, max_length=1000, description="备注")
    sets: List[SetRecordCreate] = Field(default_factory=list, description="组记录列表")

    @validator('sets')
    def validate_sets(cls, v, values):
        """验证组记录"""
        if v:
            # 检查组号是否连续
            set_numbers = [s.set_number for s in v]
            if len(set_numbers) != len(set(set_numbers)):
                raise ValueError('组号不能重复')
            if max(set_numbers) > values.get('planned_sets', 0):
                raise ValueError('组号不能超过计划组数')
        return v


class ExerciseRecordUpdate(BaseModel):
    """更新动作记录验证"""
    completed_sets: Optional[int] = Field(None, ge=0, le=50)
    notes: Optional[str] = Field(None, max_length=1000)


# ============= 训练记录验证 =============

class WorkoutRecordCreate(BaseModel):
    """创建训练记录验证"""
    training_plan_id: Optional[int] = Field(None, description="训练计划ID")
    workout_name: str = Field(..., min_length=1, max_length=100, description="训练名称")
    workout_type: WorkoutTypeEnum = Field(..., description="训练类型")
    workout_date: Optional[datetime] = Field(None, description="训练日期")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    location: Optional[str] = Field(None, max_length=100, description="训练地点")
    weather: Optional[str] = Field(None, max_length=50, description="天气")
    exercises: List[ExerciseRecordCreate] = Field(
        default_factory=list, 
        description="动作记录列表"
    )

    @validator('workout_date', 'start_time', pre=True)
    def parse_datetime(cls, v):
        """解析日期时间"""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except:
                raise ValueError('日期时间格式错误，请使用ISO格式')
        return v

    @validator('exercises')
    def validate_exercises(cls, v):
        """验证动作记录"""
        if v:
            # 检查顺序号是否连续
            order_numbers = [e.order_number for e in v]
            if len(order_numbers) != len(set(order_numbers)):
                raise ValueError('动作顺序号不能重复')
        return v

    class Config:
        use_enum_values = True


class WorkoutRecordUpdate(BaseModel):
    """更新训练记录验证"""
    workout_name: Optional[str] = Field(None, min_length=1, max_length=100)
    workout_type: Optional[WorkoutTypeEnum] = None
    end_time: Optional[datetime] = None
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10, description="难度评分")
    fatigue_level: Optional[int] = Field(None, ge=1, le=10, description="疲劳程度")
    mood_rating: Optional[int] = Field(None, ge=1, le=10, description="心情评分")
    notes: Optional[str] = Field(None, max_length=5000, description="训练笔记")
    location: Optional[str] = Field(None, max_length=100)
    weather: Optional[str] = Field(None, max_length=50)
    is_completed: Optional[bool] = None
    is_shared: Optional[bool] = None

    @validator('end_time', pre=True)
    def parse_datetime(cls, v):
        """解析日期时间"""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except:
                raise ValueError('日期时间格式错误')
        return v

    class Config:
        use_enum_values = True


class WorkoutRecordFinish(BaseModel):
    """完成训练验证"""
    end_time: Optional[datetime] = None
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10)
    fatigue_level: Optional[int] = Field(None, ge=1, le=10)
    mood_rating: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = Field(None, max_length=5000)

    @validator('end_time', pre=True)
    def parse_datetime(cls, v):
        """解析日期时间"""
        if v is None:
            return datetime.utcnow()
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except:
                raise ValueError('日期时间格式错误')
        return v


# ============= 查询参数验证 =============

class WorkoutListQuery(BaseModel):
    """训练记录列表查询参数"""
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")
    start_date: Optional[str] = Field(None, description="开始日期(YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="结束日期(YYYY-MM-DD)")
    workout_type: Optional[WorkoutTypeEnum] = None
    training_plan_id: Optional[int] = None
    is_completed: Optional[bool] = None
    keyword: Optional[str] = Field(None, max_length=100, description="搜索关键词")
    order_by: str = Field('workout_date', description="排序字段")
    order_direction: str = Field('desc', description="排序方向")

    @validator('start_date', 'end_date')
    def validate_date(cls, v):
        """验证日期格式"""
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except:
                raise ValueError('日期格式错误，应为YYYY-MM-DD')
        return v

    @validator('order_direction')
    def validate_order_direction(cls, v):
        """验证排序方向"""
        if v not in ['asc', 'desc']:
            raise ValueError('排序方向必须是asc或desc')
        return v

    class Config:
        use_enum_values = True


class CalendarQuery(BaseModel):
    """日历查询参数"""
    year: int = Field(..., ge=2000, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")


class StatsQuery(BaseModel):
    """统计查询参数"""
    start_date: Optional[str] = Field(None, description="开始日期")
    end_date: Optional[str] = Field(None, description="结束日期")
    period: str = Field('week', description="统计周期")  # day/week/month/year

    @validator('start_date', 'end_date')
    def validate_date(cls, v):
        """验证日期格式"""
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except:
                raise ValueError('日期格式错误')
        return v

    @validator('period')
    def validate_period(cls, v):
        """验证统计周期"""
        if v not in ['day', 'week', 'month', 'year']:
            raise ValueError('统计周期必须是day/week/month/year')
        return v
