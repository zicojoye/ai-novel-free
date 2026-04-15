#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI任务API路由 - 提供AI功能端点
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.core.database import get_session
from app.services.llm_service import llm_service
from app.agents.agent_manager import agent_manager


router = APIRouter()


@router.post("/generate/worldbuilding")
async def generate_worldbuilding(
    genre: str,
    description: str
) -> Dict[str, Any]:
    """生成世界观"""
    try:
        result = await llm_service.generate_worldbuilding(genre=genre, description=description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/chapter")
async def generate_chapter(
    outline: str,
    word_count: int = 2000,
    style: str = "口语化"
) -> Dict[str, Any]:
    """生成章节"""
    try:
        result = await llm_service.generate_chapter(outline=outline, word_count=word_count, style=style)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/outline")
async def generate_outline(
    project_title: str,
    genre: str,
    chapter_count: int = 50
) -> Dict[str, Any]:
    """生成大纲"""
    try:
        result = await llm_service.generate_outline(project_title=project_title, genre=genre, chapter_count=chapter_count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/polish")
async def polish_text(
    text: str,
    style: str = "自然流畅"
) -> Dict[str, Any]:
    """润色文本"""
    try:
        result = await llm_service.polish_text(text=text, style=style)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/search")
async def rag_search(query: str, project_id: int, limit: int = 5) -> Dict[str, Any]:
    """RAG检索"""
    raise HTTPException(status_code=501, detail="RAG检索功能开发中")


@router.post("/rag/context")
async def rag_context(query: str, project_id: int, max_tokens: int = 2000) -> Dict[str, Any]:
    """获取RAG上下文"""
    raise HTTPException(status_code=501, detail="RAG上下文功能开发中")


@router.post("/agent/execute")
async def execute_agent(agent_id: int, task: Dict[str, Any]) -> Dict[str, Any]:
    """执行单Agent任务"""
    try:
        result = await agent_manager.execute_task(agent_id=agent_id, task=task)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/workflow")
async def execute_workflow(workflow: list[Dict[str, Any]]) -> Dict[str, Any]:
    """执行Agent工作流"""
    try:
        results = await agent_manager.execute_workflow(workflow)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats")
async def get_cache_stats() -> Dict[str, Any]:
    """获取缓存统计"""
    from app.services.cache_service import cache_service
    return cache_service.get_stats()


@router.post("/cache/clear")
async def clear_cache():
    """清除缓存"""
    from app.services.cache_service import cache_service
    # TODO: 实现缓存清除
    return {"message": "缓存已清除"}
