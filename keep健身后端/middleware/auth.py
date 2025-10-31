"""
JWT认证中间件
用于验证和解析JWT令牌
"""
from functools import wraps
from flask import request, jsonify, g
import jwt
from typing import Optional, List

from config.config import Config
from models import User, UserRole, UserRoleEnum


def token_required(f):
    """
    JWT令牌验证装饰器
    要求请求头中包含有效的Bearer Token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头获取token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': '令牌格式错误'}), 401
        
        if not token:
            return jsonify({'error': '缺少认证令牌'}), 401
        
        try:
            # 验证token
            payload = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            
            if payload.get('type') != 'access':
                return jsonify({'error': '令牌类型错误'}), 401
            
            # 获取用户
            user_id = payload.get('user_id')
            user = User.query.get(user_id)
            
            if not user or user.is_deleted:
                return jsonify({'error': '用户不存在'}), 401
            
            if user.status != 'active':
                return jsonify({'error': f'账号状态异常: {user.status}'}), 403
            
            # 将用户信息存储到g对象
            g.current_user = user
            g.user_id = user.id
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': '令牌已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': '令牌无效'}), 401
        except Exception as e:
            return jsonify({'error': f'认证失败: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(required_roles: List[UserRoleEnum]):
    """
    角色验证装饰器
    要求用户拥有指定角色之一
    
    Args:
        required_roles: 允许的角色列表
    """
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            user = g.current_user
            
            # 获取用户角色
            user_roles = UserRole.query.filter_by(
                user_id=user.id,
                is_deleted=False
            ).all()
            
            user_role_list = [ur.role for ur in user_roles]
            
            # 检查是否拥有所需角色
            has_permission = any(role in user_role_list for role in required_roles)
            
            if not has_permission:
                return jsonify({
                    'error': '权限不足',
                    'required_roles': [role.value for role in required_roles]
                }), 403
            
            # 将角色信息存储到g对象
            g.user_roles = user_role_list
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator


def admin_required(f):
    """管理员权限验证装饰器"""
    return role_required([UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN])(f)


def coach_required(f):
    """教练权限验证装饰器"""
    return role_required([UserRoleEnum.COACH, UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN])(f)


def optional_token(f):
    """
    可选令牌装饰器
    如果提供了令牌则验证，没有提供也可以继续
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                pass
        
        if token:
            try:
                payload = jwt.decode(
                    token,
                    Config.JWT_SECRET_KEY,
                    algorithms=['HS256']
                )
                
                if payload.get('type') == 'access':
                    user_id = payload.get('user_id')
                    user = User.query.get(user_id)
                    
                    if user and not user.is_deleted and user.status == 'active':
                        g.current_user = user
                        g.user_id = user.id
            except:
                pass  # 令牌无效，继续执行但g.current_user为None
        
        return f(*args, **kwargs)
    
    return decorated


def get_current_user() -> Optional[User]:
    """获取当前登录用户"""
    return getattr(g, 'current_user', None)


def get_current_user_id() -> Optional[int]:
    """获取当前登录用户ID"""
    return getattr(g, 'user_id', None)


def check_permission(user_id: int, permission: str) -> bool:
    """
    检查用户是否拥有特定权限
    
    Args:
        user_id: 用户ID
        permission: 权限名称
    
    Returns:
        是否拥有权限
    """
    # TODO: 实现细粒度权限检查
    # 可以基于用户角色和权限表进行检查
    return True
