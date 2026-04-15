#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI小说平台 - FastAPI后端主入口 (修复版)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import json
from datetime import datetime

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print("AI Novel Platform Backend Starting...")
    yield
    print("AI Novel Platform Backend Shutting down...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI小说创作平台后端API",
    lifespan=lifespan,
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# 模拟项目数据
projects_db = []


@app.get("/api/projects")
async def get_projects():
    """获取项目列表"""
    return {"projects": projects_db, "total": len(projects_db)}


@app.post("/api/projects")
async def create_project(project: dict):
    """创建项目"""
    project["id"] = len(projects_db) + 1
    project["created_at"] = datetime.now().isoformat()
    projects_db.append(project)
    return project


@app.get("/api/projects/{project_id}")
async def get_project(project_id: int):
    """获取项目详情"""
    for project in projects_db:
        if project["id"] == project_id:
            return project
    return JSONResponse(status_code=404, content={"error": "项目不存在"})


@app.get("/api/worldbuilding/project/{project_id}")
async def get_worldbuilding(project_id: int):
    """获取世界观"""
    return {
        "project_id": project_id,
        "core_concept": "",
        "worldbuilding": "",
        "characters": {},
        "factions": {},
        "power_system": "",
        "geography": "",
        "history": "",
        "items": {},
        "main_plot": "",
        "world_rules": {},
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


@app.post("/api/worldbuilding")
async def create_worldbuilding(data: dict):
    """创建世界观"""
    result = {
        "id": 1,
        **data,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    return result


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
        "main_fixed:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True if settings.APP_ENV == "development" else False
    )
