"""
认证API路由
处理用户注册、登录、令牌刷新等请求
"""
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.third_party_auth_service import ThirdPartyAuthService
from middleware.auth import token_required, get_current_user_id

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    
    请求体:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "phone": "13800138000",
        "password": "Password123",
        "nickname": "John"
    }
    """
    try:
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        success, message, user = AuthService.register_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            nickname=data.get('nickname')
        )
        
        if success:
            return jsonify({
                'message': message,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone
                }
            }), 201
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'注册失败: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    
    请求体:
    {
        "identifier": "john_doe",  # 用户名/邮箱/手机号
        "password": "Password123",
        "device_id": "xxx",
        "device_type": "iOS",
        "device_name": "iPhone 13"
    }
    """
    try:
        data = request.get_json()
        
        identifier = data.get('identifier')
        password = data.get('password')
        
        if not identifier or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        # 设备信息
        device_info = {
            'device_id': data.get('device_id'),
            'device_type': data.get('device_type'),
            'device_name': data.get('device_name'),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
        
        success, message, tokens = AuthService.login(
            identifier=identifier,
            password=password,
            device_info=device_info
        )
        
        if success:
            return jsonify({
                'message': message,
                'tokens': tokens
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    刷新访问令牌
    
    请求体:
    {
        "refresh_token": "xxx"
    }
    """
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': '缺少刷新令牌'}), 400
        
        success, message, tokens = AuthService.refresh_access_token(refresh_token)
        
        if success:
            return jsonify({
                'message': message,
                'tokens': tokens
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': f'令牌刷新失败: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    用户登出
    
    请求头: Authorization: Bearer <access_token>
    请求体:
    {
        "refresh_token": "xxx"  # 可选
    }
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json() or {}
        refresh_token = data.get('refresh_token')
        
        success, message = AuthService.logout(user_id, refresh_token)
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'登出失败: {str(e)}'}), 500


@auth_bp.route('/password/reset/request', methods=['POST'])
def request_password_reset():
    """
    请求密码重置
    
    请求体:
    {
        "identifier": "john@example.com"  # 邮箱或手机号
    }
    """
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        
        if not identifier:
            return jsonify({'error': '邮箱或手机号不能为空'}), 400
        
        success, message, token = AuthService.request_password_reset(identifier)
        
        response_data = {'message': message}
        
        # 开发环境返回token（生产环境不应返回）
        if success and token:
            response_data['reset_token'] = token  # 仅用于测试
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': f'请求失败: {str(e)}'}), 500


@auth_bp.route('/password/reset', methods=['POST'])
def reset_password():
    """
    重置密码
    
    请求体:
    {
        "token": "xxx",
        "verification_code": "123456",
        "new_password": "NewPassword123"
    }
    """
    try:
        data = request.get_json()
        
        token = data.get('token')
        verification_code = data.get('verification_code')
        new_password = data.get('new_password')
        
        if not all([token, verification_code, new_password]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        success, message = AuthService.reset_password(
            token=token,
            verification_code=verification_code,
            new_password=new_password
        )
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'密码重置失败: {str(e)}'}), 500


@auth_bp.route('/password/change', methods=['POST'])
@token_required
def change_password():
    """
    修改密码
    
    请求头: Authorization: Bearer <access_token>
    请求体:
    {
        "old_password": "OldPassword123",
        "new_password": "NewPassword123"
    }
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'error': '旧密码和新密码不能为空'}), 400
        
        success, message = AuthService.change_password(
            user_id=user_id,
            old_password=old_password,
            new_password=new_password
        )
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'密码修改失败: {str(e)}'}), 500


@auth_bp.route('/wechat/login', methods=['POST'])
def wechat_login():
    """
    微信登录
    
    请求体:
    {
        "code": "xxx",
        "device_id": "xxx",
        "device_type": "iOS"
    }
    """
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'error': '缺少授权码'}), 400
        
        device_info = {
            'device_id': data.get('device_id'),
            'device_type': data.get('device_type'),
            'device_name': data.get('device_name'),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
        
        success, message, tokens = ThirdPartyAuthService.wechat_login(
            code=code,
            device_info=device_info
        )
        
        if success:
            return jsonify({
                'message': message,
                'tokens': tokens
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': f'微信登录失败: {str(e)}'}), 500


@auth_bp.route('/apple/login', methods=['POST'])
def apple_login():
    """
    Apple登录
    
    请求体:
    {
        "id_token": "xxx",
        "user_info": {
            "email": "xxx@example.com",
            "firstName": "John",
            "lastName": "Doe"
        },
        "device_id": "xxx"
    }
    """
    try:
        data = request.get_json()
        id_token = data.get('id_token')
        
        if not id_token:
            return jsonify({'error': '缺少ID Token'}), 400
        
        device_info = {
            'device_id': data.get('device_id'),
            'device_type': data.get('device_type'),
            'device_name': data.get('device_name'),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
        
        success, message, tokens = ThirdPartyAuthService.apple_login(
            id_token=id_token,
            user_info=data.get('user_info'),
            device_info=device_info
        )
        
        if success:
            return jsonify({
                'message': message,
                'tokens': tokens
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': f'Apple登录失败: {str(e)}'}), 500


@auth_bp.route('/third-party/bind', methods=['POST'])
@token_required
def bind_third_party():
    """
    绑定第三方账号
    
    请求头: Authorization: Bearer <access_token>
    请求体:
    {
        "provider": "wechat",  # wechat/apple
        "code": "xxx"
    }
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        provider = data.get('provider')
        code = data.get('code')
        
        if not provider or not code:
            return jsonify({'error': '缺少必要参数'}), 400
        
        success, message = ThirdPartyAuthService.bind_third_party(
            user_id=user_id,
            provider=provider,
            code=code
        )
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'绑定失败: {str(e)}'}), 500


@auth_bp.route('/third-party/unbind', methods=['POST'])
@token_required
def unbind_third_party():
    """
    解绑第三方账号
    
    请求头: Authorization: Bearer <access_token>
    请求体:
    {
        "provider": "wechat"
    }
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        provider = data.get('provider')
        
        if not provider:
            return jsonify({'error': '缺少第三方平台参数'}), 400
        
        success, message = ThirdPartyAuthService.unbind_third_party(
            user_id=user_id,
            provider=provider
        )
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'解绑失败: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user_info():
    """
    获取当前用户信息
    
    请求头: Authorization: Bearer <access_token>
    """
    try:
        from middleware.auth import get_current_user
        user = get_current_user()
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 获取用户角色
        roles = UserRole.query.filter_by(
            user_id=user.id,
            is_deleted=False
        ).all()
        
        # 获取第三方账号
        third_party_accounts = ThirdPartyAccount.query.filter_by(
            user_id=user.id,
            is_deleted=False
        ).all()
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'status': user.status,
                'is_verified': user.is_verified,
                'is_premium': user.is_premium,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'roles': [{'role': r.role.value} for r in roles],
                'third_party_accounts': [{
                    'provider': tpa.provider.value,
                    'is_bound': tpa.is_bound
                } for tpa in third_party_accounts]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500
