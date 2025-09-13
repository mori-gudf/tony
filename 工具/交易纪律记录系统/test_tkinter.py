#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tkinter测试程序
用于测试tkinter是否正常工作
"""

import tkinter as tk

def main():
    """主函数"""
    # 创建主窗口
    root = tk.Tk()
    root.title("tkinter测试")
    root.geometry("300x200")
    
    # 添加标签
    label = tk.Label(root, text="如果您能看到这个窗口，说明tkinter正常工作！", wraplength=250)
    label.pack(pady=50)
    
    # 添加按钮
    button = tk.Button(root, text="关闭", command=root.destroy)
    button.pack(pady=20)
    
    # 运行应用
    root.mainloop()

if __name__ == "__main__":
    main()