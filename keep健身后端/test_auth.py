"""
认证系统测试脚本
用于快速测试注册、登录、令牌刷新等功能
"""
import requests
import json
from typing import Dict, Optional

BASE_URL = "http://localhost:5000/api/auth"


class AuthTester:
    """认证测试类"""
    
    def __init__(self):
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_id: Optional[int] = None
    
    def print_response(self, title: str, response: requests.Response):
        """格式化打印响应"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        print(f"状态码: {response.status_code}")
        try:
            print(f"响应:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"响应: {response.text}")
        print()
    
    def test_register(self, username: str = "testuser", email: str = None, 
                     phone: str = None, password: str = "Test123456"):
        """测试注册"""
        print("\n🔹 测试用户注册")
        url = f"{BASE_URL}/register"
        data = {
            "username": username,
            "email": email or f"{username}@example.com",
            "phone": phone,
            "password": password,
            "nickname": f"{username}的昵称"
        }
        response = requests.post(url, json=data)
        self.print_response("用户注册", response)
        
        if response.status_code == 201:
            self.user_id = response.json()['user']['id']
            print(f"✅ 注册成功！用户ID: {self.user_id}")
            return True
        else:
            print("❌ 注册失败")
            return False
    
    def test_login(self, identifier: str = "testuser", password: str = "Test123456"):
        """测试登录"""
        print("\n🔹 测试用户登录")
        url = f"{BASE_URL}/login"
        data = {
            "identifier": identifier,
            "password": password,
            "device_id": "test_device_001",
            "device_type": "Python",
            "device_name": "Test Script"
        }
        response = requests.post(url, json=data)
        self.print_response("用户登录", response)
        
        if response.status_code == 200:
            tokens = response.json()['tokens']
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']
            print(f"✅ 登录成功！")
            print(f"Access Token: {self.access_token[:50]}...")
            print(f"Refresh Token: {self.refresh_token[:50]}...")
            return True
        else:
            print("❌ 登录失败")
            return False
    
    def test_get_user_info(self):
        """测试获取用户信息"""
        print("\n🔹 测试获取用户信息")
        if not self.access_token:
            print("❌ 请先登录")
            return False
        
        url = f"{BASE_URL}/me"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        self.print_response("获取用户信息", response)
        
        if response.status_code == 200:
            print("✅ 获取成功")
            return True
        else:
            print("❌ 获取失败")
            return False
    
    def test_refresh_token(self):
        """测试刷新令牌"""
        print("\n🔹 测试刷新令牌")
        if not self.refresh_token:
            print("❌ 请先登录")
            return False
        
        url = f"{BASE_URL}/refresh"
        data = {"refresh_token": self.refresh_token}
        response = requests.post(url, json=data)
        self.print_response("刷新令牌", response)
        
        if response.status_code == 200:
            tokens = response.json()['tokens']
            self.access_token = tokens['access_token']
            print(f"✅ 刷新成功！")
            print(f"新的 Access Token: {self.access_token[:50]}...")
            return True
        else:
            print("❌ 刷新失败")
            return False
    
    def test_change_password(self, old_password: str = "Test123456", 
                           new_password: str = "NewTest123456"):
        """测试修改密码"""
        print("\n🔹 测试修改密码")
        if not self.access_token:
            print("❌ 请先登录")
            return False
        
        url = f"{BASE_URL}/password/change"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "old_password": old_password,
            "new_password": new_password
        }
        response = requests.post(url, headers=headers, json=data)
        self.print_response("修改密码", response)
        
        if response.status_code == 200:
            print("✅ 修改成功")
            return True
        else:
            print("❌ 修改失败")
            return False
    
    def test_request_password_reset(self, identifier: str):
        """测试请求密码重置"""
        print("\n🔹 测试请求密码重置")
        url = f"{BASE_URL}/password/reset/request"
        data = {"identifier": identifier}
        response = requests.post(url, json=data)
        self.print_response("请求密码重置", response)
        
        if response.status_code == 200:
            print("✅ 请求成功")
            result = response.json()
            if 'reset_token' in result:
                return result['reset_token']
            return True
        else:
            print("❌ 请求失败")
            return False
    
    def test_reset_password(self, token: str, verification_code: str = "123456",
                          new_password: str = "ResetPassword123"):
        """测试重置密码"""
        print("\n🔹 测试重置密码")
        url = f"{BASE_URL}/password/reset"
        data = {
            "token": token,
            "verification_code": verification_code,
            "new_password": new_password
        }
        response = requests.post(url, json=data)
        self.print_response("重置密码", response)
        
        if response.status_code == 200:
            print("✅ 重置成功")
            return True
        else:
            print("❌ 重置失败")
            return False
    
    def test_logout(self):
        """测试登出"""
        print("\n🔹 测试登出")
        if not self.access_token:
            print("❌ 请先登录")
            return False
        
        url = f"{BASE_URL}/logout"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"refresh_token": self.refresh_token}
        response = requests.post(url, headers=headers, json=data)
        self.print_response("登出", response)
        
        if response.status_code == 200:
            print("✅ 登出成功")
            self.access_token = None
            self.refresh_token = None
            return True
        else:
            print("❌ 登出失败")
            return False
    
    def run_full_test(self):
        """运行完整测试流程"""
        print("\n" + "="*60)
        print("  🚀 开始认证系统完整测试")
        print("="*60)
        
        # 1. 注册
        success = self.test_register(
            username=f"testuser_{int(1000 * __import__('time').time())}",
            email=f"test_{int(1000 * __import__('time').time())}@example.com"
        )
        if not success:
            return
        
        # 2. 登录
        success = self.test_login()
        if not success:
            return
        
        # 3. 获取用户信息
        self.test_get_user_info()
        
        # 4. 刷新令牌
        self.test_refresh_token()
        
        # 5. 再次获取用户信息（验证新令牌）
        self.test_get_user_info()
        
        # 6. 修改密码
        self.test_change_password()
        
        # 7. 登出
        self.test_logout()
        
        print("\n" + "="*60)
        print("  ✅ 测试完成！")
        print("="*60 + "\n")


def main():
    """主函数"""
    print("""
    ╔══════════════════════════════════════════╗
    ║   Keep健身后端 - 认证系统测试工具        ║
    ╚══════════════════════════════════════════╝
    
    确保应用已启动: python app.py
    """)
    
    tester = AuthTester()
    
    while True:
        print("\n请选择测试项目：")
        print("1. 运行完整测试")
        print("2. 测试注册")
        print("3. 测试登录")
        print("4. 测试获取用户信息")
        print("5. 测试刷新令牌")
        print("6. 测试修改密码")
        print("7. 测试请求密码重置")
        print("8. 测试登出")
        print("0. 退出")
        
        choice = input("\n请输入选项 (0-8): ").strip()
        
        if choice == '0':
            print("\n再见！👋")
            break
        elif choice == '1':
            tester.run_full_test()
        elif choice == '2':
            username = input("用户名 (默认testuser): ").strip() or "testuser"
            email = input("邮箱 (默认testuser@example.com): ").strip() or "testuser@example.com"
            password = input("密码 (默认Test123456): ").strip() or "Test123456"
            tester.test_register(username, email, None, password)
        elif choice == '3':
            identifier = input("用户名/邮箱/手机 (默认testuser): ").strip() or "testuser"
            password = input("密码 (默认Test123456): ").strip() or "Test123456"
            tester.test_login(identifier, password)
        elif choice == '4':
            tester.test_get_user_info()
        elif choice == '5':
            tester.test_refresh_token()
        elif choice == '6':
            old_pwd = input("旧密码: ").strip()
            new_pwd = input("新密码: ").strip()
            if old_pwd and new_pwd:
                tester.test_change_password(old_pwd, new_pwd)
        elif choice == '7':
            identifier = input("邮箱或手机号: ").strip()
            if identifier:
                token = tester.test_request_password_reset(identifier)
                if token and isinstance(token, str):
                    print(f"\n重置令牌: {token}")
        elif choice == '8':
            tester.test_logout()
        else:
            print("❌ 无效选项，请重试")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试中断。再见！👋")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
