#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户数据统计和分析 - Pydantic验证Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


class TimeRangeEnum(str, Enum):
    """时间范围枚举"""
    week = "week"
    month = "month"
    quarter = "quarter"
    year = "year"
    all = "all"


class ChartTypeEnum(str, Enum):
    """图表类型枚举"""
    line = "line"          # 折线图
    bar = "bar"            # 柱状图
    pie = "pie"            # 饼图
    area = "area"          # 面积图
    scatter = "scatter"    # 散点图


class MetricTypeEnum(str, Enum):
    """指标类型枚举"""
    frequency = "frequency"        # 训练频率
    duration = "duration"          # 训练时长
    calories = "calories"          # 卡路里消耗
    weight = "weight"             # 体重
    strength = "strength"         # 力量
    volume = "volume"             # 训练容量


# ==================== 查询Schemas ====================

class AnalyticsQuery(BaseModel):
    """统计查询基础Schema"""
    time_range: TimeRangeEnum = Field(default=TimeRangeEnum.month, description="时间范围")
    start_date: Optional[date] = Field(default=None, description="开始日期")
    end_date: Optional[date] = Field(default=None, description="结束日期")
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        """验证日期范围"""
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError("结束日期不能早于开始日期")
        return v


class FrequencyAnalyticsQuery(AnalyticsQuery):
    """训练频率统计查询"""
    group_by: str = Field(default="day", description="分组方式: day/week/month")


class StrengthProgressQuery(AnalyticsQuery):
    """力量进步查询"""
    exercise_id: Optional[int] = Field(default=None, description="运动ID")
    muscle_group: Optional[str] = Field(default=None, description="肌群")
    metric: MetricTypeEnum = Field(default=MetricTypeEnum.strength, description="指标类型")


class BodyDataTrendQuery(AnalyticsQuery):
    """身体数据趋势查询"""
    metrics: List[str] = Field(default=["weight", "body_fat"], description="指标列表")


class CourseProgressQuery(BaseModel):
    """课程进度查询"""
    course_id: Optional[int] = Field(default=None, description="课程ID")
    status: Optional[str] = Field(default=None, description="状态: not_started/in_progress/completed")


class AchievementQuery(BaseModel):
    """成就查询"""
    category: Optional[str] = Field(default=None, description="成就分类")
    unlocked_only: bool = Field(default=False, description="仅显示已解锁")


class DashboardQuery(BaseModel):
    """仪表盘数据查询"""
    time_range: TimeRangeEnum = Field(default=TimeRangeEnum.week, description="时间范围")
    include_charts: bool = Field(default=True, description="包含图表数据")


# ==================== 响应Schemas ====================

class DataPoint(BaseModel):
    """数据点"""
    date: str = Field(..., description="日期")
    value: float = Field(..., description="数值")
    label: Optional[str] = Field(default=None, description="标签")
    extra: Optional[Dict[str, Any]] = Field(default=None, description="额外数据")


class ChartData(BaseModel):
    """图表数据"""
    chart_type: ChartTypeEnum = Field(..., description="图表类型")
    title: str = Field(..., description="图表标题")
    data: List[DataPoint] = Field(..., description="数据点列表")
    x_axis_label: Optional[str] = Field(default=None, description="X轴标签")
    y_axis_label: Optional[str] = Field(default=None, description="Y轴标签")
    unit: Optional[str] = Field(default=None, description="单位")
    
    class Config:
        json_schema_extra = {
            "example": {
                "chart_type": "line",
                "title": "训练频率趋势",
                "data": [
                    {"date": "2024-01-01", "value": 3, "label": "第1周"},
                    {"date": "2024-01-08", "value": 4, "label": "第2周"}
                ],
                "x_axis_label": "日期",
                "y_axis_label": "训练次数",
                "unit": "次"
            }
        }


class FrequencyStatistics(BaseModel):
    """训练频率统计"""
    total_workouts: int = Field(..., description="总训练次数")
    total_days: int = Field(..., description="总天数")
    average_per_week: float = Field(..., description="周平均训练次数")
    max_streak: int = Field(..., description="最长连续训练天数")
    current_streak: int = Field(..., description="当前连续训练天数")
    workout_days: int = Field(..., description="训练天数")
    rest_days: int = Field(..., description="休息天数")
    frequency_rate: float = Field(..., description="训练频率(%)")
    chart: Optional[ChartData] = Field(default=None, description="频率图表")


