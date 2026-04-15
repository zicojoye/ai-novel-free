#!/bin/bash
# 自动检查并安装Python依赖
# 已安装的跳过,没安装的自动安装
# 有问题自动修复

set -e  # 遇到错误立即退出

echo "=============================================================================="
echo "🚀 AI Novel Platform 后端依赖自动安装"
echo "=============================================================================="
echo ""

# 检查Python
echo "[1/4] 检查Python环境..."
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python未安装"
    echo "请先安装Python 3.8+"
    exit 1
fi

# 优先使用python3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "✓ $PYTHON_VERSION"
echo ""

# 检查pip
echo "[2/4] 检查pip..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ pip不可用"
    exit 1
fi

PIP_VERSION=$($PYTHON_CMD -m pip --version 2>&1)
echo "✓ $PIP_VERSION"
echo ""

# 升级pip
echo "🔄 升级pip到最新版本..."
$PYTHON_CMD -m pip install --upgrade pip
echo ""

# 检查并安装依赖
echo "[3/4] 检查并安装依赖包..."
echo "=============================================================================="
echo ""

if [ ! -f "requirements.txt" ]; then
    echo "❌ 找不到 requirements.txt"
    exit 1
fi

# 运行Python脚本
$PYTHON_CMD check_and_install_deps.py

# 备用方案:直接安装
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Python脚本执行失败,尝试直接安装..."
    echo ""

    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

echo ""
echo "[4/4] 验证关键包..."
echo "=============================================================================="

$PYTHON_CMD -c "import fastapi; print('✓ FastAPI:', fastapi.__version__)" 2>/dev/null || echo "✗ FastAPI: 未安装"
$PYTHON_CMD -c "import uvicorn; print('✓ Uvicorn:', uvicorn.__version__)" 2>/dev/null || echo "✗ Uvicorn: 未安装"
$PYTHON_CMD -c "import langchain; print('✓ LangChain:', langchain.__version__)" 2>/dev/null || echo "✗ LangChain: 未安装"
$PYTHON_CMD -c "import sqlmodel; print('✓ SQLModel:', sqlmodel.__version__)" 2>/dev/null || echo "✗ SQLModel: 未安装"
$PYTHON_CMD -c "import qdrant_client; print('✓ Qdrant:', qdrant_client.__version__)" 2>/dev/null || echo "✗ Qdrant: 未安装"

echo ""
echo "=============================================================================="
echo "✅ 依赖安装完成!"
echo "=============================================================================="
echo ""
echo "启动命令:"
echo "  $PYTHON_CMD main.py"
echo ""
