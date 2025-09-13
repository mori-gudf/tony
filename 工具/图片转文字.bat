@echo off
echo 图片转文字工具 - 图形界面版
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
python -c "import pytesseract" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装pytesseract库...
    pip install pytesseract
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

echo.
echo 注意: 此工具需要安装Tesseract OCR引擎
echo 如果尚未安装，请从以下地址下载并安装:
echo https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 安装后，请确保将Tesseract添加到系统PATH中，或在程序中设置正确的路径
echo.

echo 启动图片转文字工具...
python "%~dp0images_to_text.py"

echo.
pause