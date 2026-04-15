#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件流和聊天服务
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import Session, select

from app.models.chat import (
    EventStream, ChatMessage, ChatRoom,
    EventType, MessageStatus, RoomType
)
from app.core.websocket import manager
from app.core.database import get_session


class EventStreamService:
    """事件流服务 - 详细化的Agent事件追踪"""

    async def create_event(
        self,
        project_id: int,
        event_type: EventType,
        source_id: int,
        source_type: str,
        description: str,
        target_id: Optional[int] = None,
        target_type: Optional[str] = None,
        task_id: Optional[int] = None,
        chapter_id: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
        importance: int = 5
    ) -> Dict[str, Any]:
        """创建事件流"""
        async for session in get_session():
            event = EventStream(
                project_id=project_id,
                event_type=event_type,
                source_id=source_id,
                source_type=source_type,
                target_id=target_id,
                target_type=target_type,
                task_id=task_id,
                chapter_id=chapter_id,
                description=description,
                importance=importance,
                data=data
            )
            session.add(event)
            await session.commit()
            await session.refresh(event)

            # 实时广播事件
            await self._broadcast_event(event)

            return {
                "success": True,
                "event_id": event.id,
                "event": event
            }

    async def _broadcast_event(self, event: EventStream):
        """广播事件到所有连接"""
        event_data = {
            "type": "event",
            "event_type": event.event_type.value,
            "source": {
                "id": event.source_id,
                "type": event.source_type
            },
            "target": {
                "id": event.target_id,
                "type": event.target_type
            } if event.target_id else None,
            "description": event.description,
            "data": event.data,
            "importance": event.importance,
            "timestamp": event.created_at.isoformat()
        }

        await manager.broadcast_to_all(event_data)

    async def get_project_events(
        self,
        project_id: int,
        limit: int = 50
    ) -> List[EventStream]:
        """获取项目事件流"""
        async for session in get_session():
            stmt = select(EventStream).where(
                EventStream.project_id == project_id
            ).order_by(
                EventStream.created_at.desc()
            ).limit(limit)

            result = await session.exec(stmt)
            return result.all()

    async def get_agent_events(
        self,
        agent_id: int,
        limit: int = 50
    ) -> List[EventStream]:
        """获取Agent事件"""
        async for session in get_session():
            stmt = select(EventStream).where(
                EventStream.source_id == agent_id,
                EventStream.source_type == "agent"
            ).order_by(
                EventStream.created_at.desc()
            ).limit(limit)

            result = await session.exec(stmt)
            return result.all()

    async def categorize_events(
        self,
        project_id: int
    ) -> Dict[str, List[EventStream]]:
        """归类事件流"""
        events = await self.get_project_events(project_id, limit=200)

        categories = {
            "tasks": [],  # 任务相关
            "messages": [],  # 消息相关
            "memory": [],  # 记忆相关
            "knowledge": [],  # 知识相关
            "system": [],  # 系统通知
            "errors": []  # 错误
        }

        for event in events:
            if event.event_type in [
                EventType.TASK_START,
                EventType.TASK_PROGRESS,
                EventType.TASK_COMPLETE,
                EventType.TASK_ERROR
            ]:
                categories["tasks"].append(event)
            elif event.event_type in [
                EventType.AGENT_MESSAGE,
                EventType.AGENT_MENTION,
                EventType.AGENT_RESPONSE
            ]:
                categories["messages"].append(event)
            elif event.event_type == EventType.MEMORY_UPDATE:
                categories["memory"].append(event)
            elif event.event_type == EventType.KNOWLEDGE_UPDATE:
                categories["knowledge"].append(event)
            elif event.event_type == EventType.SYSTEM_NOTICE:
                categories["system"].append(event)
            else:
                categories["errors"].append(event)

        return categories


class ChatService:
    """聊天服务 - Agent群聊和私信"""

    async def send_message(
        self,
        project_id: int,
        room_id: str,
        sender_id: int,
        sender_type: str,
        content: str,
        mentions: Optional[List[int]] = None,
        message_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
        reply_to_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """发送消息"""
        async for session in get_session():
            message = ChatMessage(
                project_id=project_id,
                room_id=room_id,
                sender_id=sender_id,
                sender_type=sender_type,
                content=content,
                mentions=mentions,
                message_type=message_type,
                metadata=metadata,
                reply_to_id=reply_to_id
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)

            # 实时广播消息
            await self._broadcast_message(message)

            # 如果有艾特，通知相关Agent
            if mentions:
                await self._notify_mentions(message, mentions)

            # 创建事件流
            await event_service.create_event(
                project_id=project_id,
                event_type=EventType.AGENT_MESSAGE,
                source_id=sender_id,
                source_type=sender_type,
                description=f"{sender_type} {sender_id} 在 {room_id} 发送了消息",
                data={"message_id": message.id, "room_id": room_id}
            )

            return {
                "success": True,
                "message_id": message.id,
                "message": message
            }

    async def _broadcast_message(self, message: ChatMessage):
        """广播消息"""
        message_data = {
            "type": "message",
            "room_id": message.room_id,
            "sender": {
                "id": message.sender_id,
                "type": message.sender_type
            },
            "content": message.content,
            "mentions": message.mentions,
            "message_type": message.message_type,
            "timestamp": message.created_at.isoformat()
        }

        # 广播到房间内的所有连接
        await manager.broadcast_to_all(message_data)

    async def _notify_mentions(self, message: ChatMessage, mentions: List[int]):
        """通知被艾特的Agent"""
        for agent_id in mentions:
            mention_data = {
                "type": "mention",
                "agent_id": agent_id,
                "message_id": message.id,
                "room_id": message.room_id,
                "sender_id": message.sender_id,
                "content": message.content,
                "timestamp": message.created_at.isoformat()
            }
            await manager.send_to_agent(agent_id, mention_data)

            # 创建艾特事件
            await event_service.create_event(
                project_id=message.project_id,
                event_type=EventType.AGENT_MENTION,
                source_id=message.sender_id,
                source_type=message.sender_type,
                target_id=agent_id,
                target_type="agent",
                description=f"{message.sender_type} {message.sender_id} 艾特了 Agent {agent_id}",
                data={"message_id": message.id, "room_id": message.room_id}
            )

    async def get_room_messages(
        self,
        room_id: str,
        limit: int = 50
    ) -> List[ChatMessage]:
        """获取房间消息"""
        async for session in get_session():
            stmt = select(ChatMessage).where(
                ChatMessage.room_id == room_id
            ).order_by(
                ChatMessage.created_at.desc()
            ).limit(limit)

            result = await session.exec(stmt)
            return result.all()

    async def create_room(
        self,
        project_id: int,
        name: str,
        room_type: RoomType,
        member_ids: List[int],
        created_by: int,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """创建聊天房间"""
        async for session in get_session():
            room = ChatRoom(
                project_id=project_id,
                name=name,
                room_type=room_type,
                member_ids=member_ids,
                created_by=created_by,
                description=description,
                settings=settings
            )
            session.add(room)
            await session.commit()
            await session.refresh(room)

            return {
                "success": True,
                "room_id": room.id,
                "room": room
            }

    async def get_project_rooms(self, project_id: int) -> List[ChatRoom]:
        """获取项目房间列表"""
        async for session in get_session():
            stmt = select(ChatRoom).where(
                ChatRoom.project_id == project_id
            ).order_by(
                ChatRoom.last_message_at.desc()
            )

            result = await session.exec(stmt)
            return result.all()


# 全局实例
event_service = EventStreamService()
chat_service = ChatService()
