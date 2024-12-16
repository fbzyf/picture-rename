from typing import Optional
import json
import os
import pytesseract
from PIL import Image

class OCRHandler:
    """处理图片OCR文字识别"""
    
    def __init__(self) -> None:
        """初始化OCR处理器"""
        self.config = self._load_config()
        pytesseract.pytesseract.tesseract_cmd = self.config['ocr']['tesseract_path']

    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_text(self, image_path: str) -> Optional[str]:
        """
        从图片中提取文字
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            提取的文字，如果失败返回None
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(
                image, 
                lang=self.config['ocr']['lang']
            )
            return text.strip() if text else None
        except Exception as e:
            print(f"OCR处理错误: {str(e)}")
            return None 