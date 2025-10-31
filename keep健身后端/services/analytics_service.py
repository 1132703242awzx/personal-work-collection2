#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户数据统计和分析服务

功能:
1. 训练频率和时长统计
2. 力量进步曲线
3. 身体数据变化趋势
4. 课程完成情况
5. 个人成就系统
6. 综合仪表盘
7. 排行榜
8. 对比分析
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import func, and_, or_, desc, case, extract
from sqlalchemy.orm import Session, joinedload
from collections import defaultdict
import json

from models import (
    User, WorkoutRecord, ExerciseRecord, SetRecord,
    BodyData, WeightRecord, Course, Chapter, Video,
    Achievement, UserAchievement, Exercise
)
from schemas.analytics_schemas import (
    FrequencyStatistics, DurationStatistics, StrengthProgress,
    BodyDataTrend, CourseProgress, AchievementSummary,
    CalorieStatistics, VolumeStatistics, DashboardData,
    ChartData, DataPoint, TimeRangeEnum, ChartTypeEnum,
    LeaderboardEntry, LeaderboardResponse, ComparisonData
)


class AnalyticsService:
    """数据分析服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ==================== 辅助方法 ====================
    
    def _get_date_range(self, time_range: str, start_date: Optional[date] = None, 
                       end_date: Optional[date] = None) -> Tuple[datetime, datetime]:
        """获取日期范围"""
        now = datetime.now()
        
        if start_date and end_date:
            return (
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.max.time())
            )
        
        if time_range == "week":
            start = now - timedelta(days=7)
        elif time_range == "month":
            start = now - timedelta(days=30)
        elif time_range == "quarter":
            start = now - timedelta(days=90)
        elif time_range == "year":
            start = now - timedelta(days=365)
        else:  # all
            start = datetime(2000, 1, 1)
        
        return start, now
    
    def _format_duration(self, seconds: int) -> str:
        """格式化时长"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}小时{minutes}分钟"
        else:
            return f"{minutes}分钟"
    
    def _calculate_streak(self, user_id: int, end_date: datetime) -> Tuple[int, int]:
        """计算连续训练天数
        
        Returns:
            (current_streak, max_streak)
        """
        # 获取用户所有训练日期
        workout_dates = self.db.query(
            func.date(WorkoutRecord.start_time).label('date')
        ).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed'
        ).group_by(
            func.date(WorkoutRecord.start_time)
        ).order_by(
            desc(func.date(WorkoutRecord.start_time))
        ).all()
        
        if not workout_dates:
            return 0, 0
        
        dates = [d[0] for d in workout_dates]
        
        # 计算当前连续天数
        current_streak = 0
        current_date = end_date.date()
        
        for workout_date in dates:
            if workout_date == current_date or workout_date == current_date - timedelta(days=1):
                current_streak += 1
                current_date = workout_date - timedelta(days=1)
            else:
                break
        
        # 计算最长连续天数
        max_streak = 1
        temp_streak = 1
        
        for i in range(1, len(dates)):
            if dates[i] == dates[i-1] - timedelta(days=1):
                temp_streak += 1
                max_streak = max(max_streak, temp_streak)
            else:
                temp_streak = 1
        
        return current_streak, max_streak
    
    # ==================== 训练频率统计 ====================
    
    def get_frequency_statistics(self, user_id: int, time_range: str = "month",
                                 start_date: Optional[date] = None,
                                 end_date: Optional[date] = None,
                                 include_chart: bool = True) -> FrequencyStatistics:
        """获取训练频率统计"""
        start_dt, end_dt = self._get_date_range(time_range, start_date, end_date)
        
        # 查询训练记录
        workouts = self.db.query(WorkoutRecord).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        ).all()
        
        total_workouts = len(workouts)
        total_days = (end_dt - start_dt).days + 1
        
        # 获取训练天数
        workout_days_set = set()
        for workout in workouts:
            workout_days_set.add(workout.start_time.date())
        
        workout_days = len(workout_days_set)
        rest_days = total_days - workout_days
        
        # 计算周平均
        weeks = total_days / 7
        average_per_week = total_workouts / weeks if weeks > 0 else 0
        
        # 计算频率
        frequency_rate = (workout_days / total_days * 100) if total_days > 0 else 0
        
        # 计算连续天数
        current_streak, max_streak = self._calculate_streak(user_id, end_dt)
        
        # 生成图表数据
        chart = None
        if include_chart:
            # 按周分组
            weekly_data = defaultdict(int)
            for workout in workouts:
                week_key = workout.start_time.strftime("%Y-W%W")
                weekly_data[week_key] += 1
            
            data_points = []
            for week_key in sorted(weekly_data.keys()):
                data_points.append(DataPoint(
                    date=week_key,
                    value=weekly_data[week_key],
                    label=f"第{week_key.split('-W')[1]}周"
                ))
            
            chart = ChartData(
                chart_type=ChartTypeEnum.bar,
                title="训练频率趋势",
                data=data_points,
                x_axis_label="周",
                y_axis_label="训练次数",
                unit="次"
            )
        
        return FrequencyStatistics(
            total_workouts=total_workouts,
            total_days=total_days,
            average_per_week=round(average_per_week, 1),
            max_streak=max_streak,
            current_streak=current_streak,
            workout_days=workout_days,
            rest_days=rest_days,
            frequency_rate=round(frequency_rate, 1),
            chart=chart
        )
    
    # ==================== 训练时长统计 ====================
    
    def get_duration_statistics(self, user_id: int, time_range: str = "month",
                               start_date: Optional[date] = None,
                               end_date: Optional[date] = None,
                               include_chart: bool = True) -> DurationStatistics:
        """获取训练时长统计"""
        start_dt, end_dt = self._get_date_range(time_range, start_date, end_date)
        
        # 查询训练记录
        workouts = self.db.query(WorkoutRecord).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.duration.isnot(None),
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        ).all()
        
        if not workouts:
            return DurationStatistics(
                total_duration=0,
                total_duration_formatted="0分钟",
                average_duration=0,
                average_duration_formatted="0分钟",
                longest_workout=0,
                shortest_workout=0,
                duration_distribution={},
                chart=None
            )
        
        durations = [w.duration for w in workouts]
        total_duration = sum(durations)
        average_duration = total_duration // len(durations)
        longest_workout = max(durations)
        shortest_workout = min(durations)
        
        # 时长分布 (分档)
        duration_distribution = {
            "0-30分钟": 0,
            "30-60分钟": 0,
            "60-90分钟": 0,
            "90分钟以上": 0
        }
        
        for duration in durations:
            minutes = duration / 60
            if minutes <= 30:
                duration_distribution["0-30分钟"] += 1
            elif minutes <= 60:
                duration_distribution["30-60分钟"] += 1
            elif minutes <= 90:
                duration_distribution["60-90分钟"] += 1
            else:
                duration_distribution["90分钟以上"] += 1
        
        # 生成图表
        chart = None
        if include_chart:
            # 按日统计
            daily_data = defaultdict(int)
            for workout in workouts:
                date_key = workout.start_time.strftime("%Y-%m-%d")
                daily_data[date_key] += workout.duration
            
            data_points = []
            for date_key in sorted(daily_data.keys()):
                data_points.append(DataPoint(
                    date=date_key,
                    value=round(daily_data[date_key] / 60, 1),  # 转换为分钟
                    label=date_key
                ))
            
            chart = ChartData(
                chart_type=ChartTypeEnum.area,
                title="训练时长趋势",
                data=data_points,
                x_axis_label="日期",
                y_axis_label="时长",
                unit="分钟"
            )
        
        return DurationStatistics(
            total_duration=total_duration,
            total_duration_formatted=self._format_duration(total_duration),
            average_duration=average_duration,
            average_duration_formatted=self._format_duration(average_duration),
            longest_workout=longest_workout,
            shortest_workout=shortest_workout,
            duration_distribution=duration_distribution,
            chart=chart
        )
    
    # ==================== 力量进步分析 ====================
    
    def get_strength_progress(self, user_id: int, exercise_id: Optional[int] = None,
                             time_range: str = "all",
                             start_date: Optional[date] = None,
                             end_date: Optional[date] = None,
                             include_chart: bool = True) -> List[StrengthProgress]:
        """获取力量进步曲线"""
        start_dt, end_dt = self._get_date_range(time_range, start_date, end_date)
        
        # 查询条件
        query = self.db.query(
            ExerciseRecord.exercise_id,
            Exercise.name.label('exercise_name'),
            func.min(SetRecord.weight).label('min_weight'),
            func.max(SetRecord.weight).label('max_weight'),
            func.avg(SetRecord.weight).label('avg_weight'),
            func.sum(SetRecord.weight * SetRecord.reps).label('total_volume'),
            func.count(SetRecord.id).label('records_count')
        ).join(
            SetRecord, ExerciseRecord.id == SetRecord.exercise_record_id
        ).join(
            WorkoutRecord, ExerciseRecord.workout_record_id == WorkoutRecord.id
        ).join(
            Exercise, ExerciseRecord.exercise_id == Exercise.id
        ).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            SetRecord.weight.isnot(None),
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        )
        
        if exercise_id:
            query = query.filter(ExerciseRecord.exercise_id == exercise_id)
        
        query = query.group_by(ExerciseRecord.exercise_id, Exercise.name)
        
        results = query.all()
        
        progress_list = []
        
        for result in results:
            # 获取历史记录用于图表
            chart = None
            if include_chart:
                history = self.db.query(
                    func.date(WorkoutRecord.start_time).label('date'),
                    func.max(SetRecord.weight).label('max_weight')
                ).join(
                    ExerciseRecord, WorkoutRecord.id == ExerciseRecord.workout_record_id
                ).join(
                    SetRecord, ExerciseRecord.id == SetRecord.exercise_record_id
                ).filter(
                    WorkoutRecord.user_id == user_id,
                    ExerciseRecord.exercise_id == result.exercise_id,
                    WorkoutRecord.is_deleted == False,
                    WorkoutRecord.start_time >= start_dt,
                    WorkoutRecord.start_time <= end_dt
                ).group_by(
                    func.date(WorkoutRecord.start_time)
                ).order_by(
                    func.date(WorkoutRecord.start_time)
                ).all()
                
                data_points = []
                for record in history:
                    data_points.append(DataPoint(
                        date=record.date.strftime("%Y-%m-%d"),
                        value=float(record.max_weight),
                        label=f"{record.max_weight}kg"
                    ))
                
                chart = ChartData(
                    chart_type=ChartTypeEnum.line,
                    title=f"{result.exercise_name} - 力量进步",
                    data=data_points,
                    x_axis_label="日期",
                    y_axis_label="重量",
                    unit="kg"
                )
            
            # 计算进步率
            progress_rate = 0
            if result.min_weight and result.max_weight and result.min_weight > 0:
                progress_rate = ((result.max_weight - result.min_weight) / result.min_weight) * 100
            
            progress_list.append(StrengthProgress(
                exercise_id=result.exercise_id,
                exercise_name=result.exercise_name,
                start_weight=float(result.min_weight),
                current_weight=float(result.avg_weight),
                max_weight=float(result.max_weight),
                progress=round(progress_rate, 1),
                total_volume=float(result.total_volume),
                records_count=result.records_count,
                chart=chart
            ))
        
        return progress_list
    
    # ==================== 身体数据趋势 ====================
    
    def get_body_data_trends(self, user_id: int, metrics: List[str] = None,
                            time_range: str = "month",
                            start_date: Optional[date] = None,
                            end_date: Optional[date] = None,
                            include_chart: bool = True) -> List[BodyDataTrend]:
        """获取身体数据变化趋势"""
        if metrics is None:
            metrics = ["weight", "body_fat"]
        
        start_dt, end_dt = self._get_date_range(time_range, start_date, end_date)
        
        trends = []
        
        for metric in metrics:
            # 查询体重记录
            if metric == "weight":
                records = self.db.query(WeightRecord).filter(
                    WeightRecord.user_id == user_id,
                    WeightRecord.is_deleted == False,
                    WeightRecord.record_date >= start_dt.date(),
                    WeightRecord.record_date <= end_dt.date()
                ).order_by(WeightRecord.record_date).all()
                
                if not records:
                    continue
                
                values = [r.weight for r in records]
                start_value = values[0]
                current_value = values[-1]
                change = current_value - start_value
                change_rate = (change / start_value * 100) if start_value > 0 else 0
                
                # 判断趋势
                if abs(change_rate) < 1:
                    trend = "stable"
                elif change > 0:
                    trend = "up"
                else:
                    trend = "down"
                
                # 生成图表
                chart = None
                if include_chart:
                    data_points = []
                    for record in records:
                        data_points.append(DataPoint(
                            date=record.record_date.strftime("%Y-%m-%d"),
                            value=float(record.weight),
                            label=f"{record.weight}kg"
                        ))
                    
                    chart = ChartData(
                        chart_type=ChartTypeEnum.line,
                        title="体重变化趋势",
                        data=data_points,
                        x_axis_label="日期",
                        y_axis_label="体重",
                        unit="kg"
                    )
                
                trends.append(BodyDataTrend(
                    metric="体重",
                    start_value=float(start_value),
                    current_value=float(current_value),
                    change=round(change, 2),
                    change_rate=round(change_rate, 2),
                    trend=trend,
                    records_count=len(records),
                    chart=chart
                ))
            
            # 可以添加更多指标: body_fat, muscle_mass等
        
        return trends
    
    # ==================== 课程完成情况 ====================
    
    def get_course_progress(self, user_id: int, course_id: Optional[int] = None) -> List[CourseProgress]:
        """获取课程完成情况"""
        # 这里需要根据实际的课程进度表来实现
        # 暂时返回示例数据结构
        progress_list = []
        
        # 查询用户课程记录 (需要实现UserCourseProgress模型)
        # 这里提供基础框架
        
        return progress_list
    
    # ==================== 卡路里统计 ====================
    
    def get_calorie_statistics(self, user_id: int, time_range: str = "month",
                               start_date: Optional[date] = None,
                               end_date: Optional[date] = None,
                               include_chart: bool = True) -> CalorieStatistics:
        """获取卡路里统计"""
        start_dt, end_dt = self._get_date_range(time_range, start_date, end_date)
        
        # 查询训练记录
        workouts = self.db.query(WorkoutRecord).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.calories.isnot(None),
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        ).all()
        
        if not workouts:
            return CalorieStatistics(
                total_calories=0,
                average_per_workout=0,
                max_calories=0,
                chart=None
            )
        
        calories_list = [w.calories for w in workouts]
        total_calories = sum(calories_list)
        average_per_workout = total_calories / len(calories_list)
        max_calories = max(calories_list)
        
        # 生成图表
        chart = None
        if include_chart:
            daily_data = defaultdict(float)
            for workout in workouts:
                date_key = workout.start_time.strftime("%Y-%m-%d")
                daily_data[date_key] += workout.calories
            
            data_points = []
            for date_key in sorted(daily_data.keys()):
                data_points.append(DataPoint(
                    date=date_key,
                    value=round(daily_data[date_key], 1),
                    label=f"{daily_data[date_key]:.0f}卡"
                ))
            
            chart = ChartData(
                chart_type=ChartTypeEnum.area,
                title="卡路里消耗趋势",
                data=data_points,
                x_axis_label="日期",
                y_axis_label="卡路里",
                unit="千卡"
            )
        
        return CalorieStatistics(
            total_calories=round(total_calories, 1),
            average_per_workout=round(average_per_workout, 1),
            max_calories=round(max_calories, 1),
            chart=chart
        )
    
    # ==================== 训练容量统计 ====================
    
    def get_volume_statistics(self, user_id: int, time_range: str = "month",
                             start_date: Optional[date] = None,
                             end_date: Optional[date] = None,
                             include_chart: bool = True) -> VolumeStatistics:
        """获取训练容量统计"""
        start_dt, end_dt = self._get_date_range(time_range, start_date, end_date)
        
        # 查询训练容量 (重量 × 次数)
        result = self.db.query(
            func.sum(SetRecord.weight * SetRecord.reps).label('total_volume'),
            func.count(WorkoutRecord.id.distinct()).label('workout_count')
        ).join(
            ExerciseRecord, SetRecord.exercise_record_id == ExerciseRecord.id
        ).join(
            WorkoutRecord, ExerciseRecord.workout_record_id == WorkoutRecord.id
        ).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        ).first()
        
        total_volume = float(result.total_volume) if result.total_volume else 0
        workout_count = result.workout_count if result.workout_count else 0
        average_per_workout = total_volume / workout_count if workout_count > 0 else 0
        
        # 按肌群统计
        muscle_group_data = self.db.query(
            Exercise.muscle_group,
            func.sum(SetRecord.weight * SetRecord.reps).label('volume')
        ).join(
            ExerciseRecord, Exercise.id == ExerciseRecord.exercise_id
        ).join(
            SetRecord, ExerciseRecord.id == SetRecord.exercise_record_id
        ).join(
            WorkoutRecord, ExerciseRecord.workout_record_id == WorkoutRecord.id
        ).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        ).group_by(
            Exercise.muscle_group
        ).all()
        
        by_muscle_group = {
            row.muscle_group: float(row.volume) for row in muscle_group_data
        }
        
        # 生成图表
        chart = None
        if include_chart:
            data_points = []
            for muscle_group, volume in by_muscle_group.items():
                data_points.append(DataPoint(
                    date=muscle_group,
                    value=round(volume, 1),
                    label=f"{volume:.0f}kg"
                ))
            
            chart = ChartData(
                chart_type=ChartTypeEnum.pie,
                title="训练容量分布",
                data=data_points,
                unit="kg"
            )
        
        return VolumeStatistics(
            total_volume=round(total_volume, 1),
            average_per_workout=round(average_per_workout, 1),
            by_muscle_group=by_muscle_group,
            chart=chart
        )
    
    # ==================== 成就系统 ====================
    
    def get_achievement_summary(self, user_id: int) -> AchievementSummary:
        """获取成就汇总"""
        # 查询所有成就
        all_achievements = self.db.query(Achievement).filter(
            Achievement.is_deleted == False
        ).all()
        
        # 查询用户已解锁成就
        user_achievements = self.db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.is_deleted == False
        ).all()
        
        unlocked_ids = {ua.achievement_id for ua in user_achievements}
        
        total_achievements = len(all_achievements)
        unlocked_count = len(unlocked_ids)
        unlock_rate = (unlocked_count / total_achievements * 100) if total_achievements > 0 else 0
        
        # 计算点数
        total_points = sum(a.points for a in all_achievements)
        earned_points = sum(a.points for a in all_achievements if a.id in unlocked_ids)
        
        # 按分类统计
        by_category = defaultdict(int)
        for achievement in all_achievements:
            if achievement.id in unlocked_ids:
                by_category[achievement.category] += 1
        
        # 按稀有度统计
        by_rarity = defaultdict(int)
        for achievement in all_achievements:
            if achievement.id in unlocked_ids:
                by_rarity[achievement.rarity] += 1
        
        # 最近解锁
        recent = self.db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.is_deleted == False
        ).order_by(
            desc(UserAchievement.unlocked_at)
        ).limit(5).all()
        
        from schemas.analytics_schemas import Achievement as AchievementSchema
        recent_unlocked = []
        for ua in recent:
            achievement = self.db.query(Achievement).get(ua.achievement_id)
            if achievement:
                recent_unlocked.append(AchievementSchema(
                    id=achievement.id,
                    name=achievement.name,
                    description=achievement.description,
                    icon=achievement.icon,
                    category=achievement.category,
                    rarity=achievement.rarity,
                    points=achievement.points,
                    is_unlocked=True,
                    unlocked_at=ua.unlocked_at,
                    progress=ua.progress
                ))
        
        return AchievementSummary(
            total_achievements=total_achievements,
            unlocked_count=unlocked_count,
            unlock_rate=round(unlock_rate, 1),
            total_points=total_points,
            earned_points=earned_points,
            by_category=dict(by_category),
            by_rarity=dict(by_rarity),
            recent_unlocked=recent_unlocked
        )
    
    # ==================== 综合仪表盘 ====================
    
    def get_dashboard_data(self, user_id: int, time_range: str = "week",
                          include_charts: bool = True) -> DashboardData:
        """获取综合仪表盘数据"""
        # 概览数据
        start_dt, end_dt = self._get_date_range(time_range)
        
        workout_count = self.db.query(func.count(WorkoutRecord.id)).filter(
            WorkoutRecord.user_id == user_id,
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.start_time >= start_dt
        ).scalar()
        
        overview = {
            "time_range": time_range,
            "workout_count": workout_count,
            "last_updated": datetime.now().isoformat()
        }
        
        # 获取各项统计
        frequency = self.get_frequency_statistics(user_id, time_range, include_chart=include_charts)
        duration = self.get_duration_statistics(user_id, time_range, include_chart=include_charts)
        calories = self.get_calorie_statistics(user_id, time_range, include_chart=include_charts)
        achievements = self.get_achievement_summary(user_id)
        
        # 力量汇总
        strength_progress = self.get_strength_progress(user_id, time_range=time_range, include_chart=False)
        strength_summary = {
            "exercises_tracked": len(strength_progress),
            "total_volume": sum(p.total_volume for p in strength_progress),
            "average_progress": sum(p.progress for p in strength_progress) / len(strength_progress) if strength_progress else 0
        }
        
        # 身体数据汇总
        body_trends = self.get_body_data_trends(user_id, time_range=time_range, include_chart=False)
        body_data_summary = {
            "metrics_tracked": len(body_trends),
            "trends": [{"metric": t.metric, "change": t.change, "trend": t.trend} for t in body_trends]
        }
        
        # 收集图表
        charts = []
        if include_charts:
            if frequency.chart:
                charts.append(frequency.chart)
            if duration.chart:
                charts.append(duration.chart)
            if calories.chart:
                charts.append(calories.chart)
        
        return DashboardData(
            overview=overview,
            frequency=frequency,
            duration=duration,
            calories=calories,
            strength_summary=strength_summary,
            body_data_summary=body_data_summary,
            achievements=achievements,
            charts=charts if charts else None
        )
