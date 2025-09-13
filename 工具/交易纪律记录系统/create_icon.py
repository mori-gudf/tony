#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建简单的应用图标
"""

import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    """创建简单的应用图标"""
    try:
        # 创建一个128x128的图像
        img = Image.new('RGBA', (128, 128), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制圆形背景
        draw.ellipse((10, 10, 118, 118), fill=(0, 120, 212))
        
        # 绘制文字
        try:
            # 尝试加载字体
            font = ImageFont.truetype("Arial", 60)
        except:
            # 如果无法加载字体，使用默认字体
            font = ImageFont.load_default()
        
        # 绘制文字
        draw.text((40, 30), "T", fill=(255, 255, 255), font=font)
        
        # 确保assets目录存在
        os.makedirs("assets", exist_ok=True)
        
        # 保存图像
        img.save("assets/icon.png")
        print("图标已创建: assets/icon.png")
    
    except Exception as e:
        print(f"创建图标出错: {e}")
        print("请手动创建图标文件")

if __name__ == "__main__":
    create_icon()