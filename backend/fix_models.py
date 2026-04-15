#!/usr/bin/env python3
"""
修复模型文件中的类型错误
将所有 Base 类中的 Optional[dict], Optional[list], Optional[List[...]], Optional[Dict[...]]
改为 Optional[str]（在API层处理JSON）
"""

import os
import re
from pathlib import Path

models_dir = Path(__file__).parent / "app" / "models"

def fix_model_file(file_path: Path):
    """修复单个模型文件"""
    content = file_path.read_text(encoding='utf-8')
    original = content

    # 在 Base 类中，将 Optional[dict] 改为 Optional[str]
    content = re.sub(
        r'(class \w+Base\(SQLModel\):.*?)(.*?)(class \w+\(.*?table=True)',
        lambda m: fix_base_class(m.group(1)) + m.group(2),
        content,
        flags=re.DOTALL
    )

    if content != original:
        file_path.write_text(content, encoding='utf-8')
        print(f"Fixed: {file_path.name}")
        return True
    return False

def fix_base_class(class_content: str) -> str:
    """修复Base类中的字段定义"""
    # 匹配所有 Optional[dict/list/List/Dict] 字段定义
    lines = class_content.split('\n')
    fixed_lines = []

    in_base_class = False
    indent = ""

    for line in lines:
        # 检测是否进入Base类
        if 'Base(SQLModel):' in line:
            in_base_class = True
            fixed_lines.append(line)
            continue

        # 检测是否退出Base类（遇到下一个类定义）
        if in_base_class and re.match(r'^\s*class ', line) and 'Base' not in line:
            in_base_class = False
            fixed_lines.append(line)
            continue

        # 只在Base类中修复
        if not in_base_class:
            fixed_lines.append(line)
            continue

        # 修复字段定义
        if re.search(r'Optional\[(?:List\[|Dict\[|list|dict)', line):
            # 将 Optional[dict] 改为 Optional[str]
            line = re.sub(r'Optional\[list\]', 'Optional[str]', line)
            line = re.sub(r'Optional\[dict\]', 'Optional[str]', line)
            line = re.sub(r'Optional\[List\[str\]\]', 'Optional[str]', line)
            line = re.sub(r'Optional\[List\[int\]\]', 'Optional[str]', line)
            line = re.sub(r'Optional\[List\[dict\]\]', 'Optional[str]', line)
            line = re.sub(r'Optional\[Dict\[str, Any\]\]', 'Optional[str]', line)
            line = re.sub(r'List\[int\]', 'str', line)
            line = re.sub(r'List\[dict\]', 'str', line)

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def main():
    """主函数"""
    print("Fixing model type errors...")
    print()

    files_to_fix = [
        "agent.py",
        "chat.py",
        "knowledge.py",
        "memory.py",
        "prompt.py",
        "worldbuilding.py",
        "plot.py",
    ]

    fixed_count = 0
    for filename in files_to_fix:
        file_path = models_dir / filename
        if file_path.exists():
            if fix_model_file(file_path):
                fixed_count += 1

    print()
    print(f"Fixed {fixed_count} files")
    print("Done!")

if __name__ == "__main__":
    main()
