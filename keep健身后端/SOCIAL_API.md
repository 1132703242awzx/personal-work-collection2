# Keep健身 - 社交系统API文档

## 目录
- [概述](#概述)
- [数据模型](#数据模型)
- [关注关系API](#关注关系api)
- [动态Feed API](#动态feed-api)
- [互动API](#互动api)
- [通知API](#通知api)
- [消息API](#消息api)
- [成就系统API](#成就系统api)
- [标签系统API](#标签系统api)

## 概述

社交系统提供完整的社交网络功能,包括:
- 用户关注/粉丝关系管理
- 动态发布与浏览(训练分享、图文、视频等)
- 点赞和评论互动
- 实时通知系统
- 私信消息
- 成就徽章系统
- 话题标签系统

**基础URL**: `http://localhost:5000/api/social`

**认证方式**: Bearer Token (在请求头中添加 `Authorization: Bearer <token>`)

## 数据模型

### Follow(关注关系)
```json
{
    "id": 1,
    "follower_id": 1,        // 关注者ID
    "following_id": 2,       // 被关注者ID
    "is_mutual": true,       // 是否互相关注
    "group_tag": "好友",     // 分组标签
    "remark": "健身伙伴",    // 备注名
    "is_muted": false,       // 是否屏蔽动态
    "created_at": "2024-01-01T00:00:00"
}
```

### Feed(动态)
```json
{
    "id": 1,
    "user_id": 1,
    "feed_type": "workout",          // 类型: workout/achievement/photo/text/video
    "content": "今天完成5公里跑步!",  // 文字内容
    "images": ["url1", "url2"],      // 图片URLs数组
    "video_url": "video_url",        // 视频URL
    "workout_record_id": 10,         // 关联的训练记录ID
    "workout_summary": {             // 训练摘要
        "duration": 1800,
        "calories": 300,
        "distance": 5.0
    },
    "hashtags": ["#跑步", "#减脂"],  // 话题标签
    "location": "北京市朝阳区",       // 地理位置
    "visibility": "public",          // 可见性: public/friends/private
    "likes_count": 100,
    "comments_count": 20,
    "shares_count": 5,
    "views_count": 500,
    "created_at": "2024-01-01T00:00:00",
    "is_liked": false                // 当前用户是否点赞
}
```

### Comment(评论)
```json
{
    "id": 1,
    "user_id": 1,
    "target_type": "feed",      // feed/workout_record
    "target_id": 1,
    "content": "真棒!",
    "parent_id": null,          // 父评论ID(嵌套评论)
    "level": 0,                 // 层级: 0=一级评论, 1=回复
    "reply_to_user_id": null,   // 回复目标用户ID
    "mentions": [2, 3],         // @提到的用户IDs
    "likes_count": 10,
    "replies_count": 2,
    "created_at": "2024-01-01T00:00:00"
}
```

### Like(点赞)
```json
{
    "id": 1,
    "user_id": 1,
    "target_type": "feed",      // feed/comment/workout_record
    "target_id": 1,
    "is_active": true,          // 是否有效(取消点赞设为false)
    "created_at": "2024-01-01T00:00:00"
}
```

### Notification(通知)
```json
{
    "id": 1,
    "user_id": 1,               // 接收通知的用户
    "type": "like",             // 类型: follow/like/comment/reply/mention/share/achievement/system/workout_reminder/milestone
    "sender_id": 2,             // 发送者ID
    "target_type": "feed",      // 目标类型
    "target_id": 1,             // 目标ID
    "content": "张三点赞了你的动态",
    "extra_data": {},           // 额外数据(JSON)
    "is_read": false,
    "read_at": null,
    "created_at": "2024-01-01T00:00:00"
}
```

### Message(消息)
```json
{
    "id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "conversation_id": 1,
    "message_type": "text",     // text/image/workout/feed
    "content": "你好!",
    "extra_data": {},           // 额外数据
    "is_read": false,
    "read_at": null,
    "is_recalled": false,       // 是否撤回
    "created_at": "2024-01-01T00:00:00"
}
```

---

## 关注关系API

### 1. 关注用户
**POST** `/api/social/follow`

关注指定用户并建立关系。

**请求体**:
```json
{
    "following_id": 2,
    "group_tag": "好友",
    "remark": "健身伙伴"
}
```

**参数说明**:
- `following_id` (必填): 要关注的用户ID
- `group_tag` (可选): 分组标签
- `remark` (可选): 备注名称

**成功响应** (200):
```json
{
    "code": 200,
    "message": "关注成功",
    "data": {
        "id": 1,
        "follower_id": 1,
        "following_id": 2,
        "is_mutual": false,
        "group_tag": "好友",
        "remark": "健身伙伴",
        "created_at": "2024-01-01T00:00:00"
    }
}
```

**错误响应**:
- 400: 不能关注自己
- 400: 已经关注过该用户
- 404: 用户不存在

---

### 2. 取消关注
**POST** `/api/social/unfollow/{user_id}`

取消关注指定用户。

**路径参数**:
- `user_id`: 要取消关注的用户ID

**成功响应** (200):
```json
{
    "code": 200,
    "message": "取消关注成功"
}
```

**错误响应**:
- 404: 关注关系不存在

---

### 3. 更新关注信息
**PUT** `/api/social/follow/{follow_id}`

更新关注关系的分组、备注等信息。

**路径参数**:
- `follow_id`: 关注关系ID

**请求体**:
```json
{
    "group_tag": "铁子",
    "remark": "跑步搭档",
    "is_muted": false
}
```

**成功响应** (200):
```json
{
    "code": 200,
    "message": "更新成功",
    "data": {
        "id": 1,
        "group_tag": "铁子",
        "remark": "跑步搭档",
        "is_muted": false
    }
}
```

---

### 4. 获取关注列表
**GET** `/api/social/following`

获取当前用户关注的用户列表。

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量
- `group_tag` (可选): 按分组筛选

**示例**: `GET /api/social/following?page=1&per_page=20&group_tag=好友`

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "following": {
                    "id": 2,
                    "username": "zhangsan",
                    "nickname": "张三",
                    "avatar": "avatar_url"
                },
                "is_mutual": true,
                "group_tag": "好友",
                "remark": "健身伙伴",
                "created_at": "2024-01-01T00:00:00"
            }
        ],
        "total": 50,
        "page": 1,
        "per_page": 20,
        "pages": 3
    }
}
```

---

### 5. 获取粉丝列表
**GET** `/api/social/followers`

获取关注当前用户的粉丝列表。

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 2,
                "follower": {
                    "id": 3,
                    "username": "lisi",
                    "nickname": "李四",
                    "avatar": "avatar_url"
                },
                "is_mutual": false,
                "created_at": "2024-01-01T00:00:00"
            }
        ],
        "total": 30,
        "page": 1,
        "per_page": 20,
        "pages": 2
    }
}
```

---

### 6. 检查关注状态
**GET** `/api/social/follow-status/{user_id}`

检查与指定用户的关注关系状态。

**路径参数**:
- `user_id`: 目标用户ID

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "is_following": true,    // 我是否关注对方
        "is_followed": true,     // 对方是否关注我
        "is_mutual": true        // 是否互相关注
    }
}
```

---

## 动态Feed API

### 7. 发布动态
**POST** `/api/social/feeds`

发布新动态(支持训练分享、图文、视频等)。

**请求体**:
```json
{
    "feed_type": "workout",
    "content": "今天完成5公里跑步,感觉很棒!",
    "images": ["https://example.com/img1.jpg"],
    "video_url": null,
    "workout_record_id": 10,
    "hashtags": ["#跑步", "#减脂"],
    "location": "北京市朝阳区",
    "visibility": "public"
}
```

**参数说明**:
- `feed_type` (必填): 类型 - workout(训练)/achievement(成就)/photo(图文)/text(纯文字)/video(视频)
- `content` (必填): 文字内容
- `images` (可选): 图片URL数组
- `video_url` (可选): 视频URL
- `workout_record_id` (可选): 关联训练记录ID(类型为workout时使用)
- `hashtags` (可选): 话题标签数组
- `location` (可选): 地理位置
- `visibility` (必填): 可见性 - public(公开)/friends(好友可见)/private(私密)

**成功响应** (200):
```json
{
    "code": 200,
    "message": "发布成功",
    "data": {
        "id": 1,
        "user_id": 1,
        "feed_type": "workout",
        "content": "今天完成5公里跑步,感觉很棒!",
        "images": ["https://example.com/img1.jpg"],
        "workout_summary": {
            "duration": 1800,
            "calories": 300,
            "distance": 5.0
        },
        "hashtags": ["#跑步", "#减脂"],
        "visibility": "public",
        "created_at": "2024-01-01T00:00:00"
    }
}
```

---

### 8. 获取动态详情
**GET** `/api/social/feeds/{feed_id}`

获取指定动态的详细信息。

**路径参数**:
- `feed_id`: 动态ID

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "id": 1,
        "user": {
            "id": 1,
            "username": "user1",
            "nickname": "用户一",
            "avatar": "avatar_url"
        },
        "feed_type": "workout",
        "content": "今天完成5公里跑步!",
        "images": ["url1"],
        "workout_summary": {
            "duration": 1800,
            "calories": 300
        },
        "hashtags": ["#跑步"],
        "likes_count": 100,
        "comments_count": 20,
        "shares_count": 5,
        "views_count": 501,
        "is_liked": false,
        "created_at": "2024-01-01T00:00:00"
    }
}
```

**错误响应**:
- 403: 无权限查看(私密动态)
- 404: 动态不存在

---

### 9. 获取动态时间线
**GET** `/api/social/timeline`

获取关注用户的动态时间线(包括自己的动态)。

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量
- `feed_type` (可选): 按类型筛选

**示例**: `GET /api/social/timeline?page=1&per_page=20&feed_type=workout`

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "user": {
                    "id": 2,
                    "username": "zhangsan",
                    "nickname": "张三"
                },
                "feed_type": "workout",
                "content": "完成训练!",
                "likes_count": 50,
                "is_liked": true,
                "created_at": "2024-01-01T12:00:00"
            }
        ],
        "total": 100,
        "page": 1,
        "per_page": 20,
        "pages": 5
    }
}
```

---

### 10. 获取探索页动态
**GET** `/api/social/explore`

获取热门公开动态(使用热度算法排序)。

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量
- `feed_type` (可选): 按类型筛选

**热度算法**: `热度 = 点赞数 × 0.5 + 评论数 × 0.3 + 分享数 × 0.2`

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 10,
                "user": {
                    "id": 5,
                    "username": "fitness_star",
                    "nickname": "健身达人"
                },
                "content": "突破个人记录!",
                "likes_count": 500,
                "comments_count": 100,
                "hot_score": 280.0,
                "created_at": "2024-01-01T10:00:00"
            }
        ],
        "total": 200,
        "page": 1,
        "per_page": 20
    }
}
```

