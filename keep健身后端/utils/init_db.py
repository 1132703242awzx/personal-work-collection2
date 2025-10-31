"""
数据库初始化脚本
用于创建数据库表和初始数据
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from config.database import engine, Base
from models import *  # 导入所有模型


def create_tables():
    """创建所有数据表"""
    print("开始创建数据表...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ 数据表创建成功!")
        
        # 打印所有创建的表
        print("\n创建的表:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"✗ 数据表创建失败: {str(e)}")
        raise


def drop_tables():
    """删除所有数据表"""
    print("警告: 即将删除所有数据表!")
    confirm = input("确认删除? (yes/no): ")
    
    if confirm.lower() == 'yes':
        try:
            Base.metadata.drop_all(bind=engine)
            print("✓ 数据表删除成功!")
        except Exception as e:
            print(f"✗ 数据表删除失败: {str(e)}")
            raise
    else:
        print("已取消操作")


def reset_database():
    """重置数据库（删除后重新创建）"""
    print("重置数据库...")
    drop_tables()
    create_tables()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库初始化工具')
    parser.add_argument('action', choices=['create', 'drop', 'reset'],
                       help='操作类型: create(创建表), drop(删除表), reset(重置)')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_tables()
    elif args.action == 'drop':
        drop_tables()
    elif args.action == 'reset':
        reset_database()
