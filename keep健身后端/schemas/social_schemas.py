"""
社交功能数据验证Schemas
使用Pydantic进行数据验证
"""
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime


# ========== 关注相关 ==========

class FollowCreate(BaseModel):
    """创建关注"""
    following_id: int = Field(..., description="被关注用户ID", gt=0)
    group_tag: Optional[str] = Field(None, max_length=50, description="分组标签")
    remark: Optional[str] = Field(None, max_length=100, description="备注名")


class FollowUpdate(BaseModel):
    """更新关注关系"""
    group_tag: Optional[str] = Field(None, max_length=50, description="分组标签")
    remark: Optional[str] = Field(None, max_length=100, description="备注名")
    is_muted: Optional[bool] = Field(None, description="是否静音")


class FollowListQuery(BaseModel):
    """关注列表查询"""
    user_id: Optional[int] = Field(None, description="用户ID", gt=0)
    list_type: str = Field('following', description="列表类型")  # following/followers/mutual
    group_tag: Optional[str] = Field(None, description="分组标签")
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")


# ========== 动态相关 ==========

class FeedCreate(BaseModel):
    """创建动态"""
    feed_type: str = Field(..., description="动态类型")
    title: Optional[str] = Field(None, max_length=200, description="标题")
    content: Optional[str] = Field(None, description="动态内容")
    images: Optional[List[str]] = Field(None, description="图片URL列表")
    video_url: Optional[str] = Field(None, description="视频URL")
    thumbnail_url: Optional[str] = Field(None, description="视频缩略图")
    workout_id: Optional[int] = Field(None, description="关联训练记录ID")
    hashtags: Optional[List[str]] = Field(None, description="话题标签")
    location: Optional[str] = Field(None, max_length=200, description="位置")
    visibility: str = Field('public', description="可见性")
    allow_comment: bool = Field(True, description="允许评论")
    allow_share: bool = Field(True, description="允许分享")
    
    @validator('feed_type')
    def validate_feed_type(cls, v):
        allowed = ['workout', 'achievement', 'milestone', 'photo', 'text', 'video']
        if v not in allowed:
            raise ValueError(f'动态类型必须是: {", ".join(allowed)}')
        return v
    
    @validator('visibility')
    def validate_visibility(cls, v):
        allowed = ['public', 'friends', 'private']
        if v not in allowed:
            raise ValueError(f'可见性必须是: {", ".join(allowed)}')
        return v


class FeedUpdate(BaseModel):
    """更新动态"""
    title: Optional[str] = Field(None, max_length=200, description="标题")
    content: Optional[str] = Field(None, description="动态内容")
    images: Optional[List[str]] = Field(None, description="图片URL列表")
    hashtags: Optional[List[str]] = Field(None, description="话题标签")
    visibility: Optional[str] = Field(None, description="可见性")
    allow_comment: Optional[bool] = Field(None, description="允许评论")
    allow_share: Optional[bool] = Field(None, description="允许分享")


class FeedListQuery(BaseModel):
    """动态列表查询"""
    user_id: Optional[int] = Field(None, description="用户ID", gt=0)
    feed_type: Optional[str] = Field(None, description="动态类型")
    hashtag: Optional[str] = Field(None, description="话题标签")
    visibility: Optional[str] = Field(None, description="可见性")
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")
    order_by: str = Field('created_at', description="排序字段")  # created_at/likes_count/hot


class FeedShareCreate(BaseModel):
    """分享动态"""
    feed_id: int = Field(..., description="动态ID", gt=0)
    share_comment: Optional[str] = Field(None, description="分享评论")
    share_to: str = Field('timeline', description="分享目标")
    
    @validator('share_to')
    def validate_share_to(cls, v):
        allowed = ['timeline', 'group', 'friend']
        if v not in allowed:
            raise ValueError(f'分享目标必须是: {", ".join(allowed)}')
        return v


# ========== 评论相关 ==========

