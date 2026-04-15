#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent数据模型
"""

from sqlmodel import Field, SQLModel, Column, JSON
from datetime import datetime
from typing import Optional, Any
from enum import Enum


class AgentStatus(str, Enum):
    """Agent状态"""
    IDLE = "idle"
    ACTIVE = "active"
    COMPLETED = "completed"
    ERROR = "error"


class AgentRole(str, Enum):
    """Agent角色"""
    AUTHOR = "author"
    EDITOR = "editor"
    REVIEWER = "reviewer"
    PUBLISHER = "publisher"
    WORLD_BUILDER = "world_builder"
    CHARACTER_CREATOR = "character_creator"
    PLOT_DESIGNER = "plot_designer"
    KNOWLEDGE_MANAGER = "knowledge_manager"
    LOGIC_CHECKER = "logic_checker"
    STYLE_CHECKER = "style_checker"
    COMPLIANCE_CHECKER = "compliance_checker"
    SEMANTIC_RETRIEVER = "semantic_retriever"


class AgentBase(SQLModel):
    """Agent基础模型"""
    name: str = Field(description="Agent名称")
    role: AgentRole = Field(description="Agent角色")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Agent状态")
    tasks_completed: int = Field(default=0, description="已完成任务数")


class Agent(AgentBase, table=True):
    """Agent表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    last_activity: Optional[datetime] = Field(default=None, description="最后活动时间")


class AgentCreate(AgentBase):
    """创建Agent请求"""
    pass


class AgentUpdate(SQLModel):
    """更新Agent请求"""
    status: Optional[AgentStatus] = None
    tasks_completed: Optional[int] = None


class AgentRead(AgentBase):
    """Agent响应"""
    id: int
    last_activity: Optional[datetime] = None


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentTaskBase(SQLModel):
    """Agent任务基础模型"""
    agent_id: int = Field(foreign_key="agent.id", description="Agent ID")
    project_id: int = Field(foreign_key="project.id", description="项目ID")
    task_type: str = Field(description="任务类型")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    input: Optional[str] = Field(default="", description="任务输入")
    progress: int = Field(default=0, description="任务进度")


class AgentTask(AgentTaskBase, table=True):
    """Agent任务表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    output: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON), description="任务输出")
    error: Optional[str] = Field(default=None, description="错误信息")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")


class AgentTaskCreate(AgentTaskBase):
    """创建Agent任务请求"""
    pass


class AgentTaskUpdate(SQLModel):
    """更新Agent任务请求"""
    status: Optional[TaskStatus] = None
    output: Optional[dict] = None
    error: Optional[str] = None
    progress: Optional[int] = None


class AgentTaskRead(AgentTaskBase):
    """Agent任务响应"""
    id: int
    output: Optional[dict] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
