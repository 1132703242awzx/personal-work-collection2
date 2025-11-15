@echo off
chcp 65001 >nul
echo.
echo ========================================
echo        启动人脸识别应用程序
echo ========================================
echo.

cd /d "d:\图像识别"

echo [1] 检查可执行文件...
if not exist "x64\Debug\图像识别.exe" (
    echo ❌ 找不到可执行文件：x64\Debug\图像识别.exe
    echo    请先编译项目
    goto :end
)
echo ✅ 找到可执行文件

echo.
echo [2] 检查OpenCV DLL...
if not exist "x64\Debug\opencv_world4100d.dll" (
    echo 📋 复制OpenCV DLL文件...
    copy "D:\opencv4.10_vs2022\x64\vc17\bin\opencv_world4100d.dll" "x64\Debug\" >nul
    copy "D:\opencv4.10_vs2022\x64\vc17\bin\opencv_world4100.dll" "x64\Debug\" >nul
    echo ✅ OpenCV DLL已复制
) else (
    echo ✅ OpenCV DLL已存在
)

echo.
echo [3] 检查Haar级联文件...
if not exist "haarcascade_frontalface_alt.xml" (
    echo ❌ 找不到人脸检测模型文件
    echo    请确保haarcascade_frontalface_alt.xml在当前目录
    goto :end
)
echo ✅ 人脸检测模型文件已就绪

echo.
echo [4] 设置环境变量...
set "OPENCV_DIR=D:\opencv4.10_vs2022"
set "PATH=%PATH%;D:\opencv4.10_vs2022\x64\vc17\bin"
echo ✅ 环境变量已设置

echo.
echo [5] 启动应用程序...
echo.
echo 📱 人脸识别应用程序功能：
echo   • 开始摄像头：启动视频捕获
echo   • 添加人脸：输入姓名后录入新的人脸
echo   • 识别人脸：匹配已录入的人脸数据
echo   • 保存数据：保存训练数据到文件
echo   • 加载数据：从文件加载训练数据
echo.
echo 🚀 正在启动...

start "" "x64\Debug\图像识别.exe"

if %ERRORLEVEL% equ 0 (
    echo ✅ 应用程序已启动！
) else (
    echo ❌ 启动失败，错误代码：%ERRORLEVEL%
)

:end
echo.
pause