---

### 11. 获取用户动态列表
**GET** `/api/social/users/{user_id}/feeds`

获取指定用户的动态列表。

**路径参数**:
- `user_id`: 用户ID

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [...],
        "total": 30,
        "page": 1,
        "per_page": 20
    }
}
```

**注意**: 根据可见性设置,只能看到public动态或好友可见动态

---

### 12. 更新动态
**PUT** `/api/social/feeds/{feed_id}`

更新自己发布的动态。

**路径参数**:
- `feed_id`: 动态ID

**请求体**:
```json
{
    "content": "更新后的内容",
    "images": ["new_url"],
    "hashtags": ["#新标签"],
    "visibility": "friends"
}
```

**成功响应** (200):
```json
{
    "code": 200,
    "message": "更新成功",
    "data": {...}
}
```

**错误响应**:
- 403: 只能编辑自己的动态

---

### 13. 删除动态
**DELETE** `/api/social/feeds/{feed_id}`

删除自己发布的动态。

**路径参数**:
- `feed_id`: 动态ID

**成功响应** (200):
```json
{
    "code": 200,
    "message": "删除成功"
}
```

**错误响应**:
- 403: 只能删除自己的动态

---

## 互动API

### 14. 点赞/取消点赞
**POST** `/api/social/like`

对动态、评论或训练记录进行点赞或取消点赞(切换操作)。

**请求体**:
```json
{
    "target_type": "feed",
    "target_id": 1
}
```

**参数说明**:
- `target_type` (必填): 目标类型 - feed(动态)/comment(评论)/workout_record(训练记录)
- `target_id` (必填): 目标ID

**成功响应** (200):
```json
{
    "code": 200,
    "message": "点赞成功",  // 或 "取消点赞成功"
    "data": {
        "is_liked": true,
        "likes_count": 101
    }
}
```

---

### 15. 发表评论
**POST** `/api/social/comments`

对动态或训练记录发表评论,支持嵌套回复。

**请求体**:
```json
{
    "target_type": "feed",
    "target_id": 1,
    "content": "真棒!加油!",
    "parent_id": null,
    "reply_to_user_id": null,
    "mentions": [2, 3]
}
```

**参数说明**:
- `target_type` (必填): feed/workout_record
- `target_id` (必填): 目标ID
- `content` (必填): 评论内容
- `parent_id` (可选): 父评论ID(回复评论时使用)
- `reply_to_user_id` (可选): 回复的目标用户ID
- `mentions` (可选): @提到的用户ID数组

**成功响应** (200):
```json
{
    "code": 200,
    "message": "评论成功",
    "data": {
        "id": 1,
        "user_id": 1,
        "content": "真棒!加油!",
        "level": 0,
        "mentions": [2, 3],
        "created_at": "2024-01-01T00:00:00"
    }
}
```

---

### 16. 获取评论列表
**GET** `/api/social/comments`

获取指定目标的评论列表。

**查询参数**:
- `target_type` (必填): feed/workout_record
- `target_id` (必填): 目标ID
- `parent_id` (可选): 父评论ID(获取子评论)
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量
- `order_by` (可选, 默认created_at): 排序字段 - created_at(时间)/likes_count(点赞数)

**示例**: `GET /api/social/comments?target_type=feed&target_id=1&order_by=likes_count`

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "user": {
                    "id": 2,
                    "username": "zhangsan",
                    "nickname": "张三"
                },
                "content": "太厉害了!",
                "level": 0,
                "likes_count": 10,
                "replies_count": 2,
                "created_at": "2024-01-01T00:00:00"
            }
        ],
        "total": 50,
        "page": 1,
        "per_page": 20
    }
}
```

