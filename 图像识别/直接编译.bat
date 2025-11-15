@echo off
chcp 65001 >nul
echo.
echo ========================================
echo      直接编译人脸识别项目
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 设置临时环境变量...
set "OPENCV_DIR=D:\opencv4.10_vs2022"
set "PATH=%PATH%;D:\opencv4.10_vs2022\x64\vc17\bin"
echo ✅ OpenCV环境已设置

echo.
echo [2/3] 查找并设置Visual Studio环境...

:: 查找Visual Studio
set "vs_path="
for %%i in (
    "C:\Program Files\Microsoft Visual Studio\2022\Community"
    "C:\Program Files\Microsoft Visual Studio\2022\Professional" 
    "C:\Program Files\Microsoft Visual Studio\2022\Enterprise"
    "C:\Program Files (x86)\Microsoft Visual Studio\2022\Community"
    "C:\Program Files (x86)\Microsoft Visual Studio\2022\Professional"
    "C:\Program Files (x86)\Microsoft Visual Studio\2022\Enterprise"
) do (
    if exist "%%~i\VC\Auxiliary\Build\vcvars64.bat" (
        set "vs_path=%%~i"
        goto :found_vs
    )
)

echo ❌ 错误：找不到Visual Studio 2022
echo    尝试使用开发人员命令提示符...
echo.
echo    请在"开发人员命令提示符"中运行以下命令：
echo    cd d:\图像识别
echo    set OPENCV_DIR=D:\opencv4.10_vs2022
echo    MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64
echo.
pause
exit /b 1

:found_vs
echo ✅ 找到Visual Studio: %vs_path%

:: 设置VS环境
call "%vs_path%\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1

if errorlevel 1 (
    echo ❌ 无法设置Visual Studio环境
    pause
    exit /b 1
)

echo.
echo [3/3] 编译项目...
echo    配置: Debug x64
echo    OpenCV: %OPENCV_DIR%

MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64 /v:minimal /nologo

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ 编译成功！
    echo.
    
    set "exe_path=x64\Debug\图像识别.exe"
    if exist "%exe_path%" (
        echo 🚀 启动应用程序...
        echo.
        start "" "%exe_path%"
        echo ✅ 人脸识别应用程序已启动！
        echo.
        echo 📱 使用说明：
        echo   1. 点击"开始摄像头"启动视频
        echo   2. 输入姓名后点击"添加人脸"
        echo   3. 点击"识别人脸"进行识别
        echo   4. 可保存/加载训练数据
    ) else (
        echo ❌ 找不到可执行文件: %exe_path%
    )
else (
    echo.
    echo ❌ 编译失败！错误代码: %ERRORLEVEL%
    echo.
    echo 可能的解决方案：
    echo 1. 检查OpenCV安装是否完整
    echo 2. 确认环境变量设置正确
    echo 3. 使用Visual Studio打开项目进行调试
)

echo.
pause
