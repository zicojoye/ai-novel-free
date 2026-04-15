#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI小说平台 - FastAPI后端主入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import sys
from pathlib import Path

from app.core.config import settings
from app.core.database import init_db
from app.core.middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    XSSProtectionMiddleware,
    SQLInjectionProtectionMiddleware
)
from app.api import (
    projects, chapters, worldbuilding, plot,
    knowledge, agents, prompts, ai_tasks,
    websocket, chat, events, models
)


# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    base_dir = Path(__file__).parent
    directories = [
        base_dir / "data",
        base_dir / "data" / "uploads",
        base_dir / "data" / "logs",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("=" * 60)
    print("🚀 AI Novel Platform Backend Starting...")
    print("=" * 60)
    print()

    # 确保目录存在
    print("📁 检查数据目录...")
    ensure_directories()
    print()

    # 初始化数据库
    print("📊 初始化数据库...")
    try:
        await init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
        print("✓ Continuing with minimal mode...")
    print()

    print("✅ Backend startup complete!")
    print()
    print("=" * 60)
    print()
    print("📱 访问地址:")
    print(f"   - API: http://localhost:{settings.BACKEND_PORT}")
    print(f"   - Docs: http://localhost:{settings.BACKEND_PORT}/docs")
    print(f"   - Health: http://localhost:{settings.BACKEND_PORT}/health")
    print()
    print("=" * 60)
    print()

    yield

    # 关闭时
    print()
    print("=" * 60)
    print("🛑 AI Novel Platform Backend Shutting down...")
    print("=" * 60)
    print()


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI小说创作平台后端API",
    lifespan=lifespan,
)

# 添加安全中间件
# 限流中间件
app.add_middleware(RateLimitMiddleware, max_requests=60, window=60)
# 安全响应头中间件
app.add_middleware(SecurityHeadersMiddleware)
# XSS防护中间件
app.add_middleware(XSSProtectionMiddleware)
# SQL注入防护中间件
app.add_middleware(SQLInjectionProtectionMiddleware)

# 统一配置CORS,允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(projects.router, prefix="/api/projects", tags=["项目"])
app.include_router(chapters.router, prefix="/api/chapters", tags=["章节"])
app.include_router(worldbuilding.router, prefix="/api/worldbuilding", tags=["世界观"])
app.include_router(plot.router, prefix="/api/plot", tags=["剧情"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识库"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agent"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["提示词"])
app.include_router(ai_tasks.router, prefix="/api/ai", tags=["AI任务"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])
app.include_router(events.router, prefix="/api/events", tags=["事件流"])
app.include_router(models.router, prefix="/api/models", tags=["AI模型"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI Novel Platform API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "message": "服务器内部错误"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True if settings.APP_ENV == "development" else False
    )
