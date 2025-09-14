package com.tony.trading.service;

import com.tony.trading.model.AccountBalance;
import com.tony.trading.model.Trade;
import com.tony.trading.model.TradeStatus;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.List;

/**
 * 账户服务实现类
 */
@Service
public class AccountServiceImpl implements AccountService {
    
    @Value("${trading.data.path:./data}")
    private String dataPath;
    
    private final ObjectMapper objectMapper;
    
    {
        objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
    }
    private final TradeService tradeService;
    
    public AccountServiceImpl(TradeService tradeService) {
        this.tradeService = tradeService;
    }
    
    @Override
    public AccountBalance getAccountBalance() {
        try {
            File file = new File(dataPath, "account_balance.json");
            if (file.exists()) {
                AccountBalance balance = objectMapper.readValue(file, AccountBalance.class);
                // 实时更新账户信息
                updateAccountFromTrades(balance);
                return balance;
            } else {
                // 创建默认账户
                AccountBalance defaultBalance = new AccountBalance();
                updateAccountBalance(defaultBalance);
                return defaultBalance;
            }
        } catch (IOException e) {
            // 如果读取失败，返回默认账户
            return new AccountBalance();
        }
    }
    
    @Override
    public void updateAccountBalance(AccountBalance accountBalance) {
        try {
            File dataDir = new File(dataPath);
            if (!dataDir.exists()) {
                dataDir.mkdirs();
            }
            
            accountBalance.setLastUpdated(LocalDateTime.now());
            File file = new File(dataPath, "account_balance.json");
            objectMapper.writeValue(file, accountBalance);
        } catch (IOException e) {
            throw new RuntimeException("Failed to save account balance", e);
        }
    }
    
    @Override
    public boolean openPosition(Trade trade) {
        AccountBalance balance = getAccountBalance();
        
        // 检查资金是否足够
        if (!hasEnoughBalance(trade.getPositionSize())) {
            return false;
        }
        
        // 检查Tony心法合规性
        if (!checkTonyMethodCompliance(trade.getPositionSize())) {
            return false;
        }
        
        // 扣除资金
        balance.setUsedBalance(balance.getUsedBalance() + trade.getPositionSize());
        balance.setAvailableBalance(balance.getTotalBalance() - balance.getUsedBalance());
        
        updateAccountBalance(balance);
        return true;
    }
    
    @Override
    public void closePosition(Trade trade) {
        AccountBalance balance = getAccountBalance();
        
        // 释放资金
        balance.setUsedBalance(balance.getUsedBalance() - trade.getPositionSize());
        
        // 计算盈亏并更新总资金
        double pnl = trade.getPnl();
        balance.setTotalBalance(balance.getTotalBalance() + pnl);
        balance.setTotalPnl(balance.getTotalPnl() + pnl);
        balance.setAvailableBalance(balance.getTotalBalance() - balance.getUsedBalance());
        
        // 更新交易统计
        balance.setTotalTrades(balance.getTotalTrades() + 1);
        if (pnl > 0) {
            balance.setWinTrades(balance.getWinTrades() + 1);
        } else if (pnl < 0) {
            balance.setLossTrades(balance.getLossTrades() + 1);
        }
        
        // 计算胜率
        if (balance.getTotalTrades() > 0) {
            balance.setWinRate((double) balance.getWinTrades() / balance.getTotalTrades() * 100);
        }
        
        // 计算总盈亏百分比
        double initialBalance = balance.getTotalBalance() - balance.getTotalPnl();
        if (initialBalance > 0) {
            balance.setTotalPnlPercentage(balance.getTotalPnl() / initialBalance * 100);
        }
        
        // 更新Tony心法参数
        balance.updateTonyMethodParams();
        
        updateAccountBalance(balance);
    }
    
    @Override
    public boolean hasEnoughBalance(double positionSize) {
        AccountBalance balance = getAccountBalance();
        return balance.getAvailableBalance() >= positionSize;
    }
    
    @Override
    public boolean checkTonyMethodCompliance(double positionSize) {
        AccountBalance balance = getAccountBalance();
        return balance.isTonyMethodCompliant(positionSize);
    }
    
    @Override
    public String getTonyMethodAdvice(double positionSize) {
        AccountBalance balance = getAccountBalance();
        return balance.getTonyMethodAdvice(positionSize);
    }
    
    @Override
    public void resetAccount(double initialBalance) {
        AccountBalance balance = new AccountBalance();
        balance.setTotalBalance(initialBalance);
        balance.setAvailableBalance(initialBalance);
        balance.setUsedBalance(0.0);
        balance.setTotalPnl(0.0);
        balance.setTotalPnlPercentage(0.0);
        balance.setTotalTrades(0);
        balance.setWinTrades(0);
        balance.setLossTrades(0);
        balance.setWinRate(0.0);
        balance.updateTonyMethodParams();
        
        updateAccountBalance(balance);
    }
    
    /**
     * 从交易记录更新账户信息
     */
    private void updateAccountFromTrades(AccountBalance balance) {
        List<Trade> allTrades = tradeService.getAllTrades();
        
        // 重新计算已使用资金
        double usedBalance = 0.0;
        for (Trade trade : allTrades) {
            if (trade.getStatus() == TradeStatus.OPEN) {
                usedBalance += trade.getPositionSize();
            }
        }
        
        balance.setUsedBalance(usedBalance);
        balance.setAvailableBalance(balance.getTotalBalance() - usedBalance);
        
        // 重新计算交易统计
        int totalTrades = 0;
        int winTrades = 0;
        int lossTrades = 0;
        double totalPnl = 0.0;
        
        for (Trade trade : allTrades) {
            if (trade.getStatus() == TradeStatus.CLOSED) {
                totalTrades++;
                totalPnl += trade.getPnl();
                
                if (trade.getPnl() > 0) {
                    winTrades++;
                } else if (trade.getPnl() < 0) {
                    lossTrades++;
                }
            }
        }
        
        balance.setTotalTrades(totalTrades);
        balance.setWinTrades(winTrades);
        balance.setLossTrades(lossTrades);
        balance.setTotalPnl(totalPnl);
        
        if (totalTrades > 0) {
            balance.setWinRate((double) winTrades / totalTrades * 100);
        }
        
        // 计算总盈亏百分比（基于初始资金100U）
        double initialBalance = 100.0;
        balance.setTotalPnlPercentage(totalPnl / initialBalance * 100);
    }
}