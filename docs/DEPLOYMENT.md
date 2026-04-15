# AI小说平台 - 完整部署与优化指南

## 📋 目录

1. [快速开始](#快速开始)
2. [配置验证](#配置验证)
3. [安全配置](#安全配置)
4. [启动服务](#启动服务)
5. [CORS配置](#cors配置)
6. [安全加固](#安全加固)
7. [故障排查](#故障排查)

---

## 🚀 快速开始

### 前置要求

- Python 3.9+
- Node.js 18+
- 至少一个AI API密钥 (OpenAI/Anthropic/DeepSeek/Gemini)

### 1. 克隆项目并进入目录

```bash
cd ai-novel-platform
```

### 2. 后端配置

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 复制环境变量模板
copy .env.example .env

# 生成安全的SECRET_KEY (Windows)
python generate_secret_key.py
```

或手动编辑 `.env` 文件,配置以下内容:

```env
# 必须配置的AI API密钥 (至少一个)
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
DEEPSEEK_API_KEY=sk-your-key-here
GEMINI_API_KEY=your-key-here

# 默认模型配置
DEFAULT_MODEL=gpt-4o
DEFAULT_LLM_PROVIDER=openai
```

### 3. 验证配置

```bash
# 运行配置验证脚本
python validate_config.py
```

验证脚本会检查:
- ✓ SECRET_KEY是否安全
- ✓ 是否配置了AI API密钥
- ✓ 数据库连接
- ✓ API密钥连接测试
- ✓ 必要的目录和依赖

如果验证失败,请根据提示修复错误后重试。

### 4. 启动后端服务

```bash
# 使用启动脚本 (推荐)
python start.py

# 或直接启动
python main.py
```

后端将在 `http://localhost:8000` 启动。

### 5. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 复制环境变量模板
copy .env.example .env
```

前端 `.env` 文件默认配置 (开发环境):

```env
# 开发环境使用相对路径,通过Vite代理转发
VITE_API_BASE_URL=/api
VITE_PORT=3000
```

### 6. 启动前端服务

```bash
npm run dev
```

前端将在 `http://localhost:3000` 启动。

---

## 🔍 配置验证

### 运行验证脚本

```bash
python validate_config.py
```

### 验证项说明

| 验证项 | 说明 | 失败后果 |
|--------|------|----------|
| SECRET_KEY | 检查密钥长度和是否使用默认值 | 无法使用认证功能 |
| API密钥 | 检查至少配置一个AI API | 无法使用AI生成功能 |
| 数据库连接 | 测试SQLite数据库可访问性 | 无法存储数据 |
| API连接测试 | 测试OpenAI/Anthropic API | AI功能不可用 |
| 必要目录 | 检查data/uploads/logs目录 | 文件上传/日志失败 |
| Python包 | 检查必要依赖是否安装 | 服务无法启动 |

### 修复常见问题

#### 问题1: SECRET_KEY使用默认值

```bash
# 运行密钥生成脚本
python generate_secret_key.py

# 按提示确认更新.env文件
```

#### 问题2: 未配置AI API密钥

1. 选择一个AI服务提供商并获取API密钥
2. 编辑 `.env` 文件,添加对应的API密钥
3. 重新运行验证脚本

#### 问题3: API连接测试失败

检查:
- API密钥是否正确
- 网络连接是否正常
- 是否有足够的API额度

---

## 🔒 安全配置

### 1. 密码加密

系统使用bcrypt加密密码,默认12轮加密:

```python
from app.core.security import hash_password, verify_password

# 加密密码
hashed = hash_password("user_password")

# 验证密码
is_valid = verify_password("user_password", hashed)
```

### 2. JWT令牌

访问令牌默认60分钟过期:

```python
from app.core.security import create_access_token

# 创建令牌
token = create_access_token({"sub": "user_id"})
```

### 3. 请求限流

每IP每分钟最多60个请求,可在 `.env` 中调整:

```env
RATE_LIMIT_PER_MINUTE=60
```

### 4. XSS防护

系统自动检测并阻止XSS攻击:

- 危险标签: `<script>`, `<iframe>`, `<object>`等
- 危险属性: `onload`, `onclick`, `javascript:`等

### 5. SQL注入防护

系统自动检测SQL注入特征:

- UNION SELECT攻击
- 注释注入 (`--`, `/* */`)
- 命令注入 (`; DROP`, `; DELETE`)

### 6. 安全响应头

系统自动添加以下安全响应头:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: default-src 'self'; ...
```

---

## 🌐 CORS配置

### 当前配置

系统配置为允许所有来源的跨域请求:

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 限制访问来源 (生产环境建议)

编辑 `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 前端代理配置

开发环境通过Vite代理转发API请求:

```typescript
// vite.config.ts
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path,  // 直接透传路径
  }
}
```

生产环境部署时,需要配置Nginx或其他反向代理:

```nginx
location /api/ {
    proxy_pass http://localhost:8000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

---

## 🛡️ 安全加固

### 1. 生产环境检查清单

- [ ] 修改SECRET_KEY (运行 `python generate_secret_key.py`)
- [ ] 配置HTTPS
- [ ] 限制CORS来源
- [ ] 启用防火墙
- [ ] 定期备份数据库
- [ ] 监控日志文件

### 2. 数据备份

```bash
# 备份SQLite数据库
copy data\ai_novel.db backup\ai_novel_backup_%date%.db
```

### 3. 日志监控

日志文件位置: `backend/data/logs/app.log`

实时查看日志:

```bash
# Windows (PowerShell)
Get-Content data\logs\app.log -Wait -Tail 50

# Linux/Mac
tail -f data/logs/app.log
```

### 4. API密钥管理

最佳实践:

1. 永远不要将API密钥提交到版本控制
2. 使用环境变量存储密钥
3. 定期轮换密钥
4. 为不同环境使用不同密钥
5. 监控API使用量和成本

---

## 🐛 故障排查

### 问题1: 端口被占用

**错误信息:** `OSError: [WinError 10048] Address already in use`

**解决方案:**

```bash
# Windows: 查找占用8000端口的进程
netstat -ano | findstr :8000

# 终止进程 (替换PID)
taskkill /PID <进程ID> /F

# 或修改端口
# 编辑 .env: BACKEND_PORT=8001
```

### 问题2: CORS错误

**错误信息:** `Access to XMLHttpRequest blocked by CORS policy`

**解决方案:**

1. 检查 `main.py` 中的CORS配置
2. 确认前端使用相对路径 `/api` (开发环境)
3. 检查Vite代理配置

### 问题3: API连接超时

**错误信息:** `httpx.ConnectTimeout`

**解决方案:**

1. 检查网络连接
2. 验证API密钥是否正确
3. 检查API服务状态
4. 调整超时时间 (在代码中)

### 问题4: 数据库锁定

**错误信息:** `sqlite3.OperationalError: database is locked`

**解决方案:**

```bash
# 关闭所有数据库连接
# 重新启动服务
python start.py
```

### 问题5: 依赖安装失败

**错误信息:** `Could not find a version that satisfies the requirement`

**解决方案:**

```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题6: 前端代理失败

**错误信息:** `Proxy error: Could not proxy request`

**解决方案:**

1. 确认后端服务已启动
2. 检查 `vite.config.ts` 中的代理配置
3. 查看终端日志确认代理URL

---

## 📊 性能优化建议

### 1. 启用缓存

在 `.env` 中启用缓存:

```env
ENABLE_CACHE=true
CACHE_TTL=3600
ENABLE_SEMANTIC_CACHE=true
```

### 2. 预算控制

设置每日预算限制:

```env
DAILY_BUDGET=10.0
ENABLE_BUDGET_LIMIT=true
```

### 3. Agent配置

优化Agent性能:

```env
AGENT_TIMEOUT=300
AGENT_MAX_TURNS=10
```

---

## 🔗 有用链接

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [React文档](https://react.dev/)
- [Vite文档](https://vitejs.dev/)
- [OpenAI API文档](https://platform.openai.com/docs/)
- [Anthropic API文档](https://docs.anthropic.com/)

---

## 📞 技术支持

如遇到问题,请按以下顺序排查:

1. 运行 `python validate_config.py` 检查配置
2. 查看日志文件 `data/logs/app.log`
3. 检查本文档的故障排查部分
4. 查看项目GitHub Issues

---

## 📝 版本历史

- v1.0.0 (2026-04-14)
  - 初始版本
  - 完整的配置验证
  - 安全中间件集成
  - CORS配置优化
  - 全面的部署文档