---

### 17. 删除评论
**DELETE** `/api/social/comments/{comment_id}`

删除自己发表的评论。

**路径参数**:
- `comment_id`: 评论ID

**成功响应** (200):
```json
{
    "code": 200,
    "message": "删除成功"
}
```

**错误响应**:
- 403: 只能删除自己的评论

---

## 通知API

### 18. 获取通知列表
**GET** `/api/social/notifications`

获取当前用户的通知列表。

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量
- `type` (可选): 按类型筛选 - follow/like/comment/reply/mention/share/achievement/system/workout_reminder/milestone
- `is_read` (可选): 按阅读状态筛选 - true/false

**示例**: `GET /api/social/notifications?type=like&is_read=false`

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "type": "like",
                "sender": {
                    "id": 2,
                    "username": "zhangsan",
                    "nickname": "张三",
                    "avatar": "avatar_url"
                },
                "content": "张三点赞了你的动态",
                "target_type": "feed",
                "target_id": 1,
                "is_read": false,
                "created_at": "2024-01-01T00:00:00"
            }
        ],
        "total": 100,
        "page": 1,
        "per_page": 20
    }
}
```

---

### 19. 标记通知为已读
**POST** `/api/social/notifications/read`

批量标记通知为已读状态。

**请求体**:
```json
{
    "notification_ids": [1, 2, 3]
}
```

**参数说明**:
- `notification_ids` (必填): 要标记的通知ID数组

**成功响应** (200):
```json
{
    "code": 200,
    "message": "标记成功",
    "data": {
        "count": 3
    }
}
```

---

### 20. 获取未读通知数量
**GET** `/api/social/notifications/unread-count`

获取当前用户的未读通知数量。

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "unread_count": 15
    }
}
```

