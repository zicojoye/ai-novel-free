#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI模型管理API - 支持动态获取模型列表、自定义模型、网页端API Key管理
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict
from pathlib import Path
import re
import httpx

from app.core.config import settings

router = APIRouter()

# .env 文件路径（相对于 backend 目录）
ENV_FILE = Path(__file__).parent.parent.parent / ".env"


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    description: str
    is_custom: bool = False


class CustomModelRequest(BaseModel):
    id: str
    name: str
    provider: str
    description: Optional[str] = ""


class ModelsResponse(BaseModel):
    models: List[ModelInfo]
    default_model: str


class ApiKeyUpdateRequest(BaseModel):
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    # 自定义 Provider
    custom_api_key: Optional[str] = None
    custom_api_base: Optional[str] = None
    custom_model_id: Optional[str] = None
    custom_provider_name: Optional[str] = None


class ApiKeyInfo(BaseModel):
    id: str
    name: str
    configured: bool
    masked_key: str        # 脱敏显示，如 sk-****xxxx
    connection_status: str  # "connected" | "disconnected" | "unconfigured" | "testing"
    active_agents: List[str]  # 当前正在使用该 Key 的 Agent 名称列表


# 内置预设模型列表
PRESET_MODELS: List[ModelInfo] = [
    # OpenAI
    ModelInfo(id="gpt-4o", name="GPT-4o", provider="openai", description="OpenAI最强多模态模型"),
    ModelInfo(id="gpt-4o-mini", name="GPT-4o mini", provider="openai", description="高性价比快速模型"),
    ModelInfo(id="gpt-4-turbo", name="GPT-4 Turbo", provider="openai", description="支持128K上下文"),
    ModelInfo(id="gpt-3.5-turbo", name="GPT-3.5 Turbo", provider="openai", description="快速低成本模型"),
    # Anthropic
    ModelInfo(id="claude-3-5-sonnet-20241022", name="Claude 3.5 Sonnet", provider="anthropic", description="Anthropic最强推理模型"),
    ModelInfo(id="claude-3-5-haiku-20241022", name="Claude 3.5 Haiku", provider="anthropic", description="快速轻量模型"),
    ModelInfo(id="claude-3-opus-20240229", name="Claude 3 Opus", provider="anthropic", description="Anthropic高能力模型"),
    # DeepSeek
    ModelInfo(id="deepseek-chat", name="DeepSeek Chat", provider="deepseek", description="DeepSeek对话模型"),
    ModelInfo(id="deepseek-reasoner", name="DeepSeek Reasoner", provider="deepseek", description="DeepSeek推理模型"),
    # Gemini
    ModelInfo(id="gemini-1.5-pro", name="Gemini 1.5 Pro", provider="gemini", description="Google长上下文模型"),
    ModelInfo(id="gemini-1.5-flash", name="Gemini 1.5 Flash", provider="gemini", description="Google快速模型"),
    ModelInfo(id="gemini-2.0-flash", name="Gemini 2.0 Flash", provider="gemini", description="Google最新快速模型"),
]


def mask_key(key: str) -> str:
    """脱敏显示 API Key：保留前4位和后4位"""
    if not key:
        return ""
    if len(key) <= 8:
        return "*" * len(key)
    return key[:4] + "*" * (len(key) - 8) + key[-4:]


def get_all_models() -> List[ModelInfo]:
    """获取全部模型（预设 + 自定义）"""
    models = list(PRESET_MODELS)
    for m in settings.CUSTOM_MODELS:
        parts = m.split(":", 2)
        if len(parts) >= 2:
            mid = parts[0].strip()
            mname = parts[1].strip()
            mprovider = parts[2].strip() if len(parts) > 2 else "custom"
            models.append(ModelInfo(
                id=mid,
                name=mname,
                provider=mprovider,
                description="自定义模型",
                is_custom=True
            ))
    return models


