#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Keep健身后端 - 快速启动脚本
用于检查环境、初始化数据库并启动服务
"""

import os
import sys
import subprocess
import pymysql
from sqlalchemy import create_engine, text

# 数据库配置
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'keep_fitness'

def print_step(msg):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")

def check_mysql_connection():
    """检查MySQL连接"""
    print_step("步骤1: 检查MySQL连接")
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ MySQL服务器连接成功!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 无法连接到MySQL服务器: {e}")
        print("\n请确保:")
        print("1. MySQL服务器已安装并运行")
        print("2. 连接信息正确 (host=localhost, port=3306, user=root)")
        print("3. 如果密码不是'password',请修改config/config.py")
        return False

def create_database():
    """创建数据库"""
    print_step("步骤2: 创建数据库")
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cursor.execute(f"""
            CREATE DATABASE {DB_NAME} 
            DEFAULT CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        print(f"✅ 数据库 '{DB_NAME}' 创建成功!")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False

def init_tables():
    """初始化数据表"""
    print_step("步骤3: 初始化数据表")
    try:
        # 使用SQLAlchemy创建所有表
        from config.database import Base, engine
        from models import auth, user, training, workout, course, course_extended
        from models import social, body_data, feed, notification
        
        print("正在创建数据表...")
        Base.metadata.create_all(bind=engine)
        print("✅ 所有数据表创建成功!")
        
        # 显示创建的表
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"\n已创建 {len(tables)} 个表:")
            for i, table in enumerate(tables, 1):
                print(f"  {i}. {table}")
        
        return True
    except Exception as e:
        print(f"❌ 创建数据表失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_test_data():
    """创建测试数据"""
    print_step("步骤4: 创建测试数据 (可选)")
    try:
        from config.database import SessionLocal
        from models.user import User, UserProfile
        from datetime import datetime
        
        db = SessionLocal()
        
        # 检查是否已有用户
        existing_user = db.query(User).first()
        if existing_user:
            print("⚠️  数据库中已有数据,跳过测试数据创建")
            db.close()
            return True
        
        # 创建测试用户
        test_user = User(
            username='testuser',
            email='test@example.com',
            phone='13800138000',
            password_hash='$2b$12$test_hash',  # 实际应用中需要正确的hash
            status='active'
        )
        db.add(test_user)
        db.flush()
        
        # 创建用户资料
        test_profile = UserProfile(
            user_id=test_user.id,
            nickname='测试用户',
            gender='male',
            height=175,
            weight=70,
            age=25
        )
        db.add(test_profile)
        
        db.commit()
        print("✅ 测试数据创建成功!")
        print(f"   测试账号: testuser")
        print(f"   测试邮箱: test@example.com")
        
        db.close()
        return True
    except Exception as e:
        print(f"⚠️  创建测试数据失败: {e}")
        return False

def start_server():
    """启动Flask服务器"""
    print_step("步骤5: 启动Keep健身后端服务")
    print("正在启动服务器...")
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器\n")
    
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("  🏋️  Keep健身后端 - 快速启动脚本")
    print("="*60)
    
    # 检查MySQL连接
    if not check_mysql_connection():
        print("\n❌ 初始化失败: MySQL未连接")
        print("\n请先安装并启动MySQL数据库服务器")
        print("或运行: docker-compose up -d (如果使用Docker)")
        return
    
    # 创建数据库
    if not create_database():
        print("\n❌ 初始化失败: 无法创建数据库")
        return
    
    # 初始化表结构
    if not init_tables():
        print("\n❌ 初始化失败: 无法创建数据表")
        return
    
    # 创建测试数据
    create_test_data()
    
    # 启动服务器
    print("\n" + "="*60)
    print("  ✅ 数据库初始化完成!")
    print("="*60)
    
    input("\n按回车键启动服务器...")
    start_server()

if __name__ == '__main__':
    main()
