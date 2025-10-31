"""
分页工具
"""
from typing import List, TypeVar, Generic
from sqlalchemy.orm import Query
from math import ceil

T = TypeVar('T')


class Pagination(Generic[T]):
    """分页结果类"""
    
    def __init__(self, items: List[T], page: int, page_size: int, total: int):
        self.items = items
        self.page = page
        self.page_size = page_size
        self.total = total
        self.pages = ceil(total / page_size) if page_size > 0 else 0
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_page = page - 1 if self.has_prev else None
        self.next_page = page + 1 if self.has_next else None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'items': [item.to_dict() if hasattr(item, 'to_dict') else item 
                     for item in self.items],
            'pagination': {
                'page': self.page,
                'page_size': self.page_size,
                'total': self.total,
                'pages': self.pages,
                'has_prev': self.has_prev,
                'has_next': self.has_next,
                'prev_page': self.prev_page,
                'next_page': self.next_page
            }
        }


def paginate(query: Query, page: int = 1, page_size: int = 20) -> Pagination:
    """
    分页查询
    
    Args:
        query: SQLAlchemy查询对象
        page: 页码（从1开始）
        page_size: 每页数量
    
    Returns:
        Pagination: 分页结果对象
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20
    if page_size > 100:
        page_size = 100
    
    total = query.count()
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    
    return Pagination(items=items, page=page, page_size=page_size, total=total)
