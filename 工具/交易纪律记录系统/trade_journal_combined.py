#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交易纪律记录系统 - 主应用类
实现交易记录、资金管理、交易日志、统计分析和心法提示功能
"""

import os
import sys
import json
import datetime
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import matplotlib
matplotlib.use('TkAgg')  # 设置Matplotlib后端
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

# 导入配置模块
from config import (
    load_config, save_config, 
    load_trades, save_trades, 
    load_journal, save_journal, 
    load_heart_quotes, save_heart_quotes
)

# 导入对话框模块
from dialogs import (
    TradeDialog, JournalDialog, 
    HeartQuoteDialog, SettingsDialog,
    PositionCalculatorDialog
)

# 导入工具函数
from utils import calculate_statistics, create_pnl_chart, create_winrate_chart, create_capital_chart, generate_report, get_random_heart_quote, check_risk_warnings, configure_matplotlib_chinese

class TradeJournalApp:
    """交易纪律记录系统主应用类"""
    
    def __init__(self, root):
        """初始化应用"""
        self.root = root
        self.root.title("交易纪律记录系统 - 基于Tony交易心法")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # 配置matplotlib支持中文显示
        configure_matplotlib_chinese()
        
        # 加载数据
        self.config = load_config()
        self.trades = load_trades()
        self.journal = load_journal()
        self.heart_quotes = load_heart_quotes()
        
        # 创建主界面
        self.create_main_ui()
        
        # 显示每日心法提示
        self.show_daily_heart_quote()
        
        # 检查风险警告
        self.check_risk_warnings()
    
    def create_main_ui(self):
        """创建主界面"""
        # 创建选项卡
        self.tab_control = ttk.Notebook(self.root)
        
        # 交易记录选项卡
        self.tab_trades = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_trades, text="交易记录")
        self.create_trades_tab()
        
        # 资金管理选项卡
        self.tab_capital = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_capital, text="资金管理")
        self.create_capital_tab()
        
        # 交易日志选项卡
        self.tab_journal = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_journal, text="交易日志")
        self.create_journal_tab()
        
        # 统计分析选项卡
        self.tab_stats = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_stats, text="统计分析")
        self.create_stats_tab()
        
        # 心法提示选项卡
        self.tab_heart = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_heart, text="心法提示")
        self.create_heart_tab()
        
        # 设置选项卡
        self.tab_settings = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_settings, text="设置")
        self.create_settings_tab()
        
        self.tab_control.pack(expand=1, fill="both")
        
        # 状态栏
        self.status_bar = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="就绪")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.capital_label = ttk.Label(self.status_bar, text=f"当前资金: {self.calculate_current_capital():,.2f} 元")
        self.capital_label.pack(side=tk.RIGHT, padx=5)
        
        self.profit_label = ttk.Label(self.status_bar)
        self.update_profit_label()
        self.profit_label.pack(side=tk.RIGHT, padx=5)
    
    def create_trades_tab(self):
        """创建交易记录选项卡"""
        # 上部分：交易记录表格
        table_frame = ttk.Frame(self.tab_trades)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建表格
        columns = ("日期", "时间", "标的", "方向", "价格", "数量", "止损价", "目标价", "结果", "盈亏", "备注")
        self.trades_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 设置列宽和标题
        for col in columns:
            self.trades_tree.heading(col, text=col)
            width = 80
            if col == "标的" or col == "备注":
                width = 120
            elif col == "盈亏":
                width = 100
            self.trades_tree.column(col, width=width)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.trades_tree.yview)
        self.trades_tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.trades_tree.xview)
        self.trades_tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.trades_tree.pack(fill=tk.BOTH, expand=True)
        
        # 下部分：操作按钮
        button_frame = ttk.Frame(self.tab_trades)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加交易", command=self.add_trade).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑交易", command=self.edit_trade).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除交易", command=self.delete_trade).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_trades).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="导出CSV", command=self.export_trades_csv).pack(side=tk.RIGHT, padx=5)
        
        # 加载交易记录
        self.refresh_trades()
    
    def create_capital_tab(self):
        """创建资金管理选项卡"""
        # 上部分：资金概览
        overview_frame = ttk.LabelFrame(self.tab_capital, text="资金概览")
        overview_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 资金信息
        info_frame = ttk.Frame(overview_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 第一行
        row1 = ttk.Frame(info_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text="初始资金:").pack(side=tk.LEFT, padx=5)
        self.initial_capital_var = tk.StringVar(value=f"{self.config['initial_capital']:,.2f} 元")
        ttk.Label(row1, textvariable=self.initial_capital_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="当前资金:").pack(side=tk.LEFT, padx=20)
        self.current_capital_var = tk.StringVar(value=f"{self.calculate_current_capital():,.2f} 元")
        ttk.Label(row1, textvariable=self.current_capital_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="总收益率:").pack(side=tk.LEFT, padx=20)
        self.total_return_var = tk.StringVar()
        self.update_total_return()
        ttk.Label(row1, textvariable=self.total_return_var).pack(side=tk.LEFT, padx=5)
        
        # 第二行
        row2 = ttk.Frame(info_frame)
        row2.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2, text="当前仓位:").pack(side=tk.LEFT, padx=5)
        self.current_position_var = tk.StringVar()
        self.update_current_position()
        ttk.Label(row2, textvariable=self.current_position_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="最大回撤:").pack(side=tk.LEFT, padx=20)
        self.max_drawdown_var = tk.StringVar()
        self.update_max_drawdown()
        ttk.Label(row2, textvariable=self.max_drawdown_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="盈亏比:").pack(side=tk.LEFT, padx=20)
        self.profit_loss_ratio_var = tk.StringVar()
        self.update_profit_loss_ratio()
        ttk.Label(row2, textvariable=self.profit_loss_ratio_var).pack(side=tk.LEFT, padx=5)
        
        # 中部分：资金曲线图
        chart_frame = ttk.LabelFrame(self.tab_capital, text="资金曲线")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.capital_figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.capital_canvas = FigureCanvasTkAgg(self.capital_figure, chart_frame)
        self.capital_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.update_capital_chart()
        
        # 下部分：仓位计算器
        calc_frame = ttk.LabelFrame(self.tab_capital, text="仓位计算器")
        calc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 计算器按钮
        ttk.Button(calc_frame, text="打开仓位计算器", command=self.open_position_calculator).pack(padx=10, pady=10)
    
    def create_journal_tab(self):
        """创建交易日志选项卡"""
        # 上部分：日志列表
        list_frame = ttk.Frame(self.tab_journal)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建列表
        columns = ("日期", "标题", "类型")
        self.journal_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # 设置列宽和标题
        for col in columns:
            self.journal_tree.heading(col, text=col)
            width = 100
            if col == "标题":
                width = 300
            self.journal_tree.column(col, width=width)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.journal_tree.yview)
        self.journal_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.journal_tree.pack(fill=tk.BOTH, expand=True)
        self.journal_tree.bind("<Double-1>", self.view_journal)
        
        # 下部分：操作按钮
        button_frame = ttk.Frame(self.tab_journal)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加日志", command=self.add_journal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="查看日志", command=self.view_journal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除日志", command=self.delete_journal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_journal).pack(side=tk.LEFT, padx=5)
        
        # 加载日志
        self.refresh_journal()
    
    def create_stats_tab(self):
        """创建统计分析选项卡"""
        # 创建图表框架
        charts_frame = ttk.Frame(self.tab_stats)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 上部分：左右两个图表
        top_frame = ttk.Frame(charts_frame)
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：盈亏分布图
        left_frame = ttk.LabelFrame(top_frame, text="盈亏分布")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.pnl_figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.pnl_canvas = FigureCanvasTkAgg(self.pnl_figure, left_frame)
        self.pnl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 右侧：胜率统计图
        right_frame = ttk.LabelFrame(top_frame, text="胜率统计")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.winrate_figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.winrate_canvas = FigureCanvasTkAgg(self.winrate_figure, right_frame)
        self.winrate_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 下部分：交易统计表
        stats_frame = ttk.LabelFrame(charts_frame, text="交易统计")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 统计信息
        info_frame = ttk.Frame(stats_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 第一行
        row1 = ttk.Frame(info_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text="总交易次数:").pack(side=tk.LEFT, padx=5)
        self.total_trades_var = tk.StringVar(value="0")
        ttk.Label(row1, textvariable=self.total_trades_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="盈利交易:").pack(side=tk.LEFT, padx=20)
        self.winning_trades_var = tk.StringVar(value="0")
        ttk.Label(row1, textvariable=self.winning_trades_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="亏损交易:").pack(side=tk.LEFT, padx=20)
        self.losing_trades_var = tk.StringVar(value="0")
        ttk.Label(row1, textvariable=self.losing_trades_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="胜率:").pack(side=tk.LEFT, padx=20)
        self.win_rate_var = tk.StringVar(value="0.0%")
        ttk.Label(row1, textvariable=self.win_rate_var).pack(side=tk.LEFT, padx=5)
        
        # 第二行
        row2 = ttk.Frame(info_frame)
        row2.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2, text="平均盈利:").pack(side=tk.LEFT, padx=5)
        self.avg_profit_var = tk.StringVar(value="0.00 元")
        ttk.Label(row2, textvariable=self.avg_profit_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="平均亏损:").pack(side=tk.LEFT, padx=20)
        self.avg_loss_var = tk.StringVar(value="0.00 元")
        ttk.Label(row2, textvariable=self.avg_loss_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="盈亏比:").pack(side=tk.LEFT, padx=20)
        self.profit_factor_var = tk.StringVar(value="0.00")
        ttk.Label(row2, textvariable=self.profit_factor_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2, text="期望值:").pack(side=tk.LEFT, padx=20)
        self.expectancy_var = tk.StringVar(value="0.00 元")
        ttk.Label(row2, textvariable=self.expectancy_var).pack(side=tk.LEFT, padx=5)
        
        # 按钮
        button_frame = ttk.Frame(charts_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="刷新统计", command=self.update_statistics).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="生成报告", command=self.generate_report).pack(side=tk.LEFT, padx=5)
        
        # 更新统计
        self.update_statistics()
    
    def create_heart_tab(self):
        """创建心法提示选项卡"""
        # 上部分：每日心法
        daily_frame = ttk.LabelFrame(self.tab_heart, text="每日心法")
        daily_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.daily_quote_var = tk.StringVar(value="加载中...")
        quote_label = ttk.Label(daily_frame, textvariable=self.daily_quote_var, font=("黑体", 14))
        quote_label.pack(padx=20, pady=20)
        
        # 中部分：心法列表
        list_frame = ttk.LabelFrame(self.tab_heart, text="心法语录")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建列表
        columns = ("类别", "心法")
        self.heart_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # 设置列宽和标题
        self.heart_tree.heading("类别", text="类别")
        self.heart_tree.heading("心法", text="心法")
        self.heart_tree.column("类别", width=100)
        self.heart_tree.column("心法", width=500)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.heart_tree.yview)
        self.heart_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.heart_tree.pack(fill=tk.BOTH, expand=True)
        
        # 下部分：操作按钮
        button_frame = ttk.Frame(self.tab_heart)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加心法", command=self.add_heart_quote).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑心法", command=self.edit_heart_quote).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除心法", command=self.delete_heart_quote).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_heart_quotes).pack(side=tk.LEFT, padx=5)
        
        # 加载心法语录
        self.refresh_heart_quotes()
    
    def create_settings_tab(self):
        """创建设置选项卡"""
        # 设置框架
        settings_frame = ttk.Frame(self.tab_settings)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 基本设置
        basic_frame = ttk.LabelFrame(settings_frame, text="基本设置")
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 用户名
        name_frame = ttk.Frame(basic_frame)
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(name_frame, text="用户名:").pack(side=tk.LEFT, padx=5)
        self.username_var = tk.StringVar(value=self.config.get("user_name", "交易者"))
        ttk.Entry(name_frame, textvariable=self.username_var, width=20).pack(side=tk.LEFT, padx=5)
        
        # 资金设置
        capital_frame = ttk.LabelFrame(settings_frame, text="资金设置")
        capital_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 初始资金
        init_frame = ttk.Frame(capital_frame)
        init_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(init_frame, text="初始资金:").pack(side=tk.LEFT, padx=5)
        self.init_capital_var = tk.StringVar(value=str(self.config.get("initial_capital", 100000)))
        ttk.Entry(init_frame, textvariable=self.init_capital_var, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Label(init_frame, text="元").pack(side=tk.LEFT)
        
        # 风险设置
        risk_frame = ttk.LabelFrame(settings_frame, text="风险设置")
        risk_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 每笔交易风险比例
        risk_trade_frame = ttk.Frame(risk_frame)
        risk_trade_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(risk_trade_frame, text="每笔交易风险比例:").pack(side=tk.LEFT, padx=5)
        self.risk_per_trade_var = tk.StringVar(value=str(self.config.get("risk_per_trade", 0.02) * 100))
        ttk.Entry(risk_trade_frame, textvariable=self.risk_per_trade_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(risk_trade_frame, text="%").pack(side=tk.LEFT)
        
        # 最大仓位比例
        max_pos_frame = ttk.Frame(risk_frame)
        max_pos_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(max_pos_frame, text="最大仓位比例:").pack(side=tk.LEFT, padx=5)
        self.max_position_var = tk.StringVar(value=str(self.config.get("max_position_size", 0.3) * 100))
        ttk.Entry(max_pos_frame, textvariable=self.max_position_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(max_pos_frame, text="%").pack(side=tk.LEFT)
        
        # 最大回撤警告
        max_dd_frame = ttk.Frame(risk_frame)
        max_dd_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(max_dd_frame, text="最大回撤警告:").pack(side=tk.LEFT, padx=5)
        self.max_drawdown_alert_var = tk.StringVar(value=str(self.config.get("max_drawdown_alert", 0.1) * 100))
        ttk.Entry(max_dd_frame, textvariable=self.max_drawdown_alert_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(max_dd_frame, text="%").pack(side=tk.LEFT)
        
        # 日亏损限制
        daily_loss_frame = ttk.Frame(risk_frame)
        daily_loss_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(daily_loss_frame, text="日亏损限制:").pack(side=tk.LEFT, padx=5)
        self.daily_loss_limit_var = tk.StringVar(value=str(self.config.get("daily_loss_limit", 0.05) * 100))
        ttk.Entry(daily_loss_frame, textvariable=self.daily_loss_limit_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(daily_loss_frame, text="%").pack(side=tk.LEFT)
        
        # 年度收益目标
        profit_target_frame = ttk.Frame(risk_frame)
        profit_target_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(profit_target_frame, text="年度收益目标:").pack(side=tk.LEFT, padx=5)
        self.profit_target_var = tk.StringVar(value=str(self.config.get("profit_target", 0.5) * 100))
        ttk.Entry(profit_target_frame, textvariable=self.profit_target_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(profit_target_frame, text="%").pack(side=tk.LEFT)
        
        # 按钮
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="保存设置", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重置设置", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="备份数据", command=self.backup_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="恢复数据", command=self.restore_data).pack(side=tk.RIGHT, padx=5)

    def check_risk_warnings(self):
        """检查风险警告"""
        # 从utils模块导入的check_risk_warnings函数
        warnings = check_risk_warnings(self.trades, self.config)
        
        if warnings:
            message = "\n".join(warnings)
            messagebox.showwarning("风险警告", message)
    
    # 以下是从trade_journal_methods.py导入的方法
    
    def add_trade(self):
        """添加交易记录"""
        dialog = TradeDialog(self.root, "添加交易记录")
        if dialog.result:
            self.trades.append(dialog.result)
            save_trades(self.trades)
            self.refresh_trades()
            self.update_statistics()
            self.update_capital_chart()
            self.update_profit_label()
            self.status_label.config(text="交易记录已添加")

    def edit_trade(self):
        """编辑交易记录"""
        selected = self.trades_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请先选择要编辑的交易记录")
            return
        
        item = self.trades_tree.item(selected[0])
        values = item["values"]
        
        # 查找对应的交易记录
        for i, trade in enumerate(self.trades):
            if (trade.get("日期") == values[0] and 
                trade.get("时间") == values[1] and 
                trade.get("标的") == values[2]):