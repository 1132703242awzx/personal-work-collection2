"""
认证服务层
处理用户注册、登录、令牌管理等业务逻辑
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import jwt
import secrets
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

from models import (
    User, UserProfile, UserSettings, UserRole, 
    RefreshToken, PasswordResetToken, LoginHistory,
    SecurityLog, ThirdPartyAccount, UserRoleEnum
)
from config.database import db_session
from config.config import Config
from utils.validators import Validator


class AuthService:
    """认证服务类"""
    
    @staticmethod
    def register_user(
        username: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password: str = None,
        **kwargs
    ) -> Tuple[bool, str, Optional[User]]:
        """
        用户注册
        
        Args:
            username: 用户名
            email: 邮箱
            phone: 手机号
            password: 密码
            **kwargs: 其他用户信息
        
        Returns:
            (成功标志, 消息, 用户对象)
        """
        try:
            # 验证输入
            if not username:
                return False, "用户名不能为空", None
            
            if not Validator.validate_username(username):
                return False, "用户名格式不正确（4-20位字母数字下划线）", None
            
            if email and not Validator.validate_email(email):
                return False, "邮箱格式不正确", None
            
            if phone and not Validator.validate_phone(phone):
                return False, "手机号格式不正确", None
            
            if not email and not phone:
                return False, "邮箱或手机号至少提供一个", None
            
            if password and not Validator.validate_password(password):
                return False, "密码强度不够（至少8位，包含大小写字母和数字）", None
            
            # 检查用户名是否已存在
            if User.query.filter_by(username=username, is_deleted=False).first():
                return False, "用户名已被使用", None
            
            # 检查邮箱是否已存在
            if email and User.query.filter_by(email=email, is_deleted=False).first():
                return False, "邮箱已被注册", None
            
            # 检查手机号是否已存在
            if phone and User.query.filter_by(phone=phone, is_deleted=False).first():
                return False, "手机号已被注册", None
            
            # 创建用户
            user = User(
                username=username,
                email=email,
                phone=phone,
                password_hash=generate_password_hash(password) if password else None,
                status='active',
                is_verified=False
            )
            db_session.add(user)
            db_session.flush()  # 获取user.id
            
            # 创建用户资料
            profile = UserProfile(
                user_id=user.id,
                nickname=kwargs.get('nickname', username)
            )
            db_session.add(profile)
            
            # 创建用户设置
            settings = UserSettings(user_id=user.id)
            db_session.add(settings)
            
            # 分配默认角色
            role = UserRole(
                user_id=user.id,
                role=UserRoleEnum.USER
            )
            db_session.add(role)
            
            db_session.commit()
            
            return True, "注册成功", user
            
        except Exception as e:
            db_session.rollback()
            return False, f"注册失败: {str(e)}", None
    
    @staticmethod
    def login(
        identifier: str,
        password: str,
        device_info: Optional[Dict] = None
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        用户登录
        
        Args:
            identifier: 用户名/邮箱/手机号
            password: 密码
            device_info: 设备信息
        
        Returns:
            (成功标志, 消息, 令牌信息)
        """
        try:
            # 查找用户（支持用户名、邮箱、手机号登录）
            user = User.query.filter(
                (User.username == identifier) |
                (User.email == identifier) |
                (User.phone == identifier),
                User.is_deleted == False
            ).first()
            
            if not user:
                AuthService._log_login(None, 'password', False, 
                                      '用户不存在', device_info)
                return False, "用户名或密码错误", None
            
            # 验证密码
            if not user.password_hash or not check_password_hash(user.password_hash, password):
                AuthService._log_login(user.id, 'password', False,
                                      '密码错误', device_info)
                return False, "用户名或密码错误", None
            
            # 检查用户状态
            if user.status != 'active':
                return False, f"账号状态异常: {user.status}", None
            
            # 生成令牌
            tokens = AuthService._generate_tokens(user, device_info)
            
            # 更新登录信息
            user.last_login_at = datetime.now()
            user.login_count += 1
            
            # 记录登录历史
            AuthService._log_login(user.id, 'password', True, None, device_info)
            
            db_session.commit()
            
            return True, "登录成功", tokens
            
        except Exception as e:
            db_session.rollback()
            return False, f"登录失败: {str(e)}", None
    
    @staticmethod
    def _generate_tokens(
        user: User,
        device_info: Optional[Dict] = None
    ) -> Dict:
        """生成访问令牌和刷新令牌"""
        now = datetime.utcnow()
        
        # 生成访问令牌（短期）
        access_payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': now + timedelta(hours=24),
            'iat': now,
            'type': 'access'
        }
        access_token = jwt.encode(
            access_payload,
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        # 生成刷新令牌（长期）
        refresh_token_str = secrets.token_urlsafe(32)
        refresh_payload = {
            'user_id': user.id,
            'token': refresh_token_str,
            'exp': now + timedelta(days=30),
            'iat': now,
            'type': 'refresh'
        }
        refresh_token_jwt = jwt.encode(
            refresh_payload,
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        # 保存刷新令牌到数据库
        refresh_token_db = RefreshToken(
            user_id=user.id,
            token=refresh_token_str,
            expires_at=now + timedelta(days=30),
            device_id=device_info.get('device_id') if device_info else None,
            device_type=device_info.get('device_type') if device_info else None,
            device_name=device_info.get('device_name') if device_info else None,
            ip_address=device_info.get('ip_address') if device_info else None,
            user_agent=device_info.get('user_agent') if device_info else None
        )
        db_session.add(refresh_token_db)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token_jwt,
            'token_type': 'Bearer',
            'expires_in': 86400  # 24小时（秒）
        }
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        使用刷新令牌获取新的访问令牌
        
        Args:
            refresh_token: 刷新令牌
        
        Returns:
            (成功标志, 消息, 令牌信息)
        """
        try:
            # 验证JWT
            payload = jwt.decode(
                refresh_token,
                Config.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            
            if payload.get('type') != 'refresh':
                return False, "令牌类型错误", None
            
            user_id = payload.get('user_id')
            token_str = payload.get('token')
            
            # 查询数据库中的刷新令牌
            token_db = RefreshToken.query.filter_by(
                user_id=user_id,
                token=token_str,
                is_revoked=False,
                is_deleted=False
            ).first()
            
            if not token_db:
                return False, "刷新令牌无效", None
            
            # 检查是否过期
            if token_db.expires_at < datetime.utcnow():
                return False, "刷新令牌已过期", None
            
            # 获取用户
            user = User.query.get(user_id)
            if not user or user.is_deleted:
                return False, "用户不存在", None
            
            # 生成新的访问令牌
            now = datetime.utcnow()
            access_payload = {
                'user_id': user.id,
                'username': user.username,
                'exp': now + timedelta(hours=24),
                'iat': now,
                'type': 'access'
            }
            access_token = jwt.encode(
                access_payload,
                Config.JWT_SECRET_KEY,
                algorithm='HS256'
            )
            
            # 更新刷新令牌使用记录
            token_db.last_used_at = now
            token_db.use_count += 1
            db_session.commit()
            
            return True, "令牌刷新成功", {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 86400
            }
            
        except jwt.ExpiredSignatureError:
            return False, "刷新令牌已过期", None
        except jwt.InvalidTokenError:
            return False, "刷新令牌无效", None
        except Exception as e:
            return False, f"令牌刷新失败: {str(e)}", None
    
    @staticmethod
    def logout(user_id: int, refresh_token: Optional[str] = None):
        """
        用户登出
        
        Args:
            user_id: 用户ID
            refresh_token: 刷新令牌（可选，如果提供则只撤销该令牌）
        """
        try:
            if refresh_token:
                # 撤销指定的刷新令牌
                payload = jwt.decode(
                    refresh_token,
                    Config.JWT_SECRET_KEY,
                    algorithms=['HS256']
                )
                token_str = payload.get('token')
                
                token_db = RefreshToken.query.filter_by(
                    user_id=user_id,
                    token=token_str,
                    is_deleted=False
                ).first()
                
                if token_db:
                    token_db.is_revoked = True
                    token_db.revoked_at = datetime.utcnow()
            else:
                # 撤销所有刷新令牌
                RefreshToken.query.filter_by(
                    user_id=user_id,
                    is_revoked=False,
                    is_deleted=False
                ).update({
                    'is_revoked': True,
                    'revoked_at': datetime.utcnow()
                })
            
            db_session.commit()
            return True, "登出成功"
            
        except Exception as e:
            db_session.rollback()
            return False, f"登出失败: {str(e)}"
    
    @staticmethod
    def request_password_reset(identifier: str) -> Tuple[bool, str, Optional[str]]:
        """
        请求密码重置
        
        Args:
            identifier: 邮箱或手机号
        
        Returns:
            (成功标志, 消息, 重置令牌)
        """
        try:
            # 查找用户
            user = User.query.filter(
                (User.email == identifier) | (User.phone == identifier),
                User.is_deleted == False
            ).first()
            
            if not user:
                # 为了安全，不透露用户是否存在
                return True, "如果该账号存在，重置链接已发送", None
            
            # 生成重置令牌
            reset_token = secrets.token_urlsafe(32)
            verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            
            # 保存到数据库
            reset_token_db = PasswordResetToken(
                user_id=user.id,
                token=reset_token,
                verification_code=verification_code,
                verification_type='email' if '@' in identifier else 'sms',
                expires_at=datetime.utcnow() + timedelta(hours=1)
            )
            db_session.add(reset_token_db)
            db_session.commit()
            
            # TODO: 发送邮件或短信
            # send_email(user.email, verification_code)
            # send_sms(user.phone, verification_code)
            
            return True, "重置链接已发送", reset_token
            
        except Exception as e:
            db_session.rollback()
            return False, f"请求失败: {str(e)}", None
    
    @staticmethod
    def reset_password(
        token: str,
        verification_code: str,
        new_password: str
    ) -> Tuple[bool, str]:
        """
        重置密码
        
        Args:
            token: 重置令牌
            verification_code: 验证码
            new_password: 新密码
        
        Returns:
            (成功标志, 消息)
        """
        try:
            # 验证密码强度
            if not Validator.validate_password(new_password):
                return False, "密码强度不够（至少8位，包含大小写字母和数字）"
            
            # 查找令牌
            reset_token_db = PasswordResetToken.query.filter_by(
                token=token,
                verification_code=verification_code,
                is_used=False,
                is_deleted=False
            ).first()
            
            if not reset_token_db:
                return False, "重置令牌或验证码无效"
            
            # 检查是否过期
            if reset_token_db.expires_at < datetime.utcnow():
                return False, "重置令牌已过期"
            
            # 更新密码
            user = User.query.get(reset_token_db.user_id)
            if not user:
                return False, "用户不存在"
            
            user.password_hash = generate_password_hash(new_password)
            
            # 标记令牌为已使用
            reset_token_db.is_used = True
            reset_token_db.used_at = datetime.utcnow()
            
            # 撤销所有刷新令牌（强制重新登录）
            RefreshToken.query.filter_by(
                user_id=user.id,
                is_revoked=False
            ).update({'is_revoked': True, 'revoked_at': datetime.utcnow()})
            
            # 记录安全日志
            security_log = SecurityLog(
                user_id=user.id,
                event_type='password_reset',
                event_description='密码已重置',
                is_success=True
            )
            db_session.add(security_log)
            
            db_session.commit()
            
            return True, "密码重置成功"
            
        except Exception as e:
            db_session.rollback()
            return False, f"密码重置失败: {str(e)}"
    
    @staticmethod
    def change_password(
        user_id: int,
        old_password: str,
        new_password: str
    ) -> Tuple[bool, str]:
        """
        修改密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
        
        Returns:
            (成功标志, 消息)
        """
        try:
            # 验证新密码强度
            if not Validator.validate_password(new_password):
                return False, "密码强度不够（至少8位，包含大小写字母和数字）"
            
            # 获取用户
            user = User.query.get(user_id)
            if not user or user.is_deleted:
                return False, "用户不存在"
            
            # 验证旧密码
            if not check_password_hash(user.password_hash, old_password):
                return False, "旧密码错误"
            
            # 更新密码
            user.password_hash = generate_password_hash(new_password)
            
            # 记录安全日志
            security_log = SecurityLog(
                user_id=user.id,
                event_type='password_change',
                event_description='密码已修改',
                is_success=True
            )
            db_session.add(security_log)
            
            db_session.commit()
            
            return True, "密码修改成功"
            
        except Exception as e:
            db_session.rollback()
            return False, f"密码修改失败: {str(e)}"
    
    @staticmethod
    def _log_login(
        user_id: Optional[int],
        login_type: str,
        is_success: bool,
        fail_reason: Optional[str],
        device_info: Optional[Dict]
    ):
        """记录登录历史"""
        try:
            login_history = LoginHistory(
                user_id=user_id,
                login_type=login_type,
                is_success=is_success,
                fail_reason=fail_reason,
                device_id=device_info.get('device_id') if device_info else None,
                device_type=device_info.get('device_type') if device_info else None,
                device_name=device_info.get('device_name') if device_info else None,
                ip_address=device_info.get('ip_address') if device_info else None,
                user_agent=device_info.get('user_agent') if device_info else None
            )
            db_session.add(login_history)
            db_session.commit()
        except:
            pass  # 登录日志失败不影响主流程
