#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交易纪律记录系统 - 对话框模块
实现各种对话框界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime

class TradeDialog:
    """交易记录对话框"""
    
    def __init__(self, parent, title="添加交易记录", trade=None):
        """初始化对话框"""
        self.parent = parent
        self.result = None
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x550")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # 创建表单
        self.create_form(trade)
        
        # 模态显示
        self.dialog.wait_window()
    
    def create_form(self, trade=None):
        """创建表单"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 日期和时间
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(date_frame, text="日期:").pack(side=tk.LEFT, padx=5)
        self.date_var = tk.StringVar()
        if trade and "日期" in trade:
            self.date_var.set(trade["日期"])
        else:
            self.date_var.set(datetime.datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.date_var, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(date_frame, text="时间:").pack(side=tk.LEFT, padx=20)
        self.time_var = tk.StringVar()
        if trade and "时间" in trade:
            self.time_var.set(trade["时间"])
        else:
            self.time_var.set(datetime.datetime.now().strftime("%H:%M:%S"))
        ttk.Entry(date_frame, textvariable=self.time_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 标的和方向
        symbol_frame = ttk.Frame(main_frame)
        symbol_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(symbol_frame, text="标的:").pack(side=tk.LEFT, padx=5)
        self.symbol_var = tk.StringVar()
        if trade and "标的" in trade:
            self.symbol_var.set(trade["标的"])
        ttk.Entry(symbol_frame, textvariable=self.symbol_var, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(symbol_frame, text="方向:").pack(side=tk.LEFT, padx=20)
        self.direction_var = tk.StringVar()
        if trade and "方向" in trade:
            self.direction_var.set(trade["方向"])
        direction_combo = ttk.Combobox(symbol_frame, textvariable=self.direction_var, width=10)
        direction_combo["values"] = ("买入", "卖出")
        direction_combo.pack(side=tk.LEFT, padx=5)
        
        # 价格和数量
        price_frame = ttk.Frame(main_frame)
        price_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(price_frame, text="价格:").pack(side=tk.LEFT, padx=5)
        self.price_var = tk.StringVar()
        if trade and "价格" in trade:
            self.price_var.set(trade["价格"])
        ttk.Entry(price_frame, textvariable=self.price_var, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(price_frame, text="数量:").pack(side=tk.LEFT, padx=20)
        self.quantity_var = tk.StringVar()
        if trade and "数量" in trade:
            self.quantity_var.set(trade["数量"])
        ttk.Entry(price_frame, textvariable=self.quantity_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 止损和目标价
        stop_frame = ttk.Frame(main_frame)
        stop_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(stop_frame, text="止损价:").pack(side=tk.LEFT, padx=5)
        self.stop_var = tk.StringVar()
        if trade and "止损价" in trade:
            self.stop_var.set(trade["止损价"])
        ttk.Entry(stop_frame, textvariable=self.stop_var, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(stop_frame, text="目标价:").pack(side=tk.LEFT, padx=20)
        self.target_var = tk.StringVar()
        if trade and "目标价" in trade:
            self.target_var.set(trade["目标价"])
        ttk.Entry(stop_frame, textvariable=self.target_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 结果和盈亏
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(result_frame, text="结果:").pack(side=tk.LEFT, padx=5)
        self.result_var = tk.StringVar()
        if trade and "结果" in trade:
            self.result_var.set(trade["结果"])
        result_combo = ttk.Combobox(result_frame, textvariable=self.result_var, width=10)
        result_combo["values"] = ("盈利", "亏损", "持平", "未平仓")
        result_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(result_frame, text="盈亏:").pack(side=tk.LEFT, padx=20)
        self.pnl_var = tk.StringVar()
        if trade and "盈亏" in trade:
            self.pnl_var.set(trade["盈亏"])
        ttk.Entry(result_frame, textvariable=self.pnl_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 备注
        note_frame = ttk.LabelFrame(main_frame, text="备注")
        note_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.note_text = tk.Text(note_frame, height=10, width=50)
        self.note_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        if trade and "备注" in trade:
            self.note_text.insert(tk.END, trade["备注"])
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)
    
    def on_ok(self):
        """确定按钮事件"""
        # 验证输入
        if not self.validate():
            return
        
        # 收集数据
        self.result = {
            "日期": self.date_var.get(),
            "时间": self.time_var.get(),
            "标的": self.symbol_var.get(),
            "方向": self.direction_var.get(),
            "价格": self.price_var.get(),
            "数量": self.quantity_var.get(),
            "止损价": self.stop_var.get(),
            "目标价": self.target_var.get(),
            "结果": self.result_var.get(),
            "盈亏": self.pnl_var.get(),
            "备注": self.note_text.get("1.0", tk.END).strip()
        }
        
        # 关闭对话框
        self.dialog.destroy()
    
    def on_cancel(self):
        """取消按钮事件"""
        self.dialog.destroy()
    
    def validate(self):
        """验证输入"""
        # 检查必填字段
        if not self.symbol_var.get():
            messagebox.showerror("错误", "请输入交易标的")
            return False
        
        if not self.direction_var.get():
            messagebox.showerror("错误", "请选择交易方向")
            return False
        
        if not self.price_var.get():
            messagebox.showerror("错误", "请输入交易价格")
            return False
        
        if not self.quantity_var.get():
            messagebox.showerror("错误", "请输入交易数量")
            return False
        
        # 检查数值字段
        try:
            if self.price_var.get():
                float(self.price_var.get())
            
            if self.quantity_var.get():
                float(self.quantity_var.get())
            
            if self.stop_var.get():
                float(self.stop_var.get())
            
            if self.target_var.get():
                float(self.target_var.get())
            
            if self.pnl_var.get():
                float(self.pnl_var.get())
        except ValueError:
            messagebox.showerror("错误", "价格、数量、止损价、目标价和盈亏必须是数字")
            return False
        
        return True


class JournalDialog:
    """交易日志对话框"""
    
    def __init__(self, parent, title="添加交易日志", journal=None, readonly=False):
        """初始化对话框"""
        self.parent = parent
        self.result = None
        self.readonly = readonly
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # 创建表单
        self.create_form(journal)
        
        # 模态显示
        self.dialog.wait_window()
    
    def create_form(self, journal=None):
        """创建表单"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 日期和类型
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(header_frame, text="日期:").pack(side=tk.LEFT, padx=5)
        self.date_var = tk.StringVar()
        if journal and "日期" in journal:
            self.date_var.set(journal["日期"])
        else:
            self.date_var.set(datetime.datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(header_frame, textvariable=self.date_var, width=15)
        date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(header_frame, text="类型:").pack(side=tk.LEFT, padx=20)
        self.type_var = tk.StringVar()
        if journal and "类型" in journal:
            self.type_var.set(journal["类型"])
        type_combo = ttk.Combobox(header_frame, textvariable=self.type_var, width=15)
        type_combo["values"] = ("交易复盘", "市场分析", "心得体会", "策略研究", "其他")
        type_combo.pack(side=tk.LEFT, padx=5)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(title_frame, text="标题:").pack(side=tk.LEFT, padx=5)
        self.title_var = tk.StringVar()
        if journal and "标题" in journal:
            self.title_var.set(journal["标题"])
        ttk.Entry(title_frame, textvariable=self.title_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 内容
        content_frame = ttk.LabelFrame(main_frame, text="内容")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(content_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_text = tk.Text(content_frame, height=15, width=70, yscrollcommand=scrollbar.set)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.content_text.yview)
        
        if journal and "内容" in journal:
            self.content_text.insert(tk.END, journal["内容"])
        
        # 设置只读模式
        if self.readonly:
            date_entry.config(state="readonly")
            type_combo.config(state="readonly")
            self.content_text.config(state="disabled")
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        if not self.readonly:
            ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="关闭", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)
    
    def on_ok(self):
        """确定按钮事件"""
        # 验证输入
        if not self.validate():
            return
        
        # 收集数据
        self.result = {
            "日期": self.date_var.get(),
            "类型": self.type_var.get(),
            "标题": self.title_var.get(),
            "内容": self.content_text.get("1.0", tk.END).strip()
        }
        
        # 关闭对话框
        self.dialog.destroy()
    
    def on_cancel(self):
        """取消按钮事件"""
        self.dialog.destroy()
    
    def validate(self):
        """验证输入"""
        if not self.title_var.get():
            messagebox.showerror("错误", "请输入日志标题")
            return False
        
        if not self.type_var.get():
            messagebox.showerror("错误", "请选择日志类型")
            return False
        
        if not self.content_text.get("1.0", tk.END).strip():
            messagebox.showerror("错误", "请输入日志内容")
            return False
        
        return True


class HeartQuoteDialog:
    """心法语录对话框"""
    
    def __init__(self, parent, title="添加心法语录", quote=None):
        """初始化对话框"""
        self.parent = parent
        self.result = None
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # 创建表单
        self.create_form(quote)
        
        # 模态显示
        self.dialog.wait_window()
    
    def create_form(self, quote=None):
        """创建表单"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 类别
        category_frame = ttk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(category_frame, text="类别:").pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar()
        if quote and "category" in quote:
            self.category_var.set(quote["category"])
        category_combo = ttk.Combobox(category_frame, textvariable=self.category_var, width=20)
        category_combo["values"] = (
            "交易系统", "风险控制", "心理控制", "顺势而为", "资金管理", 
            "概率思维", "执行力", "交易心态", "入场策略", "出场策略", 
            "趋势分析", "持续学习", "交易纪律", "复盘分析", "情绪管理"
        )
        category_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 心法内容
        quote_frame = ttk.LabelFrame(main_frame, text="心法内容")
        quote_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.quote_text = tk.Text(quote_frame, height=8, width=50)
        self.quote_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        if quote and "quote" in quote:
            self.quote_text.insert(tk.END, quote["quote"])
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)
    
    def on_ok(self):
        """确定按钮事件"""
        # 验证输入
        if not self.validate():
            return
        
        # 收集数据
        self.result = {
            "category": self.category_var.get(),
            "quote": self.quote_text.get("1.0", tk.END).strip()
        }
        
        # 关闭对话框
        self.dialog.destroy()
    
    def on_cancel(self):
        """取消按钮事件"""
        self.dialog.destroy()
    
    def validate(self):
        """验证输入"""
        if not self.category_var.get():
            messagebox.showerror("错误", "请选择心法类别")
            return False
        
        if not self.quote_text.get("1.0", tk.END).strip():
            messagebox.showerror("错误", "请输入心法内容")
            return False
        
        return True


class SettingsDialog:
    """设置对话框"""
    
    def __init__(self, parent, config):
        """初始化对话框"""
        self.parent = parent
        self.config = config.copy()
        self.result = None
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("系统设置")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # 创建表单
        self.create_form()
        
        # 模态显示
        self.dialog.wait_window()
    
    def create_form(self):
        """创建表单"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 基本设置
        basic_frame = ttk.LabelFrame(main_frame, text="基本设置")
        basic_frame.pack(fill=tk.X, pady=10)
        
        # 用户名
        name_frame = ttk.Frame(basic_frame)
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(name_frame, text="用户名:").pack(side=tk.LEFT, padx=5)
        self.username_var = tk.StringVar(value=self.config.get("user_name", "交易者"))
        ttk.Entry(name_frame, textvariable=self.username_var, width=20).pack(side=tk.LEFT, padx=5)
        
        # 资金设置
        capital_frame = ttk.LabelFrame(main_frame, text="资金设置")
        capital_frame.pack(fill=tk.X, pady=10)
        
        # 初始资金
        init_frame = ttk.Frame(capital_frame)
        init_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(init_frame, text="初始资金:").pack(side=tk.LEFT, padx=5)
        self.init_capital_var = tk.StringVar(value=str(self.config.get("initial_capital", 100000)))
        ttk.Entry(init_frame, textvariable=self.init_capital_var, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Label(init_frame, text="元").pack(side=tk.LEFT)
        
        # 风险设置
        risk_frame = ttk.LabelFrame(main_frame, text="风险设置")
        risk_frame.pack(fill=tk.X, pady=10)
        
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
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)
    
    def on_ok(self):
        """确定按钮事件"""
        # 验证输入
        if not self.validate():
            return
        
        # 收集数据
        self.result = self.config.copy()
        self.result["user_name"] = self.username_var.get()
        
        try:
            self.result["initial_capital"] = float(self.init_capital_var.get())
            self.result["risk_per_trade"] = float(self.risk_per_trade_var.get()) / 100
            self.result["max_position_size"] = float(self.max_position_var.get()) / 100
            self.result["max_drawdown_alert"] = float(self.max_drawdown_alert_var.get()) / 100
            self.result["daily_loss_limit"] = float(self.daily_loss_limit_var.get()) / 100
            self.result["profit_target"] = float(self.profit_target_var.get()) / 100
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        # 关闭对话框
        self.dialog.destroy()
    
    def on_cancel(self):
        """取消按钮事件"""
        self.dialog.destroy()
    
    def validate(self):
        """验证输入"""
        try:
            # 检查数值字段
            if float(self.init_capital_var.get()) <= 0:
                messagebox.showerror("错误", "初始资金必须大于0")
                return False
            
            if float(self.risk_per_trade_var.get()) <= 0 or float(self.risk_per_trade_var.get()) > 100:
                messagebox.showerror("错误", "每笔交易风险比例必须大于0且小于等于100")
                return False
            
            if float(self.max_position_var.get()) <= 0 or float(self.max_position_var.get()) > 100:
                messagebox.showerror("错误", "最大仓位比例必须大于0且小于等于100")
                return False
            
            if float(self.max_drawdown_alert_var.get()) <= 0 or float(self.max_drawdown_alert_var.get()) > 100:
                messagebox.showerror("错误", "最大回撤警告必须大于0且小于等于100")
                return False
            
            if float(self.daily_loss_limit_var.get()) <= 0 or float(self.daily_loss_limit_var.get()) > 100:
                messagebox.showerror("错误", "日亏损限制必须大于0且小于等于100")
                return False
            
            if float(self.profit_target_var.get()) <= 0:
                messagebox.showerror("错误", "年度收益目标必须大于0")
                return False
            
            return True
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return False


class PositionCalculatorDialog:
    """仓位计算器对话框"""
    
    def __init__(self, parent, config):
        """初始化对话框"""
        self.parent = parent
        self.config = config
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("仓位计算器")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # 创建表单
        self.create_form()
        
        # 模态显示
        self.dialog.wait_window()
    
    def create_form(self):
        """创建表单"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 账户信息
        account_frame = ttk.LabelFrame(main_frame, text="账户信息")
        account_frame.pack(fill=tk.X, pady=10)
        
        # 账户资金
        capital_frame = ttk.Frame(account_frame)
        capital_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(capital_frame, text="账户资金:").pack(side=tk.LEFT, padx=5)
        self.capital_var = tk.StringVar(value=str(self.config.get("initial_capital", 100000)))
        ttk.Entry(capital_frame, textvariable=self.capital_var, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Label(capital_frame, text="元").pack(side=tk.LEFT)
        
        # 风险比例
        risk_frame = ttk.Frame(account_frame)
        risk_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(risk_frame, text="风险比例:").pack(side=tk.LEFT, padx=5)
        self.risk_var = tk.StringVar(value=str(self.config.get("risk_per_trade", 0.02) * 100))
        ttk.Entry(risk_frame, textvariable=self.risk_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(risk_frame, text="%").pack(side=tk.LEFT)
        
        # 交易信息
        trade_frame = ttk.LabelFrame(main_frame, text="交易信息")
        trade_frame.pack(fill=tk.X, pady=10)
        
        # 标的
        symbol_frame = ttk.Frame(trade_frame)
        symbol_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(symbol_frame, text="交易标的:").pack(side=tk.LEFT, padx=5)
        self.symbol_var = tk.StringVar()
        ttk.Entry(symbol_frame, textvariable=self.symbol_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 方向
        direction_frame = ttk.Frame(trade_frame)
        direction_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(direction_frame, text="交易方向:").pack(side=tk.LEFT, padx=5)
        self.direction_var = tk.StringVar(value="买入")
        direction_combo = ttk.Combobox(direction_frame, textvariable=self.direction_var, width=10)
        direction_combo["values"] = ("买入", "卖出")
        direction_combo.pack(side=tk.LEFT, padx=5)
        
        # 入场价
        entry_frame = ttk.Frame(trade_frame)
        entry_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(entry_frame, text="入场价格:").pack(side=tk.LEFT, padx=5)
        self.entry_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.entry_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 止损价
        stop_frame = ttk.Frame(trade_frame)
        stop_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(stop_frame, text="止损价格:").pack(side=tk.LEFT, padx=5)
        self.stop_var = tk.StringVar()
        ttk.Entry(stop_frame, textvariable=self.stop_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 计算结果
        result_frame = ttk.LabelFrame(main_frame, text="计算结果")
        result_frame.pack(fill=tk.X, pady=10)
        
        # 风险金额
        risk_amount_frame = ttk.Frame(result_frame)
        risk_amount_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(risk_amount_frame, text="风险金额:").pack(side=tk.LEFT, padx=5)
        self.risk_amount_var = tk.StringVar(value="0.00 元")
        ttk.Label(risk_amount_frame, textvariable=self.risk_amount_var).pack(side=tk.LEFT, padx=5)
        
        # 止损点数
        stop_points_frame = ttk.Frame(result_frame)
        stop_points_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(stop_points_frame, text="止损点数:").pack(side=tk.LEFT, padx=5)
        self.stop_points_var = tk.StringVar(value="0")
        ttk.Label(stop_points_frame, textvariable=self.stop_points_var).pack(side=tk.LEFT, padx=5)
        
        # 建议仓位
        position_frame = ttk.Frame(result_frame)
        position_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(position_frame, text="建议仓位:").pack(side=tk.LEFT, padx=5)
        self.position_var = tk.StringVar(value="0")
        ttk.Label(position_frame, textvariable=self.position_var).pack(side=tk.LEFT, padx=5)
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="计算", command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除", command=self.clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="关闭", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def calculate(self):
        """计算仓位"""
        try:
            # 获取输入
            capital = float(self.capital_var.get())
            risk_percent = float(self.risk_var.get()) / 100
            entry_price = float(self.entry_var.get())
            stop_price = float(self.stop_var.get())
            
            # 验证输入
            if capital <= 0:
                messagebox.showerror("错误", "账户资金必须大于0")
                return
            
            if risk_percent <= 0 or risk_percent > 1:
                messagebox.showerror("错误", "风险比例必须大于0且小于等于100%")
                return
            
            if entry_price <= 0:
                messagebox.showerror("错误", "入场价格必须大于0")
                return
            
            if stop_price <= 0:
                messagebox.showerror("错误", "止损价格必须大于0")
                return
            
            if (self.direction_var.get() == "买入" and stop_price >= entry_price) or \
               (self.direction_var.get() == "卖出" and stop_price <= entry_price):
                messagebox.showerror("错误", "买入时止损价应低于入场价，卖出时止损价应高于入场价")
                return
            
            # 计算风险金额
            risk_amount = capital * risk_percent
            self.risk_amount_var.set(f"{risk_amount:.2f} 元")
            
            # 计算止损点数
            if self.direction_var.get() == "买入":
                stop_points = entry_price - stop_price
            else:
                stop_points = stop_price - entry_price
            
            self.stop_points_var.set(f"{stop_points:.4f}")
            
            # 计算建议仓位
            if stop_points > 0:
                position_size = risk_amount / stop_points
                self.position_var.set(f"{position_size:.2f}")
            else:
                self.position_var.set("无法计算")
        
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def clear(self):
        """清除输入"""
        self.symbol_var.set("")
        self.entry_var.set("")
        self.stop_var.set("")
        self.risk_amount_var.set("0.00 元")
        self.stop_points_var.set("0")
        self.position_var.set("0")
