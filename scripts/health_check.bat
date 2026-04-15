@echo off
REM AI小说平台 - 快速健康检查 (Windows)

echo ======================================
echo AI Novel Platform - 健康检查
echo ======================================
echo.

REM 检查后端
echo [1/3] 检查后端服务...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 后端服务正常
    echo   URL: http://localhost:8000
) else (
    echo ✗ 后端服务异常
    goto :error
)

echo.

REM 检查前端
echo [2/3] 检查前端服务...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 前端服务正常
    echo   URL: http://localhost:3000
) else (
    echo ✗ 前端服务异常
    goto :error
)

echo.

REM 检查API文档
echo [3/3] 检查API文档...
curl -s http://localhost:8000/docs >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ API文档可访问
    echo   URL: http://localhost:8000/docs
) else (
    echo ✗ API文档异常
    goto :error
)

echo.
echo ======================================
echo ✓ 所有服务运行正常!
echo ======================================
echo.
echo 访问地址:
echo   前端: http://localhost:3000
echo   后端: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo.
timeout /t 2 /nobreak >nul
exit /b 0

:error
echo.
echo ======================================
echo ✗ 部分服务异常
echo ======================================
echo.
echo 请检查:
echo   1. 服务是否已启动 (运行 start.bat)
echo   2. 端口是否被占用
echo   3. 查看日志文件
echo.
timeout /t 5 /nobreak >nul
exit /b 1
