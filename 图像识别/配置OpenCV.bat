@echo off
chcp 65001 >nul
echo.
echo ========================================
echo     OpenCV 环境变量配置工具
echo ========================================
echo.

echo 请选择您的OpenCV安装路径：
echo.
echo [1] C:\opencv
echo [2] D:\opencv  
echo [3] 自定义路径
echo [4] 我已经安装了opencv4.10_vs2022
echo.
set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" set "opencv_root=C:\opencv"
if "%choice%"=="2" set "opencv_root=D:\opencv"
if "%choice%"=="4" (
    echo.
    echo 正在查找opencv4.10_vs2022安装位置...
    
    :: 检查常见安装路径
    for %%p in (
        "C:\opencv4.10_vs2022"
        "D:\opencv4.10_vs2022"
        "C:\Program Files\opencv4.10_vs2022"
        "D:\Program Files\opencv4.10_vs2022"
        "C:\opencv"
        "D:\opencv"
    ) do (
        if exist "%%p\build" (
            set "opencv_root=%%p"
            echo ✅ 找到OpenCV安装位置: %%p
            goto :found_opencv
        )
    )
    
    echo ❌ 未找到opencv4.10_vs2022安装位置
    set /p opencv_root="请手动输入OpenCV安装路径: "
    goto :found_opencv
)

if "%choice%"=="3" (
    set /p opencv_root="请输入OpenCV安装路径: "
)

:found_opencv
if "%opencv_root%"=="" (
    echo ❌ 错误：未指定OpenCV路径
    pause
    exit /b 1
)

set "opencv_build=%opencv_root%\build"
if not exist "%opencv_build%" (
    echo ❌ 错误：找不到build目录: %opencv_build%
    echo    请确保OpenCV已正确安装
    pause
    exit /b 1
)

echo.
echo 正在配置环境变量...

:: 设置OPENCV_DIR
setx OPENCV_DIR "%opencv_build%" >nul
echo ✅ 设置 OPENCV_DIR = %opencv_build%

:: 检查并添加到PATH
set "opencv_bin=%opencv_build%\x64\vc16\bin"
if exist "%opencv_bin%" (
    :: 获取当前PATH
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "current_path=%%b"
    
    :: 检查是否已在PATH中
    echo %current_path% | findstr /i "%opencv_bin%" >nul
    if errorlevel 1 (
        setx PATH "%current_path%;%opencv_bin%" >nul
        echo ✅ 添加到PATH: %opencv_bin%
    ) else (
        echo ✅ PATH中已包含OpenCV路径
    )
) else (
    echo ❌ 警告：找不到bin目录: %opencv_bin%
)

echo.
echo ========================================
echo     环境变量配置完成！
echo ========================================
echo.
echo 重要提示：
echo 1. 请重新启动命令提示符或PowerShell
echo 2. 重新启动Visual Studio (如果已打开)
echo 3. 现在可以尝试编译和运行程序了
echo.
echo 配置信息：
echo OPENCV_DIR = %opencv_build%
echo BIN路径    = %opencv_bin%
echo.
pause
