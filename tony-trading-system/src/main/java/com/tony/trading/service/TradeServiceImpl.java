package com.tony.trading.service;

import com.tony.trading.model.*;
import com.tony.trading.repository.TradeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

/**
 * 交易服务实现类
 */
@Service
public class TradeServiceImpl implements TradeService {

    private final TradeRepository tradeRepository;

    @Autowired
    public TradeServiceImpl(TradeRepository tradeRepository) {
        this.tradeRepository = tradeRepository;
    }

    @Override
    public Trade createTrade(Trade trade) {
        if (trade.getId() == null) {
            trade.setId(UUID.randomUUID().toString());
        }
        trade.setEntryTime(LocalDateTime.now());
        trade.setStatus(TradeStatus.OPEN);
        return tradeRepository.save(trade);
    }

    @Override
    public Trade updateTrade(Trade trade) {
        return tradeRepository.update(trade);
    }

    @Override
    public Trade closeTrade(String tradeId, double exitPrice) {
        Trade trade = tradeRepository.findById(tradeId)
                .orElseThrow(() -> new RuntimeException("交易记录不存在: " + tradeId));
        
        trade.setExitPrice(exitPrice);
        trade.setExitTime(LocalDateTime.now());
        trade.setStatus(TradeStatus.CLOSED);
        
        // 计算盈亏
        if (trade.getDirection() == TradeDirection.LONG) {
            trade.setPnl(trade.getPositionSize() * trade.getLeverage() * 
                    (exitPrice - trade.getEntryPrice()) / trade.getEntryPrice());
            trade.setPnlPercentage((exitPrice - trade.getEntryPrice()) / 
                    trade.getEntryPrice() * trade.getLeverage() * 100);
        } else {
            trade.setPnl(trade.getPositionSize() * trade.getLeverage() * 
                    (trade.getEntryPrice() - exitPrice) / trade.getEntryPrice());
            trade.setPnlPercentage((trade.getEntryPrice() - exitPrice) / 
                    trade.getEntryPrice() * trade.getLeverage() * 100);
        }
        
        return tradeRepository.update(trade);
    }

    @Override
    public List<Trade> getAllTrades() {
        return tradeRepository.findAll();
    }

    @Override
    public List<Trade> getAllOpenTrades() {
        return tradeRepository.findAllOpenTrades();
    }

    @Override
    public List<Trade> getAllClosedTrades() {
        return tradeRepository.findAllClosedTrades();
    }

    @Override
    public Trade getTradeById(String tradeId) {
        return tradeRepository.findById(tradeId)
                .orElseThrow(() -> new RuntimeException("交易记录不存在: " + tradeId));
    }

    @Override
    public void deleteTrade(String tradeId) {
        tradeRepository.deleteById(tradeId);
    }

    @Override
    public Trade updateTradePnl(String tradeId, double currentPrice) {
        Trade trade = tradeRepository.findById(tradeId)
                .orElseThrow(() -> new RuntimeException("交易记录不存在: " + tradeId));
        
        // 计算当前盈亏
        double pnl = trade.calculateCurrentPnl(currentPrice);
        double pnlPercentage = trade.calculateCurrentPnlPercentage(currentPrice);
        
        trade.setPnl(pnl);
        trade.setPnlPercentage(pnlPercentage);
        
        return tradeRepository.update(trade);
    }

