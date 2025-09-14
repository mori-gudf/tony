package com.tony.trading.model;

import java.time.LocalDateTime;

/**
 * 模拟交易模型类
 * 用于计算可能的交易结果，而不实际执行交易
 */
public class SimulatedTrade {
    private String symbol;              // 交易标的
    private TradeDirection direction;    // 交易方向
    private double leverage;            // 杠杆倍数
    private double positionSize;        // 仓位大小（U）
    private double entryPrice;          // 入场价格
    private double currentPrice;        // 当前价格
    private double stopLoss;            // 止损价格
    private double takeProfit;          // 止盈价格
    private LocalDateTime simulationTime; // 模拟时间

    // Getters and Setters
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
    
    public double getCurrentPrice() { return currentPrice; }
    public void setCurrentPrice(double currentPrice) { this.currentPrice = currentPrice; }
    
    public double getStopLoss() { return stopLoss; }
    public void setStopLoss(double stopLoss) { this.stopLoss = stopLoss; }
    
    public double getTakeProfit() { return takeProfit; }
    public void setTakeProfit(double takeProfit) { this.takeProfit = takeProfit; }
    
    public LocalDateTime getSimulationTime() { return simulationTime; }
    public void setSimulationTime(LocalDateTime simulationTime) { this.simulationTime = simulationTime; }
    
    /**
     * 计算模拟盈亏
     * @return 模拟盈亏金额
     */
    public double calculateSimulatedPnl() {
        if (direction == TradeDirection.LONG) {
            return positionSize * leverage * (currentPrice - entryPrice) / entryPrice;
        } else {
            return positionSize * leverage * (entryPrice - currentPrice) / entryPrice;
        }
    }
    
    /**
     * 计算模拟盈亏百分比
     * @return 模拟盈亏百分比
     */
    public double calculateSimulatedPnlPercentage() {
        if (direction == TradeDirection.LONG) {
            return (currentPrice - entryPrice) / entryPrice * leverage * 100;
        } else {
            return (entryPrice - currentPrice) / entryPrice * leverage * 100;
        }
    }
    
    /**
     * 检查是否触发止损
     * @return 是否触发止损
     */
    public boolean isStopLossTriggered() {
        if (direction == TradeDirection.LONG) {
            return currentPrice <= stopLoss;
        } else {
            return currentPrice >= stopLoss;
        }
    }
    
    /**
     * 检查是否触发止盈
     * @return 是否触发止盈
     */
    public boolean isTakeProfitTriggered() {
        if (direction == TradeDirection.LONG) {
            return currentPrice >= takeProfit;
        } else {
            return currentPrice <= takeProfit;
        }
    }
    
    /**
     * 计算风险回报比
     * @return 风险回报比
     */
    public double calculateRiskRewardRatio() {
        double risk;
        double reward;
        
        if (direction == TradeDirection.LONG) {
            risk = (entryPrice - stopLoss) / entryPrice;
            reward = (takeProfit - entryPrice) / entryPrice;
        } else {
            risk = (stopLoss - entryPrice) / entryPrice;
            reward = (entryPrice - takeProfit) / entryPrice;
        }
        
        if (risk == 0) return 0;
        return reward / risk;
    }
}