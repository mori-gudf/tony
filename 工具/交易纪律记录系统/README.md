# 交易纪律记录系统

基于Tony交易心法的交易纪律记录系统，帮助交易者记录交易信息、监控风险、提供心法提示，并生成分析报告。

## 功能特点

- **交易记录管理**：记录每笔交易的详细信息，包括日期、标的、方向、价格、数量、止损价、目标价、结果和盈亏等
- **资金管理**：监控资金变化、计算当前仓位、最大回撤和盈亏比等指标
- **交易日志**：记录交易心得、市场分析和策略研究等
- **统计分析**：生成交易统计数据、盈亏分布图、胜率统计图和资金曲线图等
- **心法提示**：基于Tony交易心法的提示和建议，帮助交易者保持正确的交易心态和纪律
- **风险警告**：监控最大回撤、日亏损限制等风险指标，及时发出警告

## 系统要求

- Python 3.6 或更高版本
- 依赖库：tkinter, matplotlib, pandas, numpy, pillow

## 安装方法

1. 确保已安装Python 3.6或更高版本
2. 安装必要的依赖库：
   ```bash
   pip install matplotlib pandas numpy pillow
   ```
   注意：tkinter通常包含在Python标准库中，如果没有，请根据您的操作系统安装它

## 使用方法

1. 运行启动脚本：
   - Windows: 双击`start.bat`
   - Mac/Linux: 在终端中执行`./start.sh`

2. 或者直接运行主程序：
   ```bash
   python main.py
   ```

3. 首次运行时，系统会自动创建必要的配置文件和数据文件

4. 在系统中，您可以：
   - 记录每笔交易的详细信息
   - 查看资金曲线和统计数据
   - 记录交易日志和心得
   - 获取基于Tony交易心法的提示
   - 生成交易报告

## 文件说明

- `main.py`: 主程序入口
- `config.py`: 配置管理模块
- `trade_journal.py`: 主应用类
- `trade_journal_methods.py`: 主应用类方法补充
- `dialogs.py`: 对话框模块
- `utils.py`: 工具函数模块
- `heart_quotes.json`: 心法语录数据
- `start.bat`: Windows启动脚本
- `start.sh`: Mac/Linux启动脚本
- `create_icon.py`: 创建应用图标的脚本

## 数据存储

系统会在当前目录下创建以下文件来存储数据：
- `config.json`: 系统配置
- `trades.json`: 交易记录
- `journal.json`: 交易日志

## 基于Tony交易心法

本系统基于Tony的期货合约交易心法，强调以下核心原则：
- 完整的交易系统（入场、出场、止损、资金管理、交易心理）
- 风险第一，利润第二
- 概率思维与期望值
- 顺势而为
- 科学的资金管理
- 心理控制与执行力

## 常见问题

1. **如果程序无法启动，显示"tkinter未安装"错误怎么办？**
   - 在Windows上，重新安装Python时勾选"tcl/tk and IDLE"选项
   - 在Ubuntu/Debian上，运行`sudo apt-get install python3-tk`
   - 在Fedora上，运行`sudo dnf install python3-tkinter`
   - 在macOS上，使用Homebrew安装Python时应该已包含tkinter

2. **如何备份我的交易数据？**
   - 在"设置"选项卡中，点击"备份数据"按钮，选择保存位置即可

3. **如何恢复备份的数据？**
   - 在"设置"选项卡中，点击"恢复数据"按钮，选择备份文件即可

## 联系方式

如有问题或建议，请联系开发者。

## 许可证

本软件仅供学习和研究使用，未经授权不得用于商业目的。