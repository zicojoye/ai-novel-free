#!/bin/bash

echo "========================================"
echo "AI Novel Platform 快速启动"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "[提示] 未找到.env文件"
    echo "从.env.example复制..."
    cp .env.example .env
    echo "[提示] 请编辑.env文件,填入API Keys"
    echo ""
fi

# 检查数据目录
mkdir -p data/uploads data/logs data/db data/cache

echo "[1/3] 检查Node.js..."
if ! command -v node &> /dev/null; then
    echo "[错误] 未安装Node.js"
    echo "请先安装: https://nodejs.org/"
    exit 1
fi
echo "[OK] Node.js已安装"

echo ""
echo "[2/3] 安装依赖..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[错误] 前端依赖安装失败"
        exit 1
    fi
    echo "[OK] 前端依赖安装完成"
else
    echo "[OK] 前端依赖已存在"
fi
cd ..

echo ""
echo "[3/3] 启动服务..."
echo ""
echo "========================================"
echo "正在启动后端服务..."
echo "后端地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "========================================"
echo ""

# 启动后端
cd backend
python main.py &
BACKEND_PID=$!
cd ..

sleep 3

echo ""
echo "========================================"
echo "正在启动前端服务..."
echo "前端地址: http://localhost:5173"
echo "========================================"
echo ""

# 启动前端
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "服务已启动!"
echo ""
echo "访问地址:"
echo "  前端: http://localhost:5173"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "========================================"

# 等待进程
wait $BACKEND_PID $FRONTEND_PID
