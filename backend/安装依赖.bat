@echo off
chcp 65001 > nul
:: 自动检查并安装Python依赖
:: 已安装的跳过,没安装的自动安装
:: 有问题自动修复

echo ==============================================================================
echo 🚀 AI Novel Platform 后端依赖自动安装
echo ==============================================================================
echo.

:: 检查Python是否安装
echo [1/4] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python版本: %PYTHON_VERSION%
echo.

:: 检查pip
echo [2/4] 检查pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  pip不可用,尝试使用python -m pip...
    python -m pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ pip不可用,请手动安装
        pause
        exit /b 1
    )
)

for /f "tokens=*" %%i in ('python -m pip --version 2^>^&1') do set PIP_VERSION=%%i
echo ✓ %PIP_VERSION%
echo.

:: 升级pip
echo 🔄 升级pip到最新版本...
python -m pip install --upgrade pip
echo.

:: 安装依赖
echo [3/4] 检查并安装依赖包...
echo ==============================================================================
echo.

if not exist "requirements.txt" (
    echo ❌ 找不到 requirements.txt
    pause
    exit /b 1
)

:: 运行Python脚本检查并安装
python check_and_install_deps.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Python脚本执行失败,尝试直接安装...
    echo.

    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo [4/4] 验证关键包...
echo ==============================================================================
python -c "import fastapi; print('✓ FastAPI:', fastapi.__version__)" 2>nul || echo ✗ FastAPI: 未安装
python -c "import uvicorn; print('✓ Uvicorn:', uvicorn.__version__)" 2>nul || echo ✗ Uvicorn: 未安装
python -c "import langchain; print('✓ LangChain:', langchain.__version__)" 2>nul || echo ✗ LangChain: 未安装
python -c "import sqlmodel; print('✓ SQLModel:', sqlmodel.__version__)" 2>nul || echo ✗ SQLModel: 未安装
python -c "import qdrant_client; print('✓ Qdrant:', qdrant_client.__version__)" 2>nul || echo ✗ Qdrant: 未安装

echo.
echo ==============================================================================
echo ✅ 依赖安装完成!
echo ==============================================================================
echo.
echo 启动命令:
echo   python main.py
echo.
echo 按任意键退出...
pause >nul
