#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交易纪律记录系统 - 工具函数模块
提供各种辅助功能
"""

import os
import json
import datetime
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.font_manager as fm

# 配置matplotlib支持中文显示
def configure_matplotlib_chinese():
    """配置matplotlib支持中文显示"""
    try:
        # 尝试查找系统中的中文字体
        chinese_fonts = []
        
        # 常见的中文字体名称
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun', 'STSong', 'STFangsong', 'STKaiti', 
                     'AR PL UMing CN', 'AR PL UKai CN', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei',
                     'Hiragino Sans GB', 'PingFang SC', 'Heiti SC', 'Source Han Sans CN', 'Noto Sans CJK SC']
        
        # 查找系统中是否有这些字体
        for font_name in font_names:
            try:
                # 允许回退到默认字体
                font_path = fm.findfont(fm.FontProperties(family=font_name))
                if font_path and 'ttf' in font_path.lower():
                    chinese_fonts.append(font_name)
            except Exception:
                continue
        
        # 如果找到中文字体，设置为默认字体
        if chinese_fonts:
            plt.rcParams['font.family'] = chinese_fonts[0]
            print(f"已设置matplotlib字体为: {chinese_fonts[0]}")
        else:
            # 设置默认字体并启用Unicode支持
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            print("未找到合适的中文字体，使用系统默认字体")
    
    except Exception as e:
        print(f"配置matplotlib中文字体时出错: {e}")
        # 确保即使出错也能使用默认字体
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

def calculate_statistics(trades):
    """计算交易统计数据"""
    if not trades:
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0,
            "avg_profit": 0,
            "avg_loss": 0,
            "profit_factor": 0,
            "expectancy": 0,
            "max_drawdown": 0,
            "profit_loss_ratio": 0
        }
    
    # 总交易次数
    total_trades = len(trades)
    
    # 盈利和亏损交易
    winning_trades = [t for t in trades if float(t.get("盈亏", 0)) > 0]
    losing_trades = [t for t in trades if float(t.get("盈亏", 0)) < 0]
    
    # 胜率
    win_count = len(winning_trades)
    lose_count = len(losing_trades)
    win_rate = win_count / total_trades if total_trades > 0 else 0
    
    # 平均盈利和亏损
    avg_profit = sum(float(t.get("盈亏", 0)) for t in winning_trades) / win_count if win_count > 0 else 0
    avg_loss = abs(sum(float(t.get("盈亏", 0)) for t in losing_trades) / lose_count) if lose_count > 0 else 0
    
    # 盈亏比
    profit_factor = avg_profit / avg_loss if avg_loss > 0 else 0
    
    # 期望值
    expectancy = (win_rate * avg_profit) - ((1 - win_rate) * avg_loss)
    
    # 最大回撤
    # 按日期排序交易记录
    sorted_trades = sorted(trades, key=lambda x: x.get("日期", ""))
    
    # 计算资金曲线
    capital = []
    current = 0
    for trade in sorted_trades:
        current += float(trade.get("盈亏", 0))
        capital.append(current)
    
    # 计算最大回撤
    max_drawdown = 0
    peak = 0
    for value in capital:
        if value > peak:
            peak = value
        drawdown = peak - value
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    return {
        "total_trades": total_trades,
        "winning_trades": win_count,
        "losing_trades": lose_count,
        "win_rate": win_rate,
        "avg_profit": avg_profit,
        "avg_loss": avg_loss,
        "profit_factor": profit_factor,
        "expectancy": expectancy,
        "max_drawdown": max_drawdown,
        "profit_loss_ratio": profit_factor
    }

def create_pnl_chart(trades, figure):
    """创建盈亏分布图"""
    if not trades:
        ax = figure.add_subplot(111)
        ax.text(0.5, 0.5, "没有交易数据", ha="center", va="center")
        ax.set_xticks([])
        ax.set_yticks([])
        return
    
    # 提取盈亏数据
    pnl_data = [float(trade.get("盈亏", 0)) for trade in trades]
    
    # 创建图表
    ax = figure.add_subplot(111)
    ax.hist(pnl_data, bins=20, color="skyblue", edgecolor="black", alpha=0.7)
    ax.axvline(x=0, color="red", linestyle="--")
    
    # 设置标题和标签
    ax.set_title("盈亏分布")
    ax.set_xlabel("盈亏金额")
    ax.set_ylabel("交易次数")
    
    # 添加网格
    ax.grid(True, linestyle="--", alpha=0.7)

def create_winrate_chart(trades, figure):
    """创建胜率统计图"""
    if not trades:
        ax = figure.add_subplot(111)
        ax.text(0.5, 0.5, "没有交易数据", ha="center", va="center")
        ax.set_xticks([])
        ax.set_yticks([])
        return
    
    # 计算胜率
    stats = calculate_statistics(trades)
    win_count = stats["winning_trades"]
    lose_count = stats["losing_trades"]
    
    # 创建饼图
    ax = figure.add_subplot(111)
    ax.pie([win_count, lose_count], labels=["盈利", "亏损"], 
           autopct="%1.1f%%", startangle=90, colors=["lightgreen", "lightcoral"])
    ax.axis("equal")  # 保持饼图为圆形
    
    # 设置标题
    ax.set_title("交易胜率")

def create_capital_chart(trades, initial_capital, figure):
    """创建资金曲线图"""
    if not trades:
        ax = figure.add_subplot(111)
        ax.text(0.5, 0.5, "没有交易数据", ha="center", va="center")
        ax.set_xticks([])
        ax.set_yticks([])
        return
    
    # 按日期排序交易记录
    sorted_trades = sorted(trades, key=lambda x: x.get("日期", ""))
    
    # 计算资金曲线
    dates = []
    capital = [initial_capital]
    current = initial_capital
    
    for trade in sorted_trades:
        dates.append(trade.get("日期", ""))
        current += float(trade.get("盈亏", 0))
        capital.append(current)
    
    # 创建图表
    ax = figure.add_subplot(111)
    ax.plot(range(len(capital)), capital, marker="o", markersize=4, linewidth=2)
    
    # 设置标题和标签
    ax.set_title("资金曲线")
    ax.set_xlabel("交易次数")
    ax.set_ylabel("资金")
    
    # 添加网格
    ax.grid(True, linestyle="--", alpha=0.7)
    
    # 设置x轴刻度
    if len(capital) > 10:
        step = len(capital) // 10
        ax.set_xticks(range(0, len(capital), step))
        ax.set_xticklabels([f"{i}" for i in range(0, len(capital), step)])
    else:
        ax.set_xticks(range(len(capital)))
        ax.set_xticklabels([f"{i}" for i in range(len(capital))])

def generate_report(trades, config, filename):
    """生成交易报告"""
    if not trades:
        return False, "没有交易数据，无法生成报告"
    
    try:
        # 计算统计数据
        stats = calculate_statistics(trades)
        
        # 创建HTML报告
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>交易报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .positive {{ color: green; }}
                .negative {{ color: red; }}
                .summary {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>交易报告</h1>
            <p>生成日期: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>用户: {config.get('user_name', '交易者')}</p>
            
            <div class="summary">
                <h2>交易概览</h2>
                <p>初始资金: {config.get('initial_capital', 100000):,.2f} 元</p>
                <p>当前资金: {config.get('initial_capital', 100000) + sum(float(t.get('盈亏', 0)) for t in trades):,.2f} 元</p>
                <p>总收益率: {(sum(float(t.get('盈亏', 0)) for t in trades) / config.get('initial_capital', 100000) * 100):.2f}%</p>
                <p>总交易次数: {stats['total_trades']}</p>
                <p>胜率: {stats['win_rate'] * 100:.1f}%</p>
                <p>盈亏比: {stats['profit_loss_ratio']:.2f}</p>
                <p>最大回撤: {stats['max_drawdown']:,.2f} 元 ({stats['max_drawdown'] / config.get('initial_capital', 100000) * 100:.2f}%)</p>
            </div>
            
            <h2>交易统计</h2>
            <table>
                <tr>
                    <th>指标</th>
                    <th>数值</th>
                </tr>
                <tr>
                    <td>总交易次数</td>
                    <td>{stats['total_trades']}</td>
                </tr>
                <tr>
                    <td>盈利交易</td>
                    <td>{stats['winning_trades']}</td>
                </tr>
                <tr>
                    <td>亏损交易</td>
                    <td>{stats['losing_trades']}</td>
                </tr>
                <tr>
                    <td>胜率</td>
                    <td>{stats['win_rate'] * 100:.1f}%</td>
                </tr>
                <tr>
                    <td>平均盈利</td>
                    <td>{stats['avg_profit']:,.2f} 元</td>
                </tr>
                <tr>
                    <td>平均亏损</td>
                    <td>{stats['avg_loss']:,.2f} 元</td>
                </tr>
                <tr>
                    <td>盈亏比</td>
                    <td>{stats['profit_loss_ratio']:.2f}</td>
                </tr>
                <tr>
                    <td>期望值</td>
                    <td>{stats['expectancy']:,.2f} 元</td>
                </tr>
                <tr>
                    <td>最大回撤</td>
                    <td>{stats['max_drawdown']:,.2f} 元</td>
                </tr>
            </table>
            
            <h2>交易记录</h2>
            <table>
                <tr>
                    <th>日期</th>
                    <th>时间</th>
                    <th>标的</th>
                    <th>方向</th>
                    <th>价格</th>
                    <th>数量</th>
                    <th>止损价</th>
                    <th>目标价</th>
                    <th>结果</th>
                    <th>盈亏</th>
                    <th>备注</th>
                </tr>
        """
        
        # 添加交易记录
        for trade in sorted(trades, key=lambda x: x.get("日期", "")):
            pnl = float(trade.get("盈亏", 0))
            pnl_class = "positive" if pnl > 0 else "negative" if pnl < 0 else ""
            
            html += f"""
                <tr>
                    <td>{trade.get('日期', '')}</td>
                    <td>{trade.get('时间', '')}</td>
                    <td>{trade.get('标的', '')}</td>
                    <td>{trade.get('方向', '')}</td>
                    <td>{trade.get('价格', '')}</td>
                    <td>{trade.get('数量', '')}</td>
                    <td>{trade.get('止损价', '')}</td>
                    <td>{trade.get('目标价', '')}</td>
                    <td>{trade.get('结果', '')}</td>
                    <td class="{pnl_class}">{pnl:,.2f}</td>
                    <td>{trade.get('备注', '')}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <h2>总结与建议</h2>
            <p>根据您的交易记录，以下是一些建议：</p>
            <ul>
        """
        
        # 添加建议
        if stats['win_rate'] < 0.4:
            html += "<li>您的胜率较低，建议检查交易系统或策略是否需要调整。</li>"
        
        if stats['profit_loss_ratio'] < 1:
            html += "<li>您的盈亏比小于1，意味着平均亏损大于平均盈利，建议调整止损和止盈策略。</li>"
        
        if stats['max_drawdown'] / config.get('initial_capital', 100000) > 0.2:
            html += "<li>您的最大回撤较大，建议加强风险控制。</li>"
        
        if stats['expectancy'] <= 0:
            html += "<li>您的交易期望值为负，长期来看可能会亏损，建议重新评估交易系统。</li>"
        
        html += """
            </ul>
            
            <p>记住：交易是一场心理游戏，控制好情绪比预测市场更重要。</p>
            
            <footer>
                <p>交易纪律记录系统 - 基于Tony交易心法</p>
                <p>报告生成时间: {}</p>
            </footer>
        </body>
        </html>
        """.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # 保存HTML报告
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return True, f"交易报告已生成: {filename}"
    
    except Exception as e:
        return False, f"生成报告失败: {e}"

