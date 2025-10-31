"""
动态内容服务层
处理用户动态发布、浏览、时间线生成等业务逻辑
"""
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import and_, or_, func, desc
from sqlalchemy.orm import joinedload
from config.database import db_session
from models.feed import Feed, FeedShare, Hashtag, HashtagFollow
from models.social import Follow, Like, Comment
from models.workout import WorkoutRecord
from models.user import User


class FeedService:
    """动态服务类"""
    
    @staticmethod
    def create_feed(user_id: int, data: Dict) -> Dict:
        """
        创建动态
        
        Args:
            user_id: 用户ID
            data: 动态数据
            
        Returns:
            动态数据
        """
        try:
            # 如果关联训练记录,获取训练摘要
            workout_summary = None
            if data.get('workout_id'):
                workout = db_session.query(WorkoutRecord).filter_by(
                    id=data['workout_id'],
                    user_id=user_id
                ).first()
                
                if workout:
                    workout_summary = {
                        'workout_type': workout.workout_type,
                        'duration': workout.duration,
                        'calories': workout.calories_burned,
                        'total_sets': workout.total_sets
                    }
            
            # 创建动态
            feed = Feed(
                user_id=user_id,
                feed_type=data['feed_type'],
                title=data.get('title'),
                content=data.get('content'),
                images=data.get('images'),
                video_url=data.get('video_url'),
                thumbnail_url=data.get('thumbnail_url'),
                workout_id=data.get('workout_id'),
                workout_summary=workout_summary,
                hashtags=data.get('hashtags'),
                location=data.get('location'),
                visibility=data.get('visibility', 'public'),
                allow_comment=data.get('allow_comment', True),
                allow_share=data.get('allow_share', True),
                status='published'
            )
            
            db_session.add(feed)
            db_session.flush()
            
            # 更新话题标签的动态数量
            if data.get('hashtags'):
                for tag_name in data['hashtags']:
                    tag = db_session.query(Hashtag).filter_by(name=tag_name).first()
                    if tag:
                        tag.feeds_count = (tag.feeds_count or 0) + 1
                    else:
                        # 自动创建标签
                        new_tag = Hashtag(
                            name=tag_name,
                            feeds_count=1
                        )
                        db_session.add(new_tag)
            
            db_session.commit()
            
            return FeedService._format_feed(feed, user_id)
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def get_feed_detail(feed_id: int, current_user_id: int = None) -> Optional[Dict]:
        """
        获取动态详情
        
        Args:
            feed_id: 动态ID
            current_user_id: 当前用户ID
            
        Returns:
            动态数据
        """
        feed = db_session.query(Feed).options(
            joinedload(Feed.user)
        ).filter(
            and_(
                Feed.id == feed_id,
                Feed.deleted_at.is_(None)
            )
        ).first()
        
        if not feed:
            return None
        
        # 检查可见性权限
        if not FeedService._check_visibility(feed, current_user_id):
            return None
        
        # 增加浏览数
        feed.views_count = (feed.views_count or 0) + 1
        db_session.commit()
        
        return FeedService._format_feed(feed, current_user_id)
    
    @staticmethod
    def get_timeline(user_id: int, filters: Dict = None) -> Dict:
        """
        获取时间线动态（关注的人的动态）
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            
        Returns:
            动态列表
        """
        filters = filters or {}
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        
        # 获取关注的用户ID列表
        following_ids = db_session.query(Follow.following_id).filter(
            and_(
                Follow.follower_id == user_id,
                Follow.deleted_at.is_(None)
            )
        ).all()
        following_ids = [f[0] for f in following_ids]
        
        # 包含自己的动态
        following_ids.append(user_id)
        
        # 构建查询
        query = db_session.query(Feed).options(
            joinedload(Feed.user)
        ).filter(
            and_(
                Feed.user_id.in_(following_ids),
                Feed.deleted_at.is_(None),
                Feed.status == 'published',
                or_(
                    Feed.visibility == 'public',
                    and_(Feed.visibility == 'friends', Feed.user_id.in_(following_ids))
                )
            )
        ).order_by(desc(Feed.created_at))
        
        # 分页
        total = query.count()
        feeds = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 构建结果
        items = [FeedService._format_feed(feed, user_id) for feed in feeds]
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def get_user_feeds(target_user_id: int, current_user_id: int = None, 
                       filters: Dict = None) -> Dict:
        """
        获取用户的动态列表
        
        Args:
            target_user_id: 目标用户ID
            current_user_id: 当前用户ID
            filters: 筛选条件
            
        Returns:
            动态列表
        """
        filters = filters or {}
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        feed_type = filters.get('feed_type')
        
        # 构建查询
        query = db_session.query(Feed).options(
            joinedload(Feed.user)
        ).filter(
            and_(
                Feed.user_id == target_user_id,
                Feed.deleted_at.is_(None),
                Feed.status == 'published'
            )
        )
        
        # 可见性过滤
        if current_user_id != target_user_id:
            # 检查是否是好友
            is_friend = db_session.query(Follow).filter(
                and_(
                    Follow.follower_id == current_user_id,
                    Follow.following_id == target_user_id,
                    Follow.deleted_at.is_(None)
                )
            ).first() is not None
            
            if is_friend:
                query = query.filter(Feed.visibility.in_(['public', 'friends']))
            else:
                query = query.filter(Feed.visibility == 'public')
        
        # 类型筛选
        if feed_type:
            query = query.filter(Feed.feed_type == feed_type)
        
        # 排序
        query = query.order_by(desc(Feed.created_at))
        
        # 分页
        total = query.count()
        feeds = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 构建结果
        items = [FeedService._format_feed(feed, current_user_id) for feed in feeds]
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def get_explore_feeds(current_user_id: int = None, filters: Dict = None) -> Dict:
        """
        获取探索页动态（推荐、热门）
        
        Args:
            current_user_id: 当前用户ID
            filters: 筛选条件
            
        Returns:
            动态列表
        """
        filters = filters or {}
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        order_by = filters.get('order_by', 'created_at')
        
        # 构建查询
        query = db_session.query(Feed).options(
            joinedload(Feed.user)
        ).filter(
            and_(
                Feed.deleted_at.is_(None),
                Feed.status == 'published',
                Feed.visibility == 'public'
            )
        )
        
        # 排序
        if order_by == 'hot':
            # 热度算法: 点赞数 * 0.5 + 评论数 * 0.3 + 分享数 * 0.2
            query = query.order_by(
                desc(
                    Feed.likes_count * 0.5 + 
                    Feed.comments_count * 0.3 + 
                    Feed.shares_count * 0.2
                )
            )
        elif order_by == 'likes_count':
            query = query.order_by(desc(Feed.likes_count))
        else:
            query = query.order_by(desc(Feed.created_at))
        
        # 分页
        total = query.count()
        feeds = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 构建结果
        items = [FeedService._format_feed(feed, current_user_id) for feed in feeds]
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def update_feed(feed_id: int, user_id: int, data: Dict) -> Optional[Dict]:
        """
        更新动态
        
        Args:
            feed_id: 动态ID
            user_id: 用户ID
            data: 更新数据
            
        Returns:
            更新后的数据
        """
        feed = db_session.query(Feed).filter(
            and_(
                Feed.id == feed_id,
                Feed.user_id == user_id,
                Feed.deleted_at.is_(None)
            )
        ).first()
        
        if not feed:
            return None
        
        try:
            # 更新字段
            if 'title' in data:
                feed.title = data['title']
            if 'content' in data:
                feed.content = data['content']
            if 'images' in data:
                feed.images = data['images']
            if 'hashtags' in data:
                feed.hashtags = data['hashtags']
            if 'visibility' in data:
                feed.visibility = data['visibility']
            if 'allow_comment' in data:
                feed.allow_comment = data['allow_comment']
            if 'allow_share' in data:
                feed.allow_share = data['allow_share']
            
            feed.updated_at = int(datetime.utcnow().timestamp())
            db_session.commit()
            
            return FeedService._format_feed(feed, user_id)
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def delete_feed(feed_id: int, user_id: int) -> bool:
        """
        删除动态
        
        Args:
            feed_id: 动态ID
            user_id: 用户ID
            
        Returns:
            是否成功
        """
        feed = db_session.query(Feed).filter(
            and_(
                Feed.id == feed_id,
                Feed.user_id == user_id,
                Feed.deleted_at.is_(None)
            )
        ).first()
        
        if not feed:
            return False
        
        try:
            # 软删除
            feed.deleted_at = int(datetime.utcnow().timestamp())
            
            # 更新话题标签的动态数量
            if feed.hashtags:
                for tag_name in feed.hashtags:
                    tag = db_session.query(Hashtag).filter_by(name=tag_name).first()
                    if tag and tag.feeds_count > 0:
                        tag.feeds_count -= 1
            
            db_session.commit()
            return True
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def _format_feed(feed: Feed, current_user_id: int = None) -> Dict:
        """格式化动态数据"""
        # 检查当前用户是否点赞
        is_liked = False
        if current_user_id:
            is_liked = db_session.query(Like).filter(
                and_(
                    Like.user_id == current_user_id,
                    Like.target_type == 'feed',
                    Like.target_id == feed.id,
                    Like.is_active == True,
                    Like.deleted_at.is_(None)
                )
            ).first() is not None
        
        return {
            'id': feed.id,
            'user': {
                'id': feed.user.id,
                'username': feed.user.username,
                'nickname': feed.user.nickname,
                'avatar': feed.user.avatar
            },
            'feed_type': feed.feed_type,
            'title': feed.title,
            'content': feed.content,
            'images': feed.images or [],
            'video_url': feed.video_url,
            'thumbnail_url': feed.thumbnail_url,
            'workout_summary': feed.workout_summary,
            'hashtags': feed.hashtags or [],
            'location': feed.location,
            'visibility': feed.visibility,
            'likes_count': feed.likes_count or 0,
            'comments_count': feed.comments_count or 0,
            'shares_count': feed.shares_count or 0,
            'views_count': feed.views_count or 0,
            'is_liked': is_liked,
            'allow_comment': feed.allow_comment,
            'allow_share': feed.allow_share,
            'created_at': feed.created_at
        }
    
    @staticmethod
    def _check_visibility(feed: Feed, current_user_id: int = None) -> bool:
        """检查可见性权限"""
        if feed.visibility == 'public':
            return True
        
        if not current_user_id:
            return False
        
        # 自己的动态
        if feed.user_id == current_user_id:
            return True
        
        # 仅好友可见
        if feed.visibility == 'friends':
            is_friend = db_session.query(Follow).filter(
                and_(
                    Follow.follower_id == current_user_id,
                    Follow.following_id == feed.user_id,
                    Follow.deleted_at.is_(None)
                )
            ).first() is not None
            return is_friend
        
        # 私密
        return False
