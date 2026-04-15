#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成安全的随机密钥
用于生产环境的SECRET_KEY配置
"""

import secrets
import sys
from pathlib import Path


def generate_secret_key(length: int = 64) -> str:
    """
    生成安全的随机密钥
    
    Args:
        length: 密钥长度(字节)
    
    Returns:
        十六进制格式的密钥字符串
    """
    return secrets.token_hex(length)


def update_env_file(env_file: Path, secret_key: str) -> bool:
    """
    更新.env文件中的SECRET_KEY
    
    Args:
        env_file: .env文件路径
        secret_key: 新的密钥
    
    Returns:
        是否更新成功
    """
    try:
        content = env_file.read_text(encoding='utf-8')
        
        # 查找SECRET_KEY行
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('SECRET_KEY='):
                # 替换密钥
                lines[i] = f'SECRET_KEY={secret_key}'
                break
        
        # 写回文件
        new_content = '\n'.join(lines)
        env_file.write_text(new_content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"错误: 更新.env文件失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("AI Novel Platform - 安全密钥生成器")
    print("=" * 60)
    print()
    
    # 生成密钥
    secret_key = generate_secret_key(64)
    
    print(f"✓ 生成的安全密钥:")
    print(f"  {secret_key}")
    print()
    print("密钥长度:", len(secret_key), "字符")
    print()
    
    # 检查.env文件
    backend_dir = Path(__file__).parent
    env_file = backend_dir / ".env"
    
    if env_file.exists():
        print(f"✓ 找到.env文件: {env_file}")
        print()
        
        # 确认更新
        print("⚠️  此操作将更新.env文件中的SECRET_KEY")
        confirm = input("是否继续? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if update_env_file(env_file, secret_key):
                print()
                print("✓ 成功更新.env文件")
                print()
                print("⚠️  请妥善保管此密钥,不要泄露或提交到版本控制系统!")
            else:
                print()
                print("✗ 更新.env文件失败")
                sys.exit(1)
        else:
            print()
            print("已取消操作")
    else:
        print(f"✗ 未找到.env文件: {env_file}")
        print()
        print("请复制.env.example为.env,然后手动添加密钥:")
        print(f"  SECRET_KEY={secret_key}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
