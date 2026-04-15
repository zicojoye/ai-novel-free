#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目数据模型
"""

from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional
from enum import Enum


class ProjectStatus(str, Enum):
    """项目状态"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ProjectBase(SQLModel):
    """项目基础模型"""
    name: str = Field(index=True, description="项目名称")
    description: Optional[str] = Field(default=None, description="项目描述")
    genre: str = Field(description="题材类型")
    target_audience: str = Field(description="目标读者")
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT, description="项目状态")


class Project(ProjectBase, table=True):
    """项目表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")


class ProjectCreate(ProjectBase):
    """创建项目请求"""
    pass


class ProjectUpdate(SQLModel):
    """更新项目请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    target_audience: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectRead(ProjectBase):
    """项目响应"""
    id: int
    created_at: datetime
    updated_at: datetime
