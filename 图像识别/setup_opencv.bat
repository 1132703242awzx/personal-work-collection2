@echo off
echo 人脸识别应用程序环境设置
echo ===============================

echo.
echo 请确保已经安装了OpenCV 4.x
echo.

set /p OPENCV_PATH="请输入OpenCV安装路径 (例如: C:\opencv): "

if not exist "%OPENCV_PATH%" (
    echo 错误: 指定的路径不存在!
    pause
    exit /b 1
)

if not exist "%OPENCV_PATH%\build" (
    echo 错误: 在指定路径下找不到build文件夹!
    pause
    exit /b 1
)

echo.
echo 正在设置环境变量...

:: 设置OPENCV_DIR环境变量
setx OPENCV_DIR "%OPENCV_PATH%\build"

:: 获取当前PATH
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "current_path=%%b"

:: 检查PATH中是否已包含OpenCV路径
echo %current_path% | findstr /i "%OPENCV_PATH%\build\x64\vc16\bin" >nul
if %errorlevel% neq 0 (
    echo 添加OpenCV bin目录到PATH...
    setx PATH "%current_path%;%OPENCV_PATH%\build\x64\vc16\bin"
) else (
    echo OpenCV bin目录已在PATH中
)

echo.
echo 环境变量设置完成!
echo.
echo 请重新启动Visual Studio以使环境变量生效。
echo.
pause
