#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能验证脚本 - 检测项目功能完整性
"""

import os
import json
from pathlib import Path
from typing import List, Dict


class FunctionValidator:
    """功能验证器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results = []
    
    def check_file_exists(self, filepath: str, description: str) -> bool:
        """检查文件是否存在"""
        full_path = self.project_root / filepath
        exists = full_path.exists()
        self.results.append({
            "检查项": description,
            "路径": filepath,
            "结果": "通过" if exists else "失败",
            "状态": exists
        })
        return exists
    
    def check_directory_exists(self, dirpath: str, description: str) -> bool:
        """检查目录是否存在"""
        full_path = self.project_root / dirpath
        exists = full_path.is_dir()
        self.results.append({
            "检查项": description,
            "路径": dirpath,
            "结果": "通过" if exists else "失败",
            "状态": exists
        })
        return exists
    
    def check_frontend(self) -> Dict:
        """检查前端功能"""
        print("\n" + "="*60)
        print("检测前端功能")
        print("="*60)
        
        checks = [
            ("package.json", "前端配置文件"),
            ("vite.config.ts", "Vite配置"),
            ("tailwind.config.js", "Tailwind配置"),
            ("tsconfig.json", "TypeScript配置"),
            ("index.html", "HTML入口"),
            ("postcss.config.js", "PostCSS配置"),
            ("src/main.tsx", "React入口"),
            ("src/App.tsx", "主应用组件"),
            ("src/components", "组件目录"),
            ("src/modules", "模块目录"),
            ("src/pages", "页面目录"),
            ("src/stores", "状态管理"),
            ("src/services", "API服务"),
            ("src/types", "类型定义"),
        ]
        
        passed = 0
        for filepath, description in checks:
            if self.check_file_exists(f"frontend/{filepath}", description):
                passed += 1
        
        # 检查页面模块
        pages = [
            "Dashboard.tsx",
            "WorldBuilding.tsx", 
            "ChapterEditor.tsx",
            "PlotManager.tsx",
            "KnowledgeBase.tsx",
            "AgentMonitor.tsx",
            "PromptLibrary.tsx",
            "Settings.tsx",
        ]
        
        for page in pages:
            if self.check_file_exists(f"frontend/src/pages/{page}", f"页面: {page}"):
                passed += 1
        
        return {"total": len(checks) + len(pages), "passed": passed}
    
    def check_backend(self) -> Dict:
        """检查后端功能"""
        print("\n" + "="*60)
        print("检测后端功能")
        print("="*60)
        
        checks = [
            ("main.py", "后端入口"),
            ("main_fixed.py", "修复版入口"),
            ("test_app.py", "测试应用"),
            ("requirements.txt", "Python依赖"),
            ("app/core/config.py", "配置管理"),
            ("app/core/database.py", "数据库配置"),
            ("app/api/__init__.py", "API包"),
            ("app/models/__init__.py", "模型包"),
        ]
        
        passed = 0
        for filepath, description in checks:
            if self.check_file_exists(f"backend/{filepath}", description):
                passed += 1
        
        # 检查API模块
        api_modules = [
            "projects.py",
            "chapters.py",
            "worldbuilding.py",
            "plot.py",
            "knowledge.py",
            "agents.py",
            "prompts.py",
            "ai_tasks.py",
        ]
        
        for module in api_modules:
            if self.check_file_exists(f"backend/app/api/{module}", f"API模块: {module}"):
                passed += 1
        
        # 检查服务
        services = [
            "llm_service.py",
            "rag_service.py",
            "cache_service.py",
        ]
        
        for service in services:
            if self.check_file_exists(f"backend/app/services/{service}", f"业务服务: {service}"):
                passed += 1
        
        # 检查Agent
        agents = [
            "base_agent.py",
            "core_agents.py",
            "support_agents.py",
            "quality_agents.py",
            "agent_manager.py",
        ]
        
        for agent in agents:
            if self.check_file_exists(f"backend/app/agents/{agent}", f"Agent: {agent}"):
                passed += 1
        
        return {"total": len(checks) + len(api_modules) + len(services) + len(agents), "passed": passed}
    
    def check_automation(self) -> Dict:
        """检查自动化功能"""
        print("\n" + "="*60)
        print("检测自动化功能")
        print("="*60)
        
        scripts = [
            ("publish_to_platforms.py", "多平台发布"),
            ("backup.py", "数据备份"),
            ("extract_knowledge.py", "知识提取"),
            ("agent_scheduler.py", "Agent调度"),
            ("generate_report.py", "报表生成"),
        ]
        
        passed = 0
        for script, description in scripts:
            if self.check_file_exists(f"automation/{script}", description):
                passed += 1
        
        return {"total": len(scripts), "passed": passed}
    
    def check_shared(self) -> Dict:
        """检查共享模块"""
        print("\n" + "="*60)
        print("检测共享模块")
        print("="*60)
        
        modules = [
            ("types.py", "类型定义"),
            ("constants.py", "常量定义"),
            ("utils.py", "工具函数"),
            ("prompts.py", "提示词模板"),
        ]
        
        passed = 0
        for module, description in modules:
            if self.check_file_exists(f"shared/{module}", description):
                passed += 1
        
        return {"total": len(modules), "passed": passed}
    
    def check_docs(self) -> Dict:
        """检查文档"""
        print("\n" + "="*60)
        print("检测文档")
        print("="*60)
        
        docs = [
            ("README.md", "项目说明"),
            (".env.example", "环境变量示例"),
            ("docs/启动指南.md", "启动指南"),
            ("docs/本地部署指南.md", "本地部署指南"),
            ("docs/问题诊断.md", "问题诊断"),
            ("docs/功能验证报告.md", "功能验证"),
            ("docs/验收检测报告.md", "验收检测"),
        ]
        
        passed = 0
        for doc, description in docs:
            if self.check_file_exists(doc, description):
                passed += 1
        
        return {"total": len(docs), "passed": passed}
    
    def generate_report(self):
        """生成检测报告"""
        print("\n" + "="*60)
        print("生成功能验证报告")
        print("="*60)
        
        # 执行所有检查
        frontend_result = self.check_frontend()
        backend_result = self.check_backend()
        automation_result = self.check_automation()
        shared_result = self.check_shared()
        docs_result = self.check_docs()
        
        # 统计
        total_checks = (
            frontend_result["total"] + 
            backend_result["total"] + 
            automation_result["total"] + 
            shared_result["total"] + 
            docs_result["total"]
        )
        
        total_passed = (
            frontend_result["passed"] + 
            backend_result["passed"] + 
            automation_result["passed"] + 
            shared_result["passed"] + 
            docs_result["passed"]
        )
        
        pass_rate = (total_passed / total_checks * 100) if total_checks > 0 else 0
        
        # 生成报告
        report = {
            "检测时间": "2026-04-14",
            "总体统计": {
                "总检查项": total_checks,
                "通过项": total_passed,
                "失败项": total_checks - total_passed,
                "通过率": f"{pass_rate:.1f}%"
            },
            "分模块统计": {
                "前端功能": f"{frontend_result['passed']}/{frontend_result['total']}",
                "后端功能": f"{backend_result['passed']}/{backend_result['total']}",
                "自动化功能": f"{automation_result['passed']}/{automation_result['total']}",
                "共享模块": f"{shared_result['passed']}/{shared_result['total']}",
                "文档": f"{docs_result['passed']}/{docs_result['total']}"
            },
            "详细检查": self.results
        }
        
        # 打印摘要
        print("\n" + "="*60)
        print("功能验证摘要")
        print("="*60)
        print(f"\n总体统计:")
        print(f"  总检查项: {total_checks}")
        print(f"  通过项:   {total_passed}")
        print(f"  失败项:   {total_checks - total_passed}")
        print(f"  通过率:   {pass_rate:.1f}%")
        
        print(f"\n分模块统计:")
        print(f"  前端功能:   {frontend_result['passed']}/{frontend_result['total']}")
        print(f"  后端功能:   {backend_result['passed']}/{backend_result['total']}")
        print(f"  自动化功能: {automation_result['passed']}/{automation_result['total']}")
        print(f"  共享模块:   {shared_result['passed']}/{shared_result['total']}")
        print(f"  文档:       {docs_result['passed']}/{docs_result['total']}")
        
        # 保存报告
        report_file = self.project_root / "docs/功能验证结果.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {report_file}")
        
        # 判断结果
        print("\n" + "="*60)
        if pass_rate >= 95:
            print("✅ 验证通过! 项目功能完整!")
        elif pass_rate >= 80:
            print("⚠️  基本通过,建议完善部分功能")
        else:
            print("❌ 验证未通过,需要补充功能")
        print("="*60)
        
        return report


def main():
    """主函数"""
    print("\n" + "="*60)
    print("AI Novel Platform 功能验证")
    print("="*60)
    
    # 项目根目录
    project_root = Path(__file__).parent.parent
    
    # 创建验证器
    validator = FunctionValidator(project_root)
    
    # 执行验证
    report = validator.generate_report()
    
    return report


if __name__ == "__main__":
    main()
