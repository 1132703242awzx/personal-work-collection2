"""
第三方登录服务
处理微信、Apple等第三方平台的登录
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import requests
import jwt

from models import User, UserProfile, UserSettings, UserRole, ThirdPartyAccount, UserRoleEnum, ThirdPartyProviderEnum
from config.database import db_session
from services.auth_service import AuthService


class ThirdPartyAuthService:
    """第三方认证服务类"""
    
    # 微信配置
    WECHAT_APP_ID = "your_wechat_app_id"
    WECHAT_APP_SECRET = "your_wechat_app_secret"
    
    # Apple配置
    APPLE_CLIENT_ID = "your_apple_client_id"
    APPLE_TEAM_ID = "your_apple_team_id"
    APPLE_KEY_ID = "your_apple_key_id"
    
    @staticmethod
    def wechat_login(code: str, device_info: Optional[Dict] = None) -> Tuple[bool, str, Optional[Dict]]:
        """
        微信登录
        
        Args:
            code: 微信授权码
            device_info: 设备信息
        
        Returns:
            (成功标志, 消息, 令牌信息)
        """
        try:
            # 1. 使用code换取access_token
            wechat_data = ThirdPartyAuthService._get_wechat_access_token(code)
            if not wechat_data:
                return False, "微信授权失败", None
            
            openid = wechat_data.get('openid')
            access_token = wechat_data.get('access_token')
            
            # 2. 获取用户信息
            user_info = ThirdPartyAuthService._get_wechat_user_info(access_token, openid)
            
            # 3. 查找或创建账号
            third_party_account = ThirdPartyAccount.query.filter_by(
                provider=ThirdPartyProviderEnum.WECHAT,
                provider_user_id=openid,
                is_deleted=False
            ).first()
            
            if third_party_account:
                # 已绑定账号，直接登录
                user = User.query.get(third_party_account.user_id)
                if not user or user.is_deleted:
                    return False, "用户不存在", None
                
                # 更新第三方账号信息
                third_party_account.access_token = access_token
                third_party_account.last_login_at = datetime.utcnow()
                if user_info:
                    third_party_account.nickname = user_info.get('nickname')
                    third_party_account.avatar_url = user_info.get('headimgurl')
                
            else:
                # 创建新用户
                username = f"wx_{openid[:16]}"
                nickname = user_info.get('nickname', '微信用户') if user_info else '微信用户'
                
                # 创建用户
                user = User(
                    username=username,
                    status='active',
                    is_verified=True  # 第三方登录默认已验证
                )
                db_session.add(user)
                db_session.flush()
                
                # 创建用户资料
                profile = UserProfile(
                    user_id=user.id,
                    nickname=nickname,
                    avatar_url=user_info.get('headimgurl') if user_info else None,
                    gender='male' if user_info and user_info.get('sex') == 1 else 'female' if user_info and user_info.get('sex') == 2 else 'other'
                )
                db_session.add(profile)
                
                # 创建用户设置
                settings = UserSettings(user_id=user.id)
                db_session.add(settings)
                
                # 分配角色
                role = UserRole(user_id=user.id, role=UserRoleEnum.USER)
                db_session.add(role)
                
                # 创建第三方账号绑定
                third_party_account = ThirdPartyAccount(
                    user_id=user.id,
                    provider=ThirdPartyProviderEnum.WECHAT,
                    provider_user_id=openid,
                    access_token=access_token,
                    nickname=nickname,
                    avatar_url=user_info.get('headimgurl') if user_info else None
                )
                db_session.add(third_party_account)
            
            # 4. 生成JWT令牌
            tokens = AuthService._generate_tokens(user, device_info)
            
            # 5. 更新登录信息
            user.last_login_at = datetime.now()
            user.login_count += 1
            
            # 6. 记录登录历史
            AuthService._log_login(user.id, 'wechat', True, None, device_info)
            
            db_session.commit()
            
            return True, "登录成功", tokens
            
        except Exception as e:
            db_session.rollback()
            return False, f"微信登录失败: {str(e)}", None
    
    @staticmethod
    def _get_wechat_access_token(code: str) -> Optional[Dict]:
        """获取微信access_token"""
        try:
            url = "https://api.weixin.qq.com/sns/oauth2/access_token"
            params = {
                'appid': ThirdPartyAuthService.WECHAT_APP_ID,
                'secret': ThirdPartyAuthService.WECHAT_APP_SECRET,
                'code': code,
                'grant_type': 'authorization_code'
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'errcode' in data:
                print(f"微信授权失败: {data}")
                return None
            
            return data
        except Exception as e:
            print(f"获取微信access_token失败: {str(e)}")
            return None
    
    @staticmethod
    def _get_wechat_user_info(access_token: str, openid: str) -> Optional[Dict]:
        """获取微信用户信息"""
        try:
            url = "https://api.weixin.qq.com/sns/userinfo"
            params = {
                'access_token': access_token,
                'openid': openid,
                'lang': 'zh_CN'
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'errcode' in data:
                print(f"获取微信用户信息失败: {data}")
                return None
            
            return data
        except Exception as e:
            print(f"获取微信用户信息失败: {str(e)}")
            return None
    
    @staticmethod
    def apple_login(
        id_token: str,
        user_info: Optional[Dict] = None,
        device_info: Optional[Dict] = None
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Apple登录
        
        Args:
            id_token: Apple ID Token
            user_info: 用户信息（首次登录时提供）
            device_info: 设备信息
        
        Returns:
            (成功标志, 消息, 令牌信息)
        """
        try:
            # 1. 验证Apple ID Token
            apple_user_id = ThirdPartyAuthService._verify_apple_token(id_token)
            if not apple_user_id:
                return False, "Apple授权失败", None
            
            # 2. 查找或创建账号
            third_party_account = ThirdPartyAccount.query.filter_by(
                provider=ThirdPartyProviderEnum.APPLE,
                provider_user_id=apple_user_id,
                is_deleted=False
            ).first()
            
            if third_party_account:
                # 已绑定账号
                user = User.query.get(third_party_account.user_id)
                if not user or user.is_deleted:
                    return False, "用户不存在", None
                
                # 更新登录时间
                third_party_account.last_login_at = datetime.utcnow()
                
            else:
                # 创建新用户
                username = f"apple_{apple_user_id[:16]}"
                
                # 从user_info获取信息
                email = user_info.get('email') if user_info else None
                first_name = user_info.get('firstName') if user_info else None
                last_name = user_info.get('lastName') if user_info else None
                nickname = f"{last_name or ''}{first_name or ''}" or 'Apple用户'
                
                user = User(
                    username=username,
                    email=email,
                    status='active',
                    is_verified=True
                )
                db_session.add(user)
                db_session.flush()
                
                # 创建用户资料
                profile = UserProfile(
                    user_id=user.id,
                    nickname=nickname
                )
                db_session.add(profile)
                
                # 创建用户设置
                settings = UserSettings(user_id=user.id)
                db_session.add(settings)
                
                # 分配角色
                role = UserRole(user_id=user.id, role=UserRoleEnum.USER)
                db_session.add(role)
                
                # 创建第三方账号绑定
                third_party_account = ThirdPartyAccount(
                    user_id=user.id,
                    provider=ThirdPartyProviderEnum.APPLE,
                    provider_user_id=apple_user_id,
                    email=email,
                    nickname=nickname
                )
                db_session.add(third_party_account)
            
            # 3. 生成JWT令牌
            tokens = AuthService._generate_tokens(user, device_info)
            
            # 4. 更新登录信息
            user.last_login_at = datetime.now()
            user.login_count += 1
            
            # 5. 记录登录历史
            AuthService._log_login(user.id, 'apple', True, None, device_info)
            
            db_session.commit()
            
            return True, "登录成功", tokens
            
        except Exception as e:
            db_session.rollback()
            return False, f"Apple登录失败: {str(e)}", None
    
    @staticmethod
    def _verify_apple_token(id_token: str) -> Optional[str]:
        """验证Apple ID Token"""
        try:
            # 解码JWT（不验证签名，生产环境需要验证）
            # 生产环境应该使用Apple的公钥验证签名
            decoded = jwt.decode(id_token, options={"verify_signature": False})
            
            # 验证issuer
            if decoded.get('iss') != 'https://appleid.apple.com':
                return None
            
            # 验证audience
            if decoded.get('aud') != ThirdPartyAuthService.APPLE_CLIENT_ID:
                return None
            
            # 返回用户ID
            return decoded.get('sub')
            
        except Exception as e:
            print(f"验证Apple Token失败: {str(e)}")
            return None
    
    @staticmethod
    def bind_third_party(
        user_id: int,
        provider: str,
        code: str
    ) -> Tuple[bool, str]:
        """
        绑定第三方账号
        
        Args:
            user_id: 用户ID
            provider: 第三方平台（wechat/apple）
            code: 授权码
        
        Returns:
            (成功标志, 消息)
        """
        try:
            user = User.query.get(user_id)
            if not user or user.is_deleted:
                return False, "用户不存在"
            
            if provider == 'wechat':
                # 获取微信信息
                wechat_data = ThirdPartyAuthService._get_wechat_access_token(code)
                if not wechat_data:
                    return False, "微信授权失败"
                
                openid = wechat_data.get('openid')
                
                # 检查是否已绑定
                existing = ThirdPartyAccount.query.filter_by(
                    provider=ThirdPartyProviderEnum.WECHAT,
                    provider_user_id=openid,
                    is_deleted=False
                ).first()
                
                if existing:
                    if existing.user_id == user_id:
                        return False, "已绑定该微信账号"
                    else:
                        return False, "该微信账号已被其他用户绑定"
                
                # 创建绑定
                user_info = ThirdPartyAuthService._get_wechat_user_info(
                    wechat_data.get('access_token'), openid
                )
                
                third_party = ThirdPartyAccount(
                    user_id=user_id,
                    provider=ThirdPartyProviderEnum.WECHAT,
                    provider_user_id=openid,
                    access_token=wechat_data.get('access_token'),
                    nickname=user_info.get('nickname') if user_info else None,
                    avatar_url=user_info.get('headimgurl') if user_info else None
                )
                db_session.add(third_party)
                
            else:
                return False, f"不支持的第三方平台: {provider}"
            
            db_session.commit()
            return True, "绑定成功"
            
        except Exception as e:
            db_session.rollback()
            return False, f"绑定失败: {str(e)}"
    
    @staticmethod
    def unbind_third_party(user_id: int, provider: str) -> Tuple[bool, str]:
        """
        解绑第三方账号
        
        Args:
            user_id: 用户ID
            provider: 第三方平台
        
        Returns:
            (成功标志, 消息)
        """
        try:
            provider_enum = ThirdPartyProviderEnum[provider.upper()]
            
            third_party = ThirdPartyAccount.query.filter_by(
                user_id=user_id,
                provider=provider_enum,
                is_deleted=False
            ).first()
            
            if not third_party:
                return False, "未绑定该第三方账号"
            
            # 检查是否有密码（至少保留一种登录方式）
            user = User.query.get(user_id)
            if not user.password_hash:
                # 检查是否还有其他第三方账号
                other_accounts = ThirdPartyAccount.query.filter(
                    ThirdPartyAccount.user_id == user_id,
                    ThirdPartyAccount.id != third_party.id,
                    ThirdPartyAccount.is_deleted == False
                ).count()
                
                if other_accounts == 0:
                    return False, "请先设置密码或绑定其他登录方式"
            
            third_party.is_bound = False
            third_party.soft_delete()
            
            db_session.commit()
            return True, "解绑成功"
            
        except Exception as e:
            db_session.rollback()
            return False, f"解绑失败: {str(e)}"