    @Override
    public TradingDecision generateTradingDecision(String symbol, TradeDirection direction, 
                                                 double entryPrice, double stopLoss, double takeProfit) {
        TradingDecision decision = new TradingDecision();
        decision.setSymbol(symbol);
        decision.setDirection(direction);
        decision.setSuggestedEntryPrice(entryPrice);
        decision.setSuggestedStopLoss(stopLoss);
        decision.setSuggestedTakeProfit(takeProfit);
        
        // 根据Tony交易心法计算建议杠杆和仓位
        double riskPerTrade = 0.02; // 每笔交易风险控制在总资金的2%
        double totalCapital = 100.0; // 总资金100U
        
        // 计算风险回报比
        double riskRewardRatio;
        if (direction == TradeDirection.LONG) {
            riskRewardRatio = (takeProfit - entryPrice) / (entryPrice - stopLoss);
        } else {
            riskRewardRatio = (entryPrice - takeProfit) / (stopLoss - entryPrice);
        }
        decision.setRiskRewardRatio(riskRewardRatio);
        
        // 根据风险回报比调整建议杠杆
        double suggestedLeverage;
        if (riskRewardRatio >= 3.0) {
            suggestedLeverage = 5.0; // 风险回报比高，可以适当提高杠杆
        } else if (riskRewardRatio >= 2.0) {
            suggestedLeverage = 3.0;
        } else {
            suggestedLeverage = 2.0; // 风险回报比低，降低杠杆
        }
        decision.setSuggestedLeverage(suggestedLeverage);
        
        // 计算建议仓位
        double riskAmount = totalCapital * riskPerTrade;
        double priceRiskPercentage;
        if (direction == TradeDirection.LONG) {
            priceRiskPercentage = (entryPrice - stopLoss) / entryPrice;
        } else {
            priceRiskPercentage = (stopLoss - entryPrice) / entryPrice;
        }
        
        double suggestedPositionSize = riskAmount / (priceRiskPercentage * suggestedLeverage);
        decision.setSuggestedPositionSize(Math.min(suggestedPositionSize, totalCapital * 0.5)); // 最大仓位不超过总资金的50%
        
        // 添加Tony交易心法建议
        generateHeartMethodAdvice(decision);
        
        return decision;
    }

    @Override
    public SimulatedTrade simulateTrade(SimulatedTrade simulatedTrade) {
        // 设置模拟时间
        simulatedTrade.setSimulationTime(LocalDateTime.now());
        
        return simulatedTrade;
    }
    
    /**
     * 生成Tony交易心法建议
     * @param decision 交易决策
     */
    private void generateHeartMethodAdvice(TradingDecision decision) {
        StringBuilder advice = new StringBuilder();
        
        // 趋势分析
        String trendAnalysis = "请确认当前趋势方向，只有顺应主要趋势方向交易才能提高胜率。";
        decision.setTrendAnalysis(trendAnalysis);
        
        // 支撑阻力分析
        String supportResistance = "识别关键支撑阻力位，在支撑位附近做多或阻力位附近做空可以提高胜率。";
        decision.setSupportResistance(supportResistance);
        
        // 风险评估
        double riskRewardRatio = decision.getRiskRewardRatio();
        String riskAssessment;
        if (riskRewardRatio < 1.5) {
            riskAssessment = "风险回报比过低（" + String.format("%.2f", riskRewardRatio) + "），不建议交易。Tony心法要求风险回报比至少为2:1。";
        } else if (riskRewardRatio < 2.0) {
            riskAssessment = "风险回报比（" + String.format("%.2f", riskRewardRatio) + "）略低，建议寻找更好的交易机会或调整止损/止盈位置。";
        } else if (riskRewardRatio < 3.0) {
            riskAssessment = "风险回报比（" + String.format("%.2f", riskRewardRatio) + "）良好，符合Tony心法要求。";
        } else {
            riskAssessment = "风险回报比（" + String.format("%.2f", riskRewardRatio) + "）优秀，是高质量的交易机会。";
        }
        decision.setRiskAssessment(riskAssessment);
        
        // 心法建议
        advice.append("【Tony交易心法建议】\n\n");
        advice.append("1. 资金管理：每笔交易风险控制在总资金的2%以内\n");
        advice.append("2. 建议仓位：").append(String.format("%.2f", decision.getSuggestedPositionSize())).append("U\n");
        advice.append("3. 建议杠杆：").append(String.format("%.1f", decision.getSuggestedLeverage())).append("倍\n");
        advice.append("4. 风险回报比：").append(String.format("%.2f", riskRewardRatio)).append("\n\n");
        
        if (riskRewardRatio >= 2.0) {
            advice.append("✅ 该交易符合Tony心法的风险回报要求\n");
        } else {
            advice.append("❌ 该交易不符合Tony心法的风险回报要求\n");
        }
        
        advice.append("\n【执行要点】\n");
        advice.append("• 严格设置止损，永远不要移动止损位置\n");
        advice.append("• 情绪稳定，按计划执行，不要被短期波动影响\n");
        advice.append("• 记录交易日志，分析每笔交易的得失\n");
        advice.append("• 保持耐心，只交易高概率的机会\n");
        
        decision.setHeartMethodAdvice(advice.toString());
    }
}