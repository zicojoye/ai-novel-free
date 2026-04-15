#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界观数据模型
"""

from sqlmodel import Field, SQLModel, Column, JSON
from sqlalchemy import String
from typing import Optional


class WorldBuildingBase(SQLModel):
    """世界观基础模型"""
    project_id: int = Field(foreign_key="project.id", description="项目ID")
    core_concept: Optional[str] = Field(default="", description="核心设定")
    worldbuilding: Optional[str] = Field(default="", description="世界观")
    characters: Optional[str] = Field(default="", description="角色系统")
    factions: Optional[str] = Field(default="", description="势力体系")
    power_system: Optional[str] = Field(default="", description="力量体系")
    geography: Optional[str] = Field(default="", description="地理环境")
    history: Optional[str] = Field(default="", description="历史背景")
    items: Optional[str] = Field(default="", description="道具物品")
    main_plot: Optional[str] = Field(default="", description="剧情主线")
    world_rules: Optional[str] = Field(default="", description="世界规则")


class WorldBuilding(WorldBuildingBase, table=True):
    """世界观表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[str] = Field(default=None, description="创建时间")
    updated_at: Optional[str] = Field(default=None, description="更新时间")

    # 使用JSON列存储复杂数据
    characters_data: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column("characters_data", JSON),
        description="角色数据"
    )
    factions_data: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column("factions_data", JSON),
        description="势力数据"
    )
    items_data: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column("items_data", JSON),
        description="物品数据"
    )
    world_rules_data: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column("world_rules_data", JSON),
        description="世界规则数据"
    )


class WorldBuildingCreate(WorldBuildingBase):
    """创建世界观请求"""
    pass


class WorldBuildingUpdate(SQLModel):
    """更新世界观请求"""
    core_concept: Optional[str] = None
    worldbuilding: Optional[str] = None
    characters: Optional[dict] = None
    factions: Optional[dict] = None
    power_system: Optional[str] = None
    geography: Optional[str] = None
    history: Optional[str] = None
    items: Optional[dict] = None
    main_plot: Optional[str] = None
    world_rules: Optional[dict] = None


class WorldBuildingRead(WorldBuildingBase):
    """世界观响应"""
    id: int
    created_at: str
    updated_at: str
