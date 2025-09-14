package com.tony.trading.service;

import com.tony.trading.model.AccountBalance;
import com.tony.trading.model.Trade;

/**
 * 账户服务接口
 */
public interface AccountService {
    
    /**
     * 获取账户余额信息
     */
    AccountBalance getAccountBalance();
    
    /**
     * 更新账户余额
     */
    void updateAccountBalance(AccountBalance accountBalance);
    
    /**
     * 开仓时扣除资金
     */
    boolean openPosition(Trade trade);
    
    /**
     * 平仓时释放资金并计算盈亏
     */
    void closePosition(Trade trade);
    
    /**
     * 检查是否有足够资金开仓
     */
    boolean hasEnoughBalance(double positionSize);
    
    /**
     * 检查是否符合Tony心法资金管理要求
     */
    boolean checkTonyMethodCompliance(double positionSize);
    
    /**
     * 获取Tony心法资金管理建议
     */
    String getTonyMethodAdvice(double positionSize);
    
    /**
     * 重置账户（用于测试）
     */
    void resetAccount(double initialBalance);
}