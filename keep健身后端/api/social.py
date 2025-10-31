"""
社交功能API路由
提供关注、动态、互动、通知等功能接口
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from middleware.auth import token_required
from services.social_service import SocialService
from services.feed_service import FeedService
from services.interaction_service import InteractionService
from services.notification_service import NotificationService
from schemas.social_schemas import (
    FollowCreate, FollowUpdate, FollowListQuery,
    FeedCreate, FeedUpdate, FeedListQuery, FeedShareCreate,
    CommentCreate, CommentUpdate, CommentListQuery,
    LikeCreate,
    NotificationListQuery, NotificationMarkRead, NotificationSettingUpdate
)


social_bp = Blueprint('social', __name__, url_prefix='/api/social')


# ========== 关注相关 ==========

@social_bp.route('/follow', methods=['POST'])
@token_required
def follow_user(current_user):
    """关注用户"""
    try:
        data = FollowCreate(**request.json)
        
        result = SocialService.follow_user(
            follower_id=current_user['id'],
            following_id=data.following_id,
            group_tag=data.group_tag,
            remark=data.remark
        )
        
        return jsonify({
            'code': 0,
            'message': '关注成功',
            'data': result
        }), 201
        
    except ValueError as e:
        return jsonify({
            'code': 400,
            'message': str(e)
        }), 400
    except ValidationError as e:
        return jsonify({
            'code': 400,
            'message': '数据验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'操作失败: {str(e)}'
        }), 500


@social_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@token_required
def unfollow_user(current_user, user_id):
    """取消关注"""
    try:
        success = SocialService.unfollow_user(
            follower_id=current_user['id'],
            following_id=user_id
        )
        
        if not success:
            return jsonify({
                'code': 404,
                'message': '关注关系不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '取消关注成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'操作失败: {str(e)}'
        }), 500


@social_bp.route('/following', methods=['GET'])
@token_required
def get_following(current_user):
    """获取关注列表"""
    try:
        query_params = FollowListQuery(
            user_id=int(request.args.get('user_id', current_user['id'])),
            page=int(request.args.get('page', 1)),
            per_page=int(request.args.get('per_page', 20)),
            group_tag=request.args.get('group_tag')
        )
        
        result = SocialService.get_following_list(
            user_id=query_params.user_id,
            filters=query_params.model_dump(exclude_none=True)
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/followers', methods=['GET'])
@token_required
def get_followers(current_user):
    """获取粉丝列表"""
    try:
        user_id = int(request.args.get('user_id', current_user['id']))
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        result = SocialService.get_followers_list(
            user_id=user_id,
            filters={'page': page, 'per_page': per_page}
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/follow-status/<int:user_id>', methods=['GET'])
@token_required
def get_follow_status(current_user, user_id):
    """检查关注状态"""
    try:
        result = SocialService.check_follow_status(
            user_id=current_user['id'],
            target_user_id=user_id
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


# ========== 动态相关 ==========

@social_bp.route('/feeds', methods=['POST'])
@token_required
def create_feed(current_user):
    """发布动态"""
    try:
        data = FeedCreate(**request.json)
        
        result = FeedService.create_feed(
            user_id=current_user['id'],
            data=data.model_dump()
        )
        
        return jsonify({
            'code': 0,
            'message': '发布成功',
            'data': result
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
            'message': f'发布失败: {str(e)}'
        }), 500


@social_bp.route('/feeds/<int:feed_id>', methods=['GET'])
@token_required
def get_feed(current_user, feed_id):
    """获取动态详情"""
    try:
        result = FeedService.get_feed_detail(
            feed_id=feed_id,
            current_user_id=current_user['id']
        )
        
        if not result:
            return jsonify({
                'code': 404,
                'message': '动态不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/timeline', methods=['GET'])
@token_required
def get_timeline(current_user):
    """获取时间线（关注的人的动态）"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        result = FeedService.get_timeline(
            user_id=current_user['id'],
            filters={'page': page, 'per_page': per_page}
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/explore', methods=['GET'])
@token_required
def get_explore(current_user):
    """获取探索页（推荐动态）"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        order_by = request.args.get('order_by', 'created_at')
        
        result = FeedService.get_explore_feeds(
            current_user_id=current_user['id'],
            filters={'page': page, 'per_page': per_page, 'order_by': order_by}
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/feeds/<int:feed_id>', methods=['PUT'])
@token_required
def update_feed(current_user, feed_id):
    """更新动态"""
    try:
        data = FeedUpdate(**request.json)
        
        result = FeedService.update_feed(
            feed_id=feed_id,
            user_id=current_user['id'],
            data=data.model_dump(exclude_none=True)
        )
        
        if not result:
            return jsonify({
                'code': 404,
                'message': '动态不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': '更新成功',
            'data': result
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


@social_bp.route('/feeds/<int:feed_id>', methods=['DELETE'])
@token_required
def delete_feed(current_user, feed_id):
    """删除动态"""
    try:
        success = FeedService.delete_feed(
            feed_id=feed_id,
            user_id=current_user['id']
        )
        
        if not success:
            return jsonify({
                'code': 404,
                'message': '动态不存在'
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


# ========== 互动相关 ==========

@social_bp.route('/like', methods=['POST'])
@token_required
def toggle_like(current_user):
    """点赞/取消点赞"""
    try:
        data = LikeCreate(**request.json)
        
        result = InteractionService.toggle_like(
            user_id=current_user['id'],
            target_type=data.target_type,
            target_id=data.target_id
        )
        
        return jsonify({
            'code': 0,
            'message': '操作成功',
            'data': result
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
            'message': f'操作失败: {str(e)}'
        }), 500


@social_bp.route('/comments', methods=['POST'])
@token_required
def create_comment(current_user):
    """发表评论"""
    try:
        data = CommentCreate(**request.json)
        
        result = InteractionService.create_comment(
            user_id=current_user['id'],
            data=data.model_dump()
        )
        
        return jsonify({
            'code': 0,
            'message': '评论成功',
            'data': result
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
            'message': f'评论失败: {str(e)}'
        }), 500


@social_bp.route('/comments', methods=['GET'])
@token_required
def get_comments(current_user):
    """获取评论列表"""
    try:
        query_params = CommentListQuery(
            target_type=request.args.get('target_type'),
            target_id=int(request.args.get('target_id')),
            parent_id=int(request.args.get('parent_id')) if request.args.get('parent_id') else None,
            page=int(request.args.get('page', 1)),
            per_page=int(request.args.get('per_page', 20)),
            order_by=request.args.get('order_by', 'created_at')
        )
        
        result = InteractionService.get_comments(
            target_type=query_params.target_type,
            target_id=query_params.target_id,
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
            'message': '参数验证失败',
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    """删除评论"""
    try:
        success = InteractionService.delete_comment(
            comment_id=comment_id,
            user_id=current_user['id']
        )
        
        if not success:
            return jsonify({
                'code': 404,
                'message': '评论不存在'
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


# ========== 通知相关 ==========

@social_bp.route('/notifications', methods=['GET'])
@token_required
def get_notifications(current_user):
    """获取通知列表"""
    try:
        query_params = NotificationListQuery(
            notification_type=request.args.get('notification_type'),
            is_read=request.args.get('is_read') == 'true' if request.args.get('is_read') else None,
            page=int(request.args.get('page', 1)),
            per_page=int(request.args.get('per_page', 20))
        )
        
        result = NotificationService.get_notifications(
            user_id=current_user['id'],
            filters=query_params.model_dump(exclude_none=True)
        )
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/notifications/read', methods=['POST'])
@token_required
def mark_notifications_read(current_user):
    """标记通知为已读"""
    try:
        data = NotificationMarkRead(**request.json)
        
        NotificationService.mark_as_read(
            user_id=current_user['id'],
            notification_ids=data.notification_ids
        )
        
        return jsonify({
            'code': 0,
            'message': '标记成功'
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
            'message': f'操作失败: {str(e)}'
        }), 500


@social_bp.route('/notifications/unread-count', methods=['GET'])
@token_required
def get_unread_count(current_user):
    """获取未读通知数"""
    try:
        count = NotificationService.get_unread_count(user_id=current_user['id'])
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': {'count': count}
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}'
        }), 500


@social_bp.route('/notification-settings', methods=['GET', 'PUT'])
@token_required
def notification_settings(current_user):
    """获取/更新通知设置"""
    if request.method == 'GET':
        # TODO: 实现获取设置
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': {}
        })
    
    else:  # PUT
        try:
            data = NotificationSettingUpdate(**request.json)
            
            result = NotificationService.update_notification_settings(
                user_id=current_user['id'],
                data=data.model_dump(exclude_none=True)
            )
            
            return jsonify({
                'code': 0,
                'message': '更新成功',
                'data': result
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
