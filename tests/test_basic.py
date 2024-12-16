import os
import sys
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.ocr_handler import OCRHandler
from src.utils.ai_handler import AIHandler
from src.utils.file_handler import FileHandler

def test_ocr():
    """测试OCR功能"""
    print("=== 测试OCR功能 ===")
    ocr = OCRHandler()
    image_path = os.path.join("tests", "test_images", "sample.png")
    
    print(f"处理图片: {image_path}")
    text = ocr.extract_text(image_path)
    print(f"识别结果: {text}")
    return text

def test_ai(text):
    """测试AI文件名生成"""
    print("\n=== 测试AI功能 ===")
    ai = AIHandler()
    
    print(f"输入文本: {text}")
    filename = ai.generate_filename(text)
    print(f"生成文件名: {filename}")
    return filename

def test_file_handler(new_name):
    """测试文件处理"""
    print("\n=== 测试文件处理 ===")
    handler = FileHandler()
    
    print(f"清理文件名: {new_name}")
    clean_name = handler.clean_filename(new_name)
    print(f"清理结果: {clean_name}")

def main():
    print("开始功能测试...\n")
    
    # 测试OCR
    text = test_ocr()
    if not text:
        print("OCR测试失败")
        return
    
    # 测试AI
    filename = test_ai(text)
    if not filename:
        print("AI测试失败")
        return
    
    # 测试文件处理
    test_file_handler(filename)
    
    print("\n测试完成!")

if __name__ == "__main__":
    main() 