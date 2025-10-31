"""
Keep健身仪表盘 - 数据分析蓝图
提供统计分析和数据可视化
使用Pandas进行数据处理
"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
import pandas as pd

from dashboard_models import db, WorkoutRecord, BodyRecord

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


@analytics_bp.route('/overview')
@login_required
def overview():
    """数据概览页面"""
    # 计算统计数据
    total_workouts = WorkoutRecord.query.filter_by(user_id=current_user.id).count()
    
    total_result = db.session.query(
        func.sum(WorkoutRecord.calories),
        func.sum(WorkoutRecord.duration)
    ).filter(WorkoutRecord.user_id == current_user.id).first()
    
    total_calories = int(total_result[0]) if total_result[0] else 0
    total_duration = int(total_result[1]) if total_result[1] else 0
    avg_duration = int(total_duration / total_workouts) if total_workouts > 0 else 0
    
    return render_template('analytics/overview.html',
                         total_workouts=total_workouts,
                         total_calories=total_calories,
                         total_duration=total_duration,
                         avg_duration=avg_duration)


@analytics_bp.route('/workout-stats')
@login_required
def workout_stats():
    """运动统计页面"""
    return render_template('analytics/workout_stats.html')


@analytics_bp.route('/body-stats')
@login_required
def body_stats():
    """身体数据统计页面"""
    return render_template('analytics/body_stats.html')


@analytics_bp.route('/api/workout-trend')
@login_required
def api_workout_trend():
    """运动趋势数据API (用于Chart.js)"""
    days = request.args.get('days', 30, type=int)
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)
    
    # 查询数据
    records = WorkoutRecord.query.filter(
        WorkoutRecord.user_id == current_user.id,
        WorkoutRecord.workout_date >= start_date,
        WorkoutRecord.workout_date <= end_date
    ).all()
    
    # 使用Pandas处理数据
    if records:
        df = pd.DataFrame([{
            'date': r.workout_date,
            'calories': r.calories or 0,
            'duration': r.duration or 0,
            'distance': r.distance or 0
        } for r in records])
        
        # 按日期分组汇总
        df_grouped = df.groupby('date').agg({
            'calories': 'sum',
            'duration': 'sum',
            'distance': 'sum'
        }).reset_index()
        
        # 补全缺失日期
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        df_complete = pd.DataFrame({'date': date_range})
        df_complete['date'] = df_complete['date'].dt.date
        
        df_final = df_complete.merge(df_grouped, on='date', how='left').fillna(0)
        
        return jsonify({
            'labels': df_final['date'].astype(str).tolist(),
            'calories': df_final['calories'].tolist(),
            'duration': df_final['duration'].tolist(),
            'distance': df_final['distance'].tolist()
        })
    else:
        return jsonify({
            'labels': [],
            'calories': [],
            'duration': [],
            'distance': []
        })


@analytics_bp.route('/api/workout-type-distribution')
@login_required
def api_workout_type_distribution():
    """运动类型分布API"""
    # 查询最近30天的数据
    days = 30
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)
    
    results = db.session.query(
        WorkoutRecord.workout_type,
        func.count(WorkoutRecord.id).label('count')
    ).filter(
        WorkoutRecord.user_id == current_user.id,
        WorkoutRecord.workout_date >= start_date
    ).group_by(WorkoutRecord.workout_type).all()
    
    return jsonify({
        'labels': [r.workout_type for r in results],
        'data': [r.count for r in results]
    })


@analytics_bp.route('/api/body-weight-trend')
@login_required
def api_body_weight_trend():
    """体重趋势数据API"""
    days = request.args.get('days', 90, type=int)
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)
    
    records = BodyRecord.query.filter(
        BodyRecord.user_id == current_user.id,
        BodyRecord.record_date >= start_date,
        BodyRecord.record_date <= end_date
    ).order_by(BodyRecord.record_date).all()
    
    if records:
        df = pd.DataFrame([{
            'date': r.record_date,
            'weight': r.weight,
            'body_fat': r.body_fat or 0
        } for r in records])
        
        return jsonify({
            'labels': df['date'].astype(str).tolist(),
            'weight': df['weight'].tolist(),
            'body_fat': df['body_fat'].tolist()
        })
    else:
        return jsonify({
            'labels': [],
            'weight': [],
            'body_fat': []
        })


@analytics_bp.route('/api/body-data-trend')
@login_required
def api_body_data_trend():
    """身体数据趋势API (统一接口名)"""
    days = request.args.get('days', 90, type=int)
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)
    
    records = BodyRecord.query.filter(
        BodyRecord.user_id == current_user.id,
        BodyRecord.record_date >= start_date,
        BodyRecord.record_date <= end_date
    ).order_by(BodyRecord.record_date).all()
    
    if records:
        labels = []
        weights = []
        body_fats = []
        bmis = []
        
        for r in records:
            labels.append(r.record_date.strftime('%m-%d'))
            weights.append(float(r.weight))
            body_fats.append(float(r.body_fat) if r.body_fat else None)
            
            # 计算BMI
            if current_user.height and current_user.height > 0:
                bmi = r.weight / ((current_user.height / 100) ** 2)
                bmis.append(round(bmi, 1))
            else:
                bmis.append(None)
        
        return jsonify({
            'labels': labels,
            'weight': weights,
            'body_fat': [bf for bf in body_fats if bf is not None],
            'bmi': [b for b in bmis if b is not None]
        })
    else:
        return jsonify({
            'labels': [],
            'weight': [],
            'body_fat': [],
            'bmi': []
        })


@analytics_bp.route('/api/monthly-stats')
@login_required
def api_monthly_stats():
    """月度统计数据API"""
    # 获取最近6个月的数据
    records = WorkoutRecord.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutRecord.workout_date).all()
    
    if records:
        df = pd.DataFrame([{
            'date': r.workout_date,
            'month': r.workout_date.strftime('%Y-%m'),
        } for r in records])
        
        monthly = df.groupby('month').size().reset_index(name='count')
        
        return jsonify({
            'labels': monthly['month'].tolist()[-6:],  # 最近6个月
            'count': monthly['count'].tolist()[-6:]
        })
    else:
        return jsonify({
            'labels': [],
            'count': []
        })


@analytics_bp.route('/api/summary-stats')
@login_required
def api_summary_stats():
    """汇总统计数据API"""
    today = datetime.today().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # 总计
    total_workouts = WorkoutRecord.query.filter_by(user_id=current_user.id).count()
    total_calories = db.session.query(func.sum(WorkoutRecord.calories))\
        .filter(WorkoutRecord.user_id == current_user.id).scalar() or 0
    total_duration = db.session.query(func.sum(WorkoutRecord.duration))\
        .filter(WorkoutRecord.user_id == current_user.id).scalar() or 0
    
    # 本周
    week_workouts = WorkoutRecord.query.filter(
        WorkoutRecord.user_id == current_user.id,
        WorkoutRecord.workout_date >= week_ago
    ).count()
    
    # 本月
    month_calories = db.session.query(func.sum(WorkoutRecord.calories)).filter(
        WorkoutRecord.user_id == current_user.id,
        WorkoutRecord.workout_date >= month_ago
    ).scalar() or 0
    
    return jsonify({
        'total_workouts': total_workouts,
        'total_calories': int(total_calories),
        'total_duration': int(total_duration),
        'week_workouts': week_workouts,
        'month_calories': int(month_calories),
        'avg_duration': int(total_duration / total_workouts) if total_workouts > 0 else 0
    })
