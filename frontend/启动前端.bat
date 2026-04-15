@echo off
chcp 65001 > nul
:: 启动前端服务 - 自动检查依赖

echo ==============================================================================
echo 🚀 AI Novel Platform 前端服务
echo ==============================================================================
echo.

cd /d "%~dp0"

echo 🔍 检查依赖...
echo.

if exist "node_modules" (
    echo ✓ node_modules存在
    echo.
) else (
    echo ⚠️  node_modules不存在,正在自动安装...
    echo.

    if exist "安装依赖.bat" (
        call 安装依赖.bat
    ) else (
        npm install
    )

    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )

    echo.
    echo ✅ 依赖安装完成!
    echo.
)

echo ==============================================================================
echo 🚀 启动前端服务...
echo ==============================================================================
echo.

if exist "start.js" (
    node start.js
) else (
    npm run dev
)

if %errorlevel% neq 0 (
    echo.
    echo ❌ 启动失败
    echo.
    echo 尝试直接启动:
    echo   npm run dev
    pause
    exit /b 1
)