class CommentCreate(BaseModel):
    """创建评论"""
    target_type: str = Field(..., description="目标类型")
    target_id: int = Field(..., description="目标ID", gt=0)
    content: str = Field(..., min_length=1, max_length=5000, description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID")
    reply_to_user_id: Optional[int] = Field(None, description="回复目标用户ID")
    images: Optional[List[str]] = Field(None, description="图片URL列表")
    mentions: Optional[List[int]] = Field(None, description="@提及的用户ID列表")
    
    @validator('target_type')
    def validate_target_type(cls, v):
        allowed = ['feed', 'workout', 'course', 'video']
        if v not in allowed:
            raise ValueError(f'目标类型必须是: {", ".join(allowed)}')
        return v


class CommentUpdate(BaseModel):
    """更新评论"""
    content: str = Field(..., min_length=1, max_length=5000, description="评论内容")
    images: Optional[List[str]] = Field(None, description="图片URL列表")


class CommentListQuery(BaseModel):
    """评论列表查询"""
    target_type: str = Field(..., description="目标类型")
    target_id: int = Field(..., description="目标ID", gt=0)
    parent_id: Optional[int] = Field(None, description="父评论ID")
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")
    order_by: str = Field('created_at', description="排序")  # created_at/likes_count


# ========== 点赞相关 ==========

class LikeCreate(BaseModel):
    """创建点赞"""
    target_type: str = Field(..., description="目标类型")
    target_id: int = Field(..., description="目标ID", gt=0)
    
    @validator('target_type')
    def validate_target_type(cls, v):
        allowed = ['feed', 'comment', 'workout', 'course']
        if v not in allowed:
            raise ValueError(f'目标类型必须是: {", ".join(allowed)}')
        return v


# ========== 通知相关 ==========

class NotificationListQuery(BaseModel):
    """通知列表查询"""
    notification_type: Optional[str] = Field(None, description="通知类型")
    is_read: Optional[bool] = Field(None, description="是否已读")
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")


class NotificationMarkRead(BaseModel):
    """标记通知已读"""
    notification_ids: List[int] = Field(..., description="通知ID列表")


class NotificationSettingUpdate(BaseModel):
    """更新通知设置"""
    follow_enabled: Optional[bool] = Field(None, description="关注通知")
    like_enabled: Optional[bool] = Field(None, description="点赞通知")
    comment_enabled: Optional[bool] = Field(None, description="评论通知")
    reply_enabled: Optional[bool] = Field(None, description="回复通知")
    mention_enabled: Optional[bool] = Field(None, description="@提及通知")
    workout_reminder_enabled: Optional[bool] = Field(None, description="训练提醒")
    milestone_enabled: Optional[bool] = Field(None, description="里程碑通知")
    achievement_enabled: Optional[bool] = Field(None, description="成就通知")
    system_enabled: Optional[bool] = Field(None, description="系统通知")
    push_enabled: Optional[bool] = Field(None, description="推送通知总开关")
    quiet_start_time: Optional[str] = Field(None, description="免打扰开始时间")
    quiet_end_time: Optional[str] = Field(None, description="免打扰结束时间")


# ========== 私信相关 ==========

class MessageCreate(BaseModel):
    """发送私信"""
    receiver_id: int = Field(..., description="接收者ID", gt=0)
    message_type: str = Field('text', description="消息类型")
    content: Optional[str] = Field(None, description="消息内容")
    image_url: Optional[str] = Field(None, description="图片URL")
    workout_id: Optional[int] = Field(None, description="关联训练记录")
    feed_id: Optional[int] = Field(None, description="关联动态")
    
    @validator('message_type')
    def validate_message_type(cls, v):
        allowed = ['text', 'image', 'workout', 'feed']
        if v not in allowed:
            raise ValueError(f'消息类型必须是: {", ".join(allowed)}')
        return v


class MessageListQuery(BaseModel):
    """消息列表查询"""
    conversation_id: Optional[str] = Field(None, description="会话ID")
    other_user_id: Optional[int] = Field(None, description="对方用户ID")
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")


class ConversationListQuery(BaseModel):
    """会话列表查询"""
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")


# ========== 话题标签相关 ==========

class HashtagCreate(BaseModel):
    """创建话题标签"""
    name: str = Field(..., min_length=1, max_length=50, description="标签名称")
    description: Optional[str] = Field(None, description="标签描述")
    category: Optional[str] = Field(None, description="标签分类")


class HashtagListQuery(BaseModel):
    """话题标签列表查询"""
    category: Optional[str] = Field(None, description="标签分类")
    is_trending: Optional[bool] = Field(None, description="是否热门")
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")
    order_by: str = Field('feeds_count', description="排序")  # feeds_count/followers_count


# ========== 成就相关 ==========

class UserAchievementListQuery(BaseModel):
    """用户成就列表查询"""
    user_id: Optional[int] = Field(None, description="用户ID")
    achievement_type: Optional[str] = Field(None, description="成就类型")
    is_unlocked: Optional[bool] = Field(None, description="是否已解锁")
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")
