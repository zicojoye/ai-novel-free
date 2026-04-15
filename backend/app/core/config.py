#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""

    # 应用信息
    APP_NAME: str = "AI Novel Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    # 服务器配置
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/ai_novel.db"

    # AI模型配置
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    DEFAULT_MODEL: str = "gpt-4o"
    DEFAULT_LLM_PROVIDER: str = "openai"
    # 自定义模型列表，格式: "model-id:显示名称:provider"，多个用逗号分隔
    # 例如: CUSTOM_MODELS=my-model:我的模型:openai,other-model:另一个模型:custom
    CUSTOM_MODELS: List[str] = []

    # 自定义 Provider（兼容 OpenAI 格式的任意接口）
    CUSTOM_API_KEY: str = ""
    CUSTOM_API_BASE: str = ""      # 例: https://api.siliconflow.cn/v1
    CUSTOM_MODEL_ID: str = ""      # 例: Qwen/Qwen2.5-72B-Instruct
    CUSTOM_PROVIDER_NAME: str = "自定义"  # 显示名称

    # 向量数据库
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_URL: str = "http://localhost:6333"

    # Redis缓存
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379"

    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 文件存储
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB

    # LLM成本优化
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 3600
    ENABLE_SEMANTIC_CACHE: bool = True
    SEMANTIC_CACHE_THRESHOLD: float = 0.9
    DAILY_BUDGET: float = 10.0
    ENABLE_BUDGET_LIMIT: bool = True

    # Agent配置
    ENABLE_AGENT_TEAM: bool = True
    AGENT_TIMEOUT: int = 300
    AGENT_MAX_TURNS: int = 10

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./data/logs/app.log"

    # 请求限流配置
    RATE_LIMIT_PER_MINUTE: int = 60

    # 安全响应头配置
    CSP_DEFAULT_SRC: str = "'self'"
    CSP_SCRIPT_SRC: str = "'self' 'unsafe-inline' 'unsafe-eval'"
    CSP_STYLE_SRC: str = "'self' 'unsafe-inline'"
    CSP_IMG_SRC: str = "'self' data: https:"
    CSP_CONNECT_SRC: str = "'self' http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建配置实例
settings = Settings()
