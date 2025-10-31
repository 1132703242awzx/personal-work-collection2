"""
Redis缓存配置
用于缓存热门课程和播放数据
"""
import redis
import json
import os
from functools import wraps
from typing import Any, Callable


class RedisCache:
    """Redis缓存类"""
    
    def __init__(self):
        """初始化Redis连接"""
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.redis_client = redis.from_url(
            redis_url,
            decode_responses=True,
            max_connections=50
        )
        
        # 缓存过期时间配置(秒)
        self.CACHE_TIMES = {
            'course_detail': 300,  # 5分钟
            'course_list': 60,  # 1分钟
            'hot_courses': 600,  # 10分钟
            'video_info': 300,  # 5分钟
            'category_tree': 3600,  # 1小时
            'user_progress': 60,  # 1分钟
            'statistics': 600,  # 10分钟
        }
    
    def get(self, key: str) -> Any:
        """获取缓存"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: Any, expire: int = None):
        """设置缓存"""
        try:
            serialized = json.dumps(value, ensure_ascii=False, default=str)
            if expire:
                self.redis_client.setex(key, expire, serialized)
            else:
                self.redis_client.set(key, serialized)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str):
        """删除缓存"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def delete_pattern(self, pattern: str):
        """批量删除匹配的key"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            print(f"Redis delete pattern error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查key是否存在"""
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False
    
    def incr(self, key: str, amount: int = 1) -> int:
        """递增计数器"""
        try:
            return self.redis_client.incr(key, amount)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return 0
    
    def expire(self, key: str, seconds: int):
        """设置过期时间"""
        try:
            self.redis_client.expire(key, seconds)
            return True
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False
    
    # ========== 课程缓存方法 ==========
    
    def get_course(self, course_id: int):
        """获取课程缓存"""
        key = f"course:detail:{course_id}"
        return self.get(key)
    
    def set_course(self, course_id: int, course_data: dict):
        """设置课程缓存"""
        key = f"course:detail:{course_id}"
        expire = self.CACHE_TIMES['course_detail']
        return self.set(key, course_data, expire)
    
    def delete_course(self, course_id: int):
        """删除课程缓存"""
        key = f"course:detail:{course_id}"
        return self.delete(key)
    
    def get_hot_courses(self, limit: int = 10):
        """获取热门课程缓存"""
        key = f"courses:hot:{limit}"
        return self.get(key)
    
    def set_hot_courses(self, courses: list, limit: int = 10):
        """设置热门课程缓存"""
        key = f"courses:hot:{limit}"
        expire = self.CACHE_TIMES['hot_courses']
        return self.set(key, courses, expire)
    
    def get_category_tree(self):
        """获取分类树缓存"""
        key = "categories:tree"
        return self.get(key)
    
    def set_category_tree(self, tree: list):
        """设置分类树缓存"""
        key = "categories:tree"
        expire = self.CACHE_TIMES['category_tree']
        return self.set(key, tree, expire)
    
    # ========== 视频播放缓存 ==========
    
    def get_video_play_count(self, video_id: int) -> int:
        """获取视频播放次数"""
        key = f"video:plays:{video_id}"
        count = self.redis_client.get(key)
        return int(count) if count else 0
    
    def incr_video_play_count(self, video_id: int):
        """增加视频播放次数"""
        key = f"video:plays:{video_id}"
        count = self.incr(key)
        # 设置24小时过期
        if count == 1:
            self.expire(key, 86400)
        return count
    
    def get_user_watch_position(self, user_id: int, video_id: int) -> int:
        """获取用户观看位置"""
        key = f"user:{user_id}:video:{video_id}:position"
        position = self.redis_client.get(key)
        return int(position) if position else 0
    
    def set_user_watch_position(self, user_id: int, video_id: int, position: int):
        """设置用户观看位置"""
        key = f"user:{user_id}:video:{video_id}:position"
        self.redis_client.setex(key, 3600, position)  # 1小时过期
        return True
    
    # ========== 学习进度缓存 ==========
    
    def get_user_progress(self, user_id: int, course_id: int):
        """获取用户学习进度"""
        key = f"user:{user_id}:course:{course_id}:progress"
        return self.get(key)
    
    def set_user_progress(self, user_id: int, course_id: int, progress: dict):
        """设置用户学习进度"""
        key = f"user:{user_id}:course:{course_id}:progress"
        expire = self.CACHE_TIMES['user_progress']
        return self.set(key, progress, expire)
    
    def delete_user_progress(self, user_id: int, course_id: int):
        """删除用户学习进度缓存"""
        key = f"user:{user_id}:course:{course_id}:progress"
        return self.delete(key)
    
    # ========== 统计缓存 ==========
    
    def get_course_stats(self, course_id: int):
        """获取课程统计"""
        key = f"course:stats:{course_id}"
        return self.get(key)
    
    def set_course_stats(self, course_id: int, stats: dict):
        """设置课程统计"""
        key = f"course:stats:{course_id}"
        expire = self.CACHE_TIMES['statistics']
        return self.set(key, stats, expire)
    
    # ========== 推荐缓存 ==========
    
    def get_recommended_courses(self, user_id: int):
        """获取推荐课程"""
        key = f"user:{user_id}:recommended"
        return self.get(key)
    
    def set_recommended_courses(self, user_id: int, courses: list):
        """设置推荐课程"""
        key = f"user:{user_id}:recommended"
        self.set(key, courses, 1800)  # 30分钟
        return True


# 创建全局缓存实例
cache = RedisCache()


# ========== 缓存装饰器 ==========

def cache_result(key_prefix: str, expire: int = 300):
    """
    缓存装饰器
    
    Args:
        key_prefix: 缓存key前缀
        expire: 过期时间(秒)
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 构建缓存key
            cache_key = f"{key_prefix}:{':'.join(map(str, args))}"
            
            # 尝试从缓存获取
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 缓存结果
            if result is not None:
                cache.set(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator
