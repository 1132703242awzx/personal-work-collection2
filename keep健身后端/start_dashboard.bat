@echo off
chcp 65001 >nul
echo ============================================================
echo   Keep健身仪表盘 - 快速启动脚本
echo ============================================================
echo.

REM 检查虚拟环境
if not exist "venv\" (
    echo [1/3] 创建虚拟环境...
    python -m venv venv
    echo ✓ 虚拟环境创建成功
) else (
    echo [1/3] 虚拟环境已存在
)

REM 激活虚拟环境并安装依赖
echo.
echo [2/3] 安装依赖包...
call venv\Scripts\activate.bat
pip install -r requirements_dashboard.txt -q
echo ✓ 依赖包安装完成

REM 初始化数据库
echo.
echo [3/3] 初始化数据库...
python init_dashboard.py

echo.
echo ============================================================
echo   按任意键启动Keep健身仪表盘...
echo ============================================================
pause >nul

echo.
echo 正在启动服务器...
echo 访问地址: http://localhost:5000
echo 测试账号: demo / 123456
echo 按 Ctrl+C 停止服务器
echo.

python app_dashboard.py
