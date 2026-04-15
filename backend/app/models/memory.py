#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆系统模型
"""

from sqlmodel import Field, SQLModel, Column, JSON, Text
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class MemoryType(str, Enum):
    """记忆类型"""
    STM = "stm"
    LTM = "ltm"
    WM = "wm"


class MemoryOperation(str, Enum):
    """Text2Mem 12个原子操作"""
    CREATE = "create_memory"
    READ = "read_memory"
    UPDATE = "update_memory"
    DELETE = "delete_memory"
    SEARCH = "search_memory"
    LINK = "link_memory"
    PRIORITIZE = "prioritize_memory"
    ARCHIVE = "archive_memory"
    RECALL = "recall_memory"
    MERGE = "merge_memory"
    SPLIT = "split_memory"
    VERIFY = "verify_memory"


class MemoryPriority(int, Enum):
    """记忆优先级"""
    CRITICAL = 10
    HIGH = 8
    MEDIUM = 5
    LOW = 3
    TRIVIAL = 1


class MemoryStatus(str, Enum):
    """记忆状态"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    VERIFIED = "verified"
    CONFLICT = "conflict"


class Memory(SQLModel, table=True):
    """记忆表"""
    __tablename__ = "memories"

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int = Field(description="Agent ID")
    project_id: int = Field(description="项目ID")
    memory_type: MemoryType = Field(description="记忆类型")
    content: str = Field(description="记忆内容")
    summary: Optional[str] = Field(default=None, description="摘要")
    priority: int = Field(default=5, description="优先级")
    importance_score: float = Field(default=5.0, description="重要性评分")
    status: MemoryStatus = Field(default=MemoryStatus.ACTIVE, description="状态")
    version: int = Field(default=1, description="版本号")
    parent_id: Optional[int] = Field(default=None, description="父记忆ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    last_accessed: Optional[datetime] = Field(default=None, description="最后访问时间")
    access_count: int = Field(default=0, description="访问次数")
    verified: bool = Field(default=False, description="是否已验证")

    # JSON字段
    tags_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    metadata_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    linked_memory_ids_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    embedding: Optional[Any] = Field(default=None, sa_column=Column(JSON))


class MemoryCreate(SQLModel):
    """创建记忆请求"""
    agent_id: int
    project_id: int
    memory_type: MemoryType
    content: str
    summary: Optional[str] = None
    priority: int = 5
    importance_score: float = 5.0
    tags: Optional[List[str]] = None
    meta: Optional[Dict[str, Any]] = None


class MemoryUpdate(SQLModel):
    """更新记忆请求"""
    content: Optional[str] = None
    summary: Optional[str] = None
    priority: Optional[int] = None
    importance_score: Optional[float] = None
    tags: Optional[List[str]] = None
    status: Optional[MemoryStatus] = None


class MemoryRead(SQLModel):
    """记忆响应"""
    id: int
    agent_id: int
    project_id: int
    memory_type: MemoryType
    content: str
    summary: Optional[str] = None
    priority: int
    importance_score: float
    status: MemoryStatus
    version: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    last_accessed: Optional[datetime] = None
    access_count: int
    verified: bool
    tags_data: Optional[Any] = None


class MemoryOperationLog(SQLModel, table=True):
    """记忆操作日志表"""
    __tablename__ = "memory_operation_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    memory_id: int = Field(description="记忆ID")
    operation: MemoryOperation = Field(description="操作类型")
    performed_by: int = Field(description="执行者ID")
    performed_at: datetime = Field(default_factory=datetime.utcnow, description="执行时间")
    result: str = Field(description="操作结果")
    error_message: Optional[str] = Field(default=None, description="错误信息")

    # JSON字段
    operation_data_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))


class AgentKnowledge(SQLModel, table=True):
    """Agent知识库表"""
    __tablename__ = "agent_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int = Field(description="Agent ID")
    project_id: int = Field(description="项目ID")
    knowledge_type: str = Field(description="知识类型")
    title: str = Field(description="知识标题")
    content: str = Field(description="知识内容")
    source: str = Field(default="manual", description="来源")
    confidence: float = Field(default=1.0, description="置信度")
    usage_count: int = Field(default=0, description="使用次数")
    last_used_at: Optional[datetime] = Field(default=None, description="最后使用时间")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

    # JSON字段
    embedding: Optional[Any] = Field(default=None, sa_column=Column(JSON))


class MemoryFile(SQLModel, table=True):
    """文件即记忆表"""
    __tablename__ = "memory_files"

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int = Field(description="Agent ID")
    project_id: int = Field(description="项目ID")
    file_path: str = Field(description="文件路径")
    file_type: str = Field(description="文件类型")
    memory_id: Optional[int] = Field(default=None, description="关联记忆ID")
    file_hash: str = Field(description="文件哈希")
    content: str = Field(sa_column=Column(Text), description="文件内容")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")


class GitMemoryCommit(SQLModel, table=True):
    """Git版本化记忆表"""
    __tablename__ = "git_memory_commits"

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int = Field(description="Agent ID")
    project_id: int = Field(description="项目ID")
    memory_id: int = Field(description="记忆ID")
    commit_hash: str = Field(description="提交哈希")
    branch: str = Field(default="main", description="分支名")
    commit_message: str = Field(description="提交信息")
    parent_commit_hash: Optional[str] = Field(default=None, description="父提交哈希")
    author: str = Field(description="作者")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")


class SleeptimeTask(SQLModel, table=True):
    """Sleeptime异步学习任务表"""
    __tablename__ = "sleeptime_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int = Field(description="Agent ID")
    task_type: str = Field(description="任务类型")
    status: str = Field(default="pending", description="状态")
    scheduled_at: datetime = Field(description="计划执行时间")
    started_at: Optional[datetime] = Field(default=None, description="开始时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    error_message: Optional[str] = Field(default=None, description="错误信息")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")

    # JSON字段
    input_data_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    output_data_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
