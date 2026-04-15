#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界观数据模型 - 修复版
"""

from sqlmodel import Field, SQLModel
from typing import Optional


class WorldBuilding(SQLModel, table=True):
    """世界观表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(description="项目ID")
    core_concept: Optional[str] = Field(default="", description="核心设定")
    worldbuilding: Optional[str] = Field(default="", description="世界观")
    # 使用String存储JSON,在API层处理
    characters_data: Optional[str] = Field(default="{}", description="角色数据(JSON)")
    factions_data: Optional[str] = Field(default="{}", description="势力数据(JSON)")
    power_system: Optional[str] = Field(default="", description="力量体系")
    geography: Optional[str] = Field(default="", description="地理环境")
    history: Optional[str] = Field(default="", description="历史背景")
    items_data: Optional[str] = Field(default="{}", description="物品数据(JSON)")
    main_plot: Optional[str] = Field(default="", description="剧情主线")
    world_rules_data: Optional[str] = Field(default="{}", description="世界规则数据(JSON)")
    created_at: Optional[str] = Field(default=None, description="创建时间")
    updated_at: Optional[str] = Field(default=None, description="更新时间")


class WorldBuildingCreate(SQLModel):
    """创建世界观请求"""
    project_id: int
    core_concept: str = ""
    worldbuilding: str = ""
    characters: dict = {}
    factions: dict = {}
    power_system: str = ""
    geography: str = ""
    history: str = ""
    items: dict = {}
    main_plot: str = ""
    world_rules: dict = {}


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


class WorldBuildingRead(SQLModel):
    """世界观响应"""
    id: int
    project_id: int
    core_concept: str
    worldbuilding: str
    characters: dict
    factions: dict
    power_system: str
    geography: str
    history: str
    items: dict
    main_plot: str
    world_rules: dict
    created_at: str
    updated_at: str
