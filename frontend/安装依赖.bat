@echo off
chcp 65001 > nul
:: 自动检查并安装Node.js依赖
:: 已安装的跳过,没安装的自动安装
:: 有问题自动修复

echo ==============================================================================
echo 🚀 AI Novel Platform 前端依赖自动安装
echo ==============================================================================
echo.

:: 检查Node.js
echo [1/5] 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装或未添加到PATH
    echo 请先安装Node.js 18+: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo ✓ Node.js版本: %NODE_VERSION%
echo.

:: 检查npm
echo [2/5] 检查npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm不可用
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
echo ✓ npm版本: %NPM_VERSION%
echo.

:: 检查yarn
echo [3/5] 检查包管理器...
yarn --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 检测到yarn
    set USE_YARN=1
) else (
    echo ✓ 使用npm
    set USE_YARN=0
)
echo.

:: 检查package.json
echo [4/5] 检查package.json...
if not exist "package.json" (
    echo ❌ 找不到 package.json
    pause
    exit /b 1
)
echo ✓ package.json 存在
echo.

:: 检查node_modules
echo 检查node_modules...
if exist "node_modules" (
    echo ✓ node_modules已存在
) else (
    echo ⚠️  node_modules不存在,需要安装依赖
)
echo.

:: 安装依赖
echo ==============================================================================
echo [5/5] 安装依赖包...
echo ==============================================================================
echo.

if %USE_YARN% equ 1 (
    echo 🔄 使用yarn安装依赖...
    yarn install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 🔄 使用npm安装依赖...
    echo 💡 提示: 可以使用 'npm install -g yarn' 安装yarn以获得更快的安装速度
    npm install
    if %errorlevel% neq 0 (
        echo.
        echo ❌ 依赖安装失败
        echo.
        echo 🔧 尝试修复...
        echo 1. 清理npm缓存...
        call npm cache clean --force

        echo 2. 删除node_modules和package-lock.json...
        if exist "node_modules" rmdir /s /q node_modules
        if exist "package-lock.json" del /f /q package-lock.json

        echo 3. 重新安装...
        call npm install
        if %errorlevel% neq 0 (
            echo.
            echo ❌ 修复失败
            echo 请尝试手动运行: npm install
            pause
            exit /b 1
        )
    )
)

echo.
echo 验证关键包...
echo ==============================================================================
npm list react 2>nul | findstr "react" >nul && echo ✓ React 已安装 || echo ✗ React 未安装
npm list react-dom 2>nul | findstr "react-dom" >nul && echo ✓ React DOM 已安装 || echo ✗ React DOM 未安装
npm list react-router-dom 2>nul | findstr "react-router-dom" >nul && echo ✓ React Router 已安装 || echo ✗ React Router 未安装
npm list zustand 2>nul | findstr "zustand" >nul && echo ✓ Zustand 已安装 || echo ✗ Zustand 未安装

echo.
echo ==============================================================================
echo ✅ 依赖安装完成!
echo ==============================================================================
echo.
echo 启动命令:
echo   npm run dev
echo.
echo 构建命令:
echo   npm run build
echo.
echo 按任意键退出...
pause >nul
