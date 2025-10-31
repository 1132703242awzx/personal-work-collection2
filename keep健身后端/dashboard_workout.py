"""
Keep健身仪表盘 - 运动记录蓝图
处理运动数据的录入、查看、编辑
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime

from dashboard_models import db, WorkoutRecord, BodyRecord

workout_bp = Blueprint('workout', __name__, url_prefix='/workout')


@workout_bp.route('/records')
@login_required
def records():
    """运动记录列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    all_records = WorkoutRecord.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutRecord.workout_date.desc())\
        .all()
    
    return render_template('workout/records.html', records=all_records)


@workout_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_record():
    """添加运动记录"""
    if request.method == 'GET':
        return render_template('workout/add.html', now=datetime.now())
    
    if request.method == 'POST':
        workout_type = request.form.get('workout_type')
        workout_name = request.form.get('workout_name')
        workout_date_str = request.form.get('workout_date')
        duration_str = request.form.get('duration')
        calories_str = request.form.get('calories')
        distance_str = request.form.get('distance')
        difficulty = request.form.get('difficulty')
        notes = request.form.get('notes')
        
        # 转换数据
        workout_date = datetime.strptime(workout_date_str, '%Y-%m-%d').date() if workout_date_str else datetime.today().date()
        duration = int(duration_str) if duration_str else None
        calories = int(calories_str) if calories_str else None
        distance = float(distance_str) if distance_str else None
        
        # 创建记录
        record = WorkoutRecord(
            user_id=current_user.id,
            workout_type=workout_type,
            workout_name=workout_name,
            workout_date=workout_date,
            duration=duration,
            calories=calories,
            distance=distance,
            difficulty=difficulty,
            notes=notes
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash('运动记录添加成功!', 'success')
        return redirect(url_for('workout.records'))
    
    return render_template('workout/add.html')


@workout_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_record(id):
    """编辑运动记录"""
    record = WorkoutRecord.query.get_or_404(id)
    
    # 权限检查
    if record.user_id != current_user.id:
        flash('无权限访问', 'danger')
        return redirect(url_for('workout.records'))
    
    if request.method == 'POST':
        record.workout_type = request.form.get('workout_type')
        record.workout_name = request.form.get('workout_name')
        
        workout_date_str = request.form.get('workout_date')
        if workout_date_str:
            record.workout_date = datetime.strptime(workout_date_str, '%Y-%m-%d').date()
        
        duration_str = request.form.get('duration')
        record.duration = int(duration_str) if duration_str else None
        
        calories_str = request.form.get('calories')
        record.calories = int(calories_str) if calories_str else None
        
        distance_str = request.form.get('distance')
        record.distance = float(distance_str) if distance_str else None
        
        record.difficulty = request.form.get('difficulty')
        record.notes = request.form.get('notes')
        
        db.session.commit()
        flash('运动记录更新成功!', 'success')
        return redirect(url_for('workout.records'))
    
    return render_template('workout/edit.html', record=record)


@workout_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_record(id):
    """删除运动记录"""
    record = WorkoutRecord.query.get_or_404(id)
    
    if record.user_id != current_user.id:
        flash('无权限访问', 'danger')
        return redirect(url_for('workout.records'))
    
    db.session.delete(record)
    db.session.commit()
    
    flash('运动记录已删除', 'info')
    return redirect(url_for('workout.records'))


@workout_bp.route('/body-records')
@login_required
def body_records():
    """身体数据记录列表"""
    all_records = BodyRecord.query.filter_by(user_id=current_user.id)\
        .order_by(BodyRecord.record_date.desc())\
        .all()
    
    return render_template('workout/body_records.html', records=all_records, now=datetime.now())


@workout_bp.route('/add-body-record', methods=['GET', 'POST'])
@login_required
def add_body_record():
    """添加身体数据记录"""
    if request.method == 'POST':
        record_date_str = request.form.get('record_date')
        weight_str = request.form.get('weight')
        body_fat_str = request.form.get('body_fat')
        notes = request.form.get('notes')
        
        record_date = datetime.strptime(record_date_str, '%Y-%m-%d').date() if record_date_str else datetime.today().date()
        weight = float(weight_str) if weight_str else None
        body_fat = float(body_fat_str) if body_fat_str else None
        
        if not weight:
            flash('请输入体重', 'danger')
            return redirect(url_for('workout.add_body_record'))
        
        record = BodyRecord(
            user_id=current_user.id,
            record_date=record_date,
            weight=weight,
            body_fat=body_fat,
            notes=notes
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash('身体数据记录添加成功!', 'success')
        return redirect(url_for('workout.body_records'))
    
    return render_template('workout/add_body.html')
