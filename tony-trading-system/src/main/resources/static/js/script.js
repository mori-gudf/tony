/**
 * Tony交易心法系统 - 前端交互脚本
 */

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initTooltips();
    
    // 初始化表单验证
    initFormValidation();
    
    // 初始化风险回报比计算
    initRiskRewardCalculator();
    
    // 初始化交易模拟计算器
    initTradeSimulator();
});

/**
 * 初始化Bootstrap工具提示
 */
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * 初始化表单验证
 */
function initFormValidation() {
    // 获取所有需要验证的表单
    var forms = document.querySelectorAll('.needs-validation');
    
    // 遍历表单并添加验证事件
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * 初始化风险回报比计算器
 */
function initRiskRewardCalculator() {
    // 获取交易决策页面的相关输入字段
    var entryPriceInput = document.getElementById('suggestedEntryPrice');
    var stopLossInput = document.getElementById('suggestedStopLoss');
    var takeProfitInput = document.getElementById('suggestedTakeProfit');
    var directionSelect = document.getElementById('direction');
    
    // 如果相关元素存在，添加事件监听器
    if (entryPriceInput && stopLossInput && takeProfitInput && directionSelect) {
        var inputs = [entryPriceInput, stopLossInput, takeProfitInput, directionSelect];
        
        inputs.forEach(function(input) {
            input.addEventListener('change', calculateRiskReward);
        });
    }
    
    /**
     * 计算风险回报比
     */
    function calculateRiskReward() {
        var entryPrice = parseFloat(entryPriceInput.value) || 0;
        var stopLoss = parseFloat(stopLossInput.value) || 0;
        var takeProfit = parseFloat(takeProfitInput.value) || 0;
        var direction = directionSelect.value;
        
        if (entryPrice > 0 && stopLoss > 0 && takeProfit > 0) {
            var riskRewardRatio;
            
            if (direction === 'LONG') {
                // 做多
                var risk = entryPrice - stopLoss;
                var reward = takeProfit - entryPrice;
                riskRewardRatio = risk > 0 ? reward / risk : 0;
            } else if (direction === 'SHORT') {
                // 做空
                var risk = stopLoss - entryPrice;
                var reward = entryPrice - takeProfit;
                riskRewardRatio = risk > 0 ? reward / risk : 0;
            }
            
            // 显示风险回报比（如果页面上有相应元素）
            var riskRewardDisplay = document.getElementById('riskRewardRatio');
            if (riskRewardDisplay) {
                riskRewardDisplay.textContent = riskRewardRatio.toFixed(2);
                
                // 根据风险回报比设置颜色
                if (riskRewardRatio >= 2) {
                    riskRewardDisplay.className = 'risk-reward-good';
                } else if (riskRewardRatio >= 1) {
                    riskRewardDisplay.className = 'risk-reward-medium';
                } else {
                    riskRewardDisplay.className = 'risk-reward-bad';
                }
            }
        }
    }
}

/**
 * 初始化交易模拟计算器
 */
function initTradeSimulator() {
    // 获取模拟交易页面的相关输入字段
    var entryPriceInput = document.getElementById('entryPrice');
    var currentPriceInput = document.getElementById('currentPrice');
    var leverageInput = document.getElementById('leverage');
    var positionSizeInput = document.getElementById('positionSize');
    var directionSelect = document.getElementById('direction');
    
    // 如果相关元素存在，添加事件监听器
    if (entryPriceInput && currentPriceInput && leverageInput && positionSizeInput && directionSelect) {
        var inputs = [entryPriceInput, currentPriceInput, leverageInput, positionSizeInput, directionSelect];
        
        inputs.forEach(function(input) {
            input.addEventListener('input', calculateSimulatedPnl);
        });
    }
    
    /**
     * 计算模拟盈亏
     */
    function calculateSimulatedPnl() {
        var entryPrice = parseFloat(entryPriceInput.value) || 0;
        var currentPrice = parseFloat(currentPriceInput.value) || 0;
        var leverage = parseFloat(leverageInput.value) || 0;
        var positionSize = parseFloat(positionSizeInput.value) || 0;
        var direction = directionSelect.value;
        
        if (entryPrice > 0 && currentPrice > 0 && leverage > 0 && positionSize > 0) {
            var pnl, pnlPercentage;
            
            if (direction === 'LONG') {
                // 做多
                pnl = positionSize * leverage * (currentPrice - entryPrice) / entryPrice;
                pnlPercentage = (currentPrice - entryPrice) / entryPrice * leverage * 100;
            } else if (direction === 'SHORT') {
                // 做空
                pnl = positionSize * leverage * (entryPrice - currentPrice) / entryPrice;
                pnlPercentage = (entryPrice - currentPrice) / entryPrice * leverage * 100;
            }
            
            // 显示模拟盈亏（如果页面上有相应元素）
            var pnlDisplay = document.getElementById('simulatedPnl');
            var pnlPercentageDisplay = document.getElementById('simulatedPnlPercentage');
            
            if (pnlDisplay) {
                pnlDisplay.textContent = pnl.toFixed(2) + ' U';
                pnlDisplay.className = pnl >= 0 ? 'text-success' : 'text-danger';
            }
            
            if (pnlPercentageDisplay) {
                pnlPercentageDisplay.textContent = pnlPercentage.toFixed(2) + '%';
                pnlPercentageDisplay.className = pnlPercentage >= 0 ? 'text-success' : 'text-danger';
            }
        }
    }
}

/**
 * 确认删除交易记录
 * @param {string} tradeId 交易ID
 * @returns {boolean} 是否确认删除
 */
function confirmDeleteTrade(tradeId) {
    return confirm('确定要删除这条交易记录吗？此操作不可撤销。');
}

/**
 * 确认平仓交易
 * @param {string} tradeId 交易ID
 * @returns {boolean} 是否确认平仓
 */
function confirmCloseTrade(tradeId) {
    return confirm('确定要平仓这笔交易吗？请确保出场价格准确无误。');
}

/**
 * 格式化日期时间
 * @param {Date} date 日期对象
 * @returns {string} 格式化后的日期时间字符串
 */
function formatDateTime(date) {
    if (!date) return '';
    
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
    var hours = String(date.getHours()).padStart(2, '0');
    var minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}`;
}

/**
 * 格式化金额
 * @param {number} amount 金额
 * @param {number} decimals 小数位数
 * @returns {string} 格式化后的金额字符串
 */
function formatAmount(amount, decimals = 2) {
    if (amount === null || amount === undefined) return '';
    return amount.toFixed(decimals);
}