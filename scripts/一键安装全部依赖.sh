#!/bin/bash
# AI Novel Platform 一键安装全部依赖
# 自动检查并安装前后端所有依赖
# 已安装的跳过,没安装的自动安装
# 有问题自动修复

set -e  # 遇到错误立即退出

echo "=============================================================================="
echo "🚀 AI Novel Platform 一键安装全部依赖"
echo "=============================================================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/ai-novel-platform/backend"
FRONTEND_DIR="$SCRIPT_DIR/ai-novel-platform/frontend"

# 安装后端依赖
echo "[1/2] 安装后端依赖..."
echo "=============================================================================="
echo ""
cd "$BACKEND_DIR"
if [ -f "安装依赖.sh" ]; then
    bash 安装依赖.sh
else
    echo "⚠️  找不到安装脚本,尝试手动安装..."
    python check_and_install_deps.py
fi

echo ""
echo "=============================================================================="
echo "[2/2] 安装前端依赖..."
echo "=============================================================================="
echo ""
cd "$FRONTEND_DIR"
if [ -f "安装依赖.sh" ]; then
    bash 安装依赖.sh
else
    echo "⚠️  找不到安装脚本,尝试手动安装..."
    npm install
fi

echo ""
echo "=============================================================================="
echo "✅ 全部依赖安装完成!"
echo "=============================================================================="
echo ""
echo "启动项目:"
echo "  1. 启动后端: cd backend && python main.py"
echo "  2. 启动前端: cd frontend && npm run dev"
echo ""
echo "或使用提供的启动脚本"
echo ""
