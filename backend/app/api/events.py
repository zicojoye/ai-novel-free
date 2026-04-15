#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件流API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_session
from app.models.chat import EventStream, EventType, EventStreamCreate
from app.services.event_service import event_service

router = APIRouter()


# ===== 事件流CRUD =====

@router.get("", response_model=List[EventStream])
async def get_events(
    project_id: int = Query(..., description="项目ID"),
    event_type: Optional[EventType] = Query(None, description="事件类型"),
    source_id: Optional[int] = Query(None, description="事件源ID"),
    limit: int = Query(50, ge=1, le=200, description="数量限制"),
    session: AsyncSession = Depends(get_session)
):
    """获取事件流"""
    stmt = select(EventStream).where(EventStream.project_id == project_id)

    if event_type:
        stmt = stmt.where(EventStream.event_type == event_type)
    if source_id:
        stmt = stmt.where(EventStream.source_id == source_id)

    stmt = stmt.order_by(
        EventStream.importance.desc(),
        EventStream.created_at.desc()
    ).limit(limit)

    result = await session.exec(stmt)
    return result.all()


@router.get("/{event_id}", response_model=EventStream)
async def get_event(
    event_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取事件详情"""
    event = await session.get(EventStream, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")
    return event


@router.post("")
async def create_event(
    event_data: EventStreamCreate
):
    """创建事件"""
    result = await event_service.create_event(
        project_id=event_data.project_id,
        event_type=event_data.event_type,
        source_id=event_data.source_id,
        source_type=event_data.source_type,
        description=event_data.description,
        target_id=event_data.target_id,
        target_type=event_data.target_type,
        data=event_data.data,
        importance=event_data.importance
    )
    return result


# ===== 项目事件 =====

@router.get("/project/{project_id}")
async def get_project_events(
    project_id: int,
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session)
):
    """获取项目事件"""
    events = await event_service.get_project_events(project_id, limit)
    return {
        "success": True,
        "events": events,
        "count": len(events)
    }


@router.get("/project/{project_id}/categorized")
async def get_categorized_events(
    project_id: int
):
    """获取分类的事件流"""
    categories = await event_service.categorize_events(project_id)
    return {
        "success": True,
        "categories": categories
    }


# ===== Agent事件 =====

@router.get("/agent/{agent_id}")
async def get_agent_events(
    agent_id: int,
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session)
):
    """获取Agent事件"""
    events = await event_service.get_agent_events(agent_id, limit)
    return {
        "success": True,
        "events": events,
        "count": len(events)
    }


# ===== 任务事件 =====

@router.get("/task/{task_id}")
async def get_task_events(
    task_id: int,
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session)
):
    """获取任务相关事件"""
    stmt = select(EventStream).where(
        EventStream.task_id == task_id
    ).order_by(
        EventStream.created_at.desc()
    ).limit(limit)

    result = await session.exec(stmt)
    return {
        "success": True,
        "events": result.all(),
        "count": len(result.all())
    }


# ===== 章节事件 =====

@router.get("/chapter/{chapter_id}")
async def get_chapter_events(
    chapter_id: int,
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session)
):
    """获取章节相关事件"""
    stmt = select(EventStream).where(
        EventStream.chapter_id == chapter_id
    ).order_by(
        EventStream.created_at.desc()
    ).limit(limit)

    result = await session.exec(stmt)
    return {
        "success": True,
        "events": result.all(),
        "count": len(result.all())
    }


# ===== 统计信息 =====

@router.get("/stats/{project_id}")
async def get_event_stats(
    project_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取事件统计"""
    # 获取所有事件
    stmt = select(EventStream).where(EventStream.project_id == project_id)
    result = await session.exec(stmt)
    events = result.all()

    # 统计各类事件
    stats = {
        "total": len(events),
        "by_type": {},
        "by_importance": {i: 0 for i in range(1, 11)},
        "by_source": {}
    }

    for event in events:
        # 按类型统计
        type_name = event.event_type.value
        stats["by_type"][type_name] = stats["by_type"].get(type_name, 0) + 1

        # 按重要性统计
        stats["by_importance"][event.importance] += 1

        # 按来源统计
        source_key = f"{event.source_type}_{event.source_id}"
        stats["by_source"][source_key] = stats["by_source"].get(source_key, 0) + 1

    return stats
