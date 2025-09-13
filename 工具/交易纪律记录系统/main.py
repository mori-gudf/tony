#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交易纪律记录系统 - 主程序入口
基于Tony交易心法的交易纪律记录系统
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

def main():
    """主函数"""
    try:
        # 导入配置模块
        from config import ensure_config_files

        # 导入主应用类
        from trade_journal import TradeJournalApp

        # 导入方法模块
        import trade_journal_methods

        # 导入工具函数
        from utils import configure_matplotlib_chinese
        
        # 确保配置文件存在
        ensure_config_files()
        
        # 配置matplotlib支持中文显示
        configure_matplotlib_chinese()
        
        # 创建主窗口
        root = tk.Tk()
        
        # 将trade_journal_methods.py中的方法添加到TradeJournalApp类
        for method_name in dir(trade_journal_methods):
            if not method_name.startswith('__'):
                method = getattr(trade_journal_methods, method_name)
                if callable(method):
                    setattr(TradeJournalApp, method_name, method)
        
        # 初始化应用
        app = TradeJournalApp(root)
        
        # 设置窗口图标
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
            if os.path.exists(icon_path):
                img = tk.PhotoImage(file=icon_path)
                root.iconphoto(True, img)
        except Exception as e:
            print(f"设置图标出错: {e}")
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("错误", f"程序启动失败: {e}")
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        sys.exit(1)
    
    # 检查必要的库
    try:
        import pandas as pd
        import matplotlib
        import numpy as np
    except ImportError as e:
        print(f"错误: 缺少必要的库 - {e}")
        print("请安装必要的库: pip install pandas matplotlib numpy")
        sys.exit(1)
    
    # 运行主程序
    main()