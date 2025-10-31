"""
社交互动服务层
处理点赞、评论等互动业务逻辑
"""
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import and_, desc
from sqlalchemy.orm import joinedload
from config.database import db_session
from models.social import Like, Comment
from models.feed import Feed
from models.workout import WorkoutRecord


class InteractionService:
    """互动服务类"""
    
    @staticmethod
    def toggle_like(user_id: int, target_type: str, target_id: int) -> Dict:
        """
        切换点赞状态（点赞/取消点赞）
        
        Args:
            user_id: 用户ID
            target_type: 目标类型
            target_id: 目标ID
            
        Returns:
            点赞状态
        """
        # 检查是否已点赞
        existing_like = db_session.query(Like).filter(
            and_(
                Like.user_id == user_id,
                Like.target_type == target_type,
                Like.target_id == target_id,
                Like.deleted_at.is_(None)
            )
        ).first()
        
        try:
            if existing_like:
                # 取消点赞
                if existing_like.is_active:
                    existing_like.is_active = False
                    InteractionService._update_like_count(target_type, target_id, -1)
                    is_liked = False
                else:
                    # 重新点赞
                    existing_like.is_active = True
                    InteractionService._update_like_count(target_type, target_id, 1)
                    is_liked = True
            else:
                # 新增点赞
                like = Like(
                    user_id=user_id,
                    target_type=target_type,
                    target_id=target_id,
                    is_active=True
                )
                db_session.add(like)
                InteractionService._update_like_count(target_type, target_id, 1)
                is_liked = True
            
            db_session.commit()
            
            # 获取最新点赞数
            likes_count = InteractionService._get_like_count(target_type, target_id)
            
            return {
                'is_liked': is_liked,
                'likes_count': likes_count
            }
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def _update_like_count(target_type: str, target_id: int, delta: int):
        """更新点赞数"""
        if target_type == 'feed':
            feed = db_session.query(Feed).filter_by(id=target_id).first()
            if feed:
                feed.likes_count = max(0, (feed.likes_count or 0) + delta)
        elif target_type == 'comment':
            comment = db_session.query(Comment).filter_by(id=target_id).first()
            if comment:
                comment.likes_count = max(0, (comment.likes_count or 0) + delta)
        elif target_type == 'workout':
            workout = db_session.query(WorkoutRecord).filter_by(id=target_id).first()
            if workout:
                workout.likes_count = max(0, (workout.likes_count or 0) + delta)
    
    @staticmethod
    def _get_like_count(target_type: str, target_id: int) -> int:
        """获取点赞数"""
        if target_type == 'feed':
            feed = db_session.query(Feed).filter_by(id=target_id).first()
            return feed.likes_count or 0 if feed else 0
        elif target_type == 'comment':
            comment = db_session.query(Comment).filter_by(id=target_id).first()
            return comment.likes_count or 0 if comment else 0
        elif target_type == 'workout':
            workout = db_session.query(WorkoutRecord).filter_by(id=target_id).first()
            return workout.likes_count or 0 if workout else 0
        return 0
    
    @staticmethod
    def create_comment(user_id: int, data: Dict) -> Dict:
        """
        创建评论
        
        Args:
            user_id: 用户ID
            data: 评论数据
            
        Returns:
            评论数据
        """
        try:
            # 确定评论层级
            level = 0
            root_comment_id = None
            
            if data.get('parent_id'):
                parent = db_session.query(Comment).filter_by(
                    id=data['parent_id']
                ).first()
                if parent:
                    level = 1  # 二级回复
                    root_comment_id = parent.root_comment_id or parent.id
            
            # 创建评论
            comment = Comment(
                user_id=user_id,
                target_type=data['target_type'],
                target_id=data['target_id'],
                content=data['content'],
                parent_id=data.get('parent_id'),
                reply_to_user_id=data.get('reply_to_user_id'),
                level=level,
                root_comment_id=root_comment_id,
                images=data.get('images'),
                mentions=','.join(map(str, data.get('mentions', []))) if data.get('mentions') else None
            )
            
            db_session.add(comment)
            db_session.flush()
            
            # 更新父评论的回复数
            if data.get('parent_id'):
                parent = db_session.query(Comment).filter_by(
                    id=data['parent_id']
                ).first()
                if parent:
                    parent.replies_count = (parent.replies_count or 0) + 1
            
            # 更新目标的评论数
            InteractionService._update_comment_count(
                data['target_type'], 
                data['target_id'], 
                1
            )
            
            db_session.commit()
            
            return InteractionService._format_comment(comment)
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def get_comments(target_type: str, target_id: int, 
                    filters: Dict = None) -> Dict:
        """
        获取评论列表
        
        Args:
            target_type: 目标类型
            target_id: 目标ID
            filters: 筛选条件
            
        Returns:
            评论列表
        """
        filters = filters or {}
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        parent_id = filters.get('parent_id')
        order_by = filters.get('order_by', 'created_at')
        
        # 构建查询
        query = db_session.query(Comment).options(
            joinedload(Comment.user)
        ).filter(
            and_(
                Comment.target_type == target_type,
                Comment.target_id == target_id,
                Comment.deleted_at.is_(None),
                Comment.is_approved == True,
                Comment.is_hidden == False
            )
        )
        
        # 筛选父评论或子回复
        if parent_id is not None:
            query = query.filter(Comment.parent_id == parent_id)
        else:
            query = query.filter(Comment.parent_id.is_(None))
        
        # 排序
        if order_by == 'likes_count':
            query = query.order_by(desc(Comment.likes_count))
        else:
            query = query.order_by(desc(Comment.created_at))
        
        # 分页
        total = query.count()
        comments = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 构建结果
        items = [InteractionService._format_comment(c) for c in comments]
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def delete_comment(comment_id: int, user_id: int) -> bool:
        """
        删除评论
        
        Args:
            comment_id: 评论ID
            user_id: 用户ID
            
        Returns:
            是否成功
        """
        comment = db_session.query(Comment).filter(
            and_(
                Comment.id == comment_id,
                Comment.user_id == user_id,
                Comment.deleted_at.is_(None)
            )
        ).first()
        
        if not comment:
            return False
        
        try:
            # 软删除
            comment.deleted_at = int(datetime.utcnow().timestamp())
            
            # 更新父评论的回复数
            if comment.parent_id:
                parent = db_session.query(Comment).filter_by(
                    id=comment.parent_id
                ).first()
                if parent and parent.replies_count > 0:
                    parent.replies_count -= 1
            
            # 更新目标的评论数
            InteractionService._update_comment_count(
                comment.target_type,
                comment.target_id,
                -1
            )
            
            db_session.commit()
            return True
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def _update_comment_count(target_type: str, target_id: int, delta: int):
        """更新评论数"""
        if target_type == 'feed':
            feed = db_session.query(Feed).filter_by(id=target_id).first()
            if feed:
                feed.comments_count = max(0, (feed.comments_count or 0) + delta)
        elif target_type == 'workout':
            workout = db_session.query(WorkoutRecord).filter_by(id=target_id).first()
            if workout:
                workout.comments_count = max(0, (workout.comments_count or 0) + delta)
    
    @staticmethod
    def _format_comment(comment: Comment) -> Dict:
        """格式化评论数据"""
        return {
            'id': comment.id,
            'user': {
                'id': comment.user.id,
                'username': comment.user.username,
                'nickname': comment.user.nickname,
                'avatar': comment.user.avatar
            },
            'content': comment.content,
            'images': comment.images,
            'parent_id': comment.parent_id,
            'reply_to_user_id': comment.reply_to_user_id,
            'level': comment.level,
            'likes_count': comment.likes_count or 0,
            'replies_count': comment.replies_count or 0,
            'is_pinned': comment.is_pinned,
            'is_author': comment.is_author,
            'created_at': comment.created_at
        }
