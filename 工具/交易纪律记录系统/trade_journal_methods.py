#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交易纪律记录系统 - 主应用类方法补充
添加TradeJournalApp类中缺失的方法
"""

import os
import sys
import json
import datetime
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import pandas as pd
import numpy as np
from utils import calculate_statistics, create_pnl_chart, create_winrate_chart, create_capital_chart, generate_report, get_random_heart_quote, check_risk_warnings

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

# 添加到TradeJournalApp类中的方法
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
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
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
            
            dialog = TradeDialog(self.root, "编辑交易记录", trade)
            if dialog.result:
                self.trades[i] = dialog.result
                save_trades(self.trades)
                self.refresh_trades()
                self.update_statistics()
                self.update_capital_chart()
                self.update_profit_label()
                if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                    self.status_label.config(text="交易记录已更新")
            break

def delete_trade(self):
    """删除交易记录"""
    selected = self.trades_tree.selection()
    if not selected:
        messagebox.showinfo("提示", "请先选择要删除的交易记录")
        return
    
    if messagebox.askyesno("确认", "确定要删除选中的交易记录吗？"):
        item = self.trades_tree.item(selected[0])
        values = item["values"]
        
        # 查找对应的交易记录
        for i, trade in enumerate(self.trades):
            if (trade.get("日期") == values[0] and 
                trade.get("时间") == values[1] and 
                trade.get("标的") == values[2]):
                
                del self.trades[i]
                save_trades(self.trades)
                self.refresh_trades()
                self.update_statistics()
                self.update_capital_chart()
                self.update_profit_label()
                if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                    self.status_label.config(text="交易记录已删除")
                break

def refresh_trades(self):
    """刷新交易记录"""
    # 清空表格
    for item in self.trades_tree.get_children():
        self.trades_tree.delete(item)
    
    # 添加交易记录
    for trade in self.trades:
        values = [
            trade.get("日期", ""),
            trade.get("时间", ""),
            trade.get("标的", ""),
            trade.get("方向", ""),
            trade.get("价格", ""),
            trade.get("数量", ""),
            trade.get("止损价", ""),
            trade.get("目标价", ""),
            trade.get("结果", ""),
            trade.get("盈亏", ""),
            trade.get("备注", "")
        ]
        self.trades_tree.insert("", tk.END, values=values)
    
    # 检查status_label是否已创建，如果已创建则更新状态
    if hasattr(self, 'status_label') and self.status_label.winfo_exists():
        self.status_label.config(text="交易记录已刷新")

def export_trades_csv(self):
    """导出交易记录为CSV文件"""
    if not self.trades:
        messagebox.showinfo("提示", "没有交易记录可导出")
        return
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
        title="导出交易记录"
    )
    
    if filename:
        try:
            df = pd.DataFrame(self.trades)
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            messagebox.showinfo("成功", f"交易记录已导出到 {filename}")
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                self.status_label.config(text="交易记录已导出")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")

def calculate_current_capital(self):
    """计算当前资金"""
    initial_capital = self.config.get("initial_capital", 100000)
    total_pnl = sum(float(trade.get("盈亏", 0)) for trade in self.trades)
    return initial_capital + total_pnl

def update_profit_label(self):
    """更新盈亏标签"""
    total_pnl = sum(float(trade.get("盈亏", 0)) for trade in self.trades)
    if total_pnl >= 0:
        self.profit_label.config(text=f"总盈亏: +{total_pnl:,.2f} 元", foreground="green")
    else:
        self.profit_label.config(text=f"总盈亏: {total_pnl:,.2f} 元", foreground="red")

def update_total_return(self):
    """更新总收益率"""
    initial_capital = self.config.get("initial_capital", 100000)
    current_capital = self.calculate_current_capital()
    total_return = (current_capital - initial_capital) / initial_capital * 100
    
    if total_return >= 0:
        self.total_return_var.set(f"+{total_return:.2f}%")
    else:
        self.total_return_var.set(f"{total_return:.2f}%")

def update_current_position(self):
    """更新当前仓位"""
    # 这里简化处理，实际应根据未平仓交易计算
    self.current_position_var.set("0.00%")

def update_max_drawdown(self):
    """更新最大回撤"""
    if not self.trades:
        self.max_drawdown_var.set("0.00%")
        return
    
    stats = calculate_statistics(self.trades)
    max_drawdown = stats["max_drawdown"]
    initial_capital = self.config.get("initial_capital", 100000)
    max_drawdown_pct = max_drawdown / initial_capital * 100
    
    self.max_drawdown_var.set(f"{max_drawdown_pct:.2f}%")

def update_profit_loss_ratio(self):
    """更新盈亏比"""
    if not self.trades:
        self.profit_loss_ratio_var.set("0.00")
        return
    
    stats = calculate_statistics(self.trades)
    self.profit_loss_ratio_var.set(f"{stats['profit_loss_ratio']:.2f}")

def update_capital_chart(self):
    """更新资金曲线图"""
    self.capital_figure.clear()
    if self.trades:
        create_capital_chart(self.trades, self.config.get("initial_capital", 100000), self.capital_figure)
    else:
        ax = self.capital_figure.add_subplot(111)
        ax.text(0.5, 0.5, "没有交易数据", ha="center", va="center")
        ax.set_xticks([])
        ax.set_yticks([])
    
    self.capital_canvas.draw()

def open_position_calculator(self):
    """打开仓位计算器"""
    dialog = PositionCalculatorDialog(self.root, self.config)

def add_journal(self):
    """添加交易日志"""
    dialog = JournalDialog(self.root, "添加交易日志")
    if dialog.result:
        self.journal.append(dialog.result)
        save_journal(self.journal)
        self.refresh_journal()
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text="交易日志已添加")

def view_journal(self, event=None):
    """查看交易日志"""
    selected = self.journal_tree.selection()
    if not selected:
        messagebox.showinfo("提示", "请先选择要查看的交易日志")
        return
    
    item = self.journal_tree.item(selected[0])
    values = item["values"]
    
    # 查找对应的日志
    for journal in self.journal:
        if (journal.get("日期") == values[0] and 
            journal.get("标题") == values[1] and 
            journal.get("类型") == values[2]):
            
            dialog = JournalDialog(self.root, "查看交易日志", journal, readonly=True)
            break

def delete_journal(self):
    """删除交易日志"""
    selected = self.journal_tree.selection()
    if not selected:
        messagebox.showinfo("提示", "请先选择要删除的交易日志")
        return
    
    if messagebox.askyesno("确认", "确定要删除选中的交易日志吗？"):
        item = self.journal_tree.item(selected[0])
        values = item["values"]
        
        # 查找对应的日志
        for i, journal in enumerate(self.journal):
            if (journal.get("日期") == values[0] and 
                journal.get("标题") == values[1] and 
                journal.get("类型") == values[2]):
                
                del self.journal[i]
                save_journal(self.journal)
                self.refresh_journal()
                if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                    self.status_label.config(text="交易日志已删除")
                break

def refresh_journal(self):
    """刷新交易日志"""
    # 清空表格
    for item in self.journal_tree.get_children():
        self.journal_tree.delete(item)
    
    # 添加日志
    for journal in self.journal:
        values = [
            journal.get("日期", ""),
            journal.get("标题", ""),
            journal.get("类型", "")
        ]
        self.journal_tree.insert("", tk.END, values=values)
    
    # 检查status_label是否已创建，如果已创建则更新状态
    if hasattr(self, 'status_label') and self.status_label.winfo_exists():
        self.status_label.config(text="交易日志已刷新")

def update_statistics(self):
    """更新统计数据"""
    if not self.trades:
        return
    
    stats = calculate_statistics(self.trades)
    
    # 更新统计信息
    self.total_trades_var.set(str(stats["total_trades"]))
    self.winning_trades_var.set(str(stats["winning_trades"]))
    self.losing_trades_var.set(str(stats["losing_trades"]))
    self.win_rate_var.set(f"{stats['win_rate'] * 100:.1f}%")
    
    self.avg_profit_var.set(f"{stats['avg_profit']:.2f} 元")
    self.avg_loss_var.set(f"{stats['avg_loss']:.2f} 元")
    self.profit_factor_var.set(f"{stats['profit_factor']:.2f}")
    self.expectancy_var.set(f"{stats['expectancy']:.2f} 元")
    
    # 更新图表
    self.pnl_figure.clear()
    create_pnl_chart(self.trades, self.pnl_figure)
    self.pnl_canvas.draw()
    
    self.winrate_figure.clear()
    create_winrate_chart(self.trades, self.winrate_figure)
    self.winrate_canvas.draw()
    
    if hasattr(self, 'status_label') and self.status_label.winfo_exists():
        self.status_label.config(text="统计数据已更新")

def generate_report(self):
    """生成交易报告"""
    if not self.trades:
        messagebox.showinfo("提示", "没有交易记录，无法生成报告")
        return
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".html",
        filetypes=[("HTML文件", "*.html"), ("所有文件", "*.*")],
        title="保存交易报告",
        initialfile="交易报告.html"
    )
    
    if filename:
        success, message = generate_report(self.trades, self.config, filename)
        if success:
            messagebox.showinfo("成功", message)
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                self.status_label.config(text="交易报告已生成")
            
            # 尝试打开报告
            try:
                import webbrowser
                webbrowser.open(filename)
            except:
                pass
        else:
            messagebox.showerror("错误", message)

def add_heart_quote(self):
    """添加心法语录"""
    dialog = HeartQuoteDialog(self.root, "添加心法语录")
    if dialog.result:
        self.heart_quotes.append(dialog.result)
        save_heart_quotes(self.heart_quotes)
        self.refresh_heart_quotes()
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text="心法语录已添加")

def edit_heart_quote(self):
    """编辑心法语录"""
    selected = self.heart_tree.selection()
    if not selected:
        messagebox.showinfo("提示", "请先选择要编辑的心法语录")
        return
    
    item = self.heart_tree.item(selected[0])
    values = item["values"]
    
    # 查找对应的心法语录
    for i, quote in enumerate(self.heart_quotes):
        if (quote.get("category") == values[0] and 
            quote.get("quote") == values[1]):
            
            dialog = HeartQuoteDialog(self.root, "编辑心法语录", quote)
            if dialog.result:
                self.heart_quotes[i] = dialog.result
                save_heart_quotes(self.heart_quotes)
                self.refresh_heart_quotes()
                if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                    self.status_label.config(text="心法语录已更新")
            break

def delete_heart_quote(self):
    """删除心法语录"""
    selected = self.heart_tree.selection()
    if not selected:
        messagebox.showinfo("提示", "请先选择要删除的心法语录")
        return
    
    if messagebox.askyesno("确认", "确定要删除选中的心法语录吗？"):
        item = self.heart_tree.item(selected[0])
        values = item["values"]
        
        # 查找对应的心法语录
        for i, quote in enumerate(self.heart_quotes):
            if (quote.get("category") == values[0] and 
                quote.get("quote") == values[1]):
                
                del self.heart_quotes[i]
                save_heart_quotes(self.heart_quotes)
                self.refresh_heart_quotes()
                if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                    self.status_label.config(text="心法语录已删除")
                break

def refresh_heart_quotes(self):
    """刷新心法语录"""
    # 清空表格
    for item in self.heart_tree.get_children():
        self.heart_tree.delete(item)
    
    # 添加心法语录
    for quote in self.heart_quotes:
        values = [
            quote.get("category", ""),
            quote.get("quote", "")
        ]
        self.heart_tree.insert("", tk.END, values=values)
    
    # 检查status_label是否已创建，如果已创建则更新状态
    if hasattr(self, 'status_label') and self.status_label.winfo_exists():
        self.status_label.config(text="心法语录已刷新")

def show_daily_heart_quote(self):
    """显示每日心法提示"""
    if self.heart_quotes:
        quote = get_random_heart_quote(self.heart_quotes)
        self.daily_quote_var.set(f"{quote['quote']}\n\n—— {quote['category']}")
    else:
        self.daily_quote_var.set("交易是一场心理游戏，控制好情绪比预测市场更重要。\n\n—— 心理控制")

def save_settings(self):
    """保存设置"""
    try:
        # 获取设置值
        user_name = self.username_var.get()
        initial_capital = float(self.init_capital_var.get())
        risk_per_trade = float(self.risk_per_trade_var.get()) / 100
        max_position_size = float(self.max_position_var.get()) / 100
        max_drawdown_alert = float(self.max_drawdown_alert_var.get()) / 100
        daily_loss_limit = float(self.daily_loss_limit_var.get()) / 100
        profit_target = float(self.profit_target_var.get()) / 100
        
        # 验证设置
        if initial_capital <= 0:
            messagebox.showerror("错误", "初始资金必须大于0")
            return
        
        if risk_per_trade <= 0 or risk_per_trade > 1:
            messagebox.showerror("错误", "每笔交易风险比例必须大于0且小于等于100%")
            return
        
        if max_position_size <= 0 or max_position_size > 1:
            messagebox.showerror("错误", "最大仓位比例必须大于0且小于等于100%")
            return
        
        if max_drawdown_alert <= 0 or max_drawdown_alert > 1:
            messagebox.showerror("错误", "最大回撤警告必须大于0且小于等于100%")
            return
        
        if daily_loss_limit <= 0 or daily_loss_limit > 1:
            messagebox.showerror("错误", "日亏损限制必须大于0且小于等于100%")
            return
        
        if profit_target <= 0:
            messagebox.showerror("错误", "年度收益目标必须大于0")
            return
        
        # 更新配置
        self.config["user_name"] = user_name
        self.config["initial_capital"] = initial_capital
        self.config["risk_per_trade"] = risk_per_trade
        self.config["max_position_size"] = max_position_size
        self.config["max_drawdown_alert"] = max_drawdown_alert
        self.config["daily_loss_limit"] = daily_loss_limit
        self.config["profit_target"] = profit_target
        
        # 保存配置
        save_config(self.config)
        
        # 更新界面
        self.initial_capital_var.set(f"{initial_capital:,.2f} 元")
        self.update_total_return()
        self.update_capital_chart()
        self.update_profit_label()
        
        messagebox.showinfo("成功", "设置已保存")
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text="设置已保存")
    
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def reset_settings(self):
    """重置设置"""
    if messagebox.askyesno("确认", "确定要重置所有设置吗？"):
        # 默认配置
        self.config = {
            "initial_capital": 100000,
            "risk_per_trade": 0.02,
            "max_position_size": 0.3,
            "max_drawdown_alert": 0.1,
            "daily_loss_limit": 0.05,
            "profit_target": 0.5,
            "user_name": "交易者",
        }
        
        # 保存配置
        save_config(self.config)
        
        # 更新界面
        self.username_var.set(self.config["user_name"])
        self.init_capital_var.set(str(self.config["initial_capital"]))
        self.risk_per_trade_var.set(str(self.config["risk_per_trade"] * 100))
        self.max_position_var.set(str(self.config["max_position_size"] * 100))
        self.max_drawdown_alert_var.set(str(self.config["max_drawdown_alert"] * 100))
        self.daily_loss_limit_var.set(str(self.config["daily_loss_limit"] * 100))
        self.profit_target_var.set(str(self.config["profit_target"] * 100))
        
        self.initial_capital_var.set(f"{self.config['initial_capital']:,.2f} 元")
        self.update_total_return()
        self.update_capital_chart()
        self.update_profit_label()
        
        messagebox.showinfo("成功", "设置已重置")
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text="设置已重置")

def backup_data(self):
    """备份数据"""
    filename = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")],
        title="备份数据"
    )
    
    if filename:
        try:
            import zipfile
            import tempfile
            
            with zipfile.ZipFile(filename, "w") as zipf:
                # 添加配置文件
                if os.path.exists("config.json"):
                    zipf.write("config.json")
                
                # 添加交易记录
                if os.path.exists("trades.json"):
                    zipf.write("trades.json")
                
                # 添加交易日志
                if os.path.exists("journal.json"):
                    zipf.write("journal.json")
                
                # 添加心法语录
                if os.path.exists("heart_quotes.json"):
                    zipf.write("heart_quotes.json")
            
            messagebox.showinfo("成功", f"数据已备份到 {filename}")
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                self.status_label.config(text="数据已备份")
        
        except Exception as e:
            messagebox.showerror("错误", f"备份失败: {e}")

def restore_data(self):
    """恢复数据"""
    filename = filedialog.askopenfilename(
        filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")],
        title="恢复数据"
    )
    
    if filename:
        try:
            import zipfile
            import tempfile
            
            with zipfile.ZipFile(filename, "r") as zipf:
                # 解压所有文件
                zipf.extractall()
            
            # 重新加载数据
            self.config = load_config()
            self.trades = load_trades()
            self.journal = load_journal()
            self.heart_quotes = load_heart_quotes()
            
            # 更新界面
            self.refresh_trades()
            self.refresh_journal()
            self.refresh_heart_quotes()
            self.update_statistics()
            self.update_capital_chart()
            self.update_profit_label()
            
            # 更新设置界面
            self.username_var.set(self.config.get("user_name", "交易者"))
            self.init_capital_var.set(str(self.config.get("initial_capital", 100000)))
            self.risk_per_trade_var.set(str(self.config.get("risk_per_trade", 0.02) * 100))
            self.max_position_var.set(str(self.config.get("max_position_size", 0.3) * 100))
            self.max_drawdown_alert_var.set(str(self.config.get("max_drawdown_alert", 0.1) * 100))
            self.daily_loss_limit_var.set(str(self.config.get("daily_loss_limit", 0.05) * 100))
            self.profit_target_var.set(str(self.config.get("profit_target", 0.5) * 100))
            
            self.initial_capital_var.set(f"{self.config.get('initial_capital', 100000):,.2f} 元")
            
            messagebox.showinfo("成功", "数据已恢复")
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                self.status_label.config(text="数据已恢复")
        
        except Exception as e:
            messagebox.showerror("错误", f"恢复失败: {e}")

def check_risk_warnings(self):
    """检查风险警告"""
    # 从utils模块导入的check_risk_warnings函数
    warnings = check_risk_warnings(self.trades, self.config)
    
    if warnings:
        message = "\n".join(warnings)
        messagebox.showwarning("风险警告", message)
    
    return warnings

def display_risk_warnings(self):
    """显示风险警告"""
    # 调用check_risk_warnings方法
    self.check_risk_warnings()