def read_env_file() -> Dict[str, str]:
    """读取 .env 文件，返回键值对字典"""
    env_dict: Dict[str, str] = {}
    if not ENV_FILE.exists():
        return env_dict
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env_dict[k.strip()] = v.strip().strip('"').strip("'")
    return env_dict


def write_env_key(env_var: str, value: str):
    """将指定环境变量写入 .env 文件（更新或追加）"""
    if not ENV_FILE.exists():
        ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
        ENV_FILE.write_text("", encoding="utf-8")

    content = ENV_FILE.read_text(encoding="utf-8")
    pattern = re.compile(rf'^({re.escape(env_var)}\s*=).*$', re.MULTILINE)

    if pattern.search(content):
        new_content = pattern.sub(rf'\g<1>{value}', content)
    else:
        new_content = content.rstrip('\n') + f'\n{env_var}={value}\n'

    ENV_FILE.write_text(new_content, encoding="utf-8")
    setattr(settings, env_var, value)


def get_active_agents_for_provider(provider_id: str) -> List[str]:
    """获取当前正在使用某 provider 的 Agent 列表"""
    try:
        from app.agents.agent_manager import agent_manager
        active = []
        default_provider = settings.DEFAULT_LLM_PROVIDER
        for agent in agent_manager.get_all_agents():
            if default_provider == provider_id:
                if hasattr(agent, 'last_activity') and agent.last_activity:
                    active.append(agent.name)
        return active
    except Exception:
        return []


