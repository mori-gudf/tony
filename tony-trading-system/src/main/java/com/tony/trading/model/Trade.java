package com.tony.trading.model;

import lombok.Data;
import java.time.LocalDateTime;

/**
 * 交易记录模型类
 */
@Data
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
}