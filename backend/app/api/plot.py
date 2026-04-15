#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from app.core.database import get_session
from app.models.plot import Foreshadow, ForeshadowCreate, ForeshadowUpdate, ForeshadowRead, Hook, HookCreate, HookUpdate, HookRead


router = APIRouter()


# ===== 伏笔相关 =====

@router.get("/foreshadows", response_model=List[ForeshadowRead])
async def get_foreshadows(
    project_id: int = Query(..., description="项目ID"),
    type: Optional[str] = Query(None, description="伏笔类型"),
    status: Optional[str] = Query(None, description="伏笔状态"),
    session: AsyncSession = Depends(get_session)
):
    """获取伏笔列表"""
    query = select(Foreshadow).where(Foreshadow.project_id == project_id)

    if type:
        query = query.where(Foreshadow.type == type)
    if status:
        query = query.where(Foreshadow.status == status)

    result = await session.exec(query.order_by(Foreshadow.chapter_number))
    return result.all()


@router.get("/foreshadows/{foreshadow_id}", response_model=ForeshadowRead)
async def get_foreshadow(
    foreshadow_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取伏笔详情"""
    foreshadow = await session.get(Foreshadow, foreshadow_id)
    if not foreshadow:
        raise HTTPException(status_code=404, detail="伏笔不存在")
    return foreshadow


@router.post("/foreshadows", response_model=ForeshadowRead)
async def create_foreshadow(
    foreshadow_data: ForeshadowCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建伏笔"""
    foreshadow = Foreshadow(**foreshadow_data.model_dump())
    session.add(foreshadow)
    await session.commit()
    await session.refresh(foreshadow)
    return foreshadow


@router.put("/foreshadows/{foreshadow_id}", response_model=ForeshadowRead)
async def update_foreshadow(
    foreshadow_id: int,
    foreshadow_data: ForeshadowUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新伏笔"""
    foreshadow = await session.get(Foreshadow, foreshadow_id)
    if not foreshadow:
        raise HTTPException(status_code=404, detail="伏笔不存在")

    foreshadow_data_dict = foreshadow_data.model_dump(exclude_unset=True)
    for key, value in foreshadow_data_dict.items():
        setattr(foreshadow, key, value)

    await session.commit()
    await session.refresh(foreshadow)
    return foreshadow


@router.delete("/foreshadows/{foreshadow_id}")
async def delete_foreshadow(
    foreshadow_id: int,
    session: AsyncSession = Depends(get_session)
):
    """删除伏笔"""
    foreshadow = await session.get(Foreshadow, foreshadow_id)
    if not foreshadow:
        raise HTTPException(status_code=404, detail="伏笔不存在")

    await session.delete(foreshadow)
    await session.commit()
    return {"message": "伏笔已删除"}


# ===== 钩子相关 =====

@router.get("/hooks", response_model=List[HookRead])
async def get_hooks(
    project_id: int = Query(..., description="项目ID"),
    session: AsyncSession = Depends(get_session)
):
    """获取钩子列表"""
    result = await session.exec(
        select(Hook)
        .where(Hook.project_id == project_id)
        .order_by(Hook.chapter_number)
    )
    return result.all()


@router.post("/hooks", response_model=HookRead)
async def create_hook(
    hook_data: HookCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建钩子"""
    hook = Hook(**hook_data.model_dump())
    session.add(hook)
    await session.commit()
    await session.refresh(hook)
    return hook


@router.put("/hooks/{hook_id}", response_model=HookRead)
async def update_hook(
    hook_id: int,
    hook_data: HookUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新钩子"""
    hook = await session.get(Hook, hook_id)
    if not hook:
        raise HTTPException(status_code=404, detail="钩子不存在")

    hook_data_dict = hook_data.model_dump(exclude_unset=True)
    for key, value in hook_data_dict.items():
        setattr(hook, key, value)

    await session.commit()
    await session.refresh(hook)
    return hook
