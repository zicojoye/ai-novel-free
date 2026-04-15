#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

from app.services.llm_service import llm_service


class BaseAgent(ABC):
    """Agent基类"""

    def __init__(self, agent_id: int, name: str, role: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.last_activity: Optional[datetime] = None
        self.tasks_completed = 0

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务"""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        pass

    async def call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """调用LLM"""
        system = system_prompt or self.get_system_prompt()
        response = await llm_service.router.generate(
            prompt=prompt,
            system_prompt=system
        )
        return response

    async def get_context(
        self,
        query: str,
        project_id: int
    ) -> str:
        """获取上下文（开源版：RAG不可用，返回空）"""
        return ""

    def update_activity(self):
        """更新活动时间"""
        self.last_activity = datetime.utcnow()

    def increment_tasks(self):
        """增加任务计数"""
        self.tasks_completed += 1
