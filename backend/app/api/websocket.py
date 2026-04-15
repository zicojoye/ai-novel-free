#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket API路由 - Agent实时通信
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
import json

from app.core.websocket import manager
from app.services.event_service import event_service, chat_service

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket连接端点"""
    await manager.connect_client(websocket, client_id)
    print(f"✓ Client {client_id} connected via WebSocket")

    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_json()

            # 处理不同类型的消息
            message_type = data.get("type")

            if message_type == "message":
                # 聊天消息
                await handle_chat_message(websocket, data)
            elif message_type == "ping":
                # 心跳
                await websocket.send_json({"type": "pong"})
            elif message_type == "subscribe":
                # 订阅项目
                project_id = data.get("project_id")
                if project_id:
                    await manager.broadcast_to_project(project_id, {
                        "type": "subscribed",
                        "project_id": project_id
                    })
            else:
                # 其他消息类型
                await manager.broadcast_to_all(data)

    except WebSocketDisconnect:
        await manager.disconnect_client(client_id)
        print(f"✗ Client {client_id} disconnected")


@router.websocket("/ws/agent/{agent_id}")
async def agent_websocket_endpoint(websocket: WebSocket, agent_id: int):
    """Agent WebSocket连接端点"""
    await manager.connect_agent(websocket, agent_id)
    print(f"✓ Agent {agent_id} connected via WebSocket")

    try:
        while True:
            # 接收Agent消息
            data = await websocket.receive_json()

            # 处理Agent消息
            message_type = data.get("type")

            if message_type == "agent_message":
                # Agent发送消息到群聊
                await handle_agent_message(websocket, agent_id, data)
            elif message_type == "task_update":
                # Agent任务更新
                await handle_task_update(websocket, agent_id, data)
            elif message_type == "event":
                # Agent触发事件
                await handle_agent_event(websocket, agent_id, data)
            elif message_type == "ping":
                # 心跳
                await websocket.send_json({"type": "pong", "agent_id": agent_id})
            else:
                # 广播其他消息
                await manager.broadcast_to_all(data)

    except WebSocketDisconnect:
        await manager.disconnect_agent(agent_id)
        print(f"✗ Agent {agent_id} disconnected")


async def handle_chat_message(websocket: WebSocket, data: dict):
    """处理聊天消息"""
    try:
        result = await chat_service.send_message(
            project_id=data.get("project_id"),
            room_id=data.get("room_id", "workspace"),
            sender_id=data.get("sender_id"),
            sender_type=data.get("sender_type", "user"),
            content=data.get("content"),
            mentions=data.get("mentions"),
            message_type=data.get("message_type", "text"),
            metadata=data.get("metadata"),
            reply_to_id=data.get("reply_to_id")
        )

        # 回复发送者确认
        await websocket.send_json({
            "type": "message_sent",
            "success": result.get("success"),
            "message_id": result.get("message_id")
        })

    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e)
        })


async def handle_agent_message(websocket: WebSocket, agent_id: int, data: dict):
    """处理Agent消息"""
    try:
        result = await chat_service.send_message(
            project_id=data.get("project_id"),
            room_id=data.get("room_id", "workspace"),
            sender_id=agent_id,
            sender_type="agent",
            content=data.get("content"),
            mentions=data.get("mentions"),
            message_type=data.get("message_type", "text"),
            metadata=data.get("metadata")
        )

        # 确认发送成功
        await websocket.send_json({
            "type": "agent_message_sent",
            "success": result.get("success"),
            "message_id": result.get("message_id")
        })

    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "agent_id": agent_id,
            "error": str(e)
        })


async def handle_task_update(websocket: WebSocket, agent_id: int, data: dict):
    """处理Agent任务更新"""
    # 广播任务更新事件
    update_event = {
        "type": "task_update",
        "agent_id": agent_id,
        "task_id": data.get("task_id"),
        "status": data.get("status"),
        "progress": data.get("progress"),
        "output": data.get("output"),
        "timestamp": data.get("timestamp")
    }

    await manager.broadcast_to_all(update_event)

    # 如果任务完成或失败，记录事件流
    if data.get("status") in ["completed", "failed"]:
        from app.models.chat import EventType
        await event_service.create_event(
            project_id=data.get("project_id"),
            event_type=EventType.TASK_COMPLETE if data.get("status") == "completed" else EventType.TASK_ERROR,
            source_id=agent_id,
            source_type="agent",
            description=f"Agent {agent_id} 任务 {data.get('task_id')} {data.get('status')}",
            task_id=data.get("task_id"),
            data=data
        )


async def handle_agent_event(websocket: WebSocket, agent_id: int, data: dict):
    """处理Agent自定义事件"""
    from app.models.chat import EventType

    # 解析事件类型
    event_type_str = data.get("event_type", "system_notice")
    try:
        event_type = EventType(event_type_str)
    except ValueError:
        event_type = EventType.SYSTEM_NOTICE

    await event_service.create_event(
        project_id=data.get("project_id"),
        event_type=event_type,
        source_id=agent_id,
        source_type="agent",
        description=data.get("description", ""),
        target_id=data.get("target_id"),
        target_type=data.get("target_type"),
        task_id=data.get("task_id"),
        chapter_id=data.get("chapter_id"),
        data=data.get("data"),
        importance=data.get("importance", 5)
    )
