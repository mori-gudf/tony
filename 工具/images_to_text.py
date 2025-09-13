#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片转文字工具
功能：将图片文件转换为文字内容并保存到指定目录
使用方法：直接运行程序，通过图形界面选择图片目录和输出目录
"""

import os
import sys
import subprocess
import time

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

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import re

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

def process_images_in_directory(input_dir, output_dir, lang='chi_sim+eng', progress_callback=None):
    """
    处理目录中的所有图片文件
    
    参数:
        input_dir: 输入图片目录
        output_dir: 输出文本目录
        lang: OCR语言
        progress_callback: 进度回调函数
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有图片文件
    image_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_files.append(file)
    
    if not image_files:
        return False, f"在目录 '{input_dir}' 中没有找到图片文件"
    
    # 按页码排序
    def extract_page_number(filename):
        match = re.search(r'第(\d+)页', filename)
        if match:
            return int(match.group(1))
        return 0
    
    image_files.sort(key=extract_page_number)
    
    # 处理每个图片
    total_files = len(image_files)
    all_text = ""
    
    for i, file in enumerate(image_files):
        if progress_callback:
            progress_callback(i, total_files)
        
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
    
    # 保存合并的文本文件
    book_name = os.path.basename(input_dir)
    combined_file_path = os.path.join(output_dir, f"{book_name}_完整文本.txt")
    
    with open(combined_file_path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    return True, f"处理完成! 共处理 {total_files} 个图片，文本已保存到 '{output_dir}'"

class ImageToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片转文字工具")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("TLabel", padding=6, font=('Helvetica', 12))
        self.style.configure("TProgressbar", thickness=20)
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入目录选择
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="图片目录:").pack(side=tk.LEFT)
        self.input_dir_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_dir_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="浏览...", command=self.browse_input_dir).pack(side=tk.RIGHT)
        
        # 输出目录选择
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_dir_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览...", command=self.browse_output_dir).pack(side=tk.RIGHT)
        
        # 语言选择
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(lang_frame, text="OCR语言:").pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="chi_sim+eng")
        lang_values = ["chi_sim+eng", "chi_sim", "eng", "chi_tra+eng", "chi_tra"]
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=lang_values, width=15)
        lang_combo.pack(side=tk.LEFT, padx=5)
        ttk.Label(lang_frame, text="(chi_sim=简体中文, eng=英文, chi_tra=繁体中文)").pack(side=tk.LEFT, padx=5)
        
        # 进度条
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=20)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="准备就绪")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(fill=tk.X, pady=5)
        
        # 转换按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.convert_button = ttk.Button(button_frame, text="开始转换", command=self.start_conversion)
        self.convert_button.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="退出", command=root.quit).pack(side=tk.RIGHT, padx=5)
    
    def browse_input_dir(self):
        dir_path = filedialog.askdirectory(title="选择图片目录")
        if dir_path:
            self.input_dir_var.set(dir_path)
            # 自动设置默认输出目录
            parent_dir = os.path.dirname(dir_path)
            dir_name = os.path.basename(dir_path)
            self.output_dir_var.set(os.path.join(parent_dir, f"{dir_name}_文本"))
    
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir_var.set(dir_path)
    
    def update_progress(self, current, total):
        progress = (current + 1) / total * 100
        self.progress_var.set(progress)
        self.status_var.set(f"正在处理第 {current + 1}/{total} 个图片 ({int(progress)}%)")
        self.root.update_idletasks()
    
    def start_conversion(self):
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()
        lang = self.lang_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("错误", "请选择图片目录和输出目录")
            return
        
        if not os.path.exists(input_dir):
            messagebox.showerror("错误", f"图片目录不存在: {input_dir}")
            return
        
        # 禁用按钮，防止重复点击
        self.convert_button.config(state=tk.DISABLED)
        self.status_var.set("正在准备转换...")
        self.progress_var.set(0)
        
        # 在新线程中执行转换，避免界面卡死
        def conversion_thread():
            try:
                # 尝试设置tesseract路径
                tesseract_path = self.find_tesseract()
                if tesseract_path:
                    pytesseract.pytesseract.tesseract_cmd = tesseract_path
                
                success, message = process_images_in_directory(input_dir, output_dir, lang, self.update_progress)
                
                # 更新UI（必须在主线程中进行）
                self.root.after(0, lambda: self.conversion_complete(success, message))
            except Exception as e:
                self.root.after(0, lambda: self.conversion_complete(False, f"转换过程中出错: {e}"))
        
        threading.Thread(target=conversion_thread).start()
    
    def find_tesseract(self):
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
    
    def conversion_complete(self, success, message):
        self.convert_button.config(state=tk.NORMAL)
        
        if success:
            self.status_var.set("转换完成!")
            messagebox.showinfo("成功", message)
        else:
            self.status_var.set("转换失败!")
            messagebox.showerror("错误", message)

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
    
    root = tk.Tk()
    app = ImageToTextApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()