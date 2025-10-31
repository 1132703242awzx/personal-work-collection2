"""
视频管理服务层
提供视频上传、播放、学习进度跟踪等功能
"""
from typing import Dict, List, Optional
from sqlalchemy import and_, func, desc
from datetime import datetime, timedelta
from config.database import db_session
from config.redis_config import cache
from models.course import Video, Chapter, Course
from models.course_extended import (
    VideoUploadTask, VideoTranscodeJob, VideoWatchRecord,
    LearningProgress, VideoPlayStatistics, VideoStatusEnum
)
from tasks.video_tasks import process_video_upload, merge_video_chunks
import os


class VideoService:
    """视频服务类"""
    
    @staticmethod
    def create_upload_task(user_id: int, data: Dict) -> Dict:
        """
        创建视频上传任务
        
        Args:
            user_id: 用户ID
            data: 上传任务数据
            
        Returns:
            任务信息
        """
        try:
            # 创建上传任务
            task = VideoUploadTask(
                user_id=user_id,
                course_id=data['course_id'],
                chapter_id=data['chapter_id'],
                original_filename=data['filename'],
                file_size=data.get('file_size'),
                file_md5=data.get('file_md5'),
                chunk_size=data.get('chunk_size'),
                total_chunks=data.get('total_chunks'),
                status=VideoStatusEnum.UPLOADING
            )
            
            db_session.add(task)
            db_session.commit()
            
            return {
                'task_id': task.id,
                'status': task.status.value,
                'message': '上传任务创建成功'
            }
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"创建上传任务失败: {str(e)}")
    
    @staticmethod
    def upload_chunk(task_id: int, chunk_index: int, chunk_data: bytes) -> Dict:
        """
        上传视频分片
        
        Args:
            task_id: 任务ID
            chunk_index: 分片索引
            chunk_data: 分片数据
            
        Returns:
            上传结果
        """
        try:
            task = db_session.query(VideoUploadTask).filter_by(id=task_id).first()
            
            if not task:
                raise Exception("上传任务不存在")
            
            # 保存分片
            chunk_dir = os.path.join('/tmp/chunks', str(task_id))
            os.makedirs(chunk_dir, exist_ok=True)
            
            chunk_file = os.path.join(chunk_dir, f"chunk_{chunk_index}")
            with open(chunk_file, 'wb') as f:
                f.write(chunk_data)
            
            # 更新进度
            task.uploaded_chunks += 1
            task.progress = int((task.uploaded_chunks / task.total_chunks) * 100)
            db_session.commit()
            
            # 检查是否所有分片都已上传
            if task.uploaded_chunks == task.total_chunks:
                # 触发合并任务
                merge_video_chunks.delay(task_id, chunk_dir)
            
            return {
                'task_id': task_id,
                'progress': task.progress,
                'uploaded_chunks': task.uploaded_chunks,
                'total_chunks': task.total_chunks
            }
            
        except Exception as e:
            raise Exception(f"上传分片失败: {str(e)}")
    
    @staticmethod
    def get_upload_task_status(task_id: int) -> Optional[Dict]:
        """
        获取上传任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态
        """
        task = db_session.query(VideoUploadTask).filter_by(id=task_id).first()
        
        if not task:
            return None
        
        result = {
            'task_id': task.id,
            'status': task.status.value,
            'progress': task.progress,
            'video_id': task.video_id,
            'error_message': task.error_message
        }
        
        # 如果已完成,获取转码任务状态
        if task.status == VideoStatusEnum.COMPLETED:
            transcode_jobs = db_session.query(VideoTranscodeJob).filter_by(
                upload_task_id=task_id
            ).all()
            
            result['transcode_jobs'] = [
                {
                    'quality': job.output_quality,
                    'status': job.status.value,
                    'progress': job.progress,
                    'output_file': job.output_file
                }
                for job in transcode_jobs
            ]
        
        return result
    
    @staticmethod
    def get_video_play_url(video_id: int, user_id: int, quality: str = 'hd') -> Optional[Dict]:
        """
        获取视频播放URL
        
        Args:
            video_id: 视频ID
            user_id: 用户ID
            quality: 清晰度
            
        Returns:
            播放信息
        """
        try:
            # 查询视频
            video = db_session.query(Video).options(
                joinedload(Video.chapter).joinedload(Chapter.course)
            ).filter_by(
                id=video_id,
                deleted_at=None
            ).first()
            
            if not video:
                return None
            
            course = video.chapter.course
            
            # 权限检查
            if not VideoService._check_video_access(user_id, video, course):
                raise Exception("无权限观看此视频")
            
            # 获取视频URL
            video_url = video.video_url
            if video.video_quality and quality in video.video_quality:
                video_url = video.video_quality[quality]['url']
            
            # 更新播放次数(异步)
            cache.incr_video_play_count(video_id)
            
            # 获取观看位置
            last_position = cache.get_user_watch_position(user_id, video_id)
            if not last_position:
                watch_record = db_session.query(VideoWatchRecord).filter_by(
                    user_id=user_id,
                    video_id=video_id
                ).first()
                if watch_record:
                    last_position = watch_record.last_position
            
            return {
                'video_id': video_id,
                'title': video.title,
                'video_url': video_url,
                'duration': video.duration,
                'quality': quality,
                'available_qualities': list(video.video_quality.keys()) if video.video_quality else ['hd'],
                'last_position': last_position,
                'subtitles': video.subtitles,
                'next_video_id': VideoService._get_next_video_id(video)
            }
            
        except Exception as e:
            raise Exception(f"获取播放URL失败: {str(e)}")
    
    @staticmethod
    def record_watch_progress(user_id: int, video_id: int, data: Dict) -> Dict:
        """
        记录观看进度
        
        Args:
            user_id: 用户ID
            video_id: 视频ID
            data: 进度数据 {position, duration, completed}
            
        Returns:
            记录结果
        """
        try:
            # 获取视频和课程信息
            video = db_session.query(Video).options(
                joinedload(Video.chapter).joinedload(Chapter.course)
            ).filter_by(id=video_id).first()
            
            if not video:
                raise Exception("视频不存在")
            
            course = video.chapter.course
            position = data['position']
            duration = data.get('duration', video.duration)
            
            # 计算观看百分比
            watch_percentage = (position / duration * 100) if duration > 0 else 0
            is_completed = watch_percentage >= 90  # 观看90%算完成
            
            # 更新或创建观看记录
            watch_record = db_session.query(VideoWatchRecord).filter_by(
                user_id=user_id,
                video_id=video_id
            ).first()
            
            if watch_record:
                watch_record.last_position = position
                watch_record.watch_percentage = watch_percentage
                watch_record.watch_duration = data.get('watch_duration', watch_record.watch_duration)
                
                if is_completed and not watch_record.is_completed:
                    watch_record.is_completed = True
                    watch_record.completed_at = datetime.utcnow()
                    
                    # 更新视频完成数
                    video.completion_count += 1
                
            else:
                watch_record = VideoWatchRecord(
                    user_id=user_id,
                    video_id=video_id,
                    course_id=course.id,
                    last_position=position,
                    watch_percentage=watch_percentage,
                    watch_duration=data.get('watch_duration', 0),
                    is_completed=is_completed,
                    completed_at=datetime.utcnow() if is_completed else None,
                    device_type=data.get('device_type'),
                    platform=data.get('platform')
                )
                db_session.add(watch_record)
                
                if is_completed:
                    video.completion_count += 1
            
            # 更新学习进度
            VideoService._update_learning_progress(
                user_id, course.id, video_id, is_completed
            )
            
            # 更新缓存
            cache.set_user_watch_position(user_id, video_id, position)
            
            db_session.commit()
            
            return {
                'message': '进度已保存',
                'position': position,
                'is_completed': is_completed
            }
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"记录进度失败: {str(e)}")
    
    @staticmethod
    def get_learning_progress(user_id: int, course_id: int) -> Optional[Dict]:
        """
        获取学习进度
        
        Args:
            user_id: 用户ID
            course_id: 课程ID
            
        Returns:
            学习进度
        """
        # 尝试从缓存获取
        cached = cache.get_user_progress(user_id, course_id)
        if cached:
            return cached
        
        progress = db_session.query(LearningProgress).filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
        
        if not progress:
            return None
        
        result = {
            'course_id': course_id,
            'total_videos': progress.total_videos,
            'watched_videos': progress.watched_videos,
            'completed_videos': progress.completed_videos,
            'completion_rate': progress.completion_rate,
            'total_watch_time': progress.total_watch_time,
            'last_watch_video_id': progress.last_watch_video_id,
            'last_watched_at': progress.last_watched_at.isoformat() if progress.last_watched_at else None,
            'is_completed': progress.is_completed
        }
        
        # 缓存结果
        cache.set_user_progress(user_id, course_id, result)
        
        return result
    
    @staticmethod
    def get_video_statistics(video_id: int, days: int = 30) -> Dict:
        """
        获取视频播放统计
        
        Args:
            video_id: 视频ID
            days: 统计天数
            
        Returns:
            统计数据
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        stats = db_session.query(VideoPlayStatistics).filter(
            and_(
                VideoPlayStatistics.video_id == video_id,
                VideoPlayStatistics.stat_date >= start_date
            )
        ).order_by(VideoPlayStatistics.stat_date).all()
        
        return {
            'video_id': video_id,
            'period_days': days,
            'total_plays': sum(s.play_count for s in stats),
            'total_unique_viewers': sum(s.unique_viewers for s in stats),
            'total_completions': sum(s.completion_count for s in stats),
            'avg_completion_rate': sum(s.completion_rate for s in stats) / len(stats) if stats else 0,
            'daily_stats': [
                {
                    'date': s.stat_date.strftime('%Y-%m-%d'),
                    'plays': s.play_count,
                    'unique_viewers': s.unique_viewers,
                    'completions': s.completion_count,
                    'completion_rate': s.completion_rate,
                    'avg_watch_time': s.avg_watch_time
                }
                for s in stats
            ]
        }
    
    # ========== 辅助方法 ==========
    
    @staticmethod
    def _check_video_access(user_id: int, video: Video, course: Course) -> bool:
        """检查用户是否有权限观看视频"""
        # 免费视频
        if video.is_free or course.is_free:
            return True
        
        # 试看视频
        if video.is_trial:
            return True
        
        # 检查是否已报名
        from models.course_extended import CourseEnrollment
        enrollment = db_session.query(CourseEnrollment).filter_by(
            user_id=user_id,
            course_id=course.id,
            is_active=True
        ).first()
        
        if not enrollment:
            return False
        
        # 检查有效期
        if not enrollment.is_lifetime:
            if enrollment.valid_until and enrollment.valid_until < datetime.utcnow():
                return False
        
        return True
    
    @staticmethod
    def _get_next_video_id(current_video: Video) -> Optional[int]:
        """获取下一个视频ID"""
        chapter = current_video.chapter
        
        # 同章节下一个视频
        next_video = db_session.query(Video).filter(
            and_(
                Video.chapter_id == chapter.id,
                Video.order_number > current_video.order_number,
                Video.deleted_at.is_(None)
            )
        ).order_by(Video.order_number).first()
        
        if next_video:
            return next_video.id
        
        # 下一章节第一个视频
        course = chapter.course
        next_chapter = db_session.query(Chapter).filter(
            and_(
                Chapter.course_id == course.id,
                Chapter.order_number > chapter.order_number,
                Chapter.deleted_at.is_(None)
            )
        ).order_by(Chapter.order_number).first()
        
        if next_chapter:
            first_video = db_session.query(Video).filter(
                and_(
                    Video.chapter_id == next_chapter.id,
                    Video.deleted_at.is_(None)
                )
            ).order_by(Video.order_number).first()
            
            return first_video.id if first_video else None
        
        return None
    
    @staticmethod
    def _update_learning_progress(user_id: int, course_id: int, 
                                  video_id: int, is_completed: bool):
        """更新学习进度"""
        progress = db_session.query(LearningProgress).filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
        
        if not progress:
            # 创建进度记录
            course = db_session.query(Course).filter_by(id=course_id).first()
            progress = LearningProgress(
                user_id=user_id,
                course_id=course_id,
                total_videos=course.video_count if course else 0
            )
            db_session.add(progress)
            db_session.flush()
        
        # 更新观看信息
        progress.last_watch_video_id = video_id
        progress.last_watched_at = datetime.utcnow()
        
        # 计算完成视频数
        if is_completed:
            completed_count = db_session.query(func.count(VideoWatchRecord.id)).filter(
                and_(
                    VideoWatchRecord.user_id == user_id,
                    VideoWatchRecord.course_id == course_id,
                    VideoWatchRecord.is_completed == True
                )
            ).scalar()
            
            progress.completed_videos = completed_count
            progress.completion_rate = (completed_count / progress.total_videos * 100) if progress.total_videos > 0 else 0
            
            # 检查是否完成课程
            if progress.completion_rate >= 100 and not progress.is_completed:
                progress.is_completed = True
                progress.completed_at = datetime.utcnow()
                
                # 更新课程完成数
                course = db_session.query(Course).filter_by(id=course_id).first()
                if course:
                    course.completion_count += 1
        
        # 清除缓存
        cache.delete_user_progress(user_id, course_id)
