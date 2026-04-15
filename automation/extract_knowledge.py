#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识提取脚本 - 从文档中提取知识条目
"""

import asyncio
from pathlib import Path
from typing import List, Dict
import json


class KnowledgeExtractor:
    """知识提取器"""
    
    def __init__(self, api_base: str = "http://localhost:8000"):
        self.api_base = api_base
    
    async def extract_from_file(self, file_path: str) -> List[Dict]:
        """从文件提取知识"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 读取文件内容
        content = file_path.read_text(encoding='utf-8')
        
        # 调用RAG API提取
        # TODO: 实现API调用
        print(f"从文件提取知识: {file_path.name}")
        print(f"内容长度: {len(content)} 字符")
        
        # 模拟提取结果
        return [
            {
                "title": "示例知识1",
                "content": "从文件提取的知识内容",
                "category": "世界观",
                "tags": ["人物", "背景"]
            }
        ]
    
    async def extract_from_chapters(self, project_id: int, chapter_ids: List[int] = None) -> List[Dict]:
        """从章节提取知识"""
        print(f"从项目 {project_id} 的章节提取知识...")
        
        # TODO: 从数据库获取章节内容
        # TODO: 调用AI提取知识
        
        return []
    
    async def batch_extract(self, directory: str) -> Dict[str, List[Dict]]:
        """批量提取目录中的文件"""
        directory = Path(directory)
        
        if not directory.is_dir():
            raise ValueError(f"不是目录: {directory}")
        
        results = {}
        
        # 支持的文件类型
        supported_extensions = ['.md', '.txt', '.json']
        
        for file_path in directory.rglob('*'):
            if file_path.suffix.lower() in supported_extensions:
                try:
                    knowledge = await self.extract_from_file(str(file_path))
                    results[str(file_path)] = knowledge
                except Exception as e:
                    print(f"提取失败 {file_path}: {e}")
        
        print(f"\n批量提取完成,共处理 {len(results)} 个文件")
        
        return results


async def main():
    """主函数"""
    import sys
    
    extractor = KnowledgeExtractor()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python extract_knowledge.py <file|directory>   - 提取知识")
        print("  python extract_knowledge.py --project <id>    - 从项目提取")
        return
    
    target = sys.argv[1]
    
    if target == "--project" and len(sys.argv) > 2:
        project_id = int(sys.argv[2])
        knowledge = await extractor.extract_from_chapters(project_id)
    else:
        # 从文件或目录提取
        target_path = Path(target)
        
        if target_path.is_dir():
            results = await extractor.batch_extract(target)
            
            # 保存结果
            output_file = Path("data/extracted_knowledge.json")
            output_file.parent.mkdir(exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"\n结果已保存到: {output_file}")
        else:
            knowledge = await extractor.extract_from_file(target)
            
            for item in knowledge:
                print(f"\n- {item['title']}")
                print(f"  {item['content']}")


if __name__ == "__main__":
    asyncio.run(main())
