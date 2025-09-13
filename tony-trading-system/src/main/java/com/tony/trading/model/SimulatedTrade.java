package com.tony.trading.model;

import lombok.Data;
import java.time.LocalDateTime;

/**
 * 模拟交易模型类
 * 用于计算可能的交易结果，而不实际执行交易
 */
@Data
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