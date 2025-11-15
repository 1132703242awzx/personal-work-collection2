@echo off
echo 编译人脸识别项目...
cd /d "d:\图像识别"

:: 设置Visual Studio环境
call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"

:: 编译项目
MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64

if %ERRORLEVEL% == 0 (
    echo 编译成功！
    echo 可执行文件位置: d:\图像识别\x64\Debug\图像识别.exe
) else (
    echo 编译失败，错误代码: %ERRORLEVEL%
)

pause
