#!/bin/bash
# 启动前端服务 - 自动检查依赖

echo "=============================================================================="
echo "🚀 AI Novel Platform 前端服务"
echo "=============================================================================="
echo ""

cd "$(dirname "$0")"

echo "🔍 检查依赖..."
echo ""

if [ -d "node_modules" ]; then
    echo "✓ node_modules存在"
    echo ""
else
    echo "⚠️  node_modules不存在,正在自动安装..."
    echo ""

    if [ -f "安装依赖.sh" ]; then
        bash 安装依赖.sh
    else
        npm install
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
echo "🚀 启动前端服务..."
echo "=============================================================================="
echo ""

if [ -f "start.js" ]; then
    node start.js
else
    npm run dev
fi
