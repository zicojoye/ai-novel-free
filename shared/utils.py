#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享工具函数
"""

import hashlib
import json
from datetime import datetime
from typing import Any, Optional
import re


def generate_id(prefix: str = "") -> str:
    """生成唯一ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique = hashlib.md5(timestamp.encode()).hexdigest()[:8]
    return f"{prefix}{timestamp}{unique}" if prefix else f"{timestamp}{unique}"


def hash_text(text: str) -> str:
    """计算文本哈希"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def count_words(text: str) -> int:
    """统计字数(支持中文)"""
    # 移除空白字符
    text = text.strip()
    if not text:
        return 0
    
    # 中文+英文混合字数统计
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    
    return chinese_chars + english_words


def count_tokens(text: str) -> int:
    """估算token数量(粗略估计)"""
    # 中文字符按1 token, 英文单词按0.75 token估算
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    
    return chinese_chars + int(english_words * 0.75)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """解析日期时间字符串"""
    try:
        return datetime.strptime(dt_str, format_str)
    except Exception:
        return None


def truncate_text(text: str, max_length: int = 100) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def clean_whitespace(text: str) -> str:
    """清理多余空白"""
    # 替换多个空格为单个空格
    text = re.sub(r' +', ' ', text)
    # 替换多个换行为单个换行
    text = re.sub(r'\n+', '\n', text)
    # 去除首尾空白
    text = text.strip()
    
    return text


def extract_chapter_number(title: str) -> Optional[int]:
    """从章节标题提取章节号"""
    # 匹配 "第X章" 或 "Chapter X" 等格式
    patterns = [
        r'第(\d+)章',
        r'Chapter (\d+)',
        r'Ch\.? (\d+)',
        r'(\d+)\.',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """验证URL格式"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def sanitize_filename(filename: str) -> str:
    """清理文件名"""
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    
    # 限制长度
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:200] + ('.' + ext if ext else '')
    
    return filename


def pretty_json(obj: Any, indent: int = 2) -> str:
    """格式化JSON为字符串"""
    return json.dumps(obj, ensure_ascii=False, indent=indent)


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """合并两个字典(深度合并)"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """将文本分割成块"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # 尽量在句子边界分割
        if end < len(text):
            # 寻找最近的句号、问号、感叹号
            for delimiter in ['。', '！', '？', '.', '!', '?', '\n']:
                delimiter_pos = text.rfind(delimiter, start, end)
                if delimiter_pos > start:
                    end = delimiter_pos + 1
                    break
        
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks


def calculate_similarity(text1: str, text2: str) -> float:
    """计算两段文本的相似度(简单Jaccard相似度)"""
    set1 = set(text1)
    set2 = set(text2)
    
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0
