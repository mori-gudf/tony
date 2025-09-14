package com.tony.trading.controller;

import com.tony.trading.model.AccountBalance;
import com.tony.trading.model.Trade;
import com.tony.trading.service.AccountService;
import com.tony.trading.service.TradeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

/**
 * 主页控制器
 */
@Controller
public class HomeController {

    private final TradeService tradeService;
    private final AccountService accountService;

    @Autowired
    public HomeController(TradeService tradeService, AccountService accountService) {
        this.tradeService = tradeService;
        this.accountService = accountService;
    }

    /**
     * 根路径重定向到/trading
     */
    @GetMapping("/")
    public String redirectToTrading() {
        return "redirect:/trading";
    }
    
    /**
     * 显示主页
     */
    @GetMapping("/trading")
    public String home(Model model) {
        List<Trade> openTrades = tradeService.getAllOpenTrades();
        AccountBalance accountBalance = accountService.getAccountBalance();
        
        // 获取爆仓预警信息
        String liquidationWarnings = tradeService.getAllLiquidationWarnings();
        
        model.addAttribute("openTrades", openTrades);
        model.addAttribute("accountBalance", accountBalance);
        model.addAttribute("liquidationWarnings", liquidationWarnings);
        return "index";
    }

    /**
     * 显示关于页面
     */
    @GetMapping("/about")
    public String about() {
        return "about";
    }

    /**
     * 显示Tony交易心法页面
     */
    @GetMapping("/heart-method")
    public String heartMethod() {
        return "heart-method";
    }
}