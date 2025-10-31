"""
Celery配置
用于异步任务处理
"""
from celery import Celery
from kombu import Exchange, Queue
import os


# Celery应用配置
def make_celery(app_name='keep_fitness'):
    """创建Celery应用实例"""
    
    # Redis配置
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    celery = Celery(
        app_name,
        broker=redis_url,
        backend=redis_url
    )
    
    # Celery配置
    celery.conf.update(
        # 任务结果配置
        result_expires=3600,  # 结果过期时间(秒)
        result_backend=redis_url,
        
        # 任务序列化
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='Asia/Shanghai',
        enable_utc=True,
        
        # 任务路由
        task_routes={
            'tasks.video.*': {'queue': 'video'},
            'tasks.stats.*': {'queue': 'stats'},
            'tasks.notify.*': {'queue': 'notify'},
        },
        
        # 队列配置
        task_queues=(
            Queue('default', Exchange('default'), routing_key='default'),
            Queue('video', Exchange('video'), routing_key='video'),
            Queue('stats', Exchange('stats'), routing_key='stats'),
            Queue('notify', Exchange('notify'), routing_key='notify'),
        ),
        
        # Worker配置
        worker_prefetch_multiplier=4,
        worker_max_tasks_per_child=1000,
        
        # 任务限制
        task_soft_time_limit=3600,  # 软超时1小时
        task_time_limit=7200,  # 硬超时2小时
        
        # 重试配置
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        
        # 监控
        worker_send_task_events=True,
        task_send_sent_event=True,
    )
    
    return celery


# 创建Celery实例
celery_app = make_celery()


# 任务自动发现
celery_app.autodiscover_tasks(['tasks'])


if __name__ == '__main__':
    celery_app.start()
