#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享类型定义 - 前后端通用类型
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentType(str, Enum):
    """Agent类型"""
    AUTHOR = "author"
    EDITOR = "editor"
    REVIEWER = "reviewer"
    PUBLISHER = "publisher"
    WORLD_BUILDER = "world_builder"
    KNOWLEDGE_MANAGER = "knowledge_manager"
    SEMANTIC_RETRIEVER = "semantic_retriever"
    LOGIC_CHECKER = "logic_checker"
    STYLE_CHECKER = "style_checker"


class ModelProvider(str, Enum):
    """模型提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    LOCAL = "local"


class ContentType(str, Enum):
    """内容类型"""
    WORLD_BUILDING = "world_building"
    CHARACTER = "character"
    SKILL = "skill"
    FACTION = "faction"
    SCENE = "scene"
    ITEM = "item"
    CHAPTER = "chapter"
    PLOT = "plot"
    FORESHADOW = "foreshadow"
    HOOK = "hook"
    KNOWLEDGE = "knowledge"


class BaseModel:
    """基础模型"""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            k: v.isoformat() if isinstance(v, datetime) else v
            for k, v in self.__dict__.items()
            if not k.startswith('_')
        }


class TaskResult(BaseModel):
    """任务结果"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration: float = 0.0
    model_used: Optional[str] = None
    tokens_used: Optional[Dict[str, int]] = None
    cache_hit: bool = False


class AgentTaskConfig(BaseModel):
    """Agent任务配置"""
    agent_type: AgentType
    task_type: str
    params: Dict[str, Any]
    priority: int = 1
    timeout: int = 60


class ModelRoutingConfig(BaseModel):
    """模型路由配置"""
    task_type: str
    preferred_model: str
    fallback_models: List[str]
    max_tokens: int
    temperature: float = 0.7
    cache_enabled: bool = True


class CacheConfig(BaseModel):
    """缓存配置"""
    l1_enabled: bool = True
    l1_max_size: int = 1000
    l2_enabled: bool = True
    l2_host: str = "localhost"
    l2_port: int = 6379
    ttl: int = 3600


class PublishConfig(BaseModel):
    """发布配置"""
    platform: str
    auto_publish: bool = False
    schedule_time: Optional[str] = None
    publish_tags: List[str] = []


class ProjectConfig(BaseModel):
    """项目配置"""
    genre: str  # 小说类型
    target_readers: str  # 目标读者
    writing_style: str  # 写作风格
    chapter_target_words: int = 1000  # 章节目标字数
    publish_config: List[PublishConfig]


class ChapterConfig(BaseModel):
    """章节配置"""
    chapter_number: int
    title: str
    target_words: int = 1000
    include_beat_sheet: bool = True
    auto_polish: bool = True


class WorldBuildingConfig(BaseModel):
    """世界观配置"""
    dimensions: List[str] = [
        "世界观概述",
        "地理环境",
        "人物设定",
        "技能体系",
        "势力格局",
        "场景设定",
        "物品设定",
        "历史背景",
        "规则设定",
        "文化特色"
    ]


class KnowledgeConfig(BaseModel):
    """知识库配置"""
    auto_extract: bool = True
    extract_from_chapters: bool = True
    extract_from_outline: bool = True
    embedding_model: str = "text-embedding-ada-002"
