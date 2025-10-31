"""
训练计划服务层
处理训练计划的业务逻辑
"""
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import joinedload
from config.database import db_session
from models import User
from models.training import TrainingPlan, PlanDay, Exercise, DifficultyEnum, MuscleGroupEnum
from models.workout import WorkoutRecord


class TrainingService:
    """训练计划服务类"""
    
    @staticmethod
    def create_plan(user_id: int, plan_data: Dict) -> TrainingPlan:
        """
        创建训练计划
        
        Args:
            user_id: 用户ID
            plan_data: 计划数据
            
        Returns:
            创建的训练计划
        """
        # 验证用户存在
        user = db_session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("用户不存在")
        
        # 如果有激活的计划，先取消激活
        if plan_data.get('is_active', False):
            db_session.query(TrainingPlan).filter(
                and_(
                    TrainingPlan.user_id == user_id,
                    TrainingPlan.is_active == True,
                    TrainingPlan.deleted_at.is_(None)
                )
            ).update({'is_active': False})
        
        # 创建训练计划
        training_plan = TrainingPlan(
            user_id=user_id,
            name=plan_data['name'],
            description=plan_data.get('description'),
            cover_image=plan_data.get('cover_image'),
            difficulty=DifficultyEnum(plan_data['difficulty']),
            duration_weeks=plan_data['duration_weeks'],
            days_per_week=plan_data['days_per_week'],
            goal=plan_data.get('goal'),
            target_muscle_group=MuscleGroupEnum(plan_data['target_muscle_group']) if plan_data.get('target_muscle_group') else None,
            is_active=plan_data.get('is_active', False),
            is_template=plan_data.get('is_template', False),
            is_public=plan_data.get('is_public', False)
        )
        
        db_session.add(training_plan)
        db_session.flush()  # 获取plan ID
        
        # 创建训练日
        if 'plan_days' in plan_data:
            for day_data in plan_data['plan_days']:
                plan_day = PlanDay(
                    training_plan_id=training_plan.id,
                    day_number=day_data['day_number'],
                    day_name=day_data.get('day_name'),
                    description=day_data.get('description'),
                    warm_up=day_data.get('warm_up'),
                    cool_down=day_data.get('cool_down'),
                    estimated_duration=day_data.get('estimated_duration'),
                    target_calories=day_data.get('target_calories'),
                    rest_time=day_data.get('rest_time', 60)
                )
                db_session.add(plan_day)
                db_session.flush()
                
                # 创建动作
                if 'exercises' in day_data:
                    for exercise_data in day_data['exercises']:
                        exercise = Exercise(
                            plan_day_id=plan_day.id,
                            name=exercise_data['name'],
                            description=exercise_data.get('description'),
                            video_url=exercise_data.get('video_url'),
                            image_url=exercise_data.get('image_url'),
                            exercise_type=exercise_data['exercise_type'],
                            muscle_group=MuscleGroupEnum(exercise_data['muscle_group']),
                            equipment=exercise_data.get('equipment'),
                            order_number=exercise_data['order_number'],
                            sets=exercise_data.get('sets'),
                            reps=exercise_data.get('reps'),
                            duration=exercise_data.get('duration'),
                            weight=exercise_data.get('weight'),
                            rest_time=exercise_data.get('rest_time', 60),
                            difficulty=DifficultyEnum(exercise_data['difficulty']) if exercise_data.get('difficulty') else None,
                            calories_per_set=exercise_data.get('calories_per_set'),
                            key_points=exercise_data.get('key_points'),
                            common_mistakes=exercise_data.get('common_mistakes')
                        )
                        db_session.add(exercise)
        
        db_session.commit()
        db_session.refresh(training_plan)
        
        return training_plan
    
    @staticmethod
    def get_plans(user_id: int, filters: Dict, page: int = 1, per_page: int = 20) -> Tuple[List[TrainingPlan], int]:
        """
        获取训练计划列表（支持分页和筛选）
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            page: 页码
            per_page: 每页数量
            
        Returns:
            (计划列表, 总数)
        """
        query = db_session.query(TrainingPlan).filter(
            TrainingPlan.deleted_at.is_(None)
        )
        
        # 筛选条件
        if filters.get('my_plans'):
            # 我的计划（包括我创建的和我复制的模板）
            query = query.filter(TrainingPlan.user_id == user_id)
        elif filters.get('templates'):
            # 公开模板
            query = query.filter(
                and_(
                    TrainingPlan.is_template == True,
                    TrainingPlan.is_public == True
                )
            )
        else:
            # 默认：我的计划 + 公开模板
            query = query.filter(
                or_(
                    TrainingPlan.user_id == user_id,
                    and_(
                        TrainingPlan.is_template == True,
                        TrainingPlan.is_public == True
                    )
                )
            )
        
        # 难度筛选
        if filters.get('difficulty'):
            query = query.filter(TrainingPlan.difficulty == DifficultyEnum(filters['difficulty']))
        
        # 目标肌群筛选
        if filters.get('target_muscle_group'):
            query = query.filter(TrainingPlan.target_muscle_group == MuscleGroupEnum(filters['target_muscle_group']))
        
        # 训练目标筛选
        if filters.get('goal'):
            query = query.filter(TrainingPlan.goal == filters['goal'])
        
        # 激活状态筛选
        if filters.get('is_active') is not None:
            query = query.filter(TrainingPlan.is_active == filters['is_active'])
        
        # 搜索
        if filters.get('keyword'):
            keyword = f"%{filters['keyword']}%"
            query = query.filter(
                or_(
                    TrainingPlan.name.like(keyword),
                    TrainingPlan.description.like(keyword)
                )
            )
        
        # 排序
        order_by = filters.get('order_by', 'created_at')
        if order_by == 'usage_count':
            query = query.order_by(desc(TrainingPlan.usage_count))
        elif order_by == 'completion_rate':
            query = query.order_by(desc(TrainingPlan.completion_rate))
        else:
            query = query.order_by(desc(TrainingPlan.created_at))
        
        # 总数
        total = query.count()
        
        # 分页
        plans = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return plans, total
    
    @staticmethod
    def get_plan_detail(plan_id: int, user_id: int) -> Optional[TrainingPlan]:
        """
        获取计划详情（包含所有训练日和动作）
        
        Args:
            plan_id: 计划ID
            user_id: 用户ID
            
        Returns:
            训练计划详情
        """
        plan = db_session.query(TrainingPlan).options(
            joinedload(TrainingPlan.plan_days).joinedload(PlanDay.exercises),
            joinedload(TrainingPlan.user)
        ).filter(
            and_(
                TrainingPlan.id == plan_id,
                TrainingPlan.deleted_at.is_(None)
            )
        ).first()
        
        if not plan:
            return None
        
        # 权限检查：只能查看自己的计划或公开的模板
        if plan.user_id != user_id and not (plan.is_template and plan.is_public):
            raise PermissionError("无权访问该计划")
        
        return plan
    
    @staticmethod
    def update_plan(plan_id: int, user_id: int, update_data: Dict) -> TrainingPlan:
        """
        更新训练计划
        
        Args:
            plan_id: 计划ID
            user_id: 用户ID
            update_data: 更新数据
            
        Returns:
            更新后的计划
        """
        plan = db_session.query(TrainingPlan).filter(
            and_(
                TrainingPlan.id == plan_id,
                TrainingPlan.deleted_at.is_(None)
            )
        ).first()
        
        if not plan:
            raise ValueError("计划不存在")
        
        # 权限检查
        if plan.user_id != user_id:
            raise PermissionError("无权修改该计划")
        
        # 如果要激活此计划，先取消其他计划的激活状态
        if update_data.get('is_active', False) and not plan.is_active:
            db_session.query(TrainingPlan).filter(
                and_(
                    TrainingPlan.user_id == user_id,
                    TrainingPlan.is_active == True,
                    TrainingPlan.id != plan_id,
                    TrainingPlan.deleted_at.is_(None)
                )
            ).update({'is_active': False})
        
        # 更新基础信息
        for key, value in update_data.items():
            if key in ['name', 'description', 'cover_image', 'goal', 'is_active', 'is_public']:
                setattr(plan, key, value)
            elif key == 'difficulty' and value:
                plan.difficulty = DifficultyEnum(value)
            elif key == 'target_muscle_group' and value:
                plan.target_muscle_group = MuscleGroupEnum(value)
            elif key in ['duration_weeks', 'days_per_week']:
                setattr(plan, key, value)
        
        # 更新训练日（如果提供）
        if 'plan_days' in update_data:
            # 删除现有训练日
            db_session.query(PlanDay).filter(
                PlanDay.training_plan_id == plan_id
            ).delete()
            
            # 创建新的训练日
            for day_data in update_data['plan_days']:
                plan_day = PlanDay(
                    training_plan_id=plan.id,
                    day_number=day_data['day_number'],
                    day_name=day_data.get('day_name'),
                    description=day_data.get('description'),
                    warm_up=day_data.get('warm_up'),
                    cool_down=day_data.get('cool_down'),
                    estimated_duration=day_data.get('estimated_duration'),
                    target_calories=day_data.get('target_calories'),
                    rest_time=day_data.get('rest_time', 60)
                )
                db_session.add(plan_day)
                db_session.flush()
                
                # 创建动作
                if 'exercises' in day_data:
                    for exercise_data in day_data['exercises']:
                        exercise = Exercise(
                            plan_day_id=plan_day.id,
                            name=exercise_data['name'],
                            description=exercise_data.get('description'),
                            video_url=exercise_data.get('video_url'),
                            image_url=exercise_data.get('image_url'),
                            exercise_type=exercise_data['exercise_type'],
                            muscle_group=MuscleGroupEnum(exercise_data['muscle_group']),
                            equipment=exercise_data.get('equipment'),
                            order_number=exercise_data['order_number'],
                            sets=exercise_data.get('sets'),
                            reps=exercise_data.get('reps'),
                            duration=exercise_data.get('duration'),
                            weight=exercise_data.get('weight'),
                            rest_time=exercise_data.get('rest_time', 60),
                            difficulty=DifficultyEnum(exercise_data['difficulty']) if exercise_data.get('difficulty') else None,
                            calories_per_set=exercise_data.get('calories_per_set'),
                            key_points=exercise_data.get('key_points'),
                            common_mistakes=exercise_data.get('common_mistakes')
                        )
                        db_session.add(exercise)
        
        db_session.commit()
        db_session.refresh(plan)
        
        return plan
    
    @staticmethod
    def delete_plan(plan_id: int, user_id: int) -> bool:
        """
        删除训练计划（软删除）
        
        Args:
            plan_id: 计划ID
            user_id: 用户ID
            
        Returns:
            是否成功
        """
        plan = db_session.query(TrainingPlan).filter(
            and_(
                TrainingPlan.id == plan_id,
                TrainingPlan.deleted_at.is_(None)
            )
        ).first()
        
        if not plan:
            raise ValueError("计划不存在")
        
        # 权限检查
        if plan.user_id != user_id:
            raise PermissionError("无权删除该计划")
        
        # 软删除
        plan.deleted_at = datetime.utcnow()
        db_session.commit()
        
        return True
    
    @staticmethod
    def start_plan(plan_id: int, user_id: int) -> TrainingPlan:
        """
        开始执行训练计划
        
        Args:
            plan_id: 计划ID
            user_id: 用户ID
            
        Returns:
            激活的计划
        """
        plan = db_session.query(TrainingPlan).filter(
            and_(
                TrainingPlan.id == plan_id,
                TrainingPlan.deleted_at.is_(None)
            )
        ).first()
        
        if not plan:
            raise ValueError("计划不存在")
        
        # 如果是模板，需要先复制一份
        if plan.is_template:
            plan = TrainingService.copy_template(plan_id, user_id)
        
        # 权限检查
        if plan.user_id != user_id:
            raise PermissionError("无权执行该计划")
        
        # 取消其他激活的计划
        db_session.query(TrainingPlan).filter(
            and_(
                TrainingPlan.user_id == user_id,
                TrainingPlan.is_active == True,
                TrainingPlan.id != plan.id,
                TrainingPlan.deleted_at.is_(None)
            )
        ).update({'is_active': False})
        
        # 激活当前计划
        plan.is_active = True
        plan.usage_count += 1
        db_session.commit()
        db_session.refresh(plan)
        
        return plan
    
    @staticmethod
    def copy_template(template_id: int, user_id: int) -> TrainingPlan:
        """
        复制模板计划
        
        Args:
            template_id: 模板ID
            user_id: 用户ID
            
        Returns:
            复制后的计划
        """
        template = db_session.query(TrainingPlan).options(
            joinedload(TrainingPlan.plan_days).joinedload(PlanDay.exercises)
        ).filter(
            and_(
                TrainingPlan.id == template_id,
                TrainingPlan.is_template == True,
                TrainingPlan.is_public == True,
                TrainingPlan.deleted_at.is_(None)
            )
        ).first()
        
        if not template:
            raise ValueError("模板不存在或不可用")
        
        # 创建新计划
        new_plan = TrainingPlan(
            user_id=user_id,
            name=f"{template.name} (副本)",
            description=template.description,
            cover_image=template.cover_image,
            difficulty=template.difficulty,
            duration_weeks=template.duration_weeks,
            days_per_week=template.days_per_week,
            goal=template.goal,
            target_muscle_group=template.target_muscle_group,
            is_active=False,
            is_template=False,
            is_public=False
        )
        
        db_session.add(new_plan)
        db_session.flush()
        
        # 复制训练日和动作
        for template_day in template.plan_days:
            new_day = PlanDay(
                training_plan_id=new_plan.id,
                day_number=template_day.day_number,
                day_name=template_day.day_name,
                description=template_day.description,
                warm_up=template_day.warm_up,
                cool_down=template_day.cool_down,
                estimated_duration=template_day.estimated_duration,
                target_calories=template_day.target_calories,
                rest_time=template_day.rest_time
            )
            db_session.add(new_day)
            db_session.flush()
            
            for template_exercise in template_day.exercises:
                new_exercise = Exercise(
                    plan_day_id=new_day.id,
                    name=template_exercise.name,
                    description=template_exercise.description,
                    video_url=template_exercise.video_url,
                    image_url=template_exercise.image_url,
                    exercise_type=template_exercise.exercise_type,
                    muscle_group=template_exercise.muscle_group,
                    equipment=template_exercise.equipment,
                    order_number=template_exercise.order_number,
                    sets=template_exercise.sets,
                    reps=template_exercise.reps,
                    duration=template_exercise.duration,
                    weight=template_exercise.weight,
                    rest_time=template_exercise.rest_time,
                    difficulty=template_exercise.difficulty,
                    calories_per_set=template_exercise.calories_per_set,
                    key_points=template_exercise.key_points,
                    common_mistakes=template_exercise.common_mistakes
                )
                db_session.add(new_exercise)
        
        # 增加模板使用次数
        template.usage_count += 1
        
        db_session.commit()
        db_session.refresh(new_plan)
        
        return new_plan
    
    @staticmethod
    def get_plan_progress(plan_id: int, user_id: int) -> Dict:
        """
        获取计划进度
        
        Args:
            plan_id: 计划ID
            user_id: 用户ID
            
        Returns:
            进度信息
        """
        plan = db_session.query(TrainingPlan).filter(
            and_(
                TrainingPlan.id == plan_id,
                TrainingPlan.user_id == user_id,
                TrainingPlan.deleted_at.is_(None)
            )
        ).first()
        
        if not plan:
            raise ValueError("计划不存在")
        
        # 获取总训练日数
        total_days = len(plan.plan_days)
        
        # 获取已完成的训练记录
        completed_workouts = db_session.query(WorkoutRecord).filter(
            and_(
                WorkoutRecord.user_id == user_id,
                WorkoutRecord.training_plan_id == plan_id,
                WorkoutRecord.is_completed == True,
                WorkoutRecord.deleted_at.is_(None)
            )
        ).count()
        
        # 计算完成率
        completion_rate = int((completed_workouts / total_days * 100)) if total_days > 0 else 0
        
        # 更新计划完成率
        plan.completion_rate = completion_rate
        db_session.commit()
        
        return {
            'plan_id': plan_id,
            'total_days': total_days,
            'completed_days': completed_workouts,
            'completion_rate': completion_rate,
            'duration_weeks': plan.duration_weeks,
            'days_per_week': plan.days_per_week
        }
