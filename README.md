# 丰宝智能图片重命名工具

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

基于 OCR 和 AI 的智能图片批量重命名工具，可以自动识别图片内容并生成合适的文件名。

## ✨ 功能特点

- 🖼️ 支持多种图片格式 (PNG, JPG, JPEG)
- 🔍 使用 Tesseract OCR 技术自动识别图片内容
- 🤖 集成 DeepSeek AI 模型生成智能文件名
- 🎯 简单直观的用户界面
- 🎨 现代化的界面设计
- ✨ 实时预览重命名结果
- ⚡ 批量处理功能

## 📥 下载和安装

### 方法一：直接使用（推荐）

1. 从 [Releases](../../releases) 页面下载最新版本的 `丰宝智能图片重命名.zip`
2. 解压到任意目录
3. 按照下方的"必需步骤"进行配置

### 方法二：从源码构建

1. 克隆仓库：
   ```bash
   git clone https://github.com/[your-username]/picture-rename.git
   cd picture-rename
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行构建脚本：
   ```bash
   python build.py
   ```

### 必需步骤

1. 安装 Tesseract OCR
   - 访问：https://github.com/UB-Mannheim/tesseract/wiki
   - 下载 Windows 版本（64位）
   - 运行安装程序，注意：
     * 安装路径选择默认的 `C:\Program Files\Tesseract-OCR`
     * 必须勾选"添加到系统路径"选项
     * 在语言包选项中勾选"Chinese (Simplified)"

## 🚀 使用方法

1. 运行程序
   - 双击"启动程序.bat"（推荐）
   - 或直接运行"丰宝智能图片重命名.exe"

2. 使用步骤
   - 点击"选择图片"按钮，选择要重命名的图片
   - 点击"开始处理"按钮，等待处理完成
   - 在列表中查看生成的新文件名
   - 确认无误后，点击"应用更改"执行重命名

## 💡 使用建议

1. 首次使用时：
   - 建议先用1-2张图片测试
   - 确保图片中的文字清晰可见
   - 检查重命名结果是否符合预期

2. 批量处理时：
   - 建议每次处理不超过20张图片
   - 处理前建议备份重要文件
   - 确保网络连接稳定

## ❓ 常见问题解决

1. 程序无法启动
   - 检查是否已正确安装 Tesseract OCR
   - 确认是否使用"启动程序.bat"运行
   - 尝试以管理员身份运行

2. OCR识别失败
   - 确保图片文字清晰、无变形
   - 检查图片格式是否支持（支持 PNG、JPG、JPEG）
   - 验证网络连接是否正常

3. 重命名失败
   - 检查文件是否被其他程序占用
   - 确认是否有文件写入权限
   - 检查新文件名是否含有特殊字符

## 🔧 技术栈

- Python 3.8+
- PyQt5 - GUI 框架
- Tesseract - OCR 引擎
- DeepSeek API - AI 文本生成
- Pillow - 图像处理

## 📞 技术支持

如遇到问题，请：
1. 查看 [常见问题](../../wiki/FAQ) 页面
2. 提交 [Issue](../../issues)
3. 联系技术支持：
   - 邮箱：[技术支持邮箱]
   - 电话：[技术支持电话]

## 📝 版本信息

- 版本号：1.0.0
- 发布日期：2024-03-20
- 支持系统：Windows 10/11

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

欢迎提交 Pull Request 或 Issue！详见 [贡献指南](CONTRIBUTING.md)。

## 👥 作者

丰宝科技