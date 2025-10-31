#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keep健身后端 - 一键安装和启动脚本
自动检测MySQL、初始化数据库、启动服务
"""

import os
import sys
import subprocess
import time
import pymysql
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🏋️  Keep健身后端 - 一键启动脚本")
    print("=" * 60)
    print()

def check_mysql_connection():
    """检查MySQL连接"""
    print("📊 检查MySQL连接...")
    
    configs = [
        {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': ''},
        {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'root'},
        {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'password'},
        {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '123456'},
    ]
    
    for config in configs:
        try:
            conn = pymysql.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                connect_timeout=3
            )
            conn.close()
            print(f"✅ MySQL连接成功! (用户: {config['user']}, 密码: {'*' * len(config['password']) if config['password'] else '(空)'})")
            return config
        except pymysql.err.OperationalError as e:
            if "Can't connect" in str(e) or "Connection refused" in str(e):
                continue
            elif "Access denied" in str(e):
                continue
        except Exception as e:
            continue
    
    print("❌ 无法连接到MySQL!")
    print()
    print("请确保:")
    print("  1. MySQL已安装并正在运行")
    print("  2. MySQL服务已启动 (Windows: net start mysql)")
    print("  3. 检查MySQL端口是否为3306")
    print()
    
    # 尝试手动输入
    print("或者手动输入MySQL连接信息:")
    try:
        manual_host = input("MySQL主机 [localhost]: ").strip() or 'localhost'
        manual_port = int(input("MySQL端口 [3306]: ").strip() or '3306')
        manual_user = input("MySQL用户 [root]: ").strip() or 'root'
        manual_password = input("MySQL密码: ").strip()
        
        conn = pymysql.connect(
            host=manual_host,
            port=manual_port,
            user=manual_user,
            password=manual_password,
            connect_timeout=5
        )
        conn.close()
        print("✅ 连接成功!")
        return {'host': manual_host, 'port': manual_port, 'user': manual_user, 'password': manual_password}
    except:
        print("❌ 手动连接也失败了")
        return None

def init_database(config):
    """初始化数据库"""
    print()
    print("📦 初始化数据库...")
    
    try:
        # 连接MySQL
        conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # 读取SQL脚本
        sql_file = Path(__file__).parent / 'init_database.sql'
        if not sql_file.exists():
            print(f"❌ SQL脚本不存在: {sql_file}")
            return False
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割SQL语句并执行
        statements = []
        current_statement = []
        
        for line in sql_content.split('\n'):
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith('--'):
                continue
            
            current_statement.append(line)
            
            # 如果遇到分号,执行语句
            if line.endswith(';'):
                statement = ' '.join(current_statement)
                statements.append(statement)
                current_statement = []
        
        print(f"   共{len(statements)}条SQL语句")
        
        success_count = 0
        for i, statement in enumerate(statements, 1):
            try:
                cursor.execute(statement)
                success_count += 1
                if i % 10 == 0:
                    print(f"   执行进度: {i}/{len(statements)}")
            except Exception as e:
                if "already exists" not in str(e).lower():
                    print(f"   警告: 第{i}条语句执行失败: {str(e)[:100]}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ 数据库初始化完成! (成功: {success_count}/{len(statements)})")
        
        # 更新环境变量中的数据库密码
        db_url = f"mysql+pymysql://root:{config['password']}@localhost:3306/keep_fitness?charset=utf8mb4"
        os.environ['DATABASE_URL'] = db_url
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

def check_database_exists(config):
    """检查数据库是否已存在"""
    try:
        conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password']
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE 'keep_fitness'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except:
        return False

def start_flask_app():
    """启动Flask应用"""
    print()
    print("🚀 启动Keep健身后端...")
    print()
    print("=" * 60)
    print()
    
    try:
        # 使用当前Python解释器启动app.py
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print()
        print("👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print_banner()
    
    # 1. 检查MySQL连接
    config = check_mysql_connection()
    if not config:
        print()
        print("请先安装并启动MySQL,然后重新运行此脚本")
        print()
        input("按回车键退出...")
        sys.exit(1)
    
    # 2. 检查数据库是否存在
    if check_database_exists(config):
        print()
        print("✅ 数据库 'keep_fitness' 已存在")
        choice = input("是否重新初始化数据库? (会删除所有数据) [y/N]: ").strip().lower()
        if choice == 'y':
            if not init_database(config):
                print()
                input("按回车键退出...")
                sys.exit(1)
    else:
        # 3. 初始化数据库
        if not init_database(config):
            print()
            input("按回车键退出...")
            sys.exit(1)
    
    # 设置数据库URL环境变量
    db_url = f"mysql+pymysql://root:{config['password']}@localhost:3306/keep_fitness?charset=utf8mb4"
    os.environ['DATABASE_URL'] = db_url
    
    # 4. 启动Flask应用
    start_flask_app()

if __name__ == '__main__':
    main()