async def test_provider_connection(provider_id: str, api_key: str) -> str:
    """快速测试 provider 连通性，返回 'connected' 或 'disconnected'"""
    if not api_key:
        return "unconfigured"
    try:
        timeout = httpx.Timeout(8.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            if provider_id == "openai":
                r = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                return "connected" if r.status_code == 200 else "disconnected"
            elif provider_id == "anthropic":
                r = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={"model": "claude-3-haiku-20240307", "max_tokens": 1,
                          "messages": [{"role": "user", "content": "hi"}]}
                )
                return "connected" if r.status_code in [200, 400] else "disconnected"
            elif provider_id == "deepseek":
                r = await client.get(
                    "https://api.deepseek.com/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                return "connected" if r.status_code == 200 else "disconnected"
            elif provider_id == "gemini":
                r = await client.get(
                    f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                )
                return "connected" if r.status_code == 200 else "disconnected"
    except Exception:
        return "disconnected"
    return "disconnected"


async def test_custom_connection(base_url: str, api_key: str) -> str:
    """测试自定义 Provider 连通性（调用 /models 列表接口）"""
    if not base_url or not api_key:
        return "unconfigured"
    try:
        # 规范化 base_url
        base = base_url.rstrip("/")
        if not base.endswith("/v1"):
            models_url = base + "/v1/models"
        else:
            models_url = base + "/models"
        timeout = httpx.Timeout(8.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(
                models_url,
                headers={"Authorization": f"Bearer {api_key}"}
            )
            return "connected" if r.status_code == 200 else "disconnected"
    except Exception:
        return "disconnected"


@router.get("", response_model=ModelsResponse)
async def list_models():
    """获取所有可用模型列表"""
    return ModelsResponse(
        models=get_all_models(),
        default_model=settings.DEFAULT_MODEL
    )


@router.get("/providers")
async def list_providers():
    """获取已配置API Key的提供商（简版，不测连通性）"""
    configured = []
    provider_map = [
        ("openai", "OpenAI", settings.OPENAI_API_KEY),
        ("anthropic", "Anthropic", settings.ANTHROPIC_API_KEY),
        ("deepseek", "DeepSeek", settings.DEEPSEEK_API_KEY),
        ("gemini", "Gemini", settings.GEMINI_API_KEY),
    ]
    for pid, pname, key in provider_map:
        configured.append({"id": pid, "name": pname, "configured": bool(key)})
    return {"providers": configured}


@router.get("/keys")
async def get_api_keys():
    """获取 API Key 配置详情（含脱敏值、连接状态、使用中的 Agent）"""
    provider_map = [
        ("openai", "OpenAI", settings.OPENAI_API_KEY),
        ("anthropic", "Anthropic", settings.ANTHROPIC_API_KEY),
        ("deepseek", "DeepSeek", settings.DEEPSEEK_API_KEY),
        ("gemini", "Gemini (Google)", settings.GEMINI_API_KEY),
        ("custom", settings.CUSTOM_PROVIDER_NAME or "自定义", settings.CUSTOM_API_KEY),
    ]
    result = []
    for pid, pname, key in provider_map:
        active_agents = get_active_agents_for_provider(pid)
        entry: Dict = {
            "id": pid,
            "name": pname,
            "configured": bool(key),
            "masked_key": mask_key(key),
            "connection_status": "connected" if key else "unconfigured",
            "active_agents": active_agents,
        }
        if pid == "custom":
            entry["api_base"] = settings.CUSTOM_API_BASE
            entry["model_id"] = settings.CUSTOM_MODEL_ID
            entry["provider_name"] = settings.CUSTOM_PROVIDER_NAME
        result.append(entry)
    return {"keys": result}


@router.put("/keys")
async def update_api_keys(data: ApiKeyUpdateRequest):
    """更新 API Key（写入 .env 文件并热更新 settings）"""
    updated = []
    key_map = [
        ("openai", "OPENAI_API_KEY", data.openai_api_key),
        ("anthropic", "ANTHROPIC_API_KEY", data.anthropic_api_key),
        ("deepseek", "DEEPSEEK_API_KEY", data.deepseek_api_key),
        ("gemini", "GEMINI_API_KEY", data.gemini_api_key),
        ("custom_key", "CUSTOM_API_KEY", data.custom_api_key),
        ("custom_base", "CUSTOM_API_BASE", data.custom_api_base),
        ("custom_model", "CUSTOM_MODEL_ID", data.custom_model_id),
        ("custom_name", "CUSTOM_PROVIDER_NAME", data.custom_provider_name),
    ]
    for pid, env_var, new_key in key_map:
        if new_key is not None:
            write_env_key(env_var, new_key)
            updated.append(pid)

    # 清空 LLM 客户端缓存，让热更新后的 Key 生效
    try:
        from app.services.llm_service import llm_service
        llm_service.router._clients.clear()
    except Exception:
        pass

    return {"success": True, "updated": updated}


@router.post("/keys/test/{provider_id}")
async def test_api_key_connection(provider_id: str):
    """测试指定 provider 的 API Key 连通性"""
    key_map = {
        "openai": settings.OPENAI_API_KEY,
        "anthropic": settings.ANTHROPIC_API_KEY,
        "deepseek": settings.DEEPSEEK_API_KEY,
        "gemini": settings.GEMINI_API_KEY,
    }
    if provider_id == "custom":
        api_key = settings.CUSTOM_API_KEY
        base_url = settings.CUSTOM_API_BASE
        if not api_key or not base_url:
            return {"provider_id": provider_id, "status": "unconfigured", "message": "请先填写密钥和 API 地址"}
        status = await test_custom_connection(base_url, api_key)
        msg_map = {
            "connected": "连接成功",
            "disconnected": "连接失败，请检查地址和 Key 是否正确",
            "unconfigured": "未配置",
        }
        return {"provider_id": provider_id, "status": status, "message": msg_map.get(status, status)}

    if provider_id not in key_map:
        return {"provider_id": provider_id, "status": "unknown", "message": "未知的 provider"}
    api_key = key_map[provider_id]
    if not api_key:
        return {"provider_id": provider_id, "status": "unconfigured", "message": "未配置 API Key"}
    status = await test_provider_connection(provider_id, api_key)
    msg_map = {
        "connected": "连接成功",
        "disconnected": "连接失败，请检查 Key 是否有效或网络是否可达",
        "unconfigured": "未配置",
    }
    return {"provider_id": provider_id, "status": status, "message": msg_map.get(status, status)}
