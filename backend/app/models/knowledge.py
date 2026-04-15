#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库数据模型
"""

from sqlmodel import Field, SQLModel, Column, JSON, Float
from datetime import datetime
from typing import Optional, List
from enum import Enum


class KnowledgeType(str, Enum):
    """知识类型"""
    CHARACTER = "character"
    PLOT = "plot"
    SETTING = "setting"
    SYSTEM = "system"
    OTHER = "other"


class KnowledgeEntryBase(SQLModel):
    """知识条目基础模型"""
    project_id: int = Field(foreign_key="project.id", description="项目ID")
    type: KnowledgeType = Field(description="知识类型")
    title: str = Field(description="知识标题")
    content: str = Field(description="知识内容")
    tags: Optional[str] = Field(default="", description="标签")
    source_chapter_id: Optional[int] = Field(default=None, description="来源章节ID")


class KnowledgeEntry(KnowledgeEntryBase, table=True):
    """知识条目表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

    # 使用JSON列存储复杂数据
    tags_data: Optional[str] = Field(default="", description="标签数据")
    embedding_data: Optional[str] = Field(default="", description="向量数据")


class KnowledgeEntryCreate(KnowledgeEntryBase):
    """创建知识条目请求"""
    pass


class KnowledgeEntryUpdate(SQLModel):
    """更新知识条目请求"""
    type: Optional[KnowledgeType] = None
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class KnowledgeEntryRead(KnowledgeEntryBase):
    """知识条目响应"""
    id: int
    created_at: datetime
    updated_at: datetime
