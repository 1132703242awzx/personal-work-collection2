#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
排行榜和对比分析服务
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from collections import defaultdict

from models import User, WorkoutRecord, SetRecord, ExerciseRecord, Follow, UserAchievement
from schemas.analytics_schemas import (
    LeaderboardEntry, LeaderboardResponse,
    ComparisonData, ComparisonResponse, ChartData, DataPoint, ChartTypeEnum
)
from services.analytics_service import AnalyticsService


class LeaderboardService:
    """排行榜服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.analytics_service = AnalyticsService(db)
    
    def get_leaderboard(self, current_user_id: int, metric: str = "workouts",
                       time_range: str = "month", limit: int = 10,
                       scope: str = "global") -> LeaderboardResponse:
        """获取排行榜
        
        Args:
            current_user_id: 当前用户ID
            metric: 排名指标 (workouts/duration/calories/volume/achievements)
            time_range: 时间范围
            limit: 返回数量
            scope: 范围 (global/friends/following)
        """
        start_dt, end_dt = self.analytics_service._get_date_range(time_range)
        
        # 根据scope确定用户范围
        user_ids = self._get_user_scope(current_user_id, scope)
        
        # 根据metric查询排名数据
        if metric == "workouts":
            rankings_data = self._get_workout_rankings(user_ids, start_dt, end_dt, limit)
            format_func = lambda v: f"{int(v)}次"
        elif metric == "duration":
            rankings_data = self._get_duration_rankings(user_ids, start_dt, end_dt, limit)
            format_func = lambda v: f"{int(v/60)}分钟"
        elif metric == "calories":
            rankings_data = self._get_calorie_rankings(user_ids, start_dt, end_dt, limit)
            format_func = lambda v: f"{int(v)}千卡"
        elif metric == "volume":
            rankings_data = self._get_volume_rankings(user_ids, start_dt, end_dt, limit)
            format_func = lambda v: f"{int(v)}kg"
        elif metric == "achievements":
            rankings_data = self._get_achievement_rankings(user_ids, limit)
            format_func = lambda v: f"{int(v)}个"
        else:
            raise ValueError(f"不支持的排名指标: {metric}")
        
        # 构建排行榜条目
        rankings = []
        current_user_rank = None
        
        for rank, (user_id, value) in enumerate(rankings_data, start=1):
            user = self.db.query(User).get(user_id)
            if not user:
                continue
            
            # 确定徽章
            badge = None
            if rank == 1:
                badge = "🥇"
            elif rank == 2:
                badge = "🥈"
            elif rank == 3:
                badge = "🥉"
            
            entry = LeaderboardEntry(
                rank=rank,
                user_id=user.id,
                username=user.username,
                nickname=user.nickname or user.username,
                avatar=getattr(user, 'avatar', None),
                value=float(value),
                formatted_value=format_func(value),
                badge=badge,
                is_current_user=(user_id == current_user_id)
            )
            
            rankings.append(entry)
            
            if user_id == current_user_id:
                current_user_rank = entry
        
        # 如果当前用户不在榜单中,单独查询
        if not current_user_rank:
            current_user_rank = self._get_user_rank(current_user_id, metric, start_dt, end_dt, user_ids)
            if current_user_rank:
                current_user_rank.formatted_value = format_func(current_user_rank.value)
        
        return LeaderboardResponse(
            metric=metric,
            time_range=time_range,
            total_participants=len(user_ids) if user_ids else 0,
            rankings=rankings,
            current_user_rank=current_user_rank,
            last_updated=datetime.now()
        )
    
    def _get_user_scope(self, user_id: int, scope: str) -> Optional[List[int]]:
        """获取用户范围"""
        if scope == "global":
            return None  # 所有用户
        elif scope == "friends":
            # 互相关注的用户
            mutual_follows = self.db.query(Follow.following_id).filter(
                Follow.follower_id == user_id,
                Follow.is_mutual == True,
                Follow.is_deleted == False
            ).all()
            return [user_id] + [f[0] for f in mutual_follows]
        elif scope == "following":
            # 关注的用户
            following = self.db.query(Follow.following_id).filter(
                Follow.follower_id == user_id,
                Follow.is_deleted == False
            ).all()
            return [user_id] + [f[0] for f in following]
        else:
            return None
    
    def _get_workout_rankings(self, user_ids: Optional[List[int]], start_dt, end_dt, limit: int):
        """训练次数排名"""
        query = self.db.query(
            WorkoutRecord.user_id,
            func.count(WorkoutRecord.id).label('workout_count')
        ).filter(
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        )
        
        if user_ids:
            query = query.filter(WorkoutRecord.user_id.in_(user_ids))
        
        query = query.group_by(WorkoutRecord.user_id).order_by(
            desc('workout_count')
        ).limit(limit)
        
        return [(row.user_id, row.workout_count) for row in query.all()]
    
    def _get_duration_rankings(self, user_ids: Optional[List[int]], start_dt, end_dt, limit: int):
        """训练时长排名"""
        query = self.db.query(
            WorkoutRecord.user_id,
            func.sum(WorkoutRecord.duration).label('total_duration')
        ).filter(
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.duration.isnot(None),
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        )
        
        if user_ids:
            query = query.filter(WorkoutRecord.user_id.in_(user_ids))
        
        query = query.group_by(WorkoutRecord.user_id).order_by(
            desc('total_duration')
        ).limit(limit)
        
        return [(row.user_id, row.total_duration) for row in query.all()]
    
    def _get_calorie_rankings(self, user_ids: Optional[List[int]], start_dt, end_dt, limit: int):
        """卡路里排名"""
        query = self.db.query(
            WorkoutRecord.user_id,
            func.sum(WorkoutRecord.calories).label('total_calories')
        ).filter(
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.calories.isnot(None),
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        )
        
        if user_ids:
            query = query.filter(WorkoutRecord.user_id.in_(user_ids))
        
        query = query.group_by(WorkoutRecord.user_id).order_by(
            desc('total_calories')
        ).limit(limit)
        
        return [(row.user_id, row.total_calories) for row in query.all()]
    
    def _get_volume_rankings(self, user_ids: Optional[List[int]], start_dt, end_dt, limit: int):
        """训练容量排名"""
        query = self.db.query(
            WorkoutRecord.user_id,
            func.sum(SetRecord.weight * SetRecord.reps).label('total_volume')
        ).join(
            ExerciseRecord, WorkoutRecord.id == ExerciseRecord.workout_record_id
        ).join(
            SetRecord, ExerciseRecord.id == SetRecord.exercise_record_id
        ).filter(
            WorkoutRecord.is_deleted == False,
            WorkoutRecord.status == 'completed',
            WorkoutRecord.start_time >= start_dt,
            WorkoutRecord.start_time <= end_dt
        )
        
        if user_ids:
            query = query.filter(WorkoutRecord.user_id.in_(user_ids))
        
        query = query.group_by(WorkoutRecord.user_id).order_by(
            desc('total_volume')
        ).limit(limit)
        
        return [(row.user_id, row.total_volume) for row in query.all()]
    
    def _get_achievement_rankings(self, user_ids: Optional[List[int]], limit: int):
        """成就排名"""
        query = self.db.query(
            UserAchievement.user_id,
            func.count(UserAchievement.id).label('achievement_count')
        ).filter(
            UserAchievement.is_deleted == False
        )
        
        if user_ids:
            query = query.filter(UserAchievement.user_id.in_(user_ids))
        
        query = query.group_by(UserAchievement.user_id).order_by(
            desc('achievement_count')
        ).limit(limit)
        
        return [(row.user_id, row.achievement_count) for row in query.all()]
    
    def _get_user_rank(self, user_id: int, metric: str, start_dt, end_dt, 
                       user_ids: Optional[List[int]]) -> Optional[LeaderboardEntry]:
        """获取用户排名"""
        # 简化实现,实际应该计算精确排名
        user = self.db.query(User).get(user_id)
        if not user:
            return None
        
        # 查询用户数据
        value = 0
        if metric == "workouts":
            value = self.db.query(func.count(WorkoutRecord.id)).filter(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.is_deleted == False,
                WorkoutRecord.status == 'completed',
                WorkoutRecord.start_time >= start_dt,
                WorkoutRecord.start_time <= end_dt
            ).scalar() or 0
        # 其他指标类似...
        
        return LeaderboardEntry(
            rank=999,  # 占位
            user_id=user.id,
            username=user.username,
            nickname=user.nickname or user.username,
            avatar=getattr(user, 'avatar', None),
            value=float(value),
            formatted_value="",
            is_current_user=True
        )


class ComparisonService:
    """对比分析服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.analytics_service = AnalyticsService(db)
    
    def compare_users(self, current_user_id: int, user_ids: List[int],
                     metrics: List[str], time_range: str = "month") -> ComparisonResponse:
        """用户对比分析
        
        Args:
            current_user_id: 当前用户ID
            user_ids: 对比用户IDs (包含当前用户)
            metrics: 对比指标
            time_range: 时间范围
        """
        if current_user_id not in user_ids:
            user_ids.append(current_user_id)
        
        start_dt, end_dt = self.analytics_service._get_date_range(time_range)
        
        # 收集每个用户的数据
        users_data = []
        
        for user_id in user_ids:
            user = self.db.query(User).get(user_id)
            if not user:
                continue
            
            metrics_data = {}
            
            for metric in metrics:
                if metric == "workouts":
                    value = self.db.query(func.count(WorkoutRecord.id)).filter(
                        WorkoutRecord.user_id == user_id,
                        WorkoutRecord.is_deleted == False,
                        WorkoutRecord.status == 'completed',
                        WorkoutRecord.start_time >= start_dt,
                        WorkoutRecord.start_time <= end_dt
                    ).scalar() or 0
                elif metric == "duration":
                    value = self.db.query(func.sum(WorkoutRecord.duration)).filter(
                        WorkoutRecord.user_id == user_id,
                        WorkoutRecord.is_deleted == False,
                        WorkoutRecord.status == 'completed',
                        WorkoutRecord.start_time >= start_dt,
                        WorkoutRecord.start_time <= end_dt
                    ).scalar() or 0
                    value = value / 60  # 转为分钟
                elif metric == "calories":
                    value = self.db.query(func.sum(WorkoutRecord.calories)).filter(
                        WorkoutRecord.user_id == user_id,
                        WorkoutRecord.is_deleted == False,
                        WorkoutRecord.status == 'completed',
                        WorkoutRecord.start_time >= start_dt,
                        WorkoutRecord.start_time <= end_dt
                    ).scalar() or 0
                else:
                    value = 0
                
                metrics_data[metric] = float(value)
            
            users_data.append(ComparisonData(
                user_id=user.id,
                username=user.username,
                nickname=user.nickname or user.username,
                metrics=metrics_data
            ))
        
        # 生成对比图表
        charts = []
        for metric in metrics:
            data_points = []
            for user_data in users_data:
                data_points.append(DataPoint(
                    date=user_data.username,
                    value=user_data.metrics[metric],
                    label=user_data.nickname
                ))
            
            metric_names = {
                "workouts": "训练次数",
                "duration": "训练时长",
                "calories": "卡路里消耗"
            }
            
            charts.append(ChartData(
                chart_type=ChartTypeEnum.bar,
                title=f"{metric_names.get(metric, metric)}对比",
                data=data_points,
                x_axis_label="用户",
                y_axis_label=metric_names.get(metric, metric),
                unit="" if metric == "workouts" else ("分钟" if metric == "duration" else "千卡")
            ))
        
        return ComparisonResponse(
            time_range=time_range,
            metrics=metrics,
            users=users_data,
            charts=charts
        )
