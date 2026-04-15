#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全中间件
提供请求限流、安全头、XSS防护等安全功能
"""

from fastapi import Request, HTTPException, status
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from collections import defaultdict
from typing import Dict, List
import re

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    请求限流中间件
    """
    
    def __init__(self, app, max_requests: int = 60, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        # 获取客户端IP
        client_ip = self._get_client_ip(request)
        
        # 检查限流
        if not self._check_rate_limit(client_ip):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": "请求过于频繁,请稍后再试"
                }
            )
        
        # 记录请求
        self._record_request(client_ip)
        
        # 继续处理请求
        response = await call_next(request)
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端IP地址"""
        # 检查代理头
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 使用客户端地址
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """检查是否超过限流"""
        now = time.time()
        requests = self.requests[client_ip]
        
        # 移除过期的请求记录
        self.requests[client_ip] = [
            req_time for req_time in requests
            if now - req_time < self.window
        ]
        
        # 检查请求数量
        return len(self.requests[client_ip]) < self.max_requests
    
    def _record_request(self, client_ip: str):
        """记录请求"""
        self.requests[client_ip].append(time.time())


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    安全响应头中间件
    """
    
    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        response = await call_next(request)
        
        # 添加安全响应头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # CSP (Content Security Policy)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self' http://localhost:8000; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        
        return response


class XSSProtectionMiddleware(BaseHTTPMiddleware):
    """
    XSS防护中间件
    """
    
    # 危险的HTML标签和属性
    DANGEROUS_TAGS = {
        'script', 'iframe', 'object', 'embed', 'form',
        'input', 'button', 'link', 'meta', 'style'
    }
    
    DANGEROUS_ATTRS = {
        'onload', 'onerror', 'onclick', 'onmouseover',
        'onfocus', 'onblur', 'onsubmit', 'javascript:',
        'data:', 'vbscript:'
    }
    
    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        # 检查请求体中的HTML内容
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            
            if "application/json" in content_type:
                try:
                    body = await request.json()
                    if self._contains_xss(body):
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "success": False,
                                "error": "检测到潜在的XSS攻击"
                            }
                        )
                except:
                    pass
        
        response = await call_next(request)
        return response
    
    def _contains_xss(self, data: any) -> bool:
        """递归检查是否包含XSS攻击"""
        if isinstance(data, dict):
            for key, value in data.items():
                if self._contains_xss(key) or self._contains_xss(value):
                    return True
        
        elif isinstance(data, list):
            for item in data:
                if self._contains_xss(item):
                    return True
        
        elif isinstance(data, str):
            # 检查危险标签
            lower_str = data.lower()
            for tag in self.DANGEROUS_TAGS:
                if f"<{tag}" in lower_str:
                    return True
            
            # 检查危险属性
            for attr in self.DANGEROUS_ATTRS:
                if attr in lower_str:
                    return True
        
        return False


class SQLInjectionProtectionMiddleware(BaseHTTPMiddleware):
    """
    SQL注入防护中间件
    """
    
    # SQL注入特征
    SQL_INJECTION_PATTERNS = [
        r"(\bOR\b|\bAND\b).{1,6}=\b1\b",
        r"(\bOR\b|\bAND\b).{1,6}=\b0\b",
        r"\bUNION\b.*\bSELECT\b",
        r"'.*'.*=.*'.*'",
        r"\bSELECT\b.*\bFROM\b.*\bWHERE\b",
        r";\s*(DROP|DELETE|INSERT|UPDATE|ALTER|EXEC)",
        r"--.*$",  # 注释
        r"/\*.*\*/",  # 多行注释
    ]
    
    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        # 检查查询参数和请求体
        if self._check_sql_injection(request):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "error": "检测到潜在的SQL注入攻击"
                }
            )
        
        response = await call_next(request)
        return response
    
    def _check_sql_injection(self, request: Request) -> bool:
        """检查SQL注入"""
        # 检查查询参数
        for key, value in request.query_params.items():
            if self._match_sql_pattern(str(value)):
                return True
        
        # 检查路径参数
        for key, value in request.path_params.items():
            if self._match_sql_pattern(str(value)):
                return True
        
        return False
    
    def _match_sql_pattern(self, text: str) -> bool:
        """匹配SQL注入模式"""
        text_upper = text.upper()
        
        for pattern in self.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return True
        
        return False


def create_security_middleware() -> List[Middleware]:
    """
    创建安全中间件列表
    
    Returns:
        中间件列表
    """
    middleware = [
        # 限流中间件
        Middleware(
            RateLimitMiddleware,
            max_requests=SecurityConfig.RATE_LIMIT_PER_MINUTE,
            window=60
        ),
        
        # 安全响应头
        Middleware(SecurityHeadersMiddleware),
        
        # XSS防护
        Middleware(XSSProtectionMiddleware),
        
        # SQL注入防护
        Middleware(SQLInjectionProtectionMiddleware),
        
        # CORS中间件(在main.py中单独配置)
        # Middleware(
        #     CORSMiddleware,
        #     allow_origins=settings.BACKEND_CORS_ORIGINS,
        #     allow_credentials=True,
        #     allow_methods=["*"],
        #     allow_headers=["*"],
        # ),
    ]
    
    return middleware


class SecurityConfig:
    """
    安全配置
    """
    
    # 限流配置
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_PER_MINUTE = 60
    
    # 文件上传配置
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = {
        'text/plain',
        'text/markdown',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/png',
        'image/gif',
    }
