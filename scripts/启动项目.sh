#!/bin/bash
# AI Novel Platform 一键启动全部服务
# 自动检查依赖后启动前后端服务

echo "=============================================================================="
echo "🚀 AI Novel Platform 一键启动"
echo "=============================================================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/ai-novel-platform/backend"
FRONTEND_DIR="$SCRIPT_DIR/ai-novel-platform/frontend"

echo "检查后端依赖..."
cd "$BACKEND_DIR"
python -c "import fastapi, uvicorn, langchain, sqlmodel" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ 后端依赖已安装"
else
    echo "⚠️  后端依赖未安装,正在自动安装..."
    bash 安装依赖.sh
fi

echo ""
echo "检查前端依赖..."
cd "$FRONTEND_DIR"
if [ -d "node_modules" ]; then
    echo "✓ 前端依赖已安装"
else
    echo "⚠️  前端依赖未安装,正在自动安装..."
    bash 安装依赖.sh
fi

echo ""
echo "=============================================================================="
echo "🚀 启动前后端服务..."
echo "=============================================================================="
echo ""

echo "[1/2] 启动后端服务..."
cd "$BACKEND_DIR"
gnome-terminal -- bash -c "bash 启动后端.sh" 2>/dev/null || \
xterm -e "bash 启动后端.sh" 2>/dev/null || \
bash 启动后端.sh &

echo "等待后端服务启动..."
sleep 5

echo ""
echo "[2/2] 启动前端服务..."
cd "$FRONTEND_DIR"
gnome-terminal -- bash -c "bash 启动前端.sh" 2>/dev/null || \
xterm -e "bash 启动前端.sh" 2>/dev/null || \
bash 启动前端.sh &

echo ""
echo "=============================================================================="
echo "✅ 服务启动中..."
echo "=============================================================================="
echo ""
echo "后端服务: http://localhost:8000"
echo "后端API文档: http://localhost:8000/docs"
echo "前端服务: http://localhost:3000"
echo ""
echo "注意: 首次启动可能需要几分钟等待依赖安装"
echo ""
