@echo off
echo ============================================================
echo   启动 Keep健身后端服务器
echo ============================================================
echo.
echo 服务器地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.
cd /d "%~dp0"
D:\keep健身后端\venv\Scripts\python.exe app.py
pause
