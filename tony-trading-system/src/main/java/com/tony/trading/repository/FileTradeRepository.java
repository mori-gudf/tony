package com.tony.trading.repository;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.tony.trading.model.Trade;
import com.tony.trading.model.TradeStatus;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Repository;

import javax.annotation.PostConstruct;
import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

/**
 * 基于文件的交易记录数据访问实现
 */
@Repository
public class FileTradeRepository implements TradeRepository {

    @Value("${trading.data.path}")
    private String dataPath;

    private final String TRADES_FILE = "trades.json";
    private final ObjectMapper objectMapper;
    private List<Trade> trades;

    public FileTradeRepository() {
        objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        trades = new ArrayList<>();
    }

    @PostConstruct
    public void init() {
        File directory = new File(dataPath);
        if (!directory.exists()) {
            directory.mkdirs();
        }
        loadTrades();
    }

    private void loadTrades() {
        File file = new File(dataPath + "/" + TRADES_FILE);
        if (file.exists()) {
            try {
                trades = objectMapper.readValue(file, new TypeReference<List<Trade>>() {});
            } catch (IOException e) {
                e.printStackTrace();
                trades = new ArrayList<>();
            }
        }
    }

    private void saveTrades() {
        File file = new File(dataPath + "/" + TRADES_FILE);
        try {
            objectMapper.writerWithDefaultPrettyPrinter().writeValue(file, trades);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public Trade save(Trade trade) {
        if (trade.getId() == null) {
            trade.setId(UUID.randomUUID().toString());
        }
        trades.add(trade);
        saveTrades();
        return trade;
    }

    @Override
    public Optional<Trade> findById(String id) {
        return trades.stream()
                .filter(trade -> trade.getId().equals(id))
                .findFirst();
    }

    @Override
    public List<Trade> findAll() {
        return new ArrayList<>(trades);
    }

    @Override
    public List<Trade> findAllOpenTrades() {
        return trades.stream()
                .filter(trade -> trade.getStatus() == TradeStatus.OPEN)
                .collect(Collectors.toList());
    }

    @Override
    public List<Trade> findAllClosedTrades() {
        return trades.stream()
                .filter(trade -> trade.getStatus() == TradeStatus.CLOSED)
                .collect(Collectors.toList());
    }

    @Override
    public void deleteById(String id) {
        trades.removeIf(trade -> trade.getId().equals(id));
        saveTrades();
    }

    @Override
    public Trade update(Trade updatedTrade) {
        for (int i = 0; i < trades.size(); i++) {
            if (trades.get(i).getId().equals(updatedTrade.getId())) {
                trades.set(i, updatedTrade);
                saveTrades();
                return updatedTrade;
            }
        }
        return null;
    }
}