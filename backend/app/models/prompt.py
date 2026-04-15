#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词数据模型
"""

from sqlmodel import Field, SQLModel, Column, JSON
from datetime import datetime
from typing import Optional, List, Any
from enum import Enum


class PromptCategory(str, Enum):
    """提示词分类"""
    WORLDBUILDING = "worldbuilding"
    CHARACTER = "character"
    SCENE = "scene"
    DIALOGUE = "dialogue"
    PLOT = "plot"
    POLISH = "polish"


class PromptVariableType(str, Enum):
    """提示词变量类型"""
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    TEXTAREA = "textarea"


class PromptBase(SQLModel):
    """提示词基础模型"""
    name: str = Field(description="提示词名称")
    category: PromptCategory = Field(description="提示词分类")
    template: str = Field(description="提示词模板")


class Prompt(PromptBase, table=True):
    """提示词表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    usage_count: int = Field(default=0, description="使用次数")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

    # 使用JSON列存储列表
    variables_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    tags_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))


class PromptCreate(PromptBase):
    """创建提示词请求"""
    variables: Optional[List[dict]] = None
    tags: Optional[List[str]] = None


class PromptUpdate(SQLModel):
    """更新提示词请求"""
    name: Optional[str] = None
    category: Optional[PromptCategory] = None
    template: Optional[str] = None
    variables: Optional[List[dict]] = None
    tags: Optional[List[str]] = None


class PromptRead(PromptBase):
    """提示词响应"""
    id: int
    usage_count: int
    variables_data: Optional[Any] = None
    tags_data: Optional[Any] = None
    created_at: datetime
    updated_at: datetime
