"""
课程管理服务层
提供课程的CRUD和管理功能
"""
from typing import Dict, List, Optional
from sqlalchemy import and_, or_, func, desc
from sqlalchemy.orm import joinedload
from datetime import datetime
from config.database import db_session
from config.redis_config import cache
from models.course import Course, Chapter, Video, CourseTypeEnum, CourseLevelEnum
from models.course_extended import (
    CourseCategory, CourseTag, CourseTagRelation,
    CourseEnrollment, LearningProgress
)


class CourseService:
    """课程服务类"""
    
    @staticmethod
    def create_course(user_id: int, data: Dict) -> Dict:
        """
        创建课程
        
        Args:
            user_id: 教练ID
            data: 课程数据
            
        Returns:
            课程信息
        """
        try:
            # 创建课程
            course = Course(
                title=data['title'],
                subtitle=data.get('subtitle'),
                description=data.get('description'),
                cover_image=data.get('cover_image'),
                course_type=CourseTypeEnum[data['course_type'].upper()],
                category=data['category'],
                level=CourseLevelEnum[data['level'].upper()],
                instructor_id=user_id,
                instructor_name=data.get('instructor_name'),
                is_free=data.get('is_free', False),
                is_premium_only=data.get('is_premium_only', False),
                price=data.get('price', 0),
                original_price=data.get('original_price')
            )
            
            db_session.add(course)
            db_session.flush()
            
            # 添加标签
            if data.get('tags'):
                CourseService._add_tags_to_course(course.id, data['tags'])
            
            db_session.commit()
            
            # 清除缓存
            cache.delete_pattern('courses:*')
            
            return CourseService._course_to_dict(course)
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"创建课程失败: {str(e)}")
    
    @staticmethod
    def get_courses(filters: Dict = None) -> Dict:
        """
        获取课程列表
        
        Args:
            filters: 筛选条件
            
        Returns:
            课程列表和分页信息
        """
        filters = filters or {}
        
        # 构建查询
        query = db_session.query(Course).filter(
            Course.deleted_at.is_(None)
        )
        
        # 筛选条件
        if filters.get('category'):
            query = query.filter(Course.category == filters['category'])
        
        if filters.get('course_type'):
            query = query.filter(Course.course_type == filters['course_type'])
        
        if filters.get('level'):
            query = query.filter(Course.level == filters['level'])
        
        if filters.get('is_free') is not None:
            query = query.filter(Course.is_free == filters['is_free'])
        
        if filters.get('is_published') is not None:
            query = query.filter(Course.is_published == filters['is_published'])
        
        if filters.get('is_featured') is not None:
            query = query.filter(Course.is_featured == filters['is_featured'])
        
        if filters.get('instructor_id'):
            query = query.filter(Course.instructor_id == filters['instructor_id'])
        
        # 搜索
        if filters.get('keyword'):
            keyword = f"%{filters['keyword']}%"
            query = query.filter(
                or_(
                    Course.title.like(keyword),
                    Course.description.like(keyword),
                    Course.instructor_name.like(keyword)
                )
            )
        
        # 排序
        sort_by = filters.get('sort_by', 'created_at')
        if sort_by == 'popularity':
            query = query.order_by(desc(Course.popularity_score))
        elif sort_by == 'rating':
            query = query.order_by(desc(Course.rating_average))
        elif sort_by == 'newest':
            query = query.order_by(desc(Course.created_at))
        else:
            query = query.order_by(desc(Course.created_at))
        
        # 分页
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        
        total = query.count()
        courses = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'courses': [CourseService._course_to_dict(c, simple=True) for c in courses],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }
    
    @staticmethod
    def get_course_detail(course_id: int, user_id: int = None) -> Optional[Dict]:
        """
        获取课程详情
        
        Args:
            course_id: 课程ID
            user_id: 用户ID(可选)
            
        Returns:
            课程详情
        """
        # 尝试从缓存获取
        cached = cache.get_course(course_id)
        if cached and not user_id:
            return cached
        
        # 查询课程
        course = db_session.query(Course).options(
            joinedload(Course.chapters).joinedload(Chapter.videos)
        ).filter_by(
            id=course_id,
            deleted_at=None
        ).first()
        
        if not course:
            return None
        
        # 构建详情
        detail = CourseService._course_to_dict(course, detail=True)
        
        # 获取用户学习进度
        if user_id:
            progress = db_session.query(LearningProgress).filter_by(
                user_id=user_id,
                course_id=course_id
            ).first()
            
            if progress:
                detail['user_progress'] = {
                    'completion_rate': progress.completion_rate,
                    'watched_videos': progress.watched_videos,
                    'total_videos': progress.total_videos,
                    'last_watch_video_id': progress.last_watch_video_id,
                    'last_watched_at': progress.last_watched_at.isoformat() if progress.last_watched_at else None
                }
        
        # 缓存结果(不包含用户进度)
        if not user_id:
            cache.set_course(course_id, detail)
        
        return detail
    
    @staticmethod
    def update_course(course_id: int, user_id: int, data: Dict) -> Optional[Dict]:
        """
        更新课程
        
        Args:
            course_id: 课程ID
            user_id: 教练ID
            data: 更新数据
            
        Returns:
            更新后的课程信息
        """
        try:
            course = db_session.query(Course).filter_by(
                id=course_id,
                instructor_id=user_id,
                deleted_at=None
            ).first()
            
            if not course:
                return None
            
            # 更新字段
            for key, value in data.items():
                if hasattr(course, key) and key not in ['id', 'instructor_id', 'created_at']:
                    if key == 'course_type':
                        setattr(course, key, CourseTypeEnum[value.upper()])
                    elif key == 'level':
                        setattr(course, key, CourseLevelEnum[value.upper()])
                    else:
                        setattr(course, key, value)
            
            course.updated_at = datetime.utcnow()
            
            # 更新标签
            if 'tags' in data:
                # 删除旧标签关系
                db_session.query(CourseTagRelation).filter_by(
                    course_id=course_id
                ).delete()
                # 添加新标签
                CourseService._add_tags_to_course(course_id, data['tags'])
            
            db_session.commit()
            
            # 清除缓存
            cache.delete_course(course_id)
            cache.delete_pattern('courses:*')
            
            return CourseService._course_to_dict(course)
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"更新课程失败: {str(e)}")
    
    @staticmethod
    def delete_course(course_id: int, user_id: int) -> bool:
        """
        删除课程(软删除)
        
        Args:
            course_id: 课程ID
            user_id: 教练ID
            
        Returns:
            是否成功
        """
        try:
            course = db_session.query(Course).filter_by(
                id=course_id,
                instructor_id=user_id,
                deleted_at=None
            ).first()
            
            if not course:
                return False
            
            course.deleted_at = datetime.utcnow()
            db_session.commit()
            
            # 清除缓存
            cache.delete_course(course_id)
            cache.delete_pattern('courses:*')
            
            return True
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"删除课程失败: {str(e)}")
    
    @staticmethod
    def publish_course(course_id: int, user_id: int) -> Optional[Dict]:
        """
        发布课程
        
        Args:
            course_id: 课程ID
            user_id: 教练ID
            
        Returns:
            课程信息
        """
        try:
            course = db_session.query(Course).filter_by(
                id=course_id,
                instructor_id=user_id,
                deleted_at=None
            ).first()
            
            if not course:
                return None
            
            # 检查是否可以发布
            if course.chapter_count == 0 or course.video_count == 0:
                raise Exception("课程必须包含章节和视频才能发布")
            
            course.is_published = True
            course.updated_at = datetime.utcnow()
            db_session.commit()
            
            # 清除缓存
            cache.delete_course(course_id)
            cache.delete_pattern('courses:*')
            
            return CourseService._course_to_dict(course)
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"发布课程失败: {str(e)}")
    
    @staticmethod
    def get_hot_courses(limit: int = 10) -> List[Dict]:
        """
        获取热门课程
        
        Args:
            limit: 数量限制
            
        Returns:
            热门课程列表
        """
        # 尝试从缓存获取
        cached = cache.get_hot_courses(limit)
        if cached:
            return cached
        
        # 查询热门课程
        courses = db_session.query(Course).filter(
            and_(
                Course.is_published == True,
                Course.deleted_at.is_(None)
            )
        ).order_by(
            desc(Course.popularity_score)
        ).limit(limit).all()
        
        result = [CourseService._course_to_dict(c, simple=True) for c in courses]
        
        # 缓存结果
        cache.set_hot_courses(result, limit)
        
        return result
    
    @staticmethod
    def enroll_course(user_id: int, course_id: int, enrollment_type: str = 'free') -> Dict:
        """
        报名课程
        
        Args:
            user_id: 用户ID
            course_id: 课程ID
            enrollment_type: 报名类型
            
        Returns:
            报名信息
        """
        try:
            # 检查是否已报名
            existing = db_session.query(CourseEnrollment).filter_by(
                user_id=user_id,
                course_id=course_id,
                is_active=True
            ).first()
            
            if existing:
                return {'message': '已经报名过此课程', 'enrollment': existing}
            
            # 创建报名记录
            enrollment = CourseEnrollment(
                user_id=user_id,
                course_id=course_id,
                enrollment_type=enrollment_type,
                valid_from=datetime.utcnow(),
                is_active=True,
                is_lifetime=True if enrollment_type == 'free' else False
            )
            db_session.add(enrollment)
            
            # 更新课程报名数
            course = db_session.query(Course).filter_by(id=course_id).first()
            if course:
                course.enrollment_count += 1
            
            # 创建学习进度记录
            progress = LearningProgress(
                user_id=user_id,
                course_id=course_id,
                total_videos=course.video_count if course else 0,
                is_enrolled=True
            )
            db_session.add(progress)
            
            db_session.commit()
            
            # 清除缓存
            cache.delete_course(course_id)
            cache.delete_user_progress(user_id, course_id)
            
            return {
                'message': '报名成功',
                'enrollment_id': enrollment.id
            }
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"报名失败: {str(e)}")
    
    # ========== 辅助方法 ==========
    
    @staticmethod
    def _course_to_dict(course: Course, simple: bool = False, detail: bool = False) -> Dict:
        """将课程对象转换为字典"""
        base_data = {
            'id': course.id,
            'title': course.title,
            'subtitle': course.subtitle,
            'cover_image': course.cover_image,
            'course_type': course.course_type.value,
            'category': course.category,
            'level': course.level.value,
            'instructor_name': course.instructor_name,
            'instructor_avatar': course.instructor_avatar,
            'chapter_count': course.chapter_count,
            'video_count': course.video_count,
            'total_duration': course.total_duration,
            'price': course.price,
            'is_free': course.is_free,
            'is_premium_only': course.is_premium_only,
            'is_published': course.is_published,
            'is_featured': course.is_featured,
            'view_count': course.view_count,
            'enrollment_count': course.enrollment_count,
            'rating_average': course.rating_average,
            'rating_count': course.rating_count,
            'created_at': course.created_at.isoformat() if course.created_at else None
        }
        
        if simple:
            return base_data
        
        if detail:
            base_data.update({
                'description': course.description,
                'promo_video': course.promo_video,
                'tags': course.tags,
                'target_audience': course.target_audience,
                'learning_objectives': course.learning_objectives,
                'instructor_bio': course.instructor_bio,
                'chapters': [
                    {
                        'id': ch.id,
                        'title': ch.title,
                        'description': ch.description,
                        'order_number': ch.order_number,
                        'video_count': ch.video_count,
                        'total_duration': ch.total_duration,
                        'is_free': ch.is_free,
                        'is_locked': ch.is_locked,
                        'videos': [
                            {
                                'id': v.id,
                                'title': v.title,
                                'cover_image': v.cover_image,
                                'duration': v.duration,
                                'order_number': v.order_number,
                                'is_free': v.is_free,
                                'is_trial': v.is_trial
                            }
                            for v in ch.videos
                        ]
                    }
                    for ch in course.chapters
                ]
            })
        
        return base_data
    
    @staticmethod
    def _add_tags_to_course(course_id: int, tag_names: List[str]):
        """为课程添加标签"""
        for tag_name in tag_names:
            # 获取或创建标签
            tag = db_session.query(CourseTag).filter_by(name=tag_name).first()
            if not tag:
                tag = CourseTag(name=tag_name)
                db_session.add(tag)
                db_session.flush()
            
            # 创建关系
            relation = CourseTagRelation(course_id=course_id, tag_id=tag.id)
            db_session.add(relation)
