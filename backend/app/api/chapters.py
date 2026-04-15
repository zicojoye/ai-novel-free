#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_session
from app.models.chapter import Chapter, ChapterCreate, ChapterUpdate, ChapterRead


router = APIRouter()


@router.get("", response_model=List[ChapterRead])
async def get_chapters(
    project_id: int = Query(..., description="项目ID"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量"),
    session: AsyncSession = Depends(get_session)
):
    """获取章节列表"""
    result = await session.exec(
        select(Chapter)
        .where(Chapter.project_id == project_id)
        .offset((page - 1) * pageSize)
        .limit(pageSize)
        .order_by(Chapter.chapter_number)
    )
    return result.all()


@router.get("/{chapter_id}", response_model=ChapterRead)
async def get_chapter(
    chapter_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取章节详情"""
    chapter = await session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")
    return chapter


@router.post("", response_model=ChapterRead)
async def create_chapter(
    chapter_data: ChapterCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建章节"""
    # 计算字数
    word_count = len(chapter_data.content)

    chapter = Chapter(
        **chapter_data.model_dump(),
        word_count=word_count
    )
    session.add(chapter)
    await session.commit()
    await session.refresh(chapter)
    return chapter


@router.put("/{chapter_id}", response_model=ChapterRead)
async def update_chapter(
    chapter_id: int,
    chapter_data: ChapterUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新章节"""
    chapter = await session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    chapter_data_dict = chapter_data.model_dump(exclude_unset=True)

    # 更新内容时重新计算字数
    if "content" in chapter_data_dict:
        chapter_data_dict["word_count"] = len(chapter_data_dict["content"])

    for key, value in chapter_data_dict.items():
        setattr(chapter, key, value)

    await session.commit()
    await session.refresh(chapter)
    return chapter


@router.delete("/{chapter_id}")
async def delete_chapter(
    chapter_id: int,
    session: AsyncSession = Depends(get_session)
):
    """删除章节"""
    chapter = await session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    await session.delete(chapter)
    await session.commit()
    return {"message": "章节已删除"}
