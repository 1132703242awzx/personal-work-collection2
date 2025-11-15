@echo off
REM 聚氨酯分子结构绘制程序启动脚本
REM Quick Start Script for Polyurethane Molecular Structure Visualization

echo.
echo ===================================================================
echo            聚氨酯分子结构绘制程序
echo        Polyurethane Molecular Structure Visualization
echo ===================================================================
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未找到，请先安装Python！
    pause
    exit /b 1
)

echo ✓ Python已找到

REM 检查是否需要安装依赖
echo.
echo 正在检查依赖库...

python -c "import rdkit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  RDKit未安装，正在安装...
    python -m pip install rdkit-pypi
    if %errorlevel% neq 0 (
        echo ❌ RDKit安装失败！
        pause
        exit /b 1
    )
)

python -c "import matplotlib" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Matplotlib未安装，正在安装...
    python -m pip install matplotlib
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Pillow未安装，正在安装...
    python -m pip install pillow
)

REM 检查NumPy版本
python -c "import numpy; print('NumPy版本:', numpy.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  NumPy问题，正在修复...
    python -m pip install "numpy<2"
)

echo.
echo ✓ 所有依赖检查完成
echo.

REM 运行程序
echo 启动聚氨酯分子结构绘制程序...
echo.

python "聚氨酯_完整版.py"

echo.
echo ===================================================================
echo 程序执行完成！生成的图像文件在当前目录中。
echo ===================================================================
echo.
pause
