#!/bin/bash
echo "正在启动交易纪律记录系统..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "创建虚拟环境失败，请确保已安装Python 3.6或更高版本。"
        read -p "按回车键继续..."
        exit 1
    fi
fi

# 激活虚拟环境
echo "正在激活虚拟环境..."
source venv/bin/activate

# 检查依赖是否安装
pip list | grep -E "pandas|matplotlib|numpy" > /dev/null
if [ $? -ne 0 ]; then
    echo "正在安装必要的依赖库..."
    pip install pandas matplotlib numpy
    if [ $? -ne 0 ]; then
        echo "安装依赖库失败，请检查网络连接。"
        read -p "按回车键继续..."
        exit 1
    fi
fi

# 运行程序
echo "正在启动程序..."
python main.py

# 检查程序是否正常退出
if [ $? -ne 0 ]; then
    echo "程序运行失败，请检查错误信息。"
    read -p "按回车键继续..."
fi

# 退出虚拟环境
deactivate
