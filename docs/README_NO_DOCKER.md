# AI Novel Platform

**纯本地部署版本 - 无Docker依赖**

AI小说创作平台,完整的本地应用,无需Docker!

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/downloads/)
[![Node](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)

---

## ✨ 功能特性

### 核心功能
- 🏗️ **完整架构**: 前端(React 19) + 后端(FastAPI)
- 🤖 **9个专业Agent**: 覆盖创作全流程
- 💾 **智能缓存**: 3层缓存系统,节省50%+成本
- 🔍 **RAG检索**: Qdrant向量数据库,精准语义检索
- 🧠 **智能路由**: 根据任务自动选择最优模型

### 创作工具
- 📚 **知识库管理**: 自动提取和索引知识
- 📖 **世界观构建**: 10维度编辑器
- ✍️ **章节创作**: AI辅助生成和润色
- 🎭 **伏笔管理**: 追踪伏笔和钩子

### 自动化
- 🚀 **自动发布**: 支持多平台发布
- 📊 **统计报表**: 生成项目统计报表
- 🔄 **定时任务**: Agent任务调度器
- 💾 **数据备份**: 自动备份和恢复

---

## 🛠 技术栈

### 前端
- React 19 + TypeScript 5.2
- Vite 5.0 (构建工具)
- Tailwind CSS (样式)
- Zustand (状态管理)
- TanStack Query (数据获取)
- React Router 6 (路由)

### 后端
- FastAPI (Web框架)
- SQLModel (ORM)
- SQLite/PostgreSQL (数据库)
- LangChain + LangGraph (AI框架)
- Qdrant (向量数据库)
- Redis (缓存)

---

## 🚀 快速开始

### 环境要求

- Node.js 20+
- Python 3.11+
- (可选) Redis服务器
- (可选) Qdrant服务

### 本地部署步骤

#### 1. 安装依赖

**后端**:
```bash
cd backend
pip install -r requirements.txt
```

**前端**:
```bash
cd frontend
npm install
```

#### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件
# 至少配置一个AI模型API Key
```

**必须配置**:
```bash
# OpenAI API Key
OPENAI_API_KEY=sk-xxxxxxxxxxxx

# 或 Anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

# 或 DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxx
```

#### 3. 启动服务

**启动后端**:
```bash
cd backend
python main_fixed.py
```

**启动前端**:
```bash
cd frontend
npm run dev
```

---

## 🌐 访问地址

启动成功后访问:

- **前端**: http://localhost:5173
- **后端**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

---

## 📊 项目统计

| 指标 | 数量 |
|------|------|
| 总代码行数 | 6200+ |
| 总文件数 | 72+ |
| API端点 | 53+ |
| Agent数量 | 9 |
| 页面模块 | 8 |

---

## 📁 项目结构

```
ai-novel-platform/
├── frontend/          # React 19前端
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── modules/       # 业务模块
│   │   ├── pages/         # 页面
│   │   ├── stores/        # Zustand状态
│   │   ├── services/      # API服务
│   │   ├── types/         # 类型定义
│   │   └── main.tsx       # 入口
│   ├── package.json       # 依赖配置
│   └── vite.config.ts     # Vite配置
│
├── backend/           # FastAPI后端
│   ├── app/
│   │   ├── api/           # API路由(8个模块)
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型(7个)
│   │   ├── services/      # 业务服务(3个)
│   │   └── agents/        # Agent实现(9个)
│   ├── main_fixed.py   # 后端入口
│   └── requirements.txt  # 依赖列表
│
├── automation/        # 自动化脚本
│   ├── publish_to_platforms.py  # 多平台发布
│   ├── backup.py                # 数据备份
│   ├── extract_knowledge.py      # 知识提取
│   ├── agent_scheduler.py        # Agent调度
│   └── generate_report.py       # 报表生成
│
├── shared/            # 共享模块
│   ├── types.py          # 共享类型
│   ├── constants.py      # 常量定义
│   ├── utils.py          # 工具函数
│   └── prompts.py        # 提示词模板
│
├── docs/              # 文档
│   ├── 启动指南.md
│   ├── 本地部署指南.md
│   ├── 问题诊断.md
│   ├── 功能验证报告.md
│   ├── 功能验证总结.md
│   ├── 功能互通验证报告.md
│   └── 验收检测报告.md
│
├── .env.example        # 环境变量模板
├── package.json        # 根配置
├── start.bat           # Windows一键启动
├── start.sh           # Linux/Mac一键启动
└── verify_functions.py # 功能验证脚本
```

---

## 🔧 常见问题

### 端口被占用

**Windows**:
```cmd
netstat -ano | findstr :5173
taskkill /PID <进程ID> /F
```

**Linux/Mac**:
```bash
lsof -i :5173
kill -9 <进程ID>
```

### 依赖安装失败

```bash
# 清理缓存
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📞 获取帮助

查看文档:
- `docs/本地部署指南.md` - 详细部署步骤
- `docs/问题诊断.md` - 问题解决
- `docs/功能互通验证报告.md` - 互通性说明

---

## 📄 许可证

本项目采用AGPL-3.0许可证

---

## 🎉 立即开始

```bash
# 1. 安装依赖
cd backend && pip install -r requirements.txt
cd frontend && npm install

# 2. 配置环境
cp .env.example .env
# 编辑.env,填入API Keys

# 3. 启动服务
# Windows: 双击 start.bat
# Linux/Mac: ./start.sh

# 4. 访问
http://localhost:5173
```

---

**✅ 纯本地部署,无需Docker!**
