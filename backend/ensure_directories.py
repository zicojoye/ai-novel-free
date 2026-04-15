#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
确保必要的目录存在
"""

import os
from pathlib import Path


def ensure_directories():
    """确保所有必要的目录存在"""
    base_dir = Path(__file__).parent

    # 需要创建的目录列表
    directories = [
        base_dir / "data",
        base_dir / "data" / "uploads",
        base_dir / "data" / "logs",
    ]

    print("🔍 检查并创建必要的目录...")

    for directory in directories:
        if not directory.exists():
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"✓ 创建目录: {directory}")
            except Exception as e:
                print(f"✗ 创建目录失败: {directory}")
                print(f"  错误: {e}")
        else:
            print(f"✓ 目录已存在: {directory}")

    print("\n✅ 目录检查完成!")


if __name__ == "__main__":
    ensure_directories()
