#!/bin/bash

echo "PDF转图片工具 - 图形界面版"
echo "==============================="

# 检查是否安装了Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未检测到Python，请先安装Python3"
    exit 1
fi

# 检查是否安装了必要的库
echo "正在检查必要的Python库..."
python3 -c "import fitz" &> /dev/null
if [ $? -ne 0 ]; then
    echo "正在安装PyMuPDF库..."
    pip3 install PyMuPDF
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
echo "启动PDF转图片工具..."
python3 "$(dirname "$0")/pdf_to_images.py"

echo ""
read -p "按回车键继续..."
