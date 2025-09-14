package com.tony.trading.model;

import java.time.LocalDateTime;

/**
 * 账户资金模型类
 * 管理总资金和资金使用情况
 */
public class AccountBalance {
    private double totalBalance;        // 总资金
    private double availableBalance;    // 可用资金
    private double usedBalance;         // 已使用资金
    private double totalPnl;            // 总盈亏
    private double totalPnlPercentage;  // 总盈亏百分比
    private LocalDateTime lastUpdated;  // 最后更新时间
    private int totalTrades;            // 总交易次数
    private int winTrades;              // 盈利交易次数
    private int lossTrades;             // 亏损交易次数
    private double winRate;             // 胜率
    
    // Tony心法相关字段
    private double maxRiskPerTrade;     // 单笔交易最大风险（总资金的3%）
    private double maxPositionRatio;    // 最大仓位比例（总资金的30%）
    private double reserveRatio;        // 资金储备比例（总资金的67%以上）
    
    public AccountBalance() {
        this.totalBalance = 100.0; // 默认100U
        this.availableBalance = 100.0;
        this.usedBalance = 0.0;
        this.totalPnl = 0.0;
        this.totalPnlPercentage = 0.0;
        this.lastUpdated = LocalDateTime.now();
        this.totalTrades = 0;
        this.winTrades = 0;
        this.lossTrades = 0;
        this.winRate = 0.0;
        
        // Tony心法默认设置
        this.maxRiskPerTrade = totalBalance * 0.03; // 3%
        this.maxPositionRatio = 0.30; // 30%
        this.reserveRatio = 0.67; // 67%
    }
    
    /**
     * 更新Tony心法相关参数
     */
    public void updateTonyMethodParams() {
        this.maxRiskPerTrade = totalBalance * 0.03; // 单笔交易最大风险3%
        this.maxPositionRatio = 0.30; // 最大仓位比例30%
        this.reserveRatio = 0.67; // 资金储备比例67%
    }
    
    /**
     * 检查是否符合Tony心法资金管理要求
     */
    public boolean isTonyMethodCompliant(double positionSize) {
        // 检查单笔交易是否超过总资金的30%
        if (positionSize > totalBalance * maxPositionRatio) {
            return false;
        }
        
        // 检查是否保持足够的资金储备
        double usageRatio = (usedBalance + positionSize) / totalBalance;
        if (usageRatio > (1 - reserveRatio)) {
            return false;
        }
        
        return true;
    }
    
    /**
     * 获取Tony心法建议
     */
    public String getTonyMethodAdvice(double positionSize) {
        StringBuilder advice = new StringBuilder();
        
        // 资金管理建议
        if (positionSize > totalBalance * maxPositionRatio) {
            advice.append("⚠️ 违反Tony心法：单笔交易不应超过总资金的30%！当前仓位过大。\n");
        }
        
        double usageRatio = (usedBalance + positionSize) / totalBalance;
        if (usageRatio > (1 - reserveRatio)) {
            advice.append("⚠️ 违反Tony心法：应保持67%以上的资金储备，当前资金使用过多。\n");
        }
        
        // 风险控制建议
        double riskAmount = positionSize * 0.03; // 假设3%的风险
        if (riskAmount > maxRiskPerTrade) {
            advice.append("⚠️ 违反Tony心法：单笔交易风险不应超过总资金的3%！\n");
        }
        
        // 正面建议
        if (advice.length() == 0) {
            advice.append("✅ 符合Tony心法资金管理要求。\n");
            advice.append("💡 Tony心法提醒：\n");
            advice.append("- 永远不亏大钱，每次损失控制在最小\n");
            advice.append("- 以小博大，冒小风险赢取大利\n");
            advice.append("- 保持主力资金储备，等待决战机会\n");
        }
        
        return advice.toString();
    }
    
    // Getters and Setters
    public double getTotalBalance() { return totalBalance; }
    public void setTotalBalance(double totalBalance) { 
        this.totalBalance = totalBalance;
        updateTonyMethodParams();
    }
    
    public double getAvailableBalance() { return availableBalance; }
    public void setAvailableBalance(double availableBalance) { this.availableBalance = availableBalance; }
    
    public double getUsedBalance() { return usedBalance; }
    public void setUsedBalance(double usedBalance) { this.usedBalance = usedBalance; }
    
    public double getTotalPnl() { return totalPnl; }
    public void setTotalPnl(double totalPnl) { this.totalPnl = totalPnl; }
    
    public double getTotalPnlPercentage() { return totalPnlPercentage; }
    public void setTotalPnlPercentage(double totalPnlPercentage) { this.totalPnlPercentage = totalPnlPercentage; }
    
    public LocalDateTime getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(LocalDateTime lastUpdated) { this.lastUpdated = lastUpdated; }
    
    public int getTotalTrades() { return totalTrades; }
    public void setTotalTrades(int totalTrades) { this.totalTrades = totalTrades; }
    
    public int getWinTrades() { return winTrades; }
    public void setWinTrades(int winTrades) { this.winTrades = winTrades; }
    
    public int getLossTrades() { return lossTrades; }
    public void setLossTrades(int lossTrades) { this.lossTrades = lossTrades; }
    
    public double getWinRate() { return winRate; }
    public void setWinRate(double winRate) { this.winRate = winRate; }
    
    public double getMaxRiskPerTrade() { return maxRiskPerTrade; }
    public void setMaxRiskPerTrade(double maxRiskPerTrade) { this.maxRiskPerTrade = maxRiskPerTrade; }
    
    public double getMaxPositionRatio() { return maxPositionRatio; }
    public void setMaxPositionRatio(double maxPositionRatio) { this.maxPositionRatio = maxPositionRatio; }
    
    public double getReserveRatio() { return reserveRatio; }
    public void setReserveRatio(double reserveRatio) { this.reserveRatio = reserveRatio; }
}