package com.tony.trading.controller;

import com.tony.trading.model.Trade;
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

    @Autowired
    public HomeController(TradeService tradeService) {
        this.tradeService = tradeService;
    }

    /**
     * 显示主页
     */
    @GetMapping("/")
    public String home(Model model) {
        List<Trade> openTrades = tradeService.getAllOpenTrades();
        model.addAttribute("openTrades", openTrades);
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