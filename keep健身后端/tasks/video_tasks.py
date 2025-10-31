"""
视频处理Celery任务
包含视频上传、转码、处理等异步任务
"""
from celery import Task
from config.celery_config import celery_app
from config.database import db_session
from config.redis_config import cache
from models.course_extended import VideoUploadTask, VideoTranscodeJob, VideoStatusEnum
from models.course import Video
from datetime import datetime
import os
import subprocess
import hashlib
import json


class CallbackTask(Task):
    """带回调的任务基类"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """任务成功回调"""
        print(f"Task {task_id} succeeded")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """任务失败回调"""
        print(f"Task {task_id} failed: {exc}")


@celery_app.task(base=CallbackTask, bind=True, max_retries=3)
def process_video_upload(self, upload_task_id: int):
    """
    处理视频上传任务
    
    Args:
        upload_task_id: 上传任务ID
    """
    try:
        # 获取上传任务
        upload_task = db_session.query(VideoUploadTask).filter_by(
            id=upload_task_id
        ).first()
        
        if not upload_task:
            raise Exception(f"Upload task {upload_task_id} not found")
        
        # 更新任务状态
        upload_task.status = VideoStatusEnum.PROCESSING
        upload_task.task_id = self.request.id
        db_session.commit()
        
        # 验证文件
        if not os.path.exists(upload_task.file_path):
            raise Exception(f"File not found: {upload_task.file_path}")
        
        # 计算文件MD5
        file_md5 = calculate_file_md5(upload_task.file_path)
        if upload_task.file_md5 and file_md5 != upload_task.file_md5:
            raise Exception("File MD5 mismatch")
        
        upload_task.file_md5 = file_md5
        
        # 获取视频信息
        video_info = get_video_info(upload_task.file_path)
        
        # 创建视频记录(如果不存在)
        if not upload_task.video_id:
            video = Video(
                chapter_id=upload_task.chapter_id,
                title=upload_task.original_filename,
                video_url=upload_task.file_path,
                duration=video_info['duration'],
                file_size=upload_task.file_size,
                order_number=1,
                is_published=False
            )
            db_session.add(video)
            db_session.flush()
            
            upload_task.video_id = video.id
        
        # 更新状态为已上传
        upload_task.status = VideoStatusEnum.UPLOADED
        upload_task.progress = 100
        db_session.commit()
        
        # 触发转码任务
        transcode_qualities = ['sd', 'hd', 'fhd']
        for quality in transcode_qualities:
            transcode_video.delay(upload_task_id, quality)
        
        return {
            'status': 'success',
            'upload_task_id': upload_task_id,
            'video_id': upload_task.video_id
        }
        
    except Exception as e:
        # 更新失败状态
        if upload_task:
            upload_task.status = VideoStatusEnum.FAILED
            upload_task.error_message = str(e)
            db_session.commit()
        
        # 重试任务
        raise self.retry(exc=e, countdown=60)


@celery_app.task(base=CallbackTask, bind=True, max_retries=2)
def transcode_video(self, upload_task_id: int, quality: str):
    """
    视频转码任务
    
    Args:
        upload_task_id: 上传任务ID
        quality: 输出清晰度(sd/hd/fhd/4k)
    """
    try:
        # 获取上传任务
        upload_task = db_session.query(VideoUploadTask).filter_by(
            id=upload_task_id
        ).first()
        
        if not upload_task:
            raise Exception(f"Upload task {upload_task_id} not found")
        
        # 创建转码任务记录
        transcode_job = VideoTranscodeJob(
            task_id=self.request.id,
            upload_task_id=upload_task_id,
            video_id=upload_task.video_id,
            input_file=upload_task.file_path,
            output_quality=quality,
            status=VideoStatusEnum.PROCESSING,
            started_at=datetime.utcnow()
        )
        db_session.add(transcode_job)
        db_session.commit()
        
        # 获取输入视频信息
        input_info = get_video_info(upload_task.file_path)
        transcode_job.input_format = input_info.get('format')
        transcode_job.input_duration = input_info.get('duration')
        transcode_job.input_resolution = input_info.get('resolution')
        transcode_job.input_bitrate = input_info.get('bitrate')
        
        # 设置输出参数
        output_params = get_transcode_params(quality)
        transcode_job.output_resolution = output_params['resolution']
        transcode_job.output_bitrate = output_params['bitrate']
        
        # 构建输出文件路径
        input_dir = os.path.dirname(upload_task.file_path)
        input_name = os.path.splitext(os.path.basename(upload_task.file_path))[0]
        output_file = os.path.join(input_dir, f"{input_name}_{quality}.mp4")
        transcode_job.output_file = output_file
        
        db_session.commit()
        
        # 执行转码
        result = ffmpeg_transcode(
            input_file=upload_task.file_path,
            output_file=output_file,
            params=output_params,
            progress_callback=lambda p: update_transcode_progress(transcode_job.id, p)
        )
        
        if result['success']:
            # 更新转码任务
            transcode_job.status = VideoStatusEnum.COMPLETED
            transcode_job.progress = 100
            transcode_job.output_size = os.path.getsize(output_file)
            transcode_job.completed_at = datetime.utcnow()
            transcode_job.processing_time = (
                transcode_job.completed_at - transcode_job.started_at
            ).seconds
            
            # 更新视频记录
            video = db_session.query(Video).filter_by(id=upload_task.video_id).first()
            if video:
                if not video.video_quality:
                    video.video_quality = {}
                video.video_quality[quality] = {
                    'url': output_file,
                    'resolution': output_params['resolution'],
                    'bitrate': output_params['bitrate'],
                    'size': transcode_job.output_size
                }
            
            db_session.commit()
            
            # 清除缓存
            cache.delete(f"video:info:{upload_task.video_id}")
            
            return {
                'status': 'success',
                'transcode_job_id': transcode_job.id,
                'output_file': output_file
            }
        else:
            raise Exception(result.get('error', 'Transcode failed'))
        
    except Exception as e:
        # 更新失败状态
        if transcode_job:
            transcode_job.status = VideoStatusEnum.FAILED
            transcode_job.error_message = str(e)
            transcode_job.completed_at = datetime.utcnow()
            db_session.commit()
        
        # 重试
        raise self.retry(exc=e, countdown=120)


@celery_app.task
def merge_video_chunks(upload_task_id: int, chunk_dir: str):
    """
    合并视频分片
    
    Args:
        upload_task_id: 上传任务ID
        chunk_dir: 分片目录
    """
    try:
        upload_task = db_session.query(VideoUploadTask).filter_by(
            id=upload_task_id
        ).first()
        
        if not upload_task:
            raise Exception(f"Upload task {upload_task_id} not found")
        
        # 获取所有分片文件
        chunk_files = []
        for i in range(upload_task.total_chunks):
            chunk_file = os.path.join(chunk_dir, f"chunk_{i}")
            if not os.path.exists(chunk_file):
                raise Exception(f"Chunk {i} not found")
            chunk_files.append(chunk_file)
        
        # 合并文件
        output_dir = os.getenv('VIDEO_UPLOAD_DIR', '/tmp/videos')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(
            output_dir,
            f"{upload_task.id}_{upload_task.original_filename}"
        )
        
        with open(output_file, 'wb') as outfile:
            for chunk_file in chunk_files:
                with open(chunk_file, 'rb') as infile:
                    outfile.write(infile.read())
        
        # 更新任务
        upload_task.file_path = output_file
        upload_task.file_size = os.path.getsize(output_file)
        upload_task.status = VideoStatusEnum.UPLOADED
        upload_task.progress = 100
        db_session.commit()
        
        # 清理分片文件
        for chunk_file in chunk_files:
            os.remove(chunk_file)
        
        # 触发处理任务
        process_video_upload.delay(upload_task_id)
        
        return {
            'status': 'success',
            'output_file': output_file
        }
        
    except Exception as e:
        if upload_task:
            upload_task.status = VideoStatusEnum.FAILED
            upload_task.error_message = str(e)
            db_session.commit()
        raise


# ========== 辅助函数 ==========

def calculate_file_md5(file_path: str) -> str:
    """计算文件MD5"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()


