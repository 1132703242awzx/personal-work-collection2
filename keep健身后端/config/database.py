"""
数据库配置模块
提供数据库连接、会话管理和基础配置
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import os

# 数据库配置
class DatabaseConfig:
    """数据库配置类"""
    
    # 开发环境配置
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:123456@localhost:3306/keep_fitness?charset=utf8mb4'
    )
    
    # 连接池配置
    SQLALCHEMY_POOL_SIZE = 10  # 连接池大小
    SQLALCHEMY_POOL_RECYCLE = 3600  # 连接回收时间（秒）
    SQLALCHEMY_POOL_TIMEOUT = 30  # 连接超时时间（秒）
    SQLALCHEMY_MAX_OVERFLOW = 20  # 超过连接池大小外最多创建的连接
    
    # 其他配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 生产环境设为 False
    SQLALCHEMY_RECORD_QUERIES = True


# 创建数据库引擎
engine = create_engine(
    DatabaseConfig.SQLALCHEMY_DATABASE_URI,
    poolclass=QueuePool,
    pool_size=DatabaseConfig.SQLALCHEMY_POOL_SIZE,
    pool_recycle=DatabaseConfig.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=DatabaseConfig.SQLALCHEMY_POOL_TIMEOUT,
    max_overflow=DatabaseConfig.SQLALCHEMY_MAX_OVERFLOW,
    echo=DatabaseConfig.SQLALCHEMY_ECHO,
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建线程安全的会话
db_session = scoped_session(SessionLocal)

# 创建基类
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """初始化数据库，创建所有表"""
    import models  # 导入所有模型
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话的依赖注入函数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def shutdown_session(exception=None):
    """关闭数据库会话"""
    db_session.remove()
