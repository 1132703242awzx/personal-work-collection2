#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户数据统计和分析API路由

提供多维度数据分析接口:
- 训练频率和时长统计
- 力量进步曲线
- 身体数据变化趋势
- 卡路里和容量统计
- 成就系统
- 综合仪表盘
- 排行榜
- 用户对比
"""

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from typing import Optional
from datetime import date

from config.database import get_db
from middleware.auth import token_required
from services.analytics_service import AnalyticsService
from services.leaderboard_service import LeaderboardService, ComparisonService
from schemas.analytics_schemas import (
    FrequencyAnalyticsQuery, StrengthProgressQuery, BodyDataTrendQuery,
    DashboardQuery, LeaderboardQuery, ComparisonQuery,
    TimeRangeEnum
)


analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


# ==================== 训练频率统计 ====================

@analytics_bp.route('/frequency', methods=['GET'])
@token_required
def get_frequency_statistics(current_user):
    """
    获取训练频率统计
    ---
    查询参数:
        - time_range: 时间范围 (week/month/quarter/year/all)
        - start_date: 开始日期 (YYYY-MM-DD)
        - end_date: 结束日期 (YYYY-MM-DD)
        - include_chart: 是否包含图表数据 (true/false)
    """
    try:
        # 获取参数
        time_range = request.args.get('time_range', 'month')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        include_chart = request.args.get('include_chart', 'true').lower() == 'true'
        
        # 转换日期
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_frequency_statistics(
            user_id=current_user['id'],
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            include_chart=include_chart
        )
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取训练频率统计失败: {str(e)}"
        }), 500


# ==================== 训练时长统计 ====================

@analytics_bp.route('/duration', methods=['GET'])
@token_required
def get_duration_statistics(current_user):
    """
    获取训练时长统计
    ---
    查询参数:
        - time_range: 时间范围
        - start_date: 开始日期
        - end_date: 结束日期
        - include_chart: 是否包含图表
    """
    try:
        time_range = request.args.get('time_range', 'month')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        include_chart = request.args.get('include_chart', 'true').lower() == 'true'
        
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_duration_statistics(
            user_id=current_user['id'],
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            include_chart=include_chart
        )
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取训练时长统计失败: {str(e)}"
        }), 500


# ==================== 力量进步分析 ====================

@analytics_bp.route('/strength-progress', methods=['GET'])
@token_required
def get_strength_progress(current_user):
    """
    获取力量进步曲线
    ---
    查询参数:
        - exercise_id: 运动ID (可选,不传则返回所有)
        - time_range: 时间范围
        - start_date: 开始日期
        - end_date: 结束日期
        - include_chart: 是否包含图表
    """
    try:
        exercise_id = request.args.get('exercise_id', type=int)
        time_range = request.args.get('time_range', 'all')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        include_chart = request.args.get('include_chart', 'true').lower() == 'true'
        
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_strength_progress(
            user_id=current_user['id'],
            exercise_id=exercise_id,
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            include_chart=include_chart
        )
        
        return jsonify({
            "code": 200,
            "data": [p.model_dump(mode='json') for p in result]
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取力量进步数据失败: {str(e)}"
        }), 500


# ==================== 身体数据趋势 ====================

@analytics_bp.route('/body-trends', methods=['GET'])
@token_required
def get_body_data_trends(current_user):
    """
    获取身体数据变化趋势
    ---
    查询参数:
        - metrics: 指标列表 (逗号分隔,如: weight,body_fat)
        - time_range: 时间范围
        - start_date: 开始日期
        - end_date: 结束日期
        - include_chart: 是否包含图表
    """
    try:
        metrics_str = request.args.get('metrics', 'weight')
        metrics = [m.strip() for m in metrics_str.split(',')]
        
        time_range = request.args.get('time_range', 'month')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        include_chart = request.args.get('include_chart', 'true').lower() == 'true'
        
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_body_data_trends(
            user_id=current_user['id'],
            metrics=metrics,
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            include_chart=include_chart
        )
        
        return jsonify({
            "code": 200,
            "data": [t.model_dump(mode='json') for t in result]
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取身体数据趋势失败: {str(e)}"
        }), 500


# ==================== 卡路里统计 ====================

@analytics_bp.route('/calories', methods=['GET'])
@token_required
def get_calorie_statistics(current_user):
    """
    获取卡路里统计
    ---
    查询参数:
        - time_range: 时间范围
        - start_date: 开始日期
        - end_date: 结束日期
        - include_chart: 是否包含图表
    """
    try:
        time_range = request.args.get('time_range', 'month')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        include_chart = request.args.get('include_chart', 'true').lower() == 'true'
        
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_calorie_statistics(
            user_id=current_user['id'],
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            include_chart=include_chart
        )
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取卡路里统计失败: {str(e)}"
        }), 500


# ==================== 训练容量统计 ====================

@analytics_bp.route('/volume', methods=['GET'])
@token_required
def get_volume_statistics(current_user):
    """
    获取训练容量统计
    ---
    查询参数:
        - time_range: 时间范围
        - start_date: 开始日期
        - end_date: 结束日期
        - include_chart: 是否包含图表
    """
    try:
        time_range = request.args.get('time_range', 'month')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        include_chart = request.args.get('include_chart', 'true').lower() == 'true'
        
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_volume_statistics(
            user_id=current_user['id'],
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            include_chart=include_chart
        )
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取训练容量统计失败: {str(e)}"
        }), 500


# ==================== 成就统计 ====================

@analytics_bp.route('/achievements', methods=['GET'])
@token_required
def get_achievement_summary(current_user):
    """
    获取成就汇总
    """
    try:
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_achievement_summary(user_id=current_user['id'])
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取成就统计失败: {str(e)}"
        }), 500


# ==================== 综合仪表盘 ====================

@analytics_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_data(current_user):
    """
    获取综合仪表盘数据
    ---
    查询参数:
        - time_range: 时间范围 (默认: week)
        - include_charts: 是否包含图表 (默认: true)
    
    返回综合统计数据,包括:
    - 训练频率
    - 训练时长
    - 卡路里消耗
    - 力量汇总
    - 身体数据汇总
    - 成就汇总
    - 图表列表
    """
    try:
        time_range = request.args.get('time_range', 'week')
        include_charts = request.args.get('include_charts', 'true').lower() == 'true'
        
        db = next(get_db())
        service = AnalyticsService(db)
        
        result = service.get_dashboard_data(
            user_id=current_user['id'],
            time_range=time_range,
            include_charts=include_charts
        )
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取仪表盘数据失败: {str(e)}"
        }), 500


# ==================== 排行榜 ====================

@analytics_bp.route('/leaderboard', methods=['GET'])
@token_required
def get_leaderboard(current_user):
    """
    获取排行榜
    ---
    查询参数:
        - metric: 排名指标 (workouts/duration/calories/volume/achievements)
        - time_range: 时间范围 (week/month/quarter/year)
        - limit: 返回数量 (默认: 10, 最大: 100)
        - scope: 范围 (global/friends/following, 默认: global)
    """
    try:
        metric = request.args.get('metric', 'workouts')
        time_range = request.args.get('time_range', 'month')
        limit = int(request.args.get('limit', 10))
        scope = request.args.get('scope', 'global')
        
        # 验证参数
        if limit > 100:
            limit = 100
        
        valid_metrics = ['workouts', 'duration', 'calories', 'volume', 'achievements']
        if metric not in valid_metrics:
            return jsonify({
                "code": 400,
                "message": f"无效的排名指标,支持: {', '.join(valid_metrics)}"
            }), 400
        
        db = next(get_db())
        service = LeaderboardService(db)
        
        result = service.get_leaderboard(
            current_user_id=current_user['id'],
            metric=metric,
            time_range=time_range,
            limit=limit,
            scope=scope
        )
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取排行榜失败: {str(e)}"
        }), 500


# ==================== 用户对比 ====================

@analytics_bp.route('/comparison', methods=['POST'])
@token_required
def compare_users(current_user):
    """
    用户对比分析
    ---
    请求体:
        - user_ids: 对比用户IDs (包含当前用户)
        - metrics: 对比指标列表
        - time_range: 时间范围
    """
    try:
        data = request.get_json()
        
        # 验证
        query = ComparisonQuery(**data)
        
        db = next(get_db())
        service = ComparisonService(db)
        
        result = service.compare_users(
            current_user_id=current_user['id'],
            user_ids=query.user_ids,
            metrics=query.metrics,
            time_range=query.time_range
        )
        
        return jsonify({
            "code": 200,
            "data": result.model_dump(mode='json')
        }), 200
        
    except ValidationError as e:
        return jsonify({
            "code": 400,
            "message": "数据验证失败",
            "errors": e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"用户对比失败: {str(e)}"
        }), 500


# ==================== 数据概览 ====================

@analytics_bp.route('/overview', methods=['GET'])
@token_required
def get_overview(current_user):
    """
    获取数据概览
    
    快速获取关键指标汇总
    """
    try:
        db = next(get_db())
        service = AnalyticsService(db)
        
        # 获取本周和本月数据
        week_stats = service.get_dashboard_data(
            user_id=current_user['id'],
            time_range='week',
            include_charts=False
        )
        
        month_stats = service.get_dashboard_data(
            user_id=current_user['id'],
            time_range='month',
            include_charts=False
        )
        
        overview = {
            "this_week": {
                "workouts": week_stats.frequency.total_workouts,
                "duration": week_stats.duration.total_duration,
                "calories": week_stats.calories.total_calories,
                "streak": week_stats.frequency.current_streak
            },
            "this_month": {
                "workouts": month_stats.frequency.total_workouts,
                "duration": month_stats.duration.total_duration,
                "calories": month_stats.calories.total_calories,
                "frequency_rate": month_stats.frequency.frequency_rate
            },
            "achievements": {
                "total": month_stats.achievements.total_achievements,
                "unlocked": month_stats.achievements.unlocked_count,
                "points": month_stats.achievements.earned_points
            }
        }
        
        return jsonify({
            "code": 200,
            "data": overview
        }), 200
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取数据概览失败: {str(e)}"
        }), 500


# ==================== 错误处理 ====================

@analytics_bp.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        "code": 404,
        "message": "接口不存在"
    }), 404


@analytics_bp.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        "code": 500,
        "message": "服务器内部错误"
    }), 500
