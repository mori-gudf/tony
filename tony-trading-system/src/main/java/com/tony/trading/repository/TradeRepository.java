package com.tony.trading.repository;

import com.tony.trading.model.Trade;
import java.util.List;
import java.util.Optional;

/**
 * 交易记录数据访问接口
 */
public interface TradeRepository {
    
    /**
     * 保存交易记录
     * @param trade 交易记录
     * @return 保存后的交易记录
     */
    Trade save(Trade trade);
    
    /**
     * 根据ID查找交易记录
     * @param id 交易ID
     * @return 交易记录
     */
    Optional<Trade> findById(String id);
    
    /**
     * 查找所有交易记录
     * @return 交易记录列表
     */
    List<Trade> findAll();
    
    /**
     * 查找所有开仓中的交易
     * @return 开仓中的交易记录列表
     */
    List<Trade> findAllOpenTrades();
    
    /**
     * 查找所有已平仓的交易
     * @return 已平仓的交易记录列表
     */
    List<Trade> findAllClosedTrades();
    
    /**
     * 删除交易记录
     * @param id 交易ID
     */
    void deleteById(String id);
    
    /**
     * 更新交易记录
     * @param trade 交易记录
     * @return 更新后的交易记录
     */
    Trade update(Trade trade);
}