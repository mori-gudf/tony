package com.tony.trading.model;

import java.time.LocalDateTime;

/**
 * 交易记录模型类
 */
public class Trade {
    private String id;                  // 交易ID
    private String symbol;              // 交易标的
    private TradeDirection direction;    // 交易方向
    private double leverage;            // 杠杆倍数
    private double positionSize;        // 仓位大小（U）
    private double entryPrice;          // 入场价格
    private LocalDateTime entryTime;    // 入场时间
    private double exitPrice;           // 出场价格
    private LocalDateTime exitTime;     // 出场时间
    private double stopLoss;            // 止损价格
    private double takeProfit;          // 止盈价格
    private double pnl;                 // 盈亏金额
    private double pnlPercentage;       // 盈亏百分比
    private String tradingReason;       // 交易原因
    private String marketAnalysis;      // 市场分析
    private String psychologicalState;  // 心理状态
    private String lessonLearned;       // 经验教训
    private TradeStatus status;         // 交易状态

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getSymbol() { return symbol; }
    public void setSymbol(String symbol) { this.symbol = symbol; }
    
    public TradeDirection getDirection() { return direction; }
    public void setDirection(TradeDirection direction) { this.direction = direction; }
    
    public double getLeverage() { return leverage; }
    public void setLeverage(double leverage) { this.leverage = leverage; }
    
    public double getPositionSize() { return positionSize; }
    public void setPositionSize(double positionSize) { this.positionSize = positionSize; }
    
    public double getEntryPrice() { return entryPrice; }
    public void setEntryPrice(double entryPrice) { this.entryPrice = entryPrice; }
    
    public LocalDateTime getEntryTime() { return entryTime; }
    public void setEntryTime(LocalDateTime entryTime) { this.entryTime = entryTime; }
    
    public double getExitPrice() { return exitPrice; }
    public void setExitPrice(double exitPrice) { this.exitPrice = exitPrice; }
    
    public LocalDateTime getExitTime() { return exitTime; }
    public void setExitTime(LocalDateTime exitTime) { this.exitTime = exitTime; }
    
    public double getStopLoss() { return stopLoss; }
    public void setStopLoss(double stopLoss) { this.stopLoss = stopLoss; }
    
    public double getTakeProfit() { return takeProfit; }
    public void setTakeProfit(double takeProfit) { this.takeProfit = takeProfit; }
    
    public double getPnl() { return pnl; }
    public void setPnl(double pnl) { this.pnl = pnl; }
    
    public double getPnlPercentage() { return pnlPercentage; }
    public void setPnlPercentage(double pnlPercentage) { this.pnlPercentage = pnlPercentage; }
    
    public String getTradingReason() { return tradingReason; }
    public void setTradingReason(String tradingReason) { this.tradingReason = tradingReason; }
    
    public String getMarketAnalysis() { return marketAnalysis; }
    public void setMarketAnalysis(String marketAnalysis) { this.marketAnalysis = marketAnalysis; }
    
    public String getPsychologicalState() { return psychologicalState; }
    public void setPsychologicalState(String psychologicalState) { this.psychologicalState = psychologicalState; }
    
    public String getLessonLearned() { return lessonLearned; }
    public void setLessonLearned(String lessonLearned) { this.lessonLearned = lessonLearned; }
    
    public TradeStatus getStatus() { return status; }
    public void setStatus(TradeStatus status) { this.status = status; }
    
    /**
     * 计算当前盈亏
     * @param currentPrice 当前价格
     * @return 盈亏金额
     */
    public double calculateCurrentPnl(double currentPrice) {
        if (direction == TradeDirection.LONG) {
            return positionSize * leverage * (currentPrice - entryPrice) / entryPrice;
        } else {
            return positionSize * leverage * (entryPrice - currentPrice) / entryPrice;
        }
    }
    
