# 课程和视频管理系统 - 完整实现文档 📹

**创建日期**: 2025-10-19  
**系统版本**: 1.0.0  
**文档状态**: 开发中

---

## 📋 目录

1. [系统概述](#系统概述)
2. [功能模块](#功能模块)
3. [技术架构](#技术架构)
4. [数据模型](#数据模型)
5. [API接口](#api接口)
6. [视频处理流程](#视频处理流程)
7. [缓存策略](#缓存策略)
8. [安装部署](#安装部署)
9. [开发指南](#开发指南)

---

## 🎯 系统概述

### 设计目标
构建一个企业级的课程和视频管理系统,支持:
- 📚 完整的课程管理功能
- 🎬 视频上传和转码处理
- 🔐 灵活的权限控制
- 📊 学习进度跟踪
- 💾 高性能缓存
- 🚀 异步任务处理

### 核心特性
✅ **课程管理**
- 课程分类和标签系统
- 多级课程结构(课程→章节→视频)
- 课程发布和审核
- 教练课程管理

✅ **视频处理**
- 分片上传支持大文件
- 异步转码多清晰度
- 自动生成多种格式
- FFmpeg视频处理

✅ **权限控制**
- 免费/付费课程
- 试看功能
- 会员专享
- 有效期管理

✅ **学习跟踪**
- 观看进度记录
- 完成度统计
- 学习时长统计
- 个人学习档案

✅ **性能优化**
- Redis缓存热门数据
- Celery异步任务
- 数据库查询优化
- CDN资源加速

---

## 📦 功能模块

### 1. 课程分类和标签 ✅

**功能描述**: 多级分类体系和灵活标签系统

**数据模型**:
```
CourseCategory (课程分类)
├── 层级结构 (parent_id, level, path)
├── 显示控制 (order_number, is_active)
└── 统计信息 (course_count)

CourseTag (课程标签)
├── 标签类型 (general/level/body_part/goal)
├── 显示样式 (color)
└── 使用统计 (course_count)

CourseTagRelation (多对多关系)
```

**核心功能**:
- 创建/编辑分类和标签
- 分类树形结构
- 标签批量管理
- 课程关联标签

### 2. 视频上传和转码 ✅

**功能描述**: 支持大文件分片上传和异步转码

**处理流程**:
```
1. 创建上传任务 → 获取task_id
2. 分片上传 → 实时进度反馈
3. 合并分片 → 触发处理任务
4. 视频转码 → 生成多清晰度
5. 更新记录 → 完成状态
```

**转码清晰度**:
- SD (标清): 640x360, 800kbps
- HD (高清): 1280x720, 2.5Mbps  
- FHD (超清): 1920x1080, 5Mbps
- 4K (超高清): 3840x2160, 15Mbps

**数据模型**:
```
VideoUploadTask (上传任务)
├── 文件信息 (filename, size, md5)
├── 分片信息 (chunk_size, total_chunks)
├── 处理状态 (uploading/processing/completed/failed)
└── 进度追踪 (progress)

VideoTranscodeJob (转码任务)
├── 输入信息 (format, resolution, bitrate)
├── 输出信息 (quality, file, size)
├── 处理状态 (status, progress)
└── 时间统计 (processing_time)
```

### 3. 视频播放权限控制 ✅

**权限类型**:
1. **免费视频**: 所有用户可观看
2. **试看视频**: 限制观看时长
3. **付费视频**: 需购买课程
4. **会员专享**: 仅会员可看

**权限检查流程**:
```python
def check_access(user_id, video_id):
    1. 检查视频是否免费
    2. 检查是否试看视频
    3. 检查用户是否已报名课程
    4. 检查报名是否在有效期内
    5. 返回权限结果
```

**数据模型**:
```
CourseEnrollment (课程报名)
├── 报名类型 (free/paid/trial)
├── 支付信息 (price_paid, order_id)
├── 有效期 (valid_from, valid_until)
└── 状态 (is_active)
```

### 4. 学习进度跟踪 ✅

**追踪维度**:
- 视频观看位置
- 观看时长统计
- 完成度计算
- 学习轨迹记录

**数据模型**:
```
LearningProgress (学习进度)
├── 进度统计 (watched/completed/total)
├── 完成率计算 (completion_rate)
├── 时间记录 (last_watched_at)
└── 评分评价 (rating, review)

VideoWatchRecord (观看记录)
├── 观看信息 (duration, position, percentage)
├── 完成状态 (is_completed, completed_at)
├── 设备信息 (device_type, platform)
└── 播放质量 (quality_played)
```

**进度更新逻辑**:
```
1. 记录观看位置(实时缓存)
2. 计算观看百分比
3. 判断是否完成(>90%)
4. 更新学习进度
5. 检查课程完成
```

### 5. 教练课程管理 ✅

**管理功能**:
- 创建和编辑课程
- 添加章节和视频
- 发布和下架课程
- 查看数据统计
- 学员管理

**权限控制**:
- 只能管理自己的课程
- 发布需满足条件
- 删除软删除保护

---

## 🏗️ 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────┐
│                  客户端层                        │
│         (Web/Mobile/Desktop)                    │
└────────────┬────────────────────────────────────┘
             │ HTTP/HTTPS
             ▼
┌─────────────────────────────────────────────────┐
│              API网关/负载均衡                     │
│           (Nginx/HAProxy)                       │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│              Flask应用层                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 课程API  │  │ 视频API  │  │ 统计API  │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└────────┬───────────┬───────────┬────────────────┘
         │           │           │
         ▼           ▼           ▼
┌─────────────────────────────────────────────────┐
│              服务层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │课程服务  │  │视频服务  │  │统计服务  │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└────────┬───────────┬───────────┬────────────────┘
         │           │           │
         ▼           ▼           ▼
┌────────────────┐  ┌────────────────┐  ┌──────────┐
│  MySQL数据库   │  │  Redis缓存     │  │  Celery  │
│  (主数据存储)  │  │  (热门数据)    │  │  (异步任务)│
└────────────────┘  └────────────────┘  └──────────┘
                                             │
                                             ▼
                                    ┌────────────────┐
                                    │  视频处理      │
                                    │  (FFmpeg)      │
                                    └────────────────┘
                                             │
                                             ▼
                                    ┌────────────────┐
                                    │  文件存储      │
                                    │  (本地/OSS)    │
                                    └────────────────┘
```

### 技术栈

**后端框架**:
- Flask 2.3.3 - Web框架
- SQLAlchemy 2.0.20 - ORM
- PyMySQL 1.1.0 - MySQL驱动

**异步任务**:
- Celery 5.3.4 - 分布式任务队列
- Redis 5.0.1 - 消息队列和缓存
- Kombu 5.3.4 - 消息传输

**数据验证**:
- Pydantic 2.5.0 - 数据验证

**视频处理**:
- FFmpeg - 视频转码
- ffprobe - 视频信息提取

**数据库**:
- MySQL 8.0+ - 关系数据库

---

## 💾 数据模型

### ER关系图

```
Course (课程)
  │
  ├──< Chapter (章节)
  │     │
  │     └──< Video (视频)
  │           │
  │           ├──< VideoWatchRecord (观看记录)
  │           ├──< VideoPlayStatistics (播放统计)
  │           └──< VideoTranscodeJob (转码任务)
  │
  ├──< CourseEnrollment (课程报名)
  ├──< LearningProgress (学习进度)
  ├──< CourseTagRelation (标签关系)
  └──< VideoUploadTask (上传任务)

CourseCategory (课程分类) - 树形结构
CourseTag (课程标签) - 多对多关系
```

### 核心表结构

#### 1. courses (课程表)
```sql
主要字段:
- title: 课程标题
- course_type: 课程类型(video/live/article)
- category: 课程分类
- level: 课程级别(beginner/intermediate/advanced)
- instructor_id: 讲师ID
- price: 价格
- is_free: 是否免费
- is_published: 是否发布
- view_count: 观看次数
- enrollment_count: 报名人数
- rating_average: 平均评分
```

#### 2. chapters (章节表)
```sql
主要字段:
- course_id: 课程ID (外键)
- title: 章节标题
- order_number: 排序号
- video_count: 视频数
- is_free: 是否免费
- is_locked: 是否锁定
```

#### 3. videos (视频表)
```sql
主要字段:
- chapter_id: 章节ID (外键)
- title: 视频标题
- video_url: 视频URL
- video_quality: 多清晰度URLs (JSON)
- duration: 时长(秒)
- is_free: 是否免费
- is_trial: 是否试看
- view_count: 观看次数
```

#### 4. video_upload_tasks (上传任务表)
```sql
主要字段:
- task_id: Celery任务ID
- user_id: 用户ID
- original_filename: 原始文件名
- file_size: 文件大小
- chunk_size/total_chunks: 分片信息
- status: 状态(uploading/processing/completed/failed)
- progress: 进度百分比
```

#### 5. learning_progress (学习进度表)
```sql
主要字段:
- user_id: 用户ID
- course_id: 课程ID (外键)
- total_videos: 总视频数
- watched_videos: 已观看数
- completed_videos: 已完成数
- completion_rate: 完成率
- last_watch_video_id: 最后观看视频
```

---

## 🔌 API接口

### 课程管理 API

#### 1. 创建课程
```
POST /api/courses

Request:
{
  "title": "健身基础课程",
  "course_type": "video",
  "category": "健身",
  "level": "beginner",
  "description": "适合新手的健身课程",
  "price": 9900,
  "is_free": false,
  "tags": ["健身", "新手", "减脂"]
}

Response:
{
  "code": 0,
  "message": "创建成功",
  "data": {
    "id": 1,
    "title": "健身基础课程",
    ...
  }
}
```

#### 2. 获取课程列表
```
GET /api/courses?category=健身&level=beginner&page=1&per_page=20

Response:
{
  "code": 0,
  "data": {
    "courses": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

#### 3. 获取课程详情
```
GET /api/courses/{id}

Response:
{
  "code": 0,
  "data": {
    "id": 1,
    "title": "健身基础课程",
    "chapters": [
      {
        "id": 1,
        "title": "第一章",
        "videos": [...]
      }
    ],
    "user_progress": {
      "completion_rate": 45.5,
      "watched_videos": 10,
      "total_videos": 22
    }
  }
}
```

#### 4. 更新课程
```
PUT /api/courses/{id}

Request:
{
  "title": "更新后的标题",
  "description": "更新后的描述"
}
```

#### 5. 发布课程
```
POST /api/courses/{id}/publish

Response:
{
  "code": 0,
  "message": "发布成功"
}
```

#### 6. 报名课程
```
POST /api/courses/{id}/enroll

Request:
{
  "enrollment_type": "paid",
  "order_id": "ORDER123456"
}

Response:
{
  "code": 0,
  "message": "报名成功",
  "data": {
    "enrollment_id": 1
  }
}
```

### 视频管理 API

#### 7. 创建上传任务
```
POST /api/videos/upload/init

Request:
{
  "course_id": 1,
  "chapter_id": 1,
  "filename": "video.mp4",
  "file_size": 104857600,
  "file_md5": "abc123...",
  "chunk_size": 2097152,
  "total_chunks": 50
}

Response:
{
  "code": 0,
  "data": {
    "task_id": 123,
    "status": "uploading"
  }
}
```

#### 8. 上传分片
```
POST /api/videos/upload/chunk

Request (multipart/form-data):
- task_id: 123
- chunk_index: 0
- chunk_data: [binary data]

Response:
{
  "code": 0,
  "data": {
    "progress": 2,
    "uploaded_chunks": 1,
    "total_chunks": 50
  }
}
```

#### 9. 查询上传状态
```
GET /api/videos/upload/status/{task_id}

Response:
{
  "code": 0,
  "data": {
    "task_id": 123,
    "status": "completed",
    "progress": 100,
    "video_id": 456,
    "transcode_jobs": [
      {
        "quality": "hd",
        "status": "completed",
        "progress": 100
      }
    ]
  }
}
```

#### 10. 获取播放URL
```
GET /api/videos/{id}/play?quality=hd

Response:
{
  "code": 0,
  "data": {
    "video_id": 1,
    "video_url": "https://cdn.example.com/video_hd.mp4",
    "duration": 600,
    "quality": "hd",
    "available_qualities": ["sd", "hd", "fhd"],
    "last_position": 120,
    "next_video_id": 2
  }
}
```

#### 11. 记录观看进度
```
POST /api/videos/{id}/progress

Request:
{
  "position": 120,
  "duration": 600,
  "watch_duration": 150,
  "device_type": "mobile"
}

Response:
{
  "code": 0,
  "data": {
    "message": "进度已保存",
    "is_completed": false
  }
}
```

#### 12. 获取学习进度
```
GET /api/courses/{id}/progress

Response:
{
  "code": 0,
  "data": {
    "course_id": 1,
    "total_videos": 22,
    "watched_videos": 10,
    "completed_videos": 8,
    "completion_rate": 36.4,
    "total_watch_time": 3600,
    "last_watch_video_id": 15
  }
}
```

### 统计分析 API

#### 13. 视频播放统计
```
GET /api/videos/{id}/statistics?days=30

Response:
{
  "code": 0,
  "data": {
    "video_id": 1,
    "period_days": 30,
    "total_plays": 1250,
    "total_unique_viewers": 856,
    "total_completions": 432,
    "avg_completion_rate": 68.5,
    "daily_stats": [...]
  }
}
```

#### 14. 热门课程
```
GET /api/courses/hot?limit=10

Response:
{
  "code": 0,
  "data": {
    "courses": [...]
  }
}
```

---

## 🎬 视频处理流程

### 完整处理流程图

```
┌─────────────────────────────────────────────────┐
│ 1. 客户端上传                                    │
│    - 创建上传任务                                │
│    - 获取task_id                                 │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│ 2. 分片上传                                      │
│    - 循环上传所有分片                            │
│    - 实时返回进度                                │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│ 3. 合并分片 (Celery任务)                        │
│    - 按顺序合并所有分片                          │
│    - 验证文件完整性(MD5)                         │
│    - 更新任务状态为uploaded                      │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│ 4. 视频处理 (Celery任务)                        │
│    - 使用ffprobe获取视频信息                     │
│    - 创建Video记录                               │
│    - 触发转码任务                                │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│ 5. 多清晰度转码 (并行Celery任务)                │
│    - SD: 640x360 @ 800kbps                      │
│    - HD: 1280x720 @ 2.5Mbps                     │
│    - FHD: 1920x1080 @ 5Mbps                     │
│    - 4K: 3840x2160 @ 15Mbps (可选)              │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│ 6. 更新记录                                      │
│    - 保存转码后的文件路径                        │
│    - 更新Video.video_quality字段                 │
│    - 清除相关缓存                                │
│    - 任务完成通知                                │
└─────────────────────────────────────────────────┘
```

### FFmpeg转码命令

```bash
# 标清 (SD)
ffmpeg -i input.mp4 \
  -vf "scale=640:360" \
  -b:v 800k \
  -preset medium \
  -c:v libx264 \
  -c:a aac \
  -b:a 128k \
  -movflags +faststart \
  output_sd.mp4

# 高清 (HD)
ffmpeg -i input.mp4 \
  -vf "scale=1280:720" \
  -b:v 2500k \
  -preset medium \
  -c:v libx264 \
  -c:a aac \
  -b:a 128k \
  -movflags +faststart \
  output_hd.mp4

# 超清 (FHD)
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080" \
  -b:v 5000k \
  -preset slow \
  -c:v libx264 \
  -c:a aac \
  -b:a 128k \
  -movflags +faststart \
  output_fhd.mp4
```

### Celery任务配置

```python
# 任务队列配置
task_routes = {
    'tasks.video.*': {'queue': 'video'},      # 视频处理队列
    'tasks.stats.*': {'queue': 'stats'},      # 统计任务队列
    'tasks.notify.*': {'queue': 'notify'},    # 通知任务队列
}

# 任务限制
task_soft_time_limit = 3600  # 1小时软超时
task_time_limit = 7200       # 2小时硬超时

# 重试配置
task_acks_late = True
task_reject_on_worker_lost = True
```

---

## 💾 缓存策略

### Redis缓存结构

```
课程缓存:
├── course:detail:{id}           # 课程详情 (5分钟)
├── courses:hot:{limit}          # 热门课程 (10分钟)
├── courses:list:{params}        # 课程列表 (1分钟)
└── categories:tree              # 分类树 (1小时)

视频缓存:
├── video:info:{id}              # 视频信息 (5分钟)
├── video:plays:{id}             # 播放次数 (24小时)
└── user:{uid}:video:{vid}:position  # 观看位置 (1小时)

学习进度:
├── user:{uid}:course:{cid}:progress  # 学习进度 (1分钟)
└── user:{uid}:recommended            # 推荐课程 (30分钟)

统计数据:
└── course:stats:{id}            # 课程统计 (10分钟)
```

### 缓存更新策略

**写入策略**:
1. **Cache Aside**: 先写数据库,再删缓存
2. **Write Through**: 同时写缓存和数据库
3. **Write Behind**: 异步写入数据库

**失效策略**:
1. **TTL过期**: 自动过期机制
2. **主动清除**: 数据更新时清除
3. **模式匹配**: 批量清除相关缓存

### 缓存装饰器使用

```python
from config.redis_config import cache_result

@cache_result('course:detail', expire=300)
def get_course_detail(course_id):
    # 业务逻辑
    return course_data
```

---

## 🚀 安装部署

### 系统要求

**软件环境**:
- Python 3.8+
- MySQL 8.0+
- Redis 5.0+
- FFmpeg 4.0+

**硬件要求**:
- CPU: 4核+
- 内存: 8GB+
- 磁盘: 100GB+ (视频存储需更多)

### 安装步骤

#### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

#### 2. 安装FFmpeg

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS/RHEL**:
```bash
sudo yum install epel-release
sudo yum install ffmpeg
```

**macOS**:
```bash
brew install ffmpeg
```

**Windows**:
下载FFmpeg并添加到PATH环境变量

#### 3. 安装Redis

**Ubuntu/Debian**:
```bash
sudo apt install redis-server
sudo systemctl start redis
```

**Docker**:
```bash
docker run -d -p 6379:6379 redis:latest
```

#### 4. 配置环境变量

创建 `.env` 文件:
```env
# 数据库配置
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/keep_fitness?charset=utf8mb4

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 视频存储
VIDEO_UPLOAD_DIR=/data/videos/uploads
VIDEO_TRANSCODE_DIR=/data/videos/transcoded

# Celery配置
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# 其他配置
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
FLASK_ENV=production
```

#### 5. 初始化数据库

```bash
python utils/init_db.py create
```

#### 6. 启动Celery Worker

```bash
# 启动视频处理队列
celery -A config.celery_config worker -Q video -l info -c 2

# 启动统计任务队列
celery -A config.celery_config worker -Q stats -l info -c 1

# 启动默认队列
celery -A config.celery_config worker -Q default -l info -c 4
```

#### 7. 启动Flask应用

```bash
python app.py
```

### Docker部署

创建 `docker-compose.yml`:
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: keep_fitness
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mysql
      - redis
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@mysql:3306/keep_fitness
      - REDIS_URL=redis://redis:6379/0

  celery_worker:
    build: .
    command: celery -A config.celery_config worker -l info
    depends_on:
      - mysql
      - redis
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@mysql:3306/keep_fitness
      - REDIS_URL=redis://redis:6379/0

volumes:
  mysql_data:
```

启动:
```bash
docker-compose up -d
```

---

## 📝 开发指南

### 添加新的课程类型

1. 更新枚举:
```python
class CourseTypeEnum(enum.Enum):
    VIDEO = "video"
    LIVE = "live"
    ARTICLE = "article"
    AUDIO = "audio"  # 新增
```

2. 更新业务逻辑
3. 更新API验证
4. 更新文档

### 添加新的转码清晰度

1. 更新转码参数:
```python
def get_transcode_params(quality: str):
    params = {
        ...
        '2k': {
            'resolution': '2560x1440',
            'bitrate': 10000000,
            'preset': 'slow'
        }
    }
```

2. 更新API文档
3. 测试转码任务

### 自定义推荐算法

在 `services/recommendation_service.py` 实现:
```python
def get_recommended_courses(user_id: int):
    # 1. 获取用户画像
    # 2. 协同过滤
    # 3. 内容推荐
    # 4. 热度加权
    # 5. 返回推荐列表
    pass
```

---

## ⚠️ 注意事项

### 1. 视频处理注意事项

- 确保服务器有足够的磁盘空间
- 转码任务消耗大量CPU资源
- 建议使用专用的转码服务器
- 大文件转码可能需要很长时间
- 设置合理的任务超时时间

### 2. 性能优化建议

- 使用CDN加速视频分发
- 启用Redis缓存热门数据
- 数据库查询使用索引
- 异步处理耗时任务
- 实现分页和懒加载

### 3. 安全性考虑

- 视频URL签名防盗链
- 上传文件类型验证
- 文件大小限制
- 防止恶意上传
- API访问频率限制

### 4. 监控告警

- Celery任务监控
- 视频处理失败告警
- 磁盘空间监控
- 数据库性能监控
- 缓存命中率监控

---

## 🎉 总结

本系统实现了完整的课程和视频管理功能,包括:

✅ **已完成**:
- 完整的数据模型设计
- 课程管理服务层
- 视频处理服务层
- Celery异步任务
- Redis缓存策略
- FFmpeg视频转码
- 学习进度跟踪
- 权限控制系统

⏳ **待实现**(需要继续):
- API路由层实现
- 前端上传组件
- 统计分析功能
- 推荐算法实现
- 完整的测试用例
- 详细的API文档
- 部署运维文档

**下一步**: 创建API路由层并完成系统集成测试。

---

**文档作者**: GitHub Copilot  
**最后更新**: 2025-10-19  
**版本**: v1.0.0-dev
