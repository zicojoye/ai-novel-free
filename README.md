# AI小说平台 Free - 开源版

> 番茄小说爆款写作辅助工具，开源免费使用。

## ✅ 开源功能

- 基础章节编辑器（Markdown + 实时字数统计）
- 单Agent生成（主创/编辑/审核/发布 4个Agent）
- 项目管理（多项目、章节管理）
- 世界观构建（10维度设定）
- 知识库基础功能（文档上传、检索）
- 番茄爆款提示词库（`docs/prompts/`）
- 导出功能（TXT/Markdown）
- WebSocket实时推送框架
- 自定义AI模型（OpenAI/Anthropic/DeepSeek/Gemini + 自定义）

## 🔖 开源/发布前清单

- **敏感信息**: `.env` 已加入 `.gitignore`，发布前不要提交任何真实密钥或数据库文件。
- **运行产物**: 已清理 `node_modules/`、`frontend/dist/`、`__pycache__`、`*.pyc`、`backend/data/ai_novel.db`、日志等；发布前可再次执行清理。
- **环境示例**: 后端 `backend/.env.example`，前端 `frontend/.env.example`，根目录 `.env.example`；复制为 `.env` 后再填写。
- **密钥**: 运行 `python generate_secret_key.py` 生成安全的 `SECRET_KEY`（在 `backend` 目录）。
- **许可证**: 仓库使用 MIT License（文件 `LICENSE` 与 `package.json` 已一致）。

## 🚀 快速开始（开发环境）

### 后端

```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # macOS/Linux 使用: cp .env.example .env
python generate_secret_key.py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend
npm install
copy .env.example .env  # macOS/Linux 使用: cp .env.example .env
npm run dev -- --host --port 3000
```

### 一键同时启动（需已安装前端/后端依赖）

```bash
# 在仓库根目录
npm install  # 安装工作区/并发脚本依赖
npm run dev  # 前端 + 后端同时启动
```

访问：
- 前端: `http://localhost:3000`
- 后端 API: `http://localhost:8000`
- API 文档: `http://localhost:8000/docs`

## 🛠️ 构建与部署（生产）

- **前端构建**: `cd frontend && npm run build`，产物在 `frontend/dist`。
- **后端服务**: `uvicorn main:app --host 0.0.0.0 --port 8000`（或使用 `gunicorn`/`supervisor`/`systemd` 部署）。
- **反向代理**: 将前端静态文件托管（如 Nginx）并将 `/api`、`/ws` 代理到后端。
- **环境变量**: 生产环境务必修改 `SECRET_KEY`，并填入实际的 AI Key、Redis/Qdrant/Postgres 地址等。

## 📂 数据与存储

- 运行时数据位于 `backend/data/uploads`、`backend/data/logs`，已被 `.gitignore` 忽略。
- 默认数据库为 SQLite (`backend/data/ai_novel.db`)，生产环境可切换到 Postgres（见 `.env.example`）。

## 📜 License

本项目基于 **MIT License** 开源，详见 `LICENSE` 文件。
