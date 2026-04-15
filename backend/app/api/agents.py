#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent API路由
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
import asyncio

from app.core.database import get_session, async_session_maker
from app.models.agent import Agent, AgentCreate, AgentUpdate, AgentRead, AgentTask, AgentTaskCreate, AgentTaskUpdate, AgentTaskRead, TaskStatus
from app.agents.agent_manager import agent_manager


router = APIRouter()


# ===== Agent相关 =====

@router.get("", response_model=List[AgentRead])
async def get_agents(
    session: AsyncSession = Depends(get_session)
):
    """获取Agent列表"""
    result = await session.exec(select(Agent))
    return result.all()


@router.get("/{agent_id}", response_model=AgentRead)
async def get_agent(
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取Agent详情"""
    agent = await session.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")
    return agent


@router.post("", response_model=AgentRead)
async def create_agent(
    agent_data: AgentCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建Agent"""
    agent = Agent(**agent_data.model_dump())
    session.add(agent)
    await session.commit()
    await session.refresh(agent)
    return agent


@router.put("/{agent_id}", response_model=AgentRead)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新Agent"""
    agent = await session.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")

    agent_data_dict = agent_data.model_dump(exclude_unset=True)
    for key, value in agent_data_dict.items():
        setattr(agent, key, value)

    await session.commit()
    await session.refresh(agent)
    return agent


# ===== Agent任务相关 =====

@router.get("/{agent_id}/tasks", response_model=List[AgentTaskRead])
async def get_agent_tasks(
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取Agent任务列表"""
    result = await session.exec(
        select(AgentTask)
        .where(AgentTask.agent_id == agent_id)
        .order_by(AgentTask.created_at.desc())
    )
    return result.all()


@router.post("/tasks", response_model=AgentTaskRead)
async def create_agent_task(
    task_data: AgentTaskCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建Agent任务"""
    task = AgentTask(**task_data.model_dump())
    task.status = TaskStatus.PENDING
    task.progress = 0
    session.add(task)
    await session.commit()
    await session.refresh(task)

    # 异步执行任务
    asyncio.create_task(execute_task_background(task.id))

    return task


async def execute_task_background(task_id: int):
    """后台执行任务"""
    from app.models.agent import AgentTask, TaskStatus

    async with async_session_maker() as session:
        task = await session.get(AgentTask, task_id)
        if not task:
            return

        try:
            # 使用AgentManager执行
            result = await agent_manager.execute_task(
                agent_id=task.agent_id,
                task=task.input
            )

            # 更新任务状态
            task.status = TaskStatus.COMPLETED if result.get("success") else TaskStatus.FAILED
            task.output = result.get("output")
            task.error = result.get("error")
            task.updated_at = datetime.utcnow()
            await session.commit()

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.updated_at = datetime.utcnow()
            await session.commit()


@router.put("/tasks/{task_id}", response_model=AgentTaskRead)
async def update_agent_task(
    task_id: int,
    task_data: AgentTaskUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新Agent任务"""
    task = await session.get(AgentTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    task_data_dict = task_data.model_dump(exclude_unset=True)
    for key, value in task_data_dict.items():
        setattr(task, key, value)

    await session.commit()
    await session.refresh(task)
    return task


@router.post("/tasks/{task_id}/execute")
async def execute_agent_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """执行Agent任务"""
    # 获取任务
    task = await session.get(AgentTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 更新任务状态为运行中
    task.status = TaskStatus.RUNNING
    await session.commit()

    try:
        # 调用Agent执行任务
        result = await agent_manager.execute_task(
            agent_id=task.agent_id,
            task=task.input
        )

        # 更新任务状态
        if result.get("success"):
            task.status = TaskStatus.COMPLETED
            task.output = result
        else:
            task.status = TaskStatus.FAILED
            task.error = result.get("error")

        await session.commit()

        return result
    except Exception as e:
        task.status = TaskStatus.FAILED
        task.error = str(e)
        await session.commit()
        raise HTTPException(status_code=500, detail=str(e))
