#!/bin/bash

echo "图片转文字工具 - 图形界面版"
echo "==============================="

# 检查是否安装了Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未检测到Python，请先安装Python3"
    exit 1
fi

# 检查是否安装了必要的库
echo "正在检查必要的Python库..."
python3 -c "import pytesseract" &> /dev/null
if [ $? -ne 0 ]; then
    echo "正在安装pytesseract库..."
    pip3 install pytesseract
fi

python3 -c "import PIL" &> /dev/null
if [ $? -ne 0 ]; then
    echo "正在安装Pillow库..."
    pip3 install Pillow
fi

python3 -c "import tkinter" &> /dev/null
if [ $? -ne 0 ]; then
    echo "错误: 未检测到tkinter库，这是Python的标准库"
    echo "在Ubuntu/Debian上，可以使用: sudo apt-get install python3-tk"
    echo "在Fedora上，可以使用: sudo dnf install python3-tkinter"
    echo "在macOS上，tkinter应该已经包含在Python安装中"
    exit 1
fi

echo ""
echo "注意: 此工具需要安装Tesseract OCR引擎"
echo "如果尚未安装，请使用系统包管理器安装:"
echo "- Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim"
echo "- Fedora: sudo dnf install tesseract tesseract-langpack-chi-sim"
echo "- macOS: brew install tesseract tesseract-lang"
echo ""

echo "启动图片转文字工具..."
python3 "$(dirname "$0")/images_to_text.py"

echo ""
read -p "按回车键继续..."