package com.tony.trading.model;

/**
 * 交易方向枚举
 */
public enum TradeDirection {
    LONG("做多"),
    SHORT("做空");
    
    private final String description;
    
    TradeDirection(String description) {
        this.description = description;
    }
    
    public String getDescription() {
        return description;
    }
}