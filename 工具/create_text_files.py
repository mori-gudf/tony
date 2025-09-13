#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建文本文件工具 - 最简版本
功能：为图片文件创建对应的空文本文件
使用方法：python3 create_text_files.py <输入目录> <输出目录>
"""

import os
import sys
import re

def main():
    # 检查命令行参数
    if len(sys.argv) < 3:
        print("用法: python3 create_text_files.py <输入目录> <输出目录>")
        print("例如: python3 create_text_files.py ../tony/pdf存档/截图源文件/tony ../tony/pdf存档/文本")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录不存在: {input_dir}")
        sys.exit(1)
    
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
        return
    
    # 按页码排序
    def extract_page_number(filename):
        match = re.search(r'第(\d+)页', filename)
        if match:
            return int(match.group(1))
        return 0
    
    image_files.sort(key=extract_page_number)
    print(f"找到 {len(image_files)} 个图片文件，已按页码排序")
    
    # 创建一个简单的文本文件，记录所有图片
    book_name = os.path.basename(input_dir)
    index_file_path = os.path.join(output_dir, f"{book_name}_图片索引.txt")
    
    with open(index_file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {book_name} 图片索引\n\n")
        f.write("本文件列出了所有图片文件，按页码排序。\n")
        f.write("需要安装OCR软件来提取文字内容。\n\n")
        
        for i, file in enumerate(image_files):
            page_num = extract_page_number(file)
            f.write(f"{i+1}. 第{page_num}页: {file}\n")
            
            # 同时创建一个空的文本文件作为占位符
            base_name = os.path.splitext(file)[0]
            text_file_path = os.path.join(output_dir, f"{base_name}.txt")
            
            with open(text_file_path, 'w', encoding='utf-8') as tf:
                tf.write(f"# 第{page_num}页\n\n")
                tf.write("此文件需要OCR软件来提取文字内容。\n")
    
    # 创建一个安装指南文件
    guide_file_path = os.path.join(output_dir, "OCR安装指南.txt")
    with open(guide_file_path, 'w', encoding='utf-8') as f:
        f.write("# OCR软件安装指南\n\n")
        f.write("要将图片转换为文字，您需要安装以下软件：\n\n")
        f.write("1. Python 3.6或更高版本\n")
        f.write("2. Tesseract OCR引擎\n")
        f.write("3. Python库：pytesseract和Pillow\n\n")
        
        f.write("## 安装步骤\n\n")
        f.write("### 1. 安装Tesseract OCR引擎\n\n")
        f.write("- Mac: brew install tesseract tesseract-lang\n")
        f.write("- Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim\n")
        f.write("- Windows: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载安装\n\n")
        
        f.write("### 2. 创建Python虚拟环境并安装必要的库\n\n")
        f.write("```bash\n")
        f.write("cd 交易学习/工具\n")
        f.write("python3 -m venv venv_ocr\n")
        f.write("source venv_ocr/bin/activate  # Windows上使用: venv_ocr\\Scripts\\activate\n")
        f.write("pip install pytesseract Pillow\n")
        f.write("```\n\n")
        
        f.write("### 3. 运行图片转文字工具\n\n")
        f.write("```bash\n")
        f.write("# 激活虚拟环境\n")
        f.write("source venv_ocr/bin/activate  # Windows上使用: venv_ocr\\Scripts\\activate\n\n")
        f.write("# 运行图形界面版本\n")
        f.write("python images_to_text.py\n\n")
        f.write("# 或者运行命令行版本\n")
        f.write("python images_to_text_cli.py ../tony/pdf存档/截图源文件/tony ../tony/pdf存档/文本 chi_sim+eng\n")
        f.write("```\n")
    
    print(f"已创建图片索引文件: {index_file_path}")
    print(f"已创建OCR安装指南: {guide_file_path}")
    print(f"处理完成! 共处理 {len(image_files)} 个图片文件。")

if __name__ == "__main__":
    main()