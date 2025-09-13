package com.tony.trading.model;

import lombok.Data;

/**
 * 交易决策模型类
 * 基于Tony交易心法提供交易建议
 */
@Data
public class TradingDecision {
    private String symbol;              // 交易标的
    private TradeDirection direction;    // 建议交易方向
    private double suggestedEntryPrice; // 建议入场价格
    private double suggestedStopLoss;   // 建议止损价格
    private double suggestedTakeProfit; // 建议止盈价格
    private double suggestedLeverage;   // 建议杠杆倍数
    private double suggestedPositionSize; // 建议仓位大小
    private double riskRewardRatio;     // 风险回报比
    private String entryReason;         // 入场理由
    private String trendAnalysis;       // 趋势分析
    private String supportResistance;   // 支撑阻力分析
    private String riskAssessment;      // 风险评估
    private String heartMethodAdvice;   // 心法建议
    
    /**
     * 计算预期盈亏
     * @param currentPrice 当前价格
     * @return 预期盈亏金额
     */
    public double calculateExpectedPnl() {
        if (direction == TradeDirection.LONG) {
            return suggestedPositionSize * suggestedLeverage * (suggestedTakeProfit - suggestedEntryPrice) / suggestedEntryPrice;
        } else {
            return suggestedPositionSize * suggestedLeverage * (suggestedEntryPrice - suggestedTakeProfit) / suggestedEntryPrice;
        }
    }
    
    /**
     * 计算最大风险
     * @return 最大风险金额
     */
    public double calculateMaxRisk() {
        if (direction == TradeDirection.LONG) {
            return suggestedPositionSize * suggestedLeverage * (suggestedEntryPrice - suggestedStopLoss) / suggestedEntryPrice;
        } else {
            return suggestedPositionSize * suggestedLeverage * (suggestedStopLoss - suggestedEntryPrice) / suggestedEntryPrice;
        }
    }
    
    /**
     * 计算风险回报比
     * @return 风险回报比
     */
    public double calculateRiskRewardRatio() {
        double risk = calculateMaxRisk();
        if (risk == 0) return 0;
        return calculateExpectedPnl() / risk;
    }
}