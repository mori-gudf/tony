package com.tony.trading.model;

/**
 * 交易决策模型类
 * 基于Tony交易心法提供交易建议
 */
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

    // Getters and Setters
    public String getSymbol() { return symbol; }
    public void setSymbol(String symbol) { this.symbol = symbol; }
    
    public TradeDirection getDirection() { return direction; }
    public void setDirection(TradeDirection direction) { this.direction = direction; }
    
    public double getSuggestedEntryPrice() { return suggestedEntryPrice; }
    public void setSuggestedEntryPrice(double suggestedEntryPrice) { this.suggestedEntryPrice = suggestedEntryPrice; }
    
    public double getSuggestedStopLoss() { return suggestedStopLoss; }
    public void setSuggestedStopLoss(double suggestedStopLoss) { this.suggestedStopLoss = suggestedStopLoss; }
    
    public double getSuggestedTakeProfit() { return suggestedTakeProfit; }
    public void setSuggestedTakeProfit(double suggestedTakeProfit) { this.suggestedTakeProfit = suggestedTakeProfit; }
    
    public double getSuggestedLeverage() { return suggestedLeverage; }
    public void setSuggestedLeverage(double suggestedLeverage) { this.suggestedLeverage = suggestedLeverage; }
    
    public double getSuggestedPositionSize() { return suggestedPositionSize; }
    public void setSuggestedPositionSize(double suggestedPositionSize) { this.suggestedPositionSize = suggestedPositionSize; }
    
    public double getRiskRewardRatio() { return riskRewardRatio; }
    public void setRiskRewardRatio(double riskRewardRatio) { this.riskRewardRatio = riskRewardRatio; }
    
    public String getEntryReason() { return entryReason; }
    public void setEntryReason(String entryReason) { this.entryReason = entryReason; }
    
    public String getTrendAnalysis() { return trendAnalysis; }
    public void setTrendAnalysis(String trendAnalysis) { this.trendAnalysis = trendAnalysis; }
    
    public String getSupportResistance() { return supportResistance; }
    public void setSupportResistance(String supportResistance) { this.supportResistance = supportResistance; }
    
    public String getRiskAssessment() { return riskAssessment; }
    public void setRiskAssessment(String riskAssessment) { this.riskAssessment = riskAssessment; }
    
    public String getHeartMethodAdvice() { return heartMethodAdvice; }
    public void setHeartMethodAdvice(String heartMethodAdvice) { this.heartMethodAdvice = heartMethodAdvice; }
    
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