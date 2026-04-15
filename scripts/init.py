#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化脚本 - 创建必要的目录和文件
"""

import os
import sys
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def init_project():
    """初始化项目结构"""

    # 项目根目录
    project_root = Path(__file__).parent
    data_dir = project_root / "data"

    # 创建必要目录
    dirs = [
        data_dir,
        data_dir / "uploads",
        data_dir / "logs",
        data_dir / "db",
        data_dir / "cache",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Create directory: {dir_path}")

    # 创建 .gitkeep 文件
    for dir_path in dirs:
        (dir_path / ".gitkeep").touch()

    # 检查 .env 文件
    env_example = project_root / ".env.example"
    env_file = project_root / ".env"

    if not env_file.exists() and env_example.exists():
        # 复制环境变量模板
        import shutil
        shutil.copy(env_example, env_file)
        print(f"[OK] Create .env file from .env.example")
    elif env_file.exists():
        print(f"[OK] .env file already exists")
    else:
        print(f"[WARNING] .env.example file not found")

    print("\n[SUCCESS] Project initialization completed!")
    print("\nNext steps:")
    print("1. Edit .env file, configure API Keys")
    print("2. cd backend && pip install -r requirements.txt")
    print("3. cd frontend && npm install")
    print("4. Run start.bat")

if __name__ == "__main__":
    init_project()
