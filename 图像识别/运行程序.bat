@echo off
chcp 65001 >nul
echo.
echo ========================================
echo      人脸识别应用程序 启动器
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查项目文件...
if not exist "图像识别.sln" (
    echo ❌ 错误：找不到项目文件
    pause
    exit /b 1
)
echo ✅ 项目文件检查完成

echo.
echo [2/4] 检查OpenCV环境...
if "%OPENCV_DIR%"=="" (
    echo ⚠️  警告：OPENCV_DIR环境变量未设置
    echo    请先配置OpenCV环境变量
    echo.
    echo    设置方法：
    echo    1. 下载OpenCV: https://opencv.org/releases/
    echo    2. 解压到C:\opencv
    echo    3. 设置环境变量OPENCV_DIR=C:\opencv\build
    echo    4. 添加C:\opencv\build\x64\vc16\bin到PATH
    echo.
    set /p continue="是否继续尝试编译？(Y/N): "
    if /i not "%continue%"=="Y" exit /b 1
) else (
    echo ✅ OpenCV环境变量已设置: %OPENCV_DIR%
)

echo.
echo [3/4] 尝试编译项目...

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
echo    请使用以下方法之一：
echo.
echo    方法1: 打开Visual Studio 2022
echo           文件 → 打开 → 项目/解决方案 → 选择图像识别.sln
echo           然后按F5运行
echo.
echo    方法2: 安装Visual Studio 2022 Community (免费)
echo           下载地址: https://visualstudio.microsoft.com/zh-hans/
echo.
pause
exit /b 1

:found_vs
echo ✅ 找到Visual Studio: %vs_path%

:: 设置VS环境并编译
call "%vs_path%\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1

echo    正在编译...
MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64 /v:minimal /nologo

if %ERRORLEVEL% equ 0 (
    echo ✅ 编译成功！
) else (
    echo ❌ 编译失败
    echo    请检查错误信息或使用Visual Studio打开项目进行调试
    pause
    exit /b 1
)

echo.
echo [4/4] 启动应用程序...

set "exe_path=x64\Debug\图像识别.exe"
if exist "%exe_path%" (
    echo ✅ 启动程序: %exe_path%
    echo.
    echo ========================================
    echo      应用程序使用说明
    echo ========================================
    echo  1. 点击"开始摄像头"启动视频
    echo  2. 输入姓名后点击"添加人脸"录入
    echo  3. 点击"识别人脸"进行识别
    echo  4. 可保存/加载训练数据
    echo ========================================
    echo.
    start "" "%exe_path%"
    echo 程序已启动！如有问题请查看控制台输出。
) else (
    echo ❌ 错误：找不到可执行文件
    echo    编译可能未完全成功
)

echo.
pause
