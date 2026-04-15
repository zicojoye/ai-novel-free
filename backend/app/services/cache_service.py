#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存服务 - 多级缓存系统
"""

import hashlib
import json
import time
from typing import Optional, Dict, Any
from redis import Redis

from app.core.config import settings


class MemoryCache:
    """L1: 内存缓存"""

    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = ttl

    def _generate_key(self, prompt: str, model: str) -> str:
        """生成缓存键"""
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Optional[str]:
        """获取缓存"""
        key = self._generate_key(prompt, model)

        if key in self.cache:
            entry = self.cache[key]

            # 检查过期
            if time.time() - entry["timestamp"] < self.ttl:
                return entry["response"]
            else:
                del self.cache[key]

        return None

    def set(self, prompt: str, model: str, response: str):
        """设置缓存"""
        key = self._generate_key(prompt, model)

        # LRU淘汰
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]["timestamp"])
            del self.cache[oldest_key]

        self.cache[key] = {
            "response": response,
            "timestamp": time.time()
        }


class RedisCache:
    """L2: Redis缓存"""

    def __init__(self, ttl: int = 3600):
        self.client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        self.ttl = ttl

    def _generate_key(self, prompt: str, model: str) -> str:
        """生成Redis键"""
        content = f"{model}:{prompt}"
        return f"llm:cache:{hashlib.md5(content.encode()).hexdigest()}"

    def get(self, prompt: str, model: str) -> Optional[str]:
        """获取缓存"""
        key = self._generate_key(prompt, model)
        data = self.client.get(key)

        if data:
            return json.loads(data)["response"]
        return None

    def set(self, prompt: str, model: str, response: str):
        """设置缓存"""
        key = self._generate_key(prompt, model)
        data = json.dumps({"response": response})
        self.client.setex(key, self.ttl, data)


class CacheService:
    """统一缓存服务"""

    def __init__(self):
        self.l1 = MemoryCache(max_size=1000, ttl=300)
        self.l2 = RedisCache(ttl=3600) if settings.ENABLE_CACHE else None

        self.stats = {
            "l1_hits": 0,
            "l2_hits": 0,
            "llm_calls": 0
        }

    async def get(self, prompt: str, model: str) -> Optional[str]:
        """多级缓存获取"""
        # L1缓存
        result = self.l1.get(prompt, model)
        if result:
            self.stats["l1_hits"] += 1
            return result

        # L2缓存
        if self.l2:
            result = self.l2.get(prompt, model)
            if result:
                self.stats["l2_hits"] += 1
                # 回填L1
                self.l1.set(prompt, model, result)
                return result

        return None

    async def set(self, prompt: str, model: str, response: str):
        """多级缓存设置"""
        # L1缓存
        self.l1.set(prompt, model, response)

        # L2缓存
        if self.l2:
            self.l2.set(prompt, model, response)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        total_hits = self.stats["l1_hits"] + self.stats["l2_hits"]
        total_requests = total_hits + self.stats["llm_calls"]

        return {
            **self.stats,
            "hit_rate": total_hits / total_requests if total_requests > 0 else 0
        }


# 全局实例
cache_service = CacheService()