def get_video_info(file_path: str) -> dict:
    """
    获取视频信息
    
    使用ffprobe获取视频元数据
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # 提取视频流信息
        video_stream = next(
            (s for s in data['streams'] if s['codec_type'] == 'video'),
            None
        )
        
        if not video_stream:
            raise Exception("No video stream found")
        
        return {
            'format': data['format']['format_name'],
            'duration': int(float(data['format']['duration'])),
            'bitrate': int(data['format'].get('bit_rate', 0)),
            'resolution': f"{video_stream['width']}x{video_stream['height']}",
            'codec': video_stream['codec_name'],
            'fps': eval(video_stream.get('r_frame_rate', '0/1'))
        }
        
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {
            'format': 'unknown',
            'duration': 0,
            'bitrate': 0,
            'resolution': '0x0'
        }


def get_transcode_params(quality: str) -> dict:
    """获取转码参数"""
    params = {
        'sd': {
            'resolution': '640x360',
            'bitrate': 800000,  # 800kbps
            'preset': 'medium'
        },
        'hd': {
            'resolution': '1280x720',
            'bitrate': 2500000,  # 2.5Mbps
            'preset': 'medium'
        },
        'fhd': {
            'resolution': '1920x1080',
            'bitrate': 5000000,  # 5Mbps
            'preset': 'slow'
        },
        '4k': {
            'resolution': '3840x2160',
            'bitrate': 15000000,  # 15Mbps
            'preset': 'slow'
        }
    }
    return params.get(quality, params['hd'])


def ffmpeg_transcode(input_file: str, output_file: str, params: dict, 
                     progress_callback=None) -> dict:
    """
    使用ffmpeg进行视频转码
    
    Args:
        input_file: 输入文件
        output_file: 输出文件
        params: 转码参数
        progress_callback: 进度回调函数
    """
    try:
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f"scale={params['resolution']}",
            '-b:v', str(params['bitrate']),
            '-preset', params['preset'],
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-y',  # 覆盖输出文件
            output_file
        ]
        
        # 执行转码
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 监控进度
        while True:
            line = process.stderr.readline()
            if not line:
                break
            
            # 解析进度
            if 'time=' in line and progress_callback:
                # 这里可以解析ffmpeg输出的时间进度
                # 调用progress_callback更新进度
                pass
        
        process.wait()
        
        if process.returncode == 0:
            return {'success': True}
        else:
            return {
                'success': False,
                'error': f"ffmpeg exited with code {process.returncode}"
            }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def update_transcode_progress(job_id: int, progress: int):
    """更新转码进度"""
    try:
        job = db_session.query(VideoTranscodeJob).filter_by(id=job_id).first()
        if job:
            job.progress = progress
            db_session.commit()
    except Exception as e:
        print(f"Error updating progress: {e}")
