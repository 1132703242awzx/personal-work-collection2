@echo off
chcp 65001 >nul
echo.
echo ========================================
echo      修复编译错误并重新构建
echo ========================================
echo.

cd /d "d:\图像识别"

echo [修复内容]
echo ✅ 添加 #include ^<algorithm^> 头文件
echo ✅ 使用 std::min 替代 min 函数
echo ✅ 解决 C3861 编译错误
echo.

echo [开始编译...]
echo 请在开发人员命令提示符中运行以下命令：
echo.
echo cd "d:\图像识别"
echo set OPENCV_DIR=D:\opencv4.10_vs2022
echo set PATH=%%PATH%%;D:\opencv4.10_vs2022\x64\vc17\bin
echo MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64
echo.
echo 编译成功后运行：
echo x64\Debug\图像识别.exe
echo.
pause
