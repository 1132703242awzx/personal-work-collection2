"""
训练计划API路由
提供训练计划的CRUD操作
"""
from flask import Blueprint, request, jsonify, g
from middleware.auth import token_required
from services.training_service import TrainingService
from models.training import DifficultyEnum, MuscleGroupEnum


training_bp = Blueprint('training', __name__, url_prefix='/api/plans')


@training_bp.route('', methods=['POST'])
@token_required
def create_plan():
    """
    创建训练计划
    
    请求体示例:
    {
        "name": "增肌训练计划",
        "description": "为期8周的增肌训练",
        "difficulty": "intermediate",
        "duration_weeks": 8,
        "days_per_week": 5,
        "goal": "增肌",
        "target_muscle_group": "full_body",
        "plan_days": [
            {
                "day_number": 1,
                "day_name": "胸部训练日",
                "description": "胸部和三头肌训练",
                "estimated_duration": 60,
                "exercises": [
                    {
                        "name": "卧推",
                        "exercise_type": "力量",
                        "muscle_group": "chest",
                        "order_number": 1,
                        "sets": 4,
                        "reps": 10,
                        "rest_time": 90,
                        "difficulty": "intermediate"
                    }
                ]
            }
        ]
    }
    """
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name', 'difficulty', 'duration_weeks', 'days_per_week']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 验证难度等级
        if data['difficulty'] not in [e.value for e in DifficultyEnum]:
            return jsonify({'error': '无效的难度等级'}), 400
        
        # 验证目标肌群
        if 'target_muscle_group' in data and data['target_muscle_group'] not in [e.value for e in MuscleGroupEnum]:
            return jsonify({'error': '无效的目标肌群'}), 400
        
        # 创建计划
        plan = TrainingService.create_plan(g.user_id, data)
        
        return jsonify({
            'message': '计划创建成功',
            'plan': _format_plan_response(plan, detail=True)
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'创建失败: {str(e)}'}), 500


