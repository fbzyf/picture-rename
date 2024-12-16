import PyInstaller.__main__
import os
import shutil
from typing import NoReturn

def build() -> NoReturn:
    # 清理之前的构建
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
        
    # 打包参数
    params = [
        'run.py',  # 入口脚本
        '--name=丰宝智能图片重命名',  # 程序名称
        '--noconsole',  # 不显示控制台
        '--add-data=src/assets;assets',  # 添加资源文件
        '--add-data=src/config.json;.',  # 添加配置文件
        '--onefile',  # 打包成单个文件
        '--clean',  # 清理临时文件
        '--windowed'  # Windows下不显示控制台
    ]
    
    # 执行打包
    PyInstaller.__main__.run(params)
    
    # 创建发布包目录
    dist_dir = 'dist/丰宝智能图片重命名'
    os.makedirs(dist_dir, exist_ok=True)
    
    # 移动可执行文件
    shutil.move('dist/丰宝智能图片重命名.exe', f'{dist_dir}/丰宝智能图片重命名.exe')
    
    # 复制必要文件
    shutil.copy('README.md', f'{dist_dir}/使用说明.txt')
    
    # 创建一个批处理文件来设置环境变量并运行程序
    with open(f'{dist_dir}/启动程序.bat', 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('set DEEPSEEK_API_KEY=sk-c0b3998ded644650a8879418e152ac64\n')
        f.write('start "" "%~dp0丰宝智能图片重命名.exe"\n')
    
    # 打包成zip文件
    shutil.make_archive('dist/丰宝智能图片重命名', 'zip', 'dist/丰宝智能图片重命名')
    
if __name__ == '__main__':
    build() 