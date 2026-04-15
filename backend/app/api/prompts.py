#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_session
from app.models.prompt import Prompt, PromptCreate, PromptUpdate, PromptRead


router = APIRouter()


@router.get("", response_model=List[PromptRead])
async def get_prompts(
    category: Optional[str] = Query(None, description="提示词分类"),
    tag: Optional[str] = Query(None, description="标签"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    session: AsyncSession = Depends(get_session)
):
    """获取提示词列表"""
    query = select(Prompt)

    if category:
        query = query.where(Prompt.category == category)
    if tag:
        query = query.where(Prompt.tags_data.any(tag))
    if search:
        query = query.where(Prompt.name.contains(search))

    result = await session.exec(
        query.order_by(Prompt.usage_count.desc())
    )
    return result.all()


@router.get("/{prompt_id}", response_model=PromptRead)
async def get_prompt(
    prompt_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取提示词详情"""
    prompt = await session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")
    return prompt


@router.post("", response_model=PromptRead)
async def create_prompt(
    prompt_data: PromptCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建提示词"""
    prompt = Prompt(**prompt_data.model_dump())
    session.add(prompt)
    await session.commit()
    await session.refresh(prompt)
    return prompt


@router.put("/{prompt_id}", response_model=PromptRead)
async def update_prompt(
    prompt_id: int,
    prompt_data: PromptUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新提示词"""
    prompt = await session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")

    prompt_data_dict = prompt_data.model_dump(exclude_unset=True)
    for key, value in prompt_data_dict.items():
        setattr(prompt, key, value)

    await session.commit()
    await session.refresh(prompt)
    return prompt


@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: int,
    session: AsyncSession = Depends(get_session)
):
    """删除提示词"""
    prompt = await session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")

    await session.delete(prompt)
    await session.commit()
    return {"message": "提示词已删除"}


@router.post("/{prompt_id}/use")
async def use_prompt(
    prompt_id: int,
    variables: dict,
    session: AsyncSession = Depends(get_session)
):
    """使用提示词"""
    prompt = await session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")

    # 替换变量
    template = prompt.template
    for key, value in variables.items():
        template = template.replace(f"{{{key}}}", str(value))

    # 增加使用次数
    prompt.usage_count += 1
    await session.commit()

    return {
        "prompt_id": prompt_id,
        "rendered_template": template,
        "usage_count": prompt.usage_count
    }
