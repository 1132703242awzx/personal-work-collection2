"""
Keep健身仪表盘 - 主蓝图
处理主页、仪表盘等核心页面
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta

from dashboard_models import db, WorkoutRecord, BodyRecord

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """仪表盘主页"""
    # 获取统计数据
    today = datetime.today().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # 总运动次数
    total_workouts = WorkoutRecord.query.filter_by(user_id=current_user.id).count()
    
    # 本周运动次数
    week_workouts = WorkoutRecord.query.filter(
        WorkoutRecord.user_id == current_user.id,
        WorkoutRecord.workout_date >= week_ago
    ).count()
    
    # 本月总卡路里
    month_calories = db.session.query(func.sum(WorkoutRecord.calories)).filter(
        WorkoutRecord.user_id == current_user.id,
        WorkoutRecord.workout_date >= month_ago
    ).scalar() or 0
    
    # 本月总时长(分钟)
    month_duration = db.session.query(func.sum(WorkoutRecord.duration)).filter(
        WorkoutRecord.user_id == current_user.id,
        WorkoutRecord.workout_date >= month_ago
    ).scalar() or 0
    
    # 最近运动记录
    recent_workouts = WorkoutRecord.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutRecord.workout_date.desc())\
        .limit(5).all()
    
    # 最新身体数据
    latest_body_record = BodyRecord.query.filter_by(user_id=current_user.id)\
        .order_by(BodyRecord.record_date.desc()).first()
    
    # BMI计算
    bmi = current_user.get_bmi()
    
    stats = {
        'total_workouts': total_workouts,
        'week_workouts': week_workouts,
        'month_calories': int(month_calories),
        'month_duration': int(month_duration),
        'bmi': bmi,
        'weight': current_user.get_latest_weight()
    }
    
    return render_template('dashboard/index.html',
                         stats=stats,
                         recent_workouts=recent_workouts,
                         latest_body_record=latest_body_record)


@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')
