"""
社交关系服务层
处理关注、粉丝等社交关系业务逻辑
"""
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import and_, or_, func, desc
from sqlalchemy.orm import joinedload
from config.database import db_session
from models.social import Follow
from models.user import User


class SocialService:
    """社交关系服务类"""
    
    @staticmethod
    def follow_user(follower_id: int, following_id: int, 
                   group_tag: str = None, remark: str = None) -> Dict:
        """
        关注用户
        
        Args:
            follower_id: 关注者ID
            following_id: 被关注者ID
            group_tag: 分组标签
            remark: 备注名
            
        Returns:
            关注关系数据
        """
        # 不能关注自己
        if follower_id == following_id:
            raise ValueError("不能关注自己")
        
        # 检查是否已关注
        existing = db_session.query(Follow).filter(
            and_(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
                Follow.deleted_at.is_(None)
            )
        ).first()
        
        if existing:
            raise ValueError("已经关注该用户")
        
        # 检查是否互关
        reverse_follow = db_session.query(Follow).filter(
            and_(
                Follow.follower_id == following_id,
                Follow.following_id == follower_id,
                Follow.deleted_at.is_(None)
            )
        ).first()
        
        is_mutual = reverse_follow is not None
        
        try:
            # 创建关注关系
            follow = Follow(
                follower_id=follower_id,
                following_id=following_id,
                is_mutual=is_mutual,
                group_tag=group_tag,
                remark=remark
            )
            db_session.add(follow)
            
            # 如果互关,更新对方的互关状态
            if is_mutual and reverse_follow:
                reverse_follow.is_mutual = True
            
            # 更新用户的关注和粉丝数
            follower = db_session.query(User).filter_by(id=follower_id).first()
            following = db_session.query(User).filter_by(id=following_id).first()
            
            if follower:
                follower.following_count = (follower.following_count or 0) + 1
            if following:
                following.followers_count = (following.followers_count or 0) + 1
            
            db_session.commit()
            
            return {
                'id': follow.id,
                'follower_id': follow.follower_id,
                'following_id': follow.following_id,
                'is_mutual': follow.is_mutual,
                'group_tag': follow.group_tag,
                'remark': follow.remark,
                'created_at': follow.created_at
            }
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def unfollow_user(follower_id: int, following_id: int) -> bool:
        """
        取消关注
        
        Args:
            follower_id: 关注者ID
            following_id: 被关注者ID
            
        Returns:
            是否成功
        """
        follow = db_session.query(Follow).filter(
            and_(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
                Follow.deleted_at.is_(None)
            )
        ).first()
        
        if not follow:
            return False
        
        try:
            # 软删除
            follow.deleted_at = int(datetime.utcnow().timestamp())
            
            # 更新对方的互关状态
            reverse_follow = db_session.query(Follow).filter(
                and_(
                    Follow.follower_id == following_id,
                    Follow.following_id == follower_id,
                    Follow.deleted_at.is_(None)
                )
            ).first()
            
            if reverse_follow:
                reverse_follow.is_mutual = False
            
            # 更新用户的关注和粉丝数
            follower = db_session.query(User).filter_by(id=follower_id).first()
            following = db_session.query(User).filter_by(id=following_id).first()
            
            if follower and follower.following_count > 0:
                follower.following_count -= 1
            if following and following.followers_count > 0:
                following.followers_count -= 1
            
            db_session.commit()
            return True
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def update_follow(follower_id: int, following_id: int, data: Dict) -> Optional[Dict]:
        """
        更新关注关系
        
        Args:
            follower_id: 关注者ID
            following_id: 被关注者ID
            data: 更新数据
            
        Returns:
            更新后的数据
        """
        follow = db_session.query(Follow).filter(
            and_(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
                Follow.deleted_at.is_(None)
            )
        ).first()
        
        if not follow:
            return None
        
        try:
            # 更新字段
            if 'group_tag' in data:
                follow.group_tag = data['group_tag']
            if 'remark' in data:
                follow.remark = data['remark']
            if 'is_muted' in data:
                follow.is_muted = data['is_muted']
            
            follow.updated_at = int(datetime.utcnow().timestamp())
            db_session.commit()
            
            return {
                'id': follow.id,
                'group_tag': follow.group_tag,
                'remark': follow.remark,
                'is_muted': follow.is_muted
            }
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def get_following_list(user_id: int, filters: Dict = None) -> Dict:
        """
        获取关注列表
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            
        Returns:
            关注列表数据
        """
        filters = filters or {}
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        group_tag = filters.get('group_tag')
        
        # 构建查询
        query = db_session.query(Follow).options(
            joinedload(Follow.following)
        ).filter(
            and_(
                Follow.follower_id == user_id,
                Follow.deleted_at.is_(None)
            )
        )
        
        # 分组筛选
        if group_tag:
            query = query.filter(Follow.group_tag == group_tag)
        
        # 排序
        query = query.order_by(desc(Follow.created_at))
        
        # 分页
        total = query.count()
        follows = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 构建结果
        items = []
        for follow in follows:
            items.append({
                'id': follow.id,
                'user': {
                    'id': follow.following.id,
                    'username': follow.following.username,
                    'nickname': follow.following.nickname,
                    'avatar': follow.following.avatar,
                    'followers_count': follow.following.followers_count
                },
                'is_mutual': follow.is_mutual,
                'group_tag': follow.group_tag,
                'remark': follow.remark,
                'is_muted': follow.is_muted,
                'followed_at': follow.created_at
            })
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def get_followers_list(user_id: int, filters: Dict = None) -> Dict:
        """
        获取粉丝列表
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            
        Returns:
            粉丝列表数据
        """
        filters = filters or {}
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        
        # 构建查询
        query = db_session.query(Follow).options(
            joinedload(Follow.follower)
        ).filter(
            and_(
                Follow.following_id == user_id,
                Follow.deleted_at.is_(None)
            )
        ).order_by(desc(Follow.created_at))
        
        # 分页
        total = query.count()
        follows = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 构建结果
        items = []
        for follow in follows:
            items.append({
                'id': follow.id,
                'user': {
                    'id': follow.follower.id,
                    'username': follow.follower.username,
                    'nickname': follow.follower.nickname,
                    'avatar': follow.follower.avatar,
                    'followers_count': follow.follower.followers_count
                },
                'is_mutual': follow.is_mutual,
                'followed_at': follow.created_at
            })
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def check_follow_status(user_id: int, target_user_id: int) -> Dict:
        """
        检查关注状态
        
        Args:
            user_id: 当前用户ID
            target_user_id: 目标用户ID
            
        Returns:
            关注状态
        """
        # 我是否关注了对方
        following = db_session.query(Follow).filter(
            and_(
                Follow.follower_id == user_id,
                Follow.following_id == target_user_id,
                Follow.deleted_at.is_(None)
            )
        ).first()
        
        # 对方是否关注了我
        followed_by = db_session.query(Follow).filter(
            and_(
                Follow.follower_id == target_user_id,
                Follow.following_id == user_id,
                Follow.deleted_at.is_(None)
            )
        ).first()
        
        return {
            'is_following': following is not None,
            'is_followed': followed_by is not None,
            'is_mutual': following is not None and followed_by is not None
        }
