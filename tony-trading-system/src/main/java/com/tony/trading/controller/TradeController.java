package com.tony.trading.controller;

import com.tony.trading.model.SimulatedTrade;
import com.tony.trading.model.Trade;
import com.tony.trading.model.TradingDecision;
import com.tony.trading.service.TradeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 交易控制器
 */
@Controller
@RequestMapping("/trades")
public class TradeController {

    private final TradeService tradeService;

    @Autowired
    public TradeController(TradeService tradeService) {
        this.tradeService = tradeService;
    }

    /**
     * 显示交易列表页面
     */
    @GetMapping
    public String listTrades(Model model) {
        List<Trade> openTrades = tradeService.getAllOpenTrades();
        List<Trade> closedTrades = tradeService.getAllClosedTrades();
        
        model.addAttribute("openTrades", openTrades);
        model.addAttribute("closedTrades", closedTrades);
        return "trades/list";
    }

    /**
     * 显示创建交易页面
     */
    @GetMapping("/create")
    public String showCreateForm(Model model) {
        model.addAttribute("trade", new Trade());
        return "trades/create";
    }

    /**
     * 处理创建交易请求
     */
    @PostMapping("/create")
    public String createTrade(@ModelAttribute Trade trade) {
        tradeService.createTrade(trade);
        return "redirect:/trades";
    }

    /**
     * 显示交易详情页面
     */
    @GetMapping("/{id}")
    public String viewTrade(@PathVariable String id, Model model) {
        Trade trade = tradeService.getTradeById(id);
        model.addAttribute("trade", trade);
        return "trades/view";
    }

    /**
     * 显示编辑交易页面
     */
    @GetMapping("/{id}/edit")
    public String showEditForm(@PathVariable String id, Model model) {
        Trade trade = tradeService.getTradeById(id);
        model.addAttribute("trade", trade);
        return "trades/edit";
    }

    /**
     * 处理更新交易请求
     */
    @PostMapping("/{id}/edit")
    public String updateTrade(@PathVariable String id, @ModelAttribute Trade trade) {
        trade.setId(id);
        tradeService.updateTrade(trade);
        return "redirect:/trades";
    }

    /**
     * 显示平仓页面
     */
    @GetMapping("/{id}/close")
    public String showCloseForm(@PathVariable String id, Model model) {
        Trade trade = tradeService.getTradeById(id);
        model.addAttribute("trade", trade);
        return "trades/close";
    }

    /**
     * 处理平仓请求
     */
    @PostMapping("/{id}/close")
    public String closeTrade(@PathVariable String id, @RequestParam double exitPrice) {
        tradeService.closeTrade(id, exitPrice);
        return "redirect:/trades";
    }

    /**
     * 处理删除交易请求
     */
    @PostMapping("/{id}/delete")
    public String deleteTrade(@PathVariable String id) {
        tradeService.deleteTrade(id);
        return "redirect:/trades";
    }

    /**
     * 显示更新价格页面
     */
    @GetMapping("/{id}/update-price")
    public String showUpdatePriceForm(@PathVariable String id, Model model) {
        Trade trade = tradeService.getTradeById(id);
        model.addAttribute("trade", trade);
        return "trades/update-price";
    }

    /**
     * 处理更新价格请求
     */
    @PostMapping("/{id}/update-price")
    public String updatePrice(@PathVariable String id, @RequestParam double currentPrice) {
        tradeService.updateTradePnl(id, currentPrice);
        return "redirect:/trades/" + id;
    }

    /**
     * 显示交易决策页面
     */
    @GetMapping("/decision")
    public String showDecisionForm(Model model) {
        model.addAttribute("tradingDecision", new TradingDecision());
        return "trades/decision";
    }

    /**
     * 处理生成交易决策请求
     */
    @PostMapping("/decision")
    public String generateDecision(@ModelAttribute TradingDecision tradingDecision, Model model) {
        TradingDecision decision = tradeService.generateTradingDecision(
                tradingDecision.getSymbol(),
                tradingDecision.getDirection(),
                tradingDecision.getSuggestedEntryPrice(),
                tradingDecision.getSuggestedStopLoss(),
                tradingDecision.getSuggestedTakeProfit()
        );
        model.addAttribute("tradingDecision", decision);
        return "trades/decision-result";
    }

    /**
     * 显示模拟交易页面
     */
    @GetMapping("/simulate")
    public String showSimulateForm(Model model) {
        model.addAttribute("simulatedTrade", new SimulatedTrade());
        return "trades/simulate";
    }

    /**
     * 处理模拟交易请求
     */
    @PostMapping("/simulate")
    public String simulateTrade(@ModelAttribute SimulatedTrade simulatedTrade, Model model) {
        SimulatedTrade result = tradeService.simulateTrade(simulatedTrade);
        model.addAttribute("simulatedTrade", result);
        return "trades/simulate-result";
    }
}