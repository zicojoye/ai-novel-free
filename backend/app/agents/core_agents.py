#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心创作Agent
"""

from typing import Dict, Any
from datetime import datetime

from app.agents.base_agent import BaseAgent
from app.services.llm_service import llm_service


class AuthorAgent(BaseAgent):
    """主创Agent - 负责核心内容创作"""

    def __init__(self, agent_id: int):
        super().__init__(
            agent_id=agent_id,
            name="主创Agent",
            role="author"
        )

    def get_system_prompt(self) -> str:
        return """你是一位专业的小说主创Agent,负责创作核心内容。

你的职责:
1. 理解大纲和要求
2. 创作高质量的章节内容
3. 保持故事连贯性
4. 符合番茄爆款铁律

创作原则:
- 每章至少2个爽点
- 20%内吸引读者
- 避免说教和堆背景
- 语言口语化、节奏快
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行创作任务"""
        task_type = task.get("type", "chapter")

        if task_type == "chapter":
            return await self.create_chapter(task)
        elif task_type == "outline":
            return await self.create_outline(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    async def create_chapter(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """创建章节"""
        outline = task.get("outline", "")
        word_count = task.get("word_count", 2000)
        project_id = task.get("project_id")

        # 获取上下文
        if project_id:
            context = await self.get_context("相关世界观和角色", project_id)
            outline = f"上下文:\n{context}\n\n大纲:\n{outline}"

        # 生成章节
        result = await llm_service.generate_chapter(
            outline=outline,
            word_count=word_count
        )

        self.update_activity()
        self.increment_tasks()

        return {
            "success": True,
            "content": result["content"],
            "word_count": result["word_count"],
            "model": result["model"]
        }

    async def create_outline(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """创建大纲"""
        project_title = task.get("project_title", "")
        genre = task.get("genre", "都市")
        chapter_count = task.get("chapter_count", 50)

        result = await llm_service.generate_outline(
            project_title=project_title,
            genre=genre,
            chapter_count=chapter_count
        )

        self.update_activity()
        self.increment_tasks()

        return {
            "success": True,
            "outline": result["content"],
            "model": result["model"]
        }


class EditorAgent(BaseAgent):
    """编辑Agent - 负责内容润色和优化"""

    def __init__(self, agent_id: int):
        super().__init__(
            agent_id=agent_id,
            name="编辑Agent",
            role="editor"
        )

    def get_system_prompt(self) -> str:
        return """你是一位专业的编辑Agent,负责内容润色和优化。

你的职责:
1. 去除AI写作痕迹
2. 增强文字表现力
3. 优化语言节奏
4. 保持原意不变

润色原则:
- 避免重复表达
- 减少弱化副词
- 去除套话结构
- 增强画面感
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行编辑任务"""
        text = task.get("text", "")
        style = task.get("style", "自然流畅")

        result = await llm_service.polish_text(
            text=text,
            style=style
        )

        self.update_activity()
        self.increment_tasks()

        return {
            "success": True,
            "polished_text": result["content"],
            "model": result["model"]
        }


class ReviewerAgent(BaseAgent):
    """审核Agent - 负责质量检查和合规审查"""

    def __init__(self, agent_id: int):
        super().__init__(
            agent_id=agent_id,
            name="审核Agent",
            role="reviewer"
        )

    def get_system_prompt(self) -> str:
        return """你是一位专业的审核Agent,负责质量检查和合规审查。

你的职责:
1. 检查番茄爆款标准
2. 验证一致性
3. 内容合规审查
4. 质量评分

审核标准:
- 每章至少2个爽点
- 节奏紧凑有力
- 无敏感内容
- 符合平台规范
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行审核任务"""
        content = task.get("content", "")
        check_type = task.get("check_type", "quality")

        if check_type == "quality":
            return await self.check_quality(content)
        elif check_type == "compliance":
            return await self.check_compliance(content)
        else:
            return await self.check_all(content)

    async def check_quality(self, content: str) -> Dict[str, Any]:
        """质量检查"""
        prompt = f"""
请审核以下章节内容的质量:

{content}

检查项:
1. 爽点数量(至少2个)
2. 节奏评估
3. 文字表现力
4. 整体质量评分(0-10)

请返回JSON格式结果。
"""

        result = await self.call_llm(prompt)

        self.update_activity()
        self.increment_tasks()

        return {
            "success": True,
            "quality_report": result
        }

    async def check_compliance(self, content: str) -> Dict[str, Any]:
        """合规审查"""
        prompt = f"""
请审查以下内容的合规性:

{content}

检查项:
1. 是否有敏感内容
2. 是否符合平台规范
3. 是否有违规内容

请返回JSON格式结果。
"""

        result = await self.call_llm(prompt)

        self.update_activity()
        self.increment_tasks()

        return {
            "success": True,
            "compliance_report": result
        }

    async def check_all(self, content: str) -> Dict[str, Any]:
        """全面检查"""
        quality = await self.check_quality(content)
        compliance = await self.check_compliance(content)

        return {
            "success": True,
            "quality_report": quality["quality_report"],
            "compliance_report": compliance["compliance_report"]
        }


class PublisherAgent(BaseAgent):
    """发布Agent - 负责多平台发布"""

    def __init__(self, agent_id: int):
        super().__init__(
            agent_id=agent_id,
            name="发布Agent",
            role="publisher"
        )

    def get_system_prompt(self) -> str:
        return """你是发布Agent,负责将内容发布到各个平台。

你的职责:
1. 格式转换
2. 平台适配
3. 发布管理
4. 数据统计

支持平台:
- 番茄小说
- 起点中文网
- 晋江文学城
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行发布任务"""
        platform = task.get("platform", "fanqie")
        content = task.get("content", "")

        # TODO: 实现实际发布逻辑
        self.update_activity()
        self.increment_tasks()

        return {
            "success": True,
            "message": f"已发布到{platform}",
            "platform": platform
        }