    /**
     * 计算当前盈亏百分比
     * @param currentPrice 当前价格
     * @return 盈亏百分比
     */
    public double calculateCurrentPnlPercentage(double currentPrice) {
        if (direction == TradeDirection.LONG) {
            return (currentPrice - entryPrice) / entryPrice * leverage * 100;
        } else {
            return (entryPrice - currentPrice) / entryPrice * leverage * 100;
        }
    }
    
    /**
     * 计算爆仓价格
     * @return 爆仓价格
     */
    public double calculateLiquidationPrice() {
        // 爆仓价格计算：当亏损达到100%时的价格
        if (direction == TradeDirection.LONG) {
            // 做多爆仓价格 = 入场价格 * (1 - 1/杠杆)
            return entryPrice * (1 - 1.0 / leverage);
        } else {
            // 做空爆仓价格 = 入场价格 * (1 + 1/杠杆)
            return entryPrice * (1 + 1.0 / leverage);
        }
    }
    
    /**
     * 计算距离爆仓的百分比
     * @param currentPrice 当前价格
     * @return 距离爆仓的百分比（正数表示安全，负数表示已爆仓）
     */
    public double calculateDistanceToLiquidation(double currentPrice) {
        double liquidationPrice = calculateLiquidationPrice();
        
        if (direction == TradeDirection.LONG) {
            // 做多：当前价格越低越危险
            return (currentPrice - liquidationPrice) / liquidationPrice * 100;
        } else {
            // 做空：当前价格越高越危险
            return (liquidationPrice - currentPrice) / liquidationPrice * 100;
        }
    }
    
    /**
     * 检查是否接近爆仓（距离爆仓小于20%）
     * @param currentPrice 当前价格
     * @return 是否接近爆仓
     */
    public boolean isNearLiquidation(double currentPrice) {
        double distanceToLiquidation = calculateDistanceToLiquidation(currentPrice);
        return distanceToLiquidation < 20.0 && distanceToLiquidation > 0;
    }
    
    /**
     * 检查是否已爆仓
     * @param currentPrice 当前价格
     * @return 是否已爆仓
     */
    public boolean isLiquidated(double currentPrice) {
        double distanceToLiquidation = calculateDistanceToLiquidation(currentPrice);
        return distanceToLiquidation <= 0;
    }
    
    /**
     * 获取爆仓预警信息
     * @param currentPrice 当前价格
     * @return 爆仓预警信息
     */
    public String getLiquidationWarning(double currentPrice) {
        double liquidationPrice = calculateLiquidationPrice();
        double distanceToLiquidation = calculateDistanceToLiquidation(currentPrice);
        
        StringBuilder warning = new StringBuilder();
        
        if (isLiquidated(currentPrice)) {
            warning.append("🚨 【爆仓警告】仓位已爆仓！\n");
            warning.append("爆仓价格: ").append(String.format("%.6f", liquidationPrice)).append("\n");
            warning.append("当前价格: ").append(String.format("%.6f", currentPrice)).append("\n");
        } else if (isNearLiquidation(currentPrice)) {
            warning.append("⚠️ 【爆仓预警】仓位接近爆仓！\n");
            warning.append("爆仓价格: ").append(String.format("%.6f", liquidationPrice)).append("\n");
            warning.append("当前价格: ").append(String.format("%.6f", currentPrice)).append("\n");
            warning.append("距离爆仓: ").append(String.format("%.2f%%", distanceToLiquidation)).append("\n");
            warning.append("💡 Tony心法提醒：犹豫不决时一定要平仓，至少应减仓一半！\n");
        } else {
            warning.append("✅ 仓位安全\n");
            warning.append("爆仓价格: ").append(String.format("%.6f", liquidationPrice)).append("\n");
            warning.append("当前价格: ").append(String.format("%.6f", currentPrice)).append("\n");
            warning.append("安全距离: ").append(String.format("%.2f%%", distanceToLiquidation)).append("\n");
        }
        
        return warning.toString();
    }
}