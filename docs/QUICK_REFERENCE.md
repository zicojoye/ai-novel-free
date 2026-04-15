# AI小说平台 - 快速参考卡

## 🚀 快速启动

```bash
# Windows - 一键启动
start.bat

# Windows - 健康检查
health_check.bat

# Windows - 停止服务
stop.bat

# 手动启动
cd backend && python start.py
cd frontend && npm run dev
```

## 🔧 配置流程

```bash
cd backend

# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境
copy .env.example .env
python generate_secret_key.py

# 3. 编辑 .env,添加API密钥
# OPENAI_API_KEY=sk-your-key-here

# 4. 验证配置
python validate_config.py

# 5. 启动服务
python start.py
```

## 🌐 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| 后端API | http://localhost:8000 |
| API文档 | http://localhost:8000/docs |
| 健康检查 | http://localhost:8000/health |

## 🔒 安全配置

### 必须配置

- ✅ 修改SECRET_KEY: `python generate_secret_key.py`
- ✅ 配置API密钥: 至少一个 (OpenAI/Anthropic/DeepSeek/Gemini)

### 可选配置

```env
# 限流
RATE_LIMIT_PER_MINUTE=60

# 缓存
ENABLE_CACHE=true
CACHE_TTL=3600

# 预算
DAILY_BUDGET=10.0
ENABLE_BUDGET_LIMIT=true
```

## 🛠️ 常用命令

### 后端

```bash
cd backend

# 启动
python start.py

# 验证配置
python validate_config.py

# 生成密钥
python generate_secret_key.py

# 健康检查
python ../health_check.py
```

### 前端

```bash
cd frontend

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 安装依赖
npm install
```

## 🔍 故障排查

### 端口被占用

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# 或修改.env
BACKEND_PORT=8001
```

### 配置验证失败

```bash
cd backend
python validate_config.py

# 根据提示修复错误
# 1. 修改SECRET_KEY
# 2. 添加API密钥
# 3. 检查数据库
```

### CORS错误

1. 检查 `main.py` 中的CORS配置
2. 确认前端使用相对路径 `/api`
3. 检查Vite代理配置

### 查看日志

```bash
# 实时查看日志 (PowerShell)
Get-Content backend\data\logs\app.log -Wait -Tail 50

# Linux/Mac
tail -f backend/data/logs/app.log
```

## 📦 文件结构

```
ai-novel-platform/
├── backend/
│   ├── app/
│   │   ├── api/          # API路由
│   │   ├── core/         # 核心配置
│   │   ├── models/       # 数据模型
│   │   ├── services/     # 业务服务
│   │   └── agents/       # Agent系统
│   ├── main.py           # 主入口
│   ├── start.py          # 启动脚本
│   ├── validate_config.py # 配置验证
│   ├── generate_secret_key.py # 密钥生成
│   └── .env             # 环境配置
├── frontend/
│   ├── src/
│   │   ├── components/   # React组件
│   │   ├── pages/        # 页面
│   │   ├── services/     # API服务
│   │   └── stores/       # 状态管理
│   ├── .env             # 环境配置
│   └── vite.config.ts   # Vite配置
├── start.bat            # 一键启动
├── stop.bat             # 停止服务
├── health_check.bat     # 健康检查
├── health_check.py      # 健康检查(Python)
└── DEPLOYMENT.md       # 完整部署指南
```

## 🔗 有用链接

| 文档 | 路径 |
|------|------|
| 完整部署指南 | [DEPLOYMENT.md](./DEPLOYMENT.md) |
| 更新日志 | [CHANGELOG.md](./CHANGELOG.md) |
| 项目README | [README.md](./README.md) |
| API文档 | http://localhost:8000/docs |

## 💡 提示

- ✅ 使用 `start.bat` 快速启动所有服务
- ✅ 运行 `validate_config.py` 检查配置
- ✅ 使用 `health_check.bat` 检查服务状态
- ✅ 定期备份数据库 `data/ai_novel.db`
- ✅ 查看日志排查问题 `data/logs/app.log`
- ✅ 至少配置一个AI API密钥
- ✅ 生产环境必须修改SECRET_KEY

## 📞 支持

1. 运行 `python validate_config.py` 检查配置
2. 查看 [DEPLOYMENT.md](./DEPLOYMENT.md) 详细文档
3. 查看日志 `backend/data/logs/app.log`
4. 提交Issue到项目仓库

---

**版本**: 1.0.0
**更新日期**: 2026-04-14
**状态**: ✅ 生产就绪
