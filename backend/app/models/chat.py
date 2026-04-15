#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天和事件流模型
"""

from sqlmodel import Field, SQLModel, Column, JSON
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class EventType(str, Enum):
    """事件类型"""
    TASK_START = "task_start"
    TASK_PROGRESS = "task_progress"
    TASK_COMPLETE = "task_complete"
    TASK_ERROR = "task_error"
    AGENT_MESSAGE = "agent_message"
    AGENT_MENTION = "agent_mention"
    AGENT_RESPONSE = "agent_response"
    SYSTEM_NOTICE = "system_notice"
    MEMORY_UPDATE = "memory_update"
    KNOWLEDGE_UPDATE = "knowledge_update"


class MessageStatus(str, Enum):
    """消息状态"""
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class ChatMessage(SQLModel, table=True):
    """聊天消息表"""
    __tablename__ = "chat_messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(description="项目ID")
    room_id: str = Field(description="房间ID")
    sender_id: int = Field(description="发送者ID")
    sender_type: str = Field(description="发送者类型: agent/user")
    recipient_id: Optional[int] = Field(default=None, description="接收者ID (私聊)")
    content: str = Field(description="消息内容")
    message_type: str = Field(default="text", description="消息类型: text/image/file")
    status: MessageStatus = Field(default=MessageStatus.SENT, description="消息状态")
    reply_to_id: Optional[int] = Field(default=None, description="回复的消息ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

    # JSON字段
    mentions_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    metadata_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))


class ChatMessageCreate(SQLModel):
    """创建聊天消息请求"""
    project_id: int
    room_id: str
    sender_id: int
    sender_type: str
    content: str
    recipient_id: Optional[int] = None
    message_type: str = "text"
    mentions: Optional[List[int]] = None
    msg_metadata: Optional[Dict[str, Any]] = None


class ChatMessageUpdate(SQLModel):
    """更新聊天消息请求"""
    status: Optional[MessageStatus] = None
    content: Optional[str] = None


class ChatMessageRead(SQLModel):
    """聊天消息响应"""
    id: int
    project_id: int
    room_id: str
    sender_id: int
    sender_type: str
    recipient_id: Optional[int] = None
    content: str
    message_type: str
    status: MessageStatus
    reply_to_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    mentions_data: Optional[Any] = None
    metadata_data: Optional[Any] = None


class RoomType(str, Enum):
    """房间类型"""
    WORKSPACE = "workspace"
    TEAM = "team"
    PRIVATE = "private"
    SYSTEM = "system"


class ChatRoom(SQLModel, table=True):
    """聊天房间表"""
    __tablename__ = "chat_rooms"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(description="项目ID")
    name: str = Field(description="房间名称")
    room_type: RoomType = Field(description="房间类型")
    description: Optional[str] = Field(default=None, description="房间描述")
    created_by: int = Field(description="创建者ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    last_message_at: Optional[datetime] = Field(default=None, description="最后消息时间")

    # JSON字段
    member_ids_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    settings_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))


class ChatRoomCreate(SQLModel):
    """创建聊天房间请求"""
    project_id: int
    name: str
    room_type: RoomType
    member_ids: Optional[List[int]] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ChatRoomUpdate(SQLModel):
    """更新聊天房间请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    member_ids: Optional[List[int]] = None
    settings: Optional[Dict[str, Any]] = None


class ChatRoomRead(SQLModel):
    """聊天房间响应"""
    id: int
    project_id: int
    name: str
    room_type: RoomType
    description: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime] = None
    member_ids_data: Optional[Any] = None


class EventStream(SQLModel, table=True):
    """事件流表"""
    __tablename__ = "event_streams"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(description="项目ID")
    event_type: EventType = Field(description="事件类型")
    source_id: int = Field(description="事件源ID")
    source_type: str = Field(description="事件源类型: agent/user/system")
    target_id: Optional[int] = Field(default=None, description="目标ID")
    target_type: Optional[str] = Field(default=None, description="目标类型")
    description: str = Field(description="事件描述")
    importance: int = Field(default=5, description="重要性 1-10")
    task_id: Optional[int] = Field(default=None, description="关联任务ID")
    chapter_id: Optional[int] = Field(default=None, description="关联章节ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")

    # JSON字段
    data_data: Optional[Any] = Field(default=None, sa_column=Column(JSON))


class EventStreamCreate(SQLModel):
    """创建事件流请求"""
    project_id: int
    event_type: EventType
    source_id: int
    source_type: str
    description: str
    target_id: Optional[int] = None
    target_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    importance: int = 5


class EventStreamRead(SQLModel):
    """事件流响应"""
    id: int
    project_id: int
    event_type: EventType
    source_id: int
    source_type: str
    target_id: Optional[int] = None
    target_type: Optional[str] = None
    description: str
    importance: int
    task_id: Optional[int] = None
    chapter_id: Optional[int] = None
    created_at: datetime
    data_data: Optional[Any] = None
