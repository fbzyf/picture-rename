from typing import Optional

class OCRHandler:
    tesseract_cmd: str
    def __init__(self) -> None: ...
    def extract_text(self, image_path: str) -> Optional[str]: ... 