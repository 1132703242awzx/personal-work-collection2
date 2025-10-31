"""
训练统计服务层
提供数据分析和统计功能
"""
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import and_, func, extract, case
from config.database import db_session
from models.workout import WorkoutRecord, ExerciseRecord


class StatsService:
    """训练统计服务类"""
    
    @staticmethod
    def get_overview_stats(user_id: int, start_date: str = None, 
                          end_date: str = None) -> Dict:
        """
        获取训练总览统计
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            统计数据
        """
        # 构建查询
        query = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        )
        
        # 日期筛选
        if start_date:
            query = query.filter(
                WorkoutRecord.workout_date >= datetime.strptime(start_date, '%Y-%m-%d')
            )
        if end_date:
            query = query.filter(
                WorkoutRecord.workout_date <= datetime.strptime(end_date, '%Y-%m-%d')
            )
        
        # 统计数据
        stats = query.with_entities(
            func.count(WorkoutRecord.id).label('total_workouts'),
            func.sum(WorkoutRecord.duration).label('total_duration'),
            func.sum(WorkoutRecord.calories_burned).label('total_calories'),
            func.sum(WorkoutRecord.total_sets).label('total_sets'),
            func.sum(WorkoutRecord.total_weight).label('total_weight'),
            func.avg(WorkoutRecord.duration).label('avg_duration')
        ).first()
        
        # 完成的训练次数
        completed_count = query.filter(WorkoutRecord.is_completed == True).count()
        
        # 最长训练时长
        max_duration_record = query.filter(
            WorkoutRecord.duration.isnot(None)
        ).order_by(WorkoutRecord.duration.desc()).first()
        
        # 单次最高卡路里消耗
        max_calories_record = query.filter(
            WorkoutRecord.calories_burned.isnot(None)
        ).order_by(WorkoutRecord.calories_burned.desc()).first()
        
        return {
            'total_workouts': stats.total_workouts or 0,
            'completed_workouts': completed_count,
            'total_duration': int(stats.total_duration or 0),  # 分钟
            'avg_duration': int(stats.avg_duration or 0),
            'total_calories': int(stats.total_calories or 0),
            'total_sets': int(stats.total_sets or 0),
            'total_weight': float(stats.total_weight or 0),
            'max_duration': max_duration_record.duration if max_duration_record else 0,
            'max_calories': max_calories_record.calories_burned if max_calories_record else 0,
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
    
    @staticmethod
    def get_weekly_stats(user_id: int) -> Dict:
        """
        获取周统计
        
        Args:
            user_id: 用户ID
            
        Returns:
            周统计数据
        """
        # 最近7天
        today = datetime.utcnow()
        week_ago = today - timedelta(days=7)
        
        # 按天分组统计
        daily_stats = db_session.query(
            func.date(WorkoutRecord.workout_date).label('date'),
            func.count(WorkoutRecord.id).label('count'),
            func.sum(WorkoutRecord.duration).label('duration'),
            func.sum(WorkoutRecord.calories_burned).label('calories')
        ).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.workout_date >= week_ago,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).group_by(
            func.date(WorkoutRecord.workout_date)
        ).all()
        
        # 构建7天数据（包含没有训练的日期）
        week_data = []
        for i in range(7):
            date = (week_ago + timedelta(days=i)).strftime('%Y-%m-%d')
            day_stat = next((s for s in daily_stats if str(s.date) == date), None)
            
            week_data.append({
                'date': date,
                'workout_count': day_stat.count if day_stat else 0,
                'duration': int(day_stat.duration or 0) if day_stat else 0,
                'calories': int(day_stat.calories or 0) if day_stat else 0
            })
        
        # 本周总计
        week_total = StatsService.get_overview_stats(
            user_id,
            week_ago.strftime('%Y-%m-%d'),
            today.strftime('%Y-%m-%d')
        )
        
        return {
            'period': 'week',
            'daily_stats': week_data,
            'week_total': week_total
        }
    
    @staticmethod
    def get_monthly_stats(user_id: int, year: int = None, month: int = None) -> Dict:
        """
        获取月统计
        
        Args:
            user_id: 用户ID
            year: 年份
            month: 月份
            
        Returns:
            月统计数据
        """
        # 默认当前月
        now = datetime.utcnow()
        year = year or now.year
        month = month or now.month
        
        # 按周分组统计
        weekly_stats = db_session.query(
            extract('week', WorkoutRecord.workout_date).label('week'),
            func.count(WorkoutRecord.id).label('count'),
            func.sum(WorkoutRecord.duration).label('duration'),
            func.sum(WorkoutRecord.calories_burned).label('calories')
        ).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                extract('year', WorkoutRecord.workout_date) == year,
                extract('month', WorkoutRecord.workout_date) == month,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).group_by(
            extract('week', WorkoutRecord.workout_date)
        ).all()
        
        # 月总计
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = datetime(year, month + 1, 1) - timedelta(days=1)
        
        month_total = StatsService.get_overview_stats(
            user_id,
            month_start.strftime('%Y-%m-%d'),
            month_end.strftime('%Y-%m-%d')
        )
        
        return {
            'period': 'month',
            'year': year,
            'month': month,
            'weekly_stats': [
                {
                    'week': stat.week,
                    'workout_count': stat.count,
                    'duration': int(stat.duration or 0),
                    'calories': int(stat.calories or 0)
                }
                for stat in weekly_stats
            ],
            'month_total': month_total
        }
    
    @staticmethod
    def get_muscle_group_distribution(user_id: int, start_date: str = None,
                                     end_date: str = None) -> Dict:
        """
        获取肌群训练分布
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            肌群分布数据
        """
        # 构建查询
        query = db_session.query(
            ExerciseRecord.muscle_group,
            func.count(ExerciseRecord.id).label('exercise_count'),
            func.sum(ExerciseRecord.completed_sets).label('total_sets'),
            func.sum(ExerciseRecord.total_weight).label('total_weight')
        ).join(WorkoutRecord).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                ExerciseRecord.muscle_group.isnot(None),
                WorkoutRecord.deleted_at.is_(None)
            )
        )
        
        # 日期筛选
        if start_date:
            query = query.filter(
                WorkoutRecord.workout_date >= datetime.strptime(start_date, '%Y-%m-%d')
            )
        if end_date:
            query = query.filter(
                WorkoutRecord.workout_date <= datetime.strptime(end_date, '%Y-%m-%d')
            )
        
        # 按肌群分组
        stats = query.group_by(ExerciseRecord.muscle_group).all()
        
        # 计算百分比
        total_exercises = sum(s.exercise_count for s in stats)
        
        distribution = [
            {
                'muscle_group': stat.muscle_group,
                'exercise_count': stat.exercise_count,
                'percentage': round((stat.exercise_count / total_exercises * 100), 1) if total_exercises > 0 else 0,
                'total_sets': int(stat.total_sets or 0),
                'total_weight': float(stat.total_weight or 0)
            }
            for stat in stats
        ]
        
        # 按训练次数排序
        distribution.sort(key=lambda x: x['exercise_count'], reverse=True)
        
        return {
            'total_exercises': total_exercises,
            'distribution': distribution
        }
    
    @staticmethod
    def get_workout_type_distribution(user_id: int, start_date: str = None,
                                     end_date: str = None) -> Dict:
        """
        获取训练类型分布
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            训练类型分布
        """
        # 构建查询
        query = db_session.query(
            WorkoutRecord.workout_type,
            func.count(WorkoutRecord.id).label('count'),
            func.sum(WorkoutRecord.duration).label('total_duration'),
            func.sum(WorkoutRecord.calories_burned).label('total_calories')
        ).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        )
        
        # 日期筛选
        if start_date:
            query = query.filter(
                WorkoutRecord.workout_date >= datetime.strptime(start_date, '%Y-%m-%d')
            )
        if end_date:
            query = query.filter(
                WorkoutRecord.workout_date <= datetime.strptime(end_date, '%Y-%m-%d')
            )
        
        # 按类型分组
        stats = query.group_by(WorkoutRecord.workout_type).all()
        
        # 计算百分比
        total_workouts = sum(s.count for s in stats)
        
        distribution = [
            {
                'workout_type': stat.workout_type,
                'count': stat.count,
                'percentage': round((stat.count / total_workouts * 100), 1) if total_workouts > 0 else 0,
                'total_duration': int(stat.total_duration or 0),
                'total_calories': int(stat.total_calories or 0)
            }
            for stat in stats
        ]
        
        return {
            'total_workouts': total_workouts,
            'distribution': distribution
        }
    
    @staticmethod
    def get_progress_trend(user_id: int, exercise_name: str = None,
                          period: str = 'month') -> Dict:
        """
        获取进步趋势
        
        Args:
            user_id: 用户ID
            exercise_name: 动作名称（可选）
            period: 统计周期 (week/month/year)
            
        Returns:
            进步趋势数据
        """
        # 确定时间范围
        now = datetime.utcnow()
        if period == 'week':
            start_date = now - timedelta(days=7)
            date_format = '%Y-%m-%d'
        elif period == 'month':
            start_date = now - timedelta(days=30)
            date_format = '%Y-%m-%d'
        else:  # year
            start_date = now - timedelta(days=365)
            date_format = '%Y-%m'
        
        # 构建查询
        query = db_session.query(
            func.date(WorkoutRecord.workout_date).label('date'),
            func.max(ExerciseRecord.max_weight).label('max_weight'),
            func.max(ExerciseRecord.max_reps).label('max_reps'),
            func.sum(ExerciseRecord.total_weight).label('total_weight')
        ).join(WorkoutRecord).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.workout_date >= start_date,
                WorkoutRecord.deleted_at.is_(None)
            )
        )
        
        # 按动作名称筛选
        if exercise_name:
            query = query.filter(ExerciseRecord.exercise_name == exercise_name)
        
        # 按日期分组
        trend_data = query.group_by(
            func.date(WorkoutRecord.workout_date)
        ).order_by(
            func.date(WorkoutRecord.workout_date)
        ).all()
        
        return {
            'period': period,
            'exercise_name': exercise_name or 'all',
            'trend': [
                {
                    'date': str(data.date),
                    'max_weight': float(data.max_weight or 0),
                    'max_reps': int(data.max_reps or 0),
                    'total_weight': float(data.total_weight or 0)
                }
                for data in trend_data
            ]
        }
    
    @staticmethod
    def get_consistency_score(user_id: int) -> Dict:
        """
        获取训练坚持度评分
        
        Args:
            user_id: 用户ID
            
        Returns:
            坚持度评分
        """
        # 最近30天
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)
        
        # 查询最近30天的训练记录
        workouts = db_session.query(
            func.date(WorkoutRecord.workout_date).label('date')
        ).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.workout_date >= thirty_days_ago,
                WorkoutRecord.is_completed == True,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).distinct().all()
        
        training_days = len(workouts)
        consistency_rate = round((training_days / 30 * 100), 1)
        
        # 计算连续训练天数
        all_workouts = db_session.query(
            func.date(WorkoutRecord.workout_date).label('date')
        ).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.is_completed == True,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).order_by(
            func.date(WorkoutRecord.workout_date).desc()
        ).distinct().all()
        
        # 计算当前连续天数
        current_streak = 0
        max_streak = 0
        temp_streak = 0
        
        if all_workouts:
            prev_date = None
            for workout in all_workouts:
                workout_date = workout.date
                
                if prev_date is None:
                    current_streak = 1
                    temp_streak = 1
                elif (prev_date - workout_date).days == 1:
                    current_streak += 1
                    temp_streak += 1
                else:
                    if prev_date is None or (now.date() - prev_date).days <= 1:
                        pass  # 继续当前连续
                    else:
                        current_streak = 0
                    temp_streak = 1
                
                max_streak = max(max_streak, temp_streak)
                prev_date = workout_date
        
        # 评分等级
        if consistency_rate >= 80:
            grade = 'S'
            grade_text = '优秀'
        elif consistency_rate >= 60:
            grade = 'A'
            grade_text = '良好'
        elif consistency_rate >= 40:
            grade = 'B'
            grade_text = '中等'
        elif consistency_rate >= 20:
            grade = 'C'
            grade_text = '需努力'
        else:
            grade = 'D'
            grade_text = '加油'
        
        return {
            'period_days': 30,
            'training_days': training_days,
            'consistency_rate': consistency_rate,
            'current_streak': current_streak,
            'max_streak': max_streak,
            'grade': grade,
            'grade_text': grade_text
        }