@training_bp.route('', methods=['GET'])
@token_required
def get_plans():
    """
    获取训练计划列表
    
    查询参数:
    - page: 页码，默认1
    - per_page: 每页数量，默认20
    - my_plans: 是否只显示我的计划，true/false
    - templates: 是否只显示模板，true/false
    - difficulty: 难度筛选，beginner/intermediate/advanced
    - target_muscle_group: 目标肌群筛选
    - goal: 训练目标筛选
    - is_active: 是否激活，true/false
    - keyword: 搜索关键词
    - order_by: 排序方式，created_at/usage_count/completion_rate
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 验证分页参数
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # 构建筛选条件
        filters = {
            'my_plans': request.args.get('my_plans', '').lower() == 'true',
            'templates': request.args.get('templates', '').lower() == 'true',
            'difficulty': request.args.get('difficulty'),
            'target_muscle_group': request.args.get('target_muscle_group'),
            'goal': request.args.get('goal'),
            'keyword': request.args.get('keyword'),
            'order_by': request.args.get('order_by', 'created_at')
        }
        
        # is_active参数处理
        is_active_param = request.args.get('is_active', '').lower()
        if is_active_param in ['true', 'false']:
            filters['is_active'] = is_active_param == 'true'
        
        # 获取计划列表
        plans, total = TrainingService.get_plans(g.user_id, filters, page, per_page)
        
        return jsonify({
            'plans': [_format_plan_response(plan) for plan in plans],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500


@training_bp.route('/<int:plan_id>', methods=['GET'])
@token_required
def get_plan_detail(plan_id: int):
    """
    获取训练计划详情
    """
    try:
        plan = TrainingService.get_plan_detail(plan_id, g.user_id)
        
        if not plan:
            return jsonify({'error': '计划不存在'}), 404
        
        return jsonify({
            'plan': _format_plan_response(plan, detail=True)
        }), 200
        
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500


@training_bp.route('/<int:plan_id>', methods=['PUT'])
@token_required
def update_plan(plan_id: int):
    """
    更新训练计划
    
    请求体示例（可选字段）:
    {
        "name": "新的计划名称",
        "description": "更新的描述",
        "difficulty": "advanced",
        "is_active": true,
        "plan_days": [...]
    }
    """
    try:
        data = request.get_json()
        
        # 验证难度等级
        if 'difficulty' in data and data['difficulty'] not in [e.value for e in DifficultyEnum]:
            return jsonify({'error': '无效的难度等级'}), 400
        
        # 验证目标肌群
        if 'target_muscle_group' in data and data['target_muscle_group'] not in [e.value for e in MuscleGroupEnum]:
            return jsonify({'error': '无效的目标肌群'}), 400
        
        # 更新计划
        plan = TrainingService.update_plan(plan_id, g.user_id, data)
        
        return jsonify({
            'message': '更新成功',
            'plan': _format_plan_response(plan, detail=True)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


@training_bp.route('/<int:plan_id>', methods=['DELETE'])
@token_required
def delete_plan(plan_id: int):
    """
    删除训练计划
    """
    try:
        TrainingService.delete_plan(plan_id, g.user_id)
        
        return jsonify({
            'message': '删除成功'
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'删除失败: {str(e)}'}), 500


@training_bp.route('/<int:plan_id>/start', methods=['POST'])
@token_required
def start_plan(plan_id: int):
    """
    开始执行训练计划
    
    如果是模板计划，会自动复制一份；
    如果已有其他激活的计划，会自动取消激活
    """
    try:
        plan = TrainingService.start_plan(plan_id, g.user_id)
        
        return jsonify({
            'message': '计划已激活',
            'plan': _format_plan_response(plan, detail=True)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'激活失败: {str(e)}'}), 500


@training_bp.route('/<int:plan_id>/copy', methods=['POST'])
@token_required
def copy_template(plan_id: int):
    """
    复制模板计划
    """
    try:
        plan = TrainingService.copy_template(plan_id, g.user_id)
        
        return jsonify({
            'message': '复制成功',
            'plan': _format_plan_response(plan, detail=True)
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'复制失败: {str(e)}'}), 500


@training_bp.route('/<int:plan_id>/progress', methods=['GET'])
@token_required
def get_plan_progress(plan_id: int):
    """
    获取训练计划进度
    """
    try:
        progress = TrainingService.get_plan_progress(plan_id, g.user_id)
        
        return jsonify(progress), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500


def _format_plan_response(plan, detail: bool = False) -> dict:
    """
    格式化计划响应数据
    
    Args:
        plan: 训练计划对象
        detail: 是否返回详细信息
        
    Returns:
        格式化的字典
    """
    base_info = {
        'id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'cover_image': plan.cover_image,
        'difficulty': plan.difficulty.value if plan.difficulty else None,
        'duration_weeks': plan.duration_weeks,
        'days_per_week': plan.days_per_week,
        'goal': plan.goal,
        'target_muscle_group': plan.target_muscle_group.value if plan.target_muscle_group else None,
        'is_active': plan.is_active,
        'is_template': plan.is_template,
        'is_public': plan.is_public,
        'usage_count': plan.usage_count,
        'completion_rate': plan.completion_rate,
        'created_at': plan.created_at.isoformat() if plan.created_at else None,
        'updated_at': plan.updated_at.isoformat() if plan.updated_at else None
    }
    
    # 如果需要详细信息，包含训练日和动作
    if detail and hasattr(plan, 'plan_days'):
        base_info['plan_days'] = [
            {
                'id': day.id,
                'day_number': day.day_number,
                'day_name': day.day_name,
                'description': day.description,
                'warm_up': day.warm_up,
                'cool_down': day.cool_down,
                'estimated_duration': day.estimated_duration,
                'target_calories': day.target_calories,
                'rest_time': day.rest_time,
                'exercises': [
                    {
                        'id': exercise.id,
                        'name': exercise.name,
                        'description': exercise.description,
                        'video_url': exercise.video_url,
                        'image_url': exercise.image_url,
                        'exercise_type': exercise.exercise_type,
                        'muscle_group': exercise.muscle_group.value if exercise.muscle_group else None,
                        'equipment': exercise.equipment,
                        'order_number': exercise.order_number,
                        'sets': exercise.sets,
                        'reps': exercise.reps,
                        'duration': exercise.duration,
                        'weight': exercise.weight,
                        'rest_time': exercise.rest_time,
                        'difficulty': exercise.difficulty.value if exercise.difficulty else None,
                        'calories_per_set': exercise.calories_per_set,
                        'key_points': exercise.key_points,
                        'common_mistakes': exercise.common_mistakes
                    }
                    for exercise in sorted(day.exercises, key=lambda e: e.order_number)
                ]
            }
            for day in sorted(plan.plan_days, key=lambda d: d.day_number)
        ]
        
        # 包含用户信息
        if hasattr(plan, 'user') and plan.user:
            base_info['creator'] = {
                'id': plan.user.id,
                'username': plan.user.username,
                'nickname': plan.user_profile.nickname if hasattr(plan.user, 'user_profile') and plan.user.user_profile else None
            }
    
    return base_info
