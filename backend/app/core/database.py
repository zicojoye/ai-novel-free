#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库配置
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator

from app.core.config import settings


# 创建异步引擎
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=settings.LOG_LEVEL == "DEBUG",
    future=True
)

# 创建异步会话工厂
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """初始化数据库"""
    try:
        # 导入所有模型以注册到SQLModel.metadata
        from app.models import (
            Project,
            Chapter,
            WorldBuilding,
            Foreshadow,
            Hook,
            KnowledgeEntry,
            Agent,
            AgentTask,
            Prompt
        )

        # 创建所有表
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")
        # 不抛出异常,允许应用继续运行
        raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
