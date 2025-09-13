#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版图片转文字工具 - 命令行版本
功能：将图片文件转换为文字内容并保存到指定目录
使用方法：python3 images_to_text_simple.py <输入目录> <输出目录>
"""

import os
import sys
import re
from PIL import Image  # 这个库通常是预装的，如果没有可以手动安装: pip install Pillow

def main():
    # 检查命令行参数
    if len(sys.argv) < 3:
        print("用法: python3 images_to_text_simple.py <输入目录> <输出目录>")
        print("例如: python3 images_to_text_simple.py ../tony/pdf存档/截图源文件/tony ../tony/pdf存档/文本")
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
        f.write("由于未安装OCR引擎，无法自动提取文字内容。\n")
        f.write("请安装Tesseract OCR引擎后使用完整版工具。\n\n")
        
        for i, file in enumerate(image_files):
            page_num = extract_page_number(file)
            f.write(f"{i+1}. 第{page_num}页: {file}\n")
            
            # 同时创建一个空的文本文件作为占位符
            base_name = os.path.splitext(file)[0]
            text_file_path = os.path.join(output_dir, f"{base_name}.txt")
            
            with open(text_file_path, 'w', encoding='utf-8') as tf:
                tf.write(f"# 第{page_num}页\n\n")
                tf.write("此文件需要OCR引擎来提取文字内容。\n")
                tf.write("请安装Tesseract OCR引擎后使用完整版工具。\n")
    
    print(f"已创建图片索引文件: {index_file_path}")
    print(f"处理完成! 共处理 {len(image_files)} 个图片文件。")
    print("\n注意: 由于未安装OCR引擎，无法提取文字内容。")
    print("请安装Tesseract OCR引擎后使用完整版工具:")
    print("- Mac: brew install tesseract tesseract-lang")
    print("- Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim")
    print("- Windows: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载安装")

if __name__ == "__main__":
    main()