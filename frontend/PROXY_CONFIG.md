# 前端路径代理配置说明

## 配置概述

前端使用Vite开发服务器的代理功能,将 `/api` 开头的请求转发到后端FastAPI服务器。

## 路径映射规则

### 开发环境

```
前端请求:  http://localhost:3000/api/projects
              ↓ (Vite Proxy)
后端接收:  http://localhost:8000/api/projects
```

### 生产环境

```
前端请求:  https://your-frontend.com/api/projects
              ↓ (Nginx / 反向代理)
后端接收:  http://your-backend.com/api/projects
```

## 配置文件说明

### 1. `.env` (默认配置)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### 2. `.env.development` (开发环境)
```bash
VITE_API_BASE_URL=/api
```
- 使用相对路径 `/api`
- Vite开发服务器会拦截 `/api` 开头的请求
- 通过proxy配置转发到 `http://localhost:8000`

### 3. `.env.production` (生产环境)
```bash
VITE_API_BASE_URL=http://your-backend-domain.com
```
- 需要填写完整的后端域名或IP地址
- **注意**: 不要在URL后面加 `/api`,因为后端路由本身就是 `/api/xxx`
- 前端构建后,请求会直接发送到这个地址

## Vite配置 (vite.config.ts)

```typescript
server: {
  proxy: {
    '/api': {
      target: env.VITE_API_BASE_URL?.startsWith('http')
        ? env.VITE_API_BASE_URL
        : 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path,  // 直接透传,不做修改
    },
  },
}
```

### 关键参数说明

1. **`/api`**: 匹配前缀,所有以 `/api` 开头的请求都会被代理
2. **`target`**: 目标服务器地址
   - 开发环境: `http://localhost:8000`
   - 生产环境: 由环境变量 `VITE_API_BASE_URL` 决定
3. **`changeOrigin: true`**: 修改请求头的origin为目标服务器的origin
4. **`rewrite: (path) => path`**: 路径重写规则
   - 直接透传路径,不做修改
   - 因为前端 `/api/xxx` → 后端 `/api/xxx`
   - 如果后端路由没有 `/api` 前缀,则需要 `rewrite: (path) => path.replace(/^\/api/, '')`

## 后端路由结构

FastAPI后端所有路由都以 `/api` 开头:

```
/api/projects     - 项目管理
/api/chapters     - 章节管理
/api/worldbuilding - 世界观
/api/plot         - 剧情
/api/knowledge    - 知识库
/api/agents       - Agent
/api/prompts      - 提示词
/api/ai           - AI任务
```

## 前端API调用

使用 `src/lib/api.ts` 中的配置:

```typescript
// API客户端会自动添加 /api 前缀
api.get('/projects')        // 请求: /api/projects
api.post('/chapters', ...)  // 请求: /api/chapters
```

## 常见问题

### 1. 404 Not Found

**原因**: 路径配置错误

**检查**:
- 开发环境: 前端请求 `/api/xxx`,后端应该收到 `/api/xxx`
- 生产环境: 检查 `VITE_API_BASE_URL` 是否正确

### 2. CORS错误

**原因**: 后端没有允许前端域名

**解决**:
- 开发环境已配置CORS允许所有域名
- 生产环境需要在 `backend/.env` 中配置 `BACKEND_CORS_ORIGINS`

### 3. 双重路径问题

**错误**: `/api/api/xxx`

**原因**: 路径重写规则配置错误

**解决**:
- 确保 `rewrite: (path) => path` 直接透传
- 不要添加额外的路径替换

### 4. 代理日志查看

开发环境会输出代理日志:

```
[Proxy] GET /api/projects -> http://localhost:8000/api/projects
[Proxy] Response /api/projects -> 200
```

## 测试方法

### 1. 启动后端
```bash
cd backend
python start.py
```

### 2. 启动前端
```bash
cd frontend
npm run dev
```

### 3. 测试API
打开浏览器访问: `http://localhost:3000/api/health`

预期返回:
```json
{
  "status": "healthy"
}
```

## 生产部署注意事项

### 1. 修改 `.env.production`
```bash
VITE_API_BASE_URL=http://your-backend-domain.com
```

### 2. 构建前端
```bash
npm run build
```

### 3. 配置Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-frontend.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API反向代理
    location /api {
        proxy_pass http://your-backend-domain.com:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 总结

- ✅ 开发环境: 使用Vite代理,路径 `/api/xxx` → `http://localhost:8000/api/xxx`
- ✅ 生产环境: 直接请求后端,路径 `/api/xxx` → `http://backend-domain.com/api/xxx`
- ✅ 路径重写规则: `rewrite: (path) => path` 直接透传
- ✅ 后端路由统一以 `/api` 开头
- ✅ 环境变量区分开发和生产配置