class DurationStatistics(BaseModel):
    """训练时长统计"""
    total_duration: int = Field(..., description="总时长(秒)")
    total_duration_formatted: str = Field(..., description="总时长(格式化)")
    average_duration: int = Field(..., description="平均时长(秒)")
    average_duration_formatted: str = Field(..., description="平均时长(格式化)")
    longest_workout: int = Field(..., description="最长训练(秒)")
    shortest_workout: int = Field(..., description="最短训练(秒)")
    duration_distribution: Dict[str, int] = Field(..., description="时长分布")
    chart: Optional[ChartData] = Field(default=None, description="时长图表")


class StrengthProgress(BaseModel):
    """力量进步"""
    exercise_id: int = Field(..., description="运动ID")
    exercise_name: str = Field(..., description="运动名称")
    start_weight: float = Field(..., description="起始重量")
    current_weight: float = Field(..., description="当前重量")
    max_weight: float = Field(..., description="最大重量")
    progress: float = Field(..., description="进步幅度(%)")
    total_volume: float = Field(..., description="总训练容量")
    records_count: int = Field(..., description="记录数")
    chart: Optional[ChartData] = Field(default=None, description="进步曲线")


class BodyDataTrend(BaseModel):
    """身体数据趋势"""
    metric: str = Field(..., description="指标名称")
    start_value: Optional[float] = Field(default=None, description="起始值")
    current_value: Optional[float] = Field(default=None, description="当前值")
    change: Optional[float] = Field(default=None, description="变化量")
    change_rate: Optional[float] = Field(default=None, description="变化率(%)")
    trend: str = Field(..., description="趋势: up/down/stable")
    records_count: int = Field(..., description="记录数")
    chart: Optional[ChartData] = Field(default=None, description="趋势图表")


class CourseProgress(BaseModel):
    """课程进度"""
    course_id: int = Field(..., description="课程ID")
    course_name: str = Field(..., description="课程名称")
    total_chapters: int = Field(..., description="总章节数")
    completed_chapters: int = Field(..., description="已完成章节数")
    progress_rate: float = Field(..., description="完成率(%)")
    total_duration: int = Field(..., description="总时长(秒)")
    watched_duration: int = Field(..., description="已观看时长(秒)")
    status: str = Field(..., description="状态")
    started_at: Optional[datetime] = Field(default=None, description="开始时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")


class Achievement(BaseModel):
    """成就"""
    id: int = Field(..., description="成就ID")
    name: str = Field(..., description="成就名称")
    description: str = Field(..., description="描述")
    icon: Optional[str] = Field(default=None, description="图标")
    category: str = Field(..., description="分类")
    rarity: str = Field(..., description="稀有度")
    points: int = Field(..., description="成就点数")
    is_unlocked: bool = Field(..., description="是否解锁")
    unlocked_at: Optional[datetime] = Field(default=None, description="解锁时间")
    progress: Optional[float] = Field(default=None, description="进度(%)")
    requirement: Optional[Dict[str, Any]] = Field(default=None, description="解锁条件")


class AchievementSummary(BaseModel):
    """成就汇总"""
    total_achievements: int = Field(..., description="总成就数")
    unlocked_count: int = Field(..., description="已解锁数")
    unlock_rate: float = Field(..., description="解锁率(%)")
    total_points: int = Field(..., description="总成就点数")
    earned_points: int = Field(..., description="已获得点数")
    by_category: Dict[str, int] = Field(..., description="分类统计")
    by_rarity: Dict[str, int] = Field(..., description="稀有度统计")
    recent_unlocked: List[Achievement] = Field(..., description="最近解锁")


class CalorieStatistics(BaseModel):
    """卡路里统计"""
    total_calories: float = Field(..., description="总消耗")
    average_per_workout: float = Field(..., description="平均每次训练")
    max_calories: float = Field(..., description="最大消耗")
    calories_goal: Optional[float] = Field(default=None, description="目标")
    goal_completion: Optional[float] = Field(default=None, description="目标完成率(%)")
    chart: Optional[ChartData] = Field(default=None, description="卡路里图表")


