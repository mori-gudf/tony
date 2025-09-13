#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片转文字工具 - 命令行版本
功能：将图片文件转换为文字内容并保存到指定目录
使用方法：python3 images_to_text_cli.py <输入目录> <输出目录> [语言]
例如：python3 images_to_text_cli.py ../tony/pdf存档/截图源文件/tony ../tony/pdf存档/文本 chi_sim+eng
"""

import os
import sys
import subprocess
import time
import re

# 尝试安装必要的库
def install_package(package):
    print(f"正在安装 {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"{package} 安装完成")
    time.sleep(1)  # 给一点时间让系统识别新安装的包

# 检查并安装必要的库
try:
    import pytesseract
except ImportError:
    install_package("pytesseract")
    try:
        import pytesseract
    except ImportError:
        print("无法安装 pytesseract，请手动安装: pip install pytesseract")
        sys.exit(1)

try:
    from PIL import Image
except ImportError:
    install_package("Pillow")
    from PIL import Image

def find_tesseract():
    """尝试找到tesseract可执行文件的路径"""
    # 默认路径
    default_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',  # Windows
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',  # Windows 32位
        '/usr/bin/tesseract',  # Linux
        '/usr/local/bin/tesseract',  # macOS
        '/opt/homebrew/bin/tesseract'  # macOS Homebrew
    ]
    
    # 首先检查环境变量
    if 'TESSERACT_CMD' in os.environ:
        return os.environ['TESSERACT_CMD']
    
    # 然后检查默认路径
    for path in default_paths:
        if os.path.isfile(path):
            print(f"找到Tesseract: {path}")
            return path
    
    # 如果找不到，返回默认命令名，让系统在PATH中查找
    print("未找到Tesseract安装路径，将使用系统PATH中的tesseract命令")
    return 'tesseract'

def extract_text_from_image(image_path, lang='chi_sim+eng'):
    """
    从图片中提取文字
    
    参数:
        image_path: 图片文件路径
        lang: OCR语言，默认为简体中文+英文
    
    返回:
        提取的文本内容
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text
    except Exception as e:
        return f"处理图片时出错: {e}"

def process_images_in_directory(input_dir, output_dir, lang='chi_sim+eng'):
    """
    处理目录中的所有图片文件
    
    参数:
        input_dir: 输入图片目录
        output_dir: 输出文本目录
        lang: OCR语言
    """
    print(f"开始处理目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"OCR语言: {lang}")
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
    
    # 获取所有图片文件
    image_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_files.append(file)
    
    if not image_files:
        print(f"错误: 在目录 '{input_dir}' 中没有找到图片文件")
        return False
    
    # 按页码排序
    def extract_page_number(filename):
        match = re.search(r'第(\d+)页', filename)
        if match:
            return int(match.group(1))
        return 0
    
    image_files.sort(key=extract_page_number)
    print(f"找到 {len(image_files)} 个图片文件，已按页码排序")
    
    # 处理每个图片
    total_files = len(image_files)
    all_text = ""
    
    for i, file in enumerate(image_files):
        print(f"处理第 {i+1}/{total_files} 个图片: {file}")
        
        image_path = os.path.join(input_dir, file)
        text = extract_text_from_image(image_path, lang)
        
        # 将文本添加到总文本中
        page_num = extract_page_number(file)
        all_text += f"\n\n--- 第{page_num}页 ---\n\n"
        all_text += text
        
        # 同时保存单独的文本文件
        base_name = os.path.splitext(file)[0]
        text_file_path = os.path.join(output_dir, f"{base_name}.txt")
        
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"已保存: {text_file_path}")
    
    # 保存合并的文本文件
    book_name = os.path.basename(input_dir)
    combined_file_path = os.path.join(output_dir, f"{book_name}_完整文本.txt")
    
    with open(combined_file_path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"已保存合并文本: {combined_file_path}")
    print(f"处理完成! 共处理 {total_files} 个图片，文本已保存到 '{output_dir}'")
    return True

def main():
    # 检查Tesseract是否已安装
    try:
        tesseract_version = pytesseract.get_tesseract_version()
        print(f"检测到Tesseract版本: {tesseract_version}")
    except Exception as e:
        print("警告: 未检测到Tesseract OCR引擎或无法访问它")
        print("错误信息:", e)
        print("\n请确保已安装Tesseract OCR引擎:")
        print("- Windows: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载安装")
        print("- Mac: brew install tesseract tesseract-lang")
        print("- Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim")
        print("- Fedora: sudo dnf install tesseract tesseract-langpack-chi-sim")
        print("\n程序将继续运行，但如果没有安装Tesseract，OCR功能将无法正常工作。")
    
    # 设置tesseract路径
    tesseract_path = find_tesseract()
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # 解析命令行参数
    if len(sys.argv) < 3:
        print("用法: python3 images_to_text_cli.py <输入目录> <输出目录> [语言]")
        print("例如: python3 images_to_text_cli.py ../tony/pdf存档/截图源文件/tony ../tony/pdf存档/文本 chi_sim+eng")
        print("\n可用的语言选项:")
        print("- chi_sim+eng: 简体中文+英文（默认）")
        print("- chi_sim: 仅简体中文")
        print("- eng: 仅英文")
        print("- chi_tra+eng: 繁体中文+英文")
        print("- chi_tra: 仅繁体中文")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else 'chi_sim+eng'
    
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    process_images_in_directory(input_dir, output_dir, lang)

if __name__ == "__main__":
    main()