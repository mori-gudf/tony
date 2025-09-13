#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交易纪律记录系统 - 调试版主程序
带有更多调试信息的版本
"""

import os
import sys
import traceback

def main():
    """主函数"""
    try:
        print("开始导入模块...")
        
        print("导入tkinter...")
        import tkinter as tk
        from tkinter import ttk, messagebox
        print("tkinter导入成功")
        
        print("导入config模块...")
        from config import ensure_config_files
        print("config模块导入成功")
        
        print("导入trade_journal模块...")
        from trade_journal import TradeJournalApp
        print("trade_journal模块导入成功")
        
        print("导入trade_journal_methods模块...")
        import trade_journal_methods
        # 将trade_journal_methods.py中的方法添加到TradeJournalApp类
        for method_name in dir(trade_journal_methods):
            if not method_name.startswith('__'):
                method = getattr(trade_journal_methods, method_name)
                if callable(method):
                    setattr(TradeJournalApp, method_name, method)
        print("trade_journal_methods模块导入成功")
        
        print("配置matplotlib支持中文显示...")
        from utils import configure_matplotlib_chinese
        configure_matplotlib_chinese()
        print("matplotlib中文配置完成")
        
        print("确保配置文件存在...")
        ensure_config_files()
        print("配置文件检查完成")
        
        print("创建主窗口...")
        root = tk.Tk()
        print("主窗口创建成功")
        
        print("初始化应用...")
        app = TradeJournalApp(root)
        print("应用初始化成功")
        
        # 设置窗口图标
        try:
            print("尝试设置图标...")
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
            if os.path.exists(icon_path):
                img = tk.PhotoImage(file=icon_path)
                root.iconphoto(True, img)
                print(f"图标设置成功: {icon_path}")
            else:
                print(f"图标文件不存在: {icon_path}")
        except Exception as e:
            print(f"设置图标出错: {e}")
        
        print("启动主循环...")
        root.mainloop()
        print("主循环结束")
        
    except Exception as e:
        print(f"发生错误: {e}")
        print("详细错误信息:")
        traceback.print_exc()

if __name__ == "__main__":
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        sys.exit(1)
    
    # 检查必要的库
    try:
        print("检查必要的库...")
        
        print("导入pandas...")
        import pandas as pd
        print(f"pandas版本: {pd.__version__}")
        
        print("导入matplotlib...")
        import matplotlib
        print(f"matplotlib版本: {matplotlib.__version__}")
        print(f"matplotlib后端: {matplotlib.get_backend()}")
        
        print("导入numpy...")
        import numpy as np
        print(f"numpy版本: {np.__version__}")
        
    except ImportError as e:
        print(f"错误: 缺少必要的库 - {e}")
        print("请安装必要的库: pip install pandas matplotlib numpy")
        sys.exit(1)
    
    # 运行主程序
    print("开始运行主程序...")
    main()