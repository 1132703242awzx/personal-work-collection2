"""
Keep健身 - 数据分析API测试工具
支持所有11个分析接口的交互式测试
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class AnalyticsAPITester:
    """数据分析API测试器"""
    
    def __init__(self, base_url: str = "http://localhost:5000", token: str = None):
        self.base_url = base_url
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    def set_token(self, token: str):
        """设置认证token"""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def _print_response(self, title: str, response: requests.Response):
        """打印响应信息"""
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {response.elapsed.total_seconds():.3f}s")
        
        try:
            data = response.json()
            print(f"\n响应数据:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except:
            print(f"响应内容: {response.text}")
    
    def test_frequency_statistics(self, time_range: str = "month", include_chart: bool = True):
        """测试训练频率统计"""
        url = f"{self.base_url}/api/analytics/frequency"
        params = {
            "time_range": time_range,
            "include_chart": include_chart
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"训练频率统计 (time_range={time_range})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n关键指标:")
            print(f"  总训练次数: {data.get('total_workouts', 0)}")
            print(f"  周平均: {data.get('average_per_week', 0):.1f}次")
            print(f"  当前连续: {data.get('current_streak', 0)}天")
            print(f"  最长连续: {data.get('max_streak', 0)}天")
            print(f"  训练频率: {data.get('frequency_rate', 0):.1f}%")
        
        return response
    
    def test_duration_statistics(self, time_range: str = "month", include_chart: bool = True):
        """测试训练时长统计"""
        url = f"{self.base_url}/api/analytics/duration"
        params = {
            "time_range": time_range,
            "include_chart": include_chart
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"训练时长统计 (time_range={time_range})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n关键指标:")
            print(f"  总时长: {data.get('total_duration_formatted', 'N/A')}")
            print(f"  平均时长: {data.get('average_duration_formatted', 'N/A')}")
            print(f"  最长训练: {data.get('longest_workout', 0)}秒")
            print(f"  时长分布: {data.get('duration_distribution', {})}")
        
        return response
    
    def test_strength_progress(self, exercise_id: int = None, time_range: str = "all"):
        """测试力量进步分析"""
        url = f"{self.base_url}/api/analytics/strength-progress"
        params = {
            "time_range": time_range,
            "include_chart": True
        }
        if exercise_id:
            params["exercise_id"] = exercise_id
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"力量进步分析 (exercise_id={exercise_id})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n进步详情:")
            for exercise in data:
                print(f"  {exercise['exercise_name']}:")
                print(f"    起始重量: {exercise['start_weight']}kg")
                print(f"    当前重量: {exercise['current_weight']}kg")
                print(f"    最大重量: {exercise['max_weight']}kg")
                print(f"    进步幅度: {exercise['progress']:.1f}%")
                print(f"    总容量: {exercise['total_volume']:.0f}kg")
                print(f"    记录数: {exercise['records_count']}")
        
        return response
    
    def test_body_trends(self, metrics: str = "weight", time_range: str = "month"):
        """测试身体数据趋势"""
        url = f"{self.base_url}/api/analytics/body-trends"
        params = {
            "metrics": metrics,
            "time_range": time_range,
            "include_chart": True
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"身体数据趋势 (metrics={metrics})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n趋势分析:")
            for trend in data:
                print(f"  {trend['metric']}:")
                print(f"    起始值: {trend['start_value']}")
                print(f"    当前值: {trend['current_value']}")
                print(f"    变化量: {trend['change']}")
                print(f"    变化率: {trend['change_rate']:.2f}%")
                print(f"    趋势: {trend['trend']}")
        
        return response
    
    def test_calorie_statistics(self, time_range: str = "month"):
        """测试卡路里统计"""
        url = f"{self.base_url}/api/analytics/calories"
        params = {
            "time_range": time_range,
            "include_chart": True
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"卡路里统计 (time_range={time_range})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n关键指标:")
            print(f"  总卡路里: {data.get('total_calories', 0):.0f}千卡")
            print(f"  平均/次: {data.get('average_per_workout', 0):.0f}千卡")
            print(f"  最大/次: {data.get('max_calories', 0):.0f}千卡")
        
        return response
    
    def test_volume_statistics(self, time_range: str = "month"):
        """测试训练容量统计"""
        url = f"{self.base_url}/api/analytics/volume"
        params = {
            "time_range": time_range,
            "include_chart": True
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"训练容量统计 (time_range={time_range})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n关键指标:")
            print(f"  总容量: {data.get('total_volume', 0):.0f}kg")
            print(f"  平均/次: {data.get('average_per_workout', 0):.0f}kg")
            print(f"  肌群分布: {data.get('by_muscle_group', {})}")
        
        return response
    
    def test_achievement_summary(self):
        """测试成就汇总"""
        url = f"{self.base_url}/api/analytics/achievements"
        
        response = requests.get(url, headers=self.headers)
        self._print_response("成就汇总", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n成就统计:")
            print(f"  总成就数: {data.get('total_achievements', 0)}")
            print(f"  已解锁: {data.get('unlocked_count', 0)}")
            print(f"  解锁率: {data.get('unlock_rate', 0):.1f}%")
            print(f"  总分: {data.get('total_points', 0)}")
            print(f"  已获得: {data.get('earned_points', 0)}")
            print(f"  分类统计: {data.get('by_category', {})}")
            print(f"  稀有度统计: {data.get('by_rarity', {})}")
        
        return response
    
    def test_dashboard(self, time_range: str = "week", include_charts: bool = True):
        """测试综合仪表盘"""
        url = f"{self.base_url}/api/analytics/dashboard"
        params = {
            "time_range": time_range,
            "include_charts": include_charts
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"综合仪表盘 (time_range={time_range})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n仪表盘概览:")
            print(f"  时间范围: {data.get('overview', {}).get('time_range')}")
            print(f"  训练次数: {data.get('overview', {}).get('workout_count')}")
            
            print(f"\n频率数据:")
            freq = data.get('frequency', {})
            print(f"  总次数: {freq.get('total_workouts', 0)}")
            print(f"  周平均: {freq.get('average_per_week', 0):.1f}")
            print(f"  连续天数: {freq.get('current_streak', 0)}")
            
            print(f"\n时长数据:")
            dur = data.get('duration', {})
            print(f"  总时长: {dur.get('total_duration_formatted', 'N/A')}")
            print(f"  平均时长: {dur.get('average_duration_formatted', 'N/A')}")
            
            print(f"\n卡路里数据:")
            cal = data.get('calories', {})
            print(f"  总卡路里: {cal.get('total_calories', 0):.0f}")
            print(f"  平均/次: {cal.get('average_per_workout', 0):.0f}")
        
        return response
    
    def test_leaderboard(self, metric: str = "workouts", time_range: str = "month", 
                        limit: int = 10, scope: str = "global"):
        """测试排行榜"""
        url = f"{self.base_url}/api/analytics/leaderboard"
        params = {
            "metric": metric,
            "time_range": time_range,
            "limit": limit,
            "scope": scope
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        self._print_response(f"排行榜 (metric={metric}, scope={scope})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n排行榜信息:")
            print(f"  指标: {data.get('metric')}")
            print(f"  时间范围: {data.get('time_range')}")
            print(f"  参与人数: {data.get('total_participants', 0)}")
            
            print(f"\n排名:")
            for entry in data.get('rankings', []):
                badge = entry.get('badge', '')
                print(f"  {badge} #{entry['rank']} - {entry['nickname']} ({entry['username']}): {entry['formatted_value']}")
            
            current = data.get('current_user_rank')
            if current:
                print(f"\n当前用户排名:")
                print(f"  #{current['rank']} - {current['formatted_value']}")
        
        return response
    
    def test_comparison(self, user_ids: List[int], metrics: List[str], time_range: str = "month"):
        """测试用户对比"""
        url = f"{self.base_url}/api/analytics/comparison"
        payload = {
            "user_ids": user_ids,
            "metrics": metrics,
            "time_range": time_range
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        self._print_response(f"用户对比 (users={len(user_ids)}, metrics={len(metrics)})", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n对比信息:")
            print(f"  时间范围: {data.get('time_range')}")
            print(f"  对比指标: {data.get('metrics')}")
            
            print(f"\n用户数据:")
            for user in data.get('users', []):
                print(f"  {user['nickname']} ({user['username']}):")
                for metric, value in user['metrics'].items():
                    print(f"    {metric}: {value}")
        
        return response
    
    def test_overview(self):
        """测试数据概览"""
        url = f"{self.base_url}/api/analytics/overview"
        
        response = requests.get(url, headers=self.headers)
        self._print_response("数据概览", response)
        
        if response.status_code == 200:
            data = response.json()['data']
            print(f"\n本周数据:")
            week = data.get('this_week', {})
            print(f"  训练次数: {week.get('workouts', 0)}")
            print(f"  训练时长: {week.get('duration', 0)}秒")
            print(f"  卡路里: {week.get('calories', 0):.0f}")
            print(f"  连续天数: {week.get('streak', 0)}")
            
            print(f"\n本月数据:")
            month = data.get('this_month', {})
            print(f"  训练次数: {month.get('workouts', 0)}")
            print(f"  训练时长: {month.get('duration', 0)}秒")
            print(f"  卡路里: {month.get('calories', 0):.0f}")
            print(f"  训练频率: {month.get('frequency_rate', 0):.1f}%")
            
            print(f"\n成就数据:")
            ach = data.get('achievements', {})
            print(f"  总成就: {ach.get('total', 0)}")
            print(f"  已解锁: {ach.get('unlocked', 0)}")
            print(f"  成就分: {ach.get('points', 0)}")
        
        return response
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("开始运行所有数据分析API测试")
        print("="*60)
        
        tests = [
            ("数据概览", lambda: self.test_overview()),
            ("训练频率统计", lambda: self.test_frequency_statistics("month")),
            ("训练时长统计", lambda: self.test_duration_statistics("month")),
            ("力量进步分析", lambda: self.test_strength_progress(time_range="all")),
            ("身体数据趋势", lambda: self.test_body_trends("weight", "month")),
            ("卡路里统计", lambda: self.test_calorie_statistics("month")),
            ("训练容量统计", lambda: self.test_volume_statistics("month")),
            ("成就汇总", lambda: self.test_achievement_summary()),
            ("综合仪表盘", lambda: self.test_dashboard("week")),
            ("排行榜-训练次数", lambda: self.test_leaderboard("workouts", "month", 10, "global")),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                response = test_func()
                status = "✓ 成功" if response.status_code == 200 else f"✗ 失败({response.status_code})"
                results.append((name, status, response.elapsed.total_seconds()))
            except Exception as e:
                results.append((name, f"✗ 异常: {str(e)}", 0))
        
        # 打印测试汇总
        print("\n" + "="*60)
        print("测试结果汇总")
        print("="*60)
        for name, status, elapsed in results:
            print(f"{name:20s} {status:20s} {elapsed:.3f}s")
        
        success_count = sum(1 for _, s, _ in results if "成功" in s)
        print(f"\n总计: {len(results)}个测试, {success_count}个成功")


def interactive_menu():
    """交互式测试菜单"""
    print("\n" + "="*60)
    print("Keep健身 - 数据分析API交互式测试工具")
    print("="*60)
    
    # 初始化
    base_url = input("\n请输入API地址 (默认: http://localhost:5000): ").strip()
    if not base_url:
        base_url = "http://localhost:5000"
    
    token = input("请输入认证Token: ").strip()
    
    tester = AnalyticsAPITester(base_url, token)
    
    while True:
        print("\n" + "-"*60)
        print("请选择测试项目:")
        print("  1. 数据概览")
        print("  2. 训练频率统计")
        print("  3. 训练时长统计")
        print("  4. 力量进步分析")
        print("  5. 身体数据趋势")
        print("  6. 卡路里统计")
        print("  7. 训练容量统计")
        print("  8. 成就汇总")
        print("  9. 综合仪表盘")
        print(" 10. 排行榜")
        print(" 11. 用户对比")
        print(" 12. 运行所有测试")
        print("  0. 退出")
        print("-"*60)
        
        choice = input("请输入选项 (0-12): ").strip()
        
        if choice == "0":
            print("测试结束!")
            break
        elif choice == "1":
            tester.test_overview()
        elif choice == "2":
            time_range = input("时间范围 (week/month/quarter/year/all, 默认:month): ").strip() or "month"
            tester.test_frequency_statistics(time_range)
        elif choice == "3":
            time_range = input("时间范围 (默认:month): ").strip() or "month"
            tester.test_duration_statistics(time_range)
        elif choice == "4":
            exercise_id = input("运动ID (留空表示所有): ").strip()
            exercise_id = int(exercise_id) if exercise_id else None
            time_range = input("时间范围 (默认:all): ").strip() or "all"
            tester.test_strength_progress(exercise_id, time_range)
        elif choice == "5":
            metrics = input("指标 (如:weight,body_fat, 默认:weight): ").strip() or "weight"
            time_range = input("时间范围 (默认:month): ").strip() or "month"
            tester.test_body_trends(metrics, time_range)
        elif choice == "6":
            time_range = input("时间范围 (默认:month): ").strip() or "month"
            tester.test_calorie_statistics(time_range)
        elif choice == "7":
            time_range = input("时间范围 (默认:month): ").strip() or "month"
            tester.test_volume_statistics(time_range)
        elif choice == "8":
            tester.test_achievement_summary()
        elif choice == "9":
            time_range = input("时间范围 (默认:week): ").strip() or "week"
            tester.test_dashboard(time_range)
        elif choice == "10":
            metric = input("排名指标 (workouts/duration/calories/volume/achievements, 默认:workouts): ").strip() or "workouts"
            time_range = input("时间范围 (默认:month): ").strip() or "month"
            limit = input("返回数量 (默认:10): ").strip()
            limit = int(limit) if limit else 10
            scope = input("范围 (global/friends/following, 默认:global): ").strip() or "global"
            tester.test_leaderboard(metric, time_range, limit, scope)
        elif choice == "11":
            user_ids_str = input("用户IDs (逗号分隔,如:1,2,3): ").strip()
            user_ids = [int(x.strip()) for x in user_ids_str.split(",")]
            metrics_str = input("对比指标 (逗号分隔,如:workouts,duration): ").strip()
            metrics = [x.strip() for x in metrics_str.split(",")]
            time_range = input("时间范围 (默认:month): ").strip() or "month"
            tester.test_comparison(user_ids, metrics, time_range)
        elif choice == "12":
            tester.run_all_tests()
        else:
            print("无效选项,请重新输入")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == "--all":
            token = sys.argv[2] if len(sys.argv) > 2 else None
            tester = AnalyticsAPITester(token=token)
            tester.run_all_tests()
        else:
            print("用法: python test_analytics.py [--all] [token]")
    else:
        # 交互式模式
        interactive_menu()
