@echo off
chcp 65001 >nul
title AI Novel Platform

cd /d "%~dp0"

echo ============================================================
echo   AI Novel Platform - 一键启动
echo ============================================================
echo.

:: ===== 启动后端 =====
echo [1/2] 启动后端服务 (http://localhost:8000)...
cd backend
start "AI Novel - Backend" cmd /k "chcp 65001 >nul && echo 后端启动中... && python -m uvicorn main:app --host 0.0.0.0 --port 8000 && pause"
cd ..

:: 等待后端启动
echo 等待后端初始化 (5秒)...
timeout /t 5 /nobreak >nul

:: ===== 启动前端 =====
echo [2/2] 启动前端服务 (http://localhost:3000)...
cd frontend
start "AI Novel - Frontend" cmd /k "chcp 65001 >nul && echo 前端启动中... && npm run dev && pause"
cd ..

echo.
echo ============================================================
echo   服务启动完成！
echo ============================================================
echo.
echo   前端界面:  http://localhost:3000
echo   后端 API:  http://localhost:8000
echo   API 文档:  http://localhost:8000/docs
echo   健康检查:  http://localhost:8000/health
echo.
echo   关闭对应窗口即可停止服务
echo.

set /p open="是否打开浏览器? (Y/N): "
if /i "%open%"=="Y" (
    timeout /t 3 /nobreak >nul
    start http://localhost:3000
)
