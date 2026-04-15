@echo off
chcp 65001 > nul
:: 启动后端服务 - 自动检查依赖

echo ==============================================================================
echo 🚀 AI Novel Platform 后端服务
echo ==============================================================================
echo.

cd /d "%~dp0"

echo [1/3] 诊断系统...
echo.
python backend_diagnostic.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ 系统诊断失败
    echo.
    echo 请先解决诊断中发现的问题
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖...
echo.

:: 尝试导入关键包
python -c "import fastapi, uvicorn, sqlmodel" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 依赖已安装
    echo.
) else (
    echo ⚠️  缺少依赖,正在自动安装...
    echo.

    if exist "check_and_install_deps.py" (
        python check_and_install_deps.py
    ) else (
        echo 未找到自动安装脚本,尝试手动安装...
        pip install -r requirements.txt
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
echo [3/3] 启动后端服务...
echo ==============================================================================
echo.

python start.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 启动失败
    echo.
    echo 尝试直接启动:
    echo   python main.py
    echo.
    echo 或者运行诊断工具查看问题:
    echo   python backend_diagnostic.py
    pause
    exit /b 1
)
