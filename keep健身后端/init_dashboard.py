"""
Keep健身仪表盘 - 数据库初始化和测试数据生成脚本
"""
from app_dashboard import create_app
from dashboard_models import db, User, WorkoutRecord, BodyRecord
from datetime import datetime, timedelta
import random

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("  Keep健身仪表盘 - 数据库初始化")
        print("=" * 60)
        
        # 删除所有表
        print("\n[1/4] 删除现有表...")
        db.drop_all()
        print("✓ 已删除所有表")
        
        # 创建所有表
        print("\n[2/4] 创建数据表...")
        db.create_all()
        print("✓ 数据表创建成功")
        
        # 创建测试用户
        print("\n[3/4] 创建测试用户...")
        test_user = User(
            username='demo',
            email='demo@keep.com',
            nickname='演示用户',
            gender='male',
            birth_date=datetime(1995, 5, 15).date(),
            height=175.0
        )
        test_user.set_password('123456')
        
        db.session.add(test_user)
        db.session.commit()
        print("✓ 测试用户创建成功")
        print(f"  用户名: demo")
        print(f"  密码: 123456")
        
        # 创建测试数据
        print("\n[4/4] 生成测试数据...")
        
        # 生成运动记录 (过去30天)
        workout_types = ['running', 'cycling', 'swimming', 'strength', 'yoga']
        workout_names = {
            'running': ['晨跑', '夜跑', '操场跑', '公园跑'],
            'cycling': ['骑行', '室内骑行', '山地骑行'],
            'swimming': ['自由泳', '蛙泳', '仰泳'],
            'strength': ['胸肌训练', '腿部训练', '背部训练', '全身训练'],
            'yoga': ['瑜伽', '拉伸', '冥想']
        }
        difficulties = ['easy', 'medium', 'hard']
        
        for i in range(30):
            date = datetime.today().date() - timedelta(days=random.randint(0, 29))
            workout_type = random.choice(workout_types)
            
            record = WorkoutRecord(
                user_id=test_user.id,
                workout_type=workout_type,
                workout_name=random.choice(workout_names[workout_type]),
                workout_date=date,
                duration=random.randint(20, 90),
                calories=random.randint(100, 600),
                distance=round(random.uniform(2, 10), 1) if workout_type in ['running', 'cycling'] else None,
                difficulty=random.choice(difficulties),
                notes='这是一次很棒的训练!'
            )
            db.session.add(record)
        
        print(f"✓ 已生成 30 条运动记录")
        
        # 生成身体数据记录 (过去60天,每5天一次)
        base_weight = 70.0
        for i in range(12):
            date = datetime.today().date() - timedelta(days=i*5)
            weight = base_weight + random.uniform(-2, 1)
            
            record = BodyRecord(
                user_id=test_user.id,
                record_date=date,
                weight=round(weight, 1),
                body_fat=round(random.uniform(15, 20), 1),
                notes='定期测量'
            )
            db.session.add(record)
        
        print(f"✓ 已生成 12 条身体数据记录")
        
        db.session.commit()
        
        print("\n" + "=" * 60)
        print("  ✓ 数据库初始化完成!")
        print("=" * 60)
        print("\n现在可以启动应用:")
        print("  python app_dashboard.py")
        print("\n然后访问:")
        print("  http://localhost:5000")
        print("\n使用以下账号登录:")
        print("  用户名: demo")
        print("  密码: 123456")
        print("")


if __name__ == '__main__':
    init_database()
