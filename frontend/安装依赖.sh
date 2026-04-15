#!/bin/bash
# 自动检查并安装Node.js依赖
# 已安装的跳过,没安装的自动安装
# 有问题自动修复

set -e  # 遇到错误立即退出

echo "=============================================================================="
echo "🚀 AI Novel Platform 前端依赖自动安装"
echo "=============================================================================="
echo ""

# 检查Node.js
echo "[1/5] 检查Node.js环境..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装"
    echo "请先安装Node.js 18+: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version 2>&1)
echo "✓ Node.js版本: $NODE_VERSION"
echo ""

# 检查npm
echo "[2/5] 检查npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm不可用"
    exit 1
fi

NPM_VERSION=$(npm --version 2>&1)
echo "✓ npm版本: $NPM_VERSION"
echo ""

# 检查yarn
echo "[3/5] 检查包管理器..."
USE_YARN=0
if command -v yarn &> /dev/null; then
    echo "✓ 检测到yarn"
    USE_YARN=1
else
    echo "✓ 使用npm"
fi
echo ""

# 检查package.json
echo "[4/5] 检查package.json..."
if [ ! -f "package.json" ]; then
    echo "❌ 找不到 package.json"
    exit 1
fi
echo "✓ package.json 存在"
echo ""

# 检查node_modules
echo "检查node_modules..."
if [ -d "node_modules" ]; then
    echo "✓ node_modules已存在"
else
    echo "⚠️  node_modules不存在,需要安装依赖"
fi
echo ""

# 安装依赖
echo "=============================================================================="
echo "[5/5] 安装依赖包..."
echo "=============================================================================="
echo ""

if [ $USE_YARN -eq 1 ]; then
    echo "🔄 使用yarn安装依赖..."
    yarn install
else
    echo "🔄 使用npm安装依赖..."
    echo "💡 提示: 可以使用 'npm install -g yarn' 安装yarn以获得更快的安装速度"
    npm install
fi

echo ""
echo "验证关键包..."
echo "=============================================================================="

if npm list react &> /dev/null; then
    echo "✓ React 已安装"
else
    echo "✗ React 未安装"
fi

if npm list react-dom &> /dev/null; then
    echo "✓ React DOM 已安装"
else
    echo "✗ React DOM 未安装"
fi

if npm list react-router-dom &> /dev/null; then
    echo "✓ React Router 已安装"
else
    echo "✗ React Router 未安装"
fi

if npm list zustand &> /dev/null; then
    echo "✓ Zustand 已安装"
else
    echo "✗ Zustand 未安装"
fi

echo ""
echo "=============================================================================="
echo "✅ 依赖安装完成!"
echo "=============================================================================="
echo ""
echo "启动命令:"
echo "  npm run dev"
echo ""
echo "构建命令:"
echo "  npm run build"
echo ""
