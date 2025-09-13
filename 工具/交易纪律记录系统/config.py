#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交易纪律记录系统 - 配置管理模块
处理系统配置、交易记录、交易日志和心法语录的加载和保存
"""

import os
import json

# 配置文件路径
CONFIG_FILE = "config.json"
TRADES_FILE = "trades.json"
JOURNAL_FILE = "journal.json"
HEART_QUOTES_FILE = "heart_quotes.json"

def load_config():
    """加载配置信息"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 默认配置
            config = {
                "initial_capital": 100000,  # 初始资金
                "risk_per_trade": 0.02,     # 每笔交易风险比例
                "max_position_size": 0.3,   # 最大仓位比例
                "max_drawdown_alert": 0.1,  # 最大回撤警告
                "daily_loss_limit": 0.05,   # 日亏损限制
                "profit_target": 0.5,       # 年度收益目标
                "user_name": "交易者",      # 用户名
            }
            save_config(config)
            return config
    except Exception as e:
        print(f"加载配置出错: {e}")
        return {
            "initial_capital": 100000,
            "risk_per_trade": 0.02,
            "max_position_size": 0.3,
            "max_drawdown_alert": 0.1,
            "daily_loss_limit": 0.05,
            "profit_target": 0.5,
            "user_name": "交易者",
        }

def save_config(config):
    """保存配置信息"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存配置出错: {e}")
        return False

def load_trades():
    """加载交易记录"""
    try:
        if os.path.exists(TRADES_FILE):
            with open(TRADES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"加载交易记录出错: {e}")
        return []

def save_trades(trades):
    """保存交易记录"""
    try:
        with open(TRADES_FILE, 'w', encoding='utf-8') as f:
            json.dump(trades, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存交易记录出错: {e}")
        return False

def load_journal():
    """加载交易日志"""
    try:
        if os.path.exists(JOURNAL_FILE):
            with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"加载交易日志出错: {e}")
        return []

def save_journal(journal):
    """保存交易日志"""
    try:
        with open(JOURNAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(journal, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存交易日志出错: {e}")
        return False

def load_heart_quotes():
    """加载心法语录"""
    try:
        if os.path.exists(HEART_QUOTES_FILE):
            with open(HEART_QUOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 如果文件不存在，返回空列表
            return []
    except Exception as e:
        print(f"加载心法语录出错: {e}")
        return []

def save_heart_quotes(quotes):
    """保存心法语录"""
    try:
        with open(HEART_QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存心法语录出错: {e}")
        return False

def ensure_config_files():
    """确保所有配置文件存在"""
    # 确保配置文件存在
    if not os.path.exists(CONFIG_FILE):
        # 创建默认配置
        config = {
            "initial_capital": 100000,  # 初始资金
            "risk_per_trade": 0.02,     # 每笔交易风险比例
            "max_position_size": 0.3,   # 最大仓位比例
            "max_drawdown_alert": 0.1,  # 最大回撤警告
            "daily_loss_limit": 0.05,   # 日亏损限制
            "profit_target": 0.5,       # 年度收益目标
            "user_name": "交易者",      # 用户名
        }
        save_config(config)
    
    # 确保交易记录文件存在
    if not os.path.exists(TRADES_FILE):
        save_trades([])
    
    # 确保交易日志文件存在
    if not os.path.exists(JOURNAL_FILE):
        save_journal([])
    
    # 确保心法语录文件存在
    if not os.path.exists(HEART_QUOTES_FILE):
        # 创建默认心法语录
        default_quotes = [
            {"category": "交易系统", "quote": "完整的交易系统必须包含：入场、出场、止损、资金管理和交易心理。缺一不可。"},
            {"category": "风险控制", "quote": "风险第一，利润第二。没有风险控制，就没有长期盈利。"},
            {"category": "心理控制", "quote": "交易是一场心理游戏，控制好情绪比预测市场更重要。"}
        ]
        save_heart_quotes(default_quotes)
