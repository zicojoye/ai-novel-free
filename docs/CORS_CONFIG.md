# CORS跨域配置说明

## 当前配置

### 后端配置

**位置**: `backend/main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)
```

**说明**:
- ✅ 允许所有来源的跨域请求
- ✅ 支持携带凭证(Cookie、Authorization)
- ✅ 允许所有HTTP方法(GET、POST、PUT、DELETE等)
- ✅ 允许所有请求头

### 前端配置

**位置**: `frontend/.env`

```bash
VITE_API_BASE_URL=/api
```

**说明**:
- 使用相对路径 `/api`
- Vite开发服务器会自动代理到后端
- 支持局域网访问(其他设备可通过IP访问)

**位置**: `frontend/vite.config.ts`

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path,
  }
}
```

## 工作原理

### 开发环境

```
浏览器: http://localhost:3000/api/projects
  ↓
Vite代理: 拦截 /api 请求
  ↓
后端: http://localhost:8000/api/projects
```

### 生产环境

```
前端: https://your-frontend.com/api/projects
  ↓
Nginx反向代理: /api 路径
  ↓
后端: http://localhost:8000/api/projects
```

## 支持的访问方式

### 1. 本地访问
- 前端: http://localhost:3000
- 后端: http://localhost:8000

### 2. 局域网访问
- 前端: http://192.168.1.100:3000
- 后端: http://192.168.1.100:8000

### 3. 外网访问(需要配置)
- 前端: http://your-domain.com
- 后端: http://your-backend-domain.com

## 常见问题

### 1. CORS错误

**症状**: 浏览器控制台显示CORS错误

**解决方案**:
- 检查后端是否允许CORS(已配置为允许所有来源)
- 检查前端请求URL是否正确
- 清除浏览器缓存

### 2. 代理不生效

**症状**: 前端请求失败,没有看到代理日志

**解决方案**:
- 确认前端请求以 `/api` 开头
- 检查 Vite 配置中的 proxy 设置
- 重启前端开发服务器

### 3. 局域网无法访问

**症状**: 其他设备无法访问

**解决方案**:
- 确认防火墙允许端口访问
- 前端和后端都使用 `0.0.0.0` 或 `host: true`
- 检查路由器端口转发配置

## 生产环境部署建议

虽然当前配置允许所有来源,但在生产环境中建议:

### 1. 限制CORS来源

```python
# backend/main.py
from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.com",
        "https://www.your-frontend.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 使用HTTPS

- 后端配置SSL证书
- 前端使用HTTPS协议
- 强制HTTPS跳转

### 3. 添加安全头

已在 `backend/app/core/middleware.py` 中配置:
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Content-Security-Policy

## 测试CORS

### 1. 使用浏览器
```javascript
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(console.log)
```

### 2. 使用curl
```bash
curl -X OPTIONS http://localhost:8000/api/health \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -v
```

### 3. 使用Postman
- 导入API文档: http://localhost:8000/docs
- 测试各个接口

## 总结

当前配置:
- ✅ 后端允许所有来源跨域请求
- ✅ 前端使用Vite代理
- ✅ 支持本地、局域网访问
- ✅ 开发和测试友好

生产环境建议:
- ⚠️  限制CORS来源到指定域名
- ⚠️  使用HTTPS协议
- ⚠️  配置反向代理(Nginx)
