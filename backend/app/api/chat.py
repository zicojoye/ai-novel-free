#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_session
from app.models.chat import (
    ChatMessage, ChatRoom, ChatRoomCreate, ChatRoomUpdate,
    ChatRoomRead, ChatMessageCreate, ChatMessageUpdate, ChatMessageRead,
    RoomType, MessageStatus
)
from app.services.event_service import chat_service

router = APIRouter()


# ===== 聊天房间相关 =====

@router.get("/rooms", response_model=List[ChatRoomRead])
async def get_chat_rooms(
    project_id: int = Query(..., description="项目ID"),
    room_type: Optional[RoomType] = Query(None, description="房间类型"),
    session: AsyncSession = Depends(get_session)
):
    """获取聊天房间列表"""
    stmt = select(ChatRoom).where(ChatRoom.project_id == project_id)

    if room_type:
        stmt = stmt.where(ChatRoom.room_type == room_type)

    stmt = stmt.order_by(ChatRoom.last_message_at.desc())
    result = await session.exec(stmt)
    return result.all()


@router.get("/rooms/{room_id}", response_model=ChatRoomRead)
async def get_chat_room(
    room_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取房间详情"""
    room = await session.get(ChatRoom, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")
    return room


@router.post("/rooms", response_model=ChatRoomRead)
async def create_chat_room(
    room_data: ChatRoomCreate,
    session: AsyncSession = Depends(get_session)
):
    """创建聊天房间"""
    result = await chat_service.create_room(
        project_id=room_data.project_id,
        name=room_data.name,
        room_type=room_data.room_type,
        member_ids=room_data.member_ids,
        created_by=1,  # TODO: 从认证信息获取
        description=room_data.description,
        settings=room_data.settings
    )
    return result.get("room")


@router.put("/rooms/{room_id}", response_model=ChatRoomRead)
async def update_chat_room(
    room_id: int,
    room_data: ChatRoomUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新聊天房间"""
    room = await session.get(ChatRoom, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    room_data_dict = room_data.model_dump(exclude_unset=True)
    for key, value in room_data_dict.items():
        setattr(room, key, value)

    room.updated_at = room.created_at
    await session.commit()
    await session.refresh(room)
    return room


@router.delete("/rooms/{room_id}")
async def delete_chat_room(
    room_id: int,
    session: AsyncSession = Depends(get_session)
):
    """删除聊天房间"""
    room = await session.get(ChatRoom, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    await session.delete(room)
    await session.commit()
    return {"message": "房间已删除"}


# ===== 聊天消息相关 =====

@router.get("/messages", response_model=List[ChatMessageRead])
async def get_messages(
    room_id: str = Query(..., description="房间ID"),
    limit: int = Query(50, ge=1, le=200, description="消息数量"),
    session: AsyncSession = Depends(get_session)
):
    """获取房间消息"""
    messages = await chat_service.get_room_messages(room_id, limit)
    return messages


@router.get("/messages/{message_id}", response_model=ChatMessageRead)
async def get_message(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取消息详情"""
    message = await session.get(ChatMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    return message


@router.post("/messages", response_model=ChatMessageRead)
async def send_message(
    message_data: ChatMessageCreate,
    session: AsyncSession = Depends(get_session)
):
    """发送消息"""
    result = await chat_service.send_message(
        project_id=message_data.project_id,
        room_id=message_data.room_id,
        sender_id=message_data.sender_id,
        sender_type=message_data.sender_type,
        content=message_data.content,
        mentions=message_data.mentions,
        message_type=message_data.message_type,
        metadata=message_data.msg_metadata
    )
    return result.get("message")


@router.put("/messages/{message_id}", response_model=ChatMessageRead)
async def update_message(
    message_id: int,
    message_data: ChatMessageUpdate,
    session: AsyncSession = Depends(get_session)
):
    """更新消息"""
    message = await session.get(ChatMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")

    message_data_dict = message_data.model_dump(exclude_unset=True)
    for key, value in message_data_dict.items():
        setattr(message, key, value)

    message.updated_at = message.created_at
    await session.commit()
    await session.refresh(message)
    return message


@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    """删除消息"""
    message = await session.get(ChatMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")

    await session.delete(message)
    await session.commit()
    return {"message": "消息已删除"}


# ===== 便捷接口 =====

@router.post("/rooms/workspace")
async def create_workspace_room(
    project_id: int,
    session: AsyncSession = Depends(get_session)
):
    """创建工作室群聊"""
    result = await chat_service.create_room(
        project_id=project_id,
        name="工作室",
        room_type=RoomType.WORKSPACE,
        member_ids=[],  # 初始为空，Agent加入时更新
        created_by=1,
        description="项目工作室群聊 - 所有Agent和成员"
    )
    return result


@router.post("/rooms/team/{team_name}")
async def create_team_room(
    project_id: int,
    team_name: str,
    member_ids: List[int],
    session: AsyncSession = Depends(get_session)
):
    """创建团队群聊"""
    result = await chat_service.create_room(
        project_id=project_id,
        name=f"团队: {team_name}",
        room_type=RoomType.TEAM,
        member_ids=member_ids,
        created_by=1,
        description=f"{team_name}团队群聊"
    )
    return result
