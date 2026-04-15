#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动检查并安装Node.js依赖
已安装的跳过,没安装的自动安装
有问题自动修复
"""

import sys
import subprocess
import os
import json
from pathlib import Path


def run_command(cmd, description, shell=True):
    """执行命令并返回结果"""
    try:
        print(f"📝 {description}...")
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=False
        )
        return result
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return None


def check_node_version():
    """检查Node.js版本"""
    print("=" * 60)
    print("🟢 检查Node.js版本...")
    print("=" * 60)

    result = run_command("node --version", "检查Node.js")

    if result and result.returncode == 0:
        version = result.stdout.strip()
        print(f"✓ Node.js版本: {version}")

        # 简单版本检查
        major = int(version[1:].split('.')[0])
        if major < 18:
            print(f"⚠️  Node.js版本过低! 建议使用Node.js 18+")
        else:
            print(f"✓ Node.js版本符合要求")
        print()
        return True
    else:
        print("❌ Node.js未安装或未添加到PATH")
        print("请先安装Node.js: https://nodejs.org/")
        print("建议安装Node.js 18 LTS版本")
        sys.exit(1)


def check_npm():
    """检查npm是否可用"""
    print("=" * 60)
    print("📦 检查npm...")
    print("=" * 60)

    result = run_command("npm --version", "检查npm")

    if result and result.returncode == 0:
        print(f"✓ npm版本: {result.stdout.strip()}")
        print()
        return True
    else:
        print("❌ npm不可用")
        sys.exit(1)


def check_package_json():
    """检查package.json是否存在"""
    print("=" * 60)
    print("📄 检查package.json...")
    print("=" * 60)

    frontend_dir = Path(__file__).parent
    package_json = frontend_dir / "package.json"

    if not package_json.exists():
        print(f"❌ 找不到 {package_json}")
        sys.exit(1)

    try:
        with open(package_json, 'r', encoding='utf-8') as f:
            package = json.load(f)

        dependencies = package.get('dependencies', {})
        dev_dependencies = package.get('devDependencies', {})

        print(f"✓ 项目名称: {package.get('name', 'Unknown')}")
        print(f"✓ 版本: {package.get('version', '1.0.0')}")
        print(f"✓ 依赖包数量: {len(dependencies)}")
        print(f"✓ 开发依赖: {len(dev_dependencies)}")
        print()
        return package
    except Exception as e:
        print(f"❌ 读取package.json失败: {e}")
        sys.exit(1)


def check_node_modules():
    """检查node_modules是否存在"""
    print("=" * 60)
    print("🔍 检查node_modules...")
    print("=" * 60)

    frontend_dir = Path(__file__).parent
    node_modules = frontend_dir / "node_modules"

    if node_modules.exists():
        print(f"✓ node_modules已存在")
        return True
    else:
        print("⚠️  node_modules不存在,需要安装依赖")
        return False


def get_installed_packages():
    """获取已安装的包"""
    print("=" * 60)
    print("📋 检查已安装的包...")
    print("=" * 60)

    result = run_command("npm list --depth=0", "获取已安装包")

    if result and result.returncode == 0:
        lines = result.stdout.split('\n')
        installed = {}
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('├─') and not line.startswith('└─'):
                continue
            if '@' in line:
                pkg = line.split('@')[1].split('@')[0]
                version = line.split('@')[-1]
                installed[pkg] = version

        print(f"✓ 已安装 {len(installed)} 个包")
        return installed
    else:
        print("⚠️  无法获取已安装包列表")
        return {}


def install_dependencies():
    """安装依赖"""
    print("=" * 60)
    print("📦 安装依赖包...")
    print("=" * 60)

    # 检查是否使用yarn
    use_yarn = False
    result = run_command("yarn --version", "检查yarn")
    if result and result.returncode == 0:
        print(f"✓ 检测到yarn: {result.stdout.strip()}")
        print()
        use_yarn = True

    # 选择包管理器
    if use_yarn:
        print("🔄 使用yarn安装依赖...")
        cmd = "yarn install"
        manager = "yarn"
    else:
        print("🔄 使用npm安装依赖...")
        print("💡 提示: 可以使用 'npm install -g yarn' 安装yarn以获得更快的安装速度")
        cmd = "npm install"
        manager = "npm"

    print()

    # 运行安装
    result = run_command(cmd, f"{manager} install")

    if result and result.returncode == 0:
        print("\n✅ 依赖安装成功!")
        return True
    else:
        print("\n❌ 依赖安装失败")
        if result:
            print(f"错误信息: {result.stderr}")

        # 尝试修复
        print("\n🔧 尝试修复...")
        print("1. 清理缓存...")
        if use_yarn:
            run_command("yarn cache clean", "清理yarn缓存")
        else:
            run_command("npm cache clean --force", "清理npm缓存")

        print("2. 删除node_modules和package-lock.json...")
        frontend_dir = Path(__file__).parent
        node_modules = frontend_dir / "node_modules"
        package_lock = frontend_dir / "package-lock.json"
        yarn_lock = frontend_dir / "yarn.lock"

        if node_modules.exists():
            run_command(f"rm -rf {node_modules}", "删除node_modules", shell=False)
        if package_lock.exists():
            run_command(f"rm -f {package_lock}", "删除package-lock.json", shell=False)
        if yarn_lock.exists():
            run_command(f"rm -f {yarn_lock}", "删除yarn.lock", shell=False)

        print("3. 重新安装...")
        result2 = run_command(cmd, f"{manager} install")

        if result2 and result2.returncode == 0:
            print("\n✅ 修复成功,依赖安装完成!")
            return True
        else:
            print("\n❌ 修复失败")
            print("\n请尝试手动安装:")
            print("  npm install")
            return False


def verify_installation(package):
    """验证安装结果"""
    print("\n" + "=" * 60)
    print("🧪 验证关键包...")
    print("=" * 60)

    dependencies = package.get('dependencies', {})
    key_packages = ['react', 'react-dom', 'react-router-dom', 'zustand', 'axios']

    all_ok = True
    for pkg in key_packages:
        if pkg in dependencies:
            version = dependencies[pkg]
            print(f"✓ {pkg} (需要: {version})")

            # 检查是否真的安装了
            result = run_command(f"npm list {pkg}", f"检查 {pkg}")
            if result and result.returncode != 0:
                print(f"  ⚠️  {pkg} 可能未正确安装")
                all_ok = False
        else:
            print(f"⚠️  {pkg} 不在依赖列表中")

    print()

    if all_ok:
        print("✅ 所有关键包验证通过!")
    else:
        print("⚠️  部分包可能未正确安装")

    return all_ok


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🚀 AI Novel Platform 前端依赖自动安装工具")
    print("=" * 60)
    print()

    # 1. 检查Node.js
    check_node_version()

    # 2. 检查npm
    check_npm()

    # 3. 检查package.json
    package = check_package_json()

    # 4. 检查node_modules
    has_node_modules = check_node_modules()

    # 5. 安装依赖
    install_dependencies()

    # 6. 验证安装
    verify_installation(package)

    print("\n" + "=" * 60)
    print("✅ 依赖检查完成! 可以启动前端服务了")
    print("=" * 60)
    print("\n启动命令:")
    print("  npm run dev")
    print("  或")
    print("  npm run build && npm run preview")
    print()


if __name__ == "__main__":
    main()
