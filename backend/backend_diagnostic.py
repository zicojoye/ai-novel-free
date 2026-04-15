#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端诊断工具 - 检查启动前的问题
"""

import sys
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    print("=" * 60)
    print("🐍 检查Python版本")
    print("=" * 60)

    version = sys.version_info
    print(f"当前版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低! 需要Python 3.8+")
        return False

    print("✅ Python版本符合要求")
    return True


def check_dependencies():
    """检查依赖"""
    print("\n" + "=" * 60)
    print("📦 检查依赖包")
    print("=" * 60)

    required = {
        'fastapi': 'FastAPI框架',
        'uvicorn': 'ASGI服务器',
        'pydantic': '数据验证',
        'pydantic_settings': '配置管理',
        'sqlmodel': '数据库ORM',
        'sqlalchemy': 'SQLAlchemy',
        'aiosqlite': '异步SQLite',
    }

    optional = {
        'langchain': 'LangChain AI框架',
        'langchain_openai': 'OpenAI集成',
        'langchain_anthropic': 'Anthropic集成',
        'qdrant_client': 'Qdrant向量数据库',
        'redis': 'Redis缓存',
    }

    missing_required = []
    missing_optional = []

    for pkg, desc in required.items():
        try:
            __import__(pkg)
            print(f"✓ {pkg} - {desc}")
        except ImportError:
            print(f"✗ {pkg} - {desc} (缺失)")
            missing_required.append(pkg)

    for pkg, desc in optional.items():
        try:
            __import__(pkg)
            print(f"✓ {pkg} - {desc} (可选)")
        except ImportError:
            print(f"⚠️  {pkg} - {desc} (可选,未安装)")
            missing_optional.append(pkg)

    if missing_required:
        print(f"\n❌ 缺少必需依赖: {', '.join(missing_required)}")
        print("请运行: pip install -r requirements.txt")
        return False

    if missing_optional:
        print(f"\n⚠️  缺少可选依赖: {', '.join(missing_optional)}")
        print("这些依赖用于AI功能,可以稍后安装")

    print("\n✅ 关键依赖检查通过")
    return True


def check_file_structure():
    """检查文件结构"""
    print("\n" + "=" * 60)
    print("📁 检查文件结构")
    print("=" * 60)

    backend_dir = Path(__file__).parent
    required_files = [
        'main.py',
        'requirements.txt',
        '.env',
        'app/__init__.py',
        'app/core/__init__.py',
        'app/core/config.py',
        'app/core/database.py',
        'app/models/__init__.py',
        'app/models/project.py',
        'app/models/chapter.py',
        'app/api/__init__.py',
    ]

    missing = []

    for file_path in required_files:
        full_path = backend_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (缺失)")
            missing.append(file_path)

    if missing:
        print(f"\n❌ 缺少文件: {', '.join(missing)}")
        return False

    print("\n✅ 文件结构完整")
    return True


def check_config():
    """检查配置"""
    print("\n" + "=" * 60)
    print("⚙️  检查配置")
    print("=" * 60)

    try:
        from app.core.config import settings

        print(f"✓ 配置加载成功")
        print(f"  APP_NAME: {settings.APP_NAME}")
        print(f"  APP_VERSION: {settings.APP_VERSION}")
        print(f"  APP_ENV: {settings.APP_ENV}")
        print(f"  BACKEND_HOST: {settings.BACKEND_HOST}")
        print(f"  BACKEND_PORT: {settings.BACKEND_PORT}")
        print(f"  DATABASE_URL: {settings.DATABASE_URL}")

        # 检查API密钥
        if settings.OPENAI_API_KEY:
            print(f"  OPENAI_API_KEY: ✓ 已配置")
        else:
            print(f"  OPENAI_API_KEY: ⚠️  未配置")

        print("\n✅ 配置检查通过")
        return True

    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False


def check_database():
    """检查数据库"""
    print("\n" + "=" * 60)
    print("🗄️  检查数据库")
    print("=" * 60)

    try:
        from app.core.database import async_engine

        print("✓ 数据库引擎创建成功")
        print(f"  数据库类型: SQLite (异步)")

        # 检查数据库文件
        backend_dir = Path(__file__).parent
        db_path = backend_dir / "data" / "ai_novel.db"

        if db_path.exists():
            size = db_path.stat().st_size
            print(f"  数据库文件: {db_path}")
            print(f"  文件大小: {size} bytes")
        else:
            print(f"  数据库文件: 将在首次启动时创建")

        print("\n✅ 数据库检查通过")
        return True

    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False


def check_imports():
    """检查关键导入"""
    print("\n" + "=" * 60)
    print("📥 检查模块导入")
    print("=" * 60)

    try:
        print("导入核心模块...")
        from app.core.config import settings
        from app.core.database import init_db
        print("✓ 核心模块导入成功")

        print("\n导入模型模块...")
        from app.models import (
            Project,
            Chapter,
            WorldBuildingElement,
            PlotPoint,
            PlotLine,
            KnowledgeItem,
            Agent,
            AgentTask,
            PromptTemplate
        )
        print("✓ 模型模块导入成功")

        print("\n导入API模块...")
        from app.api import projects, chapters, worldbuilding, plot, knowledge, agents, prompts, ai_tasks
        print("✓ API模块导入成功")

        print("\n导入FastAPI...")
        from fastapi import FastAPI
        print("✓ FastAPI导入成功")

        print("\n✅ 所有模块导入成功")
        return True

    except Exception as e:
        print(f"\n❌ 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_port():
    """检查端口是否可用"""
    print("\n" + "=" * 60)
    print("🔌 检查端口")
    print("=" * 60)

    import socket

    port = 8000
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
        print(f"✓ 端口 {port} 可用")
        return True
    except OSError:
        print(f"⚠️  端口 {port} 已被占用")
        print("提示: 可以修改配置文件中的 BACKEND_PORT")
        return True  # 不阻塞启动


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🔍 AI Novel Platform 后端诊断工具")
    print("=" * 60)
    print()

    results = []

    # 运行所有检查
    results.append(("Python版本", check_python_version()))
    results.append(("依赖包", check_dependencies()))
    results.append(("文件结构", check_file_structure()))
    results.append(("配置", check_config()))
    results.append(("数据库", check_database()))
    results.append(("模块导入", check_imports()))
    results.append(("端口", check_port()))

    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 诊断结果汇总")
    print("=" * 60)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s} {status}")

    failed = [name for name, result in results if not result]

    print()
    if failed:
        print(f"❌ 以下检查失败: {', '.join(failed)}")
        print("\n请先解决这些问题再启动后端服务")
        sys.exit(1)
    else:
        print("✅ 所有检查通过! 可以启动后端服务")
        print("\n启动命令:")
        print("  python main.py")
        print("  或")
        print("  python start.py")


if __name__ == "__main__":
    main()
