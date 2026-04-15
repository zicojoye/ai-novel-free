#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的数据模型测试
"""

from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional


class WorldBuilding(SQLModel, table=True):
    """世界观表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(description="项目ID")
    core_concept: Optional[str] = Field(default="", description="核心设定")
    characters_data: Optional[str] = Field(default="{}", description="角色数据(JSON)")
    created_at: Optional[str] = Field(default=None, description="创建时间")
