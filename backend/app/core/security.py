#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全配置模块
提供密码加密、JWT令牌、CORS等安全功能
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import hashlib
import re
from fastapi import HTTPException, status

from app.core.config import settings


# 密码加密上下文
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # 增加密钥强度
    bcrypt__ident="2b"   # 使用2b版本
)


def generate_secret_key(length: int = 64) -> str:
    """
    生成安全的随机密钥
    
    Args:
        length: 密钥长度(字节)
    
    Returns:
        十六进制格式的密钥字符串
    """
    return secrets.token_hex(length)


def hash_password(password: str) -> str:
    """
    加密密码
    
    Args:
        password: 明文密码
    
    Returns:
        加密后的密码hash
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 加密后的密码hash
    
    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建JWT访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
    
    Returns:
        JWT令牌字符串
    """
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    
    # 生成JWT令牌
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    解码JWT访问令牌
    
    Args:
        token: JWT令牌字符串
    
    Returns:
        解码后的数据
    
    Raises:
        HTTPException: 令牌无效或过期
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"}
        )


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    验证密码强度
    
    Args:
        password: 要验证的密码
    
    Returns:
        (是否有效, 错误消息)
    """
    if len(password) < 8:
        return False, "密码长度至少为8个字符"
    
    if len(password) > 128:
        return False, "密码长度不能超过128个字符"
    
    # 检查是否包含数字
    if not re.search(r"\d", password):
        return False, "密码必须包含至少一个数字"
    
    # 检查是否包含大写字母
    if not re.search(r"[A-Z]", password):
        return False, "密码必须包含至少一个大写字母"
    
    # 检查是否包含小写字母
    if not re.search(r"[a-z]", password):
        return False, "密码必须包含至少一个小写字母"
    
    # 检查是否包含特殊字符
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "密码必须包含至少一个特殊字符"
    
    return True, ""


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
    
    Returns:
        是否有效
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_filename(filename: str) -> str:
    """
    清理文件名,防止路径遍历攻击
    
    Args:
        filename: 原始文件名
    
    Returns:
        安全的文件名
    """
    # 移除路径分隔符
    filename = filename.replace("/", "").replace("\\", "")
    
    # 移除危险字符
    filename = re.sub(r'[<>:"|?*]', '', filename)
    
    # 限制长度
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:200] + ('.' + ext if ext else '')
    
    return filename


def generate_content_hash(content: str) -> str:
    """
    生成内容哈希值
    
    Args:
        content: 要哈希的内容
    
    Returns:
        SHA256哈希字符串
    """
    return hashlib.sha256(content.encode()).hexdigest()


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """
    掩码敏感数据
    
    Args:
        data: 敏感数据(如API密钥)
        visible_chars: 可见的字符数
    
    Returns:
        掩码后的数据
    """
    if len(data) <= visible_chars:
        return "*" * len(data)
    
    return data[:visible_chars] + "*" * (len(data) - visible_chars)


class SecurityConfig:
    """
    安全配置类
    """
    
    # 密码策略
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL_CHAR = True
    
    # 令牌配置
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    # 文件上传安全
    ALLOWED_EXTENSIONS = {
        '.txt', '.md', '.docx', '.doc',
        '.pdf', '.jpg', '.jpeg', '.png', '.gif'
    }
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # 请求限流
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_PER_MINUTE = 60
    
    # CORS配置
    DEFAULT_CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    @classmethod
    def is_file_extension_allowed(cls, filename: str) -> bool:
        """
        检查文件扩展名是否允许
        
        Args:
            filename: 文件名
        
        Returns:
            是否允许
        """
        import os
        ext = os.path.splitext(filename)[1].lower()
        return ext in cls.ALLOWED_EXTENSIONS
    
    @classmethod
    def get_safe_filename(cls, filename: str) -> str:
        """
        获取安全的文件名
        
        Args:
            filename: 原始文件名
        
        Returns:
            安全的文件名
        """
        import os
        
        # 清理文件名
        safe_name = sanitize_filename(filename)
        
        # 确保有扩展名
        name, ext = os.path.splitext(safe_name)
        if not ext and '.' in filename:
            ext = '.' + filename.split('.')[-1].lower()
        
        # 添加时间戳防止冲突
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        safe_name = f"{timestamp}_{name}{ext}"
        
        return safe_name


# 安全验证装饰器
def require_https(f):
    """
    要求HTTPS的装饰器
    """
    def wrapper(*args, **kwargs):
        # 在生产环境可以启用此检查
        # from fastapi import Request
        # request: Request = kwargs.get('request')
        # if request and not request.url.scheme == 'https':
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="只允许HTTPS连接"
        #     )
        return f(*args, **kwargs)
    return wrapper


# 导出常用函数
__all__ = [
    'generate_secret_key',
    'hash_password',
    'verify_password',
    'create_access_token',
    'decode_access_token',
    'validate_password_strength',
    'validate_email',
    'sanitize_filename',
    'generate_content_hash',
    'mask_sensitive_data',
    'SecurityConfig',
    'require_https',
]