class VolumeStatistics(BaseModel):
    """训练容量统计"""
    total_volume: float = Field(..., description="总容量(kg)")
    average_per_workout: float = Field(..., description="平均每次")
    by_muscle_group: Dict[str, float] = Field(..., description="按肌群统计")
    chart: Optional[ChartData] = Field(default=None, description="容量图表")


class DashboardData(BaseModel):
    """仪表盘数据"""
    overview: Dict[str, Any] = Field(..., description="概览数据")
    frequency: FrequencyStatistics = Field(..., description="训练频率")
    duration: DurationStatistics = Field(..., description="训练时长")
    calories: CalorieStatistics = Field(..., description="卡路里")
    strength_summary: Dict[str, Any] = Field(..., description="力量汇总")
    body_data_summary: Dict[str, Any] = Field(..., description="身体数据汇总")
    achievements: AchievementSummary = Field(..., description="成就汇总")
    charts: Optional[List[ChartData]] = Field(default=None, description="图表列表")


# ==================== 排行榜Schemas ====================

class LeaderboardQuery(BaseModel):
    """排行榜查询"""
    metric: str = Field(..., description="排名指标: workouts/duration/calories/volume/achievements")
    time_range: TimeRangeEnum = Field(default=TimeRangeEnum.month, description="时间范围")
    limit: int = Field(default=10, ge=1, le=100, description="返回数量")
    scope: str = Field(default="global", description="范围: global/friends/following")


class LeaderboardEntry(BaseModel):
    """排行榜条目"""
    rank: int = Field(..., description="排名")
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    nickname: str = Field(..., description="昵称")
    avatar: Optional[str] = Field(default=None, description="头像")
    value: float = Field(..., description="指标值")
    formatted_value: str = Field(..., description="格式化值")
    badge: Optional[str] = Field(default=None, description="徽章")
    is_current_user: bool = Field(default=False, description="是否当前用户")


class LeaderboardResponse(BaseModel):
    """排行榜响应"""
    metric: str = Field(..., description="排名指标")
    time_range: str = Field(..., description="时间范围")
    total_participants: int = Field(..., description="总参与人数")
    rankings: List[LeaderboardEntry] = Field(..., description="排名列表")
    current_user_rank: Optional[LeaderboardEntry] = Field(default=None, description="当前用户排名")
    last_updated: datetime = Field(..., description="最后更新时间")


# ==================== 对比分析Schemas ====================

class ComparisonQuery(BaseModel):
    """对比分析查询"""
    user_ids: List[int] = Field(..., min_length=2, max_length=5, description="对比用户IDs")
    metrics: List[str] = Field(..., description="对比指标")
    time_range: TimeRangeEnum = Field(default=TimeRangeEnum.month, description="时间范围")


class ComparisonData(BaseModel):
    """对比数据"""
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    nickname: str = Field(..., description="昵称")
    metrics: Dict[str, float] = Field(..., description="指标数据")


class ComparisonResponse(BaseModel):
    """对比分析响应"""
    time_range: str = Field(..., description="时间范围")
    metrics: List[str] = Field(..., description="对比指标")
    users: List[ComparisonData] = Field(..., description="用户数据")
    charts: List[ChartData] = Field(..., description="对比图表")


# ==================== 导出Schemas ====================

class ExportQuery(BaseModel):
    """数据导出查询"""
    export_type: str = Field(..., description="导出类型: workouts/body_data/all")
    format: str = Field(default="json", description="格式: json/csv/excel")
    time_range: TimeRangeEnum = Field(default=TimeRangeEnum.all, description="时间范围")
    start_date: Optional[date] = Field(default=None, description="开始日期")
    end_date: Optional[date] = Field(default=None, description="结束日期")


class ExportResponse(BaseModel):
    """导出响应"""
    file_url: str = Field(..., description="文件下载URL")
    file_name: str = Field(..., description="文件名")
    file_size: int = Field(..., description="文件大小(字节)")
    records_count: int = Field(..., description="记录数")
    created_at: datetime = Field(..., description="创建时间")
    expires_at: datetime = Field(..., description="过期时间")
