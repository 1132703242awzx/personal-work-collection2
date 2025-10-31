"""
运动记录API交互式测试工具
提供完整的测试功能和示例数据
"""
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional


class WorkoutAPITester:
    """运动记录API测试类"""
    
    def __init__(self, base_url: str = "http://localhost:5000/api", token: str = None):
        """
        初始化测试工具
        
        Args:
            base_url: API基础URL
            token: JWT认证令牌
        """
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Content-Type': 'application/json'
        }
        if token:
            self.headers['Authorization'] = f'Bearer {token}'
    
    def set_token(self, token: str):
        """设置认证令牌"""
        self.token = token
        self.headers['Authorization'] = f'Bearer {token}'
    
    def _request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None):
        """
        发送HTTP请求
        
        Args:
            method: 请求方法
            endpoint: 端点路径
            data: 请求体数据
            params: 查询参数
            
        Returns:
            响应对象
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )
            
            print(f"\n{'='*60}")
            print(f"请求: {method} {endpoint}")
            if params:
                print(f"参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
            if data:
                print(f"请求体: {json.dumps(data, ensure_ascii=False, indent=2)}")
            print(f"状态码: {response.status_code}")
            print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
            print(f"{'='*60}\n")
            
            return response
        except Exception as e:
            print(f"请求失败: {str(e)}")
            return None
    
    # ========== 基础操作 ==========
    
    def create_workout(self, workout_data: Dict):
        """创建训练记录"""
        return self._request('POST', '/workouts', data=workout_data)
    
    def get_workouts(self, filters: Dict = None):
        """获取训练列表"""
        return self._request('GET', '/workouts', params=filters)
    
    def get_workout_detail(self, workout_id: int):
        """获取训练详情"""
        return self._request('GET', f'/workouts/{workout_id}')
    
    def update_workout(self, workout_id: int, update_data: Dict):
        """更新训练记录"""
        return self._request('PUT', f'/workouts/{workout_id}', data=update_data)
    
    def finish_workout(self, workout_id: int, notes: str = None):
        """完成训练"""
        data = {'notes': notes} if notes else {}
        return self._request('POST', f'/workouts/{workout_id}/finish', data=data)
    
    def delete_workout(self, workout_id: int):
        """删除训练记录"""
        return self._request('DELETE', f'/workouts/{workout_id}')
    
    # ========== 训练组操作 ==========
    
    def add_set(self, workout_id: int, set_data: Dict):
        """添加训练组"""
        return self._request('POST', f'/workouts/{workout_id}/sets', data=set_data)
    
    def update_set(self, set_id: int, update_data: Dict):
        """更新训练组"""
        return self._request('PUT', f'/sets/{set_id}', data=update_data)
    
    def delete_set(self, set_id: int):
        """删除训练组"""
        return self._request('DELETE', f'/sets/{set_id}')
    
    # ========== 查询功能 ==========
    
    def get_calendar(self, year: int = None, month: int = None):
        """获取训练日历"""
        params = {}
        if year:
            params['year'] = year
        if month:
            params['month'] = month
        return self._request('GET', '/workouts/calendar', params=params)
    
    def get_personal_records(self, exercise_name: str = None):
        """获取个人最佳记录"""
        params = {}
        if exercise_name:
            params['exercise_name'] = exercise_name
        return self._request('GET', '/workouts/records', params=params)
    
    # ========== 统计功能 ==========
    
    def get_stats_overview(self, start_date: str = None, end_date: str = None):
        """获取统计总览"""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        return self._request('GET', '/stats/overview', params=params)
    
    def get_weekly_stats(self):
        """获取周统计"""
        return self._request('GET', '/stats/weekly')
    
    def get_monthly_stats(self, year: int = None, month: int = None):
        """获取月统计"""
        params = {}
        if year:
            params['year'] = year
        if month:
            params['month'] = month
        return self._request('GET', '/stats/monthly', params=params)
    
    def get_muscle_distribution(self, start_date: str = None, end_date: str = None):
        """获取肌群分布"""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        return self._request('GET', '/stats/muscle-distribution', params=params)
    
    def get_workout_type_distribution(self, start_date: str = None, end_date: str = None):
        """获取训练类型分布"""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        return self._request('GET', '/stats/workout-types', params=params)
    
    def get_progress_trend(self, exercise_name: str = None, period: str = 'month'):
        """获取进步趋势"""
        params = {'period': period}
        if exercise_name:
            params['exercise_name'] = exercise_name
        return self._request('GET', '/stats/progress', params=params)
    
    def get_consistency_score(self):
        """获取坚持度评分"""
        return self._request('GET', '/stats/consistency')


# ========== 示例数据 ==========

def get_sample_workout():
    """获取示例训练记录"""
    return {
        "workout_date": datetime.now().strftime('%Y-%m-%d'),
        "workout_type": "力量训练",
        "plan_id": 1,
        "notes": "今天状态不错",
        "exercises": [
            {
                "exercise_name": "深蹲",
                "muscle_group": "腿部",
                "sets": [
                    {
                        "set_number": 1,
                        "set_type": "warmup",
                        "reps": 10,
                        "weight": 60.0
                    },
                    {
                        "set_number": 2,
                        "set_type": "normal",
                        "reps": 8,
                        "weight": 80.0
                    },
                    {
                        "set_number": 3,
                        "set_type": "normal",
                        "reps": 8,
                        "weight": 85.0
                    }
                ]
            },
            {
                "exercise_name": "卧推",
                "muscle_group": "胸部",
                "sets": [
                    {
                        "set_number": 1,
                        "set_type": "warmup",
                        "reps": 12,
                        "weight": 40.0
                    },
                    {
                        "set_number": 2,
                        "set_type": "normal",
                        "reps": 10,
                        "weight": 60.0
                    },
                    {
                        "set_number": 3,
                        "set_type": "normal",
                        "reps": 8,
                        "weight": 65.0
                    }
                ]
            }
        ]
    }


def get_sample_cardio_workout():
    """获取示例有氧训练"""
    return {
        "workout_date": datetime.now().strftime('%Y-%m-%d'),
        "workout_type": "有氧训练",
        "notes": "晨跑",
        "exercises": [
            {
                "exercise_name": "跑步",
                "muscle_group": "全身",
                "sets": [
                    {
                        "set_number": 1,
                        "set_type": "normal",
                        "duration": 30,
                        "distance": 5.0
                    }
                ]
            }
        ]
    }


# ========== 测试场景 ==========

def test_complete_workflow(tester: WorkoutAPITester):
    """测试完整工作流程"""
    print("\n" + "="*60)
    print("测试场景: 完整训练流程")
    print("="*60)
    
    # 1. 创建训练记录
    print("\n1. 创建训练记录")
    workout_data = get_sample_workout()
    response = tester.create_workout(workout_data)
    if not response or response.status_code != 201:
        print("❌ 创建失败")
        return
    
    workout_id = response.json()['data']['id']
    print(f"✅ 创建成功, ID: {workout_id}")
    
    # 2. 查看详情
    print("\n2. 查看训练详情")
    tester.get_workout_detail(workout_id)
    
    # 3. 添加额外的训练组
    print("\n3. 添加额外的训练组")
    set_data = {
        "exercise_id": 1,
        "set_number": 4,
        "set_type": "normal",
        "reps": 6,
        "weight": 90.0
    }
    tester.add_set(workout_id, set_data)
    
    # 4. 完成训练
    print("\n4. 完成训练")
    tester.finish_workout(workout_id, "完成了!感觉很棒!")
    
    # 5. 查看个人记录
    print("\n5. 查看个人最佳记录")
    tester.get_personal_records("深蹲")
    
    print("\n✅ 完整流程测试完成!")


def test_statistics(tester: WorkoutAPITester):
    """测试统计功能"""
    print("\n" + "="*60)
    print("测试场景: 统计功能")
    print("="*60)
    
    # 1. 总览统计
    print("\n1. 获取统计总览")
    tester.get_stats_overview()
    
    # 2. 周统计
    print("\n2. 获取周统计")
    tester.get_weekly_stats()
    
    # 3. 月统计
    print("\n3. 获取月统计")
    tester.get_monthly_stats()
    
    # 4. 肌群分布
    print("\n4. 获取肌群分布")
    tester.get_muscle_distribution()
    
    # 5. 训练类型分布
    print("\n5. 获取训练类型分布")
    tester.get_workout_type_distribution()
    
    # 6. 进步趋势
    print("\n6. 获取进步趋势")
    tester.get_progress_trend("深蹲", "month")
    
    # 7. 坚持度评分
    print("\n7. 获取坚持度评分")
    tester.get_consistency_score()
    
    print("\n✅ 统计功能测试完成!")


def test_calendar_view(tester: WorkoutAPITester):
    """测试日历视图"""
    print("\n" + "="*60)
    print("测试场景: 日历视图")
    print("="*60)
    
    now = datetime.now()
    tester.get_calendar(now.year, now.month)
    
    print("\n✅ 日历视图测试完成!")


def test_filtering(tester: WorkoutAPITester):
    """测试筛选功能"""
    print("\n" + "="*60)
    print("测试场景: 训练列表筛选")
    print("="*60)
    
    # 1. 获取所有训练
    print("\n1. 获取所有训练")
    tester.get_workouts()
    
    # 2. 按日期筛选
    print("\n2. 按日期范围筛选")
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    tester.get_workouts({
        'start_date': week_ago.strftime('%Y-%m-%d'),
        'end_date': today.strftime('%Y-%m-%d')
    })
    
    # 3. 按类型筛选
    print("\n3. 按训练类型筛选")
    tester.get_workouts({'workout_type': '力量训练'})
    
    # 4. 按完成状态筛选
    print("\n4. 按完成状态筛选")
    tester.get_workouts({'is_completed': 'true'})
    
    # 5. 组合筛选
    print("\n5. 组合筛选")
    tester.get_workouts({
        'start_date': week_ago.strftime('%Y-%m-%d'),
        'workout_type': '力量训练',
        'is_completed': 'true',
        'page': 1,
        'per_page': 10
    })
    
    print("\n✅ 筛选功能测试完成!")


# ========== 交互式菜单 ==========

def print_menu():
    """打印菜单"""
    print("\n" + "="*60)
    print("运动记录API测试工具")
    print("="*60)
    print("\n基础操作:")
    print("  1. 创建训练记录")
    print("  2. 获取训练列表")
    print("  3. 查看训练详情")
    print("  4. 完成训练")
    print("  5. 删除训练记录")
    print("\n查询功能:")
    print("  6. 获取训练日历")
    print("  7. 查看个人最佳记录")
    print("\n统计功能:")
    print("  8. 统计总览")
    print("  9. 周统计")
    print("  10. 月统计")
    print("  11. 肌群分布")
    print("  12. 坚持度评分")
    print("\n测试场景:")
    print("  20. 完整工作流程测试")
    print("  21. 统计功能测试")
    print("  22. 日历视图测试")
    print("  23. 筛选功能测试")
    print("\n其他:")
    print("  0. 退出")
    print("="*60)


def interactive_mode():
    """交互式模式"""
    print("欢迎使用运动记录API测试工具!")
    
    # 获取配置
    base_url = input("请输入API基础URL (默认: http://localhost:5000/api): ").strip()
    if not base_url:
        base_url = "http://localhost:5000/api"
    
    token = input("请输入JWT令牌 (可选): ").strip() or None
    
    tester = WorkoutAPITester(base_url, token)
    
    while True:
        print_menu()
        choice = input("\n请选择操作: ").strip()
        
        if choice == '0':
            print("再见!")
            break
        elif choice == '1':
            workout_data = get_sample_workout()
            tester.create_workout(workout_data)
        elif choice == '2':
            tester.get_workouts()
        elif choice == '3':
            workout_id = input("请输入训练ID: ").strip()
            if workout_id.isdigit():
                tester.get_workout_detail(int(workout_id))
        elif choice == '4':
            workout_id = input("请输入训练ID: ").strip()
            notes = input("请输入备注 (可选): ").strip() or None
            if workout_id.isdigit():
                tester.finish_workout(int(workout_id), notes)
        elif choice == '5':
            workout_id = input("请输入训练ID: ").strip()
            if workout_id.isdigit():
                tester.delete_workout(int(workout_id))
        elif choice == '6':
            tester.get_calendar()
        elif choice == '7':
            exercise = input("请输入动作名称 (可选): ").strip() or None
            tester.get_personal_records(exercise)
        elif choice == '8':
            tester.get_stats_overview()
        elif choice == '9':
            tester.get_weekly_stats()
        elif choice == '10':
            tester.get_monthly_stats()
        elif choice == '11':
            tester.get_muscle_distribution()
        elif choice == '12':
            tester.get_consistency_score()
        elif choice == '20':
            test_complete_workflow(tester)
        elif choice == '21':
            test_statistics(tester)
        elif choice == '22':
            test_calendar_view(tester)
        elif choice == '23':
            test_filtering(tester)
        else:
            print("无效的选择,请重试!")
        
        input("\n按回车键继续...")


if __name__ == '__main__':
    interactive_mode()
