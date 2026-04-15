#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM服务 - 多模型集成和智能路由
"""

from typing import Optional, Dict, Any
from enum import Enum
import openai
import anthropic
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from app.core.config import settings


class LLMProvider(str, Enum):
    """LLM提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    CUSTOM = "custom"


class TaskComplexity(str, Enum):
    """任务复杂度"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class LLMRouter:
    """LLM智能路由器"""

    # 任务类型 -> 各 provider 默认模型（可被调用方覆盖）
    DEFAULT_TASK_MODELS = {
        "worldbuilding": {"openai": "gpt-4o", "anthropic": "claude-3-5-sonnet-20241022", "deepseek": "deepseek-chat", "gemini": "gemini-1.5-pro"},
        "chapter_generation": {"openai": "gpt-4o-mini", "anthropic": "claude-3-5-haiku-20241022", "deepseek": "deepseek-chat", "gemini": "gemini-1.5-flash"},
        "review": {"openai": "gpt-4o-mini", "anthropic": "claude-3-5-haiku-20241022", "deepseek": "deepseek-chat", "gemini": "gemini-1.5-flash"},
    }

    # 根据模型 id 推断 provider
    PROVIDER_MAP = {
        "gpt": LLMProvider.OPENAI,
        "claude": LLMProvider.ANTHROPIC,
        "deepseek": LLMProvider.DEEPSEEK,
        "gemini": LLMProvider.GEMINI,
        "custom": LLMProvider.CUSTOM,
    }

    def __init__(self):
        self._clients: Dict[str, Any] = {}

    def infer_provider(self, model: str) -> LLMProvider:
        """根据模型名推断 provider"""
        model_lower = model.lower()
        for prefix, provider in self.PROVIDER_MAP.items():
            if model_lower.startswith(prefix):
                return provider
        # 默认用全局配置的 provider
        return LLMProvider(settings.DEFAULT_LLM_PROVIDER)

    def select_model(
        self,
        task_type: str,
        provider: Optional[LLMProvider] = None,
        custom_model: Optional[str] = None,
        budget: float = 1.0
    ) -> str:
        """选择模型：custom_model > provider默认 > 全局默认"""
        # 用户指定了具体模型名，直接使用
        if custom_model:
            return custom_model

        # 全局默认模型
        global_default = settings.DEFAULT_MODEL

        task_defaults = self.DEFAULT_TASK_MODELS.get(task_type, self.DEFAULT_TASK_MODELS["review"])

        if provider:
            return task_defaults.get(provider.value, global_default)

        # 根据全局 provider 配置选
        active_provider = settings.DEFAULT_LLM_PROVIDER
        return task_defaults.get(active_provider, global_default)

    def get_client(self, model: str, provider: Optional[LLMProvider] = None) -> Any:
        """获取LLM客户端（自动推断provider）"""
        if provider is None:
            provider = self.infer_provider(model)

        cache_key = f"{provider.value}:{model}"
        if cache_key in self._clients:
            return self._clients[cache_key]

        if provider == LLMProvider.OPENAI:
            client = ChatOpenAI(
                model=model,
                api_key=settings.OPENAI_API_KEY,
                temperature=0.7,
                max_tokens=4000
            )
        elif provider == LLMProvider.ANTHROPIC:
            client = ChatAnthropic(
                model=model,
                api_key=settings.ANTHROPIC_API_KEY,
                temperature=0.7,
                max_tokens=4000
            )
        elif provider == LLMProvider.DEEPSEEK:
            # DeepSeek 兼容 OpenAI 接口
            client = ChatOpenAI(
                model=model,
                api_key=settings.DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com/v1",
                temperature=0.7,
                max_tokens=4000
            )
        elif provider == LLMProvider.GEMINI:
            # Gemini 兼容 OpenAI 接口
            client = ChatOpenAI(
                model=model,
                api_key=settings.GEMINI_API_KEY,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                temperature=0.7,
                max_tokens=4000
            )
        elif provider == LLMProvider.CUSTOM:
            # 自定义 Provider（兼容 OpenAI 格式）
            if not settings.CUSTOM_API_KEY or not settings.CUSTOM_API_BASE:
                raise ValueError("自定义 Provider 未配置 CUSTOM_API_KEY 或 CUSTOM_API_BASE")
            use_model = model if model != "custom" else (settings.CUSTOM_MODEL_ID or model)
            client = ChatOpenAI(
                model=use_model,
                api_key=settings.CUSTOM_API_KEY,
                base_url=settings.CUSTOM_API_BASE.rstrip("/"),
                temperature=0.7,
                max_tokens=4000
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        self._clients[cache_key] = client
        return client

    async def generate(
        self,
        prompt: str,
        task_type: str = "chapter_generation",
        provider: Optional[LLMProvider] = None,
        custom_model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """生成文本，支持传入自定义模型名"""
        model = self.select_model(task_type, provider, custom_model)
        inferred_provider = self.infer_provider(model)
        client = self.get_client(model, inferred_provider)

        messages: list[BaseMessage] = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        response = await client.ainvoke(messages)
        return response.content


class LLMService:
    """LLM服务"""

    def __init__(self):
        self.router = LLMRouter()

    async def generate_worldbuilding(
        self,
        genre: str,
        description: str,
        custom_model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """生成世界观"""
        prompt = f"""
