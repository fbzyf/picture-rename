import os
import sys
from typing import Dict, List, Optional, Sequence, Any, NoReturn

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog,
                         QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, 
                         QLabel, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QBrush
from PyQt5.QtSvg import QSvgWidget

from src.utils.ocr_handler import OCRHandler
from src.utils.ai_handler import AIHandler
from src.utils.file_handler import FileHandler

class ImageProcessor(QThread):
    progress = pyqtSignal(str, str, str)  # original_path, new_name, status
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, file_paths: List[str]) -> None:
        super().__init__()
        self.file_paths = file_paths
        self.ocr = OCRHandler()
        self.ai = AIHandler()
        self.file_handler = FileHandler()

    def run(self) -> None:
        for path in self.file_paths:
            try:
                # OCR识别
                text = self.ocr.extract_text(path)
                if not text:
                    self.progress.emit(path, "", "OCR识别失败")
                    continue

                # AI生成文件名
                new_name = self.ai.generate_filename(text)
                if not new_name:
                    self.progress.emit(path, "", "AI生成文件名失败")
                    continue

                # 清理文件名
                new_name = self.file_handler.clean_filename(new_name)
                self.progress.emit(path, new_name, "成功")

            except Exception as e:
                self.error.emit(f"处理文件 {path} 时出错: {str(e)}")

        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("丰宝智能图片重命名")
        self.setMinimumSize(1000, 700)
        
        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QPushButton {
                background-color: #003C97;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0050C9;
            }
            QPushButton:disabled {
                background-color: #999999;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QLabel {
                color: #1d1d1f;
                font-size: 14px;
            }
        """)
        
        # 加载图标
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 添加类型注解
        self.selected_files: List[str] = []
        self.processed_files: Dict[str, str] = {}  # {original_path: new_name}
        self.is_processing: bool = False
        self.init_ui()

    def init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 添加Logo
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        logo_widget = QSvgWidget(os.path.join(os.path.dirname(__file__), "assets", "logo.svg"))
        logo_widget.setFixedSize(200, 100)
        
        title_label = QLabel("丰宝智能图片重命名")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0; color: #1d1d1f;")
        
        logo_layout.addWidget(logo_widget)
        logo_layout.addWidget(title_label)
        main_layout.addWidget(logo_container)

        # 按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)

        # 选择文件按钮
        self.select_btn = QPushButton("选择图片")
        self.select_btn.setFixedWidth(200)
        button_layout.addWidget(self.select_btn)
        self.select_btn.clicked.connect(self.select_files)

        # 处理按钮
        self.process_btn = QPushButton("开始处理")
        self.process_btn.setFixedWidth(200)
        self.process_btn.clicked.connect(self.process_and_apply)
        self.process_btn.setEnabled(False)
        button_layout.addWidget(self.process_btn)

        button_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(button_container)

        # 文件列表
        list_container = QFrame()
        list_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        list_layout = QVBoxLayout(list_container)
        
        list_title = QLabel("文件列表")
        list_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        list_layout.addWidget(list_title)
        
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px 0;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        list_layout.addWidget(self.file_list)
        
        main_layout.addWidget(list_container)

        # 状态标签
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                padding: 10px;
                font-size: 13px;
            }
        """)
        main_layout.addWidget(self.status_label)

    def process_and_apply(self) -> None:
        if not self.is_processing:
            # 开始处理
            self.is_processing = True
            self.process_btn.setText("处理中...")
            self.process_btn.setEnabled(False)
            self.select_btn.setEnabled(False)
            self.file_list.clear()
            self.processed_files.clear()

            self.processor = ImageProcessor(self.selected_files)
            self.processor.progress.connect(self.handle_processed_file)
            self.processor.finished.connect(self.handle_process_finished)
            self.processor.error.connect(self.handle_error)
            self.processor.start()

            self.status_label.setText("正在处理...")
        else:
            # 应用更改
            success_count = 0
            fail_count = 0
            file_handler = FileHandler()

            for original_path, new_name in self.processed_files.items():
                try:
                    if file_handler.rename_file(original_path, new_name):
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception as e:
                    print(f"重命名失败: {str(e)}")
                    fail_count += 1

            self.status_label.setText(f"重命名完成: {success_count}成功, {fail_count}失败")
            self.process_btn.setEnabled(False)
            self.select_btn.setEnabled(True)
            self.is_processing = False

    def handle_processed_file(self, original_path: str, new_name: str, status: str) -> None:
        if status == "成功":
            self.processed_files[original_path] = new_name
            item = QListWidgetItem(f"{os.path.basename(original_path)} → {new_name}")
            item.setForeground(QBrush(QColor(0, 128, 0)))  # 深绿色
        else:
            item = QListWidgetItem(f"{os.path.basename(original_path)}: {status}")
            item.setForeground(QBrush(QColor(255, 0, 0)))  # 红色
        self.file_list.addItem(item)

    def handle_process_finished(self) -> None:
        self.status_label.setText("处理完成，点击按钮应用更改")
        self.select_btn.setEnabled(False)
        self.process_btn.setEnabled(True)
        self.process_btn.setText("应用更改")

    def handle_error(self, error_msg: str) -> None:
        self.status_label.setText(error_msg)

    def select_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择图片文件",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.svg)"
        )
        if files:
            self.selected_files = files
            self.file_list.clear()
            for f in files:
                self.file_list.addItem(os.path.basename(f))
            self.process_btn.setEnabled(True)
            self.process_btn.setText("开始处理")
            self.is_processing = False
            self.status_label.setText(f"已选择 {len(files)} 个文件")

def main() -> NoReturn:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 