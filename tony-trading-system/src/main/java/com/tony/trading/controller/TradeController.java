package com.tony.trading.controller;

import com.tony.trading.model.AccountBalance;
import com.tony.trading.model.SimulatedTrade;
import com.tony.trading.model.Trade;
import com.tony.trading.model.TradingDecision;
import com.tony.trading.service.AccountService;
import com.tony.trading.service.TradeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;

/**
 * 交易控制器
 */
@Controller
@RequestMapping("/trades")
public class TradeController {

    private final TradeService tradeService;
    private final AccountService accountService;

    @Autowired
    public TradeController(TradeService tradeService, AccountService accountService) {
        this.tradeService = tradeService;
        this.accountService = accountService;
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
        AccountBalance accountBalance = accountService.getAccountBalance();
        model.addAttribute("trade", new Trade());
        model.addAttribute("accountBalance", accountBalance);
        return "trades/create";
    }

    /**
     * 处理创建交易请求
     */
    @PostMapping("/create")
    public String createTrade(@ModelAttribute Trade trade, RedirectAttributes redirectAttributes) {
        try {
            // 检查资金是否足够
            if (!accountService.hasEnoughBalance(trade.getPositionSize())) {
                redirectAttributes.addFlashAttribute("error", 
                    "资金不足！可用资金：" + accountService.getAccountBalance().getAvailableBalance() + " U");
                return "redirect:/trades/create";
            }
            
            // 检查Tony心法合规性
            if (!accountService.checkTonyMethodCompliance(trade.getPositionSize())) {
                String advice = accountService.getTonyMethodAdvice(trade.getPositionSize());
                redirectAttributes.addFlashAttribute("error", 
                    "违反Tony心法资金管理原则！\n" + advice);
                return "redirect:/trades/create";
            }
            
            // 开仓扣除资金
            if (!accountService.openPosition(trade)) {
                redirectAttributes.addFlashAttribute("error", "开仓失败，请检查资金和仓位设置");
                return "redirect:/trades/create";
            }
            
            // 创建交易
            tradeService.createTrade(trade);
            
            redirectAttributes.addFlashAttribute("success", 
                "交易创建成功！已扣除资金：" + trade.getPositionSize() + " U");
            
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "创建交易失败：" + e.getMessage());
            return "redirect:/trades/create";
        }
        
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