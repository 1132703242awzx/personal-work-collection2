"""
运动记录服务层
处理运动记录的业务逻辑
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy import and_, or_, desc, func, extract
from sqlalchemy.orm import joinedload
from config.database import db_session
from models import User
from models.workout import WorkoutRecord, ExerciseRecord, SetRecord
from models.training import TrainingPlan, Exercise


class WorkoutService:
    """运动记录服务类"""
    
    @staticmethod
    def create_workout(user_id: int, workout_data: Dict) -> WorkoutRecord:
        """
        创建训练记录
        
        Args:
            user_id: 用户ID
            workout_data: 训练数据
            
        Returns:
            创建的训练记录
        """
        # 验证用户存在
        user = db_session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("用户不存在")
        
        # 如果指定了训练计划，验证计划存在且属于该用户
        if workout_data.get('training_plan_id'):
            plan = db_session.query(TrainingPlan).filter(
                and_(
                    TrainingPlan.id == workout_data['training_plan_id'],
                    TrainingPlan.user_id == user_id,
                    TrainingPlan.deleted_at.is_(None)
                )
            ).first()
            if not plan:
                raise ValueError("训练计划不存在或无权访问")
        
        # 创建训练记录
        workout = WorkoutRecord(
            user_id=user_id,
            training_plan_id=workout_data.get('training_plan_id'),
            workout_name=workout_data['workout_name'],
            workout_type=workout_data['workout_type'],
            workout_date=workout_data.get('workout_date', datetime.utcnow()),
            start_time=workout_data.get('start_time', datetime.utcnow()),
            location=workout_data.get('location'),
            weather=workout_data.get('weather'),
            is_completed=False
        )
        
        db_session.add(workout)
        db_session.flush()  # 获取workout ID
        
        # 批量创建动作记录和组记录
        if 'exercises' in workout_data:
            WorkoutService._create_exercise_records(
                workout.id, 
                workout_data['exercises']
            )
        
        db_session.commit()
        db_session.refresh(workout)
        
        return workout
    
    @staticmethod
    def _create_exercise_records(workout_id: int, exercises_data: List[Dict]):
        """
        批量创建动作记录（性能优化）
        
        Args:
            workout_id: 训练记录ID
            exercises_data: 动作数据列表
        """
        exercise_records = []
        set_records = []
        
        for exercise_data in exercises_data:
            # 创建动作记录
            exercise_record = ExerciseRecord(
                workout_record_id=workout_id,
                exercise_id=exercise_data.get('exercise_id'),
                exercise_name=exercise_data['exercise_name'],
                muscle_group=exercise_data.get('muscle_group'),
                exercise_type=exercise_data.get('exercise_type'),
                order_number=exercise_data['order_number'],
                planned_sets=exercise_data['planned_sets'],
                notes=exercise_data.get('notes')
            )
            db_session.add(exercise_record)
            db_session.flush()  # 获取exercise_record ID
            exercise_records.append(exercise_record)
            
            # 创建组记录
            if 'sets' in exercise_data:
                for set_data in exercise_data['sets']:
                    set_record = SetRecord(
                        exercise_record_id=exercise_record.id,
                        set_number=set_data['set_number'],
                        set_type=set_data.get('set_type', 'normal'),
                        reps=set_data.get('reps'),
                        weight=set_data.get('weight'),
                        duration=set_data.get('duration'),
                        distance=set_data.get('distance'),
                        rest_time=set_data.get('rest_time'),
                        avg_heart_rate=set_data.get('avg_heart_rate'),
                        max_heart_rate=set_data.get('max_heart_rate'),
                        is_completed=set_data.get('is_completed', True),
                        is_failed=set_data.get('is_failed', False),
                        difficulty_rating=set_data.get('difficulty_rating'),
                        notes=set_data.get('notes')
                    )
                    set_records.append(set_record)
        
        # 批量插入组记录
        if set_records:
            db_session.bulk_save_objects(set_records)
    
    @staticmethod
    def get_workouts(user_id: int, filters: Dict, page: int = 1, 
                    per_page: int = 20) -> Tuple[List[WorkoutRecord], int]:
        """
        获取训练记录列表
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            page: 页码
            per_page: 每页数量
            
        Returns:
            (训练记录列表, 总数)
        """
        query = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        )
        
        # 日期范围筛选
        if filters.get('start_date'):
            start_date = datetime.strptime(filters['start_date'], '%Y-%m-%d')
            query = query.filter(WorkoutRecord.workout_date >= start_date)
        
        if filters.get('end_date'):
            end_date = datetime.strptime(filters['end_date'], '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)
            query = query.filter(WorkoutRecord.workout_date <= end_date)
        
        # 训练类型筛选
        if filters.get('workout_type'):
            query = query.filter(WorkoutRecord.workout_type == filters['workout_type'])
        
        # 训练计划筛选
        if filters.get('training_plan_id'):
            query = query.filter(WorkoutRecord.training_plan_id == filters['training_plan_id'])
        
        # 完成状态筛选
        if filters.get('is_completed') is not None:
            query = query.filter(WorkoutRecord.is_completed == filters['is_completed'])
        
        # 关键词搜索
        if filters.get('keyword'):
            keyword = f"%{filters['keyword']}%"
            query = query.filter(
                or_(
                    WorkoutRecord.workout_name.like(keyword),
                    WorkoutRecord.notes.like(keyword),
                    WorkoutRecord.location.like(keyword)
                )
            )
        
        # 排序
        order_by = filters.get('order_by', 'workout_date')
        order_direction = filters.get('order_direction', 'desc')
        
        if hasattr(WorkoutRecord, order_by):
            order_column = getattr(WorkoutRecord, order_by)
            if order_direction == 'desc':
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(order_column)
        else:
            query = query.order_by(desc(WorkoutRecord.workout_date))
        
        # 总数
        total = query.count()
        
        # 分页
        workouts = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return workouts, total
    
    @staticmethod
    def get_workout_detail(workout_id: int, user_id: int) -> Optional[WorkoutRecord]:
        """
        获取训练记录详情
        
        Args:
            workout_id: 训练记录ID
            user_id: 用户ID
            
        Returns:
            训练记录详情
        """
        workout = db_session.query(WorkoutRecord).options(
            joinedload(WorkoutRecord.exercise_records)
                .joinedload(ExerciseRecord.set_records)
        ).filter(
            and_(
                WorkoutRecord.id == workout_id,
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).first()
        
        return workout
    
    @staticmethod
    def update_workout(workout_id: int, user_id: int, 
                      update_data: Dict) -> WorkoutRecord:
        """
        更新训练记录
        
        Args:
            workout_id: 训练记录ID
            user_id: 用户ID
            update_data: 更新数据
            
        Returns:
            更新后的记录
        """
        workout = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.id == workout_id,
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).first()
        
        if not workout:
            raise ValueError("训练记录不存在")
        
        # 更新字段
        for key, value in update_data.items():
            if hasattr(workout, key) and value is not None:
                setattr(workout, key, value)
        
        db_session.commit()
        db_session.refresh(workout)
        
        return workout
    
    @staticmethod
    def finish_workout(workout_id: int, user_id: int, 
                      finish_data: Dict) -> WorkoutRecord:
        """
        完成训练
        
        Args:
            workout_id: 训练记录ID
            user_id: 用户ID
            finish_data: 完成数据
            
        Returns:
            更新后的记录
        """
        workout = db_session.query(WorkoutRecord).options(
            joinedload(WorkoutRecord.exercise_records)
                .joinedload(ExerciseRecord.set_records)
        ).filter(
            and_(
                WorkoutRecord.id == workout_id,
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).first()
        
        if not workout:
            raise ValueError("训练记录不存在")
        
        # 设置结束时间
        workout.end_time = finish_data.get('end_time', datetime.utcnow())
        workout.is_completed = True
        
        # 计算训练时长
        if workout.start_time and workout.end_time:
            duration = workout.end_time - workout.start_time
            workout.duration = int(duration.total_seconds() / 60)  # 分钟
        
        # 更新评分和笔记
        if finish_data.get('difficulty_rating'):
            workout.difficulty_rating = finish_data['difficulty_rating']
        if finish_data.get('fatigue_level'):
            workout.fatigue_level = finish_data['fatigue_level']
        if finish_data.get('mood_rating'):
            workout.mood_rating = finish_data['mood_rating']
        if finish_data.get('notes'):
            workout.notes = finish_data['notes']
        
        # 计算统计数据
        WorkoutService._calculate_workout_stats(workout)
        
        # 检查并标记个人记录
        WorkoutService._check_personal_records(workout, user_id)
        
        # 更新训练计划完成率
        if workout.training_plan_id:
            WorkoutService._update_plan_completion(workout.training_plan_id, user_id)
        
        db_session.commit()
        db_session.refresh(workout)
        
        return workout
    
    @staticmethod
    def _calculate_workout_stats(workout: WorkoutRecord):
        """
        计算训练统计数据
        
        Args:
            workout: 训练记录
        """
        total_sets = 0
        total_reps = 0
        total_weight = 0.0
        total_distance = 0.0
        calories = 0
        completed_exercises = 0
        
        for exercise_record in workout.exercise_records:
            # 计算动作统计
            exercise_total_reps = 0
            exercise_total_weight = 0.0
            exercise_total_duration = 0
            exercise_calories = 0
            completed_sets = 0
            max_weight = 0.0
            max_reps = 0
            
            for set_record in exercise_record.set_records:
                if set_record.is_completed:
                    total_sets += 1
                    completed_sets += 1
                    
                    if set_record.reps:
                        exercise_total_reps += set_record.reps
                        total_reps += set_record.reps
                        max_reps = max(max_reps, set_record.reps)
                    
                    if set_record.weight:
                        exercise_total_weight += set_record.weight * (set_record.reps or 1)
                        total_weight += set_record.weight * (set_record.reps or 1)
                        max_weight = max(max_weight, set_record.weight)
                    
                    if set_record.duration:
                        exercise_total_duration += set_record.duration
                    
                    if set_record.distance:
                        total_distance += set_record.distance
                    
                    # 简单的卡路里估算
                    exercise_calories += WorkoutService._estimate_calories(
                        set_record, exercise_record.exercise_type
                    )
            
            # 更新动作记录统计
            exercise_record.completed_sets = completed_sets
            exercise_record.total_reps = exercise_total_reps
            exercise_record.total_weight = exercise_total_weight
            exercise_record.total_duration = exercise_total_duration
            exercise_record.calories_burned = exercise_calories
            exercise_record.max_weight = max_weight if max_weight > 0 else None
            exercise_record.max_reps = max_reps if max_reps > 0 else None
            
            calories += exercise_calories
            
            if completed_sets >= exercise_record.planned_sets:
                completed_exercises += 1
        
        # 更新训练记录统计
        workout.total_sets = total_sets
        workout.total_reps = total_reps
        workout.total_weight = total_weight
        workout.total_distance = total_distance
        workout.calories_burned = calories
        
        # 计算完成率
        total_exercises = len(workout.exercise_records)
        if total_exercises > 0:
            workout.completion_rate = int((completed_exercises / total_exercises) * 100)
    
    @staticmethod
    def _estimate_calories(set_record: SetRecord, exercise_type: str) -> int:
        """
        估算卡路里消耗
        
        Args:
            set_record: 组记录
            exercise_type: 动作类型
            
        Returns:
            估算的卡路里
        """
        calories = 0
        
        # 简单的估算公式（实际应根据具体动作和用户数据精确计算）
        if exercise_type == '力量':
            if set_record.reps and set_record.weight:
                # 力量训练：重量 * 次数 * 0.1
                calories = int(set_record.weight * set_record.reps * 0.1)
        elif exercise_type == '有氧':
            if set_record.duration:
                # 有氧训练：时长(分钟) * 8
                calories = int((set_record.duration / 60) * 8)
        
        return max(calories, 0)
    
    @staticmethod
    def _check_personal_records(workout: WorkoutRecord, user_id: int):
        """
        检查并标记个人记录
        
        Args:
            workout: 训练记录
            user_id: 用户ID
        """
        for exercise_record in workout.exercise_records:
            # 查询该用户该动作的历史最佳
            historical_best = db_session.query(
                func.max(ExerciseRecord.max_weight).label('max_weight'),
                func.max(ExerciseRecord.max_reps).label('max_reps')
            ).join(WorkoutRecord).filter(
                and_(
                    WorkoutRecord.user_id == user_id,
                    ExerciseRecord.exercise_name == exercise_record.exercise_name,
                    ExerciseRecord.id != exercise_record.id,
                    WorkoutRecord.deleted_at.is_(None)
                )
            ).first()
            
            is_pr = False
            
            # 判断是否创造新纪录
            if exercise_record.max_weight:
                if not historical_best.max_weight or \
                   exercise_record.max_weight > historical_best.max_weight:
                    is_pr = True
            
            if exercise_record.max_reps:
                if not historical_best.max_reps or \
                   exercise_record.max_reps > historical_best.max_reps:
                    is_pr = True
            
            exercise_record.is_personal_record = is_pr
    
    @staticmethod
    def _update_plan_completion(plan_id: int, user_id: int):
        """
        更新训练计划完成率
        
        Args:
            plan_id: 计划ID
            user_id: 用户ID
        """
        # 获取计划总天数
        plan = db_session.query(TrainingPlan).filter_by(id=plan_id).first()
        if not plan:
            return
        
        total_days = plan.duration_weeks * plan.days_per_week
        
        # 获取已完成的训练天数
        completed_days = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.training_plan_id == plan_id,
                WorkoutRecord.is_completed == True,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).count()
        
        # 更新完成率
        plan.completion_rate = int((completed_days / total_days * 100)) if total_days > 0 else 0
    
    @staticmethod
    def delete_workout(workout_id: int, user_id: int) -> bool:
        """
        删除训练记录
        
        Args:
            workout_id: 训练记录ID
            user_id: 用户ID
            
        Returns:
            是否成功
        """
        workout = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.id == workout_id,
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).first()
        
        if not workout:
            raise ValueError("训练记录不存在")
        
        # 软删除
        workout.deleted_at = datetime.utcnow()
        db_session.commit()
        
        return True
    
    @staticmethod
    def add_exercise_to_workout(workout_id: int, user_id: int, 
                               exercise_data: Dict) -> ExerciseRecord:
        """
        向训练记录添加动作
        
        Args:
            workout_id: 训练记录ID
            user_id: 用户ID
            exercise_data: 动作数据
            
        Returns:
            创建的动作记录
        """
        workout = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.id == workout_id,
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).first()
        
        if not workout:
            raise ValueError("训练记录不存在")
        
        if workout.is_completed:
            raise ValueError("训练已完成，无法添加动作")
        
        # 创建动作记录
        exercise_record = ExerciseRecord(
            workout_record_id=workout_id,
            exercise_id=exercise_data.get('exercise_id'),
            exercise_name=exercise_data['exercise_name'],
            muscle_group=exercise_data.get('muscle_group'),
            exercise_type=exercise_data.get('exercise_type'),
            order_number=exercise_data['order_number'],
            planned_sets=exercise_data['planned_sets'],
            notes=exercise_data.get('notes')
        )
        
        db_session.add(exercise_record)
        db_session.flush()
        
        # 添加组记录
        if 'sets' in exercise_data:
            for set_data in exercise_data['sets']:
                set_record = SetRecord(
                    exercise_record_id=exercise_record.id,
                    **set_data
                )
                db_session.add(set_record)
        
        db_session.commit()
        db_session.refresh(exercise_record)
        
        return exercise_record
    
    @staticmethod
    def add_set_to_exercise(exercise_record_id: int, user_id: int, 
                           set_data: Dict) -> SetRecord:
        """
        向动作记录添加组
        
        Args:
            exercise_record_id: 动作记录ID
            user_id: 用户ID
            set_data: 组数据
            
        Returns:
            创建的组记录
        """
        # 验证动作记录存在且属于该用户
        exercise_record = db_session.query(ExerciseRecord).join(
            WorkoutRecord
        ).filter(
            and_(
                ExerciseRecord.id == exercise_record_id,
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).first()
        
        if not exercise_record:
            raise ValueError("动作记录不存在")
        
        if exercise_record.workout_record.is_completed:
            raise ValueError("训练已完成，无法添加组")
        
        # 创建组记录
        set_record = SetRecord(
            exercise_record_id=exercise_record_id,
            **set_data
        )
        
        db_session.add(set_record)
        db_session.commit()
        db_session.refresh(set_record)
        
        return set_record
    
    @staticmethod
    def update_set(set_id: int, user_id: int, update_data: Dict) -> SetRecord:
        """
        更新组记录
        
        Args:
            set_id: 组记录ID
            user_id: 用户ID
            update_data: 更新数据
            
        Returns:
            更新后的记录
        """
        # 验证组记录存在且属于该用户
        set_record = db_session.query(SetRecord).join(
            ExerciseRecord
        ).join(
            WorkoutRecord
        ).filter(
            and_(
                SetRecord.id == set_id,
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).first()
        
        if not set_record:
            raise ValueError("组记录不存在")
        
        # 更新字段
        for key, value in update_data.items():
            if hasattr(set_record, key) and value is not None:
                setattr(set_record, key, value)
        
        db_session.commit()
        db_session.refresh(set_record)
        
        return set_record
    
    @staticmethod
    def get_calendar(user_id: int, year: int, month: int) -> Dict:
        """
        获取训练日历
        
        Args:
            user_id: 用户ID
            year: 年份
            month: 月份
            
        Returns:
            日历数据
        """
        # 查询该月的所有训练记录
        workouts = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                extract('year', WorkoutRecord.workout_date) == year,
                extract('month', WorkoutRecord.workout_date) == month,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).all()
        
        # 按日期分组
        calendar_data = {}
        for workout in workouts:
            date_key = workout.workout_date.strftime('%Y-%m-%d')
            if date_key not in calendar_data:
                calendar_data[date_key] = []
            
            calendar_data[date_key].append({
                'id': workout.id,
                'workout_name': workout.workout_name,
                'workout_type': workout.workout_type,
                'duration': workout.duration,
                'calories_burned': workout.calories_burned,
                'is_completed': workout.is_completed
            })
        
        return {
            'year': year,
            'month': month,
            'calendar': calendar_data
        }
    
    @staticmethod
    def get_personal_records(user_id: int) -> List[Dict]:
        """
        获取个人最佳记录
        
        Args:
            user_id: 用户ID
            
        Returns:
            个人记录列表
        """
        # 查询所有标记为PR的记录
        pr_records = db_session.query(ExerciseRecord).join(
            WorkoutRecord
        ).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                ExerciseRecord.is_personal_record == True,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).order_by(desc(WorkoutRecord.workout_date)).all()
        
        # 按动作分组，保留最新的PR
        records_dict = {}
        for record in pr_records:
            if record.exercise_name not in records_dict:
                records_dict[record.exercise_name] = {
                    'exercise_name': record.exercise_name,
                    'muscle_group': record.muscle_group,
                    'max_weight': record.max_weight,
                    'max_reps': record.max_reps,
                    'workout_date': record.workout_record.workout_date,
                    'workout_id': record.workout_record_id
                }
        
        return list(records_dict.values())
