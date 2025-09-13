#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF转图片工具
功能：将PDF文件的每一页转换为图片并保存到指定目录
使用方法：直接运行程序，通过图形界面选择PDF文件和输出目录
"""

import os
import sys
import fitz  # PyMuPDF
from PIL import Image
import io
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

def convert_pdf_to_images(pdf_path, output_dir, dpi=300, progress_callback=None):
    """
    将PDF文件的每一页转换为图片
    
    参数:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        dpi: 图像分辨率，默认300
        progress_callback: 进度回调函数
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取PDF文件名（不含扩展名）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 打开PDF文件
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        return False, f"无法打开PDF文件: {e}"
    
    # 获取PDF页数
    page_count = pdf_document.page_count
    
    # 转换每一页
    for page_num in range(page_count):
        if progress_callback:
            progress_callback(page_num, page_count)
            
        page = pdf_document.load_page(page_num)
        
        # 渲染页面为图像
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        
        # 将pixmap转换为PIL图像
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # 保存图像
        img_path = os.path.join(output_dir, f"{pdf_name}_第{page_num+1:03d}页.png")
        img.save(img_path)
    
    pdf_document.close()
    return True, f"转换完成! 共转换 {page_count} 页，图像已保存到 '{output_dir}'"

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF转图片工具")
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
        
        # PDF文件选择
        pdf_frame = ttk.Frame(main_frame)
        pdf_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(pdf_frame, text="PDF文件:").pack(side=tk.LEFT)
        self.pdf_path_var = tk.StringVar()
        ttk.Entry(pdf_frame, textvariable=self.pdf_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(pdf_frame, text="浏览...", command=self.browse_pdf).pack(side=tk.RIGHT)
        
        # 输出目录选择
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_dir_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览...", command=self.browse_output_dir).pack(side=tk.RIGHT)
        
        # DPI设置
        dpi_frame = ttk.Frame(main_frame)
        dpi_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(dpi_frame, text="图像DPI:").pack(side=tk.LEFT)
        self.dpi_var = tk.IntVar(value=300)
        dpi_values = [72, 150, 300, 600]
        dpi_combo = ttk.Combobox(dpi_frame, textvariable=self.dpi_var, values=dpi_values, width=10)
        dpi_combo.pack(side=tk.LEFT, padx=5)
        ttk.Label(dpi_frame, text="(较高的DPI会产生更清晰但更大的图像)").pack(side=tk.LEFT, padx=5)
        
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
    
    def browse_pdf(self):
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if file_path:
            self.pdf_path_var.set(file_path)
            # 自动设置默认输出目录为PDF所在目录下的"转换后图片"文件夹
            pdf_dir = os.path.dirname(file_path)
            pdf_name = os.path.splitext(os.path.basename(file_path))[0]
            self.output_dir_var.set(os.path.join(pdf_dir, f"{pdf_name}_转换后图片"))
    
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir_var.set(dir_path)
    
    def update_progress(self, current, total):
        progress = (current + 1) / total * 100
        self.progress_var.set(progress)
        self.status_var.set(f"正在处理第 {current + 1}/{total} 页 ({int(progress)}%)")
        self.root.update_idletasks()
    
    def start_conversion(self):
        pdf_path = self.pdf_path_var.get()
        output_dir = self.output_dir_var.get()
        dpi = self.dpi_var.get()
        
        if not pdf_path or not output_dir:
            messagebox.showerror("错误", "请选择PDF文件和输出目录")
            return
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("错误", f"PDF文件不存在: {pdf_path}")
            return
        
        # 禁用按钮，防止重复点击
        self.convert_button.config(state=tk.DISABLED)
        self.status_var.set("正在准备转换...")
        self.progress_var.set(0)
        
        # 在新线程中执行转换，避免界面卡死
        def conversion_thread():
            success, message = convert_pdf_to_images(pdf_path, output_dir, dpi, self.update_progress)
            
            # 更新UI（必须在主线程中进行）
            self.root.after(0, lambda: self.conversion_complete(success, message))
        
        threading.Thread(target=conversion_thread).start()
    
    def conversion_complete(self, success, message):
        self.convert_button.config(state=tk.NORMAL)
        
        if success:
            self.status_var.set("转换完成!")
            messagebox.showinfo("成功", message)
        else:
            self.status_var.set("转换失败!")
            messagebox.showerror("错误", message)

def main():
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
