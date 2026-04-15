#!/bin/bash
# 启动后端服务 - 自动检查依赖

echo "=============================================================================="
echo "🚀 AI Novel Platform 后端服务"
echo "=============================================================================="
echo ""

cd "$(dirname "$0")"

echo "[1/3] 诊断系统..."
echo ""
python backend_diagnostic.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 系统诊断失败"
    echo ""
    echo "请先解决诊断中发现的问题"
    exit 1
fi

echo ""
echo "[2/3] 检查依赖..."
echo ""

# 尝试导入关键包
python -c "import fastapi, uvicorn, sqlmodel" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ 依赖已安装"
    echo ""
else
    echo "⚠️  缺少依赖,正在自动安装..."
    echo ""

    if [ -f "check_and_install_deps.py" ]; then
        python check_and_install_deps.py
    else
        echo "未找到自动安装脚本,尝试手动安装..."
        pip install -r requirements.txt
    fi

    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi

    echo ""
    echo "✅ 依赖安装完成!"
    echo ""
fi

echo "=============================================================================="
echo "[3/3] 启动后端服务..."
echo "=============================================================================="
echo ""

python start.py
