"""
Keep健身后端启动诊断脚本
检查所有依赖和配置是否正常
"""
import sys
print("=" * 60)
print("Keep健身后端启动诊断")
print("=" * 60)

# 1. 检查Python版本
print(f"\n1. Python版本: {sys.version}")
print(f"   Python路径: {sys.executable}")

# 2. 检查关键依赖
print("\n2. 检查关键依赖:")
try:
    import flask
    print(f"   ✓ Flask {flask.__version__}")
except Exception as e:
    print(f"   ✗ Flask: {e}")

try:
    import sqlalchemy
    print(f"   ✓ SQLAlchemy {sqlalchemy.__version__}")
except Exception as e:
    print(f"   ✗ SQLAlchemy: {e}")

try:
    import pydantic
    print(f"   ✓ Pydantic {pydantic.__version__}")
except Exception as e:
    print(f"   ✗ Pydantic: {e}")

try:
    import pymysql
    print(f"   ✓ PyMySQL {pymysql.__version__}")
except Exception as e:
    print(f"   ✗ PyMySQL: {e}")

# 3. 检查环境变量
print("\n3. 检查环境变量:")
import os
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv('DATABASE_URL', '未配置')
print(f"   DATABASE_URL: {db_url[:50]}..." if len(db_url) > 50 else f"   DATABASE_URL: {db_url}")
print(f"   FLASK_ENV: {os.getenv('FLASK_ENV', '未配置')}")
print(f"   SECRET_KEY: {'已配置' if os.getenv('SECRET_KEY') else '未配置'}")

# 4. 测试数据库连接
print("\n4. 测试数据库连接:")
try:
    from sqlalchemy import create_engine
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1"))
            print("   ✓ 数据库连接成功")
    else:
        print("   ⚠ DATABASE_URL未配置")
except Exception as e:
    print(f"   ✗ 数据库连接失败: {e}")

# 5. 测试导入主应用
print("\n5. 测试导入主应用:")
try:
    from app import create_app
    print("   ✓ 应用模块导入成功")
    
    # 尝试创建应用实例
    try:
        app = create_app('development')
        print("   ✓ 应用实例创建成功")
        print(f"   - 已注册蓝图数量: {len(app.blueprints)}")
        print(f"   - 已注册路由数量: {len(list(app.url_map.iter_rules()))}")
    except Exception as e:
        print(f"   ✗ 应用实例创建失败: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"   ✗ 应用模块导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)
