package com.tony.trading.service;

import com.tony.trading.model.SimulatedTrade;
import com.tony.trading.model.Trade;
import com.tony.trading.model.TradeDirection;
import com.tony.trading.model.TradingDecision;

import java.util.List;

/**
 * 交易服务接口
 */
public interface TradeService {
    
    /**
     * 创建新交易
     * @param trade 交易记录
     * @return 创建的交易记录
     */
    Trade createTrade(Trade trade);
    
    /**
     * 更新交易
     * @param trade 交易记录
     * @return 更新后的交易记录
     */
    Trade updateTrade(Trade trade);
    
    /**
     * 关闭交易（平仓）
     * @param tradeId 交易ID
     * @param exitPrice 出场价格
     * @return 关闭后的交易记录
     */
    Trade closeTrade(String tradeId, double exitPrice);
    
    /**
     * 获取所有交易
     * @return 交易记录列表
     */
    List<Trade> getAllTrades();
    
    /**
     * 获取所有开仓中的交易
     * @return 开仓中的交易记录列表
     */
    List<Trade> getAllOpenTrades();
    
    /**
     * 获取所有已平仓的交易
     * @return 已平仓的交易记录列表
     */
    List<Trade> getAllClosedTrades();
    
    /**
     * 获取交易记录
     * @param tradeId 交易ID
     * @return 交易记录
     */
    Trade getTradeById(String tradeId);
    
    /**
     * 删除交易记录
     * @param tradeId 交易ID
     */
    void deleteTrade(String tradeId);
    
    /**
     * 根据当前价格更新交易盈亏
     * @param tradeId 交易ID
     * @param currentPrice 当前价格
     * @return 更新后的交易记录
     */
    Trade updateTradePnl(String tradeId, double currentPrice);
    
    /**
     * 生成交易决策
     * @param symbol 交易标的
     * @param direction 交易方向
     * @param entryPrice 入场价格
     * @param stopLoss 止损价格
     * @param takeProfit 止盈价格
     * @return 交易决策
     */
    TradingDecision generateTradingDecision(String symbol, TradeDirection direction, 
                                           double entryPrice, double stopLoss, double takeProfit);
    
    /**
     * 模拟交易结果
     * @param simulatedTrade 模拟交易
     * @return 模拟交易结果
     */
    SimulatedTrade simulateTrade(SimulatedTrade simulatedTrade);
    
    /**
     * 检查交易的爆仓风险
     * @param tradeId 交易ID
     * @param currentPrice 当前价格
     * @return 爆仓预警信息
     */
    String checkLiquidationRisk(String tradeId, double currentPrice);
    
    /**
     * 获取所有开仓交易的爆仓预警
     * @return 所有交易的爆仓预警信息
     */
    String getAllLiquidationWarnings();
}