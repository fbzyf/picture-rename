import os
import re
import json
from typing import Optional

class FileHandler:
    """处理文件重命名操作"""
    
    def __init__(self) -> None:
        """初始化文件处理器"""
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def clean_filename(self, filename: str) -> str:
        """
        清理并规范化文件名
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        # 移除非法字符
        pattern = f'[{"".join(self.config["file"]["illegal_chars"])}]'
        filename = re.sub(pattern, '', filename)
        # 替换多个空格为单个下划线
        filename = re.sub(r'\s+', '_', filename)
        # 限制长度
        return filename[:self.config["file"]["max_length"]]

    def rename_file(self, original_path: str, new_name: str) -> bool:
        """
        重命名文件
        
        Args:
            original_path: 原始文件路径
            new_name: 新文件名（不含扩展名）
            
        Returns:
            是否重命名成功
        """
        try:
            directory = os.path.dirname(original_path)
            extension = os.path.splitext(original_path)[1]
            new_path = os.path.join(directory, new_name + extension)
            
            # 处理文件名冲突
            counter = 1
            while os.path.exists(new_path):
                new_path = os.path.join(directory, f"{new_name}_{counter}{extension}")
                counter += 1
            
            os.rename(original_path, new_path)
            return True
        except Exception as e:
            print(f"重命名失败: {str(e)}")
            return False 