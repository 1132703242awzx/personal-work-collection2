"""
通知服务层
处理系统通知、消息推送等业务逻辑
"""
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import and_, desc
from sqlalchemy.orm import joinedload
from config.database import db_session
from models.notification import Notification, NotificationSetting, Message, Conversation
from models.user import User


class NotificationService:
    """通知服务类"""
    
    @staticmethod
    def create_notification(user_id: int, data: Dict) -> Dict:
        """
        创建通知
        
        Args:
            user_id: 接收用户ID
            data: 通知数据
            
        Returns:
            通知数据
        """
        # 检查用户通知设置
        setting = db_session.query(NotificationSetting).filter_by(
            user_id=user_id
        ).first()
        
        notification_type = data['notification_type']
        
        # 如果用户关闭了该类型通知,不创建
        if setting:
            type_to_setting = {
                'follow': setting.follow_enabled,
                'like': setting.like_enabled,
                'comment': setting.comment_enabled,
                'reply': setting.reply_enabled,
                'mention': setting.mention_enabled,
                'achievement': setting.achievement_enabled,
                'milestone': setting.milestone_enabled,
                'workout_reminder': setting.workout_reminder_enabled,
                'system': setting.system_enabled
            }
            
            if notification_type in type_to_setting and not type_to_setting[notification_type]:
                return {'message': '用户已关闭此类型通知'}
        
        try:
            notification = Notification(
                user_id=user_id,
                sender_id=data.get('sender_id'),
                notification_type=notification_type,
                title=data['title'],
                content=data.get('content'),
                target_type=data.get('target_type'),
                target_id=data.get('target_id'),
                extra_data=data.get('extra_data'),
                action_url=data.get('action_url')
            )
            
            db_session.add(notification)
            db_session.commit()
            
            return {
                'id': notification.id,
                'title': notification.title,
                'created_at': notification.created_at
            }
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def get_notifications(user_id: int, filters: Dict = None) -> Dict:
        """
        获取通知列表
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            
        Returns:
            通知列表
        """
        filters = filters or {}
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        notification_type = filters.get('notification_type')
        is_read = filters.get('is_read')
        
        # 构建查询
        query = db_session.query(Notification).options(
            joinedload(Notification.sender)
        ).filter(
            and_(
                Notification.user_id == user_id,
                Notification.deleted_at.is_(None)
            )
        )
        
        # 类型筛选
        if notification_type:
            query = query.filter(Notification.notification_type == notification_type)
        
        # 已读状态筛选
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        
        # 排序
        query = query.order_by(desc(Notification.created_at))
        
        # 分页
        total = query.count()
        notifications = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 构建结果
        items = []
        for notif in notifications:
            sender_info = None
            if notif.sender:
                sender_info = {
                    'id': notif.sender.id,
                    'username': notif.sender.username,
                    'nickname': notif.sender.nickname,
                    'avatar': notif.sender.avatar
                }
            
            items.append({
                'id': notif.id,
                'sender': sender_info,
                'notification_type': notif.notification_type,
                'title': notif.title,
                'content': notif.content,
                'target_type': notif.target_type,
                'target_id': notif.target_id,
                'extra_data': notif.extra_data,
                'action_url': notif.action_url,
                'is_read': notif.is_read,
                'created_at': notif.created_at
            })
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def mark_as_read(user_id: int, notification_ids: List[int]) -> bool:
        """
        标记通知为已读
        
        Args:
            user_id: 用户ID
            notification_ids: 通知ID列表
            
        Returns:
            是否成功
        """
        try:
            notifications = db_session.query(Notification).filter(
                and_(
                    Notification.id.in_(notification_ids),
                    Notification.user_id == user_id,
                    Notification.deleted_at.is_(None)
                )
            ).all()
            
            for notif in notifications:
                notif.is_read = True
                notif.read_at = int(datetime.utcnow().timestamp())
            
            db_session.commit()
            return True
            
        except Exception as e:
            db_session.rollback()
            raise e
    
    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """
        获取未读通知数
        
        Args:
            user_id: 用户ID
            
        Returns:
            未读数量
        """
        count = db_session.query(Notification).filter(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.deleted_at.is_(None)
            )
        ).count()
        
        return count
    
    @staticmethod
    def update_notification_settings(user_id: int, data: Dict) -> Dict:
        """
        更新通知设置
        
        Args:
            user_id: 用户ID
            data: 设置数据
            
        Returns:
            更新后的设置
        """
        setting = db_session.query(NotificationSetting).filter_by(
            user_id=user_id
        ).first()
        
        if not setting:
            # 创建默认设置
            setting = NotificationSetting(user_id=user_id)
            db_session.add(setting)
        
        try:
            # 更新字段
            for key, value in data.items():
                if hasattr(setting, key):
                    setattr(setting, key, value)
            
            db_session.commit()
            
            return {
                'follow_enabled': setting.follow_enabled,
                'like_enabled': setting.like_enabled,
                'comment_enabled': setting.comment_enabled,
                'reply_enabled': setting.reply_enabled,
                'mention_enabled': setting.mention_enabled,
                'workout_reminder_enabled': setting.workout_reminder_enabled,
                'milestone_enabled': setting.milestone_enabled,
                'achievement_enabled': setting.achievement_enabled,
                'system_enabled': setting.system_enabled,
                'push_enabled': setting.push_enabled,
                'quiet_start_time': setting.quiet_start_time,
                'quiet_end_time': setting.quiet_end_time
            }
            
        except Exception as e:
            db_session.rollback()
            raise e


# ========== 辅助函数 ==========

def send_follow_notification(follower_id: int, following_id: int):
    """发送关注通知"""
    follower = db_session.query(User).filter_by(id=follower_id).first()
    if follower:
        NotificationService.create_notification(
            user_id=following_id,
            data={
                'sender_id': follower_id,
                'notification_type': 'follow',
                'title': '新关注',
                'content': f'{follower.nickname or follower.username} 关注了你',
                'action_url': f'/user/{follower_id}'
            }
        )


def send_like_notification(liker_id: int, target_user_id: int, 
                          target_type: str, target_id: int):
    """发送点赞通知"""
    liker = db_session.query(User).filter_by(id=liker_id).first()
    if liker:
        type_text = {
            'feed': '动态',
            'comment': '评论',
            'workout': '训练记录'
        }.get(target_type, '内容')
        
        NotificationService.create_notification(
            user_id=target_user_id,
            data={
                'sender_id': liker_id,
                'notification_type': 'like',
                'title': '新点赞',
                'content': f'{liker.nickname or liker.username} 赞了你的{type_text}',
                'target_type': target_type,
                'target_id': target_id,
                'action_url': f'/{target_type}/{target_id}'
            }
        )


def send_comment_notification(commenter_id: int, target_user_id: int,
                             target_type: str, target_id: int, content: str):
    """发送评论通知"""
    commenter = db_session.query(User).filter_by(id=commenter_id).first()
    if commenter:
        type_text = {
            'feed': '动态',
            'workout': '训练记录'
        }.get(target_type, '内容')
        
        NotificationService.create_notification(
            user_id=target_user_id,
            data={
                'sender_id': commenter_id,
                'notification_type': 'comment',
                'title': '新评论',
                'content': f'{commenter.nickname or commenter.username} 评论了你的{type_text}: {content[:50]}',
                'target_type': target_type,
                'target_id': target_id,
                'action_url': f'/{target_type}/{target_id}'
            }
        )
