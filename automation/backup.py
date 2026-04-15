#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据备份脚本 - 自动备份项目数据
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import zipfile
import sys


class DataBackup:
    """数据备份管理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.data_dir = self.project_root / "data"
        self.backup_dir = self.project_root / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, backup_name: str = None) -> Path:
        """创建备份"""
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
        
        backup_path = self.backup_dir / f"{backup_name}.zip"
        
        print(f"开始备份: {backup_name}")
        
        # 创建ZIP文件
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.data_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.project_root)
                    zipf.write(file_path, arcname)
                    print(f"  已备份: {arcname}")
        
        # 添加项目配置
        config_files = [".env", "package.json", "backend/requirements.txt"]
        for config_file in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                zipf.write(config_path, config_file)
                print(f"  已备份: {config_file}")
        
        size_mb = backup_path.stat().st_size / (1024 * 1024)
        print(f"\n备份完成: {backup_path}")
        print(f"文件大小: {size_mb:.2f} MB")
        
        return backup_path
    
    def restore_backup(self, backup_path: str):
        """恢复备份"""
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            raise FileNotFoundError(f"备份文件不存在: {backup_path}")
        
        print(f"开始恢复: {backup_path}")
        
        # 备份当前数据
        current_backup = self.create_backup("before_restore")
        print(f"当前数据已备份到: {current_backup}")
        
        # 解压备份
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(self.project_root)
            print(f"\n已恢复文件:")
            for name in zipf.namelist():
                print(f"  {name}")
        
        print(f"\n恢复完成!")
    
    def list_backups(self) -> list:
        """列出所有备份"""
        backups = []
        
        for backup_file in self.backup_dir.glob("*.zip"):
            stat = backup_file.stat()
            size_mb = stat.st_size / (1024 * 1024)
            backups.append({
                "name": backup_file.stem,
                "path": str(backup_file),
                "size_mb": round(size_mb, 2),
                "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return sorted(backups, key=lambda x: x["created"], reverse=True)
    
    def clean_old_backups(self, keep_count: int = 10):
        """清理旧备份,保留最新的N个"""
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            print(f"备份数量({len(backups)})未超过保留数量({keep_count})")
            return
        
        # 删除旧备份
        for backup in backups[keep_count:]:
            backup_path = Path(backup["path"])
            backup_path.unlink()
            print(f"已删除: {backup['name']}")
        
        print(f"\n清理完成,保留最新的 {keep_count} 个备份")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python backup.py create [name]    - 创建备份")
        print("  python backup.py restore <path>   - 恢复备份")
        print("  python backup.py list             - 列出备份")
        print("  python backup.py clean [count]    - 清理旧备份")
        return
    
    command = sys.argv[1]
    backup_manager = DataBackup()
    
    if command == "create":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        backup_manager.create_backup(name)
    
    elif command == "restore":
        if len(sys.argv) < 3:
            print("请指定备份路径")
            return
        backup_manager.restore_backup(sys.argv[2])
    
    elif command == "list":
        backups = backup_manager.list_backups()
        print(f"\n备份列表 ({len(backups)} 个):\n")
        print(f"{'名称':<30} {'大小(MB)':<10} {'创建时间'}")
        print("-" * 60)
        for backup in backups:
            print(f"{backup['name']:<30} {backup['size_mb']:<10.2f} {backup['created']}")
    
    elif command == "clean":
        keep_count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        backup_manager.clean_old_backups(keep_count)
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