---

### 21. 获取通知设置
**GET** `/api/social/notification-settings`

获取当前用户的通知偏好设置。

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "user_id": 1,
        "push_enabled": true,
        "follow_enabled": true,
        "like_enabled": true,
        "comment_enabled": true,
        "reply_enabled": true,
        "mention_enabled": true,
        "share_enabled": true,
        "achievement_enabled": true,
        "system_enabled": true,
        "workout_reminder_enabled": true,
        "milestone_enabled": true,
        "quiet_start_time": "22:00",
        "quiet_end_time": "08:00"
    }
}
```

---

### 22. 更新通知设置
**PUT** `/api/social/notification-settings`

更新通知偏好设置。

**请求体**:
```json
{
    "push_enabled": true,
    "like_enabled": false,
    "quiet_start_time": "23:00",
    "quiet_end_time": "07:00"
}
```

**成功响应** (200):
```json
{
    "code": 200,
    "message": "更新成功",
    "data": {...}
}
```

---

## 消息API

### 23. 发送私信
**POST** `/api/social/messages`

向指定用户发送私信。

**请求体**:
```json
{
    "receiver_id": 2,
    "message_type": "text",
    "content": "你好!",
    "extra_data": {}
}
```

**参数说明**:
- `receiver_id` (必填): 接收者用户ID
- `message_type` (必填): 消息类型 - text(文字)/image(图片)/workout(训练分享)/feed(动态分享)
- `content` (必填): 消息内容
- `extra_data` (可选): 额外数据(JSON对象)

**成功响应** (200):
```json
{
    "code": 200,
    "message": "发送成功",
    "data": {
        "id": 1,
        "sender_id": 1,
        "receiver_id": 2,
        "conversation_id": 1,
        "message_type": "text",
        "content": "你好!",
        "created_at": "2024-01-01T00:00:00"
    }
}
```

---

### 24. 获取会话列表
**GET** `/api/social/conversations`

获取当前用户的所有会话列表。

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认20): 每页数量

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "user1": {...},
                "user2": {...},
                "last_message": "你好!",
                "last_message_time": "2024-01-01T00:00:00",
                "unread_count_user1": 0,
                "unread_count_user2": 3
            }
        ],
        "total": 10,
        "page": 1,
        "per_page": 20
    }
}
```

