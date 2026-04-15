@echo off
chcp 65001 >nul
echo ========================================
echo   AI Novel Platform 一键初始化
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查必要目录...
if not exist "data" mkdir data
if not exist "data\uploads" mkdir data\uploads
echo ✓ 目录检查完成
echo.

echo [2/4] 安装后端依赖...
cd backend
echo 正在安装 Python 依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ 后端依赖安装失败！
    pause
    exit /b 1
)
echo ✓ 后端依赖安装完成
echo.

cd ..

echo [3/4] 安装前端依赖...
cd frontend
echo 正在安装 Node.js 依赖...
call npm install
if errorlevel 1 (
    echo ✗ 前端依赖安装失败！
    pause
    exit /b 1
)
echo ✓ 前端依赖安装完成
echo.

cd ..

echo [4/4] 配置说明...
echo.
echo ========================================
echo   初始化完成！
echo ========================================
echo.
echo 下一步：
echo 1. 编辑 .env 文件，配置至少一个 AI API Key：
echo    - OPENAI_API_KEY=sk-your-key
echo    - ANTHROPIC_API_KEY=sk-ant-your-key
echo    - DEEPSEEK_API_KEY=sk-your-key
echo.
echo 2. 运行启动脚本：start.bat
echo.
echo 按任意键继续...
pause >nul
