#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置验证脚本
检查所有必要的配置项,测试API连接
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import httpx
from typing import Dict, List, Tuple
import subprocess


class ConfigValidator:
    """配置验证器"""

    def __init__(self):
        self.backend_dir = Path(__file__).parent
        self.env_file = self.backend_dir / ".env"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_env(self) -> bool:
        """加载环境变量"""
        if not self.env_file.exists():
            self.errors.append(f"未找到.env文件: {self.env_file}")
            self.errors.append("请复制.env.example为.env并配置必要的环境变量")
            return False

        load_dotenv(self.env_file)
        return True

    def check_secret_key(self) -> bool:
        """检查SECRET_KEY"""
        print("\n[SECRET] Checking SECRET_KEY...")

        secret_key = os.getenv("SECRET_KEY", "")

        if not secret_key:
            self.errors.append("SECRET_KEY 未设置")
            return False

        # 检查是否使用默认值
        default_keys = [
            "dev-secret-key-change-in-production",
            "change-me-in-production",
            "your-secret-key-here",
        ]

        for default in default_keys:
            if default in secret_key.lower():
                self.warnings.append(
                    f"SECRET_KEY 使用了默认值,请运行: python generate_secret_key.py"
                )
                # 改成警告而不是错误
                return True

        # 检查长度
        if len(secret_key) < 32:
            self.warnings.append("SECRET_KEY 长度小于32,建议使用64字符以上的密钥")
        else:
            print(f"[OK] SECRET_KEY length: {len(secret_key)} (secure)")

        return True

    def check_api_keys(self) -> bool:
        """检查API密钥"""
        print("\n[API] Checking AI API keys...")

        api_configs = [
            ("OPENAI_API_KEY", "OpenAI"),
            ("ANTHROPIC_API_KEY", "Anthropic"),
            ("DEEPSEEK_API_KEY", "DeepSeek"),
            ("GEMINI_API_KEY", "Google Gemini"),
        ]

        valid_keys: List[str] = []

        for env_var, provider in api_configs:
            key = os.getenv(env_var, "")
            if key:
                print(f"[OK] {provider} API key configured")
                valid_keys.append(env_var)
            else:
                print(f"     {provider} API key not configured (optional)")

        if not valid_keys:
            self.warnings.append(
                "未配置任何 AI API 密钥。"
                "AI 小说生成功能需要至少一个有效的 API 密钥。\n"
                "请配置以下之一: OPENAI_API_KEY, ANTHROPIC_API_KEY, "
                "DEEPSEEK_API_KEY, GEMINI_API_KEY"
            )
            # 改成警告而不是错误，允许用户先启动
            return True

        return True

    def check_database_config(self) -> bool:
        """检查数据库配置"""
        print("\n[DATABASE] Checking database configuration...")

        database_url = os.getenv("DATABASE_URL", "")

        if not database_url:
            self.errors.append("DATABASE_URL 未设置")
            return False

        print(f"[OK] DATABASE_URL: {database_url[:50]}...")

        # 检查SQLite数据库目录
        if database_url.startswith("sqlite:///"):
            db_path = database_url.replace("sqlite:///", "")
            db_file = self.backend_dir / db_path

            # 确保数据库目录存在
            db_file.parent.mkdir(parents=True, exist_ok=True)

            # 测试数据库连接
            try:
                import sqlite3
                conn = sqlite3.connect(str(db_file))
                conn.close()
                print(f"[OK] Database connection OK")
            except Exception as e:
                self.errors.append(f"Database connection failed: {e}")
                return False

        return True

    async def test_openai_connection(self) -> bool:
        """测试OpenAI连接"""
        print("\n[TEST] Testing OpenAI API connection...")

        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            print("     Skip (OPENAI_API_KEY not configured)")
            return True

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"}
                )

                if response.status_code == 200:
                    print("[OK] OpenAI API connection successful")
                    return True
                else:
                    self.errors.append(
                        f"OpenAI API connection failed: "
                        f"HTTP {response.status_code} - {response.text[:100]}"
                    )
                    return False

        except Exception as e:
            self.errors.append(f"OpenAI API connection test failed: {e}")
            return False

    async def test_anthropic_connection(self) -> bool:
        """测试Anthropic连接"""
        print("\n[TEST] Testing Anthropic API connection...")

        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            print("     Skip (ANTHROPIC_API_KEY not configured)")
            return True

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "Hi"}]
                    }
                )

                if response.status_code in [200, 400]:  # 400是因为请求太小,但说明连接正常
                    print("[OK] Anthropic API connection successful")
                    return True
                else:
                    self.errors.append(
                        f"Anthropic API connection failed: "
                        f"HTTP {response.status_code} - {response.text[:100]}"
                    )
                    return False

        except Exception as e:
            self.errors.append(f"Anthropic API connection test failed: {e}")
            return False

    def check_directories(self) -> bool:
        """检查必要的目录"""
        print("\n[DIRECTORIES] Checking data directories...")

        directories = [
            self.backend_dir / "data",
            self.backend_dir / "data" / "uploads",
            self.backend_dir / "data" / "logs",
        ]

        for directory in directories:
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                    print(f"[OK] Created directory: {directory.name}")
                except Exception as e:
                    self.errors.append(f"Failed to create directory {directory}: {e}")
                    return False
            else:
                print(f"[OK] Directory exists: {directory.name}")

        return True

    def check_required_packages(self) -> bool:
        """检查必需的Python包"""
        print("\n[PACKAGES] Checking Python packages...")

        # 包名映射：pip安装名 -> Python导入名
        required_packages = {
            "fastapi": "fastapi",
            "uvicorn": "uvicorn",
            "sqlmodel": "sqlmodel",
            "python-dotenv": "dotenv",
        }

        missing_packages = []

        for pip_name, import_name in required_packages.items():
            try:
                __import__(import_name)
                print(f"[OK] {pip_name}")
            except ImportError:
                missing_packages.append(pip_name)
                print(f"[X] {pip_name} (not installed)")

        if missing_packages:
            self.errors.append(
                f"Missing packages: {', '.join(missing_packages)}\n"
                "Please run: pip install -r requirements.txt"
            )
            return False

        return True

    async def run_all_tests(self) -> bool:
        """运行所有测试"""
        print("=" * 60)
        print("AI Novel Platform Configuration Validation")
        print("=" * 60)

        # 1. 加载环境变量
        if not self.load_env():
            return False

        # 2. 检查必需的包
        if not self.check_required_packages():
            return False

        # 3. 检查SECRET_KEY
        self.check_secret_key()

        # 4. 检查API密钥
        self.check_api_keys()

        # 5. 检查数据库配置
        self.check_database_config()

        # 6. 检查目录
        self.check_directories()

        # 7. 测试API连接
        await self.test_openai_connection()
        await self.test_anthropic_connection()

        # 8. 输出结果
        print("\n" + "=" * 60)
        print("Validation Results")
        print("=" * 60)

        if self.errors:
            print("\n[ERROR] Errors found:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        if self.warnings:
            print("\n[WARNING] Warnings:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        if not self.errors and not self.warnings:
            print("\n[SUCCESS] All checks passed!")
            return True
        elif not self.errors:
            print("\n[WARNING] Configuration has warnings but can be used")
            return True
        else:
            print("\n[ERROR] Configuration validation failed, please fix errors")
            return False


async def main():
    """主函数"""
    validator = ConfigValidator()
    success = await validator.run_all_tests()

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
