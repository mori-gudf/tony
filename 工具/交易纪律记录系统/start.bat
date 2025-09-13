@echo off
echo 正在启动交易纪律记录系统...
python main.py
if errorlevel 1 (
    echo 启动失败，请检查Python环境和依赖库是否正确安装。
    echo 需要Python 3.6或更高版本，以及pandas、matplotlib和numpy库。
    pause
)