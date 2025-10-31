"""
运动记录API路由
提供训练记录的CRUD和统计功能
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from middleware.auth import token_required
from services.workout_service import WorkoutService
from services.stats_service import StatsService
from schemas.workout_schemas import (
    WorkoutRecordCreate,
    WorkoutRecordUpdate,
    WorkoutRecordFinish,
    SetRecordCreate,
    SetRecordUpdate,
    WorkoutListQuery,
    CalendarQuery,
    StatsQuery
)


workout_bp = Blueprint('workout', __name__)


@workout_bp.route('/workouts', methods=['POST'])
@token_required
def create_workout(current_user):
    """创建训练记录"""
    try:
        # 验证请求数据
        workout_data = WorkoutRecordCreate(**request.json)
        
        # 创建训练记录
        workout = WorkoutService.create_workout(
            user_id=current_user['id'],
            data=workout_data.model_dump()
        )
        
        return jsonify({
            'code': 0,
            'message': '训练记录创建成功',
            'data': workout
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '数据验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'创建失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts', methods=['GET'])
@token_required
def list_workouts(current_user):
    """获取训练记录列表"""
    try:
        # 验证查询参数
        query_params = WorkoutListQuery(
            start_date=request.args.get('start_date'),
            end_date=request.args.get('end_date'),
            workout_type=request.args.get('workout_type'),
            plan_id=int(request.args.get('plan_id')) if request.args.get('plan_id') else None,
            is_completed=request.args.get('is_completed'),
            page=int(request.args.get('page', 1)),
            per_page=int(request.args.get('per_page', 20))
        )
        
        # 获取列表
        result = WorkoutService.get_workouts(
            user_id=current_user['id'],
            filters=query_params.model_dump(exclude_none=True)
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '查询参数验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts/<int:workout_id>', methods=['GET'])
@token_required
def get_workout_detail(current_user, workout_id):
    """获取训练记录详情"""
    try:
        workout = WorkoutService.get_workout_detail(
            workout_id=workout_id,
            user_id=current_user['id']
        )
        
        if not workout:
            return jsonify({
                'code': 404,
                'message': '训练记录不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': workout
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts/<int:workout_id>', methods=['PUT'])
@token_required
def update_workout(current_user, workout_id):
    """更新训练记录"""
    try:
        # 验证请求数据
        update_data = WorkoutRecordUpdate(**request.json)
        
        # 更新记录
        workout = WorkoutService.update_workout(
            workout_id=workout_id,
            user_id=current_user['id'],
            data=update_data.model_dump(exclude_none=True)
        )
        
        if not workout:
            return jsonify({
                'code': 404,
                'message': '训练记录不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '更新成功',
            'data': workout
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '数据验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts/<int:workout_id>/finish', methods=['POST'])
@token_required
def finish_workout(current_user, workout_id):
    """完成训练"""
    try:
        # 验证请求数据
        finish_data = WorkoutRecordFinish(**request.json) if request.json else WorkoutRecordFinish()
        
        # 完成训练
        workout = WorkoutService.finish_workout(
            workout_id=workout_id,
            user_id=current_user['id'],
            notes=finish_data.notes
        )
        
        if not workout:
            return jsonify({
                'code': 404,
                'message': '训练记录不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '训练已完成',
            'data': workout
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '数据验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'完成失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts/<int:workout_id>', methods=['DELETE'])
@token_required
def delete_workout(current_user, workout_id):
    """删除训练记录（软删除）"""
    try:
        success = WorkoutService.delete_workout(
            workout_id=workout_id,
            user_id=current_user['id']
        )
        
        if not success:
            return jsonify({
                'code': 404,
                'message': '训练记录不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts/<int:workout_id>/sets', methods=['POST'])
@token_required
def add_set(current_user, workout_id):
    """添加训练组"""
    try:
        # 验证请求数据
        set_data = SetRecordCreate(**request.json)
        
        # 添加训练组
        set_record = WorkoutService.add_set_to_exercise(
            workout_id=workout_id,
            user_id=current_user['id'],
            exercise_id=set_data.exercise_id,
            set_data=set_data.model_dump()
        )
        
        if not set_record:
            return jsonify({
                'code': 404,
                'message': '训练记录或动作不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '训练组添加成功',
            'data': set_record
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '数据验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'添加失败: {str(e)}'
        }), 500


@workout_bp.route('/sets/<int:set_id>', methods=['PUT'])
@token_required
def update_set(current_user, set_id):
    """更新训练组"""
    try:
        # 验证请求数据
        update_data = SetRecordUpdate(**request.json)
        
        # 更新训练组
        set_record = WorkoutService.update_set(
            set_id=set_id,
            user_id=current_user['id'],
            data=update_data.model_dump(exclude_none=True)
        )
        
        if not set_record:
            return jsonify({
                'code': 404,
                'message': '训练组不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '更新成功',
            'data': set_record
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '数据验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}'
        }), 500


@workout_bp.route('/sets/<int:set_id>', methods=['DELETE'])
@token_required
def delete_set(current_user, set_id):
    """删除训练组"""
    try:
        success = WorkoutService.delete_set(
            set_id=set_id,
            user_id=current_user['id']
        )
        
        if not success:
            return jsonify({
                'code': 404,
                'message': '训练组不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts/calendar', methods=['GET'])
@token_required
def get_calendar(current_user):
    """获取训练日历"""
    try:
        # 验证查询参数
        query_params = CalendarQuery(
            year=int(request.args.get('year')) if request.args.get('year') else None,
            month=int(request.args.get('month')) if request.args.get('month') else None
        )
        
        # 获取日历数据
        calendar_data = WorkoutService.get_calendar(
            user_id=current_user['id'],
            year=query_params.year,
            month=query_params.month
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': calendar_data
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '查询参数验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/workouts/records', methods=['GET'])
@token_required
def get_personal_records(current_user):
    """获取个人最佳记录"""
    try:
        exercise_name = request.args.get('exercise_name')
        
        # 获取个人记录
        records = WorkoutService.get_personal_records(
            user_id=current_user['id'],
            exercise_name=exercise_name
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': records
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/stats/overview', methods=['GET'])
@token_required
def get_stats_overview(current_user):
    """获取统计总览"""
    try:
        # 验证查询参数
        query_params = StatsQuery(
            start_date=request.args.get('start_date'),
            end_date=request.args.get('end_date')
        )
        
        # 获取统计数据
        stats = StatsService.get_overview_stats(
            user_id=current_user['id'],
            start_date=query_params.start_date,
            end_date=query_params.end_date
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': stats
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '查询参数验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/stats/weekly', methods=['GET'])
@token_required
def get_weekly_stats(current_user):
    """获取周统计"""
    try:
        stats = StatsService.get_weekly_stats(user_id=current_user['id'])
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/stats/monthly', methods=['GET'])
@token_required
def get_monthly_stats(current_user):
    """获取月统计"""
    try:
        year = int(request.args.get('year')) if request.args.get('year') else None
        month = int(request.args.get('month')) if request.args.get('month') else None
        
        stats = StatsService.get_monthly_stats(
            user_id=current_user['id'],
            year=year,
            month=month
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/stats/muscle-distribution', methods=['GET'])
@token_required
def get_muscle_distribution(current_user):
    """获取肌群训练分布"""
    try:
        # 验证查询参数
        query_params = StatsQuery(
            start_date=request.args.get('start_date'),
            end_date=request.args.get('end_date')
        )
        
        stats = StatsService.get_muscle_group_distribution(
            user_id=current_user['id'],
            start_date=query_params.start_date,
            end_date=query_params.end_date
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': stats
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '查询参数验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/stats/workout-types', methods=['GET'])
@token_required
def get_workout_type_distribution(current_user):
    """获取训练类型分布"""
    try:
        # 验证查询参数
        query_params = StatsQuery(
            start_date=request.args.get('start_date'),
            end_date=request.args.get('end_date')
        )
        
        stats = StatsService.get_workout_type_distribution(
            user_id=current_user['id'],
            start_date=query_params.start_date,
            end_date=query_params.end_date
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': stats
        })
        
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '查询参数验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/stats/progress', methods=['GET'])
@token_required
def get_progress_trend(current_user):
    """获取进步趋势"""
    try:
        exercise_name = request.args.get('exercise_name')
        period = request.args.get('period', 'month')
        
        if period not in ['week', 'month', 'year']:
            return jsonify({
                'code': 400,
                'message': 'period参数必须是: week, month, year'
            }), 400
        
        stats = StatsService.get_progress_trend(
            user_id=current_user['id'],
            exercise_name=exercise_name,
            period=period
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@workout_bp.route('/stats/consistency', methods=['GET'])
@token_required
def get_consistency_score(current_user):
    """获取训练坚持度评分"""
    try:
        score = StatsService.get_consistency_score(user_id=current_user['id'])
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': score
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500