为以下类型和描述的小说生成完整的10维度世界观:

类型: {genre}
描述: {description}

请生成以下10个维度:
1. 核心设定
2. 世界观
3. 角色系统
4. 势力体系
5. 力量体系
6. 地理环境
7. 历史背景
8. 道具物品
9. 剧情主线
10. 世界规则

以JSON格式返回,每个维度详细描述。
"""
        response = await self.router.generate(
            prompt=prompt,
            task_type="worldbuilding",
            custom_model=custom_model,
            system_prompt="你是一个专业的世界观构建专家,擅长创作详细而有趣的世界设定。"
        )
        return {
            "content": response,
            "model": self.router.select_model("worldbuilding", custom_model=custom_model)
        }

    async def generate_chapter(
        self,
        outline: str,
        word_count: int = 2000,
        style: str = "口语化",
        custom_model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """生成章节"""
        prompt = f"""
根据以下大纲创作章节:

大纲:
{outline}

要求:
- 字数: 约{word_count}字
- 风格: {style}
- 内容: 生动、有吸引力
- 节奏: 紧凑有力

直接输出章节内容,不要有任何说明。
"""
        response = await self.router.generate(
            prompt=prompt,
            task_type="chapter_generation",
            custom_model=custom_model,
            system_prompt="你是一个专业的小说作家,擅长创作引人入胜的故事内容。"
        )
        return {
            "content": response,
            "word_count": len(response),
            "model": self.router.select_model("chapter_generation", custom_model=custom_model)
        }

    async def generate_outline(
        self,
        project_title: str,
        genre: str,
        chapter_count: int = 50,
        custom_model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """生成大纲"""
        prompt = f"""
为以下项目生成完整大纲:

项目标题: {project_title}
类型: {genre}
章节数: {chapter_count}

要求:
1. 整体故事线
2. 主要角色弧光
3. 章节大纲(每章简要描述)
4. 关键转折点
5. 伏笔设置

以清晰的结构输出。
"""
        response = await self.router.generate(
            prompt=prompt,
            task_type="worldbuilding",
            custom_model=custom_model,
            system_prompt="你是一个专业的剧情设计师,擅长构建引人入胜的故事结构。"
        )
        return {
            "content": response,
            "model": self.router.select_model("worldbuilding", custom_model=custom_model)
        }

    async def polish_text(
        self,
        text: str,
        style: str = "自然流畅",
        custom_model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """润色文本"""
        prompt = f"""
请润色以下文本,使其更加{style}:

{text}

要求:
1. 保持原意
2. 去除AI痕迹
3. 增强表现力
4. 语言更自然

只返回润色后的文本。
"""
        response = await self.router.generate(
            prompt=prompt,
            task_type="review",
            custom_model=custom_model,
            system_prompt="你是一个专业的编辑,擅长润色文本,去除AI写作痕迹。"
        )
        return {
            "content": response,
            "model": self.router.select_model("review", custom_model=custom_model)
        }


# 全局实例
llm_service = LLMService()
