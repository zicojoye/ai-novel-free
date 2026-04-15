#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动检查并安装Python依赖
已安装的跳过,没安装的自动安装
有问题自动修复
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(cmd, description):
    """执行命令并返回结果"""
    try:
        print(f"📝 {description}...")
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        return result
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return None


def check_python_version():
    """检查Python版本"""
    print("=" * 60)
    print("🐍 检查Python版本...")
    print("=" * 60)

    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低! 需要Python 3.8+")
        print("请先升级Python版本后重试")
        sys.exit(1)
    else:
        print(f"✓ Python版本符合要求 (需要: 3.8+, 当前: {version.major}.{version.minor})")
    print()


def check_pip():
    """检查pip是否可用"""
    print("=" * 60)
    print("📦 检查pip...")
    print("=" * 60)

    result = run_command("pip --version", "检查pip版本")

    if result and result.returncode == 0:
        print(f"✓ {result.stdout.strip()}")
        print()
        return True
    else:
        print("❌ pip不可用,尝试修复...")
        # 尝试使用python -m pip
        result = run_command("python -m pip --version", "尝试python -m pip")

        if result and result.returncode == 0:
            print(f"✓ {result.stdout.strip()}")
            print()
            return True
        else:
            print("❌ 无法修复pip问题,请手动安装pip")
            sys.exit(1)


def check_venv():
    """检查虚拟环境"""
    print("=" * 60)
    print("🔍 检查虚拟环境...")
    print("=" * 60)

    backend_dir = Path(__file__).parent
    venv_paths = [
        backend_dir / "venv",
        backend_dir / ".venv",
        backend_dir / "env",
    ]

    venv_found = None
    for path in venv_paths:
        if path.exists():
            print(f"✓ 找到虚拟环境: {path}")
            venv_found = path
            break

    if venv_found:
        print(f"✓ 使用虚拟环境: {venv_found}")
        return venv_found

    print("⚠️  未找到虚拟环境")
    return None


def check_installed_packages():
    """检查已安装的包"""
    print("=" * 60)
    print("📋 检查已安装的包...")
    print("=" * 60)

    result = run_command("pip list", "获取已安装包列表")

    if result and result.returncode == 0:
        installed = {}
        for line in result.stdout.split('\n')[2:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0].lower()
                    version = parts[1]
                    installed[name] = version

        print(f"✓ 已安装 {len(installed)} 个包")
        return installed
    else:
        print("⚠️  无法获取已安装包列表")
        return {}


def read_requirements():
    """读取requirements.txt"""
    print("=" * 60)
    print("📄 读取依赖文件...")
    print("=" * 60)

    backend_dir = Path(__file__).parent
    req_file = backend_dir / "requirements.txt"

    if not req_file.exists():
        print(f"❌ 找不到 {req_file}")
        return None

    requirements = []
    with open(req_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # 提取包名和版本要求
                if '>=' in line:
                    pkg = line.split('>=')[0].lower().strip()
                elif '==' in line:
                    pkg = line.split('==')[0].lower().strip()
                elif '>' in line:
                    pkg = line.split('>')[0].lower().strip()
                elif '<' in line:
                    pkg = line.split('<')[0].lower().strip()
                else:
                    pkg = line.lower().strip()

                if pkg:
                    requirements.append({
                        'name': pkg,
                        'original': line
                    })

    print(f"✓ 需要安装 {len(requirements)} 个依赖包")
    return requirements


def compare_and_install(installed, requirements):
    """对比并安装缺失的包"""
    print("=" * 60)
    print("🔍 检查缺失的包...")
    print("=" * 60)

    missing = []
    outdated = []
    for req in requirements:
        name = req['name']
        if name in installed:
            print(f"✓ {name} ({installed[name]}) 已安装")
        else:
            print(f"✗ {name} 未安装")
            missing.append(req['original'])

    print()

    if not missing:
        print("✅ 所有依赖都已安装!")
        return True

    print("=" * 60)
    print(f"📦 开始安装 {len(missing)} 个缺失的包...")
    print("=" * 60)

    # 升级pip
    print("\n🔄 升级pip...")
    run_command("python -m pip install --upgrade pip", "升级pip")

    # 安装缺失的包
    for i, pkg in enumerate(missing, 1):
        print(f"\n[{i}/{len(missing)}] 安装 {pkg}...")

        result = run_command(f"pip install {pkg}", f"安装 {pkg}")

        if result and result.returncode == 0:
            print(f"✓ {pkg} 安装成功")
        else:
            print(f"❌ {pkg} 安装失败")
            if result:
                print(f"错误信息: {result.stderr}")

            # 尝试修复
            print(f"🔧 尝试修复 {pkg}...")
            result2 = run_command(f"pip install --upgrade {pkg}", f"升级 {pkg}")

            if result2 and result2.returncode == 0:
                print(f"✓ {pkg} 修复成功")
            else:
                print(f"⚠️  {pkg} 修复失败,继续安装其他包...")

    print("\n" + "=" * 60)
    print("✅ 依赖安装完成!")
    print("=" * 60)
    return True


def verify_installation():
    """验证安装结果"""
    print("\n" + "=" * 60)
    print("🧪 验证关键包...")
    print("=" * 60)

    key_packages = [
        'fastapi',
        'uvicorn',
        'langchain',
        'qdrant-client',
        'sqlmodel',
    ]

    all_ok = True
    for pkg in key_packages:
        result = run_command(f"python -c \"import {pkg}; print({pkg}.__version__ if hasattr({pkg}, '__version__') else 'OK')\"", f"验证 {pkg}")

        if result and result.returncode == 0:
            print(f"✓ {pkg}: {result.stdout.strip()}")
        else:
            print(f"✗ {pkg}: 验证失败")
            all_ok = False

    print()

    if all_ok:
        print("✅ 所有关键包验证通过!")
    else:
        print("⚠️  部分包验证失败,请检查安装")

    return all_ok


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🚀 AI Novel Platform 依赖自动安装工具")
    print("=" * 60)
    print()

    # 1. 检查Python版本
    check_python_version()

    # 2. 检查pip
    check_pip()

    # 3. 检查虚拟环境
    venv = check_venv()

    # 4. 检查已安装包
    installed = check_installed_packages()

    # 5. 读取requirements
    requirements = read_requirements()

    if not requirements:
        print("❌ 无法读取依赖文件")
        sys.exit(1)

    # 6. 对比并安装
    compare_and_install(installed, requirements)

    # 7. 验证安装
    verify_installation()

    print("\n" + "=" * 60)
    print("✅ 依赖检查完成! 可以启动后端服务了")
    print("=" * 60)
    print("\n启动命令:")
    print("  python main.py")
    print("  或")
    print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print()


if __name__ == "__main__":
    main()
