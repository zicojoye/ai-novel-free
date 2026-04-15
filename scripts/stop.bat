@echo off
REM AI小说平台 - 停止服务脚本 (Windows)

echo ======================================
echo AI Novel Platform - 停止服务
echo ======================================
echo.

echo 正在查找Python进程...
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo list ^| findstr PID') do (
    echo 终止Python进程 PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo 正在查找Node.js进程...
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq node.exe" /fo list ^| findstr PID') do (
    echo 终止Node.js进程 PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo ======================================
echo ✓ 服务已停止
echo ======================================
echo.
timeout /t 2 /nobreak >nul
