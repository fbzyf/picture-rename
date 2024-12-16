import os
import sys

if __name__ == '__main__':
    # 添加src目录到Python路径
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
    sys.path.insert(0, src_path)
    
    # 切换到src目录
    os.chdir(src_path)
    
    # 运行主程序
    from main import main
    main() 