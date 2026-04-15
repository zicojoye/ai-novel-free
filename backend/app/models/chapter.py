#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节数据模型
"""

from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional
from enum import Enum


class ChapterStatus(str, Enum):
    """章节状态"""
    DRAFT = "draft"
    REVIEWING = "reviewing"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ChapterBase(SQLModel):
    """章节基础模型"""
    project_id: int = Field(foreign_key="project.id", description="项目ID")
    chapter_number: int = Field(description="章节序号")
    title: str = Field(description="章节标题")
    content: str = Field(default="", description="章节内容")
    status: ChapterStatus = Field(default=ChapterStatus.DRAFT, description="章节状态")
    outline: Optional[str] = Field(default=None, description="章节大纲")


class Chapter(ChapterBase, table=True):
    """章节表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    word_count: int = Field(default=0, description="字数统计")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")


class ChapterCreate(ChapterBase):
    """创建章节请求"""
    pass


class ChapterUpdate(SQLModel):
    """更新章节请求"""
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[ChapterStatus] = None
    outline: Optional[str] = None


class ChapterRead(ChapterBase):
    """章节响应"""
    id: int
    word_count: int
    created_at: datetime
    updated_at: datetime


class BeatSheetBase(SQLModel):
    """节拍表基础模型"""
    chapter_id: int = Field(foreign_key="chapter.id", description="章节ID")
    beat: str = Field(description="节拍类型")
    description: str = Field(description="节拍描述")
    content: str = Field(default="", description="节拍内容")
    order: int = Field(description="排序")


class BeatSheet(BeatSheetBase, table=True):
    """节拍表"""
    id: Optional[int] = Field(default=None, primary_key=True)


class BeatSheetCreate(BeatSheetBase):
    """创建节拍请求"""
    pass


class BeatSheetRead(BeatSheetBase):
    """节拍响应"""
    id: int
