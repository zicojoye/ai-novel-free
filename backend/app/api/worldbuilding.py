#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界观API路由
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.database import get_session
from app.models.worldbuilding import WorldBuilding, WorldBuildingCreate, WorldBuildingUpdate, WorldBuildingRead
from app.models.project import Project


router = APIRouter()


@router.get("/project/{project_id}", response_model=Optional[WorldBuildingRead])
async def get_worldbuilding(
    project_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取世界观"""
    result = await session.exec(
        select(WorldBuilding).where(WorldBuilding.project_id == project_id)
    )
    worldbuilding = result.first()
    return worldbuilding


@router.post("", response_model=WorldBuildingRead)
async def create_worldbuilding(
    worldbuilding_data: WorldBuildingCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建世界观"""
    # 检查项目是否存在
    project = await session.get(Project, worldbuilding_data.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    worldbuilding = WorldBuilding(**worldbuilding_data.model_dump())
    session.add(worldbuilding)
    await session.commit()
    await session.refresh(worldbuilding)
    return worldbuilding


@router.put("/{worldbuilding_id}", response_model=WorldBuildingRead)
async def update_worldbuilding(
    worldbuilding_id: int,
    worldbuilding_data: WorldBuildingUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新世界观"""
    worldbuilding = await session.get(WorldBuilding, worldbuilding_id)
    if not worldbuilding:
        raise HTTPException(status_code=404, detail="世界观不存在")

    worldbuilding_data_dict = worldbuilding_data.model_dump(exclude_unset=True)
    for key, value in worldbuilding_data_dict.items():
        setattr(worldbuilding, key, value)

    await session.commit()
    await session.refresh(worldbuilding)
    return worldbuilding
