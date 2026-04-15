@echo off
chcp 65001 >nul
echo ================================================
echo         AI Novel Platform - 停止服务
echo ================================================
echo.

echo 正在停止服务...
echo.

::: 杀掉所有Python进程（后端）
taskkill /f /im python.exe 2>nul
if %errorlevel%==0 (
    echo [OK] 后端服务已停止
) else (
    echo [INFO] 后端服务未运行
)

::: 杀掉所有Node进程（前端）
taskkill /f /im node.exe 2>nul
if %errorlevel%==0 (
    echo [OK] 前端服务已停止
) else (
    echo [INFO] 前端服务未运行
)

echo.
echo ================================================
echo 服务已停止
echo ================================================
echo.
pause
