@echo off
chcp 65001 >nul
echo.
echo ========================================
echo      图像质量优化修复版本
echo ========================================
echo.

cd /d "d:\图像识别"

echo 📋 修复内容：
echo   ✅ 设置摄像头标准分辨率 (640x480)
echo   ✅ 启用自动曝光和对焦
echo   ✅ 保持图像长宽比显示
echo   ✅ 优化颜色格式转换
echo   ✅ 减少显示延迟
echo   ✅ 添加人脸检测标识
echo.

echo [1] 检查编译状态...
if not exist "x64\Debug\图像识别.exe" (
    echo ❌ 需要重新编译项目
    echo.
    echo 📝 请在开发人员命令提示符中运行：
    echo    cd "d:\图像识别"
    echo    set OPENCV_DIR=D:\opencv4.10_vs2022
    echo    set PATH=%%PATH%%;D:\opencv4.10_vs2022\x64\vc17\bin
    echo    MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64
    echo.
    goto :end
)

echo ✅ 找到可执行文件

echo.
echo [2] 检查所需文件...
if not exist "x64\Debug\opencv_world4100d.dll" (
    echo 📋 复制OpenCV DLL...
    copy "D:\opencv4.10_vs2022\x64\vc17\bin\opencv_world4100d.dll" "x64\Debug\" >nul
    copy "D:\opencv4.10_vs2022\x64\vc17\bin\opencv_world4100.dll" "x64\Debug\" >nul
    echo ✅ DLL文件已复制
) else (
    echo ✅ DLL文件已存在
)

if not exist "haarcascade_frontalface_alt.xml" (
    echo ❌ 缺少人脸检测模型文件
    goto :end
)
echo ✅ 模型文件已就绪

echo.
echo [3] 启动优化版本...
echo.
echo 🎯 新功能特性：
echo   • 标准分辨率：640x480，减少失真
echo   • 自动曝光：改善图像质量
echo   • 保持比例：避免拉伸变形
echo   • 实时检测：绿色框标记人脸
echo   • 低延迟：减少视频滞后
echo.
echo 📱 使用说明：
echo   1. 点击"开始摄像头"
echo   2. 现在图像应该清晰无失真
echo   3. 检测到人脸时会显示绿色方框
echo   4. 可以正常使用所有功能
echo.

set "OPENCV_DIR=D:\opencv4.10_vs2022"
set "PATH=%PATH%;D:\opencv4.10_vs2022\x64\vc17\bin"

echo 🚀 启动应用程序...
start "" "x64\Debug\图像识别.exe"

if %ERRORLEVEL% equ 0 (
    echo ✅ 人脸识别应用程序已启动！
    echo.
    echo 💡 提示：
    echo   - 如果图像仍有问题，请检查摄像头驱动
    echo   - 确保光线充足，提高检测精度
    echo   - 面部正对摄像头，距离适中
) else (
    echo ❌ 启动失败
)

:end
echo.
pause
