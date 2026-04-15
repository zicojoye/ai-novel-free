@echo off
chcp 65001 >nul
cd /d "%~dp0\backend"

echo ================================================
echo           修复缺失的Python依赖
echo ================================================
echo.

echo 正在检查并安装 python-dotenv...
python -m pip install python-dotenv

if errorlevel 1 (
    echo [错误] 安装失败
    pause
    exit /b 1
)

echo [OK] python-dotenv 安装完成
echo.
echo 现在可以运行启动.bat
echo.
pause
