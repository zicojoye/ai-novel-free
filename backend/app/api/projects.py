#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from app.core.database import get_session
from app.models.project import Project, ProjectCreate, ProjectUpdate, ProjectRead


router = APIRouter()


@router.get("", response_model=List[ProjectRead])
async def get_projects(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量"),
    session: AsyncSession = Depends(get_session)
):
    """获取项目列表"""
    result = await session.exec(
        select(Project)
        .offset((page - 1) * pageSize)
        .limit(pageSize)
        .order_by(Project.created_at.desc())
    )
    return result.all()


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取项目详情"""
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return project


@router.post("", response_model=ProjectRead)
async def create_project(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建项目"""
    project = Project(**project_data.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新项目"""
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    project_data_dict = project_data.model_dump(exclude_unset=True)
    for key, value in project_data_dict.items():
        setattr(project, key, value)

    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_session)
):
    """删除项目"""
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    await session.delete(project)
    await session.commit()
    return {"message": "项目已删除"}


@router.get("/stats/count", response_model=dict)
async def get_project_count(
    session: AsyncSession = Depends(get_session)
):
    """获取项目统计"""
    total = await session.exec(select(func.count(Project.id)))
    active = await session.exec(
        select(func.count(Project.id)).where(Project.status == "active")
    )
    return {
        "total": total.one(),
        "active": active.one()
    }
