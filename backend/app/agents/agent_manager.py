#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent管理器 - 开源版（4个核心Agent）
付费版(Pro)包含完整12人Agent团队
"""

from typing import Dict, List, Optional
import asyncio

from app.agents.base_agent import BaseAgent
from app.agents.core_agents import AuthorAgent, EditorAgent, ReviewerAgent, PublisherAgent


class AgentManager:
    """Agent管理器（开源版）"""

    def __init__(self):
        self.agents: Dict[int, BaseAgent] = {}
        self._init_agents()

    def _init_agents(self):
        """初始化核心Agent（开源版4个）"""
        self.agents[1] = AuthorAgent(agent_id=1)
        self.agents[2] = EditorAgent(agent_id=2)
        self.agents[3] = ReviewerAgent(agent_id=3)
        self.agents[4] = PublisherAgent(agent_id=4)

    def get_agent(self, agent_id: int) -> Optional[BaseAgent]:
        return self.agents.get(agent_id)

    def get_all_agents(self) -> List[BaseAgent]:
        return list(self.agents.values())

    async def execute_task(self, agent_id: int, task: Dict) -> Dict:
        agent = self.get_agent(agent_id)
        if not agent:
            return {"success": False, "error": f"Agent {agent_id} 不存在"}
        try:
            result = await agent.execute(task)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def execute_workflow(self, workflow: List[Dict]) -> List[Dict]:
        results = []
        for step in workflow:
            agent_id = step.get("agent_id")
            task = step.get("task", {})
            result = await self.execute_task(agent_id, task)
            results.append({"step": step, "result": result})
            if not result.get("success"):
                break
        return results


# 全局实例
agent_manager = AgentManager()
