#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent任务调度器 - 定时执行Agent任务
"""

import asyncio
import schedule
from datetime import datetime
from typing import Dict, List
import httpx
from pathlib import Path


class AgentScheduler:
    """Agent任务调度器"""
    
    def __init__(self, api_base: str = "http://localhost:8000"):
        self.api_base = api_base
        self.client = httpx.AsyncClient(timeout=60.0)
        self.tasks: List[Dict] = []
    
    async def add_task(self, task_config: Dict):
        """添加定时任务
        
        Args:
            task_config: {
                "name": "任务名称",
                "agent_type": "agent类型",
                "schedule": "cron表达式",
                "params": {} 任务参数
            }
        """
        self.tasks.append(task_config)
        print(f"添加任务: {task_config['name']} - {task_config['schedule']}")
    
    async def execute_task(self, task: Dict):
        """执行单个任务"""
        try:
            print(f"\n[{datetime.now()}] 执行任务: {task['name']}")
            
            # 调用Agent API
            response = await self.client.post(
                f"{self.api_base}/api/ai/agent/execute",
                json={
                    "agent_type": task['agent_type'],
                    "task": task.get('params', {})
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"任务完成: {result.get('message', '成功')}")
            else:
                print(f"任务失败: {response.status_code}")
        
        except Exception as e:
            print(f"任务执行异常: {e}")
    
    async def run_scheduled_tasks(self):
        """运行定时任务"""
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)
    
    def schedule_task(self, task: Dict):
        """调度任务"""
        task_name = task['name']
        schedule_str = task['schedule']
        
        # 解析调度表达式
        # 简化版,支持: "daily:09:00", "hourly", "interval:30"
        
        if schedule_str.startswith("daily:"):
            time = schedule_str.split(":")[1]
            schedule.every().day.at(time).do(
                lambda: asyncio.create_task(self.execute_task(task))
            )
            print(f"  每天在 {time} 执行")
        
        elif schedule_str.startswith("hourly"):
            schedule.every().hour.do(
                lambda: asyncio.create_task(self.execute_task(task))
            )
            print(f"  每小时执行一次")
        
        elif schedule_str.startswith("interval:"):
            minutes = int(schedule_str.split(":")[1])
            schedule.every(minutes).minutes.do(
                lambda: asyncio.create_task(self.execute_task(task))
            )
            print(f"  每 {minutes} 分钟执行一次")
    
    def load_tasks_from_config(self, config_path: str = "data/scheduler_config.json"):
        """从配置文件加载任务"""
        config_file = Path(config_path)
        
        if not config_file.exists():
            print(f"配置文件不存在: {config_path}")
            return
        
        import json
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        for task in config.get('tasks', []):
            self.schedule_task(task)
    
    async def start(self):
        """启动调度器"""
        print(f"\nAgent任务调度器启动 - {datetime.now()}")
        
        # 加载配置
        self.load_tasks_from_config()
        
        # 运行定时任务
        await self.run_scheduled_tasks()
    
    async def close(self):
        """关闭调度器"""
        await self.client.aclose()
        print("调度器已关闭")


async def main():
    """主函数"""
    scheduler = AgentScheduler()
    
    # 添加示例任务
    await scheduler.add_task({
        "name": "每日剧情检查",
        "agent_type": "reviewer",
        "schedule": "daily:09:00",
        "params": {"check_type": "plot_consistency"}
    })
    
    await scheduler.add_task({
        "name": "知识库更新",
        "agent_type": "knowledge_manager",
        "schedule": "interval:60",
        "params": {"action": "update_index"}
    })
    
    try:
        await scheduler.start()
    except KeyboardInterrupt:
        print("\n停止调度器")
        await scheduler.close()


if __name__ == "__main__":
    asyncio.run(main())
