#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情与伏笔数据模型
"""

from sqlmodel import Field, SQLModel, Column, JSON
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ForeshadowType(str, Enum):
    """伏笔类型"""
    CHEKHOVS_GUN = "chekhovs_gun"
    GRASS_SNAKE = "grass_snake"
    SUSPENSE = "suspense"
    SETUP = "setup"
    FORESHADOWING = "foreshadowing"
    CALLBACK = "callback"
    PAYOFF = "payoff"
    TWIST = "twist"
    HOOK = "hook"
    ECHO = "echo"


class ForeshadowStatus(str, Enum):
    """伏笔状态"""
    SETUP = "setup"
    CALLBACK = "callback"
    PAID_OFF = "paid_off"
    FORGOTTEN = "forgotten"


class ForeshadowBase(SQLModel):
    """伏笔基础模型"""
    project_id: int = Field(foreign_key="project.id", description="项目ID")
    type: ForeshadowType = Field(description="伏笔类型")
    title: str = Field(description="伏笔标题")
    description: str = Field(description="伏笔描述")
    chapter_id: Optional[int] = Field(default=None, description="关联章节ID")
    chapter_number: int = Field(description="章节序号")
    status: ForeshadowStatus = Field(default=ForeshadowStatus.SETUP, description="伏笔状态")
    related_foreshadows: Optional[str] = Field(default="", description="关联伏笔")


class Foreshadow(ForeshadowBase, table=True):
    """伏笔表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

    # 使用JSON列存储列表
    related_foreshadows_data: Optional[str] = Field(default="", description="关联伏笔数据")


class ForeshadowCreate(ForeshadowBase):
    """创建伏笔请求"""
    pass


class ForeshadowUpdate(SQLModel):
    """更新伏笔请求"""
    type: Optional[ForeshadowType] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ForeshadowStatus] = None
    related_foreshadows: Optional[str] = None


class ForeshadowRead(ForeshadowBase):
    """伏笔响应"""
    id: int
    created_at: datetime
    updated_at: datetime


class HookBase(SQLModel):
    """钩子基础模型"""
    project_id: int = Field(foreign_key="project.id", description="项目ID")
    chapter_id: Optional[int] = Field(default=None, description="关联章节ID")
    chapter_number: int = Field(description="章节序号")
    content: str = Field(description="钩子内容")
    is_triggered: bool = Field(default=False, description="是否已触发")
    triggered_at: Optional[datetime] = Field(default=None, description="触发时间")


class Hook(HookBase, table=True):
    """钩子表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")


class HookCreate(HookBase):
    """创建钩子请求"""
    pass


class HookUpdate(SQLModel):
    """更新钩子请求"""
    content: Optional[str] = None
    is_triggered: Optional[bool] = None


class HookRead(HookBase):
    """钩子响应"""
    id: int
    created_at: datetime
    triggered_at: Optional[datetime] = None
