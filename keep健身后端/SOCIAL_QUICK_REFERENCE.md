# Keep健身 - 社交系统快速参考

## 🚀 快速开始

### 基础信息
- **Base URL**: `http://localhost:5000/api/social`
- **认证**: `Authorization: Bearer <token>`
- **内容类型**: `Content-Type: application/json`

---

## 📋 API速查表

### 关注关系 (5个接口)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/follow` | 关注用户 |
| POST | `/unfollow/{user_id}` | 取消关注 |
| GET | `/following` | 我的关注列表 |
| GET | `/followers` | 我的粉丝列表 |
| GET | `/follow-status/{user_id}` | 检查关注状态 |

### 动态Feed (7个接口)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/feeds` | 发布动态 |
| GET | `/feeds/{id}` | 动态详情 |
| GET | `/timeline` | 关注动态流 |
| GET | `/explore` | 探索热门 |
| GET | `/users/{id}/feeds` | 用户动态 |
| PUT | `/feeds/{id}` | 更新动态 |
| DELETE | `/feeds/{id}` | 删除动态 |

### 互动系统 (3个接口)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/like` | 点赞/取消 |
| POST | `/comments` | 发表评论 |
| GET | `/comments` | 评论列表 |
| DELETE | `/comments/{id}` | 删除评论 |

### 通知系统 (4个接口)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/notifications` | 通知列表 |
| POST | `/notifications/read` | 标记已读 |
| GET | `/notifications/unread-count` | 未读数量 |
| GET/PUT | `/notification-settings` | 通知设置 |

---

## 🔥 常用场景

### 场景1: 关注用户流程
```http
# 1. 关注用户
POST /api/social/follow
{
    "following_id": 2,
    "group_tag": "好友",
    "remark": "健身伙伴"
}

# 2. 检查关注状态
GET /api/social/follow-status/2
# 返回: {"is_following": true, "is_followed": false, "is_mutual": false}
```

---

### 场景2: 发布训练动态
```http
# 发布训练动态
POST /api/social/feeds
{
    "feed_type": "workout",
    "content": "今天完成5公里跑步,感觉很棒!💪",
    "workout_record_id": 10,
    "hashtags": ["#跑步", "#减脂"],
    "location": "北京市朝阳区",
    "visibility": "public"
}

# 系统会自动提取训练记录摘要到 workout_summary
```

---

### 场景3: 浏览动态流
```http
# 方式1: 查看关注用户动态(时间线)
GET /api/social/timeline?page=1&per_page=20

# 方式2: 浏览热门动态(探索页)
GET /api/social/explore?page=1&per_page=20

# 方式3: 查看某用户所有动态
GET /api/social/users/2/feeds?page=1
```

---

### 场景4: 互动(点赞+评论)
```http
# 1. 点赞动态
POST /api/social/like
{
    "target_type": "feed",
    "target_id": 1
}

# 2. 发表评论
POST /api/social/comments
{
    "target_type": "feed",
    "target_id": 1,
    "content": "真棒!加油!💪"
}

# 3. 回复评论
POST /api/social/comments
{
    "target_type": "feed",
    "target_id": 1,
    "content": "谢谢鼓励!",
    "parent_id": 5,
    "reply_to_user_id": 2
}

# 4. 获取评论列表
GET /api/social/comments?target_type=feed&target_id=1&order_by=likes_count
```

---

### 场景5: 通知管理
```http
# 1. 获取未读通知数(用于角标显示)
GET /api/social/notifications/unread-count
# 返回: {"unread_count": 15}

# 2. 获取通知列表
GET /api/social/notifications?is_read=false&page=1&per_page=20

# 3. 批量标记已读
POST /api/social/notifications/read
{
    "notification_ids": [1, 2, 3, 4, 5]
}

# 4. 更新通知设置(关闭点赞通知)
PUT /api/social/notification-settings
{
    "like_enabled": false,
    "quiet_start_time": "23:00",
    "quiet_end_time": "07:00"
}
```

---

## 📊 数据模型快览

