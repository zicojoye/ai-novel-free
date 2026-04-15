@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title AI Novel Platform - 一键启动

cls
echo ================================================
echo         AI Novel Platform - 一键启动
echo ================================================
echo.

cd /d "%~dp0"

::: 检查首次运行
if not exist "backend\venv" (
    if not exist "backend\.venv" (
        echo [首次运行] 正在初始化环境...
        echo.
        goto :install
    )
)

::: 检查依赖
if not exist "frontend\node_modules" (
    echo [警告] 前端依赖未安装，正在安装...
    cd frontend
    call npm install --legacy-peer-deps
    cd ..
)

::: 启动服务
goto :start

:install
echo ================================================
echo              安装依赖
echo ================================================
echo.

::: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo.
    echo 请先安装Python 3.8+: https://www.python.org/downloads/
    echo 安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python环境正常

::: 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Node.js未安装或未添加到PATH
    echo.
    echo 请先安装Node.js: https://nodejs.org/
    echo 下载LTS版本（推荐18.x或20.x）
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js环境正常
echo.

::: 创建目录
echo [1/4] 创建必要目录...
if exist "init.py" (
    python init.py
) else (
    if not exist "data\novels" mkdir data\novels
    if not exist "data\characters" mkdir data\characters
    if not exist "data\outlines" mkdir data\outlines
    if not exist "data\settings" mkdir data\settings
    if not exist "data\chapters" mkdir data\chapters
    if not exist "data\logs" mkdir data\logs
)
echo [OK] 目录创建完成
echo.

::: 安装后端依赖
echo [2/4] 安装后端依赖...
cd backend
if not exist "requirements.txt" (
    echo [错误] 找不到 requirements.txt
    pause
    exit /b 1
)
echo 正在安装Python依赖（可能需要几分钟）...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [警告] 安装失败，正在重试...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 后端依赖安装失败
        pause
        exit /b 1
    )
)

::: 确保python-dotenv已安装
python -c "import dotenv" 2>nul
if errorlevel 1 (
    echo [警告] python-dotenv未安装，正在单独安装...
    python -m pip install python-dotenv
)
echo [OK] 后端依赖安装完成
cd ..
echo.

::: 安装前端依赖
echo [3/4] 安装前端依赖...
cd frontend
if not exist "package.json" (
    echo [错误] 找不到 package.json
    pause
    exit /b 1
)
echo 正在使用 --legacy-peer-deps 安装...
call npm install --legacy-peer-deps
if errorlevel 1 (
    echo [错误] 前端依赖安装失败
    echo.
    echo 解决方案：
    echo   1. 清除缓存：npm cache clean --force
    echo   2. 删除 node_modules：rmdir /s /q node_modules
    echo   3. 重新运行此脚本
    pause
    exit /b 1
)
echo [OK] 前端依赖安装完成
cd ..
echo.

::: 检查配置
echo [4/4] 检查配置...
cd backend
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [OK] 已创建.env文件
        echo.
        echo [提示] 请先配置.env文件中的以下内容:
        echo   1. 运行: python generate_secret_key.py
        echo   2. 配置至少一个AI API密钥（OPENAI_API_KEY 或其他）
        echo   3. 保存文件后重新运行此脚本
        echo.
        pause
        exit /b 0
    )
)
cd ..
echo [OK] 配置检查完成
echo.

echo ================================================
echo              安装完成
echo ================================================
echo.
timeout /t 2 /nobreak >nul

:start
cls
echo ================================================
echo         AI Novel Platform - 启动中
echo ================================================
echo.

cd backend

::: 验证配置
echo [1/3] 验证配置...
if exist "validate_config.py" (
    python validate_config.py
    if errorlevel 1 (
        echo.
        echo [WARNING] Configuration has issues, but starting anyway...
        echo You can configure API keys in backend/.env later
        timeout /t 3 /nobreak >nul
    )
)
echo [OK] Configuration check completed
echo.

::: 启动后端
echo [2/3] 启动后端服务...
echo 后端将在 http://localhost:8000 启动
echo.
start "AI Novel - Backend" cmd /k "python start.py"

::: 等待后端启动
echo 等待后端启动...
timeout /t 5 /nobreak >nul

::: 启动前端
echo [3/3] 启动前端服务...
echo 前端将在 http://localhost:3000 启动
echo.
cd ..\frontend
start "AI Novel - Frontend" cmd /k "npm run dev"

cd ..

cls
echo ================================================
echo              启动成功
echo ================================================
echo.
echo 访问地址:
echo   前端界面: http://localhost:3000
echo   后端API: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo.
echo 提示:
echo   - 在后端和前端窗口按 Ctrl+C 停止服务
echo   - 修改 .env 配置后请重启
echo   - 日志保存在 data/logs 目录
echo.
echo ================================================
echo.

set /p choice="是否打开浏览器访问前端界面? (Y/N): "
if /i "%choice%"=="Y" start http://localhost:3000

:end
echo.
echo 服务已启动，此窗口可以关闭（服务将继续运行）
echo.
pause
