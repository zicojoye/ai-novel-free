#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证脚本
"""

import os
from pathlib import Path


def main():
    print("=" * 60)
    print("AI Novel Platform Quick Function Verification")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    
    checks = [
        ("frontend/package.json", "Frontend dependency config"),
        ("frontend/vite.config.ts", "Frontend Vite config"),
        ("frontend/src/main.tsx", "Frontend entry"),
        ("backend/requirements.txt", "Backend dependency config"),
        ("backend/main_fixed.py", "Backend entry"),
        ("backend/app/api/projects.py", "Project API"),
        ("backend/app/api/ai_tasks.py", "AI tasks API"),
        ("backend/app/services/llm_service.py", "LLM service"),
        ("backend/app/agents/agent_manager.py", "Agent manager"),
        ("backend/app/services/cache_service.py", "Cache service"),
        ("automation/publish_to_platforms.py", "Auto publish"),
        ("automation/backup.py", "Data backup"),
        ("automation/generate_report.py", "Report generator"),
        (".env.example", "Env var template"),
        ("README.md", "Project README"),
    ]
    
    total = len(checks)
    passed = 0
    
    print("\nFile checks:")
    for filepath, desc in checks:
        full_path = project_root / filepath
        if full_path.exists():
            print(f"  [OK] {desc}")
            passed += 1
        else:
            print(f"  [FAIL] {desc}")
    
    print("\n" + "=" * 60)
    print(f"Statistics: {passed}/{total} passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n[SUCCESS] All core files exist!")
    else:
        print(f"\n[WARNING] {total-passed} files missing")
    
    print("=" * 60)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
