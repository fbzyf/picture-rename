from typing import Optional
import json
import os
from openai import OpenAI

class AIHandler:
    """处理AI文件名生成"""
    
    def __init__(self) -> None:
        """初始化AI处理器"""
        self.config = self._load_config()
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url=self.config['api']['base_url']
        )

    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_filename(self, text: str) -> Optional[str]:
        """
        根据文字生成文件名
        
        Args:
            text: 输入的文字内容
            
        Returns:
            生成的文件名，如果失败返回None
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config['api']['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个文件命名助手。请根据提供的文本内容，生成一个简短的、描述性的文件名（不超过50个字符）。"
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                max_tokens=50,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI处理错误: {str(e)}")
            return None 