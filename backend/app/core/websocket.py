#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket管理器 - 实时Agent通信
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

# 连接管理器
class ConnectionManager:
    """WebSocket连接管理器"""

    def __init__(self):
        # agent_id -> WebSocket连接
        self.agent_connections: Dict[int, WebSocket] = {}
        # 项目ID -> 所有连接的WebSocket列表
        self.project_connections: Dict[int, List[WebSocket]] = {}
        # 客户端ID -> WebSocket连接
        self.client_connections: Dict[str, WebSocket] = {}

    async def connect_agent(self, websocket: WebSocket, agent_id: int):
        """连接Agent"""
        await websocket.accept()
        self.agent_connections[agent_id] = websocket
        print(f"✓ Agent {agent_id} connected")

    async def connect_client(self, websocket: WebSocket, client_id: str):
        """连接客户端"""
        await websocket.accept()
        self.client_connections[client_id] = websocket
        print(f"✓ Client {client_id} connected")

    async def disconnect_agent(self, agent_id: int):
        """断开Agent连接"""
        if agent_id in self.agent_connections:
            del self.agent_connections[agent_id]
            print(f"✗ Agent {agent_id} disconnected")

    async def disconnect_client(self, client_id: str):
        """断开客户端连接"""
        if client_id in self.client_connections:
            del self.client_connections[client_id]
            print(f"✗ Client {client_id} disconnected")

    async def send_to_agent(self, agent_id: int, message: dict):
        """发送消息给特定Agent"""
        if agent_id in self.agent_connections:
            websocket = self.agent_connections[agent_id]
            await websocket.send_json(message)
            return True
        return False

    async def send_to_client(self, client_id: str, message: dict):
        """发送消息给特定客户端"""
        if client_id in self.client_connections:
            websocket = self.client_connections[client_id]
            await websocket.send_json(message)
            return True
        return False

    async def broadcast_to_all(self, message: dict, exclude: Optional[int] = None):
        """广播消息给所有连接"""
        # 发送给所有Agent
        for agent_id, websocket in self.agent_connections.items():
            if agent_id != exclude:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    print(f"Error sending to agent {agent_id}: {e}")

        # 发送给所有客户端
        for client_id, websocket in self.client_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending to client {client_id}: {e}")

    async def broadcast_to_project(self, project_id: int, message: dict):
        """广播消息给项目相关的所有连接"""
        if project_id in self.project_connections:
            for websocket in self.project_connections[project_id]:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    print(f"Error broadcasting to project {project_id}: {e}")


# 全局实例
manager = ConnectionManager()
