"""
训练计划API测试脚本
测试训练计划的创建、查询、更新、删除和启动功能
"""
import requests
import json
from typing import Optional


BASE_URL = "http://localhost:5000/api"


class TrainingPlanTester:
    """训练计划测试类"""
    
    def __init__(self):
        self.access_token: Optional[str] = None
        self.plan_id: Optional[int] = None
        self.template_id: Optional[int] = None
    
    def print_response(self, title: str, response: requests.Response):
        """格式化打印响应"""
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}")
        print(f"状态码: {response.status_code}")
        try:
            result = response.json()
            print(f"响应:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except:
            print(f"响应: {response.text}")
            return None
    
    def login(self, username: str = "testuser", password: str = "Test123456"):
        """登录获取token"""
        print("\n🔹 用户登录")
        url = f"{BASE_URL}/auth/login"
        data = {
            "identifier": username,
            "password": password,
            "device_id": "test_device"
        }
        response = requests.post(url, json=data)
        result = self.print_response("用户登录", response)
        
        if response.status_code == 200 and result:
            self.access_token = result['tokens']['access_token']
            print(f"✅ 登录成功！Token: {self.access_token[:50]}...")
            return True
        else:
            print("❌ 登录失败，请先运行 test_auth.py 创建测试用户")
            return False
    
    def get_headers(self):
        """获取请求头"""
        if not self.access_token:
            raise Exception("请先登录")
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def test_create_plan(self):
        """测试创建训练计划"""
        print("\n🔹 测试创建训练计划")
        
        url = f"{BASE_URL}/plans"
        data = {
            "name": "8周增肌训练计划",
            "description": "适合中级健身者的全面增肌计划，包含胸背腿肩臂的全方位训练",
            "difficulty": "intermediate",
            "duration_weeks": 8,
            "days_per_week": 5,
            "goal": "增肌",
            "target_muscle_group": "full_body",
            "is_active": False,
            "plan_days": [
                {
                    "day_number": 1,
                    "day_name": "胸部+三头肌",
                    "description": "胸部和三头肌强化训练",
                    "warm_up": "动态拉伸5分钟",
                    "cool_down": "静态拉伸10分钟",
                    "estimated_duration": 60,
                    "target_calories": 400,
                    "rest_time": 90,
                    "exercises": [
                        {
                            "name": "杠铃卧推",
                            "description": "经典的胸部力量训练动作",
                            "exercise_type": "力量",
                            "muscle_group": "chest",
                            "equipment": "杠铃",
                            "order_number": 1,
                            "sets": 4,
                            "reps": 10,
                            "weight": 60,
                            "rest_time": 90,
                            "difficulty": "intermediate",
                            "calories_per_set": 50,
                            "key_points": [
                                "保持肩胛骨收紧",
                                "下放时控制速度",
                                "推起时胸部发力"
                            ],
                            "common_mistakes": [
                                "臀部离开卧推凳",
                                "手肘过度外展"
                            ]
                        },
                        {
                            "name": "哑铃飞鸟",
                            "description": "胸部孤立训练动作",
                            "exercise_type": "力量",
                            "muscle_group": "chest",
                            "equipment": "哑铃",
                            "order_number": 2,
                            "sets": 3,
                            "reps": 12,
                            "weight": 15,
                            "rest_time": 60,
                            "difficulty": "intermediate",
                            "calories_per_set": 40
                        },
                        {
                            "name": "绳索下压",
                            "description": "三头肌孤立训练",
                            "exercise_type": "力量",
                            "muscle_group": "arms",
                            "equipment": "绳索",
                            "order_number": 3,
                            "sets": 3,
                            "reps": 15,
                            "rest_time": 60,
                            "difficulty": "beginner",
                            "calories_per_set": 30
                        }
                    ]
                },
                {
                    "day_number": 2,
                    "day_name": "背部+二头肌",
                    "description": "背部和二头肌强化训练",
                    "estimated_duration": 65,
                    "target_calories": 420,
                    "exercises": [
                        {
                            "name": "引体向上",
                            "exercise_type": "力量",
                            "muscle_group": "back",
                            "equipment": "单杠",
                            "order_number": 1,
                            "sets": 4,
                            "reps": 8,
                            "rest_time": 90,
                            "difficulty": "advanced",
                            "calories_per_set": 60
                        },
                        {
                            "name": "杠铃划船",
                            "exercise_type": "力量",
                            "muscle_group": "back",
                            "equipment": "杠铃",
                            "order_number": 2,
                            "sets": 4,
                            "reps": 10,
                            "weight": 50,
                            "rest_time": 90,
                            "difficulty": "intermediate",
                            "calories_per_set": 55
                        }
                    ]
                },
                {
                    "day_number": 3,
                    "day_name": "腿部训练",
                    "description": "下肢力量强化",
                    "estimated_duration": 70,
                    "target_calories": 500,
                    "exercises": [
                        {
                            "name": "深蹲",
                            "exercise_type": "力量",
                            "muscle_group": "legs",
                            "equipment": "杠铃",
                            "order_number": 1,
                            "sets": 5,
                            "reps": 8,
                            "weight": 80,
                            "rest_time": 120,
                            "difficulty": "advanced",
                            "calories_per_set": 70
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(url, headers=self.get_headers(), json=data)
        result = self.print_response("创建训练计划", response)
        
        if response.status_code == 201 and result:
            self.plan_id = result['plan']['id']
            print(f"✅ 创建成功！计划ID: {self.plan_id}")
            return True
        else:
            print("❌ 创建失败")
            return False
    
    def test_get_plans(self):
        """测试获取计划列表"""
        print("\n🔹 测试获取计划列表")
        
        url = f"{BASE_URL}/plans?my_plans=true&page=1&per_page=10"
        response = requests.get(url, headers=self.get_headers())
        result = self.print_response("获取计划列表", response)
        
        if response.status_code == 200:
            print(f"✅ 获取成功！共 {result['pagination']['total']} 个计划")
            return True
        else:
            print("❌ 获取失败")
            return False
    
    def test_get_plan_detail(self):
        """测试获取计划详情"""
        print("\n🔹 测试获取计划详情")
        
        if not self.plan_id:
            print("❌ 请先创建计划")
            return False
        
        url = f"{BASE_URL}/plans/{self.plan_id}"
        response = requests.get(url, headers=self.get_headers())
        result = self.print_response("获取计划详情", response)
        
        if response.status_code == 200:
            print(f"✅ 获取成功！计划包含 {len(result['plan']['plan_days'])} 个训练日")
            return True
        else:
            print("❌ 获取失败")
            return False
    
    def test_update_plan(self):
        """测试更新计划"""
        print("\n🔹 测试更新计划")
        
        if not self.plan_id:
            print("❌ 请先创建计划")
            return False
        
        url = f"{BASE_URL}/plans/{self.plan_id}"
        data = {
            "name": "8周增肌训练计划 (已更新)",
            "description": "更新后的描述：增加了强度",
            "difficulty": "advanced"
        }
        
        response = requests.put(url, headers=self.get_headers(), json=data)
        result = self.print_response("更新计划", response)
        
        if response.status_code == 200:
            print(f"✅ 更新成功！")
            return True
        else:
            print("❌ 更新失败")
            return False
    
    def test_start_plan(self):
        """测试开始执行计划"""
        print("\n🔹 测试开始执行计划")
        
        if not self.plan_id:
            print("❌ 请先创建计划")
            return False
        
        url = f"{BASE_URL}/plans/{self.plan_id}/start"
        response = requests.post(url, headers=self.get_headers())
        result = self.print_response("开始执行计划", response)
        
        if response.status_code == 200:
            print(f"✅ 激活成功！")
            return True
        else:
            print("❌ 激活失败")
            return False
    
    def test_get_progress(self):
        """测试获取计划进度"""
        print("\n🔹 测试获取计划进度")
        
        if not self.plan_id:
            print("❌ 请先创建计划")
            return False
        
        url = f"{BASE_URL}/plans/{self.plan_id}/progress"
        response = requests.get(url, headers=self.get_headers())
        result = self.print_response("获取计划进度", response)
        
        if response.status_code == 200:
            print(f"✅ 获取成功！完成率: {result['completion_rate']}%")
            return True
        else:
            print("❌ 获取失败")
            return False
    
    def test_filter_plans(self):
        """测试筛选功能"""
        print("\n🔹 测试计划筛选")
        
        # 按难度筛选
        url = f"{BASE_URL}/plans?difficulty=intermediate"
        response = requests.get(url, headers=self.get_headers())
        result = self.print_response("按难度筛选", response)
        
        # 按目标肌群筛选
        url = f"{BASE_URL}/plans?target_muscle_group=full_body"
        response = requests.get(url, headers=self.get_headers())
        result = self.print_response("按目标肌群筛选", response)
        
        # 搜索
        url = f"{BASE_URL}/plans?keyword=增肌"
        response = requests.get(url, headers=self.get_headers())
        result = self.print_response("搜索计划", response)
        
        if response.status_code == 200:
            print("✅ 筛选功能正常")
            return True
        else:
            print("❌ 筛选失败")
            return False
    
    def test_delete_plan(self):
        """测试删除计划"""
        print("\n🔹 测试删除计划")
        
        if not self.plan_id:
            print("❌ 请先创建计划")
            return False
        
        confirm = input(f"\n⚠️  确定要删除计划 {self.plan_id} 吗？(y/n): ")
        if confirm.lower() != 'y':
            print("已取消删除")
            return False
        
        url = f"{BASE_URL}/plans/{self.plan_id}"
        response = requests.delete(url, headers=self.get_headers())
        self.print_response("删除计划", response)
        
        if response.status_code == 200:
            print(f"✅ 删除成功！")
            self.plan_id = None
            return True
        else:
            print("❌ 删除失败")
            return False
    
    def run_full_test(self):
        """运行完整测试流程"""
        print("\n" + "="*70)
        print("  🚀 开始训练计划API完整测试")
        print("="*70)
        
        # 1. 登录
        if not self.login():
            return
        
        # 2. 创建计划
        self.test_create_plan()
        
        # 3. 获取列表
        self.test_get_plans()
        
        # 4. 获取详情
        self.test_get_plan_detail()
        
        # 5. 更新计划
        self.test_update_plan()
        
        # 6. 开始执行
        self.test_start_plan()
        
        # 7. 获取进度
        self.test_get_progress()
        
        # 8. 筛选功能
        self.test_filter_plans()
        
        # 9. 删除计划（可选）
        # self.test_delete_plan()
        
        print("\n" + "="*70)
        print("  ✅ 测试完成！")
        print("="*70 + "\n")


def main():
    """主函数"""
    print("""
    ╔════════════════════════════════════════════════╗
    ║   Keep健身后端 - 训练计划API测试工具          ║
    ╚════════════════════════════════════════════════╝
    
    确保应用已启动: python app.py
    确保已创建测试用户: python test_auth.py
    """)
    
    tester = TrainingPlanTester()
    
    while True:
        print("\n请选择测试项目：")
        print("1. 运行完整测试")
        print("2. 登录")
        print("3. 创建训练计划")
        print("4. 获取计划列表")
        print("5. 获取计划详情")
        print("6. 更新计划")
        print("7. 开始执行计划")
        print("8. 获取计划进度")
        print("9. 测试筛选功能")
        print("10. 删除计划")
        print("0. 退出")
        
        choice = input("\n请输入选项 (0-10): ").strip()
        
        if choice == '0':
            print("\n再见！👋")
            break
        elif choice == '1':
            tester.run_full_test()
        elif choice == '2':
            username = input("用户名 (默认testuser): ").strip() or "testuser"
            password = input("密码 (默认Test123456): ").strip() or "Test123456"
            tester.login(username, password)
        elif choice == '3':
            tester.test_create_plan()
        elif choice == '4':
            tester.test_get_plans()
        elif choice == '5':
            tester.test_get_plan_detail()
        elif choice == '6':
            tester.test_update_plan()
        elif choice == '7':
            tester.test_start_plan()
        elif choice == '8':
            tester.test_get_progress()
        elif choice == '9':
            tester.test_filter_plans()
        elif choice == '10':
            tester.test_delete_plan()
        else:
            print("❌ 无效选项，请重试")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试中断。再见！👋")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
