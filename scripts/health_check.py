#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康检查脚本
检查后端和前端服务是否正常运行
"""

import requests
import sys
from typing import Dict, List
import time


class HealthChecker:
    """健康检查器"""

    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.results: List[Dict] = []

    def check_backend(self) -> bool:
        """检查后端服务"""
        print("\n🔍 检查后端服务...")

        try:
            # 检查健康接口
            response = requests.get(
                f"{self.backend_url}/health",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✓ 后端服务正常")
                print(f"  状态: {data.get('status', 'unknown')}")

                self.results.append({
                    "service": "backend",
                    "status": "healthy",
                    "url": self.backend_url,
                    "response_time": response.elapsed.total_seconds()
                })
                return True
            else:
                print(f"✗ 后端服务异常: HTTP {response.status_code}")
                self.results.append({
                    "service": "backend",
                    "status": "error",
                    "error": f"HTTP {response.status_code}"
                })
                return False

        except requests.exceptions.ConnectionError:
            print("✗ 无法连接到后端服务")
            self.results.append({
                "service": "backend",
                "status": "error",
                "error": "Connection refused"
            })
            return False
        except Exception as e:
            print(f"✗ 后端检查失败: {e}")
            self.results.append({
                "service": "backend",
                "status": "error",
                "error": str(e)
            })
            return False

    def check_frontend(self) -> bool:
        """检查前端服务"""
        print("\n🔍 检查前端服务...")

        try:
            response = requests.get(
                self.frontend_url,
                timeout=5
            )

            if response.status_code == 200:
                print(f"✓ 前端服务正常")
                print(f"  URL: {self.frontend_url}")

                self.results.append({
                    "service": "frontend",
                    "status": "healthy",
                    "url": self.frontend_url,
                    "response_time": response.elapsed.total_seconds()
                })
                return True
            else:
                print(f"✗ 前端服务异常: HTTP {response.status_code}")
                self.results.append({
                    "service": "frontend",
                    "status": "error",
                    "error": f"HTTP {response.status_code}"
                })
                return False

        except requests.exceptions.ConnectionError:
            print("✗ 无法连接到前端服务")
            self.results.append({
                "service": "frontend",
                "status": "error",
                "error": "Connection refused"
            })
            return False
        except Exception as e:
            print(f"✗ 前端检查失败: {e}")
            self.results.append({
                "service": "frontend",
                "status": "error",
                "error": str(e)
            })
            return False

    def check_api_docs(self) -> bool:
        """检查API文档"""
        print("\n🔍 检查API文档...")

        try:
            response = requests.get(
                f"{self.backend_url}/docs",
                timeout=5
            )

            if response.status_code == 200:
                print(f"✓ API文档可访问")
                print(f"  URL: {self.backend_url}/docs")

                self.results.append({
                    "service": "api_docs",
                    "status": "healthy",
                    "url": f"{self.backend_url}/docs"
                })
                return True
            else:
                print(f"✗ API文档异常: HTTP {response.status_code}")
                self.results.append({
                    "service": "api_docs",
                    "status": "error",
                    "error": f"HTTP {response.status_code}"
                })
                return False

        except Exception as e:
            print(f"✗ API文档检查失败: {e}")
            self.results.append({
                "service": "api_docs",
                "status": "error",
                "error": str(e)
            })
            return False

    def print_summary(self):
        """打印摘要"""
        print("\n" + "=" * 60)
        print("📊 健康检查摘要")
        print("=" * 60)

        healthy_count = sum(1 for r in self.results if r["status"] == "healthy")
        total_count = len(self.results)

        print(f"\n总体状态: {healthy_count}/{total_count} 服务正常")
        print()

        for result in self.results:
            icon = "✓" if result["status"] == "healthy" else "✗"
            print(f"{icon} {result['service']}: {result['status']}")

            if result["status"] == "error":
                print(f"  错误: {result.get('error', 'unknown')}")

        print()

        if healthy_count == total_count:
            print("✅ 所有服务运行正常!")
            return 0
        else:
            print("⚠️  部分服务异常,请检查日志")
            return 1

    def run(self) -> int:
        """运行健康检查"""
        print("=" * 60)
        print("AI Novel Platform - 健康检查")
        print("=" * 60)

        # 检查各项服务
        self.check_backend()
        self.check_frontend()
        self.check_api_docs()

        # 打印摘要
        return self.print_summary()


def main():
    """主函数"""
    checker = HealthChecker()
    exit_code = checker.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
