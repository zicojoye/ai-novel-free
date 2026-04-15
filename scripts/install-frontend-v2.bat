@echo off
chcp 65001 >nul
echo ========================================
echo AI Novel Platform - 前端依赖安装
echo ========================================
echo.

cd /d "%~dp0frontend"

echo 正在检查 Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Node.js!
    echo 请从 https://nodejs.org/ 下载安装
    pause
    exit /b 1
)

echo Node.js 已安装
node --version
echo.

echo 正在检查 npm...
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 npm!
    pause
    exit /b 1
)

npm --version
echo.

echo 正在清除旧的 node_modules...
if exist node_modules (
    rmdir /s /q node_modules
)
if exist package-lock.json (
    del package-lock.json
)
echo.

echo 正在安装前端依赖...
echo 这可能需要 3-5 分钟,请耐心等待...
echo.

call npm install --legacy-peer-deps

if %errorlevel% neq 0 (
    echo.
    echo [错误] 依赖安装失败!
    echo.
    echo 尝试解决方案:
    echo 1. 清除 npm 缓存: npm cache clean --force
    echo 2. 使用国内镜像: npm config set registry https://registry.npmmirror.com
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [成功] 前端依赖安装完成!
echo ========================================
echo.
echo 现在可以运行: npm run dev
echo.
pause