---

### 25. 获取会话消息
**GET** `/api/social/conversations/{conversation_id}/messages`

获取指定会话的消息记录。

**路径参数**:
- `conversation_id`: 会话ID

**查询参数**:
- `page` (可选, 默认1): 页码
- `per_page` (可选, 默认50): 每页数量

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "sender": {...},
                "message_type": "text",
                "content": "你好!",
                "is_read": true,
                "created_at": "2024-01-01T00:00:00"
            }
        ],
        "total": 100,
        "page": 1,
        "per_page": 50
    }
}
```

---

## 成就系统API

### 26. 获取用户成就列表
**GET** `/api/social/users/{user_id}/achievements`

获取用户已解锁的成就列表。

**路径参数**:
- `user_id`: 用户ID

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "achievement": {
                    "id": 1,
                    "name": "跑步新手",
                    "description": "完成首次跑步",
                    "icon": "icon_url",
                    "category": "running",
                    "rarity": "common"
                },
                "unlocked_at": "2024-01-01T00:00:00",
                "progress": 100
            }
        ],
        "total": 15
    }
}
```

---

### 27. 获取所有成就
**GET** `/api/social/achievements`

获取系统所有可获得的成就。

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "name": "跑步新手",
                "description": "完成首次跑步",
                "icon": "icon_url",
                "category": "running",
                "rarity": "common",
                "unlock_condition": {
                    "type": "workout_count",
                    "exercise_id": 1,
                    "count": 1
                }
            }
        ]
    }
}
```

---

## 标签系统API

### 28. 获取热门标签
**GET** `/api/social/hashtags/trending`

获取热门话题标签。

**查询参数**:
- `limit` (可选, 默认10): 返回数量

**成功响应** (200):
```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "tag": "#跑步",
                "feeds_count": 1000,
                "followers_count": 500,
                "is_trending": true
            }
        ]
    }
}
```

---

### 29. 关注标签
**POST** `/api/social/hashtags/{hashtag_id}/follow`

关注话题标签,关注后会在时间线看到该标签的动态。

**路径参数**:
- `hashtag_id`: 标签ID

**成功响应** (200):
```json
{
    "code": 200,
    "message": "关注成功"
}
```

---

### 30. 取消关注标签
**DELETE** `/api/social/hashtags/{hashtag_id}/follow`

取消关注话题标签。

**路径参数**:
- `hashtag_id`: 标签ID

**成功响应** (200):
```json
{
    "code": 200,
    "message": "取消关注成功"
}
```

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权(token无效或过期) |
| 403 | 禁止访问(无权限) |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 最佳实践

### 1. 动态时间线刷新策略
- 首次加载: `GET /api/social/timeline?page=1&per_page=20`
- 下拉刷新: 获取最新动态
- 上拉加载: `page=2,3...`

### 2. 点赞优化
- 使用`toggle_like`实现点赞/取消点赞切换
- 客户端立即更新UI,无需等待服务器响应

### 3. 评论层级
- 一级评论: `parent_id=null, level=0`
- 二级评论(回复): `parent_id=父评论ID, level=1`
- 显示"查看更多回复"按钮加载子评论

### 4. 通知轮询
- 定时调用`GET /api/social/notifications/unread-count`
- 建议间隔: 30-60秒
- 或使用WebSocket实现实时推送(待开发)

### 5. 隐私控制
- 动态可见性: public(所有人)/friends(好友)/private(仅自己)
- 屏蔽用户动态: 设置`is_muted=true`

---

## 开发计划

**已完成**:
- ✅ 关注关系管理
- ✅ 动态发布与浏览
- ✅ 点赞评论系统
- ✅ 通知系统
- ✅ 私信消息
- ✅ 成就徽章
- ✅ 话题标签

**待开发**:
- ⏳ WebSocket实时通知
- ⏳ 消息已读回执
- ⏳ 社交数据分析
- ⏳ 推荐算法优化
- ⏳ 动态置顶功能
- ⏳ 用户黑名单

---

**更新时间**: 2024-01-01
**版本**: v1.0