### Feed动态类型
```python
feed_type = "workout"     # 训练分享
feed_type = "achievement" # 成就分享
feed_type = "photo"       # 图文动态
feed_type = "text"        # 纯文字
feed_type = "video"       # 视频动态
```

### Feed可见性
```python
visibility = "public"   # 公开(所有人可见)
visibility = "friends"  # 好友可见
visibility = "private"  # 私密(仅自己)
```

### 点赞目标类型
```python
target_type = "feed"           # 动态
target_type = "comment"        # 评论
target_type = "workout_record" # 训练记录
```

### 通知类型
```python
type = "follow"           # 新关注
type = "like"            # 点赞
type = "comment"         # 评论
type = "reply"           # 回复
type = "mention"         # @提到
type = "share"           # 分享
type = "achievement"     # 成就解锁
type = "system"          # 系统通知
type = "workout_reminder" # 训练提醒
type = "milestone"       # 里程碑
```

---

## 💡 技术要点

### 1. 分页参数
所有列表接口统一使用:
- `page`: 页码(默认1)
- `per_page`: 每页数量(默认20)

返回格式:
```json
{
    "items": [...],
    "total": 100,
    "page": 1,
    "per_page": 20,
    "pages": 5
}
```

---

### 2. 热度算法
探索页动态排序算法:
```
热度分 = 点赞数 × 0.5 + 评论数 × 0.3 + 分享数 × 0.2
```

---

### 3. 评论层级
- **一级评论**: `parent_id=null, level=0`
- **二级评论**: `parent_id=父评论ID, level=1`

加载策略:
1. 首次加载一级评论
2. 点击"查看N条回复"加载二级评论: `GET /comments?parent_id=5`

---

### 4. 可见性权限
| 可见性 | 可查看者 |
|--------|---------|
| public | 所有人 |
| friends | 互相关注的好友 |
| private | 仅作者本人 |

---

### 5. 互相关注判断
```json
{
    "is_following": true,  // 我关注了对方
    "is_followed": true,   // 对方关注了我
    "is_mutual": true      // 互相关注(好友)
}
```

---

## 🎯 性能优化建议

### 1. 时间线缓存
- 时间线数据可缓存5-10分钟
- 下拉刷新时清除缓存

### 2. 点赞乐观更新
```javascript
// 先更新UI(乐观更新)
likes_count++
is_liked = true

// 再调API
POST /api/social/like
```

### 3. 评论分批加载
- 一级评论: 首次加载20条
- 二级评论: 点击时加载,每次10条

### 4. 通知轮询间隔
- 活跃状态: 30秒轮询一次
- 后台状态: 暂停轮询

---

## 🛡️ 安全注意事项

### 1. Token验证
所有接口都需要有效的JWT Token:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. 权限检查
- 只能编辑/删除自己的动态
- 只能删除自己的评论
- 查看私密动态需要权限

### 3. 频率限制(建议)
- 发布动态: 1分钟内最多3条
- 评论: 1分钟内最多10条
- 点赞: 1分钟内最多30次

---

## 📱 前端集成示例

### React Hook示例
```javascript
// 获取时间线
const useTimeline = () => {
    const [feeds, setFeeds] = useState([])
    const [loading, setLoading] = useState(false)
    
    const loadMore = async (page = 1) => {
        setLoading(true)
        const res = await fetch(
            `/api/social/timeline?page=${page}&per_page=20`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        )
        const data = await res.json()
        setFeeds(prev => [...prev, ...data.data.items])
        setLoading(false)
    }
    
    return { feeds, loading, loadMore }
}

// 点赞功能
const toggleLike = async (feedId) => {
    await fetch('/api/social/like', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            target_type: 'feed',
            target_id: feedId
        })
    })
}
```

---

## 🧪 测试工具

使用提供的测试工具快速验证功能:
```bash
python test_social.py
```

---

## 📞 支持

- **完整文档**: `SOCIAL_API.md`
- **问题反馈**: GitHub Issues
- **技术支持**: tech@keep.com

---

**最后更新**: 2024-01-01 | **版本**: v1.0
