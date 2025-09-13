package com.tony.trading.model;

/**
 * 交易状态枚举
 */
public enum TradeStatus {
    OPEN("持仓中"),
    CLOSED("已平仓"),
    PLANNED("计划中");
    
    private final String description;
    
    TradeStatus(String description) {
        this.description = description;
    }
    
    public String getDescription() {
        return description;
    }
}