def get_random_heart_quote(quotes):
    """获取随机心法语录"""
    if not quotes:
        return {"category": "心理控制", "quote": "交易是一场心理游戏，控制好情绪比预测市场更重要。"}
    
    return random.choice(quotes)

def check_risk_warnings(trades, config):
    """检查风险警告"""
    warnings = []
    
    if not trades:
        return warnings
    
    # 计算统计数据
    stats = calculate_statistics(trades)
    
    # 检查最大回撤
    max_drawdown_pct = stats["max_drawdown"] / config.get("initial_capital", 100000)
    max_drawdown_alert = config.get("max_drawdown_alert", 0.1)
    
    if max_drawdown_pct > max_drawdown_alert:
        warnings.append(f"警告: 最大回撤 ({max_drawdown_pct:.2%}) 超过警戒线 ({max_drawdown_alert:.2%})")
    
    # 检查日亏损
    # 按日期分组计算每日盈亏
    daily_pnl = {}
    for trade in trades:
        date = trade.get("日期", "")
        pnl = float(trade.get("盈亏", 0))
        
        if date in daily_pnl:
            daily_pnl[date] += pnl
        else:
            daily_pnl[date] = pnl
    
    # 检查是否有日亏损超过限制
    daily_loss_limit = config.get("daily_loss_limit", 0.05) * config.get("initial_capital", 100000)
    
    for date, pnl in daily_pnl.items():
        if pnl < -daily_loss_limit:
            warnings.append(f"警告: {date} 日亏损 ({-pnl:.2f} 元) 超过日亏损限制 ({daily_loss_limit:.2f} 元)")
    
    # 检查连续亏损
    consecutive_losses = 0
    max_consecutive_losses = 0
    
    for trade in sorted(trades, key=lambda x: (x.get("日期", ""), x.get("时间", ""))):
        pnl = float(trade.get("盈亏", 0))
        
        if pnl < 0:
            consecutive_losses += 1
            max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
        else:
            consecutive_losses = 0
    
    if max_consecutive_losses >= 5:
        warnings.append(f"警告: 检测到连续 {max_consecutive_losses} 次亏损交易，请检查交易系统或暂停交易")
    
    return warnings