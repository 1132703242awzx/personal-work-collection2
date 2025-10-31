"""
基础模型类
提供所有模型的公共字段和方法
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr
from config.database import Base


class BaseModel(Base):
    """所有模型的基类"""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, 
                       index=True, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                       nullable=False, comment='更新时间')
    is_deleted = Column(Boolean, default=False, nullable=False, 
                       index=True, comment='软删除标记')
    
    @declared_attr
    def __tablename__(cls):
        """自动生成表名：类名转下划线"""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    def to_dict(self):
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update(self, **kwargs):
        """批量更新字段"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def soft_delete(self):
        """软删除"""
        self.is_deleted = True
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
