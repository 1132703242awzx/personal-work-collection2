:: 人脸识别项目编译脚本
@echo off
chcp 65001 >nul
echo.
echo ========================================
echo        人脸识别项目编译器
echo ========================================
echo.

cd /d "d:\图像识别"

echo [1] 设置OpenCV环境变量...
set "OPENCV_DIR=D:\opencv4.10_vs2022"
set "PATH=%PATH%;D:\opencv4.10_vs2022\x64\vc17\bin"
echo ✅ OpenCV环境已配置

echo.
echo [2] 检查编译环境...

:: 尝试不同的Visual Studio版本
set "devenv_path="

:: Community版本
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe" (
    set "devenv_path=C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe"
    echo ✅ 找到Visual Studio 2022 Community
    goto :compile
)

:: Professional版本  
if exist "C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\devenv.exe" (
    set "devenv_path=C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\devenv.exe"
    echo ✅ 找到Visual Studio 2022 Professional
    goto :compile
)

:: Enterprise版本
if exist "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.exe" (
    set "devenv_path=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.exe"
    echo ✅ 找到Visual Studio 2022 Enterprise
    goto :compile
)

:: 如果都找不到，显示手动编译说明
echo ❌ 未找到Visual Studio 2022
echo.
echo 📋 手动编译步骤：
echo    1. 打开"开发人员命令提示符" (搜索Developer Command Prompt)
echo    2. 运行以下命令：
echo.
echo       cd "d:\图像识别"
echo       set OPENCV_DIR=D:\opencv4.10_vs2022
echo       set PATH=%%PATH%%;D:\opencv4.10_vs2022\x64\vc17\bin
echo       MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64
echo.
echo    3. 如果编译成功，运行：
echo       x64\Debug\图像识别.exe
echo.
goto :end

:compile
echo.
echo [3] 开始编译...
echo    配置: Debug x64
echo    使用: %devenv_path%

"%devenv_path%" 图像识别.sln /build "Debug|x64"

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ 编译成功！
    echo.
    if exist "x64\Debug\图像识别.exe" (
        echo 🚀 启动人脸识别应用...
        echo.
        echo 📱 功能说明：
        echo   • 开始摄像头：启动视频捕获
        echo   • 添加人脸：录入新的人脸数据
        echo   • 识别人脸：匹配已录入的人脸
        echo   • 保存数据：保存训练数据到文件
        echo   • 加载数据：从文件加载训练数据
        echo.
        start "" "x64\Debug\图像识别.exe"
        echo ✅ 应用程序已启动！
    ) else (
        echo ❌ 编译成功但找不到可执行文件
        echo    请检查输出目录：x64\Debug\
    )
) else (
    echo.
    echo ❌ 编译失败！
    echo.
    echo 🔧 可能的解决方案：
    echo    1. 确认OpenCV安装完整
    echo    2. 检查项目配置是否正确
    echo    3. 在Visual Studio中打开项目进行详细调试
    echo    4. 确认所有依赖库都存在
)

:end
echo.
pause
