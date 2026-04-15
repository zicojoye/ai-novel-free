#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动脚本 - 自动检查依赖后启动后端服务
已安装的依赖会跳过,没安装的会自动安装
"""

import sys
import subprocess
import os
from pathlib import Path


def check_and_install_deps():
    """检查并安装依赖"""
    print("=" * 60)
    print("🔍 检查依赖...")
    print("=" * 60)
    print()

    # 尝试导入关键包
    missing_deps = []
    try:
        import fastapi
        print("✓ fastapi")
    except ImportError:
        missing_deps.append("fastapi")

    try:
        import uvicorn
        print("✓ uvicorn")
    except ImportError:
        missing_deps.append("uvicorn")

    try:
        import sqlmodel
        print("✓ sqlmodel")
    except ImportError:
        missing_deps.append("sqlmodel")

    try:
        import langchain
        print("✓ langchain (可选,用于AI功能)")
    except ImportError:
        print("⚠️  langchain 未安装 (可选,用于AI功能)")

    print()

    if not missing_deps:
        print("✅ 所有关键依赖已安装!")
        print()
        return True

    print(f"⚠️  缺少关键依赖: {', '.join(missing_deps)}")
    print()
    print("=" * 60)
    print("📦 自动安装缺失的依赖...")
    print("=" * 60)
    print()

    # 运行依赖安装脚本
    backend_dir = Path(__file__).parent
    install_script = backend_dir / "check_and_install_deps.py"

    if install_script.exists():
        result = subprocess.run(
            [sys.executable, str(install_script)],
            check=False
        )
        if result.returncode == 0:
            print()
            print("✅ 依赖安装完成!")
            print()
            return True
        else:
            print("❌ 依赖安装失败")
            return False
    else:
        print("⚠️  找不到自动安装脚本,尝试手动安装...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=False
        )
        if result.returncode == 0:
            print("✅ 依赖安装完成!")
            return True
        else:
            print("❌ 依赖安装失败")
            print("\n请手动运行: pip install -r requirements.txt")
            return False


def start_server():
    """启动服务器"""
    print("=" * 60)
    print("🚀 启动AI Novel Platform后端服务...")
    print("=" * 60)
    print()

    try:
        import uvicorn

        # 切换到backend目录，确保模块导入路径正确
        backend_dir = Path(__file__).parent
        os.chdir(backend_dir)

        # 必须用字符串形式才能支持reload，同时确保sys.path包含backend目录
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))

        # 启动uvicorn服务器（字符串形式支持reload）
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False  # 生产/直接启动模式，避免reload导致的WARNING
        )

    except KeyboardInterrupt:
        print("\n\n🛑 服务已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n请检查:")
        print("1. 依赖是否正确安装")
        print("2. 端口8000是否被占用")
        print("3. 配置文件是否正确")
        sys.exit(1)


def validate_config():
    """验证配置"""
    print("=" * 60)
    print("🔍 验证配置...")
    print("=" * 60)
    print()

    backend_dir = Path(__file__).parent
    validate_script = backend_dir / "validate_config.py"

    if validate_script.exists():
        result = subprocess.run(
            [sys.executable, str(validate_script)],
            check=False
        )
        
        if result.returncode != 0:
            print("\n" + "=" * 60)
            print("⛔ 配置验证失败!")
            print("=" * 60)
            print()
            print("请先完成以下配置:")
            print("1. 修改 SECRET_KEY (运行: python generate_secret_key.py)")
            print("2. 配置至少一个 AI API 密钥")
            print("3. 确保数据库可访问")
            print()
            print("运行验证脚本查看详细信息:")
            print("  python validate_config.py")
            print()
            confirm = input("是否跳过验证继续启动? (不推荐) (y/N): ").strip().lower()
            if confirm != 'y':
                print("\n启动已取消")
                sys.exit(1)
            else:
                print("\n⚠️  跳过配置验证继续启动...")
                print()
    else:
        print("⚠️  配置验证脚本不存在,跳过验证")
        print()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🎯 AI Novel Platform 后端启动器")
    print("=" * 60)
    print()

    # 1. 检查并安装依赖
    if not check_and_install_deps():
        print("❌ 依赖检查失败,无法启动服务")
        sys.exit(1)

    # 2. 验证配置
    validate_config()

    # 3. 启动服务器
    start_server()


if __name__ == "__main__":
    main()
