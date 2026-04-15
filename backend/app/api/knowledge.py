#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from app.core.database import get_session
from app.models.knowledge import KnowledgeEntry, KnowledgeEntryCreate, KnowledgeEntryUpdate, KnowledgeEntryRead


router = APIRouter()


@router.get("", response_model=List[KnowledgeEntryRead])
async def get_knowledge_entries(
    project_id: int = Query(..., description="项目ID"),
    type: Optional[str] = Query(None, description="知识类型"),
    tag: Optional[str] = Query(None, description="标签"),
    session: AsyncSession = Depends(get_session)
):
    """获取知识条目列表"""
    query = select(KnowledgeEntry).where(KnowledgeEntry.project_id == project_id)

    if type:
        query = query.where(KnowledgeEntry.type == type)
    if tag:
        query = query.where(KnowledgeEntry.tags_data.any(tag))

    result = await session.exec(query.order_by(KnowledgeEntry.created_at.desc()))
    return result.all()


@router.get("/{knowledge_id}", response_model=KnowledgeEntryRead)
async def get_knowledge_entry(
    knowledge_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取知识条目详情"""
    entry = await session.get(KnowledgeEntry, knowledge_id)
    if not entry:
        raise HTTPException(status_code=404, detail="知识条目不存在")
    return entry


@router.post("", response_model=KnowledgeEntryRead)
async def create_knowledge_entry(
    entry_data: KnowledgeEntryCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建知识条目"""
    entry = KnowledgeEntry(**entry_data.model_dump())
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


@router.put("/{knowledge_id}", response_model=KnowledgeEntryRead)
async def update_knowledge_entry(
    knowledge_id: int,
    entry_data: KnowledgeEntryUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新知识条目"""
    entry = await session.get(KnowledgeEntry, knowledge_id)
    if not entry:
        raise HTTPException(status_code=404, detail="知识条目不存在")

    entry_data_dict = entry_data.model_dump(exclude_unset=True)
    for key, value in entry_data_dict.items():
        setattr(entry, key, value)

    await session.commit()
    await session.refresh(entry)
    return entry


@router.delete("/{knowledge_id}")
async def delete_knowledge_entry(
    knowledge_id: int,
    session: AsyncSession = Depends(get_session)
):
    """删除知识条目"""
    entry = await session.get(KnowledgeEntry, knowledge_id)
    if not entry:
        raise HTTPException(status_code=404, detail="知识条目不存在")

    await session.delete(entry)
    await session.commit()
    return {"message": "知识条目已删除"}


@router.post("/extract/{project_id}")
async def extract_knowledge(
    project_id: int,
    chapter_id: int = Query(..., description="章节ID"),
    session: AsyncSession = Depends(get_session)
):
    """AI提取知识"""
    # TODO: 实现AI知识提取
    return {"message": "知识提取功能开发中"}
