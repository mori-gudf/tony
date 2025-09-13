@echo off
echo PDF转图片工具 - 图形界面版
echo ===============================

REM 检查是否安装了Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python，请先安装Python
    echo 可以从 https://www.python.org/downloads/ 下载安装
    pause
    exit /b
)

REM 检查是否安装了必要的库
echo 正在检查必要的Python库...
python -c "import fitz" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装PyMuPDF库...
    pip install PyMuPDF
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装Pillow库...
    pip install Pillow
)

python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到tkinter库，这是Python的标准库
    echo 请确保安装了完整版的Python
    pause
    exit /b
)

echo 启动PDF转图片工具...
python "%~dp0pdf_to_images.py"

echo.
pause
