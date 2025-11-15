@echo off
chcp 65001 >nul
echo.
echo ========================================
echo      开发人员命令提示符指南
echo ========================================
echo.
echo 请按照以下步骤操作：
echo.
echo 🔍 1. 找到开发人员命令提示符：
echo    - 按Win键，搜索"Developer Command Prompt"
echo    - 或搜索"开发人员命令提示符"
echo.
echo 📂 2. 在开发人员命令提示符中运行这些命令：
echo.
echo    cd "d:\图像识别"
echo    set OPENCV_DIR=D:\opencv4.10_vs2022
echo    set PATH=%%PATH%%;D:\opencv4.10_vs2022\x64\vc17\bin
echo    MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64
echo.
echo ✨ 3. 如果编译成功，运行：
echo    x64\Debug\图像识别.exe
echo.
echo 📝 提示：
echo    - 确保使用x64版本的开发人员命令提示符
echo    - 如果编译失败，请检查错误信息
echo.
pause
